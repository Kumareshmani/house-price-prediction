import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os

# Load dataset (using California Housing dataset as an example)
from sklearn.datasets import fetch_california_housing

print("Loading data...")
housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target, name='Price')

print(f"Dataset shape: {X.shape}")
print(f"Features: {list(X.columns)}")

# Split the data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train the model
print("\nTraining linear regression model...")
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Performance:")
print(f"  RMSE: {rmse:.4f}")
print(f"  R² Score: {r2:.4f}")

# Save the model
model_path = 'models/house_price_model.pkl'
os.makedirs('models', exist_ok=True)

with open(model_path, 'wb') as f:
    pickle.dump(model, f)

print(f"\nModel saved to {model_path}")

# Save feature names for the Flask app
with open('models/feature_names.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

print("Feature names saved.")
