#!/usr/bin/env python3
"""
Boundary Drawing Tool Launcher for Airport Security Video

This script launches the interactive boundary drawing tool for creating
zones in the airport security video door2.mp4.
"""

import os
import sys
from pathlib import Path

# Add the python-sdk to the path so we can import matrice modules
# Navigate up from usage folder to find the src directory
current_dir = Path(__file__).parent.absolute()
src_path = current_dir.parent.parent.parent
sys.path.insert(0, str(src_path))

# Alternative: Add the matrice package directly
matrice_path = src_path / "matrice"
if matrice_path.exists():
    sys.path.insert(0, str(src_path))

try:
    from matrice_analytics.boundary_drawing_internal import (
        EasyBoundaryTool,
        quick_boundary_tool
    )
except ImportError as e:
    print(f"❌ Error importing matrice modules: {e}")
    print("Make sure you're running this from the matriceai directory")
    sys.exit(1)


def main():
    """Launch the boundary drawing tool for the airport security video."""
    
    # Video path
    video_path = r"C:\Users\pathi\OneDrive\Desktop\matriceai\matrice-applications\airport-security\door2.mp4"
    
    print("🎯 Airport Security Boundary Drawing Tool")
    print("=" * 50)
    print(f"📹 Video: {video_path}")
    
    # Check if video exists
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        print("\nPlease check that the file exists and the path is correct.")
        return
    
    print("✅ Video file found!")
    print("\n🚀 Launching boundary drawing tool...")
    
    try:
        # Launch the boundary drawing tool with relevant zones for airport security
        html_path = quick_boundary_tool(
            video_path,
            zones_needed=[
                "entry_zone", 
                "security_checkpoint", 
                "waiting_area", 
                "restricted_area",
                "exit_zone",
                "monitoring_zone"
            ]
        )
        
        print(f"✅ Boundary drawing tool launched!")
        print(f"🌐 Tool URL: {html_path}")
        print("\n📋 Instructions:")
        print("1. The tool should open in your default browser")
        print("2. Select a zone type from the dropdown")
        print("3. Click on the video frame to create boundary points")
        print("4. Right-click or press Enter to complete a zone")
        print("5. Generate Python code when finished")
        print("6. Copy the generated code for use in your application")
        
        print("\n💡 Suggested zones for airport security:")
        print("- entry_zone: Area where people enter")
        print("- security_checkpoint: X-ray and metal detector area")
        print("- waiting_area: Queue or waiting zones")
        print("- restricted_area: Staff-only or secure areas")
        print("- exit_zone: Exit doors and pathways")
        print("- monitoring_zone: Areas under special surveillance")
        
    except Exception as e:
        print(f"❌ Error launching tool: {e}")
        print("\nTrying alternative method...")
        
        # Alternative method using the class directly
        try:
            tool = EasyBoundaryTool(auto_open_browser=True)
            html_path = tool.create_from_video(video_path)
            print(f"✅ Alternative launch successful!")
            print(f"🌐 Tool URL: {html_path}")
        except Exception as e2:
            print(f"❌ Alternative method also failed: {e2}")
            print("Please check the matrice installation and try again.")


if __name__ == "__main__":
    main() 