"""A child run started by a MODEL must arrive with something to answer.

Live 2026-10-16 (PB-02, Compass Mandate Desk → Lane Planner): the desk's first
``agent_call`` carried only ``variables={"destination_city": "Mexico City"}``.
Lane Planner has a system prompt and nothing else — no authored opening turn,
no declared variables — so the variable filled nothing, no user turn existed,
and the child reached the send boundary EMPTY (``empty_conversation``). The
tool error then told the model to "check the agent's variables and
configuration"; the model guessed ``user_input`` on its retry and succeeded.

Every tool that lets a model start a child agent run (``agent_call``, agent
tools) asks :func:`refuse_empty_child_turn` BEFORE the run. A child with no
turn of its own and no input is refused with a sentence the calling model can
act on: which argument to send, and which of the variables it sent the agent
does not declare. Nothing is authored on the caller's behalf — the platform
never invents a user message (variables are template values, not words).

:func:`empty_child_turn_guidance` is the same sentence for the late case the
pre-check cannot see: an authored opening turn that the variables filled with
nothing, refused by the send boundary as ``empty_conversation``.
"""

from __future__ import annotations

from typing import Any

EMPTY_CONVERSATION_ERROR_TYPE = "empty_conversation"
MISSING_CHILD_INPUT_ERROR_TYPE = "missing_user_input"

_INSTRUCTION_ROLES = frozenset({"system", "developer"})


def _role(message: Any) -> str:
    role = message.get("role") if isinstance(message, dict) else getattr(message, "role", None)
    return str(getattr(role, "value", role) or "")


def has_own_turn(agent: Any) -> bool | None:
    """Whether the agent carries any non-instruction message of its own.

    None when the agent exposes no message list (nothing to judge — the send
    boundary still guards the run).
    """
    config = getattr(agent, "config", None)
    messages = getattr(config, "messages", None)
    if messages is None:
        return None
    return any(_role(m) not in _INSTRUCTION_ROLES for m in messages)


def undeclared_variable_names(agent: Any, variables: dict[str, Any] | None) -> list[str]:
    """Names in ``variables`` the saved agent does not declare (they fill nothing)."""
    if not variables or not getattr(agent, "declares_variables", False):
        # An agent with no definitions keeps the caller's dict as its declaration.
        return []
    declared = set((getattr(agent, "variable_defaults", None) or {}).keys())
    return sorted(str(name) for name in variables if name not in declared)


def _has_input(user_input: Any) -> bool:
    if isinstance(user_input, str):
        return bool(user_input.strip())
    return bool(user_input)


def empty_child_turn_guidance(
    agent_name: str,
    *,
    input_arg: str,
    undeclared: list[str] | None = None,
) -> tuple[str, str]:
    """(message, suggested_action) telling the calling model what to send."""
    message = (
        f"Agent '{agent_name}' received no message: it has instructions but no "
        f"turn of its own, and this call passed no {input_arg}. Nothing ran and "
        "nothing was spent."
    )
    if undeclared:
        names = ", ".join(undeclared)
        message += (
            f" The variables you sent ({names}) are not declared by this agent, "
            "so they filled nothing — variables are template values, never a message."
        )
    suggested = (
        f"Call again with {input_arg} set to the request for '{agent_name}' in plain "
        "words (put the values it needs in that text)."
    )
    return message, suggested


def refuse_empty_child_turn(
    agent: Any,
    *,
    user_input: Any,
    variables: dict[str, Any] | None,
    input_arg: str,
) -> tuple[str, str] | None:
    """The refusal for a child that would arrive empty, else None.

    Judges ROLES only — an authored opening turn whose text the variables fill
    is a turn; whether its filled text is empty is the send boundary's call
    (see :func:`empty_child_turn_guidance` for that late refusal).
    """
    if _has_input(user_input):
        return None
    if has_own_turn(agent) is not False:
        return None
    name = getattr(agent, "name", None) or "the agent"
    return empty_child_turn_guidance(
        str(name),
        input_arg=input_arg,
        undeclared=undeclared_variable_names(agent, variables),
    )
