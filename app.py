from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
import os
from sklearn.datasets import fetch_california_housing

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load the trained model and feature names
MODEL_PATH = 'models/house_price_model.pkl'
FEATURES_PATH = 'models/feature_names.pkl'

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Please run train_model.py first.")

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

with open(FEATURES_PATH, 'rb') as f:
    feature_names = pickle.load(f)

# Load the dataset for display
print("Loading dataset for UI...")
housing = fetch_california_housing()
X = pd.DataFrame(housing.data, columns=housing.feature_names)
y = pd.Series(housing.target, name='Price')

print(f"Model loaded successfully!")
print(f"Features: {feature_names}")
print(f"Dataset loaded: {X.shape[0]} samples")


@app.route('/', methods=['GET'])
def home():
    """Serve the main UI page."""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'model_loaded': True})


@app.route('/api/features', methods=['GET'])
def get_features():
    """Get the list of required features for predictions."""
    return jsonify({
        'features': feature_names,
        'feature_count': len(feature_names),
        'description': 'Provide these features in the same order for predictions'
    })


@app.route('/api/dataset', methods=['GET'])
def get_dataset():
    """Get the dataset samples for UI display."""
    samples = []
    for idx, row in X.iterrows():
        sample = dict(zip(feature_names, row.values))
        sample['price'] = y.iloc[idx]
        samples.append(sample)
    
    return jsonify({
        'samples': samples,
        'total': len(samples)
    })


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get dataset statistics."""
    return jsonify({
        'total_samples': len(y),
        'avg_price': float(y.mean()),
        'min_price': float(y.min()),
        'max_price': float(y.max()),
        'std_price': float(y.std()),
        'median_price': float(y.median())
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Make a prediction based on input features.
    
    Expected JSON format:
    {
        "features": [value1, value2, ..., value8]
    }
    or
    {
        "MedInc": value,
        "HouseAge": value,
        ...
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Handle both array and dictionary input
        if 'features' in data:
            # Array format
            features = np.array(data['features']).reshape(1, -1)
            if len(data['features']) != len(feature_names):
                return jsonify({
                    'error': f'Expected {len(feature_names)} features, got {len(data["features"])}'
                }), 400
        else:
            # Dictionary format
            features = []
            for feature in feature_names:
                if feature not in data:
                    return jsonify({
                        'error': f'Missing feature: {feature}'
                    }), 400
                features.append(data[feature])
            features = np.array(features).reshape(1, -1)
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        return jsonify({
            'prediction': float(prediction),
            'features_used': feature_names,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/predict-batch', methods=['POST'])
def predict_batch():
    """
    Make predictions for multiple samples.
    
    Expected JSON format:
    {
        "data": [
            [value1, value2, ..., value8],
            [value1, value2, ..., value8],
            ...
        ]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided. Use format: {"data": [[...], [...]]}'})
        
        features = np.array(data['data'])
        
        if features.shape[1] != len(feature_names):
            return jsonify({
                'error': f'Expected {len(feature_names)} features per sample, got {features.shape[1]}'
            }), 400
        
        predictions = model.predict(features)
        
        return jsonify({
            'predictions': predictions.tolist(),
            'count': len(predictions),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Backward compatibility endpoints (without /api/ prefix)
@app.route('/predict', methods=['POST'])
def predict_legacy():
    """Legacy endpoint - redirects to new API."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        if 'features' in data:
            features = np.array(data['features']).reshape(1, -1)
            if len(data['features']) != len(feature_names):
                return jsonify({
                    'error': f'Expected {len(feature_names)} features, got {len(data["features"])}'
                }), 400
        else:
            features = []
            for feature in feature_names:
                if feature not in data:
                    return jsonify({
                        'error': f'Missing feature: {feature}'
                    }), 400
                features.append(data[feature])
            features = np.array(features).reshape(1, -1)
        
        prediction = model.predict(features)[0]
        
        return jsonify({
            'prediction': float(prediction),
            'features_used': feature_names,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/features', methods=['GET'])
def get_features_legacy():
    """Legacy endpoint - redirects to new API."""
    return jsonify({
        'features': feature_names,
        'feature_count': len(feature_names),
        'description': 'Provide these features in the same order for predictions'
    })


@app.route('/predict-batch', methods=['POST'])
def predict_batch_legacy():
    """Legacy endpoint - redirects to new API."""
    try:
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({'error': 'No data provided. Use format: {"data": [[...], [...]]}'})
        
        features = np.array(data['data'])
        
        if features.shape[1] != len(feature_names):
            return jsonify({
                'error': f'Expected {len(feature_names)} features per sample, got {features.shape[1]}'
            }), 400
        
        predictions = model.predict(features)
        
        return jsonify({
            'predictions': predictions.tolist(),
            'count': len(predictions),
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
