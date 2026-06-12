"""SIEM forwarder CRUD for the Smpl Audit client.

Forwarders are part of the single unified audit surface. This module holds
the forwarder CRUD sub-clients that the
:class:`smplkit.audit.AuditClient` / :class:`AsyncAuditClient` expose
as ``.forwarders``:

* sync :class:`ForwardersClient` — ``forwarders.new/get/list/save/delete``
* async :class:`AsyncForwardersClient` — the genuinely-async counterpart,
  returning :class:`smplkit.audit.AsyncForwarder` active records.

The forwarder dataclasses (:class:`Forwarder`, :class:`AsyncForwarder`,
:class:`ForwarderEnvironment`, …) live in :mod:`smplkit.audit.models`.
"""

from __future__ import annotations

from typing import Any

from smplkit._generated.audit.api.forwarders import (
    create_forwarder as _gen_create_forwarder,
    delete_forwarder as _gen_delete_forwarder,
    get_forwarder as _gen_get_forwarder,
    list_forwarders as _gen_list_forwarders,
    update_forwarder as _gen_update_forwarder,
)
from smplkit._errors import Error as _SmplError, _raise_for_status
from smplkit._generated.audit.client import AuthenticatedClient as _AuditAuthClient
from smplkit._generated.audit.models.forwarder import Forwarder as _GenForwarder
from smplkit._generated.audit.models.forwarder_create_request import (
    ForwarderCreateRequest as _GenForwarderCreateRequest,
)
from smplkit._generated.audit.models.forwarder_environment import (
    ForwarderEnvironment as _GenForwarderEnvironment,
)
from smplkit._generated.audit.models.forwarder_environments import (
    ForwarderEnvironments as _GenForwarderEnvironments,
)
from smplkit._generated.audit.models.forwarder_create_resource import (
    ForwarderCreateResource as _GenForwarderCreateResource,
)
from smplkit._generated.audit.models.forwarder_filter_type_0 import (
    ForwarderFilterType0 as _GenForwarderFilter,
)
from smplkit._generated.audit.models.forwarder_request import (
    ForwarderRequest as _GenForwarderRequest,
)
from smplkit._generated.audit.models.forwarder_resource import (
    ForwarderResource as _GenForwarderResource,
)
from smplkit._generated.audit.models.http_configuration import (
    HttpConfiguration as _GenHttpConfiguration,
)
from smplkit._generated.audit.models.http_header import HttpHeader as _GenHttpHeader
from smplkit._generated.audit.types import UNSET
from smplkit.audit.models import (
    AsyncForwarder,
    Forwarder,
    ForwarderEnvironment,
    ForwarderType,
    HttpConfiguration,
    TransformType,
)


def _expect_status(resp: Any, *expected: int) -> None:
    # The generated client raises JSONDecodeError for unparseable 2xx
    # bodies before we see them, so we only need to handle status-code
    # mismatches here. _raise_for_status maps 4xx/5xx to typed errors
    # (NotFoundError, PaymentRequiredError, ValidationError, ConflictError,
    # Error); a 2xx code the caller didn't expect falls through to the
    # defensive raise below.
    if resp.status_code not in expected:
        _raise_for_status(resp.status_code, resp.content)
        raise _SmplError(
            f"HTTP {resp.status_code} not among expected {expected}",
            status_code=resp.status_code,
        )


def _extract_pagination(body_dict: dict[str, Any]) -> dict[str, int]:
    """Return the `meta.pagination` block from a list response.

    Always present; `total` and `total_pages` are only populated when the
    request included `meta[total]=true`.
    """
    return (body_dict.get("meta") or {}).get("pagination") or {}


# ---------------------------------------------------------------------------
# Forwarders — CRUD
# ---------------------------------------------------------------------------


class ForwarderListPage:
    """A single page from ``client.audit.forwarders.list(...)``.

    ``forwarders`` is the page's forwarders; ``pagination`` is the
    response's ``meta.pagination`` block (`page`, `size`, and — only
    when the caller passed `meta_total=True` — `total` and
    `total_pages`).
    """

    __slots__ = ("forwarders", "pagination")

    def __init__(
        self,
        *,
        forwarders: list[Forwarder],
        pagination: dict[str, int],
    ) -> None:
        self.forwarders = forwarders
        self.pagination = pagination

    def __iter__(self):
        return iter(self.forwarders)

    def __len__(self) -> int:
        return len(self.forwarders)


