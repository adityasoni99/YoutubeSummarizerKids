from flow import youtube_summarizer_flow
import ssl
import certifi
import os

# Initialize SSL certificate settings
try:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl._create_default_https_context = lambda: ssl_context
    print("SSL certificates initialized.")
except Exception as e:
    print(f"Warning: SSL certificate initialization failed: {str(e)}")
    print("The program will continue, but you may encounter SSL errors.")
    print("If you do, run: python fix_ssl.py")

def main():
    """Main function to run the YouTube Video Summarizer."""
    print("=" * 80)
    print("🎬 YouTube Video Summarizer for Kids 🎬")
    print("This tool creates a kid-friendly summary of any YouTube video!")
    print("=" * 80)
    
    # Get YouTube URL from user
    youtube_url = input("\n📺 Enter a YouTube video URL: ")
    
    # Initialize shared store
    shared = {
        "youtube_url": youtube_url
    }
    
    # Run the flow
    print("\n🔄 Processing video... This may take a minute or two.")
    youtube_summarizer_flow.run(shared)
    
    # Handle error case
    if "error" in shared:
        print(f"\n❌ Error: {shared['error']}")
        
        # Suggest fixes for common errors
        if "SSL" in shared['error'] or "certificate" in shared['error'].lower():
            print("\n🔧 This appears to be an SSL certificate issue. Try:")
            print("1. Run: python fix_ssl.py")
        
        return
        
    # Success case
    print("\n✅ Summary generated successfully!")
    print(f"📝 Title: {shared['video_info']['title']}")
    print(f"⏱️ Duration: {shared['video_info']['duration']} seconds")
    print(f"📊 Topics identified: {len(shared['topics'])}")
    print(f"🌈 HTML summary saved to: {shared['output_path']}")
    print("\n🔍 Brief summary:")
    print("-" * 60)
    print(shared["summary"])
    print("-" * 60)
    print("\n👉 Open the HTML file to see the complete kid-friendly summary with Q&A!")

if __name__ == "__main__":
    main()
