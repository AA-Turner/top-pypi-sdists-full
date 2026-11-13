from __future__ import annotations

import warnings
from collections.abc import Iterable, Mapping
from typing import TYPE_CHECKING, Literal

from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.exceptions import WorkflowError

if TYPE_CHECKING:
    from mistralai.workflows.core.auth.run_as import ConnectorRunAs as ConnectorRunAs
    from mistralai.workflows.core.auth.run_as import RunAs as RunAs

    from .decorator import ConnectorSlot
    from .models import ResolvedConnectorBinding

else:
    # Cores 3.15–3.16 only ship the old name.
    try:
        from mistralai.workflows.core.auth.run_as import RunAs, _deprecated_alias_getattr
    except ImportError:
        from mistralai.workflows.core.auth.run_as import ConnectorRunAs

        RunAs = ConnectorRunAs
    else:
        __getattr__ = _deprecated_alias_getattr(__name__)


RunAsArg = RunAs | Literal["auto", "deployment"] | None


def require_connector_run_as(run_as: RunAs) -> RunAs:
    if run_as == RunAs.EXECUTOR:
        raise ValueError(
            "Invalid connector run_as 'executor'; it is for SDK clients only, expected 'auto' or 'deployment'"
        )
    return run_as


def require_connector_activity_run_as(run_as: RunAs) -> RunAs:
    """Like :func:`require_connector_run_as`, but fails the activity without retrying."""
    try:
        return require_connector_run_as(run_as)
    except ValueError as exc:
        raise WorkflowError(str(exc), non_retryable=True) from None


def normalize_run_as(value: RunAsArg) -> RunAs:
    """Coerce the public ``run_as=`` argument into a :class:`RunAs`.

    ``None`` (unspecified) maps to ``AUTO`` — follow the workflow's
    ``on_behalf_of`` flag.
    """
    if value is None:
        return RunAs.AUTO
    try:
        run_as = RunAs(value)
    except ValueError:
        raise ValueError(f"Invalid connector run_as {value!r}; expected 'auto', 'deployment', or None") from None
    return require_connector_run_as(run_as)


def use_executor_credentials_for(run_as: RunAs = RunAs.AUTO) -> bool:
    """Whether a connector running as ``run_as`` should use executor (OBO) credentials.

    ``DEPLOYMENT`` always uses the deployment's service identity; ``AUTO`` follows
    the workflow's ``on_behalf_of`` flag.

    Deprecated: removed in v4. Pass ``run_as`` to ``connector()`` or ``get_mistral_client()`` instead.
    """
    warnings.warn(
        "use_executor_credentials_for() is deprecated and will be removed in v4; "
        "pass run_as to connector() or get_mistral_client() instead.",
        FutureWarning,
        stacklevel=2,
    )
    if require_connector_run_as(run_as) == RunAs.DEPLOYMENT:
        return False
    context = retrieve_context()
    return bool(context and context.on_behalf_of)


def pinned_run_as_values(
    slots: Iterable["ConnectorSlot"],
    binding_by_name: Mapping[str, "ResolvedConnectorBinding"] | None = None,
) -> set[RunAs]:
    """The identities ``slots`` pin a conversation to.

    An explicit ``run_as`` pins that value. An omitted one means "inherit": it takes
    the preflight binding's identity, and pins nothing when there is no binding to
    inherit from.
    """
    pinned: set[RunAs] = set()
    for slot in slots:
        if slot.run_as_explicit:
            pinned.add(slot.run_as)
            continue
        binding = binding_by_name.get(slot.connector_name) if binding_by_name is not None else None
        if binding is not None:
            pinned.add(binding.run_as)
    return pinned


def raise_if_mixed_run_as(subject: str, run_as_values: set[RunAs]) -> None:
    """Reject connectors that mix ``run_as`` identities within one conversation."""
    if len(run_as_values) <= 1:
        return
    raise ValueError(
        f"{subject} mixes connector run_as values {sorted(v.value for v in run_as_values)}. "
        f"A conversation runs as a single identity, so all connectors must share the same "
        f"run_as; use ToolCallClient for per-connector identity."
    )
