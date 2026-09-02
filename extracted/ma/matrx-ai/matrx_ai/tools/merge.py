"""Single write path for mutating an agent's active tool set.

Every source that adds tools to a request — the agent's own definition, the
request body (``tools`` / ``tools_replace``), capability bundles, editable
structured-input blocks, and mid-loop dynamic injection — funnels through
``merge_request_tools``. This is the only place that mutates
``UnifiedConfig.tools`` / ``UnifiedConfig.custom_tools`` /
``AppContext.client_tools``.

Centralising the write path lets us enforce two invariants in exactly one
place:

  1. **Idempotence.** Calling the primitive with specs that are already
     present is a no-op. Sources can be re-applied without fear.
  2. **Conflict detection.** A name that already resolves to a different
     ``(kind, delegate)`` is a hard error (``ToolMergeError``). Same name,
     same shape: silently dedup. Same name, different shape: refuse.
  3. **Hard exclusions.** A host may bind the request to an authoritative
     execution environment and place names in ``metadata['hard_excluded_tools']``.
     Those names are removed from preloaded tools and cannot be reintroduced by
     any source, including a mid-loop discovery mutation.

Source-aware concerns (``auto_tools_disabled``, capability auth gates) are
the *caller's* responsibility — they decide whether to invoke the primitive
at all. The primitive only knows about specs and exclusions.
"""

from __future__ import annotations

import asyncio
import hashlib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from matrx_utils import detached_task, vcprint

from matrx_ai.tools.models import CustomTool, CustomToolInputSchema, ToolDefinition, ToolType
from matrx_ai.tools.specs import (
    AgentToolSpec,
    InlineToolSpec,
    RegisteredToolSpec,
    ToolSpec,
    spec_display_name,
)

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext

    from matrx_ai.config.unified_config import UnifiedConfig


# ----------------------------------------------------------------------------
# Step 1 toggle (TOOL_INJECTION_REFACTOR.md / Arman's 2-step plan).
#
# When True, every InlineToolSpec processed by ``merge_request_tools`` is
# also handed to ``ToolRegistry.ensure_registered`` so the executor can
# dispatch the tool when the model invokes it. When False, that hook is
# skipped — the bug returns ("Tool 'X' not found in registry" at
# dispatch time) for any tool that wasn't pre-loaded into the registry
# at startup.
#
# Flip to False ONLY to confirm the failure mode is exactly what we
# think it is. Production should keep this True.
# ----------------------------------------------------------------------------
ENABLE_AUTO_REGISTER_INLINE_TOOLS: bool = True
UNRUNNABLE_TOOL_CONFIGURATION_KIND = "unrunnable_tool_configuration"

# Host-owned routing policy may impose exclusions that are stronger than the
# normal agent/user precedence rules.  The value is a JSON-safe list of
# canonical tool names on AppContext.metadata so it survives context forks and
# remains available to the dynamic-mutation drain between loop iterations.
HARD_EXCLUDED_TOOLS_KEY = "hard_excluded_tools"
CLIENT_DELEGATION_DISABLED_KEY = "client_delegation_disabled"
# Retired request-local snapshot key. It is still cleared when encountered so
# contexts created by an older process cannot resurrect stale routing state.
HARD_EXCLUSION_BASE_DECLARATION_KEY = "hard_exclusion_base_declaration"

_TOOL_RUNTIME_METADATA_KEYS: frozenset[str] = frozenset(
    {
        HARD_EXCLUDED_TOOLS_KEY,
        HARD_EXCLUSION_BASE_DECLARATION_KEY,
        "active_tool_executors",
        "active_ui_surface",
        "client_capabilities_payloads",
        "desktop_target_instance_id",
        "filesystem_authority",
    }
)


async def _capture_unrunnable_tool_configuration(
    *,
    ctx: AppContext,
    dropped_tools: Sequence[str],
    active_executors: frozenset[str],
    delegated_tools: set[str],
) -> None:
    from matrx_connect.streaming.error_capture import capture_error

    exc = RuntimeError(
        f"{len(dropped_tools)} configured tool(s) had no executor at request pre-flight"
    )
    await capture_error(
        exc,
        kind=UNRUNNABLE_TOOL_CONFIGURATION_KIND,
        request_id=ctx.request_id or None,
        user_id=ctx.user_id or None,
        conversation_id=ctx.conversation_id or None,
        route=ctx.route or "tool_merge.preflight",
        error_type="ToolRoutingConfigurationError",
        context={
            "dropped_tools": sorted(dropped_tools),
            "active_client_kinds": sorted(active_executors),
            "delegated_to_client": sorted(delegated_tools),
        },
    )


def _schedule_unrunnable_tool_configuration_capture(
    *,
    ctx: AppContext,
    dropped_tools: Sequence[str],
    active_executors: frozenset[str],
    delegated_tools: set[str],
) -> None:
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    detached_task(
        _capture_unrunnable_tool_configuration(
            ctx=ctx,
            dropped_tools=dropped_tools,
            active_executors=active_executors,
            delegated_tools=delegated_tools,
        ),
        name="capture_unrunnable_tool_configuration",
    )


def _ensure_authored_tool_declaration(config: UnifiedConfig) -> None:
    """Initialize the durable authored declaration on legacy configs."""
    if getattr(config, "authored_tools", None) is None:
        config.authored_tools = list(getattr(config, "tools", None) or [])
    if getattr(config, "authored_custom_tools", None) is None:
        config.authored_custom_tools = list(getattr(config, "custom_tools", None) or [])
    if getattr(config, "authored_mcp_servers", None) is None:
        config.authored_mcp_servers = list(getattr(config, "mcp_servers", None) or [])


def _restorable_registered_tools(config: UnifiedConfig) -> list[str]:
    """Return authored + conversation-dynamic registered tools, stably deduped."""
    _ensure_authored_tool_declaration(config)
    return canonical_tool_names(
        [
            *(getattr(config, "authored_tools", None) or []),
            *(getattr(config, "dynamic_tools", None) or []),
        ]
    )


