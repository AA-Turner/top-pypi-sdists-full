#!/usr/bin/env python3
"""
Simple Boundary Drawing Tool Launcher

A simpler version of the boundary drawing launcher with more configuration options.
"""

import logging
import os
import sys
from pathlib import Path

_logger = logging.getLogger(__name__)

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
        _logger.info("❌ Error importing matrice modules: %s", e)
        return None

    # Default zones if none provided
    if custom_zones is None:
        custom_zones = ["zone1", "zone2", "zone3", "zone4"]

    _logger.info("🎯 Launching boundary tool for: %s", os.path.basename(video_path))
    _logger.info("📍 Zones to create: %s", ", ".join(custom_zones))

    # Check if file exists
    if not os.path.exists(video_path):
        _logger.info("❌ File not found: %s", video_path)
        return None

    try:
        # Create the tool with custom settings
        tool = EasyBoundaryTool(
            auto_open_browser=True,
            grid_step=20,  # Automatically open browser  # Grid step for precise drawing
        )

        # Create the boundary tool
        html_path = tool.quick_setup(video_path, zones_needed=custom_zones)

        _logger.info("✅ Tool created successfully!")
        _logger.info("🌐 Browser should open automatically")
        _logger.info("📄 Tool file: %s", html_path)

        return html_path

    except Exception as e:  # noqa: BLE001 - launcher reports any failure and returns None
        _logger.info("❌ Error creating tool: %s", e)
        return None


if __name__ == "__main__":
    # Your video path
    VIDEO_PATH = (
        r"C:\Users\pathi\OneDrive\Desktop\matriceai\matrice-applications\airport-security\door2.mp4"
    )

    # Custom zones for airport security (you can modify these)
    SECURITY_ZONES = [
        "entry_door",
        "security_line",
        "checkpoint",
        "waiting_area",
        "restricted_zone",
        "exit_door",
    ]

    _logger.info("🔒 Airport Security Boundary Drawing Tool")
    _logger.info("%s", "=" * 45)

    # Launch the tool
    result = launch_boundary_tool(VIDEO_PATH, SECURITY_ZONES)

    if result:
        _logger.info("\n✨ Success! The boundary drawing tool is now open.")
        _logger.info("\n📋 How to use:")
        _logger.info("1. Select a zone type from the dropdown menu")
        _logger.info("2. Click points on the video frame to draw boundaries")
        _logger.info("3. Complete each zone by right-clicking or pressing Enter")
        _logger.info("4. Click 'Generate Code' when finished")
        _logger.info("5. Copy the generated Python code for your application")

        _logger.info("\n💾 The generated code will look like:")
        _logger.info("zones = {")
        _logger.info('    "entry_door": [[x1, y1], [x2, y2], ...],')
        _logger.info('    "security_line": [[x1, y1], [x2, y2], ...],')
        _logger.info("    ...")
        _logger.info("}")
    else:
        _logger.info("\n❌ Failed to launch the tool. Please check the error messages above.")
