#!/bin/bash

# Quick Start Script for House Price Prediction API

echo "=========================================="
echo "House Price Prediction - Quick Start"
echo "=========================================="
echo

# Check if we're in the right directory
if [ ! -f "train_model.py" ]; then
    echo "Error: Please run this script from the house_price_prediction directory"
    exit 1
fi

# Install dependencies
echo "Step 1: Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo

# Train the model
echo "Step 2: Training the model..."
python train_model.py
echo "✓ Model trained"
echo

# Start Flask app
echo "Step 3: Starting Flask application..."
echo "The API will be available at http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo
python app.py