def restore_request_filtered_tool_surface(
    config: UnifiedConfig,
    *,
    restore_delegation: bool = True,
) -> None:
    """Restore canonical declarations filtered only for a prior request.

    Capability and client-delegation gates are properties of one execution,
    never authored agent configuration. Their effective mutations may be
    persisted with a conversation, so the next compatible request must restore
    the authored set before applying its own policy.
    """
    _ensure_authored_tool_declaration(config)
    if getattr(config, "tool_capability_filtered", False):
        config.tools = _restorable_registered_tools(config)
        config.custom_tools = list(config.authored_custom_tools or [])
        config.mcp_servers = list(config.authored_mcp_servers or [])
        config.tool_capability_filtered = False
    if restore_delegation and getattr(config, "tool_delegation_filtered", False):
        config.tools = _restorable_registered_tools(config)
        config.custom_tools = list(config.authored_custom_tools or [])
        config.tool_delegation_filtered = False
        config.tool_delegation_executors = None
        config.tool_delegation_disabled_policy = False
        config.tool_delegation_registry_fingerprint = None
        config.tool_delegation_filter_applied_runtime = False


def filter_tool_surface_for_unsupported_model(config: UnifiedConfig) -> None:
    """Clear the effective tool surface while preserving authored config."""
    _ensure_authored_tool_declaration(config)
    config.tools = []
    config.custom_tools = []
    if getattr(config, "mcp_servers", None):
        config.mcp_servers = []
    config.tool_capability_filtered = True


def client_delegation_disabled(ctx: AppContext | None) -> bool:
    if ctx is None or not getattr(ctx, "metadata", None):
        return False
    return ctx.metadata.get(CLIENT_DELEGATION_DISABLED_KEY) is True


def clear_tool_runtime_state(ctx: AppContext) -> AppContext:
    """Clear request-scoped tool routing state from a reusable context."""
    metadata = dict(getattr(ctx, "metadata", None) or {})
    for key in _TOOL_RUNTIME_METADATA_KEYS:
        metadata.pop(key, None)
    if not hasattr(ctx, "with_overrides"):
        return ctx
    return ctx.with_overrides(metadata=metadata, client_tools=[])


def hard_excluded_tool_names(ctx: AppContext | None) -> frozenset[str]:
    if ctx is None or not getattr(ctx, "metadata", None):
        return frozenset()
    raw = ctx.metadata.get(HARD_EXCLUDED_TOOLS_KEY) or []
    if not isinstance(raw, list | tuple | set | frozenset):
        return frozenset()
    return frozenset(str(name) for name in raw if isinstance(name, str) and name)


def enforce_hard_tool_exclusions(
    config: UnifiedConfig,
    ctx: AppContext,
) -> AppContext:
    """Remove host-forbidden tools from every active tool collection.

    Unlike the ordinary ``excluded`` argument, this applies to tools already
    loaded on the agent and cannot be overridden by ``user.add``.  Calling it
    is idempotent; ``merge_request_tools`` invokes it on every write and hosts
    may invoke it before an early return such as ``auto_tools_disabled``.
    """
    _ensure_authored_tool_declaration(config)
    hard = hard_excluded_tool_names(ctx)
    prior_hard = frozenset(getattr(config, "tool_authority_exclusions", None) or [])
    metadata = dict(getattr(ctx, "metadata", None) or {})
    metadata.pop(HARD_EXCLUSION_BASE_DECLARATION_KEY, None)
    if not hard:
        if getattr(config, "tool_authority_filtered", False):
            config.tools = _restorable_registered_tools(config)
            config.custom_tools = list(config.authored_custom_tools or [])
            config.tool_authority_filtered = False
        config.tool_authority_exclusions = []
        config.tool_authority_filter_applied_runtime = False
        if metadata != dict(getattr(ctx, "metadata", None) or {}) and hasattr(
            ctx, "with_overrides"
        ):
            return ctx.with_overrides(metadata=metadata)
        return ctx

    if (
        not getattr(config, "tool_authority_filtered", False)
        or prior_hard != hard
        or not bool(getattr(config, "tool_authority_filter_applied_runtime", False))
    ):
        config.tools = _restorable_registered_tools(config)
        config.custom_tools = list(config.authored_custom_tools or [])
    config.tool_authority_filtered = True
    config.tool_authority_exclusions = sorted(hard)
    config.tool_authority_filter_applied_runtime = True

    before_registered = len(config.tools)
    before_inline = len(config.custom_tools)
    config.tools = [
        entry
        for entry in config.tools
        if not isinstance(entry, str) or _canonical_registered_name(entry) not in hard
    ]
    config.custom_tools = [
        tool for tool in config.custom_tools if getattr(tool, "name", None) not in hard
    ]
    client_tools = [
        name
        for name in (ctx.client_tools or [])
        if name not in hard and _canonical_registered_name(name) not in hard
    ]
    if client_tools != list(ctx.client_tools or []):
        ctx = ctx.with_overrides(client_tools=client_tools)

    removed = (before_registered - len(config.tools)) + (before_inline - len(config.custom_tools))
    if removed:
        vcprint(
            f"[merge_request_tools] HARD EXCLUSION removed {removed} active "
            f"tool(s): {sorted(hard)}",
            color="cyan",
        )
    return ctx


def build_tools_on_call(
    config: UnifiedConfig, app_ctx: AppContext | None = None
) -> list[dict[str, Any]]:
    """Resolve the FINAL toolset offered on this call into a compact, durable
    record: ``[{id, name, kind}]``.

    - Registered tools (``config.tools``, canonical names): ``id`` is the
      ``tool.definition`` UUID from the registry (``None`` when the name is unknown);
      ``kind="registered"``.
    - Inline tools (``config.custom_tools``): no registry id → ``id=None``;
      ``kind="agent"`` when the inline tool is an agent projection (its name is
      in ``AppContext.metadata[PROJECTED_AGENT_TOOLS_KEY]``), else ``kind="inline"``.

    Stamped on the user message at send time so every turn carries the exact
    tools the model was offered — NOT the conversation's latest config (which is
    overwritten each turn). Never raises; returns ``[]`` on any failure
    (telemetry, not control flow).
    """
    try:
        from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        projected: dict[str, Any] = {}
        if app_ctx is not None and getattr(app_ctx, "metadata", None):
            projected = app_ctx.metadata.get(PROJECTED_AGENT_TOOLS_KEY) or {}

        out: list[dict[str, Any]] = []
        seen: set[tuple[str, str]] = set()
        for name in config.tools or []:
            if not isinstance(name, str):
                continue
            # A projected agent tool (custom_tool_N) rides config.tools as a
            # RegisteredToolSpec name but is NEVER in the registry — its def lives
            # in the projection map. Label it kind="agent" (not "registered") so
            # the tools_on_call telemetry reflects what it actually is.
            is_projected = name in projected
            kind = "agent" if is_projected else "registered"
            key = (kind, name)
            if key in seen:
                continue
            seen.add(key)
            td = None if is_projected else registry.get(name)
            out.append({"id": td.tool_id if td else None, "name": name, "kind": kind})
        for ct in config.custom_tools or []:
            ct_name = getattr(ct, "name", None)
            if not ct_name:
                continue
            kind = "agent" if ct_name in projected else "inline"
            key = (kind, ct_name)
            if key in seen:
                continue
            seen.add(key)
            out.append({"id": None, "name": ct_name, "kind": kind})
        return out
    except Exception as exc:
        vcprint(f"[build_tools_on_call] failed (non-fatal): {exc}", color="yellow")
        return []


