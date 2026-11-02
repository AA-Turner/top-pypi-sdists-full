"""``flow.*`` — run-pacing primitives: sleep, wait-until, throttle, no-op.

Pass-through by design: every node in this pack hands its input payload
downstream unchanged, so none of them declares an ``output_kind`` — runtime
``__kind`` propagation carries the payload's identity through them (the same
posture as ``data.transform``; ``"json"`` is a format word, never an identity).
"""

from matrx_graph.nodes.flow.noop import NoopExecutor
from matrx_graph.nodes.flow.sleep import (
    SLEEP_MARKER,
    SleepExecutor,
    WaitUntilExecutor,
)
from matrx_graph.nodes.flow.throttle import ThrottleExecutor

__all__ = [
    "SLEEP_MARKER",
    "NoopExecutor",
    "SleepExecutor",
    "ThrottleExecutor",
    "WaitUntilExecutor",
]
