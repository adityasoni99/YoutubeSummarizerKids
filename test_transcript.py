#!/usr/bin/env python
"""
YouTube Transcript Test Script

This script tests the get_transcript function with various YouTube URLs
to verify its functionality and provide diagnostics.
"""

import sys
from utils.get_transcript import get_transcript

def test_transcript(url):
    """Test getting a transcript from a YouTube URL"""
    print(f"\nTesting URL: {url}")
    print("-" * 60)
    
    try:
        info = get_transcript(url)
        if info['title'] == "Video Unavailable":
            print("❌ Failed to get transcript")
            print(f"Error message: {info['transcript']}")
        else:
            print("✅ Successfully retrieved transcript")
            print(f"Title: {info['title']}")
            print(f"Duration: {info['duration']} seconds")
            print(f"Transcript preview: {info['transcript'][:150]}...")
    except Exception as e:
        print(f"❌ Exception occurred: {str(e)}")

def main():
    print("=" * 60)
    print("YouTube Transcript Test Script")
    print("=" * 60)
    
    # List of videos to test (mix of popular videos that likely have transcripts)
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up
        "https://www.youtube.com/watch?v=jNQXAC9IVRw",  # Me at the zoo (first YouTube video)
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # PSY - Gangnam Style
        # Add your own test URLs here
    ]
    
    # If URLs provided as arguments, use those instead
    if len(sys.argv) > 1:
        test_urls = sys.argv[1:]
    
    # Test each URL
    for url in test_urls:
        test_transcript(url)
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    main()