@dataclass
class _ToolMergeErrorInfo:
    """Classified envelope read by the streaming layer
    (``matrx_connect.streaming.response``) off ``exc.error_info`` to surface a
    clean, typed error to the frontend instead of a generic 500 / "Failed to
    fetch". Mirrors the provider-error ``error_info`` convention."""

    error_type: str
    message: str
    user_message: str
    status_code: int = 422


class ToolMergeError(ValueError):
    """Raised when a merge would produce an inconsistent tool set — a name that
    resolves to two different kinds (registered vs inline), a non-string entry
    in ``config.tools``, or an unprojected ``AgentToolSpec``.

    This is a server-side tool/agent/capability MISCONFIGURATION, not something
    the end user can fix from the request body. Every instance carries an
    ``error_info`` envelope so a request that fails here streams a clean
    ``tool_merge_error`` event to the client (via the prepared-streaming-task
    path) rather than collapsing into an opaque transport-level "Failed to
    fetch".
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.error_info = _ToolMergeErrorInfo(
            error_type="tool_merge_error",
            message=str(message),
            user_message=(
                "This agent's tool configuration is inconsistent and can't run. "
                "An administrator needs to fix the agent or capability definition "
                "(a tool is declared in two incompatible ways)."
            ),
        )


# Key under which the active UI surface is stashed on AppContext.metadata.
# A short string like "chrome-extension/pilot" or "web-ui/code-editor".
# Set by the request entry point (aidream's apply_unified_tools); read
# here for surface-aware logging only.
ACTIVE_UI_SURFACE_KEY = "active_ui_surface"

# The host resolves which client executors are live once at the request edge,
# then stores the canonical result here so mid-loop tool mutations use the
# exact same routing authority as the initial merge.  Dynamic discovery runs
# after the request builder has returned and cannot safely re-query host-owned
# surface tables; carrying the resolved names on AppContext also preserves them
# across context forks and async tool-task boundaries.
ACTIVE_TOOL_EXECUTORS_KEY = "active_tool_executors"


def active_tool_executors(ctx: AppContext | None) -> frozenset[str]:
    """Return the request's host-resolved live client executor names."""
    if client_delegation_disabled(ctx):
        return frozenset()
    if ctx is None or not getattr(ctx, "metadata", None):
        return frozenset()
    raw = ctx.metadata.get(ACTIVE_TOOL_EXECUTORS_KEY) or []
    if not isinstance(raw, list | tuple | set | frozenset):
        return frozenset()
    return frozenset(name for name in raw if isinstance(name, str) and name)


def required_client_executor_unmet(
    tool_def: object | None, active_executors: frozenset[str]
) -> str | None:
    """Evaluate the ``requires_client_executor`` gate for one tool.

    A server-implemented discovery/loader tool whose entire payload is
    client-delegated (e.g. ``load_chrome_tools`` → the Chrome extension's
    toolset) declares ``{"gate": "requires_client_executor",
    "args": {"executor": "chrome-extension"}}`` on ``tool_def.gating``.
    Returns the required executor name when the gate is UNMET (the executor —
    or a dot-descendant like ``chrome-extension.pilot`` — is not in this
    request's active client-kind set), else ``None``. Callers drop unmet
    tools before the model sees them.
    """
    if tool_def is None:
        return None
    for gate_spec in getattr(tool_def, "gating", None) or []:
        if not isinstance(gate_spec, dict):
            continue
        if gate_spec.get("gate") != "requires_client_executor":
            continue
        executor = str((gate_spec.get("args") or {}).get("executor") or "").strip()
        if executor and not any(
            k == executor or k.startswith(f"{executor}.") for k in active_executors
        ):
            return executor
    return None


def _surface_check_failed(spec_name: str, ctx: AppContext) -> str | None:
    """Surface-gating moved from the per-tool ``tl_def_surface`` join to
    per-surface defaults expressed as arrays on ``tool_surface_defaults``
    (always_include_tools / never_include_tools). That filtering happens
    at request-build time in the host (``aidream/services/tooling/tool_merge.py``
    + ``tool_resolve_for_request`` RPC), not here — by the time a spec
    reaches ``merge_request_tools`` it has already passed the surface's
    include/exclude lists. So this hook is now a no-op kept for the
    structural ``if reason is not None`` flow below; future per-surface
    rejections can repopulate it without disturbing the call site.
    """
    return None


def _canonical_registered_id(name_or_id: str) -> str:
    """Normalise a ``config.tools`` entry to its registry UUID when known.

    Accepts either a canonical name or a DB UUID. Returns the UUID when
    ``ToolRegistry`` resolves the input to a registered tool with a
    ``tool_id``; falls back to the literal input string otherwise (so
    synthetic projection names, foreign-namespace names, deleted tool
    UUIDs round-trip safely). Used by ``merge_request_tools`` to key dedup
    on a single identifier space (UUIDs for registered tools).
    """
    try:
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        tool = registry.get(name_or_id)
        if tool is None or tool.tool_id is None:
            return name_or_id
        return tool.tool_id
    except Exception:
        return name_or_id


def _canonical_registered_name(name_or_id: str) -> str:
    """Resolve a registered tool ref (UUID or name) to its canonical NAME.

    ``ctx.client_tools`` is the delegation set the executor consults via
    ``tool_name in client_tools`` — and the model always calls tools by
    their canonical NAME, never the UUID. So the set MUST be keyed by name.
    This is the name-space counterpart of ``_canonical_registered_id``
    (which keys dedup by UUID). Falls back to the literal input when the
    registry doesn't recognize it (synthetic projections, foreign names).
    """
    try:
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        tool = registry.get(name_or_id)
        return tool.name if tool is not None else name_or_id
    except Exception:
        return name_or_id


