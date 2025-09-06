# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Start both services
CMD ["/usr/bin/supervisord"]
