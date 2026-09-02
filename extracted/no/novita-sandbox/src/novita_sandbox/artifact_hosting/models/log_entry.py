"""Log entry model for deployment logs in Artifact Hosting SDK V2."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class LogEntry:
    """A single log entry from deployment logs.
    
    Attributes:
        message: Log message content (mapped from API's "line" field).
    """
    message: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        """Create LogEntry from API response dictionary.
        
        The API returns:
            {"line": "..."}
        
        We map "line" -> "message" for a cleaner SDK interface.
        
        Args:
            data: Dictionary with key "line".
        
        Returns:
            LogEntry instance.
        """
        # API uses "line", SDK exposes as "message"
        message = data.get("line") or data.get("message", "")
        
        return cls(message=message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (uses "line" to match API format)."""
        return {"line": self.message}
    
    def __str__(self) -> str:
        """Format as readable string."""
        return self.message
