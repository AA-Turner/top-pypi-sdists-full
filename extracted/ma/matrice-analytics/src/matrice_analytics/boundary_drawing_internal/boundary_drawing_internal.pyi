"""Auto-generated stub for module: boundary_drawing_internal."""
from typing import Any, Dict

# Functions
def main() -> Any:
    """
    Main function for command line usage.
    """
    ...

# Classes
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

