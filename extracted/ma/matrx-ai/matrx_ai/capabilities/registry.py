"""Capability registry and resolver.

Module-level dict holding the global capability registry. Populated at
startup by:

  1. matrx-ai's own built-in bundles (imported as a side-effect of
     ``import matrx_ai.capabilities``).
  2. Host applications calling ``matrx_ai.configure(capabilities=[...])``,
     which forwards into ``register_capability`` for each entry.

Read at request time by ``resolve_client_capabilities`` to validate the
incoming ``ClientContext`` and produce ``ToolSpec``s for the merge primitive.

Strict-by-default: unknown capability names raise ``CapabilityResolutionError``.
No silent drops — clients that send something the server doesn't understand
get a loud, actionable error.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from matrx_utils import vcprint

from matrx_ai.tools.specs import ToolSpec

from .models import Capability, CapabilityResolutionError, ClientContext

if TYPE_CHECKING:
    from pydantic import BaseModel


_REGISTRY: dict[str, Capability] = {}


def register_capability(cap: Capability, *, replace: bool = False) -> None:
    """Add a capability to the global registry.

    Idempotent for the same instance — re-registering the exact same object
    is a no-op so module-level ``register_capability`` calls in built-in
    bundles are safe to re-import. Different objects with the same name
    require ``replace=True`` to override (used when a host wants to swap
    a default).
    """
    existing = _REGISTRY.get(cap.name)
    if existing is None:
        _REGISTRY[cap.name] = cap
        return
    if existing is cap:
        return
    if not replace:
        raise ValueError(
            f"Capability {cap.name!r} is already registered. "
            f"Pass replace=True to override the existing entry."
        )
    _REGISTRY[cap.name] = cap


def get_capability(name: str) -> Capability | None:
    return _REGISTRY.get(name)


def list_capabilities() -> dict[str, Capability]:
    """Return a snapshot copy of the registry. Mutating the result does not
    affect the registry."""
    return dict(_REGISTRY)


def clear_capabilities() -> None:
    """Test helper — wipe the registry. Production code should never call
    this. Tests that want a clean slate use this in a fixture."""
    _REGISTRY.clear()


def resolve_client_capabilities(
    client_ctx: ClientContext,
    *,
    is_authenticated: bool = True,
) -> tuple[list[ToolSpec], list[ToolSpec], dict[str, BaseModel]]:
    """Validate a ``ClientContext`` against the registry.

    Returns
    -------
    (default_specs, optional_specs, payloads)
        ``default_specs``  — tool specs with ``default`` disposition (always
                             injected when the capability is declared, unless
                             excluded).
        ``optional_specs`` — tool specs with ``optional`` disposition (injected
                             only when the agent or user requests them by name).
        ``payloads``       — capability_name → validated Pydantic instance.
                             Caller stashes these on ``AppContext``
                             (``metadata['client_capabilities_payloads']``) so
                             tools can read typed state at execution time.

    Raises
    ------
    CapabilityResolutionError
        Aggregates every problem in a single error message so a misbehaving
        client sees all violations at once. Triggered by:
          - Unknown capability name.
          - ``requires_auth=True`` declared by an unauthenticated caller.
          - Payload that doesn't validate against the capability's
            ``payload_model``.

    No-op when ``client_ctx.capabilities`` is empty.
    """
    if not client_ctx.capabilities:
        return [], [], {}

    default_specs: list[ToolSpec] = []
    optional_specs: list[ToolSpec] = []
    payloads: dict[str, BaseModel] = {}
    errors: list[str] = []

    seen: set[str] = set()
    for name in client_ctx.capabilities:
        if name in seen:
            continue
        seen.add(name)

        cap = _REGISTRY.get(name)
        if cap is None:
            errors.append(f"unknown capability {name!r} (not registered on this server)")
            continue

        if cap.requires_auth and not is_authenticated:
            errors.append(f"capability {name!r} requires authentication")
            continue

        if cap.payload_model is not None:
            raw = client_ctx.state.get(name)
            if raw is not None:
                try:
                    payloads[name] = cap.payload_model.model_validate(raw)
                except Exception as exc:
                    errors.append(f"capability {name!r} payload invalid: {exc}")
                    continue

        if cap.enabled_tools_factory is not None:
            default_specs.extend(cap.enabled_tools_factory())
        else:
            default_specs.extend(cap.enabled_tools)

        if cap.optional_tools_factory is not None:
            optional_specs.extend(cap.optional_tools_factory())
        else:
            optional_specs.extend(cap.optional_tools)

    if errors:
        raise CapabilityResolutionError("; ".join(errors))

    if default_specs or optional_specs or payloads:
        vcprint(
            f"[capabilities] Resolved {len(client_ctx.capabilities)} cap(s) "
            f"{client_ctx.capabilities} → "
            f"{len(default_specs)} default spec(s), "
            f"{len(optional_specs)} optional spec(s), "
            f"{len(payloads)} typed payload(s)",
            color="cyan",
        )

    return default_specs, optional_specs, payloads
