from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class CameraConfig:
    """Configuration for a camera stream."""
    camera_id: str
    input_topic: str
    output_topic: str
    stream_config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True


@dataclass
class StreamMessage:
    """Raw message from stream."""
    camera_id: str
    message_key: str
    data: Any
    timestamp: datetime
    priority: int = 1