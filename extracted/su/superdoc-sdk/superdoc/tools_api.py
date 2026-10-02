"""Public LLM-tools API (Python SDK). Thin layer over the preset registry.

Every call here resolves a preset (defaulting to ``legacy`` for backwards
compat) and delegates to it. Mirrors ``packages/sdk/langs/node/src/tools.ts``.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TypedDict, cast

from .presets import (
    DEFAULT_PRESET,
    ToolProvider,
    get_preset,
    list_presets,
    register_preset,
    unregister_preset,
)
from .errors import SuperDocError

__all__ = [
    'DEFAULT_PRESET',
    'ToolChooserInput',
    'ToolProvider',
    'choose_tools',
    'create_agent_toolkit',
    'dispatch_superdoc_tool',
    'dispatch_superdoc_tool_async',
    'get_preset',
    'get_mcp_prompt',
    'get_system_prompt',
    'get_tool_catalog',
    'list_presets',
    'list_tools',
    'register_preset',
    'unregister_preset',
]


class ToolChooserInput(TypedDict, total=False):
    provider: ToolProvider
    # Preset ID to load tools from. Defaults to DEFAULT_PRESET ('legacy')
    # for backwards compatibility. Use list_presets() to discover presets.
    preset: str
    # When True, applies provider-specific prompt-cache markers (Anthropic
    # ``cache_control: { type: "ephemeral" }`` on the last tool, etc).
    cache: bool
    # Action names to REMOVE from the advertised action surface (core preset:
    # the superdoc_perform_action enum/description/args shrink together).
    # Unknown names fail. Presets without an action surface ignore it.
    excludeActions: List[str]
    # Fail-closed tracked-only policy (core preset). ``'tracked'`` removes every
    # direct-only action from the surface (unless allowlisted) and forces
    # tracked mode at dispatch. Only ``'tracked'`` is accepted.
    enforceChangeMode: str
    # Direct-only actions kept callable under ``enforceChangeMode``; ``['*']``
    # allows all of them. Requires ``enforceChangeMode``.
    allowDirectActions: List[str]


def get_tool_catalog(preset: Optional[str] = None) -> Dict[str, Any]:
    """Return the full tool catalog for a preset (default: legacy)."""
    return get_preset(preset).get_catalog()


def list_tools(provider: ToolProvider, preset: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return the raw tool array for a provider from a preset (default: legacy).

    No cache markers applied. Use :func:`choose_tools` for cache markers and metadata.
    """
    if provider not in ('openai', 'anthropic', 'vercel', 'generic'):
        raise SuperDocError(
            'provider is required.',
            code='INVALID_ARGUMENT',
            details={'provider': provider},
        )
    result = get_preset(preset).get_tools(provider, cache=False)
    tools = result.get('tools') if isinstance(result.get('tools'), list) else []
    return cast(List[Dict[str, Any]], tools)


