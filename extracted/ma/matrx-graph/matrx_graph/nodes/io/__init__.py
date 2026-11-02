"""I/O node pack — nodes that move data between the run and the outside world.

- ``io.user_input``    seeds a run with values the person running it provides.
- ``output.to_frontend`` (in the sibling ``output`` pack) sends data back to
  the screen mid-run without stopping the workflow.
"""

from matrx_graph.nodes.io.user_input import UserInputExecutor

__all__ = ["UserInputExecutor"]
