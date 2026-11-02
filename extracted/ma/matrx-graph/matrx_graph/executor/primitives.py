"""Re-export Send from the types layer so callers can say
`from matrx_graph.executor import Send`.

Send itself lives in `matrx_graph.types.send` to avoid a circular import
between the executor and checkpoint modules (Checkpointer.NodeOutcome needs
to reference Send).
"""

from matrx_graph.types.send import Send

__all__ = ["Send"]
