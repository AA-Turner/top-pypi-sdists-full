"""Core preset (Python) — thin proxy over the Node SDK preset registry.

Unlike :mod:`superdoc.presets.legacy`, which reads packaged tool artifacts and
dispatches by traversing the local Python doc handle, the ``core`` preset has
NO bundled assets and NO action ports. Every call is forwarded to the running
SuperDoc CLI host (the same subprocess the rest of the Python SDK already
talks to) via six dedicated CLI-only operations:

    doc.preset.list           → {presets, defaultPreset}
    doc.preset.getCatalog     → preset.getCatalog()
    doc.preset.getTools       → preset.getTools(provider, {cache})
    doc.preset.getSystemPrompt → preset.getSystemPrompt()
    doc.preset.getMcpPrompt   → preset.getMcpPrompt()
    doc.preset.dispatch       → preset.dispatch(boundDoc, toolName, args)

For ``dispatch``, the document handle's session-bound runtime is reused so the
CLI op resolves to the same open editor; for the other five (session-less)
ops, a fresh sync runtime is spun up per call.

Cross-runtime contract: the CLI host runs the Node SDK preset, so behavior —
catalog shape, prompt content, action receipts — is byte-for-byte identical
between Python ``preset='core'`` and Node ``preset: 'core'``.
"""

from __future__ import annotations

import inspect
import math
import re
from dataclasses import dataclass
from typing import Any, Awaitable, Dict, Optional, Union, cast

from ..errors import SuperDocError
from ..runtime import SuperDocAsyncRuntime, SuperDocSyncRuntime
from . import ToolProvider


# ---------------------------------------------------------------------------
# Runtime resolution
# ---------------------------------------------------------------------------


def _stateless_runtime() -> SuperDocSyncRuntime:
    """Spawn a one-shot sync runtime for session-less preset reads."""
    return SuperDocSyncRuntime()


def _runtime_from_handle(document_handle: Any) -> Any:
    """Pull the session-bound runtime off a SuperDocDocument-shaped handle.

    The Python client wraps the raw transport runtime with a
    ``_BoundSyncRuntime`` / ``_BoundAsyncRuntime`` that injects ``sessionId``
    into every invoke. We need exactly that wrapper so ``doc.preset.dispatch``
    lands on the right session in the CLI host.
    """
    bound = getattr(document_handle, '_bound_runtime', None)
    if bound is None or not hasattr(bound, 'invoke'):
        raise SuperDocError(
            'core preset: document_handle must be a session-bound SuperDocDocument '
            '(missing _bound_runtime.invoke). Did you pass the raw client by mistake?',
            code='TOOL_DISPATCH_NOT_FOUND',
            details={'preset': 'core'},
        )
    return bound


# ---------------------------------------------------------------------------
# Response unwrapping — extract envelope.data from CLI responses
# ---------------------------------------------------------------------------


def _unwrap(response: Any) -> Dict[str, Any]:
    """Normalize a CLI response into a plain ``dict`` payload.

    The Python transport already strips the JSON-RPC envelope so most reads
    return the operation's ``data`` directly. We still defensively unwrap a
    ``{ data: ... }`` shape and verify the result is dict-like — every
    ``doc.preset.*`` op declares a JSON object output.
    """
    if isinstance(response, dict) and 'data' in response and len(response) == 1:
        response = response['data']
    if not isinstance(response, dict):
        raise SuperDocError(
            'core preset: CLI returned a non-object response.',
            code='TOOLS_ASSET_INVALID',
            details={'response_type': type(response).__name__},
        )
    return cast(Dict[str, Any], response)


# ---------------------------------------------------------------------------
# Cache markers — mirrors Node corePreset.applyCacheMarkers
# ---------------------------------------------------------------------------


def _apply_cache_markers(tools: list, provider: ToolProvider, cache_requested: bool) -> Dict[str, Any]:
    if not cache_requested:
        return {'tools': tools, 'cacheStrategy': 'disabled'}
    if provider == 'anthropic':
        if not tools:
            return {'tools': tools, 'cacheStrategy': 'explicit'}
        next_tools = list(tools[:-1])
        last = dict(tools[-1]) if isinstance(tools[-1], dict) else tools[-1]
        if isinstance(last, dict):
            last['cache_control'] = {'type': 'ephemeral'}
        next_tools.append(last)
        return {'tools': next_tools, 'cacheStrategy': 'explicit'}
    if provider == 'openai':
        return {'tools': tools, 'cacheStrategy': 'automatic'}
    return {'tools': tools, 'cacheStrategy': 'unsupported'}