def _policy_kwargs(
    *,
    exclude_actions: Optional[List[str]] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Core-preset surface policy as kwargs, forwarded ONLY when set.

    Third-party preset descriptors whose methods lack these kwargs keep
    working unchanged; the core preset validates the combination (Node parity:
    ``allow_direct_actions`` requires ``enforce_change_mode``, only
    ``'tracked'`` is accepted, unknown names fail).
    """
    kwargs: Dict[str, Any] = {}
    if exclude_actions:
        kwargs['exclude_actions'] = list(exclude_actions)
    if enforce_change_mode is not None:
        kwargs['enforce_change_mode'] = enforce_change_mode
    if allow_direct_actions is not None:
        kwargs['allow_direct_actions'] = list(allow_direct_actions)
    return kwargs


def _policy_from_input(input: Dict[str, Any]) -> Dict[str, Any]:
    """Read the policy fields from a camelCase (Node parity) or snake_case dict."""
    exclude_actions = input.get('excludeActions') or input.get('exclude_actions')
    enforce_change_mode = input.get('enforceChangeMode')
    if enforce_change_mode is None:
        enforce_change_mode = input.get('enforce_change_mode')
    allow_direct_actions = input.get('allowDirectActions')
    if allow_direct_actions is None:
        allow_direct_actions = input.get('allow_direct_actions')
    return _policy_kwargs(
        exclude_actions=list(exclude_actions) if exclude_actions else None,
        enforce_change_mode=enforce_change_mode,
        allow_direct_actions=list(allow_direct_actions) if allow_direct_actions is not None else None,
    )


def choose_tools(input: ToolChooserInput) -> Dict[str, Any]:
    """Select tools for a specific provider from a preset.

    Example::

        # Default — legacy preset.
        result = choose_tools({'provider': 'openai'})

        # Pick a specific preset.
        result = choose_tools({'provider': 'anthropic', 'preset': 'legacy', 'cache': True})
    """
    provider = input.get('provider')
    if provider not in ('openai', 'anthropic', 'vercel', 'generic'):
        raise SuperDocError(
            'provider is required.',
            code='INVALID_ARGUMENT',
            details={'provider': provider},
        )

    # Default only when `preset` is absent. An explicit empty string is passed
    # through to get_preset() so it raises PRESET_NOT_FOUND, matching Node/MCP
    # fail-fast behavior. Using `or DEFAULT_PRESET` would silently treat
    # `preset: ''` as legacy and hide misconfiguration.
    preset_arg = input.get('preset')
    preset_id = preset_arg if preset_arg is not None else DEFAULT_PRESET
    cache_requested = bool(input.get('cache'))

    preset = get_preset(preset_id)
    # Core-preset policy knobs (Node parity: chooseTools({excludeActions,
    # enforceChangeMode, allowDirectActions})), forwarded only when provided.
    result = preset.get_tools(cast(ToolProvider, provider), cache=cache_requested, **_policy_from_input(input))
    tools = result.get('tools') if isinstance(result.get('tools'), list) else []
    cache_strategy = result.get('cacheStrategy', 'disabled')

    return {
        'tools': tools,
        'meta': {
            'provider': provider,
            'preset': preset_id,
            'toolCount': len(tools) if isinstance(tools, list) else 0,
            'cacheStrategy': cache_strategy,
        },
    }


def dispatch_superdoc_tool(
    document_handle: Any,
    tool_name: str,
    args: Optional[Dict[str, Any]] = None,
    invoke_options: Optional[Dict[str, Any]] = None,
    *,
    preset: Optional[str] = None,
    exclude_actions: Optional[List[str]] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[List[str]] = None,
) -> Any:
    """Dispatch a tool call against a bound document handle.

    ``preset`` selects the LLM-tools preset (defaults to :data:`DEFAULT_PRESET`,
    currently ``'legacy'``). Pass ``preset='core'`` to route through the
    actions-only core LLM surface proxied to the Node SDK over the CLI.

    ``exclude_actions`` mirrors :func:`choose_tools`: pass the SAME exclusions
    so the dispatch guard refuses actions the narrowed tool surface cannot
    call (core preset; legacy ignores it). ``enforce_change_mode='tracked'``
    (with optional ``allow_direct_actions``; ``['*']`` allows every direct-only
    action) likewise refuses direct-only actions and forces tracked mode on
    every other action.

    The handle injects session targeting automatically; arguments should not
    contain ``doc`` or ``sessionId`` — those are stripped if present.
    """
    return get_preset(preset).dispatch(
        document_handle, tool_name, args, invoke_options,
        exclude_actions=list(exclude_actions) if exclude_actions else None,
        **_policy_kwargs(
            enforce_change_mode=enforce_change_mode,
            allow_direct_actions=allow_direct_actions,
        ),
    )


async def dispatch_superdoc_tool_async(
    document_handle: Any,
    tool_name: str,
    args: Optional[Dict[str, Any]] = None,
    invoke_options: Optional[Dict[str, Any]] = None,
    *,
    preset: Optional[str] = None,
    exclude_actions: Optional[List[str]] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[List[str]] = None,
) -> Any:
    """Async version of :func:`dispatch_superdoc_tool`."""
    return await get_preset(preset).dispatch_async(
        document_handle, tool_name, args, invoke_options,
        exclude_actions=list(exclude_actions) if exclude_actions else None,
        **_policy_kwargs(
            enforce_change_mode=enforce_change_mode,
            allow_direct_actions=allow_direct_actions,
        ),
    )


def create_agent_toolkit(
    input: Dict[str, Any],
) -> Dict[str, Any]:
    """One-call agent surface: tools, system prompt, and pre-bound dispatchers
    that are coherent BY CONSTRUCTION — the same preset and ``excludeActions``
    apply to all three, so an action can never linger in the system prompt
    after being excluded from the tool array (or vice versa).

    Mirrors the Node SDK's ``createAgentToolkit``. Returns a dict with
    ``tools``, ``meta``, ``system_prompt``, ``dispatch`` and
    ``dispatch_async`` (both pre-bound to the preset + exclusions).

    The legacy preset ignores exclusion options everywhere (it has no action
    surface); passing ``excludeActions`` with ``preset='legacy'`` is a no-op.
    """
    preset_arg = input.get('preset')
    preset = preset_arg if preset_arg is not None else DEFAULT_PRESET
    # Copied once so later caller mutation cannot desync dispatch from the
    # tools and prompt generated here (Node parity).
    policy = _policy_from_input(input)
    exclude_actions = policy.get('exclude_actions')

    # One-call custom-actions path: hand your actions to the toolkit and use it.
    # Build an ephemeral extended/composed preset over `base` (default 'core')
    # and drive it directly — no register_preset, no preset id to thread through
    # dispatch.
    actions = input.get('customActions')
    if actions is None:
        actions = input.get('custom_actions')
    actions = actions or []
    include_actions = input.get('includeActions')
    if include_actions is None:
        include_actions = input.get('include_actions')
    # An explicit `base` selects this path even with an empty actions list —
    # otherwise {'base': 'core', 'customActions': []} would silently fall through to
    # the default (legacy) preset, a different tool family than the one named.
    if actions or include_actions is not None or input.get('base') is not None:
        # A custom action runs its own step list and never passes the core
        # dispatch guard, so the tracked-only policy cannot cover it. Enforcing
        # built-ins while custom actions edit directly would be a policy that
        # silently does not hold — refuse the combination instead (Node parity).
        if policy.get('enforce_change_mode') is not None:
            raise SuperDocError(
                'enforce_change_mode is not supported together with custom actions; '
                'a custom action bypasses the tracked-changes guard.',
                code='INVALID_ARGUMENT',
                details={
                    'enforceChangeMode': policy.get('enforce_change_mode'),
                    'reason': 'custom-actions-unsupported',
                },
            )
        from .presets.custom import extend_preset  # lazy: avoid import cycle
        provider = input.get('provider')
        # Validate provider up front (parity with choose_tools) — the actions
        # path builds tools directly, so it must not skip this check.
        if provider not in ('openai', 'anthropic', 'vercel', 'generic'):
            raise SuperDocError('provider is required.', code='INVALID_ARGUMENT', details={'provider': provider})
        # `preset` doubles as the base to extend here; `base` wins if both given.
        base_arg = input.get('base')
        base_id = base_arg if base_arg is not None else (preset_arg if preset_arg is not None else 'core')
        descriptor = extend_preset(base_id, id='custom_superdoc_preset', actions=actions,
                                   include_actions=include_actions)
        tools_res = descriptor.get_tools(provider, cache=bool(input.get('cache')),
                                         exclude_actions=exclude_actions)
        tools = tools_res.get('tools') if isinstance(tools_res.get('tools'), list) else []
        sys_prompt = descriptor.get_system_prompt(exclude_actions=exclude_actions)

        def _dispatch(document_handle: Any, tool_name: str,
                      args: Optional[Dict[str, Any]] = None,
                      invoke_options: Optional[Dict[str, Any]] = None) -> Any:
            return descriptor.dispatch(document_handle, tool_name, args, invoke_options,
                                       exclude_actions=exclude_actions)

        async def _dispatch_async(document_handle: Any, tool_name: str,
                                  args: Optional[Dict[str, Any]] = None,
                                  invoke_options: Optional[Dict[str, Any]] = None) -> Any:
            return await descriptor.dispatch_async(document_handle, tool_name, args, invoke_options,
                                                   exclude_actions=exclude_actions)

        return {
            'tools': tools,
            'meta': {
                'provider': provider,
                'preset': descriptor.id,
                'toolCount': len(tools),
                'cacheStrategy': tools_res.get('cacheStrategy', 'disabled'),
            },
            'system_prompt': sys_prompt,
            'dispatch': _dispatch,
            'dispatch_async': _dispatch_async,
        }

    chosen = choose_tools({**input, 'preset': preset})
    system_prompt = get_system_prompt(preset, **policy) if policy else get_system_prompt(preset)

    def dispatch(document_handle: Any, tool_name: str,
                 args: Optional[Dict[str, Any]] = None,
                 invoke_options: Optional[Dict[str, Any]] = None) -> Any:
        return dispatch_superdoc_tool(
            document_handle, tool_name, args, invoke_options,
            preset=preset, **policy,
        )

    async def dispatch_async(document_handle: Any, tool_name: str,
                             args: Optional[Dict[str, Any]] = None,
                             invoke_options: Optional[Dict[str, Any]] = None) -> Any:
        return await dispatch_superdoc_tool_async(
            document_handle, tool_name, args, invoke_options,
            preset=preset, **policy,
        )

    return {
        'tools': chosen['tools'],
        'meta': chosen['meta'],
        'system_prompt': system_prompt,
        'dispatch': dispatch,
        'dispatch_async': dispatch_async,
    }


def get_system_prompt(
    preset: Optional[str] = None,
    *,
    exclude_actions: Optional[List[str]] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[List[str]] = None,
) -> str:
    """Read the packaged SDK system prompt (default preset: legacy).

    Includes a persona preamble suitable for embedded LLM usage. For MCP
    server instructions, use :func:`get_mcp_prompt` instead.

    ``exclude_actions`` mirrors ``choose_tools``: pass the SAME exclusions so
    the prompt stops documenting actions the narrowed tool surface cannot
    call (core preset; legacy ignores it). ``enforce_change_mode`` and
    ``allow_direct_actions`` drop direct-only actions the same way.
    """
    policy = _policy_kwargs(
        exclude_actions=exclude_actions,
        enforce_change_mode=enforce_change_mode,
        allow_direct_actions=allow_direct_actions,
    )
    if policy:
        return get_preset(preset).get_system_prompt(**policy)
    return get_preset(preset).get_system_prompt()


def get_mcp_prompt(preset: Optional[str] = None) -> str:
    """Read the packaged MCP system prompt for intent tools (default preset: legacy).

    Omits the persona preamble and includes session lifecycle instructions
    (open/save/close) suitable for MCP server ``instructions``.
    """
    return get_preset(preset).get_mcp_prompt()
