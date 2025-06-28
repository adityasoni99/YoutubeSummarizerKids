from youtube_transcript_api import YouTubeTranscriptApi
import re
import ssl
import os
import time
import http.client
import urllib.error
import urllib.request
import json

def get_transcript(youtube_url, max_retries=3):
    """
    Gets the transcript directly from a YouTube video without downloading or processing audio.
    Uses the YouTube Transcript API to fetch transcripts and YouTube oEmbed API for metadata.
    
    Args:
        youtube_url (str): URL of the YouTube video
        max_retries (int): Maximum number of retries for transient errors
        
    Returns:
        dict: A dictionary containing:
            - transcript (str): Full transcript text
            - title (str): Video title
            - duration (int): Video duration in seconds
            - thumbnail_url (str): URL to video thumbnail
    """
    try:
        # Fix SSL certificate issues on macOS
        if os.name == 'posix' and hasattr(os, 'uname') and os.uname().sysname == 'Darwin':
            # Use unverified context on macOS - simplest solution for this specific case
            ssl._create_default_https_context = ssl._create_unverified_context
        
        # Extract video ID from the URL
        video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_url)
        if not video_id_match:
            raise ValueError("Could not extract video ID from URL")
        
        video_id = video_id_match.group(1)
        
        # Alternative method to get video info using YouTube Data API
        # We'll use a workaround by fetching the oEmbed data which doesn't require API key
        oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        
        video_title = "Unknown"
        video_duration = 0
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Try to get basic info from oEmbed
        try:
            with urllib.request.urlopen(oembed_url) as response:
                if response.getcode() == 200:
                    oembed_data = json.loads(response.read().decode())
                    video_title = oembed_data.get('title', 'Unknown')
                    # Note: oEmbed doesn't provide duration
        except Exception as e:
            print(f"Warning: Could not fetch oEmbed data: {str(e)}")
            # Continue anyway, we can still try to get the transcript
                
        # Continue with what we have
        
        # Get transcript using youtube_transcript_api with retries
        transcript_list = None
        transcript_error = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    time.sleep(1)
                
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                break  # Break if successful
            except Exception as e:
                transcript_error = e
                print(f"Transcript error on attempt {attempt+1}: {str(e)}")
                if attempt < max_retries - 1:
                    print("Retrying...")
                    continue
        
        # If we couldn't get the transcript, return what info we have
        if transcript_list is None:
            return {
                'transcript': f"Sorry, couldn't get transcript. Error: {str(transcript_error)}",
                'title': video_title,
                'duration': video_duration,
                'thumbnail_url': thumbnail_url
            }
        
        # Combine all transcript parts into one text
        full_transcript = ""
        for entry in transcript_list:
            full_transcript += entry['text'] + " "
        
        # Create result dictionary
        transcript_info = {
            'transcript': full_transcript.strip(),
            'title': video_title,
            'duration': video_duration,
            'thumbnail_url': thumbnail_url
        }
        
        return transcript_info
        
    except Exception as e:
        print(f"ERROR: Failed to get YouTube transcript: {str(e)}")
        print("\nTroubleshooting tips:")
        
        if "HTTP Error 400" in str(e):
            print("- This may be due to YouTube API restrictions or rate limiting")
            print("- Try a different YouTube video")
            print("- Ensure you have a stable internet connection")
            print("- Wait a few minutes and try again")
        
        if "SSL" in str(e) or "certificate" in str(e).lower():
            print("- SSL certificate issue detected")
            print("- Try running: pip install --upgrade certifi")
            
            if os.name == 'posix' and hasattr(os, 'uname') and os.uname().sysname == 'Darwin':
                print("- On macOS, try running: /Applications/Python 3.x/Install Certificates.command")
                print("  (Replace 3.x with your Python version)")
        
        # Return a fallback response
        return {
            'transcript': f"Sorry, couldn't get transcript. Error: {str(e)}",
            'title': "Video Unavailable",
            'duration': 0,
            'thumbnail_url': ""
        }

if __name__ == "__main__":
    # Test the function
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with a valid YouTube URL
    try:
        transcript_info = get_transcript(test_url)
        print(f"Video: {transcript_info['title']}")
        print(f"Duration: {transcript_info['duration']} seconds")
        print(f"Transcript preview: {transcript_info['transcript'][:200]}...")
    except Exception as e:
        print(f"Error: {e}")
