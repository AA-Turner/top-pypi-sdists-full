"""Bingo Engine v7 — Claude Code CLI architecture for penetration testing.

Public API:
    from bingo.engine import AgentLoop
    loop = AgentLoop(target="https://example.com", config=cfg)
    loop.run("Find vulnerabilities in this target.")
"""
from .loop import AgentLoop
from .executor import ToolExecutor, ToolCall, ToolResult
from .context import ContextManager, Message
from .reporter import generate_report, save_report

__all__ = [
    "AgentLoop",
    "ToolExecutor",
    "ToolCall",
    "ToolResult",
    "ContextManager",
    "Message",
    "generate_report",
    "save_report",
]
