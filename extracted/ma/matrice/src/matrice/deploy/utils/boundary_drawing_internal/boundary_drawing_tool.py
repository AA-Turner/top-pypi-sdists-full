"""
Easy-to-use boundary drawing tool for creating interactive zone definitions.

This module provides a simple interface for creating boundary drawing tools
from videos or images with just a few lines of code.
"""

import cv2
import numpy as np
import os
import webbrowser
import base64
import datetime
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, Union
from .boundary_drawing_internal import BoundaryDrawingTool


class EasyBoundaryTool:
    """
    A simplified, easy-to-use boundary drawing tool that can be imported and used
    with minimal code. Perfect for quickly creating zone definitions from videos or images.
    
    Example:
        from matrice.deploy.utils.boundary_drawing_internal import EasyBoundaryTool
        
        # Create tool and open interactive interface
        tool = EasyBoundaryTool()
        zones = tool.create_from_video("my_video.mp4")
        
        # Or from an image
        zones = tool.create_from_image("frame.jpg")
    """
    
    def __init__(self, auto_open_browser: bool = True, grid_step: int = 50):
        """
        Initialize the easy boundary drawing tool.
        
        Args:
            auto_open_browser (bool): Whether to automatically open the tool in browser
            grid_step (int): Grid line spacing in pixels for reference
        """
        self.auto_open_browser = auto_open_browser
        self.grid_step = grid_step
        self.tool = BoundaryDrawingTool()
        self._data_dir = None
        
    def _create_unique_data_dir(self, input_filename: str) -> str:
        """
        Create a unique directory in the boundary_drawing_internal/data folder.
        
        Args:
            input_filename (str): Name of the input file to create unique folder for
            
        Returns:
            str: Path to the created unique directory
        """
        # Get the boundary_drawing_internal directory
        base_dir = Path(__file__).parent
        data_dir = base_dir / "data"
        
        # Create data directory if it doesn't exist
        data_dir.mkdir(exist_ok=True)
        
        # Create unique directory name with timestamp and UUID
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        input_name = Path(input_filename).stem
        
        unique_dir_name = f"{input_name}_{timestamp}_{unique_id}"
        unique_dir = data_dir / unique_dir_name
        
        # Create the unique directory
        unique_dir.mkdir(exist_ok=True)
        
        self._data_dir = str(unique_dir)
        return self._data_dir
        
    def create_from_video(self, video_path: str, output_dir: Optional[str] = None) -> str:
        """
        Create an interactive boundary drawing tool from a video file.
        Extracts the first frame and opens the drawing interface.
        
        Args:
            video_path (str): Path to the video file
            output_dir (str, optional): Directory to save output files. 
                                      If None, creates a unique directory in boundary_drawing_internal/data.
        
        Returns:
            str: Path to the HTML boundary drawing tool
            
        Example:
            tool = EasyBoundaryTool()
            html_path = tool.create_from_video("security_camera.mp4")
            # Interactive tool opens in browser
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Set up output directory
        if output_dir is None:
            output_dir = self._create_unique_data_dir(video_path)
        else:
            os.makedirs(output_dir, exist_ok=True)
            
        # Process the video
        results = self.tool.process_input_file(
            input_path=video_path,
            output_dir=output_dir,
            grid_step=self.grid_step,
            open_browser=self.auto_open_browser,
            embed_image=True
        )
        
        print(f"🎯 Boundary drawing tool created from video: {video_path}")
        print(f"📁 Files saved to: {output_dir}")
        if self.auto_open_browser:
            print("🌐 Interactive tool opened in your browser")
        else:
            print(f"🌐 Open this file in browser: {results['html_tool']}")
            
        return results['html_tool']
        
    def create_from_image(self, image_path: str, output_dir: Optional[str] = None) -> str:
        """
        Create an interactive boundary drawing tool from an image file.
        
        Args:
            image_path (str): Path to the image file
            output_dir (str, optional): Directory to save output files.
                                      If None, creates a unique directory in boundary_drawing_internal/data.
        
        Returns:
            str: Path to the HTML boundary drawing tool
            
        Example:
            tool = EasyBoundaryTool()
            html_path = tool.create_from_image("frame.jpg")
            # Interactive tool opens in browser
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
            
        # Set up output directory
        if output_dir is None:
            output_dir = self._create_unique_data_dir(image_path)
        else:
            os.makedirs(output_dir, exist_ok=True)
            
        # Process the image
        results = self.tool.process_input_file(
            input_path=image_path,
            output_dir=output_dir,
            grid_step=self.grid_step,
            open_browser=self.auto_open_browser,
            embed_image=True
        )
        
        print(f"🎯 Boundary drawing tool created from image: {image_path}")
        print(f"📁 Files saved to: {output_dir}")
        if self.auto_open_browser:
            print("🌐 Interactive tool opened in your browser")
        else:
            print(f"🌐 Open this file in browser: {results['html_tool']}")
            
        return results['html_tool']
        
    def quick_setup(self, file_path: str, zones_needed: list = None) -> str:
        """
        Quick setup method that auto-detects file type and creates the tool.
        
        Args:
            file_path (str): Path to video or image file
            zones_needed (list, optional): List of zone types you plan to create.
                                         Used for informational purposes.
        
        Returns:
            str: Path to the HTML boundary drawing tool
            
        Example:
            tool = EasyBoundaryTool()
            tool.quick_setup("video.mp4", zones_needed=["queue", "staff", "entry"])
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        # Detect file type
        file_type = self.tool.get_file_type(file_path)
        
        if file_type == 'video':
            html_path = self.create_from_video(file_path)
        elif file_type == 'image':
            html_path = self.create_from_image(file_path)
        else:
            raise ValueError(f"Unsupported file format: {Path(file_path).suffix}")
            
        # Print helpful information
        if zones_needed:
            print(f"\n📝 Zones you plan to create: {', '.join(zones_needed)}")
            
        print("\n💡 Tips:")
        print("1. Select a zone type from the sidebar")
        print("2. Click on the image to add points")
        print("3. Right-click or press Enter to complete a zone")
        print("4. Use the 'Generate Code' button to get Python code")
        print("5. Copy the generated code for use in your applications")
        
        return html_path
        
    def create_standalone_tool(self, output_path: str = "boundary_tool.html") -> str:
        """
        Create a standalone HTML tool that can accept file uploads.
        This creates a self-contained tool that doesn't need a specific input file.
        
        Args:
            output_path (str): Path where to save the standalone HTML tool
            
        Returns:
            str: Path to the created HTML tool
            
        Example:
            tool = EasyBoundaryTool()
            html_path = tool.create_standalone_tool("my_boundary_tool.html")
            # Opens a tool where you can drag & drop any video/image
        """
        # Read the template HTML
        template_path = Path(__file__).parent / "boundary_tool_template.html"
        
        if not template_path.exists():
            raise FileNotFoundError("Template HTML file not found")
            
        # Copy template to output location
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"🎯 Standalone boundary drawing tool created: {output_path}")
        
        if self.auto_open_browser:
            try:
                webbrowser.open(f'file://{os.path.abspath(output_path)}')
                print("🌐 Standalone tool opened in your browser")
            except Exception as e:
                print(f"Could not open browser: {e}")
                print(f"🌐 Please manually open: {output_path}")
        else:
            print(f"🌐 Open this file in browser: {output_path}")
            
        print("\n💡 With the standalone tool you can:")
        print("- Drag & drop any video or image file")
        print("- Create multiple zone configurations")
        print("- Save and load configurations")
        print("- Generate code for different projects")
        
        return output_path
        
    def get_template_code(self, zone_types: list = None) -> str:
        """
        Get template Python code showing how to use the generated zones.
        
        Args:
            zone_types (list, optional): List of zone types to include in template
            
        Returns:
            str: Template Python code
            
        Example:
            tool = EasyBoundaryTool()
            template = tool.get_template_code(["queue", "staff", "service"])
            print(template)
        """
        if zone_types is None:
            zone_types = ["queue", "staff", "entry", "exit"]
            
        template = """# Template code for using your boundary zones
