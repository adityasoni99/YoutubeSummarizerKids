<h1 align="center">YouTube Video Summarizer for Kids</h1>

<p align="center">
  <a href="https://github.com/The-Pocket/PocketFlow" target="_blank">
    <img 
      src="./assets/banner.png" width="800"
    />
  </a>
</p>

## Overview

This project creates kid-friendly summaries of YouTube videos, making complex content accessible to children. The tool:

1. Takes a YouTube video URL as input
2. Extracts key topics from the video's transcript
3. Generates simple Q&A pairs for each topic
4. Explains everything in language a 5-year-old can understand
5. Creates a beautiful HTML page to visualize the summary

## Features

- **Topic Extraction**: Identifies the main themes and topics discussed in the video
- **Child-Friendly Explanations**: Simplifies complex concepts with analogies and simple vocabulary
- **Interactive Q&A**: Generates questions and answers to help understand each topic
- **Collapsible Sections**: Makes Q&A sections expandable/collapsible for better readability
- **Visual Presentation**: Creates an engaging, colorful HTML summary

## Installation

### Option 1: Using Conda (Recommended)

1. Clone this repository
2. Run the setup script to create a conda environment with all dependencies:
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```
   
   Alternatively, you can use the environment.yml file:
   ```bash
   conda env create -f environment.yml
   ```

3. Activate the conda environment:
   ```bash
   conda activate youtube-summarizer
   ```
   
4. Verify that the Google Generative AI package is installed:
   ```bash
   pip list | grep google-generativeai
   ```
   
   If it's not installed, install it manually:
   ```bash
   pip install google-generativeai
   ```
   
5. Set up your Google Gemini API key as an environment variable:
   ```bash
   export GEMINI_API_KEY=your-api-key
   ```
   See `env_setup.md` for detailed instructions.

### Option 2: Using Pip

1. Clone this repository
2. Run the installation script:
   ```bash
   chmod +x install_dependencies.sh
   ./install_dependencies.sh
   ```
   
   Or install the packages manually:
   ```bash
   pip install -r requirements.txt
   ```
   
3. Verify that the Google Generative AI package is installed:
   ```bash
   pip list | grep google-generativeai
   ```
   
   If it's not installed, install it manually:
   ```bash
   pip install google-generativeai
   ```
   
4. Set up your Google Gemini API key as an environment variable:
   ```bash
   export GEMINI_API_KEY=your-api-key
   ```
   See `env_setup.md` for detailed instructions.

## Usage

Run the main script:
```
python main.py
```

Enter a YouTube URL when prompted, and the tool will:
1. Validate the URL
2. Extract the transcript
3. Process the content
4. Generate a kid-friendly summary
5. Save an HTML file with the results

## Project Structure

- `main.py`: Entry point for the application
- `flow.py`: Defines the flow of nodes for processing
- `nodes.py`: Contains all node implementations
- `utils/`: Utility functions for various tasks
- `docs/design.md`: Detailed project design documentation

## Troubleshooting

### "No module named 'google'" Error

If you encounter this error:
```
ModuleNotFoundError: No module named 'google'
```

Run the fix script:
```bash
chmod +x fix_google_module.sh
./fix_google_module.sh
```

Or install the package manually:
```bash
pip install google-generativeai
```

### API Key Issues

If you encounter errors related to the Gemini API key:
1. Make sure you've set the environment variable correctly:
   ```bash
   export GEMINI_API_KEY=your-api-key
   ```
2. Verify it's set by running:
   ```bash
   echo $GEMINI_API_KEY
   ```
3. If needed, get a new API key from [Google AI Studio](https://makersuite.google.com/)

### YouTube API Restrictions

If you encounter errors like `HTTP Error 400: Bad Request` when trying to access YouTube:

1. This is a common issue due to YouTube API restrictions or rate limiting.
2. The tool implements several fallback mechanisms to still get the transcript and basic video information.
3. You might see warnings like `Warning: Could not fetch detailed video info`, but the tool should still work.
4. If the tool can't get any transcript data, try these tips:
   - Try a different YouTube video (some videos don't have transcripts)
   - Wait a few minutes and try again (YouTube has rate limits)
   - Ensure you have a stable internet connection

If you want to test the transcript functionality directly, run:
```bash
python test_transcript.py
```

### SSL Certificate Issues (Common on macOS)

If you encounter SSL certificate verification errors:

1. Run the comprehensive SSL fix script:
   ```bash
   python fix_ssl.py
   ```
   
   This script will:
   - Test your SSL connections
   - Update the certifi package
   - Apply macOS-specific fixes if needed
   - Set up environment variables
   - Provide code fixes for SSL issues

2. For macOS users, you may need to run the Certificate Installation Command:
   ```bash
   /Applications/Python 3.x/Install Certificates.command
   ```
   (Replace '3.x' with your Python version)

## Built With

- [Pocket Flow](https://github.com/The-Pocket/PocketFlow) - A minimalist LLM framework
- [Google Gemini API](https://ai.google.dev/) - For AI text generation
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) - For fetching video transcripts and metadata
- [Jinja2](https://jinja.palletsprojects.com/) - For HTML templating
