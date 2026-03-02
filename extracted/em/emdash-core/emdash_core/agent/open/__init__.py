"""Open Agent - Self-evolving personal assistant with memory.

This module provides the OpenAgent, a minimal, self-evolving, user-driven
personal assistant that writes itself based on user needs rather than
having heavy predefined opinions.

Components:
- OpenAgent: Main agent implementation
- CapabilityRegistry: Discovers and manages capabilities
- HierarchicalMemory: Two-layer memory system (long-term/short-term)
- OpenToolkit: Extended toolkit with memory and capability tools
"""

from .main_agent import OpenAgent
from .capabilities import Capability, CapabilityRegistry
from .memory import (
    HierarchicalMemory,
    LongTermMemory,
    ShortTermMemory,
    MemoryEntry,
)
from .memory_tools import MemoryToolSet
from .toolkit import OpenToolkit
from .tools import (
    AddCapabilityTool,
    RemoveCapabilityTool,
    ListCapabilitiesTool,
)
from .prompts import build_open_system_prompt, OPEN_BOOTSTRAP_PROMPT

__all__ = [
    # Main agent
    "OpenAgent",
    # Components
    "Capability",
    "CapabilityRegistry",
    # Memory system
    "HierarchicalMemory",
    "LongTermMemory",
    "ShortTermMemory",
    "MemoryEntry",
    "MemoryToolSet",
    # Toolkit
    "OpenToolkit",
    # Tools
    "AddCapabilityTool",
    "RemoveCapabilityTool",
    "ListCapabilitiesTool",
    # Prompts
    "build_open_system_prompt",
    "OPEN_BOOTSTRAP_PROMPT",
]
