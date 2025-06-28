#!/bin/bash

# Install pip packages
echo "Installing dependencies..."
pip install --upgrade pip
pip install pocketflow
pip install youtube-transcript-api
pip install pytube
pip install jinja2
pip install validators
pip install pyyaml
pip install google-generativeai
pip install certifi --upgrade

# Verify installation of critical packages
echo "Verifying installations..."
pip list | grep google-generativeai

# Create necessary directories
mkdir -p output
mkdir -p downloads

# Run SSL certificate fix script
echo "Fixing SSL certificates..."
python fix_ssl.py

echo "Dependencies installed successfully!"
echo ""
echo "Make sure to set your GEMINI_API_KEY environment variable:"
echo "    export GEMINI_API_KEY=your-api-key-here"
echo ""
echo "To run the program, execute:"
echo "    python main.py"
