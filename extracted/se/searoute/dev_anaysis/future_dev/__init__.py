
"""
try:
    from .graph import Graph
    from networkx import bidirectional_dijkstra, astar_path
except ImportError:
    from .core import CGraph as Graph
    from .core import c_bidirectional_dijkstra as bidirectional_dijkstra, c_astar_path as astar_path
"""

from .core import CGraph as Graph
from .core import c_bidirectional_dijkstra as bidirectional_dijkstra, c_astar_path as astar_path

__all__ = [
    "Graph",
    "bidirectional_dijkstra",
    "astar_path"
]