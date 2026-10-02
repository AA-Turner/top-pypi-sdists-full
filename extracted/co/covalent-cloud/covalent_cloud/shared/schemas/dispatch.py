# Copyright 2023 Agnostiq Inc.

"""Schemas for dispatch-related operations."""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class DispatchRecord(BaseModel):
    dispatch_id: str
    name: str  # Lattice name
    status: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    updated_at: datetime
    electron_num: int
    completed_task_num: int
    tags: List[str]
    is_pinned: bool
    redispatch_count: int

    def __str__(self) -> str:
        # Format timestamps
        created_str = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        started_str = (
            self.started_at.strftime("%Y-%m-%d %H:%M:%S") if self.started_at else "Not started"
        )
        completed_str = (
            self.completed_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.completed_at
            else "Not completed"
        )
        updated_str = self.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # Calculate completion percentage
        completion_pct = (
            (self.completed_task_num / self.electron_num * 100) if self.electron_num > 0 else 0
        )

        # Format tags
        tags_str = ", ".join(self.tags) if self.tags else "None"

        # Duration calculation if both start and end times are available
        duration_str = ""
        if self.started_at and self.completed_at:
            duration = self.completed_at - self.started_at
            duration_str = f"\nDuration: {duration}"

        return f"""Dispatch Record
===============
ID: {self.dispatch_id}
Name: {self.name}
Status: {self.status}
Progress: {self.completed_task_num}/{self.electron_num} tasks ({completion_pct:.1f}%)

Timestamps:
  Created: {created_str}
  Started: {started_str}
  Completed: {completed_str}
  Updated: {updated_str}{duration_str}

Tags: {tags_str}
Pinned: {'Yes' if self.is_pinned else 'No'}
Redispatch Count: {self.redispatch_count}"""


class DispatchMetadata(BaseModel):
    total_count: int
    page: int
    count: int
    status_count: Dict[str, int]

    def __str__(self) -> str:
        return f"DispatchMetadata(page={self.page}, count={self.count}, total={self.total_count})"


class DispatchListResponse(BaseModel):
    records: List[DispatchRecord]
    metadata: DispatchMetadata

    def __str__(self) -> str:
        return f"DispatchListResponse({len(self.records)} dispatches, {self.metadata})"
