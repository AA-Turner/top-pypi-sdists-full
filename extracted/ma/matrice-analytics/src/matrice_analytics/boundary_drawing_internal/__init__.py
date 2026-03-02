"""
Boundary Drawing Tool - Interactive zone definition for computer vision applications.

This module provides tools for creating interactive boundary definitions from video frames
or images. Perfect for defining zones like queues, staff areas, entry/exit points, 
security zones, and more for computer vision applications.

Easy Usage Examples:
    # Quick one-liner to create a tool from any file
    from matrice_analytics.boundary_drawing_internal import quick_boundary_tool
    quick_boundary_tool("my_video.mp4", zones_needed=["queue", "staff", "exit"])
    
    # Or use the class for more control
    from matrice_analytics.boundary_drawing_internal import EasyBoundaryTool
    tool = EasyBoundaryTool()
    html_path = tool.create_from_video("security_camera.mp4")
    
    # Create a standalone tool for drag & drop
    from matrice_analytics.boundary_drawing_internal import create_standalone_tool
    create_standalone_tool("my_boundary_tool.html")
"""

# Import both the detailed and easy-to-use tools
from .boundary_drawing_internal import BoundaryDrawingTool
from .boundary_drawing_tool import (
    EasyBoundaryTool,
    quick_boundary_tool,
    create_standalone_tool,
    get_usage_template
)

__all__ = [
    # Main detailed tool
    'BoundaryDrawingTool',
    
    # Easy-to-use tools (recommended for most users)
    'EasyBoundaryTool',
    'quick_boundary_tool',
    'create_standalone_tool',
    'get_usage_template'
]

__version__ = '1.0.0'
__author__ = 'Matrice AI'
__description__ = 'Interactive boundary drawing tool for computer vision applications' 