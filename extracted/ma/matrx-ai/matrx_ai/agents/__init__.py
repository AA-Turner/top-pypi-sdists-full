"""
AI Agents Module

Core components for agent-based AI interactions:
- Agent: Main class for executing prompts with variable support
- AgentCache: In-memory cache for multi-turn conversations
- AgentVariable: Variable definition for prompt templates
- AgentConfig: Configuration container for agent initialization
- AgentExecuteResult: Return type from Agent.execute()
- AgentRunResult: Typed result returned by run_agent (executor)
- run_agent: Canonical executor; wraps Agent.execute in child_agent_context
- NamedAgent: Declarative class-based agent definition with typed Pydantic Inputs/Output
- AgentSource / AgentRecordSource / AnyIdAgentSource / InlineAgentSource: NamedAgent loader descriptors
- ConversationResolver: Resolves UnifiedConfig from conversation_id
- AgentConfigResolver: Resolves UnifiedConfig from agent/prompt id
- pm: PromptManagers aggregator — single access point for prompt/builtin operations

Usage:
    from matrx_ai.agents import Agent, run_agent, AgentRunResult
    from matrx_ai.agents import NamedAgent, AgentRecordSource, InlineAgentSource
    from matrx_ai.agents import ConversationResolver, AgentConfigResolver
"""

__all__ = [
    "Agent",
    "AgentCache",
    "AgentConfig",
    "AgentConfigResolver",
    "AgentExecuteResult",
    "AgentRecordSource",
    "AgentRunResult",
    "AgentSource",
    "AgentValidationReport",
    "AgentVariable",
    "AnyIdAgentSource",
    "iter_registered_named_agents",
    "validate_all_named_agents",
    "ConversationResolver",
    "hydrate_persisted_history",
    "InlineAgentSource",
    "NamedAgent",
    "PromptManagers",
    "PromptType",
    "SchemaCoerceAgent",
    "SchemaCoerceErrorResponse",
    "SchemaCoerceInputs",
    "SchemaCoerceResult",
    "JsonExtraction",
    "extract_json",
    "extract_json_block",
    "extract_model",
    "parse_agent_output",
    "pm",
    "resolve_output_schema",
    "run_agent",
    "to_template_value",
]


def __getattr__(name: str):
    """Lazy import to avoid circular dependencies."""
    if name == "Agent":
        from matrx_ai.agents.definition import Agent

        return Agent
    elif name == "AgentCache":
        from matrx_ai.agents.cache import AgentCache

        return AgentCache
    elif name == "AgentConfig":
        from matrx_ai.agents.types import AgentConfig

        return AgentConfig
    elif name == "AgentConfigResolver":
        from matrx_ai.agents.resolver import AgentConfigResolver

        return AgentConfigResolver
    elif name == "AgentExecuteResult":
        from matrx_ai.agents.definition import AgentExecuteResult

        return AgentExecuteResult
    elif name == "AgentRunResult":
        from matrx_ai.agents.executor import AgentRunResult

        return AgentRunResult
    elif name == "run_agent":
        from matrx_ai.agents.executor import run_agent

        return run_agent
    elif name == "NamedAgent":
        from matrx_ai.agents.named import NamedAgent

        return NamedAgent
    elif name == "AgentValidationReport":
        from matrx_ai.agents.named import AgentValidationReport

        return AgentValidationReport
    elif name == "iter_registered_named_agents":
        from matrx_ai.agents.named import iter_registered_named_agents

        return iter_registered_named_agents
    elif name == "validate_all_named_agents":
        from matrx_ai.agents.named import validate_all_named_agents

        return validate_all_named_agents
    elif name == "AgentSource":
        from matrx_ai.agents.named import AgentSource

        return AgentSource
    elif name == "AgentRecordSource":
        from matrx_ai.agents.named import AgentRecordSource

        return AgentRecordSource
    elif name == "AnyIdAgentSource":
        from matrx_ai.agents.named import AnyIdAgentSource

        return AnyIdAgentSource
    elif name == "InlineAgentSource":
        from matrx_ai.agents.named import InlineAgentSource

        return InlineAgentSource
    elif name == "AgentVariable":
        from matrx_ai.agents.variables import AgentVariable

        return AgentVariable
    elif name == "ConversationResolver":
        from matrx_ai.agents.resolver import ConversationResolver

        return ConversationResolver
    elif name == "hydrate_persisted_history":
        from matrx_ai.agents.history_hydration import hydrate_persisted_history

        return hydrate_persisted_history
    elif name == "PromptManagers":
        from matrx_ai.agents.DEPRECATED_prompts_manager import PromptManagers

        return PromptManagers
    elif name == "PromptType":
        from matrx_ai.agents.DEPRECATED_prompts_manager import PromptType

        return PromptType
    elif name == "pm":
        from matrx_ai.agents.DEPRECATED_prompts_manager import pm

        return pm
    elif name == "to_template_value":
        from matrx_ai.agents.named import to_template_value

        return to_template_value
    elif name == "extract_json_block":
        from matrx_ai.agents.executor import extract_json_block

        return extract_json_block
    elif name == "extract_json":
        from matrx_ai.agents.response_parser import extract_json

        return extract_json
    elif name == "extract_model":
        from matrx_ai.agents.response_parser import extract_model

        return extract_model
    elif name == "JsonExtraction":
        from matrx_ai.agents.response_parser import JsonExtraction

        return JsonExtraction
    elif name == "parse_agent_output":
        from matrx_ai.agents.output import parse_agent_output

        return parse_agent_output
    elif name == "resolve_output_schema":
        from matrx_ai.agents.output import resolve_output_schema

        return resolve_output_schema
    elif name == "SchemaCoerceAgent":
        from matrx_ai.agents.library import SchemaCoerceAgent

        return SchemaCoerceAgent
    elif name == "SchemaCoerceErrorResponse":
        from matrx_ai.agents.library import SchemaCoerceErrorResponse

        return SchemaCoerceErrorResponse
    elif name == "SchemaCoerceInputs":
        from matrx_ai.agents.library import SchemaCoerceInputs

        return SchemaCoerceInputs
    elif name == "SchemaCoerceResult":
        from matrx_ai.agents.library import SchemaCoerceResult

        return SchemaCoerceResult
    raise AttributeError(f"module 'matrx_ai.agents' has no attribute '{name}'")
