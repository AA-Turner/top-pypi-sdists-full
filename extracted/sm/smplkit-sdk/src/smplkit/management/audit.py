"""Smpl Audit management surface — ``mgmt.audit.*``.

Counterpart to the runtime :class:`smplkit.audit.AuditClient`. The
runtime client owns event recording and read-side queries; this client
owns SIEM forwarder CRUD:

* ``mgmt.audit.forwarders.new/get/list/save/delete`` — manage the
  customer's configured forwarders.

Async support mirrors the runtime audit client today: the
``AsyncAuditClient`` placeholder delegates to the sync surface so
async callers reach the same endpoints. Full asyncio_detailed wiring
is a follow-up; the contract on this module is stable regardless of
which transport powers it underneath.

New audit-management capabilities should add classes here, not in
``smplkit.audit.client``.
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

    Always present per ADR-014; `total` and `total_pages` are only
    populated when the request included `meta[total]=true`.
    """
    return (body_dict.get("meta") or {}).get("pagination") or {}


# ---------------------------------------------------------------------------
# Forwarders — CRUD
# ---------------------------------------------------------------------------


class ForwarderListPage:
    """A single page from ``mgmt.audit.forwarders.list(...)``.

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
    """Surface for ``mgmt.audit.forwarders.*``."""

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
                an :class:`HttpConfiguration` instance. Headers carry
                credentials and are encrypted at rest server-side;
                reads return them redacted.
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
        if (transform is None) != (transform_type is None):
            raise ValueError("transform and transform_type must be specified together")
        if transform_type == TransformType.JSONATA and not isinstance(transform, str):
            raise ValueError("transform must be a string when transform_type is JSONATA")
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

        Offset paginated per ADR-014: pass ``page_number`` (1-based) and
        ``page_size`` (default 1000, max 1000). Pass ``meta_total=True``
        to populate ``total`` and ``total_pages`` in the returned
        ``pagination`` dict (costs an extra COUNT query server-side).
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
        """Fetch a single forwarder by id; returned instance is bound to this
        client so ``forwarder.save()`` and ``forwarder.delete()`` work."""
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
        """Soft-delete a forwarder."""
        resp = _gen_delete_forwarder.sync_detailed(forwarder_id=forwarder_id, client=self._auth)
        if resp.status_code != 204:
            _raise_for_status(resp.status_code, resp.content)
            raise _SmplError(
                f"HTTP {resp.status_code} not 204",
                status_code=resp.status_code,
            )


# ---------------------------------------------------------------------------
# Top-level audit management clients
# ---------------------------------------------------------------------------


class AuditClient:
    """``mgmt.audit.*`` synchronous management surface.

    Constructed by :class:`smplkit.SmplManagementClient`; not intended
    for direct instantiation.
    """

    forwarders: ForwardersClient

    def __init__(self, *, auth_client: _AuditAuthClient) -> None:
        self._auth = auth_client
        self.forwarders = ForwardersClient(auth_client=auth_client)


class AsyncAuditClient:
    """``mgmt.audit.*`` async management surface.

    Today this delegates to the sync surface — the audit-service
    network calls are short and any awaitable wrapper is uncontroversial
    on top. Full ``asyncio_detailed`` plumbing is a follow-up; the
    contract on this client is stable regardless of which transport
    powers it underneath.
    """

    forwarders: ForwardersClient

    def __init__(self, *, auth_client: _AuditAuthClient) -> None:
        self._inner = AuditClient(auth_client=auth_client)
        self.forwarders = self._inner.forwarders


__all__ = [
    "AsyncAuditClient",
    "AuditClient",
    "ForwarderEnvironment",
    "ForwarderListPage",
    "ForwardersClient",
    "ForwarderType",
    "TransformType",
]
