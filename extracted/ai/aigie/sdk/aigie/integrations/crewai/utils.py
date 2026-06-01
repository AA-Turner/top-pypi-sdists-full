"""
Utility functions for CrewAI integration.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


def is_crewai_available() -> bool:
    """Check if CrewAI is installed and importable.

    Returns:
        True if CrewAI is available
    """
    try:
        import crewai

        return True
    except ImportError:
        return False


def get_crewai_version() -> str | None:
    """Get the installed CrewAI version.

    Returns:
        Version string or None if not installed
    """
    try:
        import crewai

        return getattr(crewai, "__version__", "unknown")
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
    """Extract information from a CrewAI Agent.

    Args:
        agent: The CrewAI Agent object

    Returns:
        Dictionary with agent information
    """
    info = {
        "role": getattr(agent, "role", "unknown"),
        "goal": None,
        "backstory": None,
        "allow_delegation": getattr(agent, "allow_delegation", False),
        "tools": [],
        "llm": None,
    }

    try:
        # Get goal
        goal = getattr(agent, "goal", None)
        if goal:
            info["goal"] = safe_str(goal, 500)

        # Get backstory
        backstory = getattr(agent, "backstory", None)
        if backstory:
            info["backstory"] = safe_str(backstory, 500)

        # Get tools
        tools = getattr(agent, "tools", []) or []
        info["tools"] = [getattr(t, "name", str(t)[:50]) for t in tools[:10]]

        # Get LLM info
        llm = getattr(agent, "llm", None)
        if llm:
            info["llm"] = {
                "model": getattr(llm, "model_name", None) or getattr(llm, "model", "unknown"),
                "temperature": getattr(llm, "temperature", None),
            }

    except Exception as e:
        logger.debug(f"Error extracting agent info: {e}")

    return info


def extract_task_info(task: Any) -> dict[str, Any]:
    """Extract information from a CrewAI Task.

    Args:
        task: The CrewAI Task object

    Returns:
        Dictionary with task information
    """
    info = {
        "description": None,
        "expected_output": None,
        "agent_role": None,
        "context_count": 0,
        "tools": [],
    }

    try:
        # Get description
        description = getattr(task, "description", None)
        if description:
            info["description"] = safe_str(description, 500)

        # Get expected output
        expected_output = getattr(task, "expected_output", None)
        if expected_output:
            info["expected_output"] = safe_str(expected_output, 300)

        # Get assigned agent
        agent = getattr(task, "agent", None)
        if agent:
            info["agent_role"] = getattr(agent, "role", "unknown")

        # Get context tasks
        context = getattr(task, "context", []) or []
        info["context_count"] = len(context)

        # Get tools
        tools = getattr(task, "tools", []) or []
        info["tools"] = [getattr(t, "name", str(t)[:50]) for t in tools[:10]]

    except Exception as e:
        logger.debug(f"Error extracting task info: {e}")

    return info


def extract_crew_info(crew: Any) -> dict[str, Any]:
    """Extract information from a CrewAI Crew.

    Args:
        crew: The CrewAI Crew object

    Returns:
        Dictionary with crew information
    """
    info = {
        "name": getattr(crew, "name", "unnamed"),
        "process_type": "sequential",
        "agent_count": 0,
        "task_count": 0,
        "verbose": getattr(crew, "verbose", False),
        "agents": [],
        "tasks": [],
    }

    try:
        # Get process type
        process = getattr(crew, "process", None)
        if process:
            if hasattr(process, "value"):
                info["process_type"] = process.value
            else:
                info["process_type"] = str(process)

        # Get agents
        agents = getattr(crew, "agents", []) or []
        info["agent_count"] = len(agents)
        info["agents"] = [
            {
                "role": getattr(a, "role", "unknown"),
                "allow_delegation": getattr(a, "allow_delegation", False),
            }
            for a in agents
        ]

        # Get tasks
        tasks = getattr(crew, "tasks", []) or []
        info["task_count"] = len(tasks)
        info["tasks"] = [
            {
                "description": safe_str(getattr(t, "description", ""), 100),
                "agent_role": getattr(getattr(t, "agent", None), "role", None),
            }
            for t in tasks
        ]

    except Exception as e:
        logger.debug(f"Error extracting crew info: {e}")

    return info


def format_step_output(step_output: Any) -> dict[str, Any]:
    """Format a CrewAI step output for tracing.

    Args:
        step_output: The step output object

    Returns:
        Formatted dictionary
    """
    formatted = {}

    try:
        # Extract thought/reasoning
        thought = getattr(step_output, "thought", None) or getattr(step_output, "text", None)
        if thought:
            formatted["thought"] = safe_str(thought, 500)

        # Extract action/tool
        action = getattr(step_output, "tool", None) or getattr(step_output, "action", None)
        if action:
            formatted["action"] = str(action)

        # Extract action input
        action_input = getattr(step_output, "tool_input", None) or getattr(
            step_output, "action_input", None
        )
        if action_input:
            formatted["action_input"] = safe_str(action_input, 300)

        # Extract observation/result
        observation = getattr(step_output, "result", None) or getattr(
            step_output, "observation", None
        )
        if observation:
            formatted["observation"] = safe_str(observation, 500)

        # Extract final answer
        final_answer = getattr(step_output, "final_answer", None)
        if final_answer:
            formatted["final_answer"] = safe_str(final_answer, 1000)

    except Exception as e:
        logger.debug(f"Error formatting step output: {e}")

    return formatted


def get_execution_path(crew_result: Any) -> list[dict[str, Any]]:
    """Extract the execution path from a crew result.

    Args:
        crew_result: The result from crew.kickoff()

    Returns:
        List of execution steps with agent and task info
    """
    path = []

    try:
        # Try to get tasks_output
        tasks_output = getattr(crew_result, "tasks_output", []) or []
        for output in tasks_output:
            step = {
                "description": safe_str(getattr(output, "description", ""), 200),
                "agent_role": getattr(output, "agent", "unknown"),
                "output": safe_str(
                    getattr(output, "raw_output", "") or getattr(output, "output", ""), 500
                ),
            }
            path.append(step)

    except Exception as e:
        logger.debug(f"Error extracting execution path: {e}")

    return path


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
