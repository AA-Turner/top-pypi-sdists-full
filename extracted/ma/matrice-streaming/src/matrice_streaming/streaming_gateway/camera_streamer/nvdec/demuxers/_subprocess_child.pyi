"""Auto-generated stub for module: _subprocess_child."""
from typing import Any

from __future__ import annotations
import json
import struct
import sys

# Functions
def read_json(proc: Any) -> Any: ...
    """
    Read one length-prefixed message and decode as JSON.
    """
def read_msg(proc: Any) -> Any: ...
    """
    Read one length-prefixed message from proc.stdout.
    
        Returns raw bytes payload. Caller interprets as JSON or binary.
        Raises EOFError on pipe close.
    """
def write_json(obj: Any) -> None: ...
    """
    Serialize obj to JSON and write as a length-prefixed message.
    """
def write_msg(data: Any) -> None: ...
    """
    Write length-prefixed message to stdout.
    """
