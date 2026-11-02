"""DEPRECATED STEP TYPES — the one list, and the one sentence every scream uses.

A step type is deprecated by adding a record to ``deprecated_steps.json`` beside this
module (step type, one-sentence reason, replacement, date). While any workflow still
uses it, the platform screams everywhere a coding agent will see it — server boot,
every save / publish response, every run (log WARNING + one review flag per run +
a deduped ``system_error``), the release-health check, Workflow Studio's palette and
step card — until usages reach zero and the step is deleted (then it moves to
``validation.REMOVED_NODE_TYPES``). Guide: common-docs/systems/workflows/projects/
generic-only/DEPRECATION.md.

Deprecation never blocks: validation offers, never refuses. Every message is
addressed to agents and is built by :func:`deprecation_message` only.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from functools import cache
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

#: Stable ``system_error.kind`` / review-flag label for every deprecation scream.
DEPRECATED_STEP_ERROR_KIND = "workflow_deprecated_step_in_use"
DEPRECATED_STEP_FLAG_LABEL = "engine.deprecated_step"

_LIST_FILE = Path(__file__).with_name("deprecated_steps.json")


class StepDeprecation(BaseModel):
    """One deprecated step type."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    step_type: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    replacement: str = Field(min_length=1)
    deprecated_on: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


class DeprecatedUsage(BaseModel):
    """One node of one workflow that uses a deprecated step type."""

    model_config = ConfigDict(frozen=True)

    workflow_id: str
    workflow_name: str
    node_id: str
    step_type: str
    display_name: str
    deprecation: StepDeprecation

    @property
    def message(self) -> str:
        return deprecation_message(
            self.deprecation,
            display_name=self.display_name,
            node_id=self.node_id,
            workflow_name=self.workflow_name,
            workflow_id=self.workflow_id,
        )


def _parse(entries: Iterable[Mapping[str, Any]]) -> dict[str, StepDeprecation]:
    from matrx_graph.executor.registry import canonical_spec_type

    out: dict[str, StepDeprecation] = {}
    for raw in entries:
        record = StepDeprecation.model_validate(raw)
        key = canonical_spec_type(record.step_type)
        if key in out:
            raise ValueError(f"deprecated_steps.json lists {key!r} twice")
        out[key] = record
    return out


@cache
def _file_payload() -> dict[str, Any]:
    payload = json.loads(_LIST_FILE.read_text())
    if not isinstance(payload, dict) or not isinstance(payload.get("deprecated_steps"), list):
        raise ValueError(f"{_LIST_FILE} must hold an object with a 'deprecated_steps' list")
    return payload


_override: dict[str, StepDeprecation] | None = None


@cache
def _parsed_list() -> dict[str, StepDeprecation]:
    return _parse(_file_payload()["deprecated_steps"])


def deprecated_steps() -> dict[str, StepDeprecation]:
    """Every deprecated step type, keyed by canonical step type (parsed once per process —
    the scheduler asks on every step)."""
    if _override is not None:
        return dict(_override)
    return dict(_parsed_list())


def fixture_deprecations() -> list[StepDeprecation]:
    """The one record ``deprecated_steps.json`` carries for tests and ``--self-test`` only."""
    return list(_parse(_file_payload().get("test_fixture") or []).values())


@contextmanager
def use_deprecations(records: Iterable[StepDeprecation]) -> Iterator[None]:
    """Test / self-test seam: replace the list for the duration of the block."""
    global _override
    previous = _override
    _override = {r.step_type: r for r in records}
    try:
        yield
    finally:
        _override = previous


def deprecation_for(step_type: str | None) -> StepDeprecation | None:
    if not step_type:
        return None
    from matrx_graph.executor.registry import canonical_spec_type

    return deprecated_steps().get(canonical_spec_type(step_type))


def deprecation_message(
    deprecation: StepDeprecation,
    *,
    display_name: str,
    node_id: str,
    workflow_name: str,
    workflow_id: str,
) -> str:
    """THE sentence. Every scream — boot, save, publish, run, system_error, release check — uses it."""
    if workflow_name and workflow_name != workflow_id:
        workflow = f"'{workflow_name}' ({workflow_id})"
    else:
        workflow = workflow_id or "unsaved"
    return (
        f"DEPRECATED STEP IN USE: this workflow uses deprecated step {deprecation.step_type} "
        f"({display_name}) in step {node_id} of workflow {workflow}. "
        f"Why it is deprecated: {deprecation.reason} "
        "Any agent seeing this message is required to report it immediately "
        "(AI Dream MCP `feedback` tool) and fix it by replacing the step with "
        f"{deprecation.replacement}. This step will stop working when it is deleted "
        f"(deprecated {deprecation.deprecated_on})."
    )


def _node_spec_type(node: Any) -> str:
    if isinstance(node, Mapping):
        data = node.get("data") or {}
        from_data = data.get("spec_type") if isinstance(data, Mapping) else None
        if isinstance(from_data, str) and from_data:
            return from_data
        return str(node.get("type") or "")
    return str(getattr(node, "spec_type", "") or "")


def _display_name(step_type: str) -> str:
    from matrx_graph.executor.registry import default_registry

    registry = default_registry()
    if registry.has(step_type):
        return registry.get(step_type).spec.display_name
    return step_type


def find_deprecated_usages(
    nodes: Iterable[Any],
    *,
    workflow_id: str,
    workflow_name: str = "",
) -> list[DeprecatedUsage]:
    """Every node in ``nodes`` (raw dicts or ``NodeDef``) whose step type is deprecated."""
    table = deprecated_steps()
    if not table:
        return []
    found: list[DeprecatedUsage] = []
    for node in nodes:
        dep = deprecation_for(_node_spec_type(node))
        if dep is None:
            continue
        node_id = str(node.get("id") if isinstance(node, Mapping) else getattr(node, "id", ""))
        found.append(
            DeprecatedUsage(
                workflow_id=workflow_id,
                workflow_name=workflow_name,
                node_id=node_id,
                step_type=dep.step_type,
                display_name=_display_name(dep.step_type),
                deprecation=dep,
            )
        )
    return found


def palette_entry(step_type: str) -> dict[str, str] | None:
    """The ``deprecation`` field of a palette descriptor (Workflow Studio reads it)."""
    dep = deprecation_for(step_type)
    return dep.model_dump() if dep is not None else None


__all__ = [
    "DEPRECATED_STEP_ERROR_KIND",
    "DEPRECATED_STEP_FLAG_LABEL",
    "DeprecatedUsage",
    "StepDeprecation",
    "deprecated_steps",
    "deprecation_for",
    "deprecation_message",
    "find_deprecated_usages",
    "palette_entry",
    "fixture_deprecations",
    "use_deprecations",
]
