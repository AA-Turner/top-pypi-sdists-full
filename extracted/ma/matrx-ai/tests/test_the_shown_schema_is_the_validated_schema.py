"""The schema a model is SHOWN is the schema its call is VALIDATED against — every provider.

Defect 43 (live 2026-10-18 07:36Z, PB-02 calls 1 and 7a; PB-03 conversation 6b861a8b…):
the ``agent`` row in ``tool.definition`` advertised ``settings``, ``variables``,
``remember``, ``result_mode`` and ``result_key`` while the deployed ``ToolArgs`` model
forbade them, so calls built from the shown schema were refused
(``Extra inputs are not permitted``) and the model burned turns guessing. The reverse
skew — code requiring a field the row does not show yet — refuses every call.

SUT: ``ToolRegistry._load_rows`` (the row beside its declared ``ToolArgs``), then
``ToolDefinition.get_provider_format`` for every provider. A call made of exactly the
shown properties (all of them, required ones present) must validate; a call missing a
shown-required property must be the only kind refused for "required".
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from pydantic import Field

from matrx_ai.tools.declared import ToolArgs
from matrx_ai.tools.models import ToolDefinition

PROVIDERS = ["openai", "anthropic", "google", "cerebras", "xai", "together", "groq", "generic_openai"]


class _RunningCodeArgs(ToolArgs):
    """The deployed validator: a narrower model than the row (05:23 build)."""

    agent_id: str = Field(description="The id of the agent to call.")
    prompt: str | None = Field(default=None, description="The task.")
    description: str | None = Field(default=None, description="A label.")


#: The row as stored (the 06:22 update): advertises fields the code forbids and
#: does not show the code's required ``agent_id``.
_ROW_PARAMETERS: dict[str, Any] = {
    "prompt": {"type": "string", "default": None, "description": "The task."},
    "description": {"type": "string", "default": None, "description": "A label."},
    "subagent_type": {"type": "string", "default": None, "description": "Which agent."},
    "settings": {"type": "object", "default": None, "description": "Model settings."},
    "variables": {"type": "object", "default": None, "description": "Variables."},
    "remember": {"type": "boolean", "default": False, "description": "Remember."},
    "result_mode": {"type": "string", "enum": ["inline", "reference"], "default": "inline"},
}


def _shown(fmt: dict[str, Any]) -> dict[str, Any]:
    """The JSON-schema object a provider format carries, wherever it nests it."""
    stack: list[Any] = [fmt]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            if isinstance(node.get("properties"), dict):
                return node
            stack.extend(node.values())
    raise AssertionError(f"no schema in {fmt}")


def _sample(prop: dict[str, Any]) -> Any:
    kind = str(prop.get("type", "string")).lower()
    if prop.get("enum"):
        return prop["enum"][0]
    return {"object": {}, "boolean": False, "integer": 1, "number": 1, "array": []}.get(kind, "x")


async def _run(args: dict[str, Any], ctx: Any) -> Any:  # the declared implementation
    return None


def _loaded(monkeypatch: pytest.MonkeyPatch) -> ToolDefinition:
    """The row loaded the way the server loads it, beside its declared code."""
    import matrx_ai.tools.declared as declared

    from matrx_ai.tools.registry import ToolRegistry

    declaration = SimpleNamespace(
        function_path="tests.agent_skew", func=_run, args_model=_RunningCodeArgs
    )
    real = declared.get_effective_declared
    monkeypatch.setattr(
        declared,
        "get_effective_declared",
        lambda name: declaration if name == "agent_skew" else real(name),
    )
    registry = ToolRegistry()
    registry._load_rows(
        [
            {
                "id": "6a1c0f7e-0000-4000-8000-0000000000aa",
                "name": "agent_skew",
                "description": "Start another agent.",
                "parameters": {k: dict(v) for k, v in _ROW_PARAMETERS.items()},
                "source_kind": "native",
            }
        ]
    )
    return registry._tools["agent_skew"]


@pytest.mark.parametrize("provider", PROVIDERS)
def test_every_shown_property_validates(provider: str, monkeypatch: pytest.MonkeyPatch) -> None:
    schema = _shown(_loaded(monkeypatch).get_provider_format(provider))
    call = {name: _sample(prop) for name, prop in schema["properties"].items()}
    _RunningCodeArgs.model_validate(call)  # raises on any shown-but-forbidden key


@pytest.mark.parametrize("provider", PROVIDERS)
def test_what_the_code_requires_is_shown_required(provider: str, monkeypatch: pytest.MonkeyPatch) -> None:
    schema = _shown(_loaded(monkeypatch).get_provider_format(provider))
    required = {n for n, f in _RunningCodeArgs.model_fields.items() if f.is_required()}
    assert required <= set(schema["properties"]), schema["properties"].keys()
    assert required <= set(schema.get("required") or []), schema.get("required")

