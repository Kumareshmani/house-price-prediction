# House Price Prediction Model with Flask

A machine learning project that trains a linear regression model to predict house prices and deploys it via a Flask REST API with a beautiful, interactive web UI.

## ✨ Features

✅ **Interactive Web UI** - Beautiful, user-friendly interface for making predictions  
✅ **Real-time Filtering** - Filter dataset by income, age, and location  
✅ **Quick Sample Selection** - Load pre-existing data with one click  
✅ **Similar Properties Display** - See comparable properties from the dataset  
✅ **Dataset Statistics** - View averages, ranges, and distribution  
✅ **REST API** - Full-featured API for programmatic access  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **No External Dependencies** - Frontend uses vanilla JavaScript  

## 📊 Model Performance

- **RMSE**: 0.7456 (Root Mean Squared Error)
- **R² Score**: 0.5758 (57.58% of variance explained)
- **Dataset**: California Housing (20,640 samples, 8 features)
- **Algorithm**: Linear Regression

## 🚀 Quick Start

## API Endpoints

### 1. Health Check
```
GET /health
```
Check if the API is running and the model is loaded.

### 2. Get Features
```
GET /features
```
Get the list of required features for making predictions.

Example Response:
```json
{
  "features": ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"],
  "feature_count": 8,
  "description": "Provide these features in the same order for predictions"
}
```

### 3. Single Prediction
```
POST /predict
```

**Array Format:**
```json
{
  "features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
}
```

**Dictionary Format:**
```json
{
  "MedInc": 8.3252,
  "HouseAge": 41.0,
  "AveRooms": 6.984127,
  "AveBedrms": 1.023810,
  "Population": 322.0,
  "AveOccup": 2.555556,
  "Latitude": 37.88,
  "Longitude": -122.23
}
```

Example Response:
```json
{
  "prediction": 4.576,
  "features_used": ["MedInc", "HouseAge", "AveRooms", "AveBedrms", "Population", "AveOccup", "Latitude", "Longitude"],
  "status": "success"
}
```

### 4. Batch Predictions
```
POST /predict-batch
```

Request:
```json
{
  "data": [
    [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23],
    [8.3014, 21.0, 6.238137, 0.971880, 2401.0, 2.109842, 37.86, -122.22]
  ]
}
```

Response:
```json
{
  "predictions": [4.576, 4.389],
  "count": 2,
  "status": "success"
}
```

## Features Used

The model uses the California Housing dataset with the following features:
1. **MedInc** - Median income in block group (in $10K)
2. **HouseAge** - Median house age in block group
3. **AveRooms** - Average number of rooms per household
4. **AveBedrms** - Average number of bedrooms per household
5. **Population** - Block group population
6. **AveOccup** - Average occupancy per household
7. **Latitude** - Block group latitude
8. **Longitude** - Block group longitude

## Testing with cURL

```bash
# Health check
curl http://localhost:5000/health

# Get features
curl http://localhost:5000/features

# Single prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'

# Batch prediction
curl -X POST http://localhost:5000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"data": [[8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]]}'
```

## Testing with Python

```python
import requests
import json

# Single prediction
url = "http://localhost:5000/predict"
data = {
    "features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
}
response = requests.post(url, json=data)
print(response.json())

# Batch prediction
url = "http://localhost:5000/predict-batch"
data = {
    "data": [
        [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23],
        [8.3014, 21.0, 6.238137, 0.971880, 2401.0, 2.109842, 37.86, -122.22]
    ]
}
response = requests.post(url, json=data)
print(response.json())
```

## Model Performance

The linear regression model is trained on the California Housing dataset with 80/20 train-test split. Performance metrics (RMSE, R²) will be displayed when running the training script.

## Production Deployment

For production, consider:
- Using a production WSGI server (gunicorn, uWSGI)
- Setting `debug=False` in Flask
- Using environment variables for configuration
- Adding input validation and error handling
- Implementing logging
- Using Docker for containerization
- Setting up monitoring and alerting

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## License

MIT
