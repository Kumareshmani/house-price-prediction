# QUICK START GUIDE

## Project Successfully Created! 🎉

Your house price prediction model with Flask deployment is ready to go.

### What was created:

```
house_price_prediction/
├── train_model.py              # Script to train the linear regression model
├── app.py                      # Flask REST API application
├── test_api.py                 # API testing script
├── requirements.txt            # Python dependencies
├── quickstart.sh               # Quick start bash script
├── README.md                   # Full documentation
├── .gitignore                  # Git ignore rules
└── models/                     # Trained model directory
    ├── house_price_model.pkl   # Trained model (READY)
    └── feature_names.pkl       # Feature names (READY)
```

### Model Performance:
- **RMSE**: 0.7456 (Root Mean Squared Error)
- **R² Score**: 0.5758 (57.58% of variance explained)
- **Dataset**: California Housing (20,640 samples)

---

## How to Run

### Option 1: Using the Quick Start Script
```bash
cd house_price_prediction
chmod +x quickstart.sh
./quickstart.sh
```

### Option 2: Manual Setup
```bash
cd house_price_prediction

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Start the Flask application
python app.py
```

The API will start at: **http://localhost:5000**

---

## Testing the API

### Option 1: Using the Test Script
```bash
# In a new terminal
cd house_price_prediction
pip install requests  # if not already installed
python test_api.py
```

### Option 2: Using cURL
```bash
# Check API health
curl http://localhost:5000/health

# Get required features
curl http://localhost:5000/features

# Make a prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'
```

### Option 3: Using Python
```python
import requests

url = "http://localhost:5000/predict"
data = {"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}
response = requests.post(url, json=data)
print(response.json())
```

---

## API Endpoints

1. **GET /health** - Check if API is running
2. **GET /features** - Get required features for predictions
3. **POST /predict** - Make single prediction
4. **POST /predict-batch** - Make multiple predictions

---

## Required Features (in order)
1. MedInc - Median income ($10K)
2. HouseAge - House age (years)
3. AveRooms - Average rooms per household
4. AveBedrms - Average bedrooms per household
5. Population - Population
6. AveOccup - Average occupancy
7. Latitude - Geographic latitude
8. Longitude - Geographic longitude

---

## Next Steps

### For Development:
- Modify `train_model.py` to use your own dataset
- Add data validation in `app.py`
- Implement authentication if needed
- Add logging and monitoring

### For Production:
- Install Gunicorn: `pip install gunicorn`
- Run with: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
- Containerize with Docker
- Deploy to cloud (AWS, GCP, Azure, etc.)

---

## Documentation
See [README.md](README.md) for full API documentation and examples.

---

Enjoy your ML deployment! 🚀
