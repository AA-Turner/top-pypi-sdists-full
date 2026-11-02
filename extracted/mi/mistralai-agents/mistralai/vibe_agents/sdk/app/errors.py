from __future__ import annotations

from pathlib import Path

from mistralai.vibe_agents.agents_client.api_models import reserved_agent_name_message
from mistralai.vibe_agents.sdk.authoring.errors import SdkError

__all__ = [
    "AgentProjectError",
    "conflicting_connectors_slots",
    "duplicate_name",
    "harness_build_error",
    "harness_conflict",
    "invalid_project_runtime",
    "missing_agent_file",
    "missing_agent_name",
    "reserved_agent_name",
    "slot_import_error",
    "wrong_agent_count",
    "wrong_object_count",
]


class AgentProjectError(SdkError):
    """Raised when a file-defined agent project is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def missing_agent_file(root: Path) -> AgentProjectError:
    return AgentProjectError(
        f"No agent found: expected 'agent/agent.py' under {root}. Create it with `agent = agents.Agent(model=...)`."
    )


def missing_agent_name(root: Path) -> AgentProjectError:
    return AgentProjectError(
        f"agent/agent.py under {root} must set an explicit name: `agents.Agent(model=..., name=...)`. "
        "The name is the deployed workflow name."
    )


def reserved_agent_name(name: str) -> AgentProjectError:
    return AgentProjectError(
        f"{reserved_agent_name_message(name)}. Choose another name with "
        "`agents.Agent(model=..., name=...)` or `--name`."
    )


def wrong_agent_count(rel: str, found: int, names: list[str]) -> AgentProjectError:
    detail = f" ({', '.join(names)})" if names else ""
    return AgentProjectError(
        f"{rel} must define exactly one agents.Agent; found {found}{detail}. "
        "Define a single `agent = agents.Agent(...)`."
    )


def wrong_object_count(rel: str, kind: str, found: int, hint: str) -> AgentProjectError:
    return AgentProjectError(f"{rel} must define exactly one {kind}; found {found}. {hint}")


def duplicate_name(kind: str, name: str, first: str, second: str) -> AgentProjectError:
    return AgentProjectError(f"Duplicate {kind} name {name!r} defined in {first} and {second}. Names must be unique.")


def slot_import_error(rel: str, exc: BaseException) -> AgentProjectError:
    return AgentProjectError(f"Failed to load {rel}: {type(exc).__name__}: {exc}")


def harness_build_error(exc: BaseException) -> AgentProjectError:
    return AgentProjectError(str(exc))


def missing_skill_file(rel: str) -> AgentProjectError:
    return AgentProjectError(
        f"Skill directory {rel} has no SKILL.md file. "
        "Add a SKILL.md with YAML frontmatter (name, description) and a markdown body."
    )


def invalid_skill_file(rel: str, exc: BaseException) -> AgentProjectError:
    return AgentProjectError(f"Failed to parse {rel}: {type(exc).__name__}: {exc}")


def invalid_project_runtime(exc: BaseException) -> AgentProjectError:
    return AgentProjectError(str(exc))


def conflicting_connectors_slots(root: Path) -> AgentProjectError:
    return AgentProjectError(
        f"{root} has both agent/connectors/ and agent/connections/. "
        "agent/connections/ is deprecated; remove it and keep agent/connectors/."
    )


def harness_conflict(conflicts: list[str]) -> AgentProjectError:
    names = ", ".join(f"agent/{name}" for name in conflicts)
    return AgentProjectError(
        f"agent/harness.py takes full control of the harness and cannot coexist with discovered slots ({names}). "
        "Move that wiring into harness.py, or delete harness.py to use slot discovery."
    )