def _http_to_gen(configuration: HttpConfiguration) -> _GenHttpConfiguration:
    """Convert a wrapper HttpConfiguration to the typed generated model.

    Going through the typed constructor means a spec change that drops a
    field will fail to compile here, instead of silently passing through
    on the wire.
    """
    src = configuration._to_dict()
    headers = [_GenHttpHeader(name=h["name"], value=h["value"]) for h in src["headers"]]
    return _GenHttpConfiguration(
        url=src["url"],
        method=src["method"],
        headers=headers,
        success_status=src["success_status"],
    )


def _normalize_environments(
    environments: dict[str, ForwarderEnvironment | dict[str, Any]] | None,
) -> dict[str, ForwarderEnvironment]:
    """Coerce a caller's ``environments`` map to wrapper instances.

    Accepts either :class:`ForwarderEnvironment` values or plain dicts
    (``{"enabled": True, "configuration": HttpConfiguration(...)}``) so
    callers can use the lightweight dict form without importing the model.
    """
    if not environments:
        return {}
    out: dict[str, ForwarderEnvironment] = {}
    for env_key, value in environments.items():
        if isinstance(value, ForwarderEnvironment):
            out[env_key] = value
        else:
            out[env_key] = ForwarderEnvironment(
                enabled=bool(value.get("enabled", False)),
                configuration=value.get("configuration"),
            )
    return out


def _environments_to_gen(
    environments: dict[str, ForwarderEnvironment],
) -> _GenForwarderEnvironments:
    """Convert the wrapper ``environments`` map to the generated model.

    Per-environment ``configuration`` overrides are sent as full
    :class:`HttpConfiguration` payloads (plaintext headers in), mirroring
    the base configuration's round-trip semantics.
    """
    gen = _GenForwarderEnvironments()
    for env_key, env in environments.items():
        gen[env_key] = _GenForwarderEnvironment(
            enabled=env.enabled,
            configuration=(_http_to_gen(env.configuration) if env.configuration is not None else UNSET),
        )
    return gen


def _validate_transform(transform: Any, transform_type: TransformType | None) -> None:
    """Validate the ``transform`` / ``transform_type`` pairing (shared sync/async).

    Raises:
        ValueError: If exactly one of the two is provided, or if
            ``transform_type`` is JSONATA and ``transform`` is not a string.
    """
    if (transform is None) != (transform_type is None):
        raise ValueError("transform and transform_type must be specified together")
    if transform_type == TransformType.JSONATA and not isinstance(transform, str):
        raise ValueError("transform must be a string when transform_type is JSONATA")


def _build_forwarder_attrs(
    *,
    name: str,
    forwarder_type: ForwarderType,
    configuration: HttpConfiguration,
    environments: dict[str, ForwarderEnvironment],
    description: str | None,
    forward_smplkit_events: bool,
    filter: dict[str, Any] | None,
    transform: Any,
    transform_type: TransformType | None,
) -> _GenForwarder:
    # ``ForwarderType`` is a ``str`` subclass — passing the enum directly
    # gives the generated model a string that matches its Literal type
    # constraint, while keeping enum identity for callers reading back.
    #
    # The base ``enabled`` is server-pinned false (ADR-055); we don't send
    # it. Enablement travels entirely through ``environments``.
    attrs = _GenForwarder(
        name=name,
        forwarder_type=ForwarderType(forwarder_type).value,
        configuration=_http_to_gen(configuration),
    )
    if environments:
        attrs.environments = _environments_to_gen(environments)
    if description is not None:
        attrs.description = description
    # Additive opt-in; only put it on the wire when enabled so the default
    # (false) stays implicit and existing callers' bodies are unchanged.
    # The generated model defaults this field to ``False`` (not ``UNSET``),
    # so it would otherwise always be serialized — pin it back to ``UNSET``
    # to keep the body minimal when the caller hasn't opted in.
    attrs.forward_smplkit_events = True if forward_smplkit_events else UNSET
    if filter is not None:
        attrs.filter_ = _GenForwarderFilter.from_dict(filter)
    if transform is not None:
        attrs.transform = transform
        attrs.transform_type = TransformType(transform_type).value if transform_type is not None else None
    return attrs


