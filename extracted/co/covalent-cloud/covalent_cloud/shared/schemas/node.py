# Copyright 2023 Agnostiq Inc.

"""Schemas for node-related operations."""

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class NodeResult(BaseModel):
    """Result data for a node."""

    node_id: int
    function_name: str
    result: Any  # The actual result
    status: str

    def __str__(self) -> str:
        result_preview = (
            str(self.result)[:30] + "..."
            if self.result and len(str(self.result)) > 30
            else self.result
        )
        return f"NodeResult(id={self.node_id}, function='{self.function_name}', status={self.status}, result={result_preview})"


class NodeError(BaseModel):
    """Error data for a node."""

    node_id: int
    function_name: str
    error: str  # Error message/traceback
    status: str

    def __str__(self) -> str:
        error_preview = self.error[:50] + "..." if len(self.error) > 50 else self.error
        return f"NodeError(id={self.node_id}, function='{self.function_name}', status={self.status}, error='{error_preview}')"


class NodeOutput(BaseModel):
    """Stdout output for a node."""

    node_id: int
    function_name: str
    stdout: str
    status: str

    def __str__(self) -> str:
        stdout_lines = len(self.stdout.splitlines()) if self.stdout else 0
        return f"NodeOutput(id={self.node_id}, function='{self.function_name}', status={self.status}, {stdout_lines} lines)"


class NodeStderr(BaseModel):
    """Stderr output for a node."""

    node_id: int
    function_name: str
    stderr: str
    status: str

    def __str__(self) -> str:
        stderr_lines = len(self.stderr.splitlines()) if self.stderr else 0
        return f"NodeStderr(id={self.node_id}, function='{self.function_name}', status={self.status}, {stderr_lines} lines)"


class NodeFailure(BaseModel):
    """Failure information for a node."""

    node_id: int
    function_name: str
    status: str
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    error_detail: str

    def __str__(self) -> str:
        # Format timestamps
        started_str = (
            self.started_at.strftime("%Y-%m-%d %H:%M:%S") if self.started_at else "Unknown"
        )
        ended_str = self.ended_at.strftime("%Y-%m-%d %H:%M:%S") if self.ended_at else "Unknown"

        # Calculate duration
        duration_str = ""
        if self.started_at and self.ended_at:
            duration = self.ended_at - self.started_at
            duration_str = f"Duration: {duration}"

        # Format error detail with line breaks preserved for readability
        error_lines = self.error_detail.split("\n")
        if len(error_lines) > 10:
            error_display = (
                "\n".join(error_lines[:5]) + f"\n... ({len(error_lines) - 5} more lines)"
            )
        else:
            error_display = self.error_detail

        return f"""Node Failure
============
Node ID: {self.node_id}
Function: {self.function_name}
Status: {self.status}

Timing:
  Started: {started_str}
  Ended: {ended_str}
  {duration_str}

Error Details:
{error_display}"""