from matrice.deploy.utils.post_processing import (
    CustomerServiceProcessor, 
    AdvancedTrackingProcessor,
    CountingProcessor
)

# Your zones dictionary (replace with generated code)
zones = {
"""
        
        for i, zone_type in enumerate(zone_types):
            template += f'    "{zone_type}": [[100, 100], [200, 100], [200, 200], [100, 200]]'
            if i < len(zone_types) - 1:
                template += ","
            template += "\n"
            
        template += """}\n
# Usage examples:

# 1. Customer Service Processor
customer_processor = CustomerServiceProcessor(
    customer_areas=zones.get("queue", {}),
    staff_areas=zones.get("staff", {}),
    service_areas=zones.get("service", {})
)

# 2. Advanced Tracking with Boundaries
from matrice.deploy.utils.post_processing.config import AdvancedTrackingConfig

tracking_config = AdvancedTrackingConfig(
    boundary_config={
        "points": zones.get("entry", []),
        "type": "line"
    }
)
tracking_processor = AdvancedTrackingProcessor(tracking_config)

# 3. Counting in Zones
from matrice.deploy.utils.post_processing.config import CountingConfig

counting_config = CountingConfig(
    count_rules={"enable_time_based_counting": True}
)
counting_processor = CountingProcessor(counting_config)

