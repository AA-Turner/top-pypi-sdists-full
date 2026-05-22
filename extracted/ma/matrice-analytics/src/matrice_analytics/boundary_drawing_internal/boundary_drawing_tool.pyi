"""Auto-generated stub for module: boundary_drawing_tool."""
from typing import Any, List, Optional

from .boundary_drawing_internal import BoundaryDrawingTool

# Functions
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

# Classes
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

