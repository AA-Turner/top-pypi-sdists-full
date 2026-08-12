from __future__ import annotations

from collections.abc import Iterable, Mapping
from enum import Enum
from typing import TYPE_CHECKING, Literal

from mistralai.workflows.client import should_use_executor_credentials

if TYPE_CHECKING:
    from .decorator import ConnectorSlot
    from .models import ResolvedConnectorBinding


class ConnectorRunAs(str, Enum):
    """Which identity a connector runs as for its preflight and tool calls.

    - ``AUTO`` — follow the workflow's ``on_behalf_of`` flag: the executing
      user's credentials when the workflow runs on behalf of a user, the
      deployment's service credentials otherwise. This is the default,
      backward-compatible behaviour.
    - ``DEPLOYMENT`` — always the deployment's (worker's) service identity.
    """

    AUTO = "auto"
    DEPLOYMENT = "deployment"


RunAsArg = Literal["auto", "deployment"] | None


def normalize_run_as(value: RunAsArg) -> ConnectorRunAs:
    """Coerce the public ``run_as=`` argument into a :class:`ConnectorRunAs`.

    ``None`` (unspecified) maps to ``AUTO`` — follow the workflow's
    ``on_behalf_of`` flag.
    """
    if value is None:
        return ConnectorRunAs.AUTO
    try:
        return ConnectorRunAs(value)
    except ValueError:
        raise ValueError(f"Invalid connector run_as {value!r}; expected 'auto', 'deployment', or None") from None


def use_executor_credentials_for(run_as: ConnectorRunAs = ConnectorRunAs.AUTO) -> bool:
    """Whether a connector running as ``run_as`` should use executor (OBO) credentials.

    ``DEPLOYMENT`` always uses the deployment's service identity; ``AUTO`` follows
    the workflow's ``on_behalf_of`` flag.
    """
    if run_as == ConnectorRunAs.DEPLOYMENT:
        return False
    return should_use_executor_credentials()


def pinned_run_as_values(
    slots: Iterable["ConnectorSlot"],
    binding_by_name: Mapping[str, "ResolvedConnectorBinding"] | None = None,
) -> set[ConnectorRunAs]:
    """The identities ``slots`` pin a conversation to.

    An explicit ``run_as`` pins that value. An omitted one means "inherit": it takes
    the preflight binding's identity, and pins nothing when there is no binding to
    inherit from.
    """
    pinned: set[ConnectorRunAs] = set()
    for slot in slots:
        if slot.run_as_explicit:
            pinned.add(slot.run_as)
            continue
        binding = binding_by_name.get(slot.connector_name) if binding_by_name is not None else None
        if binding is not None:
            pinned.add(binding.run_as)
    return pinned


def raise_if_mixed_run_as(subject: str, run_as_values: set[ConnectorRunAs]) -> None:
    """Reject connectors that mix ``run_as`` identities within one conversation."""
    if len(run_as_values) <= 1:
        return
    raise ValueError(
        f"{subject} mixes connector run_as values {sorted(v.value for v in run_as_values)}. "
        f"A conversation runs as a single identity, so all connectors must share the same "
        f"run_as; use ToolCallClient for per-connector identity."
    )
