# Copyright 2025 Agnostiq Inc.

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator


class LogEvent(BaseModel):
    """
    Represents a single log event from environment build logs.

    Attributes:
        timestamp: The timestamp when the log event occurred
        message: The log message content
    """

    timestamp: datetime
    message: str

    def __str__(self) -> str:
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        message_preview = self.message[:50] + "..." if len(self.message) > 50 else self.message
        return f"LogEvent({timestamp_str}: {message_preview})"

    @model_validator(mode="before")
    @classmethod
    def convert_timestamp(cls, values):
        """Convert timestamp from milliseconds since epoch to datetime."""
        if isinstance(values, dict) and "timestamp" in values:
            # CloudWatch logs use milliseconds since epoch
            if isinstance(values["timestamp"], (int, float)):
                values["timestamp"] = datetime.fromtimestamp(values["timestamp"] / 1000)
        return values


class EnvironmentLogs(BaseModel):
    """
    Contains environment build logs with pagination support.

    Attributes:
        events: List of log events
        next_token: Token for fetching next page of logs, None if no more pages
    """

    events: List[LogEvent] = Field(default_factory=list)
    next_token: Optional[str] = None

    def __str__(self) -> str:
        pagination_info = "More pages available" if self.next_token else "All logs loaded"

        # Show sample of recent events
        events_preview = ""
        if self.events:
            events_preview = "\n\nRecent Events:\n"
            for i, event in enumerate(self.events[:3]):  # Show first 3 events
                timestamp_str = event.timestamp.strftime("%H:%M:%S")
                message_preview = (
                    event.message[:60] + "..." if len(event.message) > 60 else event.message
                )
                events_preview += f"  [{timestamp_str}] {message_preview}\n"

            if len(self.events) > 3:
                events_preview += f"  ... and {len(self.events) - 3} more events"

        return f"""Environment Build Logs
=====================
Event Count: {len(self.events)}
Pagination: {pagination_info}{events_preview}"""

    @model_validator(mode="before")
    @classmethod
    def convert_server_response(cls, values):
        """Convert server response format to our schema."""
        if isinstance(values, dict):
            # Convert from server format
            if "events" in values and isinstance(values["events"], list):
                converted_events = []
                for event in values["events"]:
                    if isinstance(event, dict):
                        converted_events.append(
                            {
                                "timestamp": event.get("timestamp"),
                                "message": event.get("message", ""),
                            }
                        )
                    else:
                        # If event is already a LogEvent object, keep it as is
                        converted_events.append(event)
                values["events"] = converted_events

            # Map server token field names
            if "nextForwardToken" in values:
                values["next_token"] = values.get("nextForwardToken")
            elif "nextBackwardToken" in values:
                values["next_token"] = values.get("nextBackwardToken")

        return values
