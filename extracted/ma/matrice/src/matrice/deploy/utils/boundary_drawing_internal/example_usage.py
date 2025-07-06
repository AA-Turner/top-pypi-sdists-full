#!/usr/bin/env python3
"""
Example usage of the Easy Boundary Drawing Tool.

This file demonstrates various ways to use the boundary drawing tool
with minimal code for quick zone definition.
"""

import os
from matrice.deploy.utils.boundary_drawing_internal import (
    EasyBoundaryTool,
    quick_boundary_tool,
    create_standalone_tool,
    get_usage_template
)


def example_1_quick_video_tool():
    """Example 1: Create a boundary tool from a video file with one line."""
    print("📹 Example 1: Quick video boundary tool")
    print("=" * 50)
    
    # Replace with your video file path
    video_path = "example_video.mp4"
    
    if os.path.exists(video_path):
        # One line to create and open the tool
        html_path = quick_boundary_tool(
            video_path, 
            zones_needed=["queue", "staff", "entry", "exit"]
        )
        print(f"✅ Tool created: {html_path}")
    else:
        print(f"⚠️  Video file not found: {video_path}")
        print("Replace 'example_video.mp4' with your actual video file path")


def example_2_image_tool():
    """Example 2: Create a boundary tool from an image file."""
    print("\n🖼️  Example 2: Image boundary tool")
    print("=" * 50)
    
    # Replace with your image file path
    image_path = "example_frame.jpg"
    
    if os.path.exists(image_path):
        tool = EasyBoundaryTool()
        html_path = tool.create_from_image(image_path)
        print(f"✅ Tool created: {html_path}")
    else:
        print(f"⚠️  Image file not found: {image_path}")
        print("Replace 'example_frame.jpg' with your actual image file path")


def example_3_class_usage():
    """Example 3: Using the class for more control."""
    print("\n🔧 Example 3: Class-based usage with more control")
    print("=" * 50)
    
    # Initialize tool with custom settings
    tool = EasyBoundaryTool(
        auto_open_browser=False,  # Don't auto-open browser
        grid_step=25              # Smaller grid for precision
    )
    
    # Replace with your file path
    file_path = "your_file.mp4"  # or .jpg, .png, etc.
    
    if os.path.exists(file_path):
        # Auto-detect file type and create tool
        html_path = tool.quick_setup(
            file_path,
            zones_needed=["customer_area", "service_desk", "waiting_zone"]
        )
        print(f"✅ Tool created (browser not opened): {html_path}")
        
        # Get template code for integration
        template = tool.get_template_code(["customer_area", "service_desk"])
        print("\n📝 Template code for using your zones:")
        print(template[:300] + "..." if len(template) > 300 else template)
        
        # Clean up temporary files when done
        tool.cleanup()
    else:
        print(f"⚠️  File not found: {file_path}")
        print("Replace 'your_file.mp4' with your actual file path")


def example_4_standalone_tool():
    """Example 4: Create a standalone tool for drag & drop."""
    print("\n📎 Example 4: Standalone drag & drop tool")
    print("=" * 50)
    
    # Create a standalone HTML tool
    html_path = create_standalone_tool(
        output_path="my_boundary_tool.html",
        auto_open=True
    )
    
    print(f"✅ Standalone tool created: {html_path}")
    print("🎯 You can now drag & drop any video or image file into the tool!")


def example_5_integration_code():
    """Example 5: Show how to integrate generated zones with post-processing."""
    print("\n🔗 Example 5: Integration with post-processing")
    print("=" * 50)
    
    # Example zones (replace with your generated zones)
    zones = {
        "queue": [[100, 200], [300, 200], [300, 400], [100, 400]],
        "staff": [[500, 100], [700, 100], [700, 300], [500, 300]],
        "entry": [[50, 50], [150, 100]]
    }
    
    print("📝 Example integration code:")
    print("""
# 1. Customer Service Processor
from matrice.deploy.utils.post_processing import CustomerServiceProcessor

processor = CustomerServiceProcessor(
    customer_areas=zones["queue"],
    staff_areas=zones["staff"],
    service_areas=zones.get("service", {})
)

# 2. Advanced Tracking with Entry/Exit
from matrice.deploy.utils.post_processing import AdvancedTrackingProcessor
from matrice.deploy.utils.post_processing.config import AdvancedTrackingConfig

config = AdvancedTrackingConfig(
    boundary_config={
        "points": zones["entry"],
        "type": "line"
    }
)
tracker = AdvancedTrackingProcessor(config)

# 3. Count objects in zones
from matrice.deploy.utils.post_processing import CountingProcessor

counter = CountingProcessor(your_config)
results = counter.count_in_zones(detection_results, zones=zones)
    """)


def example_6_workflow():
    """Example 6: Complete workflow example."""
    print("\n🔄 Example 6: Complete workflow")
    print("=" * 50)
    
    print("""
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
    print("🎯 Easy Boundary Drawing Tool - Usage Examples")
    print("=" * 60)
    
    # Run examples
    example_1_quick_video_tool()
    example_2_image_tool()
    example_3_class_usage()
    example_4_standalone_tool()
    example_5_integration_code()
    example_6_workflow()
    
    print("\n" + "=" * 60)
    print("💡 Tips:")
    print("- Replace example file paths with your actual files")
    print("- The tool supports MP4, AVI, MOV, JPG, PNG, and more")
    print("- Generated zones work directly with Matrice post-processing")
    print("- Save configurations as JSON for reuse")
    print("- Use custom zone names for specific use cases")


if __name__ == "__main__":
    main() 