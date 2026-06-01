import os
import json
from typing import List, Optional, Dict, Any
from enum import Enum

class ErrorCode(Enum):
    """
    Error codes for MSBench.
    """
    AGENT_TIMEOUT = "AGENT_TIMEOUT"
    CES_TIMEOUT = "CES_TIMEOUT"
    RATE_LIMIT = "RATE_LIMIT"
    FILESYSTEM = "FILESYSTEM"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DEPENDENCY = "DEPENDENCY"
    ERROR = "ERROR"

def _validate_code(code: str):
    if code in ErrorCode.__members__:
        return
    if code.startswith("X_"):
        return
    raise ValueError(
        f"Invalid error code {code!r}: must be one of {sorted(ErrorCode.__members__.keys())} or start with 'X_'."
    )

class ErrorDetail:
    def __init__(self, *, type: str, message: Optional[str] = None, trace: Optional[str] = None):
        self.type = type
        self.message = message
        self.trace = trace

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"type": self.type}
        if self.message is not None:
            d["message"] = self.message
        if self.trace is not None:
            d["trace"] = self.trace
        return d

class Reporter:
    """
    Builds and writes a structured `error.json` according to MSBench spec.
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.main_error: Optional[ErrorDetail] = None
        self.warnings: List[ErrorDetail] = []

    def set_error(self, *, type: str, message: Optional[str] = None, trace: Optional[str] = None):
        """
        Set the primary (fatal) error.
        - type: one of the canonical codes or X_* or ERROR
        - message: required for ERROR & X_*; optional otherwise
        - trace: optional detailed debug info
        """
        _validate_code(type)
        self.main_error = ErrorDetail(type=type, message=message, trace=trace)

    def add_warning(self, *, type: str, message: Optional[str] = None, trace: Optional[str] = None):
        """
        Add a non-fatal warning.
        """
        _validate_code(type)
        self.warnings.append(ErrorDetail(type=type, message=message, trace=trace))

    def write(self) -> str:
        """
        Serialize to JSON and write to `$output_dir/error.json`.
        Returns the path written.
        """
        payload: Dict[str, Any] = {}
        if self.main_error:
            payload.update(self.main_error.to_dict())
        if self.warnings:
            payload["warnings"] = [w.to_dict() for w in self.warnings]

        path = os.path.join(self.output_dir, "error.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return path
