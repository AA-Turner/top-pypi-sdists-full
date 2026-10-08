#!/usr/bin/env python3
"""
Boundary Drawing Tool Launcher for Airport Security Video

This script launches the interactive boundary drawing tool for creating
zones in the airport security video door2.mp4.
"""

import logging
import os
import sys
from pathlib import Path

_logger = logging.getLogger(__name__)

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
        quick_boundary_tool,
    )
except ImportError as e:
    _logger.info("❌ Error importing matrice modules: %s", e)
    _logger.info("Make sure you're running this from the matriceai directory")
    sys.exit(1)


def main():
    """Launch the boundary drawing tool for the airport security video."""

    # Video path
    video_path = (
        r"C:\Users\pathi\OneDrive\Desktop\matriceai\matrice-applications\airport-security\door2.mp4"
    )

    _logger.info("🎯 Airport Security Boundary Drawing Tool")
    _logger.info("=" * 50)
    _logger.info("📹 Video: %s", video_path)

    # Check if video exists
    if not os.path.exists(video_path):
        _logger.info("❌ Video file not found: %s", video_path)
        _logger.info("\nPlease check that the file exists and the path is correct.")
        return

    _logger.info("✅ Video file found!")
    _logger.info("\n🚀 Launching boundary drawing tool...")

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
                "monitoring_zone",
            ],
        )

        _logger.info("✅ Boundary drawing tool launched!")
        _logger.info("🌐 Tool URL: %s", html_path)
        _logger.info("\n📋 Instructions:")
        _logger.info("1. The tool should open in your default browser")
        _logger.info("2. Select a zone type from the dropdown")
        _logger.info("3. Click on the video frame to create boundary points")
        _logger.info("4. Right-click or press Enter to complete a zone")
        _logger.info("5. Generate Python code when finished")
        _logger.info("6. Copy the generated code for use in your application")

        _logger.info("\n💡 Suggested zones for airport security:")
        _logger.info("- entry_zone: Area where people enter")
        _logger.info("- security_checkpoint: X-ray and metal detector area")
        _logger.info("- waiting_area: Queue or waiting zones")
        _logger.info("- restricted_area: Staff-only or secure areas")
        _logger.info("- exit_zone: Exit doors and pathways")
        _logger.info("- monitoring_zone: Areas under special surveillance")

    except Exception as err:  # noqa: BLE001 - launcher falls back to the class API
        _logger.info("❌ Error launching tool: %s", err)
        _logger.info("\nTrying alternative method...")

        # Alternative method using the class directly
        try:
            tool = EasyBoundaryTool(auto_open_browser=True)
            html_path = tool.create_from_video(video_path)
            _logger.info("✅ Alternative launch successful!")
            _logger.info("🌐 Tool URL: %s", html_path)
        except Exception as e2:  # noqa: BLE001 - last resort, reported to the operator
            _logger.info("❌ Alternative method also failed: %s", e2)
            _logger.info("Please check the matrice installation and try again.")


if __name__ == "__main__":
    main()