def _delegation_registry_fingerprint(config: UnifiedConfig) -> str:
    """Hash the registry facts that decide authored-tool viability.

    Active executor names alone are insufficient: a binding or server
    implementation can appear after cache reload/deploy while the same client
    remains attached. Persisting this compact fingerprint makes that policy
    change restore and re-evaluate the authored declaration.
    """
    try:
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
        rows: list[tuple[str, str, bool, tuple[str, ...]]] = []
        for raw_name in getattr(config, "authored_tools", None) or []:
            if not isinstance(raw_name, str):
                continue
            name = _canonical_registered_name(raw_name)
            definition = registry.get(name)
            tool_type = (
                str(getattr(getattr(definition, "tool_type", None), "value", "missing"))
                if definition is not None
                else "missing"
            )
            has_function_path = bool(
                (getattr(definition, "function_path", "") or "").strip()
                if definition is not None
                else False
            )
            rows.append(
                (
                    name,
                    tool_type,
                    has_function_path,
                    tuple(sorted(registry.bindings_for_tool(name))),
                )
            )
        return hashlib.sha256(repr(rows).encode("utf-8")).hexdigest()
    except Exception:
        return "registry-unavailable"


def _inline_definition_shape(description: str, input_schema: Any) -> tuple[str, object]:
    """Return a deterministic semantic shape for inline-definition identity.

    Pydantic normalizes defaults/types. This final pass canonicalizes JSON
    object key order and the schema arrays whose order has no meaning, avoiding
    false conflicts for equivalent ``required``/``enum``/union declarations.
    Order-sensitive arrays such as tuple-style item schemas remain untouched.
    """

    def normalize(value: Any, *, parent_key: str | None = None) -> object:
        if isinstance(value, dict):
            return tuple(
                (key, normalize(child, parent_key=key))
                for key, child in sorted(value.items())
            )
        if isinstance(value, list):
            normalized = [normalize(child) for child in value]
            if parent_key in {"required", "enum", "type", "allOf", "anyOf", "oneOf"}:
                normalized.sort(key=repr)
            return tuple(normalized)
        return value

    raw = input_schema.model_dump(mode="json", exclude_none=False)
    return description, normalize(raw)


def canonical_tool_names(tools: list) -> list[str]:
    """Resolve every ``config.tools`` entry (name OR DB UUID) to its canonical
    NAME — order-preserving + deduped. ``config.tools`` must hold names, never
    UUIDs: this is the edge normalization that keeps tool IDs out of
    ``UnifiedConfig``'s depths and out of every provider payload. Non-string
    entries pass through untouched for the downstream type-guard to reject.

    This is the single platform primitive for "make ``config.tools`` safe for
    the provider boundary". It is applied at two independent edges so a tool
    UUID can never reach a provider regardless of how the request was built:

      1. the HTTP request edge — ``merge_request_tools`` (this module), and
      2. the direct agent-execution edge — ``Agent.execute`` (definition.py),
         which is the path every ``NamedAgent`` / ``run_agent`` internal call
         takes. Without (2), a DB agent that carries tools as ``agx_agent.tools``
         UUIDs leaked raw IDs to the provider and the call hard-failed (the
         ``TOOL ID(s) REACHED THE PROVIDER BOUNDARY`` guard).
    """
    seen: set[str] = set()
    out: list = []
    for entry in tools:
        if not isinstance(entry, str):
            out.append(entry)
            continue
        nm = _canonical_registered_name(entry)
        if nm not in seen:
            seen.add(nm)
            out.append(nm)
    return out


