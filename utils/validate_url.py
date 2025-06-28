import validators
import re

def validate_url(url):
    """
    Validates if a URL is a valid YouTube video URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if valid, False otherwise
            - error_message (str): Error message if invalid, None otherwise
    """
    # Check if it's a valid URL
    if not validators.url(url):
        return False, "The provided URL is not valid"
    
    # Check if it's a YouTube URL
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11}).*$'
    match = re.match(youtube_regex, url)
    
    if not match:
        return False, "The URL is not a valid YouTube video URL"
    
    # Extract video ID
    video_id = match.group(4)
    
    if not video_id or len(video_id) != 11:
        return False, "Could not extract a valid YouTube video ID"
    
    return True, None

if __name__ == "__main__":
    # Test cases
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Valid
        "https://youtu.be/dQw4w9WgXcQ",                 # Valid
        "https://www.youtube.com/playlist?list=123456",  # Invalid (not a video)
        "https://example.com",                          # Invalid (not YouTube)
        "not a url"                                     # Invalid (not a URL)
    ]
    
    for url in test_urls:
        is_valid, error = validate_url(url)
        if is_valid:
            print(f"✅ Valid: {url}")
        else:
            print(f"❌ Invalid: {url} - {error}")
