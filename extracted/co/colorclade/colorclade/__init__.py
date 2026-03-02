__author__ = "Matthew Andres Moreno"
__copyright__ = "Copyright 2024, Matthew Andres Moreno"
__credits__ = ["Matthew Andres Moreno"]
__license__ = "MIT"
__version__ = "0.3.0"
__maintainer__ = "Matthew Andres Moreno"
__email__ = "m.more500@gmail.com"

from ._biopython_draw_colorclade_tree import biopython_draw_colorclade_tree
from ._draw_colorclade_tree import draw_colorclade_tree

__all__ = [
    "draw_colorclade_tree",
    "biopython_draw_colorclade_tree",
    "val_to_color_hls",
    "val_to_color_muted",
]
