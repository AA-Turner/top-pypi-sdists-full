"""Checkpointer protocol, in-memory backend, and Postgres backend.

PostgresCheckpointer is imported lazily — it requires `matrx-orm` + a
registered database. Importing this module never fails even when matrx-orm
isn't installed; accessing `PostgresCheckpointer` at runtime is what pulls
in the dependency.
"""

from matrx_graph.checkpoint.memory import MemoryCheckpointer
from matrx_graph.checkpoint.protocol import (
    Checkpoint,
    Checkpointer,
    NextInvocation,
    NodeOutcome,
    PendingBinding,
    PendingEdgeBinding,
)


def __getattr__(name: str):  # pragma: no cover - trivial
    if name == "PostgresCheckpointer":
        from matrx_graph.checkpoint.postgres import PostgresCheckpointer

        return PostgresCheckpointer
    raise AttributeError(f"module 'matrx_graph.checkpoint' has no attribute {name!r}")


__all__ = [
    "Checkpoint",
    "Checkpointer",
    "MemoryCheckpointer",
    "NextInvocation",
    "NodeOutcome",
    "PendingBinding",
    "PendingEdgeBinding",
    "PostgresCheckpointer",
]
