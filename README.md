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

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation & Setup

1. Navigate to the project directory:
```bash
cd house_price_prediction
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model (if not already trained):
```bash
python train_model.py
```

4. Start the Flask application:
```bash
python app.py
```

5. Open your browser and go to:
```
http://localhost:5000
```

## 📁 Project Structure

```
house_price_prediction/
├── app.py                      # Flask application
├── train_model.py              # Model training script
├── test_api.py                 # API testing script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICKSTART.md               # Quick start guide
├── UI_GUIDE.md                 # Detailed UI guide
├── models/                     # Trained model directory
│   ├── house_price_model.pkl   # Trained model
│   └── feature_names.pkl       # Feature names
├── templates/                  # HTML templates
│   └── index.html              # Main UI page
└── static/                     # Static assets
    ├── style.css               # UI styling
    └── script.js               # UI interactivity
```

## 🎨 Web Interface Overview

### Main Sections

**1. Prediction Form (Left Panel)**
- Quick select from 50 dataset samples
- Manual input with validation
- Helpful hints for each feature
- Real-time form updates

**2. Results Display (Right Panel)**
- Large predicted price display
- Total price calculation
- Model confidence metrics
- 5 most similar properties from dataset

**3. Dataset Filters**
- Filter by income level (Low/Medium/High)
- Filter by house age (New/Medium/Old)
- Filter by location (Northern/Central/Southern CA)
- Real-time dataset statistics

**4. Browsable Samples**
- Grid view of filtered samples
- Click to load into prediction form
- Details: income, age, rooms, location, price

For detailed UI guide, see [UI_GUIDE.md](UI_GUIDE.md)

## 🔌 API Endpoints

### Web UI Endpoints

```
GET  /                    Access the web interface
GET  /api/dataset         Get all dataset samples (for UI)
GET  /api/statistics      Get dataset statistics
GET  /api/health         Health check
GET  /api/features       Get required features list
```

### Prediction Endpoints

```
POST /api/predict        Make single prediction
     Body: {"features": [val1, val2, ..., val8]}
     or: {"MedInc": val, "HouseAge": val, ...}

POST /api/predict-batch  Make batch predictions
     Body: {"data": [[val1, ..., val8], [val1, ..., val8]]}
```

### Legacy Endpoints (Backward Compatible)

```
GET  /features           Get required features
POST /predict            Make single prediction
POST /predict-batch      Make batch predictions
GET  /health            Health check
```

## 📋 Features Used

The model uses the California Housing dataset with 8 features:

| Feature | Description | Range |
|---------|-------------|-------|
| **MedInc** | Median income in block group ($10K) | 0.5 - 15.0 |
| **HouseAge** | Median house age (years) | 1 - 52 |
| **AveRooms** | Average rooms per household | 1.0 - 141.0 |
| **AveBedrms** | Average bedrooms per household | 0.33 - 34.07 |
| **Population** | Block group population | 3 - 35,682 |
| **AveOccup** | Average occupancy per household | 0.69 - 55.23 |
| **Latitude** | Block group latitude | 32.54 - 41.95 |
| **Longitude** | Block group longitude | -124.35 - -114.13 |

## 🧪 Testing

### Using the Web UI (Recommended)

1. Open http://localhost:5000
2. Select a sample or enter manual values
3. Click "Predict Price"
4. Explore filters and browse the dataset

### Using Python Scripts

Run the included test script:
```bash
python test_api.py
```

### Using Python Requests

```python
import requests

# Single prediction
url = "http://localhost:5000/api/predict"
data = {
    "features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
}
response = requests.post(url, json=data)
print(response.json())

# Dictionary format
data = {
    "MedInc": 8.3252,
    "HouseAge": 41.0,
    "AveRooms": 6.984127,
    "AveBedrms": 1.023810,
    "Population": 322.0,
    "AveOccup": 2.555556,
    "Latitude": 37.88,
    "Longitude": -122.23
}
response = requests.post(url, json=data)
print(response.json())

# Batch predictions
url = "http://localhost:5000/api/predict-batch"
data = {
    "data": [
        [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23],
        [8.3014, 21.0, 6.238137, 0.971880, 2401.0, 2.109842, 37.86, -122.22]
    ]
}
response = requests.post(url, json=data)
print(response.json())
```

### Using cURL

```bash
# Get dataset statistics
curl http://localhost:5000/api/statistics

# Get features
curl http://localhost:5000/api/features

# Make prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]}'

# Health check
curl http://localhost:5000/api/health
```

## 🛠️ Development

### Training the Model

To retrain the model with different data or parameters:

```bash
python train_model.py
```

This will:
- Load the California Housing dataset
- Split into 80/20 train-test sets
- Train linear regression model
- Evaluate and save model to `models/`
- Display performance metrics

### Project Scripts

- **app.py** - Flask web server
- **train_model.py** - Model training script
- **test_api.py** - Comprehensive API tests
- **quickstart.sh** - Quick start bash script

## 📦 Dependencies

```
Flask>=3.0.0              # Web framework
scikit-learn>=1.5.0       # Machine learning
numpy>=1.26.0             # Numerical computing
pandas>=2.2.0             # Data manipulation
```

See [requirements.txt](requirements.txt) for exact versions.

## 🚀 Production Deployment

### Using Gunicorn

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run production server:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker

Create a Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t house-price-predictor .
docker run -p 5000:5000 house-price-predictor
```

### Best Practices

- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set `debug=False` in Flask
- [ ] Use environment variables for configuration
- [ ] Add input validation and error handling
- [ ] Implement comprehensive logging
- [ ] Use HTTPS/SSL in production
- [ ] Set up monitoring and alerting
- [ ] Implement rate limiting
- [ ] Add database for prediction history (optional)

## 🎯 Use Cases

1. **Real Estate Valuation** - Estimate property values
2. **Market Analysis** - Understand pricing trends
3. **Investment Decisions** - Compare similar properties
4. **Data Exploration** - Learn from the dataset
5. **API Integration** - Use predictions in other apps
6. **ML Education** - Study linear regression models

## 📊 Model Interpretation

- The model explains ~58% of price variance (R² = 0.5758)
- RMSE of 0.7456 means predictions are typically off by ±0.7456 ($74,560)
- Better for bulk estimates than individual high-value properties
- Works well within the training data range

## 🔍 Troubleshooting

**Port 5000 already in use:**
```bash
# On Linux/Mac:
lsof -ti:5000 | xargs kill -9

# On Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Model not found error:**
```bash
# Make sure to train the model first:
python train_model.py
```

**Dependencies not installing:**
```bash
# Update pip and try again:
pip install --upgrade pip
pip install -r requirements.txt
```

## 📚 Additional Resources

- [UI Guide](UI_GUIDE.md) - Detailed web interface documentation
- [Quick Start](QUICKSTART.md) - Getting started guide
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Submit pull requests
- Add new features

## 📞 Support

For issues or questions:
1. Check the [UI_GUIDE.md](UI_GUIDE.md)
2. Review the [QUICKSTART.md](QUICKSTART.md)
3. Run the test script: `python test_api.py`

---

**Built with ❤️ using Flask, scikit-learn, and vanilla JavaScript**

Happy predicting! 🎉
