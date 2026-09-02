"""Provider API-key resolution — the ONE place provider keys come from.

Every provider client resolves its API key through :func:`resolve_api_key`
instead of reading ``os.environ`` directly. Resolution order, per env name:

1. The host-injected resolver (``_ext`` key ``"api_key_resolver"``, a
   ``Callable[[str], str | None]``), tried for each env name in order. A
   desktop host (matrx-local) injects one that reads its own secure store,
   so provider keys never need to live in the process environment.
2. The ambient ``AppContext.api_keys`` mapping, accepting either the exact
   env-style name or its provider shorthand (``ANTHROPIC_API_KEY`` /
   ``anthropic``). This preserves per-request and explicit workflow keys while
   keeping provider clients behind the canonical resolver.
3. ``os.environ`` for each env name in order — the unchanged server path.
   A server host that injects nothing behaves exactly as before.

The resolver is registered via ``matrx_ai.configure(api_key_resolver=...)``.

Key rotation: provider client singletons/memos are keyed ON THE RESOLVED KEY
VALUE (see the ``_clients: dict[str, ...]`` pattern in ``providers/*/client.py``
and the ``self._client_key`` memo in the ``*_api.py`` classes). When the
resolver starts returning a new key, the next request constructs a fresh SDK
client under the new key — no process restart required.
"""

from __future__ import annotations

import asyncio
import os
import threading
from collections.abc import Callable

from matrx_ai._ext import get_ext, has_ext

_RESOLVER_KEY = "api_key_resolver"
_CREDENTIAL_RESOLVER_KEY = "credential_resolver"


class ApiKeyNotFoundError(RuntimeError):
    """Raised when ``required=True`` and no source produced a key."""


def get_credential_resolver():
    """The host-injected vault ``CredentialResolver`` (see
    ``matrx_connect.credentials``), or None when the host injected none.
    Registered via ``matrx_ai.configure(credential_resolver=...)``."""
    resolver = get_ext(_CREDENTIAL_RESOLVER_KEY) if has_ext(_CREDENTIAL_RESOLVER_KEY) else None
    if resolver is not None and not hasattr(resolver, "resolve"):
        raise TypeError(
            "matrx-ai 'credential_resolver' must implement "
            "matrx_connect.credentials.CredentialResolver (async resolve(request)); "
            f"got {type(resolver).__name__!r}. Fix the configure() call."
        )
    return resolver


async def resolve_credential_field(
    *,
    item_id: str | None = None,
    field_key: str | None = None,
    field_id: str | None = None,
    consumer: str = "agent",
    purpose: str,
    invocation_id: str | None = None,
    required: bool = False,
) -> str | None:
    """Resolve ONE credential value by stable reference through the
    host-injected vault resolver. This is the stable-ref sibling of
    :func:`resolve_api_key` — use it when a config or agent carries an
    ``{item_id, field_key}`` / ``field_id`` reference instead of an env name.

    The actor is the ambient ``AppContext`` user; a missing context or missing
    resolver returns None (or raises when ``required=True``)."""
    resolver = get_credential_resolver()
    if resolver is None:
        if required:
            raise ApiKeyNotFoundError(
                "A stable credential reference was supplied but the host injected "
                "no credential_resolver (matrx_ai.configure(credential_resolver=...))."
            )
        return None
    from matrx_connect.context.app_context import try_get_app_context
    from matrx_connect.credentials import (
        CredentialRef,
        CredentialRequest,
        CredentialResolutionError,
    )

    ctx = try_get_app_context()
    actor_user_id = getattr(ctx, "user_id", None) if ctx is not None else None
    if not actor_user_id:
        if required:
            raise ApiKeyNotFoundError(
                "Cannot resolve a credential reference without an authenticated "
                "AppContext actor."
            )
        return None
    try:
        resolution = await resolver.resolve(
            CredentialRequest(
                actor_user_id=actor_user_id,
                organization_id=getattr(ctx, "organization_id", None),
                ref=CredentialRef(item_id=item_id, field_key=field_key, field_id=field_id),
                consumer=consumer,  # type: ignore[arg-type]
                purpose=purpose,
                invocation_id=invocation_id,
                output="value",
            )
        )
    except CredentialResolutionError as exc:
        if required:
            raise ApiKeyNotFoundError(str(exc)) from exc
        return None
    return resolution.value


def get_api_key_resolver() -> Callable[[str], str | None] | None:
    """Return the host-injected key resolver, or None when unset."""
    resolver = get_ext(_RESOLVER_KEY) if has_ext(_RESOLVER_KEY) else None
    if resolver is not None and not callable(resolver):
        raise TypeError(
            "matrx-ai 'api_key_resolver' must be a Callable[[str], str | None]; "
            f"got {type(resolver).__name__!r}. Fix the configure() call."
        )
    return resolver


