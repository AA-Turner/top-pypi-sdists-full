"""
Utility functions for AutoGen/AG2 integration.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def is_autogen_available() -> bool:
    """Check if AutoGen/AG2 is installed and importable.

    Returns:
        True if AutoGen/AG2 is available
    """
    try:
        # Try ag2 first (newer package name)
        import ag2

        return True
    except ImportError:
        try:
            import autogen

            return True
        except ImportError:
            return False


def get_autogen_version() -> str | None:
    """Get the installed AutoGen/AG2 version.

    Returns:
        Version string or None if not installed
    """
    try:
        # Try ag2 first
        try:
            import ag2

            return getattr(ag2, "__version__", "unknown")
        except ImportError:
            import autogen

            return getattr(autogen, "__version__", "unknown")
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
    """Extract information from an AutoGen Agent.

    Args:
        agent: The AutoGen Agent object

    Returns:
        Dictionary with agent information
    """
    info = {
        "name": getattr(agent, "name", "unknown"),
        "type": type(agent).__name__,
        "human_input_mode": None,
        "llm_config": None,
        "code_execution_config": None,
    }

    try:
        # Get human_input_mode
        info["human_input_mode"] = getattr(agent, "human_input_mode", None)

        # Get LLM config summary
        llm_config = getattr(agent, "llm_config", None)
        if llm_config and isinstance(llm_config, dict):
            config_list = llm_config.get("config_list", [])
            if config_list:
                first_config = config_list[0] if config_list else {}
                info["llm_config"] = {
                    "model": first_config.get("model", "unknown"),
                    "temperature": llm_config.get("temperature"),
                }

        # Get code execution config
        code_config = getattr(agent, "code_execution_config", None)
        if code_config and isinstance(code_config, dict):
            info["code_execution_config"] = {
                "work_dir": code_config.get("work_dir"),
                "use_docker": code_config.get("use_docker", False),
            }

    except Exception as e:
        logger.debug(f"Error extracting agent info: {e}")

    return info


def extract_message_info(message: Any) -> dict[str, Any]:
    """Extract information from an AutoGen message.

    Args:
        message: The message object or dict

    Returns:
        Dictionary with message information
    """
    info = {
        "role": None,
        "content_length": 0,
        "has_function_call": False,
        "function_name": None,
    }

    try:
        if isinstance(message, dict):
            info["role"] = message.get("role")
            content = message.get("content", "")
            info["content_length"] = len(content) if content else 0

            # Check for function call
            function_call = message.get("function_call") or message.get("tool_calls")
            if function_call:
                info["has_function_call"] = True
                if isinstance(function_call, dict):
                    info["function_name"] = function_call.get("name")
                elif isinstance(function_call, list) and function_call:
                    first_call = function_call[0]
                    if isinstance(first_call, dict):
                        func = first_call.get("function", {})
                        info["function_name"] = func.get("name")

        elif hasattr(message, "content"):
            content = getattr(message, "content", "")
            info["content_length"] = len(content) if content else 0
            info["role"] = getattr(message, "role", None)

    except Exception as e:
        logger.debug(f"Error extracting message info: {e}")

    return info


def extract_conversation_summary(chat_history: list[Any]) -> dict[str, Any]:
    """Extract summary from a conversation history.

    Args:
        chat_history: List of messages

    Returns:
        Dictionary with conversation summary
    """
    summary = {
        "message_count": len(chat_history) if chat_history else 0,
        "participants": set(),
        "function_calls": 0,
        "code_blocks": 0,
    }

    try:
        for message in chat_history or []:
            if isinstance(message, dict):
                # Track participants
                sender = message.get("name") or message.get("role", "unknown")
                summary["participants"].add(sender)

                # Count function calls
                if message.get("function_call") or message.get("tool_calls"):
                    summary["function_calls"] += 1

                # Count code blocks
                content = message.get("content", "")
                if "```" in str(content):
                    summary["code_blocks"] += content.count("```") // 2

        summary["participants"] = list(summary["participants"])

    except Exception as e:
        logger.debug(f"Error extracting conversation summary: {e}")
        summary["participants"] = []

    return summary


def extract_group_chat_info(groupchat: Any) -> dict[str, Any]:
    """Extract information from an AutoGen GroupChat.

    Args:
        groupchat: The GroupChat object

    Returns:
        Dictionary with group chat information
    """
    info = {
        "agent_count": 0,
        "agent_names": [],
        "max_round": None,
        "admin_name": None,
        "speaker_selection_method": None,
    }

    try:
        # Get agents
        agents = getattr(groupchat, "agents", [])
        info["agent_count"] = len(agents)
        info["agent_names"] = [getattr(a, "name", "unknown") for a in agents]

        # Get configuration
        info["max_round"] = getattr(groupchat, "max_round", None)
        info["admin_name"] = getattr(groupchat, "admin_name", None)
        info["speaker_selection_method"] = getattr(groupchat, "speaker_selection_method", None)

    except Exception as e:
        logger.debug(f"Error extracting group chat info: {e}")

    return info


def get_conversation_participants(chat_result: Any) -> list[str]:
    """Extract participant names from a chat result.

    Args:
        chat_result: The result from initiate_chat

    Returns:
        List of participant names
    """
    participants = []

    try:
        # Try to get chat history
        chat_history = getattr(chat_result, "chat_history", [])
        if not chat_history and isinstance(chat_result, dict):
            chat_history = chat_result.get("chat_history", [])

        names = set()
        for message in chat_history or []:
            if isinstance(message, dict):
                name = message.get("name") or message.get("role")
                if name:
                    names.add(name)

        participants = list(names)

    except Exception as e:
        logger.debug(f"Error getting conversation participants: {e}")

    return participants


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
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),  # Email
        (r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", "[PHONE]"),  # Phone
        (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[CARD]"),  # Credit card
        (r"\b\d{3}[-]?\d{2}[-]?\d{4}\b", "[SSN]"),  # SSN
        (r"(?i)(password|secret|token|api_key|apikey)[\s]*[=:]\s*[^\s,]+", "[REDACTED]"),  # Keys
    ]

    patterns_to_use = patterns if patterns is not None else default_patterns

    result = content
    for pattern, replacement in patterns_to_use:
        result = re.sub(pattern, replacement, result)

    return result
