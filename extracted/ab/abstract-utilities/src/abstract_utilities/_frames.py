"""Cheap call-stack inspection. ``light_stack`` and ``FrameLite`` live in
abstract_essentials (the single source); re-exported here for existing imports."""
from .imports import FrameLite, light_stack

__all__ = ["FrameLite", "light_stack"]
