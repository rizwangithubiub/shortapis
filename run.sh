#!/bin/bash

# URL Shortening Service - Run Script
# This script sets up and runs the URL shortening service

echo "=== URL Shortening Service Setup ==="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting the URL Shortening Service..."
echo "Access the web interface at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "=================================="

python app.py