"""
Unit tests for model training logic.

These tests validate the ML pipeline independently of the Flask app —
covering data shapes, model fitting, prediction output, and persistence.
"""

import os
import pickle
import tempfile

import numpy as np
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
FEATURE_NAMES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude",
]

N_FEATURES = len(FEATURE_NAMES)


@pytest.fixture(scope="module")
def synthetic_dataset():
    """Return a reproducible synthetic dataset with 8 features."""
    rng = np.random.default_rng(42)
    X = rng.random((200, N_FEATURES))
    # y is a linear combination so a LinearRegression should score ~1.0
    coef = np.array([1.5, -2.0, 0.5, 1.0, -0.5, 2.0, 0.3, -1.2])
    y = X @ coef + 3.0
    return X, y


@pytest.fixture(scope="module")
def trained_model(synthetic_dataset):
    """Return a LinearRegression model trained on synthetic data."""
    X, y = synthetic_dataset
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model, X, y


# ---------------------------------------------------------------------------
# Feature metadata
# ---------------------------------------------------------------------------
class TestFeatureNames:
    def test_feature_count_is_eight(self):
        assert len(FEATURE_NAMES) == 8

    def test_feature_names_are_strings(self):
        assert all(isinstance(f, str) for f in FEATURE_NAMES)

    def test_required_features_present(self):
        required = {"MedInc", "HouseAge", "Latitude", "Longitude"}
        assert required.issubset(set(FEATURE_NAMES))


# ---------------------------------------------------------------------------
# Model training
# ---------------------------------------------------------------------------
class TestModelTraining:
    def test_model_fits_without_error(self, synthetic_dataset):
        X, y = synthetic_dataset
        model = LinearRegression()
        model.fit(X, y)  # should not raise
        assert hasattr(model, "coef_")

    def test_coefficient_shape_matches_features(self, trained_model):
        model, _, _ = trained_model
        assert model.coef_.shape == (N_FEATURES,)

    def test_intercept_is_scalar(self, trained_model):
        model, _, _ = trained_model
        assert model.intercept_.ndim == 0 or isinstance(float(model.intercept_), float)

    def test_r2_near_one_on_linear_data(self, trained_model):
        model, X, y = trained_model
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        r2 = r2_score(y_test, model.predict(X_test))
        assert r2 > 0.99, f"R² should be ~1 on linear data, got {r2:.4f}"

    def test_rmse_is_low_on_linear_data(self, trained_model):
        model, X, y = trained_model
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
        assert rmse < 0.01, f"RMSE should be near 0 on linear data, got {rmse:.6f}"


# ---------------------------------------------------------------------------
# Model predictions
# ---------------------------------------------------------------------------
class TestModelPredictions:
    def test_predict_returns_array(self, trained_model):
        model, X, _ = trained_model
        preds = model.predict(X[:5])
        assert isinstance(preds, np.ndarray)

    def test_predict_output_shape(self, trained_model):
        model, X, _ = trained_model
        preds = model.predict(X[:10])
        assert preds.shape == (10,)

    def test_single_row_prediction_returns_scalar(self, trained_model):
        model, X, _ = trained_model
        pred = model.predict(X[0].reshape(1, -1))
        assert pred.shape == (1,)
        assert isinstance(float(pred[0]), float)

    def test_predictions_are_finite(self, trained_model):
        model, X, _ = trained_model
        preds = model.predict(X)
        assert np.all(np.isfinite(preds)), "All predictions should be finite"

    def test_prediction_wrong_feature_count_raises(self, trained_model):
        model, _, _ = trained_model
        wrong_input = np.array([[1.0, 2.0, 3.0]])  # 3 features instead of 8
        with pytest.raises(ValueError):
            model.predict(wrong_input)


# ---------------------------------------------------------------------------
# Model persistence
# ---------------------------------------------------------------------------
class TestModelPersistence:
    def test_model_saves_and_loads(self, trained_model):
        model, X, _ = trained_model
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            tmp_path = f.name
        try:
            with open(tmp_path, "wb") as f:
                pickle.dump(model, f)
            with open(tmp_path, "rb") as f:
                loaded_model = pickle.load(f)
            np.testing.assert_array_almost_equal(
                model.predict(X[:5]), loaded_model.predict(X[:5])
            )
        finally:
            os.unlink(tmp_path)

    def test_feature_names_save_and_load(self):
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            tmp_path = f.name
        try:
            with open(tmp_path, "wb") as f:
                pickle.dump(FEATURE_NAMES, f)
            with open(tmp_path, "rb") as f:
                loaded = pickle.load(f)
            assert loaded == FEATURE_NAMES
        finally:
            os.unlink(tmp_path)

    def test_loaded_model_predicts_same_shape(self, trained_model):
        model, X, _ = trained_model
        with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as f:
            tmp_path = f.name
        try:
            with open(tmp_path, "wb") as f:
                pickle.dump(model, f)
            with open(tmp_path, "rb") as f:
                loaded = pickle.load(f)
            assert loaded.predict(X).shape == model.predict(X).shape
        finally:
            os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Data validation helpers (mirrors logic in train_model.py)
# ---------------------------------------------------------------------------
class TestDataPreprocessing:
    def test_train_test_split_sizes(self, synthetic_dataset):
        X, y = synthetic_dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        assert len(X_train) == 160
        assert len(X_test) == 40
        assert len(y_train) == 160
        assert len(y_test) == 40

    def test_no_nan_in_synthetic_data(self, synthetic_dataset):
        X, y = synthetic_dataset
        assert not np.any(np.isnan(X))
        assert not np.any(np.isnan(y))

    def test_feature_matrix_shape(self, synthetic_dataset):
        X, _ = synthetic_dataset
        assert X.shape[1] == N_FEATURES
