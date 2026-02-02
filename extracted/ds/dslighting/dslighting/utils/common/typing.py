"""
DSLighting Common - Type Definitions

Re-export dsat.common.typing.
"""
try:
    from dsat.common.typing import *
except ImportError:
    # If DSAT is unavailable, define fallback typing aliases.
    from typing import Any, Dict, List, Optional, Union

    # Shared type aliases.
    TaskID = str
    FilePath = str
    MetricValue = float

__all__ = [
    "TaskID",
    "FilePath",
    "MetricValue",
]
