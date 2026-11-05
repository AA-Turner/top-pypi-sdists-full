"""signal_sender: which process sent this one a signal (DESIGN.md)."""

from .signal_sender import Sent, SignalSender, load_sender, read_session

__all__ = ["Sent", "SignalSender", "load_sender", "read_session"]
