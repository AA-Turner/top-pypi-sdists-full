#!/usr/bin/env python3
"""Complete workflow example: Upload, Process, and Download with Cleanvoice SDK."""

import os
import sys
from pathlib import Path

# Add the src directory to the path to import cleanvoice
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cleanvoice import Cleanvoice


def main():
    """Demonstrate complete file processing workflow."""
    # Get API key from environment variable
    api_key = os.environ.get("CLEANVOICE_API_KEY")
    if not api_key:
        print("Please set CLEANVOICE_API_KEY environment variable")
        sys.exit(1)
    
    # Initialize Cleanvoice SDK
    cv = Cleanvoice({"api_key": api_key})
    
    print("🎵 Cleanvoice Complete Workflow Demo")
    print("=" * 50)
    
    # Check if we have a sample file
    sample_file = "sample_audio.mp3"  # Replace with your actual file path
    
    if not os.path.exists(sample_file):
        print(f"Sample file '{sample_file}' not found.")
        print("Please provide a valid audio file path.")
        print("\nAlternatively, you can test with a URL:")
        demo_with_url(cv)
        return
    
    # === WORKFLOW 1: Step-by-step process ===
    print("\n🔄 WORKFLOW 1: Step-by-step process")
    print("-" * 40)
    
    try:
        # Step 1: Upload file
        print(f"📤 Step 1: Uploading '{sample_file}'...")
        uploaded_url = cv.upload_file(sample_file, "my_audio_file.mp3")
        print(f"✅ Upload successful! URL: {uploaded_url}")
        
        # Step 2: Process the uploaded file
        print("⚙️  Step 2: Processing audio...")
        result = cv.process(uploaded_url, {
            "fillers": True,
            "normalize": True,
            "transcription": True,
            "summarize": True
        })
        print("✅ Processing complete!")
        
        # Step 3: Download processed file
        print("📥 Step 3: Downloading processed file...")
        downloaded_path = cv.download_file(result.audio.url, "processed_step_by_step.mp3")
        print(f"✅ Download complete! Saved as: {downloaded_path}")
        
        # Show results
        print(f"\n📊 Processing Statistics:")
        print(f"   Original filename: {result.audio.filename}")
        if result.audio.statistics:
            print(f"   Statistics: {result.audio.statistics}")
        
        if result.transcript:
            print(f"\n📝 Transcript preview: {result.transcript.text[:150]}...")
            if result.transcript.summary:
                print(f"📄 Summary: {result.transcript.summary[:100]}...")
        
    except Exception as e:
        print(f"❌ Error in step-by-step workflow: {e}")
    
    # === WORKFLOW 2: One-step process and download ===
    print("\n\n🚀 WORKFLOW 2: One-step process and download")
    print("-" * 50)
    
    try:
        print(f"🔄 Processing and downloading '{sample_file}' in one step...")
        result, downloaded_path = cv.process_and_download(
            sample_file,
            "processed_one_step.mp3",
            {
                "fillers": True,
                "normalize": True,
                "remove_noise": True,
                "transcription": True
            }
        )
        
        print(f"✅ Complete! File saved as: {downloaded_path}")
        print(f"📊 Processing took care of upload, processing, and download automatically!")
        
        if result.transcript:
            print(f"📝 Transcript available with {len(result.transcript.paragraphs)} paragraphs")
        
    except Exception as e:
        print(f"❌ Error in one-step workflow: {e}")
    
    # === WORKFLOW 3: Direct local file processing ===
    print("\n\n⚡ WORKFLOW 3: Direct local file processing")
    print("-" * 50)
    
    try:
        print(f"🔄 Processing local file directly: '{sample_file}'")
        print("(SDK handles upload automatically)")
        
        result = cv.process(sample_file, {
            "fillers": True,
            "stutters": True,
            "normalize": True
        })
        
        print("✅ Processing complete!")
        
        # Download the result
        downloaded_path = cv.download_file(result.audio.url, "processed_direct.mp3")
        print(f"📥 Downloaded to: {downloaded_path}")
        
    except Exception as e:
        print(f"❌ Error in direct processing workflow: {e}")
    
    print("\n🎉 Demo complete! Check the downloaded files:")
    for filename in ["processed_step_by_step.mp3", "processed_one_step.mp3", "processed_direct.mp3"]:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   📁 {filename} ({size:,} bytes)")


def demo_with_url(cv):
    """Demo workflow using a URL instead of local file."""
    print("\n🌐 URL-based workflow demo:")
    
    # Note: This would work with a real audio URL
    sample_url = "https://example.com/sample-audio.mp3"
    
    print(f"📝 Example workflow with URL: {sample_url}")
    print("💡 Replace with a real audio URL to test:")
    
    example_code = '''
    # Process and download from URL
    result, downloaded_path = cv.process_and_download(
        "https://your-audio-url.com/audio.mp3",
        "output.mp3",
        {"fillers": True, "normalize": True}
    )
    print(f"Downloaded to: {downloaded_path}")
    '''
    
    print(example_code)


if __name__ == "__main__":
    main()