def merge_request_tools(
    config: UnifiedConfig,
    ctx: AppContext,
    specs: Sequence[ToolSpec],
    *,
    excluded: Iterable[str] = (),
    active_executors: frozenset[str] | None = None,
) -> AppContext:
    """Merge ``specs`` into ``config`` and ``ctx``.

    Mutates ``config.tools`` / ``config.custom_tools`` in place (they are
    list fields on a dataclass). Returns a (possibly-updated) ``AppContext``
    because ``AppContext`` is immutable — the caller MUST rebind the result:

        ctx = merge_request_tools(config, ctx, specs)
        set_app_context(ctx)

    Parameters
    ----------
    config
        The ``UnifiedConfig`` whose ``tools`` and ``custom_tools`` lists are
        the destination for registered and inline specs respectively.
    ctx
        The active ``AppContext``. Returned with ``client_tools`` extended
        for any spec that should be delegated to the client.
    specs
        The tool specifications to merge. Order matters only for the
        conflict-detection error message — first writer wins; second
        conflicting writer raises.
    excluded
        Names to filter out of the merge entirely. Per-agent deny lists,
        opt-outs, etc. Filtering happens *before* conflict detection so an
        excluded name never blocks a legitimate later spec.
    active_executors
        The set of executor names live for this request (server executors
        are always present; client executors only when a client is
        connected; MCP executors only when the user has a connection). This
        is the SOLE input to delegation: a registered tool is added to
        ``ctx.client_tools`` iff
        ``registry.resolve_executor_binding(name, active_executors)`` is
        ``"surface"`` (i.e. the tool is bound to a CLIENT executor that's
        live this session). Default empty ⇒ server-only. The per-spec
        ``RegisteredToolSpec.delegate`` flag is no longer consulted for
        routing — delegation is resolved here, once, for every tool
        regardless of source, so two sources can never disagree. ``None``
        (the default) reuses the canonical set already resolved onto ``ctx``;
        pass an explicit empty frozenset only to force a detached/server-only
        reconciliation.

    Raises
    ------
    ToolMergeError
        On a genuine kind clash (a name registered as both ``registered`` and
        ``inline``). ``delegate`` is no longer part of tool identity, so the
        old "same name, different delegate" conflict class cannot occur.
    NotImplementedError
        For ``AgentToolSpec`` until phase E lands the projection logic.
    """
    # CANONICAL CAPABILITY GATE — function calling.
    # When this request's model has no function calling (config.supports_tools is
    # False — a TTS / image / video / audio / extraction model, resolved from the
    # single source of truth in providers/capabilities.py), the single tool
    # write-path simply adds nothing. This is the agreed-upon path DOING ITS JOB,
    # so it is informational (cyan), never a warning — the loud "this should never
    # have reached here" backstop lives at the provider boundary (unified_client)
    # for anything that bypasses this gate.
    _ensure_authored_tool_declaration(config)
    if active_executors is None:
        active_executors = active_tool_executors(ctx)
    delegation_disabled = client_delegation_disabled(ctx)
    if delegation_disabled:
        active_executors = frozenset()
    current_delegation_executors = sorted(active_executors)
    prior_delegation_executors = getattr(config, "tool_delegation_executors", None)
    current_registry_fingerprint = _delegation_registry_fingerprint(config)
    delegation_policy_changed = (
        not bool(getattr(config, "tool_delegation_filter_applied_runtime", False))
        or prior_delegation_executors is None
        or list(prior_delegation_executors) != current_delegation_executors
        or bool(getattr(config, "tool_delegation_disabled_policy", False))
        != delegation_disabled
        or getattr(config, "tool_delegation_registry_fingerprint", None)
        != current_registry_fingerprint
    )
    if config.supports_tools:
        restore_request_filtered_tool_surface(
            config,
            restore_delegation=delegation_policy_changed,
        )
    else:
        if specs:
            vcprint(
                f"[merge_request_tools] model has no function calling "
                f"(supports_tools=False) — not adding {len(specs)} tool spec(s).",
                color="cyan",
            )
        filter_tool_surface_for_unsupported_model(config)
        return clear_tool_runtime_state(ctx)

    # Host-level authority policy applies even on early-return paths below.
    # (Deliberately AFTER the no-function-calling gate: that branch clears the
    # entire tool surface and must leave a minimal ctx untouched — enforcing
    # exclusions on a model that can't call tools is moot.)
    ctx = enforce_hard_tool_exclusions(config, ctx)
    if delegation_disabled and config.custom_tools:
        # Inline tools have no server implementation. A silenced/reference
        # child cannot announce a delegated call, so never offer them.
        config.custom_tools = []
        config.tool_delegation_filtered = True
        config.tool_delegation_executors = current_delegation_executors
        config.tool_delegation_disabled_policy = True
        config.tool_delegation_registry_fingerprint = current_registry_fingerprint
        config.tool_delegation_filter_applied_runtime = True

    # Host policy is absolute: remove forbidden preloaded tools first, then
    # include the same names in the spec filter so no capability, request, or
    # dynamic discovery mutation can add them back.
    hard_excluded = hard_excluded_tool_names(ctx)
    excluded_set = {n for n in excluded if n} | set(hard_excluded)
    if not specs and not excluded_set and not config.tools and not config.custom_tools:
        # Genuinely nothing to route — no specs, no exclusions, no pre-loaded
        # tools. Only THEN is it safe to short-circuit.
        #
        # When there ARE pre-loaded tools but no new specs we must NOT return
        # early: the delegation pass AND the executor-viability gate below still
        # have to run over them. A pre-loaded client tool (e.g. `user`) must get
        # delegated to the active client, and a pre-loaded tool with no viable
        # executor must get dropped — even on a request that adds no new specs.
        # (The early-return here was silently skipping both; that left
        # un-delegated `user` routing server-side → no_viable_executor.)
        config.tools = canonical_tool_names(config.tools)
        if ctx.client_tools:
            ctx = ctx.with_overrides(client_tools=[])
        return ctx

    # Build an index of what's already present so we can detect cross-call
    # conflicts. Identity is (key → kind) ONLY — never (kind, delegate).
    # Delegation is a request-time routing decision resolved in one final
    # pass (see below) from ``active_executors``, not a per-source attribute
    # baked into identity; that is what makes the old "same name, different
    # delegate" conflict class structurally impossible.
    #
    # Registered-tool entries are keyed by their **registry UUID** whenever the
    # registry recognizes the value — both DB UUIDs (from ``agx_agent.tools``)
    # and canonical names collapse to the same key. Without this collapse, the
    # agent's stored UUID and a capability that adds the same tool by name
    # would both land in ``config.tools`` and the API request would carry two
    # function declarations that resolve to one tool (Anthropic 400, Gemini
    # 400, OpenAI silently degrades). Inline tools are caller-defined, never in
    # the registry; keyed by literal name.
    existing: dict[str, tuple[str, object | None]] = {}
    for raw in config.tools:
        # config.tools is supposed to be list[str] — a flat list of registered
        # tool names / UUIDs. If a non-string sneaks in (e.g. someone dumped
        # the raw wire ToolSpec dicts directly into UnifiedConfig.tools — see
        # the chat router's _EXCLUDE_FROM_CONFIG list), bail with a clear
        # message naming the offending entry's type. The historical failure
        # was "TypeError: unhashable type: 'dict'" buried under 30 frames of
        # starlette/anyio middleware which gave no hint about the real cause.
        if not isinstance(raw, str):
            raise ToolMergeError(
                f"config.tools must be a list of registered tool names/UUIDs "
                f"(strings), got entry of type {type(raw).__name__}: {raw!r}. "
                f"Caller is dumping wire-format ToolSpec objects into "
                f"UnifiedConfig.tools — they must go through apply_unified_tools "
                f"/ merge_request_tools instead."
            )
        canonical = _canonical_registered_id(raw)
        existing[canonical] = ("registered", None)
    for ct in config.custom_tools:
        # Inline (CustomTool) is always client-delegated (no server impl).
        existing[ct.name] = (
            "inline",
            _inline_definition_shape(ct.description, ct.input_schema),
        )

    appended_registered: list[str] = []
    appended_inline: list[CustomTool] = []

    def _record(
        key: str,
        display: str,
        kind: str,
        definition_shape: object | None = None,
    ) -> bool:
        """Returns True if this is a new addition, False if it's a no-op
        dedup. Raises ToolMergeError only on a genuine KIND clash.

        Identity is ``kind`` alone — ``delegate`` is resolved separately, once,
        after the loop. So two sources adding the same registered tool (even
        with different delegate intents) always dedup; the only thing that can
        still conflict is the same name arriving as both ``registered`` and
        ``inline``, which is a real definition clash (§4 of TOOL_ROUTING_RULES).

        ``key`` is the canonical identifier (UUID for registered tools when
        knowable, name otherwise); ``display`` is the user-facing name used
        only for error messages.
        """
        prior = existing.get(key)
        if prior is None:
            existing[key] = (kind, definition_shape)
            return True
        prior_kind, prior_shape = prior
        if prior_kind == kind:
            if kind == "inline" and prior_shape != definition_shape:
                raise ToolMergeError(
                    f"Tool definition conflict: inline tool {display!r} was declared "
                    "more than once with a different description or input_schema. "
                    "One name maps to one immutable definition; rename one tool."
                )
            vcprint(
                f"[merge_request_tools] dedup: {display!r} already present as "
                f"kind={prior_kind}",
                color="cyan",
                log_level="DEBUG",
                stdout=False,
            )
            return False
        raise ToolMergeError(
            f"Tool conflict: {display!r} is already present as kind={prior_kind!r} "
            f"but a new spec wants kind={kind!r}. One name → one kind "
            f"(a tool cannot be both a registered tool and an inline tool) — "
            f"fix the capability/agent definition."
        )

    for spec in specs:
        if isinstance(spec, RegisteredToolSpec) and spec.tool_id:
            # ``tool_id`` wins at dispatch, while exclusions and conflict checks
            # are name-based. Accepting a mismatched pair lets an allowed-looking
            # name smuggle an excluded tool UUID through the merge boundary.
            from matrx_ai.tools.registry import ToolRegistry

            registry = ToolRegistry.get_instance()
            canonical = registry._resolve_tool_name(spec.tool_id)
            if canonical is not None and canonical != spec.name:
                # Only a genuine SMUGGLE is rejected: ``name`` resolving to a
                # DIFFERENT registered tool than ``tool_id`` (an allowed-looking
                # name carrying an excluded tool's UUID past name-based checks).
                # Everything else — name set to the UUID itself, an alias of the
                # same tool, or an unresolvable placeholder — identifies ONE
                # tool unambiguously; rejecting it kills a real request over a
                # spelling. Reconcile to the canonical name (COERCED) so the
                # name-based exclusion/conflict checks below see the truth.
                name_canonical = registry._resolve_tool_name(spec.name) if spec.name else None
                if name_canonical is not None and name_canonical != canonical:
                    raise ToolMergeError(
                        f"Registered tool identity mismatch: name {spec.name!r} "
                        f"resolves to {name_canonical!r} but tool_id "
                        f"{spec.tool_id!r} resolves to {canonical!r} — two "
                        f"different tools in one spec."
                    )
                vcprint(
                    f"[merge_request_tools] COERCED registered spec name "
                    f"{spec.name!r} → canonical {canonical!r} (tool_id "
                    f"{spec.tool_id!r}); caller sent the UUID/alias as the name.",
                    color="yellow",
                )
                spec = spec.model_copy(update={"name": canonical})

        if delegation_disabled and isinstance(spec, InlineToolSpec):
            config.tool_delegation_filtered = True
            config.tool_delegation_executors = current_delegation_executors
            config.tool_delegation_disabled_policy = True
            config.tool_delegation_registry_fingerprint = current_registry_fingerprint
            config.tool_delegation_filter_applied_runtime = True
            vcprint(
                f"[merge_request_tools] Skipping inline tool {spec.name!r}: "
                "client delegation is disabled for this execution.",
                color="cyan",
            )
            continue

        display = spec_display_name(spec)
        if display in excluded_set:
            vcprint(
                f"[merge_request_tools] Skipping "
                f"{'hard-excluded' if display in hard_excluded else 'excluded'} "
                f"tool: {display}",
                color="cyan" if display in hard_excluded else "yellow",
            )
            continue

        # Surface enforcement — historically rejected specs whose
        # tl_def_surface assignments didn't intersect the request's active
        # UI surface. That filter moved to the host's resolver (via the
        # surface defaults arrays); _surface_check_failed is a no-op stub
        # kept for the structural call site.
        # InlineToolSpec is exempt: client-supplied ad-hoc tools have no
        # registry row to consult, so we can't gate them on surfaces; the
        # client took explicit responsibility by sending them inline.
        if not isinstance(spec, InlineToolSpec):
            reason = _surface_check_failed(display, ctx)
            if reason is not None:
                from matrx_ai.tools._debug_log import log_event as _debug_log

                active = (ctx.metadata or {}).get(ACTIVE_UI_SURFACE_KEY)
                _debug_log(
                    "SURFACE_REJECT",
                    tool=display,
                    active_surface=active,
                )
                vcprint(
                    f"[merge_request_tools] surface-gate rejected: {reason}",
                    color="red",
                )
                continue

        if isinstance(spec, RegisteredToolSpec):
            # Use UUID-when-knowable as the dedup key so a name spec
            # collapses against an agent's UUID-form entry for the same tool.
            spec_key = spec.resolved_tool_id() or spec.name
            if _record(spec_key, spec.name, "registered"):
                # Append the spec_key (UUID when known, name otherwise).
                # Translators resolve either form on lookup, so either is fine
                # on the wire — but appending UUIDs keeps config.tools
                # uniform when the agent already had UUIDs.
                appended_registered.append(spec_key)
        elif isinstance(spec, InlineToolSpec):
            _reject_wire_squatter(spec.name)
            definition_shape = _inline_definition_shape(spec.description, spec.input_schema)
            # Bind the executor definition even when this spec deduplicates
            # against an identical CustomTool already present on the config.
            # Request assembly can legitimately materialize the wire tool
            # before the unified merge pass.  Skipping the stash on that
            # no-op branch makes dispatch fall back to the process-global
            # first-seen definition, leaking another request's narrower
            # Content IR contract into this one.
            request_tool_def = _tool_definition_from_inline_spec(spec)
            from matrx_ai.tools.agent_projection import stash_request_tool_definition

            stash_request_tool_definition(ctx, request_tool_def)
            if _record(spec.name, spec.name, "inline", definition_shape):
                # Synthesize a registry entry so the executor's dispatch
                # path (``self.registry.get(tool_name)``) can find this
                # tool when the model invokes it. Without this, an inline
                # spec gets the model the schema (via config.custom_tools
                # / translator) but the executor errors with "Tool 'x'
                # not found in registry" at dispatch time. Idempotent:
                # if a registry entry already exists under this name (the
                # tool was loaded from the DB at startup, or a previous
                # request already ensured it), the existing entry stays.
                if ENABLE_AUTO_REGISTER_INLINE_TOOLS:
                    _ensure_registered_for_dispatch(spec)
                else:
                    vcprint(
                        f"[merge_request_tools] STEP-1 DISABLED — skipping "
                        f"ensure_registered for inline {spec.name!r}; expect "
                        f"'not found in registry' at dispatch time",
                        color="yellow",
                    )
                appended_inline.append(
                    CustomTool(
                        name=spec.name,
                        description=spec.description,
                        input_schema=_coerce_input_schema(spec.input_schema),
                    )
                )
        elif isinstance(spec, AgentToolSpec):
            # AgentToolSpec must be pre-resolved into a RegisteredToolSpec by
            # the request handler (see aidream/services/tooling/tool_merge.py
            # apply_unified_tools → resolve_agent_specs). Reaching here means
            # the caller skipped that step.
            raise ToolMergeError(
                f"AgentToolSpec for agent_id={spec.agent_id!r} reached the "
                f"merge primitive without being projected. The request handler "
                f"must call resolve_agent_specs() before merge_request_tools()."
            )

        else:
            raise ToolMergeError(f"Unknown ToolSpec variant: {type(spec).__name__}")

    if appended_registered:
        config.tools = list(config.tools) + appended_registered
    if appended_inline:
        config.custom_tools = list(config.custom_tools) + appended_inline

    # ---- Single delegation-resolution pass -------------------------------
    # Every registered tool in the final set (pre-loaded agent tools AND
    # newly-merged specs) is routed here, ONCE, by the registry's single
    # authority. A tool is delegated to the client iff one of its client-side
    # executor kinds is in this request's active client kinds. Empty
    # active_executors ⇒ every registered tool stays server-side, so a
    # no-client / server-originated run delegates nothing and the executor
    # never waits on a client that won't connect.
    try:
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
    except Exception:
        registry = None
    # This is a RECONCILIATION, not an additive update. AppContext can be
    # deliberately reused across continuation/resume paths; carrying its prior
    # registered delegation set forward would let a detached client retain
    # routing authority. Rebuild from the schemas active on this request:
    # registered tools route by binding × active executors, while inline tools
    # remain client-delegated because they have no server implementation.
    new_client_tools: list[str] = []
    if registry is not None:
        for raw_name in config.tools:
            canonical_name = _canonical_registered_name(raw_name)
            if (
                registry.resolve_executor_binding(canonical_name, set(active_executors))
                == "surface"
            ):
                if canonical_name not in new_client_tools:
                    new_client_tools.append(canonical_name)
    if not delegation_disabled:
        # Inline tools delegate to the client by default (no server impl) —
        # EXCEPT when the name shadows a registry row that carries explicit
        # executor bindings. Then the registry is the routing authority: the
        # tool delegates only if one of its bound client executors is live on
        # THIS request. Without this check, a discovery tool that republishes
        # registered client tools as inline specs (the load_chrome_tools
        # pattern) smuggles them past the binding × active-executor authority
        # and the executor delegates them to a client that can never answer —
        # the call sits in status='delegated' and the whole user request in
        # status='paused' until the 30-day abandonment sweep (the 2026-08-21
        # matrx-user/chat incident). Names with NO registry bindings keep the
        # unconditional-delegate behavior: those are genuinely caller-authored
        # ad-hoc client tools the client took responsibility for.
        kept_custom: list[CustomTool] = []
        dropped_unbound_inline: list[str] = []
        for custom_tool in config.custom_tools:
            bindings = (
                registry.bindings_for_tool(custom_tool.name) if registry is not None else None
            )
            if bindings and (
                registry.resolve_executor_binding(custom_tool.name, set(active_executors))
                != "surface"
            ):
                dropped_unbound_inline.append(custom_tool.name)
                continue
            kept_custom.append(custom_tool)
            if custom_tool.name not in new_client_tools:
                new_client_tools.append(custom_tool.name)
        if dropped_unbound_inline:
            config.custom_tools = kept_custom
            config.tool_delegation_filtered = True
            config.tool_delegation_executors = current_delegation_executors
            config.tool_delegation_disabled_policy = delegation_disabled
            config.tool_delegation_registry_fingerprint = current_registry_fingerprint
            config.tool_delegation_filter_applied_runtime = True
            vcprint(
                {
                    "dropped": sorted(dropped_unbound_inline),
                    "active_client_kinds": sorted(active_executors),
                },
                f"[merge_request_tools] INLINE EXECUTOR-VIABILITY DROP — "
                f"{len(dropped_unbound_inline)} inline tool(s) shadow registered "
                f"tools whose bound client executor is NOT live on this request. "
                f"Delegating them would strand the call in status='delegated' "
                f"forever. Whoever queued these (a discovery/loader tool?) must "
                f"gate on the active executor set before loading.",
                color="red",
            )

    if new_client_tools != list(ctx.client_tools or []):
        ctx = ctx.with_overrides(client_tools=new_client_tools)

    if appended_registered or appended_inline:
        vcprint(
            f"[merge_request_tools] +{len(appended_registered)} registered, "
            f"+{len(appended_inline)} inline. "
            f"config.tools now {len(config.tools)} entries; "
            f"config.custom_tools now {len(config.custom_tools)} entries.",
            color="cyan",
        )

    # ── Edge normalization: config.tools carries NAMES, never UUIDs ──────────
    # The model and every provider API speak tool NAMES. Internal DB UUIDs are
    # resolved to canonical names HERE — the single tool write-path — so no UUID
    # ever reaches UnifiedConfig's depths or a provider. (Dedup above keys on
    # UUIDs for stability; the stored result is names.) A UUID that survives past
    # this point is a bug — registry.get_provider_tools screams + raises on one.
    config.tools = canonical_tool_names(config.tools)

    # ── Pre-flight executor-viability gate ───────────────────────────────────
    # NEVER hand the model a tool it cannot run. A tool has no viable executor
    # for THIS request when it is a LOCAL tool with no server ``function_path``
    # AND was not delegated to an active client surface (not in client_tools).
    # That is the exact condition the dispatcher rejects with
    # ``no_viable_executor`` (executor.py) — but by then the model has already
    # CALLED the tool and the user sees a hard failure mid-turn (the live
    # ``user``-on-agent-builder incident). Drop these here, loudly, so the model
    # never sees a tool that can't run. The fix for a tool that SHOULD be
    # runnable is to wire its server handler or activate the client surface that
    # delegates it — not to let it reach the model and fail.
    if registry is not None and config.tools:
        delegated_set = set(new_client_tools)
        kept_tools: list[str] = []
        dropped_unrunnable: list[str] = []
        dropped_gated: list[str] = []
        for _name in config.tools:
            _td = registry.get(_name)
            if (
                _td is not None
                and _td.tool_type == ToolType.LOCAL
                and not (_td.function_path or "").strip()
                and _name not in delegated_set
            ):
                # A client-only tool on a server-originated request is not a
                # broken declaration: it has a configured executor, but that
                # executor is deliberately absent. Treat it like every other
                # unmet client gate. Only a LOCAL tool with neither a server
                # implementation nor a configured client binding belongs in
                # the structured repair queue.
                client_bindings = registry.client_bindings_for_tool(_name)
                if client_bindings:
                    dropped_gated.append(
                        f"{_name} (needs one of {sorted(client_bindings)})"
                    )
                    continue
                dropped_unrunnable.append(_name)
                continue
            _unmet = required_client_executor_unmet(_td, active_executors)
            if _unmet is not None:
                dropped_gated.append(f"{_name} (needs {_unmet})")
                continue
            kept_tools.append(_name)
        if dropped_gated:
            config.tools = kept_tools
            config.tool_delegation_filtered = True
            config.tool_delegation_executors = current_delegation_executors
            config.tool_delegation_disabled_policy = delegation_disabled
            config.tool_delegation_registry_fingerprint = current_registry_fingerprint
            config.tool_delegation_filter_applied_runtime = True
            vcprint(
                f"[merge_request_tools] requires_client_executor gate dropped "
                f"{len(dropped_gated)} tool(s) whose required client executor is "
                f"not live on this request: {sorted(dropped_gated)} "
                f"(active client kinds: {sorted(active_executors) or '[]'}). "
                f"This is the gate doing its job — the tool only works when "
                f"that client is connected.",
                color="cyan",
            )
        if dropped_unrunnable:
            config.tools = kept_tools
            config.tool_delegation_filtered = True
            config.tool_delegation_executors = current_delegation_executors
            config.tool_delegation_disabled_policy = delegation_disabled
            config.tool_delegation_registry_fingerprint = current_registry_fingerprint
            config.tool_delegation_filter_applied_runtime = True
            _schedule_unrunnable_tool_configuration_capture(
                ctx=ctx,
                dropped_tools=dropped_unrunnable,
                active_executors=active_executors,
                delegated_tools=delegated_set,
            )
            vcprint(
                {
                    "dropped": sorted(dropped_unrunnable),
                    "active_client_kinds": sorted(active_executors),
                    "delegated_to_client": sorted(delegated_set),
                    "remaining_tools": len(kept_tools),
                },
                f"[merge_request_tools] PRE-FLIGHT DROP — {len(dropped_unrunnable)} "
                f"tool(s) have NO viable executor for this request (LOCAL, no server "
                f"function_path, and not delegated to an active client surface). "
                f"Removed from the model's tool set so they can't be called and fail "
                f"with no_viable_executor. To make one runnable: wire its server "
                f"handler, or activate the client surface that delegates it.",
                color="yellow",
            )

    return ctx


