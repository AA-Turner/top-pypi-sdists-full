"""Shared httpx plumbing for the sync + async clients.

Centralises three things that would otherwise drift between
:class:`hogland.Hogland` and :class:`hogland.AsyncHogland`:

* Building the ``httpx.Client`` / ``AsyncClient`` with the same base
  URL, bearer header, and timeout policy.
* Normalising config lookup: ``HOG_HOST`` / ``HOG_TOKEN`` env vars,
  matching the hogland CLI (``pkg/cliconfig/cliconfig.go``).
* Mapping non-2xx responses to the typed exception tree in
  :mod:`hogland._errors`.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

import httpx

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Mapping, Sequence

from ._errors import APIError, ConfigurationError, from_status
from ._version import __version__

DEFAULT_BASE_URL = "https://hogland.prod-us.posthog.dev"
DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=10.0, read=30.0, write=30.0)


def resolve_base_url(base_url: str | None) -> str:
    """Resolve the API base URL from arg → env → default."""
    if base_url:
        return base_url.rstrip("/")
    env = os.environ.get("HOG_HOST")
    if env:
        return env.rstrip("/")
    return DEFAULT_BASE_URL


def resolve_token(token: str | None) -> str:
    """Resolve the bearer token from arg → env, raising if absent."""
    if token:
        return token
    env = os.environ.get("HOG_TOKEN")
    if env:
        return env
    msg = (
        "hogland: no API token provided. Pass token=... to the client "
        "or set HOG_TOKEN in the environment."
    )
    raise ConfigurationError(msg)


class _BearerAuth(httpx.Auth):
    """Per-request bearer injection from a token-provider callable.

    Used when the client is constructed with ``token_provider=``: the
    callable runs on every request, so a credential that rotates on disk
    (K8s projected ServiceAccount tokens are rewritten ~every 50 min)
    is always presented fresh. httpx adapts the sync generator for the
    async client, so one implementation serves both.
    """

    def __init__(self, provider: Callable[[], str]) -> None:
        self._provider = provider

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self._provider()}"
        yield request


def token_provider_from_file(path: str | os.PathLike[str]) -> Callable[[], str]:
    """Return a provider that re-reads a token file on every call.

    The read-per-call is the point: K8s rewrites projected SA token
    files in place, so caching the contents would 401 after the first
    rotation. Existence is checked eagerly so a mistyped mount path
    fails at construction with a clear error, not on the first request.
    """
    resolved = Path(path)
    if not resolved.is_file():
        msg = f"hogland: token file not found: {resolved}"
        raise ConfigurationError(msg)

    def read_token() -> str:
        # Re-read on every request, so wrap the I/O: the kubelet swaps the
        # projected token in atomically via a symlink flip, and a read that
        # races that swap can raise a transient OSError. Surface it as our
        # own ConfigurationError instead of leaking a raw OSError out of the
        # httpx auth hook.
        try:
            return resolved.read_text(encoding="utf-8").strip()
        except OSError as exc:
            msg = f"hogland: failed to read token file: {resolved}"
            raise ConfigurationError(msg) from exc

    return read_token


def base_headers() -> dict[str, str]:
    """Non-auth default request headers."""
    return {
        "User-Agent": f"hogland-python/{__version__}",
        "Accept": "application/json",
    }


def default_headers(token: str) -> dict[str, str]:
    """Default request headers.

    ``Authorization: Bearer <token>`` is the wire format for *all*
    AUTH_PLAN paths — long-lived APIToken (Path 1), K8s ServiceAccount
    JWT verified cross-account via EKS OIDC (Path 3), and GitHub OIDC.
    Hogplane parses the credential and selects the resolution path
    server-side; the SDK is intentionally credential-agnostic.
    """
    return {"Authorization": f"Bearer {token}", **base_headers()}


def _build_create_body(  # noqa: PLR0912, PLR0913, C901 — mirrors the BoxSpec wire shape
    *,
    cpus: float | None,
    memory_mib: int | None,
    disk_gib: int | None,
    disk_class: object | None,
    disk_mbps: int,
    disk_iops: int,
    net_mbps: float,
    access_type: object | None,
    snapshot_id: str | None,
    ssh_public_key: str | None,
    bootstrap: str | None,
    env: Mapping[str, str] | None,
    ttl_seconds: int | None,
    name: str | None,
    kind: str | None,
    tags: Sequence[str] | None,
    web_port: int | None = None,
) -> dict[str, Any]:
    """Build the create-box request body, omitting fields the caller didn't set.

    ``cpus`` / ``memory_mib`` / ``disk_gib`` / ``disk_class`` are omitted
    when ``None`` so the server's ``applyDefaults`` fills them in for
    fresh creates and so they inherit from the snapshot on restore (the
    spec requires omission or exact match on ``snapshot_id`` calls).
    ``disk_mbps`` / ``disk_iops`` / ``net_mbps`` are always sent because
    ``0`` is an explicit "unthrottled" value, distinct from "omitted".

    We don't run this through pydantic ``CreateBoxRequest`` because that
    model copies the spec's ``required: [cpus, memory_mib, ...]`` list,
    which contradicts the server's ``applyDefaults`` + snapshot-inherit
    behaviour. Hand-built dict avoids the mismatch; server-side
    validation still enforces ranges.
    """
    body: dict[str, Any] = {
        "disk_mbps": disk_mbps,
        "disk_iops": disk_iops,
        "net_mbps": net_mbps,
    }
    if cpus is not None:
        body["cpus"] = cpus
    if memory_mib is not None:
        body["memory_mib"] = memory_mib
    if disk_gib is not None:
        body["disk_gib"] = disk_gib
    if disk_class is not None:
        body["disk_class"] = str(disk_class)
    if access_type is not None:
        body["access_type"] = str(access_type)
    elif ssh_public_key is None and snapshot_id is None:
        # The server default is ssh-public, which REQUIRES ssh_public_key
        # on cold boot — so the README's minimal create() would 400. An
        # SDK consumer without a key drives the box through exec/files/
        # proxy anyway; "none" is the shape that works. Restores are
        # excluded: they inherit the snapshot's access_type + baked keys.
        body["access_type"] = "none"
    if snapshot_id is not None:
        body["snapshot_id"] = snapshot_id
    if ssh_public_key is not None:
        body["ssh_public_key"] = ssh_public_key
    if bootstrap is not None:
        body["bootstrap"] = bootstrap
    if env is not None:
        body["env"] = dict(env)
    if ttl_seconds is not None:
        body["ttl_seconds"] = ttl_seconds
    if name is not None:
        body["name"] = name
    if kind is not None:
        body["kind"] = kind
    if tags is not None:
        body["tags"] = list(tags)
    if web_port is not None:
        # Opt the box into HTTP exposure at its own per-box hostname
        # (https://<box>.<box-edge>/). Sent as a flat ``web_port`` int;
        # requires the "exec" boot feature server-side. Range-check
        # client-side (the CLI does too) so a bad port fails fast with a clear
        # error instead of a server 4xx mid-create.
        if not 1 <= web_port <= 65535:
            raise ValueError(f"web_port must be in 1-65535 (got {web_port})")
        body["web_port"] = web_port
    return body


_UNSET: Any = object()
"""Sentinel distinguishing "leave the field alone" from explicit values
in pen PATCH kwargs — ``current_box_id=""`` clears the pointer (the
server's pointer-typed patch shape), while omitting the kwarg sends
nothing. ``None`` can't carry both meanings."""


def _pen_path(name: str) -> str:
    return f"/v1/pens/{quote(name, safe='')}"


def _spec_to_wire(spec: Any) -> dict[str, Any]:
    """Normalise a ``BoxSpec`` model or plain mapping to a JSON dict."""
    if hasattr(spec, "model_dump"):
        return spec.model_dump(exclude_none=True, by_alias=True, exclude={"field_schema"})
    return dict(spec)


def _build_pen_create_body(  # noqa: PLR0913 — mirrors the CreatePenRequest wire shape
    *,
    name: str,
    source_alias: str | None,
    spec: Any | None,
    on_idle: str | None,
    wake: str | None,
    metadata: Mapping[str, str] | None,
) -> dict[str, Any]:
    """Build the create-pen request body, omitting fields the caller didn't set."""
    body: dict[str, Any] = {"name": name}
    if source_alias is not None:
        body["source_alias"] = source_alias
    if spec is not None:
        body["spec"] = _spec_to_wire(spec)
    if on_idle is not None:
        body["on_idle"] = on_idle
    if wake is not None:
        body["wake"] = wake
    if metadata is not None:
        body["metadata"] = dict(metadata)
    return body


def _build_pen_patch_body(  # noqa: PLR0913 — mirrors the UpdatePenRequest wire shape
    *,
    current_box_id: str | Any,
    latest_snapshot_id: str | Any,
    source_alias: str | Any,
    spec: Any,
    on_idle: str | Any,
    wake: str | Any,
    metadata: Mapping[str, str] | Any,
) -> dict[str, Any]:
    """Build the PATCH /v1/pens/{name} body from sentinel-defaulted kwargs.

    Only fields whose kwarg moved off ``_UNSET`` are sent — the server's
    patch shape is pointer-typed, so presence means "set" (including
    explicit empty: ``current_box_id=""`` clears the pointer, and
    ``metadata={}`` clears the map, which otherwise replaces wholesale).
    """
    fields: dict[str, Any] = {
        "current_box_id": current_box_id,
        "latest_snapshot_id": latest_snapshot_id,
        "source_alias": source_alias,
        "spec": spec,
        "on_idle": on_idle,
        "wake": wake,
        "metadata": metadata,
    }
    body: dict[str, Any] = {}
    for key, value in fields.items():
        if value is _UNSET:
            continue
        if value is None:
            # Explicit None is ambiguous: a JSON null reads as "absent"
            # to the server's pointer-typed patch, silently doing
            # nothing. Reject it with the correct spelling instead.
            msg = (
                f"update_pen: {key}=None is ambiguous — omit the kwarg to "
                'leave the field unchanged, or pass an explicit empty ("" '
                "for ids/strings, {} for metadata) to clear it"
            )
            raise ValueError(msg)
        if key == "spec":
            body[key] = _spec_to_wire(value)
        elif key == "metadata":
            body[key] = dict(value)
        else:
            body[key] = value
    if not body:
        msg = "update_pen: pass at least one field to change"
        raise ValueError(msg)
    return body


def raise_for_status(response: httpx.Response) -> None:
    """Map a non-2xx response to the typed exception tree.

    The server returns ``application/problem+json`` (RFC 7807) for
    errors; we parse the body when present and surface the ``detail``
    field as the message. The full body is attached to ``APIError.body``
    so callers can inspect ``type``/``title``/``instance``/etc.
    """
    if response.is_success:
        return
    body: dict[str, Any] | None = None
    detail: str | None = None
    ctype = response.headers.get("content-type", "")
    if "json" in ctype:
        try:
            parsed = response.json()
        except ValueError:
            parsed = None
        if isinstance(parsed, dict):
            body = parsed
            detail = parsed.get("detail") or parsed.get("title")
    request = response.request
    message = detail or (f"hogland {request.method} {request.url}: HTTP {response.status_code}")
    raise from_status(response.status_code, message, body)


def _auth_kwargs(
    token: str | None,
    token_provider: Callable[[], str] | None,
) -> tuple[dict[str, Any], str | None]:
    """Resolve the credential into httpx constructor kwargs.

    ``token_provider`` wins over ``token`` / ``$HOG_TOKEN``: a caller
    passing both has opted into rotation, and the static value would
    otherwise silently mask it. With a provider the Authorization header
    is set per request by :class:`_BearerAuth`; without one it is baked
    into the client's default headers as before.
    """
    if token_provider is not None:
        return {"headers": base_headers(), "auth": _BearerAuth(token_provider)}, None
    resolved_token = resolve_token(token)
    return {"headers": default_headers(resolved_token)}, resolved_token


def build_sync_client(  # noqa: PLR0913 — keyword-only pass-through of httpx.Client kwargs
    *,
    base_url: str | None,
    token: str | None,
    timeout: httpx.Timeout | float | None,
    transport: httpx.BaseTransport | None,
    token_provider: Callable[[], str] | None = None,
    trust_env: bool = True,
) -> tuple[httpx.Client, str, str | None]:
    """Build a sync httpx.Client plus the resolved (base_url, token).

    The returned token is ``None`` when a ``token_provider`` is in play —
    there is no single static credential to surface.

    ``trust_env=False`` makes the client ignore ``HTTP(S)_PROXY`` / ``NO_PROXY``
    and other environment configuration. Pass it when the caller reaches hogland
    over an in-cluster / PrivateLink path that must not go through an egress
    proxy.
    """
    resolved_url = resolve_base_url(base_url)
    auth_kwargs, resolved_token = _auth_kwargs(token, token_provider)
    client = httpx.Client(
        base_url=resolved_url,
        timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        transport=transport,
        trust_env=trust_env,
        **auth_kwargs,
    )
    return client, resolved_url, resolved_token


def build_async_client(  # noqa: PLR0913 — keyword-only pass-through of httpx.AsyncClient kwargs
    *,
    base_url: str | None,
    token: str | None,
    timeout: httpx.Timeout | float | None,
    transport: httpx.AsyncBaseTransport | None,
    token_provider: Callable[[], str] | None = None,
    trust_env: bool = True,
) -> tuple[httpx.AsyncClient, str, str | None]:
    """Build an async httpx.AsyncClient plus the resolved (base_url, token).

    The returned token is ``None`` when a ``token_provider`` is in play —
    there is no single static credential to surface.

    ``trust_env=False`` makes the client ignore ``HTTP(S)_PROXY`` / ``NO_PROXY``
    and other environment configuration. Pass it when the caller reaches hogland
    over an in-cluster / PrivateLink path that must not go through an egress
    proxy.
    """
    resolved_url = resolve_base_url(base_url)
    auth_kwargs, resolved_token = _auth_kwargs(token, token_provider)
    client = httpx.AsyncClient(
        base_url=resolved_url,
        timeout=timeout if timeout is not None else DEFAULT_TIMEOUT,
        transport=transport,
        trust_env=trust_env,
        **auth_kwargs,
    )
    return client, resolved_url, resolved_token


__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_TIMEOUT",
    "APIError",
    "base_headers",
    "build_async_client",
    "build_sync_client",
    "default_headers",
    "raise_for_status",
    "resolve_base_url",
    "resolve_token",
    "token_provider_from_file",
]
