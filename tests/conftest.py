"""
Pytest configuration and shared fixtures.

Creates a minimal trained model before the app module is imported,
since app.py loads the model at module level.
"""

import os
import sys
import pickle
import numpy as np
import pytest
from sklearn.linear_model import LinearRegression

# Ensure the project root is on sys.path so `import app` works
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def _ensure_test_model() -> None:
    """Create a minimal trained model if one does not already exist."""
    models_dir = os.path.join(PROJECT_ROOT, "models")
    model_path = os.path.join(models_dir, "house_price_model.pkl")
    features_path = os.path.join(models_dir, "feature_names.pkl")

    if os.path.exists(model_path) and os.path.exists(features_path):
        return  # Real model already present (e.g., trained in CI before pytest)

    os.makedirs(models_dir, exist_ok=True)

    feature_names = [
        "MedInc", "HouseAge", "AveRooms", "AveBedrms",
        "Population", "AveOccup", "Latitude", "Longitude",
    ]

    # Minimal synthetic dataset that mirrors California Housing feature order
    X = np.array([
        [8.3252, 41.0, 6.984127, 1.023810,  322.0, 2.555556, 37.88, -122.23],
        [8.3014, 21.0, 6.238137, 0.971880, 2401.0, 2.109842, 37.86, -122.22],
        [7.2574, 52.0, 8.288136, 1.081081, 1496.0, 2.802198, 37.85, -122.24],
        [5.6431, 52.0, 5.817352, 1.073059,  558.0, 2.547945, 37.85, -122.25],
        [3.8462, 52.0, 6.281853, 1.081081,  565.0, 2.181467, 37.85, -122.25],
        [4.0368, 52.0, 4.761658, 1.103627,  413.0, 2.139896, 37.85, -122.25],
        [3.6591, 52.0, 4.931907, 0.951362, 1094.0, 2.128405, 37.84, -122.25],
        [3.1200, 52.0, 4.797527, 1.061824, 1157.0, 1.788253, 37.84, -122.25],
        [2.0804, 42.0, 4.294118, 1.117647, 1206.0, 2.026891, 37.84, -122.26],
        [3.6912, 52.0, 4.970588, 0.990196, 1551.0, 2.172269, 37.84, -122.25],
    ])
    y = np.array([4.526, 3.585, 3.521, 3.413, 3.422, 2.697, 2.992, 2.414, 2.267, 2.611])

    model = LinearRegression()
    model.fit(X, y)

    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(features_path, "wb") as f:
        pickle.dump(feature_names, f)


# ---------------------------------------------------------------------------
# Bootstrap: model must exist BEFORE app.py is imported (it loads at module level)
# ---------------------------------------------------------------------------
_ensure_test_model()

# Set cwd to project root so app.py's relative model paths resolve correctly
os.chdir(PROJECT_ROOT)

from app import app as flask_app  # noqa: E402 – intentional late import


@pytest.fixture(scope="session")
def app():
    flask_app.config["TESTING"] = True
    yield flask_app


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
