"""Coworker agent module.

This module provides the CoworkerAgent - a general-purpose assistant
without coding capabilities, focused on research, planning, and collaboration.
"""

from .main_agent import CoworkerAgent
from .toolkit import CoworkerToolkit

__all__ = ["CoworkerAgent", "CoworkerToolkit"]