def _reject_wire_squatter(name: str) -> None:
    """Refuse an inline tool whose WIRE form collides with a different
    registry tool's wire form.

    Providers see wire names (``:`` → ``__``, ``matrx_ai.config.wire_names``),
    so ``bundle__list_supabase`` (inline, request-supplied) and
    ``bundle:list_supabase`` (canonical registry row) are the SAME name to
    the model — but different identities internally. Accepting the inline
    spec would (a) let its ``ensure_registered`` entry direct-hit at dispatch
    and shadow the canonical tool for the whole process, and (b) hand the
    model's arguments for the canonical tool to the request-supplied one.
    Rejecting at merge time surfaces a clean request error to the caller;
    ``ToolRegistry.ensure_registered`` independently refuses the
    registration as the second layer.
    """
    try:
        from matrx_ai.tools.registry import ToolRegistry

        registry = ToolRegistry.get_instance()
    except Exception:
        return
    from matrx_ai.config.wire_names import to_wire_name

    wire = to_wire_name(name)
    for existing in registry.list_tool_names():
        if existing != name and to_wire_name(existing) == wire:
            vcprint(
                {"inline_name": name, "existing_tool": existing, "shared_wire_name": wire},
                "🚨 [merge_request_tools] WIRE-SQUATTING REJECTED — an inline tool "
                "spec's name collides on the provider wire form with an existing "
                "registry tool. The spec is refused; rename the inline tool.",
                color="red",
            )
            raise ToolMergeError(
                f"Inline tool name {name!r} collides on the provider wire form "
                f"({wire!r}) with the registered tool {existing!r} — ':' and '__' "
                f"collapse to the same wire spelling. Rename the inline tool."
            )


