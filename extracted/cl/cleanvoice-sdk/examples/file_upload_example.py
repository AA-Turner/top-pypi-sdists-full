#!/usr/bin/env python3
"""Example demonstrating file upload functionality with Cleanvoice SDK."""

import os
import sys
from pathlib import Path

# Add the src directory to the path to import cleanvoice
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cleanvoice import Cleanvoice


def main():
    """Demonstrate file upload functionality."""
    # Get API key from environment variable
    api_key = os.environ.get("CLEANVOICE_API_KEY")
    if not api_key:
        print("Please set CLEANVOICE_API_KEY environment variable")
        sys.exit(1)
    
    # Initialize Cleanvoice SDK
    cv = Cleanvoice({"api_key": api_key})
    
    # Example 1: Upload a file and get the URL
    print("=== File Upload Example ===")
    
    # Check if we have a sample file
    sample_file = "sample_audio.mp3"  # Replace with your actual file path
    
    if not os.path.exists(sample_file):
        print(f"Sample file '{sample_file}' not found.")
        print("Please provide a valid audio file path.")
        return
    
    try:
        # Upload the file
        print(f"Uploading file: {sample_file}")
        uploaded_url = cv.upload_file(sample_file)
        print(f"File uploaded successfully! URL: {uploaded_url}")
        
        # Now you can use this URL for processing
        print("\nProcessing uploaded file...")
        result = cv.process(uploaded_url, {
            "fillers": True,
            "transcription": True,
            "summarize": True
        })
        
        print(f"Processing completed!")
        print(f"Download URL: {result.audio.url}")
        if result.transcript:
            print(f"Transcript: {result.transcript.text[:200]}...")
        
        # Download the processed file
        print("Downloading processed file...")
        downloaded_file = cv.download_file(result.audio.url, "processed_audio.mp3")
        print(f"File downloaded to: {downloaded_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Example 2: Upload with custom filename
    print("\n=== Custom Filename Upload Example ===")
    
    try:
        # Upload with a custom filename
        custom_filename = "my_custom_name.mp3"
        uploaded_url = cv.upload_file(sample_file, custom_filename)
        print(f"File uploaded with custom filename! URL: {uploaded_url}")
        
    except Exception as e:
        print(f"Error with custom filename upload: {e}")
    
    # Example 3: Direct processing with local file (automatic upload)
    print("\n=== Direct Processing with Local File ===")
    
    try:
        # Process a local file directly (SDK will handle upload automatically)
        print(f"Processing local file directly: {sample_file}")
        result = cv.process(sample_file, {
            "fillers": True,
            "transcription": True
        })
        
        print(f"Direct processing completed!")
        print(f"Download URL: {result.audio.url}")
        
    except Exception as e:
        print(f"Error with direct processing: {e}")
    
    # Example 4: Process and download in one step
    print("\n=== Process and Download in One Step ===")
    
    try:
        # Process and download automatically
        print(f"Processing and downloading: {sample_file}")
        result, downloaded_path = cv.process_and_download(
            sample_file, 
            "final_output.mp3",
            {"fillers": True, "normalize": True}
        )
        
        print(f"✅ Process and download completed!")
        print(f"📁 File saved as: {downloaded_path}")
        
    except Exception as e:
        print(f"Error with process and download: {e}")


if __name__ == "__main__":
    main()