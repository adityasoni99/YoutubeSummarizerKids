#!/bin/bash

# Create a new conda environment named 'youtube-summarizer'
conda create -n youtube-summarizer python=3.10 -y

# Activate the environment
echo "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate youtube-summarizer

# Install pip packages
echo "Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install pocketflow
python -m pip install youtube-transcript-api
python -m pip install jinja2
python -m pip install validators
python -m pip install pyyaml
python -m pip install google-generativeai
python -m pip install certifi
python -m pip install --upgrade certifi

# Verify installation of critical packages
echo "Verifying installations..."
python -m pip list | grep google-generativeai
python -m pip list | grep certifi

# Create necessary directories
mkdir -p output
mkdir -p downloads

# Run SSL certificate fix script
echo "Fixing SSL certificates..."
python fix_ssl.py

echo "Conda environment 'youtube-summarizer' has been created and dependencies installed!"
echo "To activate this environment, use:"
echo "    conda activate youtube-summarizer"
echo ""
echo "To run the program, execute:"
echo "    python main.py"