def resolve_api_key(*env_names: str, required: bool = False) -> str | None:
    """Resolve a provider API key.

    Args:
        env_names: One or more env-style key names, tried in order (e.g.
            ``resolve_api_key("GEMINI_API_KEY", "GOOGLE_API_KEY")``).
        required: When True, raise :class:`ApiKeyNotFoundError` instead of
            returning None — for call sites that previously used
            ``os.environ["X"]`` (KeyError on missing) so a missing key still
            fails loudly, with a clearer message.

    Returns:
        The first non-empty key found, or None (when ``required=False``).
    """
    if not env_names:
        raise ValueError("resolve_api_key() requires at least one env name")

    resolver = get_api_key_resolver()
    if resolver is not None:
        for name in env_names:
            value = resolver(name)
            if value:
                return value
    try:
        from matrx_connect.context.app_context import try_get_app_context

        ctx = try_get_app_context()
    except (ImportError, RuntimeError):
        ctx = None
    ambient_keys = getattr(ctx, "api_keys", None) if ctx is not None else None
    if isinstance(ambient_keys, dict):
        for name in env_names:
            shorthand = name.removesuffix("_API_KEY").lower()
            for candidate in (name, name.lower(), shorthand):
                value = ambient_keys.get(candidate)
                if value:
                    return str(value)
    for name in env_names:
        value = os.environ.get(name)
        if value:
            return value
    if required:
        raise ApiKeyNotFoundError(
            f"No API key found for {' / '.join(env_names)}. Provide it via the "
            "host's api_key_resolver (matrx_ai.configure(api_key_resolver=...)), "
            "AppContext.api_keys, or the environment variable."
        )
    return None


class keyed_provider_client:  # noqa: N801 — descriptor, used like a property
    """Data descriptor that memoizes a provider SDK client ON THE RESOLVED KEY.

    Usage::

        class OpenAIChat:
            client = keyed_provider_client(
                "OPENAI_API_KEY",
                factory=lambda api_key: AsyncOpenAI(api_key=api_key),
            )

    Semantics:
      * First access resolves the key via :func:`resolve_api_key` and builds
        the client via ``factory(api_key)``; the client is memoized on the
        INSTANCE together with the key it was built for.
      * If a later access resolves a DIFFERENT key (host rotated it), a fresh
        client is built under the new key — rotation takes effect on the next
        request with no process restart.
      * Assignment (``obj.client = stub``) PINS the value: tests and hosts can
        inject a stub/instance and re-keying is disabled for that instance.
    """

    def __init__(
        self,
        *env_names: str,
        factory: Callable[[str | None], object],
        required: bool = False,
    ) -> None:
        if not env_names:
            raise ValueError("keyed_provider_client requires at least one env name")
        self._env_names = env_names
        self._factory = factory
        self._required = required
        self._state_attr = "__keyed_client_state"
        self._build_lock = threading.Lock()

    def __set_name__(self, owner: type, name: str) -> None:
        self._state_attr = f"__keyed_client_{name}"

    def __get__(self, obj: object | None, objtype: type | None = None):
        if obj is None:
            return self
        state = obj.__dict__.get(self._state_attr)
        if state is not None and state[0]:
            return state[2]
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return self._get_or_create(obj)
        if state is not None:
            # Async dispatch preflights every keyed client off-loop. During the
            # call, use that stable client without resolving credentials again;
            # the next dispatch preflight observes key rotation.
            return state[2]
        raise RuntimeError(
            "A provider SDK client was accessed cold on the asyncio event loop. "
            "Call prepare_provider_clients(instance) before async dispatch."
        )

    def _get_or_create(self, obj: object) -> object:
        api_key = resolve_api_key(*self._env_names, required=self._required)
        state = obj.__dict__.get(self._state_attr)
        if state is not None:
            pinned, built_key, client = state
            if pinned or built_key == api_key:
                return client
        with self._build_lock:
            state = obj.__dict__.get(self._state_attr)
            if state is not None:
                pinned, built_key, client = state
                if pinned or built_key == api_key:
                    return client
            client = self._factory(api_key)
            obj.__dict__[self._state_attr] = (False, api_key, client)
            return client

    async def prepare(self, obj: object) -> object:
        return await asyncio.to_thread(self._get_or_create, obj)

    def __set__(self, obj: object, value: object) -> None:
        obj.__dict__[self._state_attr] = (True, None, value)


async def prepare_provider_clients(instance: object) -> None:
    """Construct every keyed SDK client on a worker thread before dispatch."""
    descriptors: list[keyed_provider_client] = []
    for cls in type(instance).__mro__:
        descriptors.extend(
            value for value in vars(cls).values() if isinstance(value, keyed_provider_client)
        )
    for descriptor in descriptors:
        await descriptor.prepare(instance)


__all__ = [
    "ApiKeyNotFoundError",
    "get_api_key_resolver",
    "get_credential_resolver",
    "keyed_provider_client",
    "prepare_provider_clients",
    "resolve_api_key",
    "resolve_credential_field",
]
