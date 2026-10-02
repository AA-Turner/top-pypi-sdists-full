from __future__ import annotations


class ListenToMeError(Exception):
    """Base class for all listentome errors."""


class PortAudioError(ListenToMeError):
    """PortAudio returned an error code."""


class Overflow(ListenToMeError):
    """Input blocks arrived faster than they were consumed and `on_overflow="raise"` was set."""


class StreamClosed(ListenToMeError):
    """The stream was used outside its `async with` block."""