class ForwardersClient:
    """Surface for ``client.audit.forwarders.*``."""

    def __init__(self, *, auth_client: _AuditAuthClient) -> None:
        self._auth = auth_client

    def new(
        self,
        id: str,
        *,
        name: str | None = None,
        forwarder_type: ForwarderType,
        configuration: HttpConfiguration,
        environments: dict[str, ForwarderEnvironment | dict[str, Any]] | None = None,
        description: str | None = None,
        forward_smplkit_events: bool = False,
        filter: dict[str, Any] | None = None,
        transform: Any = None,
        transform_type: TransformType | None = None,
    ) -> Forwarder:
        """Return an unsaved :class:`Forwarder`. Call :meth:`Forwarder.save` to persist.

        Args:
            id: Caller-supplied unique identifier (the forwarder's key).
                Unique within the account; immutable for the lifetime of
                the forwarder. The audit service returns 409 if another
                live forwarder already uses this id.
            name: Display name. Free-form. Defaults to ``id`` when not
                supplied.
            forwarder_type: A :class:`ForwarderType` enum member
                (e.g. ``ForwarderType.HTTP``, ``ForwarderType.DATADOG``).
            configuration: Destination HTTP request configuration —
                an :class:`HttpConfiguration` instance. Header values
                carry credentials: supply them plaintext on writes; reads
                return them redacted, so re-supply real values before
                saving.
            environments: Per-environment overrides keyed by environment
                key (e.g. ``"production"``). A forwarder delivers in an
                environment only when that environment's entry has
                ``enabled=True``. Values may be :class:`ForwarderEnvironment`
                instances or plain dicts (``{"enabled": True}``, optionally
                with a ``"configuration"`` :class:`HttpConfiguration`
                override). Omit to create a forwarder that delivers
                nowhere until enabled per environment.
            description: Optional free-text description.
            forward_smplkit_events: When ``True``, this forwarder also
                receives platform change events that smplkit records about
                your own resources (flag, configuration, and similar
                changes), delivered through every environment this forwarder
                is enabled in. Independent of the per-environment
                ``environments`` settings. Defaults to ``False`` — platform
                change events are not forwarded unless you opt in.
            filter: Optional JSON Logic filter; events that don't match
                are recorded as ``filtered_out`` deliveries.
            transform: Optional template applied to the event payload
                before POST. Shape depends on ``transform_type`` — for
                :attr:`TransformType.JSONATA`, a string containing a
                JSONata expression. Any value of any type is accepted.
                ``None`` sends the event as-is.
            transform_type: A :class:`TransformType` enum member naming
                the engine that evaluates ``transform``. Must be
                provided together with ``transform`` — neither field is
                meaningful in isolation.

        Raises:
            ValueError: If exactly one of ``transform`` /
                ``transform_type`` is provided, or if ``transform_type``
                is :attr:`TransformType.JSONATA` and ``transform`` is
                not a string.
        """
        _validate_transform(transform, transform_type)
        return Forwarder(
            self,
            id=id,
            name=name if name is not None else id,
            forwarder_type=forwarder_type,
            configuration=configuration,
            environments=_normalize_environments(environments),
            description=description,
            forward_smplkit_events=forward_smplkit_events,
            filter=filter,
            transform=transform,
            transform_type=transform_type,
        )

    def list(
        self,
        *,
        forwarder_type: ForwarderType | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> ForwarderListPage:
        """List forwarders for the authenticated account.

        Offset paginated: pass ``page_number`` (1-based) and ``page_size``
        (default 1000, max 1000).

        Args:
            forwarder_type: Restrict the listing to forwarders of this
                :class:`ForwarderType`. Omit to list every type.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of forwarders to return in this page
                (default 1000, max 1000).
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination`` dict
                (costs an extra count server-side). Omit to skip it.

        Returns:
            A :class:`ForwarderListPage` of the matching forwarders.
        """
        ft = ForwarderType(forwarder_type).value if forwarder_type is not None else UNSET
        resp = _gen_list_forwarders.sync_detailed(
            client=self._auth,
            filterforwarder_type=ft,
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        forwarders = [Forwarder._from_resource(r, client=self) for r in body_dict.get("data", [])]
        return ForwarderListPage(
            forwarders=forwarders,
            pagination=_extract_pagination(body_dict),
        )

    def get(self, forwarder_id: str) -> Forwarder:
        """Fetch a single forwarder by id.

        The returned instance is bound to this client, so
        ``forwarder.save()`` and ``forwarder.delete()`` work. Header values
        come back redacted — re-supply real values before saving.

        Args:
            forwarder_id: The forwarder's id (key).

        Returns:
            The matching :class:`Forwarder`, bound to this client.

        Raises:
            NotFoundError: If no live forwarder with that id exists in the
                caller's account.
        """
        resp = _gen_get_forwarder.sync_detailed(forwarder_id=forwarder_id, client=self._auth)
        _expect_status(resp, 200)
        return Forwarder._from_resource(resp.parsed.to_dict()["data"], client=self)

    def _create(self, forwarder: Forwarder) -> Forwarder:
        """POST a new forwarder. Called by :meth:`Forwarder.save` on unsaved
        instances; not intended for direct use."""
        if not forwarder.id:
            raise ValueError("Forwarder.id is required on create (caller-supplied key)")
        attrs = _build_forwarder_attrs(
            name=forwarder.name,
            forwarder_type=forwarder.forwarder_type,
            configuration=forwarder.configuration,
            environments=forwarder.environments,
            description=forwarder.description,
            forward_smplkit_events=forwarder.forward_smplkit_events,
            filter=forwarder.filter,
            transform=forwarder.transform,
            transform_type=forwarder.transform_type,
        )
        body = _GenForwarderCreateRequest(
            data=_GenForwarderCreateResource(id=forwarder.id, attributes=attrs),
        )
        resp = _gen_create_forwarder.sync_detailed(client=self._auth, body=body)
        _expect_status(resp, 201)
        return Forwarder._from_resource(resp.parsed.to_dict()["data"], client=self)

    def _update(self, forwarder: Forwarder) -> Forwarder:
        """Full-replace PUT for an existing forwarder. Called by
        :meth:`Forwarder.save` on instances with ``created_at``; not intended
        for direct use.

        Header values must be re-supplied as plaintext; the GET path redacts
        them, so a PUT body containing ``"<redacted>"`` would persist that
        literal. Track real header values client-side and round-trip them.
        """
        if not forwarder.id:
            raise ValueError("cannot update a Forwarder with no id")
        attrs = _build_forwarder_attrs(
            name=forwarder.name,
            forwarder_type=forwarder.forwarder_type,
            configuration=forwarder.configuration,
            environments=forwarder.environments,
            description=forwarder.description,
            forward_smplkit_events=forwarder.forward_smplkit_events,
            filter=forwarder.filter,
            transform=forwarder.transform,
            transform_type=forwarder.transform_type,
        )
        body = _GenForwarderRequest(data=_GenForwarderResource(id=forwarder.id, attributes=attrs))
        resp = _gen_update_forwarder.sync_detailed(forwarder_id=forwarder.id, client=self._auth, body=body)
        _expect_status(resp, 200)
        return Forwarder._from_resource(resp.parsed.to_dict()["data"], client=self)

    def delete(self, forwarder_id: str) -> None:
        """Delete a forwarder.

        Args:
            forwarder_id: The id (key) of the forwarder to delete.
        """
        resp = _gen_delete_forwarder.sync_detailed(forwarder_id=forwarder_id, client=self._auth)
        if resp.status_code != 204:
            _raise_for_status(resp.status_code, resp.content)
            raise _SmplError(
                f"HTTP {resp.status_code} not 204",
                status_code=resp.status_code,
            )


class AsyncForwardersClient:
    """Async surface for forwarder CRUD (``AsyncAuditClient.forwarders``).

    Genuinely async — every method performs its network round-trip with
    ``await`` and returns :class:`AsyncForwarder` active records whose
    ``save()`` / ``delete()`` are also coroutines.
    """

    def __init__(self, *, auth_client: _AuditAuthClient) -> None:
        self._auth = auth_client

    def new(
        self,
        id: str,
        *,
        name: str | None = None,
        forwarder_type: ForwarderType,
        configuration: HttpConfiguration,
        environments: dict[str, ForwarderEnvironment | dict[str, Any]] | None = None,
        description: str | None = None,
        forward_smplkit_events: bool = False,
        filter: dict[str, Any] | None = None,
        transform: Any = None,
        transform_type: TransformType | None = None,
    ) -> AsyncForwarder:
        """Return an unsaved :class:`AsyncForwarder`. ``await forwarder.save()`` to persist.

        Args:
            id: Caller-supplied unique identifier (the forwarder's key).
                Unique within the account; immutable for the lifetime of
                the forwarder. The audit service returns 409 if another
                live forwarder already uses this id.
            name: Display name. Free-form. Defaults to ``id`` when not
                supplied.
            forwarder_type: A :class:`ForwarderType` enum member
                (e.g. ``ForwarderType.HTTP``, ``ForwarderType.DATADOG``).
            configuration: Destination HTTP request configuration —
                an :class:`HttpConfiguration` instance. Header values
                carry credentials: supply them plaintext on writes; reads
                return them redacted, so re-supply real values before
                saving.
            environments: Per-environment overrides keyed by environment
                key (e.g. ``"production"``). A forwarder delivers in an
                environment only when that environment's entry has
                ``enabled=True``. Values may be :class:`ForwarderEnvironment`
                instances or plain dicts (``{"enabled": True}``, optionally
                with a ``"configuration"`` :class:`HttpConfiguration`
                override). Omit to create a forwarder that delivers
                nowhere until enabled per environment.
            description: Optional free-text description.
            forward_smplkit_events: When ``True``, this forwarder also
                receives platform change events that smplkit records about
                your own resources (flag, configuration, and similar
                changes), delivered through every environment this forwarder
                is enabled in. Independent of the per-environment
                ``environments`` settings. Defaults to ``False`` — platform
                change events are not forwarded unless you opt in.
            filter: Optional JSON Logic filter; events that don't match
                are recorded as ``filtered_out`` deliveries.
            transform: Optional template applied to the event payload
                before POST. Shape depends on ``transform_type`` — for
                :attr:`TransformType.JSONATA`, a string containing a
                JSONata expression. Any value of any type is accepted.
                ``None`` sends the event as-is.
            transform_type: A :class:`TransformType` enum member naming
                the engine that evaluates ``transform``. Must be
                provided together with ``transform`` — neither field is
                meaningful in isolation.

        Raises:
            ValueError: If exactly one of ``transform`` /
                ``transform_type`` is provided, or if ``transform_type``
                is :attr:`TransformType.JSONATA` and ``transform`` is
                not a string.
        """
        _validate_transform(transform, transform_type)
        return AsyncForwarder(
            self,
            id=id,
            name=name if name is not None else id,
            forwarder_type=forwarder_type,
            configuration=configuration,
            environments=_normalize_environments(environments),
            description=description,
            forward_smplkit_events=forward_smplkit_events,
            filter=filter,
            transform=transform,
            transform_type=transform_type,
        )

    async def list(
        self,
        *,
        forwarder_type: ForwarderType | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
        meta_total: bool | None = None,
    ) -> ForwarderListPage:
        """List forwarders for the authenticated account, awaited.

        Offset paginated: pass ``page_number`` (1-based) and ``page_size``
        (default 1000, max 1000).

        Args:
            forwarder_type: Restrict the listing to forwarders of this
                :class:`ForwarderType`. Omit to list every type.
            page_number: 1-based page index. Omit for the first page.
            page_size: Maximum number of forwarders to return in this page
                (default 1000, max 1000).
            meta_total: When ``True``, populate ``total`` and
                ``total_pages`` in the returned page's ``pagination`` dict
                (costs an extra count server-side). Omit to skip it.

        Returns:
            A :class:`ForwarderListPage` of the matching forwarders.
        """
        ft = ForwarderType(forwarder_type).value if forwarder_type is not None else UNSET
        resp = await _gen_list_forwarders.asyncio_detailed(
            client=self._auth,
            filterforwarder_type=ft,
            pagenumber=page_number if page_number is not None else UNSET,
            pagesize=page_size if page_size is not None else UNSET,
            metatotal=meta_total if meta_total is not None else UNSET,
        )
        _expect_status(resp, 200)
        body_dict = resp.parsed.to_dict()
        forwarders = [AsyncForwarder._from_resource(r, client=self) for r in body_dict.get("data", [])]
        return ForwarderListPage(forwarders=forwarders, pagination=_extract_pagination(body_dict))

    async def get(self, forwarder_id: str) -> AsyncForwarder:
        """Fetch a single forwarder by id, awaited.

        The returned instance is bound to this client, so
        ``await forwarder.save()`` and ``await forwarder.delete()`` work.
        Header values come back redacted — re-supply real values before
        saving.

        Args:
            forwarder_id: The forwarder's id (key).

        Returns:
            The matching :class:`AsyncForwarder`, bound to this client.

        Raises:
            NotFoundError: If no live forwarder with that id exists in the
                caller's account.
        """
        resp = await _gen_get_forwarder.asyncio_detailed(forwarder_id=forwarder_id, client=self._auth)
        _expect_status(resp, 200)
        return AsyncForwarder._from_resource(resp.parsed.to_dict()["data"], client=self)

    async def _create(self, forwarder: Forwarder) -> AsyncForwarder:
        if not forwarder.id:
            raise ValueError("Forwarder.id is required on create (caller-supplied key)")
        attrs = _build_forwarder_attrs(
            name=forwarder.name,
            forwarder_type=forwarder.forwarder_type,
            configuration=forwarder.configuration,
            environments=forwarder.environments,
            description=forwarder.description,
            forward_smplkit_events=forwarder.forward_smplkit_events,
            filter=forwarder.filter,
            transform=forwarder.transform,
            transform_type=forwarder.transform_type,
        )
        body = _GenForwarderCreateRequest(data=_GenForwarderCreateResource(id=forwarder.id, attributes=attrs))
        resp = await _gen_create_forwarder.asyncio_detailed(client=self._auth, body=body)
        _expect_status(resp, 201)
        return AsyncForwarder._from_resource(resp.parsed.to_dict()["data"], client=self)

    async def _update(self, forwarder: Forwarder) -> AsyncForwarder:
        if not forwarder.id:
            raise ValueError("cannot update a Forwarder with no id")
        attrs = _build_forwarder_attrs(
            name=forwarder.name,
            forwarder_type=forwarder.forwarder_type,
            configuration=forwarder.configuration,
            environments=forwarder.environments,
            description=forwarder.description,
            forward_smplkit_events=forwarder.forward_smplkit_events,
            filter=forwarder.filter,
            transform=forwarder.transform,
            transform_type=forwarder.transform_type,
        )
        body = _GenForwarderRequest(data=_GenForwarderResource(id=forwarder.id, attributes=attrs))
        resp = await _gen_update_forwarder.asyncio_detailed(forwarder_id=forwarder.id, client=self._auth, body=body)
        _expect_status(resp, 200)
        return AsyncForwarder._from_resource(resp.parsed.to_dict()["data"], client=self)

    async def delete(self, forwarder_id: str) -> None:
        """Delete a forwarder, awaited.

        Args:
            forwarder_id: The id (key) of the forwarder to delete.
        """
        resp = await _gen_delete_forwarder.asyncio_detailed(forwarder_id=forwarder_id, client=self._auth)
        if resp.status_code != 204:
            _raise_for_status(resp.status_code, resp.content)
            raise _SmplError(
                f"HTTP {resp.status_code} not 204",
                status_code=resp.status_code,
            )


__all__ = [
    "AsyncForwardersClient",
    "ForwarderEnvironment",
    "ForwarderListPage",
    "ForwardersClient",
    "ForwarderType",
    "TransformType",
]


# The forwarders sub-client is reached through ``client.audit.forwarders``;
# present it as ``smplkit.audit.<Name>`` in IDE hover / help() rather than the
# private ``smplkit.audit._forwarders`` path.
ForwardersClient.__module__ = "smplkit.audit"
AsyncForwardersClient.__module__ = "smplkit.audit"
