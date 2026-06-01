"""
codrninja: AI-first coding assistant for automation
"""

__author__ = "Milan"
__license__ = "MIT"
__version__ = "1.5.114"

from .core import AICode, Session
from .config import Config
from .agent import Agent
from .providers import ProviderManager, OllamaProvider, OpenAIProvider, AnthropicProvider, OpenRouterProvider
from .subagent import Subagent, SubagentManager
from .todo import TodoItem, TodoManager
from .lsp import LSPClient, LSPManager

__all__ = ["AICode", "Session", "Config", "Agent", "Subagent", "SubagentManager", "ProviderManager", "OllamaProvider", "OpenAIProvider", "AnthropicProvider", "OpenRouterProvider", "TodoItem", "TodoManager", "LSPClient", "LSPManager"]
