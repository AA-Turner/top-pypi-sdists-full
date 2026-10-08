#!/usr/bin/env python3
"""
Example usage of the Easy Boundary Drawing Tool.

This file demonstrates various ways to use the boundary drawing tool
with minimal code for quick zone definition.
"""

import logging
import os

from matrice_analytics.boundary_drawing_internal import (
    EasyBoundaryTool,
    create_standalone_tool,
    quick_boundary_tool,
)

_logger = logging.getLogger(__name__)


def example_1_quick_video_tool():
    """Example 1: Create a boundary tool from a video file with one line."""
    _logger.info("📹 Example 1: Quick video boundary tool")
    _logger.info("=" * 50)

    # Replace with your video file path
    video_path = "example_video.mp4"

    if os.path.exists(video_path):
        # One line to create and open the tool
        html_path = quick_boundary_tool(
            video_path, zones_needed=["queue", "staff", "entry", "exit"]
        )
        _logger.info("✅ Tool created: %s", html_path)
    else:
        _logger.info("⚠️  Video file not found: %s", video_path)
        _logger.info("Replace 'example_video.mp4' with your actual video file path")


def example_2_image_tool():
    """Example 2: Create a boundary tool from an image file."""
    _logger.info("\n🖼️  Example 2: Image boundary tool")
    _logger.info("=" * 50)

    # Replace with your image file path
    image_path = "example_frame.jpg"

    if os.path.exists(image_path):
        tool = EasyBoundaryTool()
        html_path = tool.create_from_image(image_path)
        _logger.info("✅ Tool created: %s", html_path)
    else:
        _logger.info("⚠️  Image file not found: %s", image_path)
        _logger.info("Replace 'example_frame.jpg' with your actual image file path")


def example_3_class_usage():
    """Example 3: Using the class for more control."""
    _logger.info("\n🔧 Example 3: Class-based usage with more control")
    _logger.info("=" * 50)

    # Initialize tool with custom settings
    tool = EasyBoundaryTool(
        auto_open_browser=False,
        grid_step=25,  # Don't auto-open browser  # Smaller grid for precision
    )

    # Replace with your file path
    file_path = "your_file.mp4"  # or .jpg, .png, etc.

    if os.path.exists(file_path):
        # Auto-detect file type and create tool
        html_path = tool.quick_setup(
            file_path, zones_needed=["customer_area", "service_desk", "waiting_zone"]
        )
        _logger.info("✅ Tool created (browser not opened): %s", html_path)

        # Get template code for integration
        template = tool.get_template_code(["customer_area", "service_desk"])
        _logger.info("\n📝 Template code for using your zones:")
        _logger.info("%s", template[:300] + "..." if len(template) > 300 else template)

        # Clean up temporary files when done
        tool.cleanup()
    else:
        _logger.info("⚠️  File not found: %s", file_path)
        _logger.info("Replace 'your_file.mp4' with your actual file path")


def example_4_standalone_tool():
    """Example 4: Create a standalone tool for drag & drop."""
    _logger.info("\n📎 Example 4: Standalone drag & drop tool")
    _logger.info("=" * 50)

    # Create a standalone HTML tool
    html_path = create_standalone_tool(output_path="my_boundary_tool.html", auto_open=True)

    _logger.info("✅ Standalone tool created: %s", html_path)
    _logger.info("🎯 You can now drag & drop any video or image file into the tool!")


def example_5_integration_code():
    """Example 5: Show how to integrate generated zones with post-processing."""
    _logger.info("\n🔗 Example 5: Integration with post-processing")
    _logger.info("=" * 50)

    # Example zones (replace with your generated zones)
    zones = {
        "queue": [[100, 200], [300, 200], [300, 400], [100, 400]],
        "staff": [[500, 100], [700, 100], [700, 300], [500, 300]],
        "entry": [[50, 50], [150, 100]],
    }
    _ = len(zones)  # example data; reserved for zone API usage

    _logger.info("📝 Example integration code:")
    _logger.info("""
# 1. Customer Service Processor
from matrice_analytics.post_processing import CustomerServiceProcessor

processor = CustomerServiceProcessor(
    customer_areas=zones["queue"],
    staff_areas=zones["staff"],
    service_areas=zones.get("service", {})
)

# 2. Advanced Tracking with Entry/Exit
from matrice_analytics.post_processing import AdvancedTrackingProcessor
from matrice_analytics.post_processing.config import AdvancedTrackingConfig

config = AdvancedTrackingConfig(
    boundary_config={
        "points": zones["entry"],
        "type": "line"
    }
)
tracker = AdvancedTrackingProcessor(config)

# 3. Count objects in zones
from matrice_analytics.post_processing import CountingProcessor

counter = CountingProcessor(your_config)
results = counter.count_in_zones(detection_results, zones=zones)
    """)


def example_6_workflow():
    """Example 6: Complete workflow example."""
    _logger.info("\n🔄 Example 6: Complete workflow")
    _logger.info("=" * 50)

    _logger.info("""
📋 Complete Boundary Drawing Workflow:

1. 📹 Start with your video/image:
   tool = EasyBoundaryTool()
   html_path = tool.create_from_video("security_camera.mp4")

2. 🎨 Use the interactive tool to draw zones:
   - Select zone types (queue, staff, entry, etc.)
   - Click on image to add points
   - Complete zones with right-click or Enter
   - Generate and copy the Python code

3. 📝 Use generated zones in your application:
   # Paste the generated code
   zones = {
       "queue": [[x1, y1], [x2, y2], ...],
       "staff": [[x1, y1], [x2, y2], ...]
   }

4. 🔧 Integrate with post-processing:
   processor = CustomerServiceProcessor(
       customer_areas=zones["queue"],
       staff_areas=zones["staff"]
   )

5. 🚀 Process your data:
   results = processor.process_detections(detection_data)
    """)


def main():
    """Run all examples."""
    _logger.info("🎯 Easy Boundary Drawing Tool - Usage Examples")
    _logger.info("=" * 60)

    # Run examples
    example_1_quick_video_tool()
    example_2_image_tool()
    example_3_class_usage()
    example_4_standalone_tool()
    example_5_integration_code()
    example_6_workflow()

    _logger.info("\n" + "=" * 60)
    _logger.info("💡 Tips:")
    _logger.info("- Replace example file paths with your actual files")
    _logger.info("- The tool supports MP4, AVI, MOV, JPG, PNG, and more")
    _logger.info("- Generated zones work directly with Matrice post-processing")
    _logger.info("- Save configurations as JSON for reuse")
    _logger.info("- Use custom zone names for specific use cases")


if __name__ == "__main__":
    main()
