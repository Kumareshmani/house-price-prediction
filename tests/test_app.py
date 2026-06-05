"""
Unit tests for the House Price Prediction Flask API (app.py).

Covers:
  - GET  /                     – home page
  - GET  /api/health            – health check
  - GET  /api/features          – feature metadata
  - GET  /api/statistics        – dataset statistics
  - GET  /api/dataset           – dataset samples
  - POST /api/predict           – single prediction (array & dict formats)
  - POST /api/predict-batch     – batch predictions
"""

import json
import pytest


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------
class TestHomeEndpoint:
    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_html(self, client):
        response = client.get("/")
        assert b"html" in response.data.lower()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------
class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_status_healthy(self, client):
        data = json.loads(client.get("/api/health").data)
        assert data["status"] == "healthy"

    def test_health_model_loaded_true(self, client):
        data = json.loads(client.get("/api/health").data)
        assert data["model_loaded"] is True


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------
class TestFeaturesEndpoint:
    def test_features_returns_200(self, client):
        assert client.get("/api/features").status_code == 200

    def test_features_count_is_eight(self, client):
        data = json.loads(client.get("/api/features").data)
        assert data["feature_count"] == 8

    def test_features_list_matches_california_housing(self, client):
        expected = [
            "MedInc", "HouseAge", "AveRooms", "AveBedrms",
            "Population", "AveOccup", "Latitude", "Longitude",
        ]
        data = json.loads(client.get("/api/features").data)
        assert data["features"] == expected

    def test_features_has_description(self, client):
        data = json.loads(client.get("/api/features").data)
        assert "description" in data


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
class TestStatisticsEndpoint:
    def test_statistics_returns_200(self, client):
        assert client.get("/api/statistics").status_code == 200

    def test_statistics_contains_required_fields(self, client):
        data = json.loads(client.get("/api/statistics").data)
        for field in ("total_samples", "avg_price", "min_price", "max_price", "std_price", "median_price"):
            assert field in data, f"Missing field: {field}"

    def test_statistics_values_are_numeric(self, client):
        data = json.loads(client.get("/api/statistics").data)
        assert isinstance(data["avg_price"], float)
        assert isinstance(data["total_samples"], int)

    def test_statistics_min_lte_max(self, client):
        data = json.loads(client.get("/api/statistics").data)
        assert data["min_price"] <= data["max_price"]


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------
class TestDatasetEndpoint:
    def test_dataset_returns_200(self, client):
        assert client.get("/api/dataset").status_code == 200

    def test_dataset_has_samples_list(self, client):
        data = json.loads(client.get("/api/dataset").data)
        assert "samples" in data
        assert isinstance(data["samples"], list)

    def test_dataset_limit_param_respected(self, client):
        data = json.loads(client.get("/api/dataset?limit=10").data)
        assert len(data["samples"]) <= 10

    def test_dataset_sample_has_price_key(self, client):
        data = json.loads(client.get("/api/dataset?limit=1").data)
        assert "price" in data["samples"][0]