# ---------------------------------------------------------------------------
# Policy options — shared by get_tools / get_system_prompt / dispatch
# ---------------------------------------------------------------------------


def _apply_policy_payload(
    payload: Dict[str, Any],
    *,
    exclude_actions: Optional[list] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[list] = None,
) -> Dict[str, Any]:
    """Encode the surface-narrowing policy the way the CLI ops accept it.

    Lists travel as comma-separated strings — the CLI op accepts one plain
    string on both the flag and JSON-RPC paths; action names contain no commas.
    Validation (unknown names, ``allow_direct_actions`` without enforcement,
    unsupported modes) happens once, in the Node preset behind the host, so
    Python and Node fail with the same error.
    """
    if exclude_actions:
        payload['excludeActions'] = ','.join(str(name) for name in exclude_actions)
    if enforce_change_mode is not None:
        payload['enforceChangeMode'] = str(enforce_change_mode)
    if allow_direct_actions is not None:
        # An empty allowlist is still an allowlist (it must trip the
        # "requires enforce_change_mode" check like Node does), so it is
        # forwarded whenever the caller set it.
        payload['allowDirectActions'] = ','.join(str(name) for name in allow_direct_actions)
    return payload


# ---------------------------------------------------------------------------
# Session-less reads — fresh sync runtime per call
# ---------------------------------------------------------------------------


def _core_get_catalog() -> Dict[str, Any]:
    runtime = _stateless_runtime()
    try:
        return _unwrap(runtime.invoke('doc.preset.getCatalog', {'preset': 'core'}))
    finally:
        runtime.dispose()


def _core_get_tools(
    provider: ToolProvider,
    *,
    cache: bool = False,
    exclude_actions: Optional[list] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[list] = None,
) -> Dict[str, Any]:
    if provider not in ('openai', 'anthropic', 'vercel', 'generic'):
        raise SuperDocError(
            'provider is required.',
            code='INVALID_ARGUMENT',
            details={'provider': provider},
        )
    payload: Dict[str, Any] = {'preset': 'core', 'provider': provider, 'cache': False}
    _apply_policy_payload(
        payload,
        exclude_actions=exclude_actions,
        enforce_change_mode=enforce_change_mode,
        allow_direct_actions=allow_direct_actions,
    )
    runtime = _stateless_runtime()
    try:
        # We always request cache=False from the host and apply markers locally:
        # the CLI host's getTools response goes through JSON-RPC and we want a
        # single deterministic implementation of provider cache markers.
        result = _unwrap(runtime.invoke('doc.preset.getTools', payload))
    finally:
        runtime.dispose()
    tools = result.get('tools') if isinstance(result.get('tools'), list) else []
    return _apply_cache_markers(cast(list, tools), provider, cache)


def _core_get_system_prompt(
    *,
    exclude_actions: Optional[list] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[list] = None,
) -> str:
    payload: Dict[str, Any] = {'preset': 'core'}
    _apply_policy_payload(
        payload,
        exclude_actions=exclude_actions,
        enforce_change_mode=enforce_change_mode,
        allow_direct_actions=allow_direct_actions,
    )
    runtime = _stateless_runtime()
    try:
        result = _unwrap(runtime.invoke('doc.preset.getSystemPrompt', payload))
    finally:
        runtime.dispose()
    prompt = result.get('prompt')
    if not isinstance(prompt, str):
        raise SuperDocError(
            'core preset: getSystemPrompt response missing string prompt.',
            code='TOOLS_ASSET_INVALID',
            details={'preset': 'core'},
        )
    return prompt


def _core_get_mcp_prompt() -> str:
    runtime = _stateless_runtime()
    try:
        result = _unwrap(runtime.invoke('doc.preset.getMcpPrompt', {'preset': 'core'}))
    finally:
        runtime.dispose()
    prompt = result.get('prompt')
    if not isinstance(prompt, str):
        raise SuperDocError(
            'core preset: getMcpPrompt response missing string prompt.',
            code='TOOLS_ASSET_INVALID',
            details={'preset': 'core'},
        )
    return prompt


# ---------------------------------------------------------------------------
# Dispatch — reuse the document handle's session-bound runtime
# ---------------------------------------------------------------------------