def _ensure_registered_for_dispatch(spec: InlineToolSpec) -> None:
    """Ensure the executor can dispatch ``spec`` at call time.

    Inline tools have always reached the model via ``config.custom_tools``
    and the translator, but the executor's lookup is registry-based —
    ``self.registry.get(tool_name)`` returns ``None`` for any tool that
    wasn't loaded from the ``public.tool_def`` table at startup. The result:
    the model sees the schema, calls the tool, and the executor errors
    with ``Tool 'X' not found in registry``.

    This shim closes the gap by synthesizing a registry entry from the
    inline spec's name + description + input_schema. Idempotent — already-
    registered names are a no-op. The synthesized entry has no callable;
    its only valid execution path is client delegation, which is exactly
    what inline tools always do (the merge primitive adds inline tools
    to ``ctx.client_tools`` above).

    Lazy import + try/except: the registry is shared infrastructure with
    its own setup/teardown; merge primitive callers shouldn't fail just
    because the registry isn't available (test paths without a DB-loaded
    registry, etc.).
    """
    try:
        from matrx_ai.tools.registry import ToolRegistry

        request_tool_def = _tool_definition_from_inline_spec(spec)

        ToolRegistry.get_instance().ensure_registered(
            name=spec.name,
            description=spec.description,
            parameters=request_tool_def.parameters,
            source_kind="agent_authored",
        )
    except Exception as exc:
        vcprint(
            f"[merge_request_tools] ensure_registered failed for {spec.name!r}: "
            f"{exc!r} — dispatch may fail downstream",
            color="yellow",
        )


