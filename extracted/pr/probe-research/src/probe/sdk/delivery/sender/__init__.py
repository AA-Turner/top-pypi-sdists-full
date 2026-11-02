"""sender: send a write now (`Sender`) under one write's failure rules (`SendPolicy`)."""

from .policy import SendPolicy, resolve_policy
from .sender import Sender, is_queue_only, queue_only

__all__ = ["SendPolicy", "Sender", "is_queue_only", "queue_only", "resolve_policy"]