def _core_revision(value: Any, explicit_input: bool = False) -> int:
    numeric = None
    if isinstance(value, str) and len(value) <= 16 and re.fullmatch(r'0|[1-9][0-9]*', value):
        numeric = int(value)
    elif not explicit_input:
        if type(value) is int:
            numeric = value
        elif type(value) is float and math.isfinite(value) and value.is_integer():
            numeric = int(value)
    if numeric is None or not 0 <= numeric <= 9007199254740991:
        raise SuperDocError(
            'Core dispatch expected_revision must be a canonical non-negative safe integer revision.',
            code='INVALID_ARGUMENT',
            details={'preset': 'core', 'option': 'expectedRevision'},
        )
    return numeric


def _core_action_revision(value: Any, explicit_input: bool = False) -> str:
    if isinstance(value, str) and value:
        return value
    return str(_core_revision(value, explicit_input=explicit_input))


def _core_invoke_options(
    payload: Dict[str, Any], invoke_options: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    options = dict(invoke_options or {})
    for key in ('dry_run', 'dryRun'):
        value = options.pop(key, None)
        if value is not None and not isinstance(value, bool):
            raise SuperDocError(
                'Core dispatch dry_run must be a boolean.',
                code='INVALID_ARGUMENT',
                details={'preset': 'core', 'option': key},
            )
        if value is True:
            raise SuperDocError(
                'Core tool dispatch does not support dry-run preview.',
                code='CAPABILITY_UNSUPPORTED',
                details={'preset': 'core', 'capability': 'dryRun'},
            )
    snake_mode = options.pop('change_mode', None)
    camel_mode = options.pop('changeMode', None)
    if snake_mode is not None and camel_mode is not None and snake_mode != camel_mode:
        raise SuperDocError(
            'Cannot provide change_mode and changeMode with different values.',
            code='INVALID_ARGUMENT',
            details={'preset': 'core'},
        )
    change_mode = camel_mode if camel_mode is not None else snake_mode
    if change_mode is not None:
        if change_mode not in ('direct', 'tracked'):
            raise SuperDocError(
                'Core dispatch change_mode must be "direct" or "tracked".',
                code='INVALID_ARGUMENT',
                details={'preset': 'core'},
            )
        payload['changeMode'] = change_mode
    snake_revision = options.pop('expected_revision', None)
    camel_revision = options.pop('expectedRevision', None)
    action_dispatch = payload['toolName'] == 'superdoc_perform_action'
    normalize_revision = _core_action_revision if action_dispatch else _core_revision
    revision: Optional[Union[str, int]]
    if action_dispatch and 'expectedRevision' in payload['args']:
        revision = _core_action_revision(payload['args']['expectedRevision'], explicit_input=True)
    else:
        snake_value = normalize_revision(snake_revision) if snake_revision is not None else None
        camel_value = normalize_revision(camel_revision) if camel_revision is not None else None
        if snake_revision is not None and camel_revision is not None and snake_revision != camel_revision:
            raise SuperDocError(
                'Cannot provide expected_revision and expectedRevision with different values.',
                code='INVALID_ARGUMENT',
                details={'preset': 'core'},
            )
        revision = camel_value if camel_value is not None else snake_value
    if revision is not None:
        if action_dispatch:
            payload['args'] = {**payload['args'], 'expectedRevision': revision}
        else:
            payload['expectedRevision'] = revision
    return options


def _core_dispatch(
    document_handle: Any,
    tool_name: str,
    args: Optional[Dict[str, Any]] = None,
    invoke_options: Optional[Dict[str, Any]] = None,
    *,
    exclude_actions: Optional[list] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[list] = None,
) -> Any:
    if args is not None and not isinstance(args, dict):
        raise SuperDocError(
            'Tool arguments must be an object.',
            code='INVALID_ARGUMENT',
            details={'toolName': tool_name},
        )
    payload: Dict[str, Any] = {
        'preset': 'core',
        'toolName': tool_name,
        'args': args or {},
    }
    # Defense-in-depth parity with Node: a host that narrowed the advertised
    # surface passes the same policy so dispatch refuses hidden calls and
    # forces tracked mode where enforcement is on.
    _apply_policy_payload(
        payload,
        exclude_actions=exclude_actions,
        enforce_change_mode=enforce_change_mode,
        allow_direct_actions=allow_direct_actions,
    )
    runtime = _runtime_from_handle(document_handle)
    invoke_kwargs = _core_invoke_options(payload, invoke_options)
    raw = runtime.invoke('doc.preset.dispatch', payload, **invoke_kwargs)
    # When called against the async client, the bound runtime returns an
    # awaitable. dispatch() (sync) cannot await it; surface the misuse rather
    # than block.
    if inspect.isawaitable(raw):
        raise SuperDocError(
            'core preset: dispatch() received an awaitable from the async runtime. '
            'Use dispatch_superdoc_tool_async (or the descriptor.dispatch_async) '
            'with AsyncSuperDocDocument handles.',
            code='INVALID_ARGUMENT',
            details={'preset': 'core', 'toolName': tool_name},
        )
    return _unwrap(raw).get('result')


async def _core_dispatch_async(
    document_handle: Any,
    tool_name: str,
    args: Optional[Dict[str, Any]] = None,
    invoke_options: Optional[Dict[str, Any]] = None,
    *,
    exclude_actions: Optional[list] = None,
    enforce_change_mode: Optional[str] = None,
    allow_direct_actions: Optional[list] = None,
) -> Any:
    if args is not None and not isinstance(args, dict):
        raise SuperDocError(
            'Tool arguments must be an object.',
            code='INVALID_ARGUMENT',
            details={'toolName': tool_name},
        )
    payload: Dict[str, Any] = {
        'preset': 'core',
        'toolName': tool_name,
        'args': args or {},
    }
    _apply_policy_payload(
        payload,
        exclude_actions=exclude_actions,
        enforce_change_mode=enforce_change_mode,
        allow_direct_actions=allow_direct_actions,
    )
    runtime = _runtime_from_handle(document_handle)
    invoke_kwargs = _core_invoke_options(payload, invoke_options)
    raw = runtime.invoke('doc.preset.dispatch', payload, **invoke_kwargs)
    if inspect.isawaitable(raw):
        raw = await raw
    return _unwrap(raw).get('result')


# ---------------------------------------------------------------------------
# Descriptor
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _CorePreset:
    id: str = 'core'
    description: str = (
        'Actions-only LLM surface proxied to the Node SDK preset registry via CLI. '
        'No bundled assets in Python; all calls go through the SuperDoc CLI host.'
    )
    supports_cache_control: bool = True

    def get_tools(
        self,
        provider: ToolProvider,
        *,
        cache: bool = False,
        exclude_actions: Optional[list] = None,
        enforce_change_mode: Optional[str] = None,
        allow_direct_actions: Optional[list] = None,
    ) -> Dict[str, Any]:
        return _core_get_tools(
            provider,
            cache=cache,
            exclude_actions=exclude_actions,
            enforce_change_mode=enforce_change_mode,
            allow_direct_actions=allow_direct_actions,
        )

    def get_catalog(self) -> Dict[str, Any]:
        return _core_get_catalog()

    def get_system_prompt(
        self,
        *,
        exclude_actions: Optional[list] = None,
        enforce_change_mode: Optional[str] = None,
        allow_direct_actions: Optional[list] = None,
    ) -> str:
        return _core_get_system_prompt(
            exclude_actions=exclude_actions,
            enforce_change_mode=enforce_change_mode,
            allow_direct_actions=allow_direct_actions,
        )

    def get_mcp_prompt(self) -> str:
        return _core_get_mcp_prompt()

    def dispatch(
        self,
        document_handle: Any,
        tool_name: str,
        args: Optional[Dict[str, Any]] = None,
        invoke_options: Optional[Dict[str, Any]] = None,
        *,
        exclude_actions: Optional[list] = None,
        enforce_change_mode: Optional[str] = None,
        allow_direct_actions: Optional[list] = None,
    ) -> Any:
        return _core_dispatch(
            document_handle, tool_name, args, invoke_options,
            exclude_actions=exclude_actions,
            enforce_change_mode=enforce_change_mode,
            allow_direct_actions=allow_direct_actions,
        )

    def dispatch_async(
        self,
        document_handle: Any,
        tool_name: str,
        args: Optional[Dict[str, Any]] = None,
        invoke_options: Optional[Dict[str, Any]] = None,
        *,
        exclude_actions: Optional[list] = None,
        enforce_change_mode: Optional[str] = None,
        allow_direct_actions: Optional[list] = None,
    ) -> Awaitable[Any]:
        return _core_dispatch_async(
            document_handle, tool_name, args, invoke_options,
            exclude_actions=exclude_actions,
            enforce_change_mode=enforce_change_mode,
            allow_direct_actions=allow_direct_actions,
        )


core_preset: _CorePreset = _CorePreset()
