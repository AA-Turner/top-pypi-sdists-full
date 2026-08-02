"""Auto-generated stub for module: databus_backpressure."""
from typing import Any, Dict, Optional

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import os
import time

# Classes
class BackpressurePolicy(Enum):
    BLOCK: str
    DROP_OLDEST: str
    DROP_TO_KEYFRAME: str

    pass
class BackpressurePublisher:
    """
    Wraps ``DataBusProducer.publish`` with lag-aware backpressure.
    """

    def __init__(self: Any, producer: Any, camera_id: str, maxsize: Optional[int] = None, policy: Optional[BackpressurePolicy] = None) -> None: ...

    def depth(self: Any) -> int: ...

    def is_full(self: Any) -> bool: ...

    def publish(self: Any, data: Any, metadata: Optional[Dict] = None) -> bool: ...

class QueueMetrics:
    def drop_rate(self: Any) -> float: ...

    def p99_depth(self: Any) -> float: ...

