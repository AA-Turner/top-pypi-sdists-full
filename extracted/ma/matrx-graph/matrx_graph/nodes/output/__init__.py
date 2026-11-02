"""Output node pack — nodes that send data out of the run to the screen.

- ``output.to_frontend`` sends data back to the frontend mid-run (a custom
  render component or the generic viewer) WITHOUT stopping the workflow.
"""

from matrx_graph.nodes.output.to_frontend import ToFrontendExecutor

__all__ = ["ToFrontendExecutor"]
