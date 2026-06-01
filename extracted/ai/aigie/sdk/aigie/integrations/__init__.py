"""
Aigie Framework Integrations

This module contains integrations for various AI agent frameworks.

Available integrations:
- agno: Full workflow tracing for Agno agents and teams
- langchain: Full workflow tracing for LangChain chains, agents, and tools
- langgraph: Full workflow tracing for LangGraph stateful graphs
- browser_use: Full workflow tracing for browser-use browser automation
- crewai: Multi-agent orchestration tracing for CrewAI
- autogen: Multi-agent conversation tracing for AutoGen/AG2
- llamaindex: RAG workflow tracing for LlamaIndex
- openai_agents: Agent workflow tracing for OpenAI Agents SDK
- dspy: Program tracing for DSPy modules, predictions, and optimizations
- claude_agent_sdk: Tracing for Anthropic Claude Agent SDK (query, sessions, tools)
- livekit_agents: Real-time voice AI tracing for LiveKit Agents
- instructor: Tracing for Instructor structured output library
- semantic_kernel: Tracing for Microsoft Semantic Kernel
"""

__all__ = [
    "agno",
    "autogen",
    "browser_use",
    "claude_agent_sdk",
    "crewai",
    "dspy",
    "instructor",
    "langchain",
    "langgraph",
    "livekit_agents",
    "llamaindex",
    "openai_agents",
    "semantic_kernel",
]
