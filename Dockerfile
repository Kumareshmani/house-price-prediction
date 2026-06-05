FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies (gunicorn is already in requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Train the model and bake it into the image
RUN python train_model.py

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
