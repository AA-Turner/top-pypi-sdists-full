"""``content_ir.*`` — asking the platform about Shapes, from inside a workflow.

The engine has always CHECKED kinds at its own boundaries (the input gate, the
output drift-check). What it could not do was let a workflow ASK the question
about an arbitrary value and act on the answer — so a run could hand an agent
a value nobody had ever checked (Arman, 2026-08-23).
"""

from matrx_graph.nodes.content_ir.validate import ValidateKindExecutor

__all__ = ["ValidateKindExecutor"]
