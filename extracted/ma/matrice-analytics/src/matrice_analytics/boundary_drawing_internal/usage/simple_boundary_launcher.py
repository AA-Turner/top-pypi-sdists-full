#!/usr/bin/env python3
"""
Simple Boundary Drawing Tool Launcher

A simpler version of the boundary drawing launcher with more configuration options.
"""

import os
import sys
from pathlib import Path

# Add the python-sdk to the path
# Navigate up from usage folder to find the src directory
current_dir = Path(__file__).parent.absolute()
src_path = current_dir.parent.parent.parent
sys.path.insert(0, str(src_path))

# Alternative: Add the matrice package directly
matrice_path = src_path / "matrice"
if matrice_path.exists():
    sys.path.insert(0, str(src_path))

def launch_boundary_tool(video_path, custom_zones=None):
    """
    Launch the boundary drawing tool for any video file.
    
    Args:
        video_path (str): Path to the video file
        custom_zones (list): List of zone names to use
    """
    
    try:
        from matrice_analytics.boundary_drawing_internal import EasyBoundaryTool
    except ImportError as e:
        print(f"❌ Error importing matrice modules: {e}")
        return None
    
    # Default zones if none provided
    if custom_zones is None:
        custom_zones = ["zone1", "zone2", "zone3", "zone4"]
    
    print(f"🎯 Launching boundary tool for: {os.path.basename(video_path)}")
    print(f"📍 Zones to create: {', '.join(custom_zones)}")
    
    # Check if file exists
    if not os.path.exists(video_path):
        print(f"❌ File not found: {video_path}")
        return None
    
    try:
        # Create the tool with custom settings
        tool = EasyBoundaryTool(
            auto_open_browser=True,  # Automatically open browser
            grid_step=20            # Grid step for precise drawing
        )
        
        # Create the boundary tool
        html_path = tool.quick_setup(video_path, zones_needed=custom_zones)
        
        print(f"✅ Tool created successfully!")
        print(f"🌐 Browser should open automatically")
        print(f"📄 Tool file: {html_path}")
        
        return html_path
        
    except Exception as e:
        print(f"❌ Error creating tool: {e}")
        return None


if __name__ == "__main__":
    # Your video path
    VIDEO_PATH = r"C:\Users\pathi\OneDrive\Desktop\matriceai\matrice-applications\airport-security\door2.mp4"
    
    # Custom zones for airport security (you can modify these)
    SECURITY_ZONES = [
        "entry_door",
        "security_line", 
        "checkpoint",
        "waiting_area",
        "restricted_zone",
        "exit_door"
    ]
    
    print("🔒 Airport Security Boundary Drawing Tool")
    print("=" * 45)
    
    # Launch the tool
    result = launch_boundary_tool(VIDEO_PATH, SECURITY_ZONES)
    
    if result:
        print("\n✨ Success! The boundary drawing tool is now open.")
        print("\n📋 How to use:")
        print("1. Select a zone type from the dropdown menu")
        print("2. Click points on the video frame to draw boundaries") 
        print("3. Complete each zone by right-clicking or pressing Enter")
        print("4. Click 'Generate Code' when finished")
        print("5. Copy the generated Python code for your application")
        
        print("\n💾 The generated code will look like:")
        print("zones = {")
        print('    "entry_door": [[x1, y1], [x2, y2], ...],')
        print('    "security_line": [[x1, y1], [x2, y2], ...],')
        print("    ...")
        print("}")
    else:
        print("\n❌ Failed to launch the tool. Please check the error messages above.") 