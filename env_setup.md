# Setting Up Environment Variables

To run this project, you need to set up an environment variable for the Google Gemini API key.

## Getting a Gemini API Key

If you don't already have a Gemini API key:

1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Sign in with your Google account
3. Create a new API key or use an existing one
4. Copy the API key for use in the next step

## Setting the Environment Variable

### On macOS/Linux:

```bash
# In your terminal, run:
export GEMINI_API_KEY=your-api-key-here

# To make it permanent, add it to your shell profile file:
echo 'export GEMINI_API_KEY=your-api-key-here' >> ~/.zshrc  # For zsh
# OR
echo 'export GEMINI_API_KEY=your-api-key-here' >> ~/.bash_profile  # For bash
```

### On Windows:

```bash
# In Command Prompt:
set GEMINI_API_KEY=your-api-key-here

# In PowerShell:
$env:GEMINI_API_KEY = "your-api-key-here"

# To set it permanently via System Properties:
# 1. Search for "Environment Variables" in the Start menu
# 2. Click "Edit the system environment variables"
# 3. Click "Environment Variables"
# 4. Add a new User variable with:
#    - Name: GEMINI_API_KEY
#    - Value: your-api-key-here
```

## Testing the Configuration

You can test if your API key is properly set up by running:

```bash
python -c "import os; print('Gemini API Key is set' if os.environ.get('GEMINI_API_KEY') else 'Gemini API Key is NOT set')"
```

If the key is properly set, you should see "Gemini API Key is set" as the output.

## Fixing SSL Certificate Issues (Common on macOS)

Python on macOS often has issues with SSL certificate verification when making HTTPS requests. Here's how to fix them:

### Option 1: Run the Comprehensive SSL Fix Script

We've included a comprehensive SSL fix script that handles certificate issues:

```bash
# Run the all-in-one SSL fix script
python fix_ssl.py
```

This script will:
- Test your SSL connections
- Update the certifi package
- Apply macOS-specific fixes if needed
- Set up environment variables
- Provide code fixes for persistent issues

### Option 2: Manual Certificate Installation

If you're using Python installed via the official installer on macOS:

```bash
# Find your Python version
python --version  # For example, Python 3.9

# Run the certificate installer for your version
/Applications/Python\ 3.9/Install\ Certificates.command
```

### Verification

To verify your SSL certificate setup is working:

```bash
python -c "import ssl; import urllib.request; print('SSL works!' if urllib.request.urlopen('https://www.google.com').getcode() == 200 else 'SSL still has issues')"
```
