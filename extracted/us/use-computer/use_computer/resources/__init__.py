"""Shared sandbox resource clients."""

from use_computer.resources.accessibility import Accessibility, AsyncAccessibility
from use_computer.resources.display import AsyncDisplay, Display
from use_computer.resources.recording import AsyncRecording, Recording
from use_computer.resources.screenshot import AsyncScreenshot, Screenshot

__all__ = [
    "Accessibility",
    "AsyncAccessibility",
    "AsyncDisplay",
    "AsyncRecording",
    "AsyncScreenshot",
    "Display",
    "Recording",
    "Screenshot",
]
