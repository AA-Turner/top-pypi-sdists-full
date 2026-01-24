"""Basic usage example for Cleanvoice Python SDK."""

import os
from cleanvoice import Cleanvoice

def main():
    # Initialize SDK with your API key
    cv = Cleanvoice({
        'api_key': 'your-api-key-here'  # Replace with your actual API key
    })
    
    # Example 1: Processing with URL
    print("=== Processing audio from URL ===")
    
    result = cv.process(
        "https://example.com/sample-audio.mp3",  # Replace with your audio URL
        {
            'fillers': True,        # Remove filler sounds
            'normalize': True,      # Normalize audio levels
            'remove_noise': True,   # Remove background noise
            'transcription': True,  # Generate transcript
        }
    )
    
    print(f"✅ Processing complete!")
    print(f"📁 Download URL: {result.audio.url}")
    print(f"📊 Statistics: {result.audio.statistics}")
    
    if result.transcript:
        print(f"📝 Transcript: {result.transcript.text[:100]}...")
    
    # Example 2: Upload and process local file
    print("\n=== Processing local file (with upload) ===")
    
    local_file = "path/to/your/audio.mp3"  # Replace with your local file path
    
    if os.path.exists(local_file):
        try:
            # Option A: Upload first, then process
            print("Uploading file...")
            uploaded_url = cv.upload_file(local_file)
            print(f"File uploaded: {uploaded_url}")
            
            result = cv.process(uploaded_url, {'fillers': True})
            print(f"✅ Processing complete!")
            
            # Option B: Process local file directly (automatic upload)
            print("Processing local file directly...")
            result = cv.process(local_file, {
                'fillers': True,
                'transcription': True
            })
            print(f"✅ Direct processing complete!")
            
            # Download the processed file
            print("Downloading processed file...")
            downloaded_path = cv.download_file(result.audio.url, "downloaded_audio.mp3")
            print(f"📁 File downloaded to: {downloaded_path}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print(f"Local file not found: {local_file}")
        print("Please update the file path or use the URL example above.")
    
    # Example 3: Process and download in one step
    print("\n=== One-Step Process and Download ===")
    print("Using process_and_download for convenience...")
    
    try:
        # This would process a URL and download the result automatically
        # result, downloaded_path = cv.process_and_download(
        #     "https://example.com/sample-audio.mp3",
        #     "output.mp3",
        #     {"fillers": True, "normalize": True}
        # )
        # print(f"✅ Processed and saved to: {downloaded_path}")
        print("(Commented out - uncomment with a real URL)")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()