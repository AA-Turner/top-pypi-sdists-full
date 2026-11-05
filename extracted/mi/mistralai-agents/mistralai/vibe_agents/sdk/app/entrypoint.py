from __future__ import annotations

import importlib
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from mistralai.vibe_agents.agents_client.api_models import is_reserved_agent_name
from mistralai.vibe_agents.sdk.authoring.agent import DEFAULT_AGENT_NAME, Agent

from . import errors
from ._unused_env import UnusedEnvironmentError

ENTRYPOINT_FORM = "module:attr"
# Used when a project declares none, so a single-file agent needs no configuration at all.
DEFAULT_ENTRYPOINT = "main:agent"


def resolve_agent(spec: str, root: Path) -> Agent:
    """Import ``module:attr`` from a project root and return the Agent it names."""

    module_name, separator, attribute = spec.partition(":")
    if not separator or not module_name.strip() or not attribute.strip():
        raise errors.AgentProjectError(
            f"Invalid entrypoint {spec!r}: expected the form {ENTRYPOINT_FORM}, e.g. 'main:agent'."
        )

    module_name, attribute = module_name.strip(), attribute.strip()
    with _project_on_path(root):
        try:
            module = importlib.import_module(module_name)
        except UnusedEnvironmentError:
            # Strict settings refused the environment while the module built a settings class; the
            # project itself is fine, so the refusal is not reported as a failed import.
            raise
        except Exception as exc:
            raise errors.AgentProjectError(
                f"Cannot import {module_name!r} from {root}: {type(exc).__name__}: {exc}"
            ) from exc

    try:
        agent = getattr(module, attribute)
    except AttributeError as exc:
        raise errors.AgentProjectError(
            f"{module_name!r} has no attribute {attribute!r}. "
            f"Assign the agent at module level, e.g. `{attribute} = agents.Agent(...)`."
        ) from exc
    if not isinstance(agent, Agent):
        raise errors.AgentProjectError(
            f"{spec} is a {type(agent).__name__}, not a mistralai.agents.Agent. "
            "Point the entrypoint at an Agent built with `from mistralai import agents`."
        )
    if agent.name == DEFAULT_AGENT_NAME or not agent.name.strip():
        raise errors.AgentProjectError(
            f"{spec} must set an explicit name: `agents.Agent(model=..., name=...)`. "
            "The name is the deployed workflow name. Set it in code even when you pass `--name`."
        )
    if is_reserved_agent_name(agent.name):
        raise errors.reserved_agent_name(agent.name)
    return agent


def resolve_agent_name(defined_name: str, override: str | None) -> str:
    """The name serve and deploy register the agent under: the `--name` override, else the agent's own."""

    agent_name = override or defined_name
    if is_reserved_agent_name(agent_name):
        raise errors.reserved_agent_name(agent_name)
    return agent_name


@contextmanager
def _project_on_path(root: Path) -> Iterator[None]:
    # A project is usually a flat script next to pyproject.toml rather than an installed package, so
    # its root has to be importable for the duration of the import.
    root_path = str(Path(root).resolve())
    if root_path in sys.path:
        yield
        return
    sys.path.insert(0, root_path)
    try:
        yield
    finally:
        sys.path.remove(root_path)
