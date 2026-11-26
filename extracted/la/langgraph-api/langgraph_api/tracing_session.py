"""LangSmith tracing session helpers."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

import structlog
from langsmith.utils import LangSmithUserError, get_tracer_project

try:
    from langsmith.address import (  # ty: ignore[unresolved-import]
        EnvAddressError,
        resolve_destination,
    )

    ADDRESS_SUPPORT = True
except ImportError:
    # langsmith predates agent addressing: runs trace into projects only.
    ADDRESS_SUPPORT = False

if TYPE_CHECKING:
    from langsmith.address import AgentAddress  # ty: ignore[unresolved-import]

logger = structlog.stdlib.get_logger(__name__)

Destination = tuple[str | None, "AgentAddress | None"]


def tracer_destination(payload: Mapping[str, Any]) -> Destination | None:
    """Return the destination a run's ``langsmith_tracer`` names, as ``(project, address)``.

    ``None`` when it names neither. A run goes to one or the other.

    Raises:
        ValueError: If the address is malformed, both are named, or the installed
            langsmith cannot trace to an address.
    """
    ls_tracing = payload.get("langsmith_tracer")
    if not isinstance(ls_tracing, Mapping):
        return None
    project_name = ls_tracing.get("project_name") or None
    if project_name is not None and not isinstance(project_name, str):
        raise ValueError("langsmith_tracer.project_name must be a string.")
    address = ls_tracing.get("address")
    if address is not None and not ADDRESS_SUPPORT:
        raise ValueError(
            "langsmith_tracer.address is not supported by the langsmith version installed here."
        )
    if project_name is None and address is None:
        return None
    if not ADDRESS_SUPPORT:
        return project_name, None
    try:
        return resolve_destination(project_name, address)
    except LangSmithUserError as exc:
        raise ValueError(f"Invalid langsmith_tracer: {exc}") from None


def deployment_destination() -> Destination:
    """The destination the deployment's own env vars trace into."""
    if not ADDRESS_SUPPORT:
        return get_tracer_project(), None
    try:
        return resolve_destination()
    except EnvAddressError:
        logger.exception(
            "Invalid LANGSMITH_AGENT_* configuration; tracing to the default project instead"
        )
        return get_tracer_project(), None


def resolve_tracing_session_name(payload: Mapping[str, Any]) -> str | None:
    """Return the LangSmith session (project) name for a run.

    Per-run ``langsmith_tracer.project_name`` overrides the deployment default
    from ``LANGSMITH_PROJECT`` / ``LANGCHAIN_PROJECT``. A run addressed to an
    agent, per run or by the deployment, has no project name: the endpoint
    resolves the address to its project.
    """
    project_name, _ = tracer_destination(payload) or deployment_destination()
    return project_name


def _replica(project_name: str | None, address: AgentAddress | None) -> dict[str, Any]:
    return {"address": address} if address else {"project_name": project_name}


def run_tracing_replicas(
    configurable: Mapping[str, Any],
) -> list[dict[str, Any]] | None:
    """Replicas for a run that names its own tracing destination, or ``None``.

    The run's destination comes first, then the deployment's default one, so the
    run lands in both.
    """
    project_name = configurable.get("__langsmith_project__") or None
    address = configurable.get("__langsmith_address__") or None
    if project_name is None and address is None:
        return None
    updates = None
    if example_id := configurable.get("__langsmith_example_id__"):
        updates = {"reference_example_id": example_id}
    return [
        {**_replica(project_name, address), "updates": updates},
        {**_replica(*deployment_destination()), "updates": None},
    ]
