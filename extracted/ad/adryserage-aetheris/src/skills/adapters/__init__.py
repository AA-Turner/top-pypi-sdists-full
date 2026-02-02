"""
Skill Adapters for Aetheris (v3.0)

Provider-specific adapters for skill execution:
- Claude: Tool Use format
- Gemini: Function Calling format
- OpenAI: Function Calling format
"""

from src.skills.adapters.base_adapter import SkillAdapter
from src.skills.adapters.claude_adapter import ClaudeAdapter
from src.skills.adapters.gemini_adapter import GeminiAdapter

__all__ = [
    "SkillAdapter",
    "ClaudeAdapter",
    "GeminiAdapter",
]