# ---------------------------------------------------------------------------
# Single Predict
# ---------------------------------------------------------------------------
VALID_FEATURES_ARRAY = [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
VALID_FEATURES_DICT = {
    "MedInc": 8.3252, "HouseAge": 41.0, "AveRooms": 6.984127,
    "AveBedrms": 1.023810, "Population": 322.0, "AveOccup": 2.555556,
    "Latitude": 37.88, "Longitude": -122.23,
}


class TestPredictEndpoint:
    def test_predict_array_format_returns_200(self, client):
        response = client.post("/api/predict", json={"features": VALID_FEATURES_ARRAY})
        assert response.status_code == 200

    def test_predict_array_format_returns_float(self, client):
        data = json.loads(client.post("/api/predict", json={"features": VALID_FEATURES_ARRAY}).data)
        assert isinstance(data["prediction"], float)
        assert data["status"] == "success"

    def test_predict_array_format_lists_features_used(self, client):
        data = json.loads(client.post("/api/predict", json={"features": VALID_FEATURES_ARRAY}).data)
        assert "features_used" in data
        assert len(data["features_used"]) == 8

    def test_predict_dict_format_returns_200(self, client):
        response = client.post("/api/predict", json=VALID_FEATURES_DICT)
        assert response.status_code == 200

    def test_predict_dict_format_returns_float(self, client):
        data = json.loads(client.post("/api/predict", json=VALID_FEATURES_DICT).data)
        assert isinstance(data["prediction"], float)
        assert data["status"] == "success"

    def test_predict_array_and_dict_return_same_value(self, client):
        r_arr = json.loads(client.post("/api/predict", json={"features": VALID_FEATURES_ARRAY}).data)
        r_dict = json.loads(client.post("/api/predict", json=VALID_FEATURES_DICT).data)
        assert abs(r_arr["prediction"] - r_dict["prediction"]) < 1e-6

    def test_predict_too_few_features_returns_400(self, client):
        response = client.post("/api/predict", json={"features": [8.3252, 41.0]})
        assert response.status_code == 400
        assert "error" in json.loads(response.data)

    def test_predict_missing_dict_key_returns_400(self, client):
        partial = {"MedInc": 8.3252}  # 7 features missing
        response = client.post("/api/predict", json=partial)
        assert response.status_code == 400
        assert "error" in json.loads(response.data)

    def test_predict_empty_json_object_returns_400(self, client):
        # {} is falsy in Python, so the `if not data` guard fires → 400
        response = client.post("/api/predict", json={})
        assert response.status_code == 400
        assert "error" in json.loads(response.data)

    def test_predict_wrong_feature_count_error_message(self, client):
        data = json.loads(
            client.post("/api/predict", json={"features": [1.0, 2.0, 3.0]}).data
        )
        assert "8" in data["error"]  # message should mention expected count


# ---------------------------------------------------------------------------
# Batch Predict
# ---------------------------------------------------------------------------
BATCH_PAYLOAD = {
    "data": [
        [8.3252, 41.0, 6.984127, 1.023810,  322.0, 2.555556, 37.88, -122.23],
        [8.3014, 21.0, 6.238137, 0.971880, 2401.0, 2.109842, 37.86, -122.22],
        [7.2574, 52.0, 8.288136, 1.081081, 1496.0, 2.802198, 37.85, -122.24],
    ]
}


class TestBatchPredictEndpoint:
    def test_batch_predict_returns_200(self, client):
        assert client.post("/api/predict-batch", json=BATCH_PAYLOAD).status_code == 200

    def test_batch_predict_returns_correct_count(self, client):
        data = json.loads(client.post("/api/predict-batch", json=BATCH_PAYLOAD).data)
        assert data["count"] == 3
        assert len(data["predictions"]) == 3

    def test_batch_predict_status_success(self, client):
        data = json.loads(client.post("/api/predict-batch", json=BATCH_PAYLOAD).data)
        assert data["status"] == "success"

    def test_batch_predict_single_row(self, client):
        payload = {"data": [VALID_FEATURES_ARRAY]}
        data = json.loads(client.post("/api/predict-batch", json=payload).data)
        assert data["count"] == 1
        assert isinstance(data["predictions"][0], float)

    def test_batch_predict_matches_single_predict(self, client):
        """Batch result for one row should match single-predict result."""
        batch_data = json.loads(
            client.post("/api/predict-batch", json={"data": [VALID_FEATURES_ARRAY]}).data
        )
        single_data = json.loads(
            client.post("/api/predict", json={"features": VALID_FEATURES_ARRAY}).data
        )
        assert abs(batch_data["predictions"][0] - single_data["prediction"]) < 1e-6

    def test_batch_predict_wrong_feature_count_returns_400(self, client):
        payload = {"data": [[8.3252, 41.0]]}  # Only 2 features
        response = client.post("/api/predict-batch", json=payload)
        assert response.status_code == 400

    def test_batch_predict_missing_data_key_returns_error(self, client):
        response = client.post("/api/predict-batch", json={})
        data = json.loads(response.data)
        assert "error" in data
