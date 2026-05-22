"""Stub file for boundary_drawing_internal directory."""
from typing import Any, Dict, List, Optional

from .boundary_drawing_internal import BoundaryDrawingTool

# Functions
# From boundary_drawing_internal
def main() -> Any:
    """
    Main function for command line usage.
    """
    ...

# From boundary_drawing_tool
def create_standalone_tool(output_path: str = 'boundary_tool.html', auto_open: bool = True) -> str:
    """
    One-line function to create a standalone boundary drawing tool.
    
    Args:
        output_path (str): Where to save the HTML tool
        auto_open (bool): Whether to automatically open in browser
    
    Returns:
        str: Path to the created HTML tool
    
    Example:
        from matrice_analytics.boundary_drawing_internal import create_standalone_tool
    
        # Create a standalone tool
        create_standalone_tool("my_tool.html")
    """
    ...

# From boundary_drawing_tool
def get_usage_template(zone_types: list = None) -> str:
    """
    Get template code for using generated zones.
    
    Args:
        zone_types (list, optional): Zone types to include in template
    
    Returns:
        str: Template Python code
    
    Example:
        from matrice_analytics.boundary_drawing_internal import get_usage_template
    
        template = get_usage_template(["queue", "staff"])
        print(template)
    """
    ...

# From boundary_drawing_tool
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
        from matrice_analytics.boundary_drawing_internal import quick_boundary_tool
    
        # One line to create and open the tool
        quick_boundary_tool("my_video.mp4", ["queue", "staff", "exit"])
    """
    ...

# From example_usage
def example_1_quick_video_tool() -> Any:
    """
    Example 1: Create a boundary tool from a video file with one line.
    """
    ...

# From example_usage
def example_2_image_tool() -> Any:
    """
    Example 2: Create a boundary tool from an image file.
    """
    ...

# From example_usage
def example_3_class_usage() -> Any:
    """
    Example 3: Using the class for more control.
    """
    ...

# From example_usage
def example_4_standalone_tool() -> Any:
    """
    Example 4: Create a standalone tool for drag & drop.
    """
    ...

# From example_usage
def example_5_integration_code() -> Any:
    """
    Example 5: Show how to integrate generated zones with post-processing.
    """
    ...

# From example_usage
def example_6_workflow() -> Any:
    """
    Example 6: Complete workflow example.
    """
    ...

# From example_usage
def main() -> Any:
    """
    Run all examples.
    """
    ...

# Classes
# From boundary_drawing_internal
class BoundaryDrawingTool:
    # A comprehensive tool for drawing boundaries, polygons, and lines on video frames or images.
    # Supports multiple zones with custom tags like queue, staff, entry, exit, restricted zone, etc.

    def __init__(self: Any) -> None:
        """
        Initialize the boundary drawing tool.
        """
        ...

    def create_grid_reference_image(self: Any, frame_path: str, output_path: str = None, grid_step: int = 50) -> str:
        """
        Create a grid reference image to help users define coordinates.
        
        Args:
            frame_path (str): Path to the input frame/image
            output_path (str): Path to save the grid reference image
            grid_step (int): Grid line spacing in pixels
        
        Returns:
            str: Path to the grid reference image
        """
        ...

    def create_interactive_html(self: Any, image_path: str, output_html: str = None, embed_image: bool = True) -> str:
        """
        Create an interactive HTML page for drawing boundaries with custom tags.
        
        Args:
            image_path (str): Path to the reference image
            output_html (str): Path to save the HTML file
            embed_image (bool): Whether to embed image as base64 or use file path
        
        Returns:
            str: Path to the HTML file
        """
        ...

    def extract_first_frame(self: Any, video_path: str, output_path: str = None) -> str:
        """
        Extract the first frame from a video file.
        
        Args:
            video_path (str): Path to the video file
            output_path (str): Path to save the extracted frame
        
        Returns:
            str: Path to the extracted frame
        """
        ...

    def get_file_type(self: Any, file_path: str) -> str:
        """
        Determine if the file is a video or image.
        
        Args:
            file_path (str): Path to the file
        
        Returns:
            str: 'video', 'image', or 'unknown'
        """
        ...

    def image_to_base64(self: Any, image_path: str) -> str:
        """
        Convert image to base64 for embedding in HTML.
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            str: Base64 encoded image data
        """
        ...

    def open_in_browser(self: Any, html_path: str) -> Any:
        """
        Open the HTML file in the default web browser.
        
        Args:
            html_path (str): Path to the HTML file
        """
        ...

    def process_input_file(self: Any, input_path: str, output_dir: str = None, grid_step: int = 50, open_browser: bool = True, embed_image: bool = True) -> Dict[str, str]:
        """
        Process an input video or image file and create the boundary drawing tool.
        
        Args:
            input_path (str): Path to input video or image file
            output_dir (str): Directory to save output files
            grid_step (int): Grid line spacing for reference image
            open_browser (bool): Whether to open the tool in browser
            embed_image (bool): Whether to embed image as base64 in HTML
        
        Returns:
            Dict[str, str]: Dictionary with paths to created files
        """
        ...


# From boundary_drawing_tool
class EasyBoundaryTool:
    # A simplified, easy-to-use boundary drawing tool that can be imported and used
    # with minimal code. Perfect for quickly creating zone definitions from videos or images.
    #
    # Example:
    #     from matrice_analytics.boundary_drawing_internal import EasyBoundaryTool
    #
    #     # Create tool and open interactive interface
    #     tool = EasyBoundaryTool()
    #     zones = tool.create_from_video("my_video.mp4")
    #
    #     # Or from an image
    #     zones = tool.create_from_image("frame.jpg")

    def __init__(self: Any, auto_open_browser: bool = True, grid_step: int = 50) -> None:
        """
        Initialize the easy boundary drawing tool.
        
        Args:
            auto_open_browser (bool): Whether to automatically open the tool in browser
            grid_step (int): Grid line spacing in pixels for reference
        """
        ...

    def cleanup(self: Any) -> None:
        """
        Optionally clean up data files created by the tool.
        Note: Files are now saved permanently in boundary_drawing_internal/data/
        """
        ...

    def create_from_image(self: Any, image_path: str, output_dir: Optional[str] = None) -> str:
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
        ...

    def create_from_video(self: Any, video_path: str, output_dir: Optional[str] = None) -> str:
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
        ...

    def create_standalone_tool(self: Any, output_path: str = 'boundary_tool.html') -> str:
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
        ...

    def get_data_directory(self: Any) -> Optional[str]:
        """
        Get the data directory where files are saved.
        
        Returns:
            str: Path to the data directory, or None if not created yet
        """
        ...

    def get_template_code(self: Any, zone_types: list = None) -> str:
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
        ...

    def quick_setup(self: Any, file_path: str, zones_needed: list = None) -> str:
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
        ...


from . import boundary_drawing_internal, boundary_drawing_tool, example_usage