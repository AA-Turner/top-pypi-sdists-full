"""Runner factory for creating agent runners.

This module provides factory functions to create AgentRunner instances
with the appropriate configuration.
"""

from pathlib import Path
from typing import Optional, TYPE_CHECKING

from .agent_runner import AgentRunner
from ...utils.logger import log

if TYPE_CHECKING:
    from ..events import AgentEventEmitter


def get_runner(
    model: str,
    cwd: Optional[str] = None,
    emitter: Optional["AgentEventEmitter"] = None,
    system_prompt: Optional[str] = None,
    plan_mode: bool = False,
    session_id: Optional[str] = None,
    **kwargs,
) -> AgentRunner:
    """Get an AgentRunner for the specified model.

    Args:
        model: Model string (e.g., "minimax", "fireworks:accounts/fireworks/models/minimax-m2p1")
        cwd: Working directory
        emitter: Event emitter for streaming
        system_prompt: Custom system prompt
        plan_mode: If True, restrict to read-only tools
        session_id: Session ID for plan file isolation. If None, generates a new one.
        **kwargs: Additional arguments passed to runner

    Returns:
        AgentRunner instance

    Example:
        runner = get_runner("minimax")
        runner = get_runner("fireworks:accounts/fireworks/models/minimax-m2p1")
    """
    log.info(f"Using AgentRunner for model: {model}")

    # Import toolkit here to avoid circular imports
    from ..toolkit import AgentToolkit
    import uuid

    # Generate session_id if not provided
    if session_id is None:
        session_id = str(uuid.uuid4())

    # Generate plan file path when in plan mode
    # Use session-specific path in ~/.emdash/sessions/{session_id}/ to avoid persistence issues
    plan_file_path = None
    repo_root = Path(cwd) if cwd else Path.cwd()
    if plan_mode:
        session_plan_dir = Path.home() / ".emdash" / "sessions" / session_id
        session_plan_dir.mkdir(parents=True, exist_ok=True)
        plan_file_path = str(session_plan_dir / "plan.md")

    toolkit = AgentToolkit(
        repo_root=repo_root,
        plan_mode=plan_mode,
        plan_file_path=plan_file_path,
    )

    return AgentRunner(
        toolkit=toolkit,
        model=model,
        emitter=emitter,
        system_prompt=system_prompt,
        session_id=session_id,
        **kwargs,
    )


def create_hybrid_runner(
    model: str,
    **kwargs,
) -> AgentRunner:
    """Convenience alias for get_runner.

    Args:
        model: Model string
        **kwargs: Passed to get_runner

    Returns:
        AgentRunner instance
    """
    return get_runner(model, **kwargs)
