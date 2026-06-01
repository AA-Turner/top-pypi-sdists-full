"""
Utility functions for OpenAI Agents SDK integration.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def is_openai_agents_available() -> bool:
    """Check if OpenAI Agents SDK is installed and importable.

    Returns:
        True if OpenAI Agents SDK is available
    """
    try:
        import agents

        return True
    except ImportError:
        try:
            import openai_agents

            return True
        except ImportError:
            return False


def get_openai_agents_version() -> str | None:
    """Get the installed OpenAI Agents SDK version.

    Returns:
        Version string or None if not installed
    """
    try:
        import agents

        return getattr(agents, "__version__", "unknown")
    except ImportError:
        try:
            import openai_agents

            return getattr(openai_agents, "__version__", "unknown")
        except ImportError:
            return None


def safe_str(value: Any, max_length: int = 1000) -> str:
    """Safely convert a value to string with length limit.

    Args:
        value: Value to convert
        max_length: Maximum length of output string

    Returns:
        String representation, truncated if necessary
    """
    try:
        if value is None:
            return ""
        s = str(value)
        if len(s) > max_length:
            return s[:max_length] + "..."
        return s
    except Exception as e:
        return f"<error: {e}>"


def extract_agent_info(agent: Any) -> dict[str, Any]:
    """Extract information from an OpenAI Agents SDK agent.

    Args:
        agent: The agent object

    Returns:
        Dictionary with agent information
    """
    info = {
        "name": None,
        "model": None,
        "tools": [],
        "handoffs": [],
        "has_instructions": False,
    }

    try:
        # Get name
        if hasattr(agent, "name"):
            info["name"] = agent.name

        # Get model
        if hasattr(agent, "model"):
            info["model"] = agent.model

        # Get tools
        if hasattr(agent, "tools"):
            tools = agent.tools or []
            info["tools"] = [
                getattr(t, "name", None) or getattr(t, "__name__", str(t)) for t in tools
            ]
            info["tool_count"] = len(info["tools"])

        # Get handoffs
        if hasattr(agent, "handoffs"):
            handoffs = agent.handoffs or []
            info["handoffs"] = [getattr(h, "name", None) or str(h) for h in handoffs]
            info["handoff_count"] = len(info["handoffs"])

        # Check for instructions
        if hasattr(agent, "instructions"):
            info["has_instructions"] = bool(agent.instructions)
            if agent.instructions:
                info["system_prompt"] = agent.instructions

        # Get guardrails
        if hasattr(agent, "input_guardrails"):
            info["input_guardrails"] = len(agent.input_guardrails) if agent.input_guardrails else 0
        if hasattr(agent, "output_guardrails"):
            info["output_guardrails"] = (
                len(agent.output_guardrails) if agent.output_guardrails else 0
            )

    except Exception as e:
        logger.debug(f"Error extracting agent info: {e}")

    return info


def extract_tool_info(tool: Any) -> dict[str, Any]:
    """Extract information from a tool/function.

    Args:
        tool: The tool object

    Returns:
        Dictionary with tool information
    """
    info = {
        "name": None,
        "type": type(tool).__name__,
        "description": None,
    }

    try:
        # Get name
        if hasattr(tool, "name"):
            info["name"] = tool.name
        elif hasattr(tool, "__name__"):
            info["name"] = tool.__name__

        # Get description
        if hasattr(tool, "description"):
            info["description"] = tool.description
        elif hasattr(tool, "__doc__") and tool.__doc__:
            info["description"] = tool.__doc__[:200]

        # Get parameters if available
        if hasattr(tool, "parameters"):
            params = tool.parameters
            if isinstance(params, dict):
                info["parameter_count"] = len(params.get("properties", {}))

    except Exception as e:
        logger.debug(f"Error extracting tool info: {e}")

    return info


def extract_handoff_info(handoff: Any) -> dict[str, Any]:
    """Extract information from a handoff definition.

    Args:
        handoff: The handoff object

    Returns:
        Dictionary with handoff information
    """
    info = {
        "name": None,
        "target_agent": None,
        "description": None,
    }

    try:
        # Get name
        if hasattr(handoff, "name"):
            info["name"] = handoff.name

        # Get target agent
        if hasattr(handoff, "agent"):
            target = handoff.agent
            if hasattr(target, "name"):
                info["target_agent"] = target.name

        # Get description
        if hasattr(handoff, "description"):
            info["description"] = handoff.description

    except Exception as e:
        logger.debug(f"Error extracting handoff info: {e}")

    return info


def extract_guardrail_info(guardrail: Any) -> dict[str, Any]:
    """Extract information from a guardrail.

    Args:
        guardrail: The guardrail object

    Returns:
        Dictionary with guardrail information
    """
    info = {
        "name": None,
        "type": type(guardrail).__name__,
        "description": None,
    }

    try:
        # Get name
        if hasattr(guardrail, "name"):
            info["name"] = guardrail.name
        elif hasattr(guardrail, "__name__"):
            info["name"] = guardrail.__name__

        # Get description
        if hasattr(guardrail, "description"):
            info["description"] = guardrail.description

    except Exception as e:
        logger.debug(f"Error extracting guardrail info: {e}")

    return info


def format_messages(messages: list[dict[str, Any]], max_messages: int = 10) -> str:
    """Format messages for tracing.

    Args:
        messages: List of message dictionaries
        max_messages: Maximum number of messages to include

    Returns:
        Formatted string representation
    """
    try:
        formatted = []

        for msg in messages[-max_messages:]:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            if isinstance(content, str):
                preview = content[:200] + "..." if len(content) > 200 else content
            elif isinstance(content, list):
                # Handle content arrays (e.g., with images)
                text_parts = [
                    p.get("text", "")
                    for p in content
                    if isinstance(p, dict) and p.get("type") == "text"
                ]
                preview = " ".join(text_parts)[:200]
            else:
                preview = str(content)[:200]

            formatted.append(f"{role}: {preview}")

        return "\n".join(formatted)

    except Exception as e:
        return f"<error formatting messages: {e}>"


def extract_workflow_summary(result: Any) -> dict[str, Any]:
    """Extract summary from a workflow result.

    Args:
        result: The workflow result object

    Returns:
        Dictionary with workflow summary
    """
    summary = {
        "output": None,
        "agent_chain": [],
        "tool_calls": 0,
        "handoffs": 0,
    }

    try:
        # Get final output
        if hasattr(result, "output"):
            output = result.output
            if isinstance(output, str):
                summary["output"] = output[:500] + "..." if len(output) > 500 else output
            else:
                summary["output"] = str(output)[:500]
        elif hasattr(result, "final_output"):
            summary["output"] = str(result.final_output)[:500]

        # Get agent chain
        if hasattr(result, "agent_chain"):
            summary["agent_chain"] = [getattr(a, "name", str(a)) for a in result.agent_chain]

        # Count tool calls
        if hasattr(result, "tool_calls"):
            summary["tool_calls"] = len(result.tool_calls) if result.tool_calls else 0

        # Count handoffs
        if hasattr(result, "handoffs"):
            summary["handoffs"] = len(result.handoffs) if result.handoffs else 0

        # Get usage if available
        if hasattr(result, "usage"):
            summary["usage"] = {
                "input_tokens": getattr(result.usage, "input_tokens", 0),
                "output_tokens": getattr(result.usage, "output_tokens", 0),
            }

    except Exception as e:
        logger.debug(f"Error extracting workflow summary: {e}")

    return summary


def mask_sensitive_content(content: str, patterns: list[str] | None = None) -> str:
    """Mask potentially sensitive content in strings.

    Args:
        content: Content to mask
        patterns: Optional list of regex patterns to mask

    Returns:
        Content with sensitive data masked
    """
    import re

    if not content:
        return content

    # Default patterns for common sensitive data
    default_patterns = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),
        (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),
        (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD]"),
        (r"\b\d{3}[-]?\d{2}[-]?\d{4}\b", "[SSN]"),
        (r"(?i)(password|secret|token|api_key|apikey|bearer)[\s]*[=:][\s]*[^\s,]+", "[REDACTED]"),
        (r"sk-[a-zA-Z0-9]{20,}", "[API_KEY]"),  # OpenAI API keys
    ]

    patterns_to_use = patterns if patterns is not None else default_patterns

    result = content
    for pattern, replacement in patterns_to_use:
        result = re.sub(pattern, replacement, result)

    return result