def _tool_definition_from_inline_spec(spec: InlineToolSpec) -> ToolDefinition:
    """Build the exact request-local executor definition for an inline spec."""
    coerced = _coerce_input_schema(spec.input_schema)
    properties = dict(coerced.properties or {})
    required_set = set(coerced.required or [])
    parameters: dict[str, Any] = {}
    for prop_name, prop_schema in properties.items():
        if isinstance(prop_schema, dict):
            entry = dict(prop_schema)
        elif hasattr(prop_schema, "model_dump"):
            entry = prop_schema.model_dump(by_alias=True, exclude_none=True)
        else:
            entry = {"type": "string"}
        if prop_name in required_set:
            entry["required"] = True
        parameters[prop_name] = entry
    return ToolDefinition(
        name=spec.name,
        description=spec.description,
        parameters=parameters,
        tool_type=ToolType.LOCAL,
        function_path="",
        source_kind="agent_authored",
    )


def _coerce_input_schema(
    raw: CustomToolInputSchema | dict | None,
) -> CustomToolInputSchema:
    if raw is None:
        return CustomToolInputSchema()
    if isinstance(raw, CustomToolInputSchema):
        return raw
    return CustomToolInputSchema(
        type=raw.get("type", "object"),
        properties=raw.get("properties", {}),
        required=raw.get("required", []),
    )