# Count objects in specific zones
detection_results = {}  # Your detection results
count_results = counting_processor.count_in_zones(
    results=detection_results,
    zones=zones
)

print("Zone counts:", count_results)
"""
        
        return template
        
    def cleanup(self):
        """
        Optionally clean up data files created by the tool.
        Note: Files are now saved permanently in boundary_drawing_internal/data/
        """
        if self._data_dir and os.path.exists(self._data_dir):
            import shutil
            try:
                response = input(f"🗂️  Delete saved boundary tool files in {self._data_dir}? (y/N): ")
                if response.lower() in ['y', 'yes']:
                    shutil.rmtree(self._data_dir)
                    print(f"🧹 Cleaned up boundary tool files: {self._data_dir}")
                else:
                    print(f"📁 Files preserved in: {self._data_dir}")
            except Exception as e:
                print(f"Warning: Could not clean up files: {e}")
    
    def get_data_directory(self) -> Optional[str]:
        """
        Get the data directory where files are saved.
        
        Returns:
            str: Path to the data directory, or None if not created yet
        """
        return self._data_dir
                
    def __del__(self):
        """Clean up on object destruction - but don't auto-delete data files."""
        # Don't auto-cleanup data files since they're meant to be permanent
        pass


# Convenience functions for even easier usage
def quick_boundary_tool(file_path: str, zones_needed: list = None, auto_open: bool = True) -> str:
    """
    One-line function to create a boundary drawing tool from any file.
    
    Args:
        file_path (str): Path to video or image file
        zones_needed (list, optional): List of zone types you plan to create
        auto_open (bool): Whether to automatically open in browser
        
    Returns:
        str: Path to the HTML boundary drawing tool
        
    Example:
        from matrice.deploy.utils.boundary_drawing_internal import quick_boundary_tool
        
        # One line to create and open the tool
        quick_boundary_tool("my_video.mp4", ["queue", "staff", "exit"])
    """
    tool = EasyBoundaryTool(auto_open_browser=auto_open)
    return tool.quick_setup(file_path, zones_needed)


def create_standalone_tool(output_path: str = "boundary_tool.html", auto_open: bool = True) -> str:
    """
    One-line function to create a standalone boundary drawing tool.
    
    Args:
        output_path (str): Where to save the HTML tool
        auto_open (bool): Whether to automatically open in browser
        
    Returns:
        str: Path to the created HTML tool
        
    Example:
        from matrice.deploy.utils.boundary_drawing_internal import create_standalone_tool
        
        # Create a standalone tool
        create_standalone_tool("my_tool.html")
    """
    tool = EasyBoundaryTool(auto_open_browser=auto_open)
    return tool.create_standalone_tool(output_path)


def get_usage_template(zone_types: list = None) -> str:
    """
    Get template code for using generated zones.
    
    Args:
        zone_types (list, optional): Zone types to include in template
        
    Returns:
        str: Template Python code
        
    Example:
        from matrice.deploy.utils.boundary_drawing_internal import get_usage_template
        
        template = get_usage_template(["queue", "staff"])
        print(template)
    """
    tool = EasyBoundaryTool()
    return tool.get_template_code(zone_types) 