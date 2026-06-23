"""Audit resource models exposed by the SDK.

The wrapper layer's domain types — ``Event``, ``Forwarder``,
``HttpConfiguration``, ``ForwarderEnvironment``, ``ResourceType``,
``EventType`` — sit on top of the auto-generated
``smplkit._generated.audit.models``. The split keeps the public-facing
SDK surface stable across regenerations.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

if TYPE_CHECKING:
    from smplkit.audit.forwarders import ForwardersClient


class ForwarderType(str, enum.Enum):
    """Supported SIEM forwarder destination types.

    The audit service declares ``forwarder_type`` as a string with an
    enum constraint; this Python-side Enum mirrors that constraint so
    customers get autocomplete and type-checked values instead of
    stringly-typed inputs. ``str`` subclassing keeps interop with the
    auto-generated client transparent — a ``ForwarderType`` member
    compares equal to its string literal (``ForwarderType.HTTP ==
    "http"``).

    The available types are real-time HTTP destinations sharing one
    outbound delivery path. Object-storage archival (S3, GCS, etc.) has
    a different operational shape (batching, IAM, lifecycle policies) and
    may get its own type if customer demand warrants.
    """

    DATADOG = "datadog"
    ELASTIC = "elastic"
    HONEYCOMB = "honeycomb"
    HTTP = "http"
    NEW_RELIC = "new_relic"
    SPLUNK_HEC = "splunk_hec"
    SUMO_LOGIC = "sumo_logic"


class HttpMethod(str, enum.Enum):
    """HTTP verb used by a forwarder's outbound delivery.

    Mirrors the audit spec's ``HttpConfigurationMethod`` enum so
    customers get autocomplete and a typed value back from
    ``forwarder.configuration.method``. ``str`` subclassing keeps
    interop with raw strings transparent (``HttpMethod.POST == "POST"``).
    """

    DELETE = "DELETE"
    GET = "GET"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"


class TransformType(str, enum.Enum):
    """Engine used to evaluate a forwarder's ``transform``.

    Today only :attr:`JSONATA` is supported. ``str`` subclassing keeps
    interop with raw strings transparent
    (``TransformType.JSONATA == "JSONATA"``).
    """

    JSONATA = "JSONATA"


@dataclass(frozen=True, slots=True)
class Event:
    """A single audit event as returned by the audit service.

    Field set mirrors the JSON:API resource attributes plus the resource
    ``id``.

    Actor attribution (``actor_type``, ``actor_id``, ``actor_label``) is
    customer-supplied and all three are free-form, nullable strings. The
    audit service stores whatever the caller passed in and never
    backfills from the request credential — callers that want events
    attributed to the calling user or API key must populate the fields
    themselves on ``record(...)``.

    Attributes:
        id (UUID): Server-assigned UUID for this event.
        event_type (str): What happened (e.g. ``"user.created"``,
            ``"invoice.paid"``). Any non-empty string.
        resource_type (str): Kind of resource the event is about
            (e.g. ``"invoice"``). Any non-empty string.
        resource_id (str): Identifier of the specific resource the
            event is about.
        occurred_at (datetime): When the event actually happened, as
            reported by the source.
        created_at (datetime): When the audit service first ingested
            this event.
        actor_type (str | None): Kind of actor that caused the event
            (e.g. ``"USER"``, ``"API_KEY"``, ``"SYSTEM"``, or any label
            the caller chose). ``None`` when not supplied.
        actor_id (str | None): Identifier of the actor that caused the
            event. Free-form — any identifier scheme is accepted.
            ``None`` when not supplied.
        actor_label (str | None): Human-readable label for the actor
            (e.g. an email address or API key name). ``None`` when not
            supplied.
        category (str | None): Free-form bucket label for the event
            (e.g. ``"auth"``, ``"billing"``, ``"config-change"``). Stored
            exactly as supplied; drives the audit log's category filter and
            the ``categories`` discovery listing
            (:meth:`~smplkit.audit.AuditClient.categories`). ``None`` when
            not supplied.
        data (dict[str, Any]): Free-form per-event payload defined by
            the customer. Surfaced on the audit-event resource as a
            structured JSONB column.
        idempotency_key (str): Customer-supplied dedupe key. Empty when
            the customer didn't supply one.
        do_not_forward (bool): When ``True``, skip this event from SIEM
            forwarder delivery regardless of any matching forwarder
            filter.
        environment (str | None): The environment the event was recorded
            in. Read-only and always present on reads — the audit service
            resolves it when the event is recorded (from a
            single-environment credential, or from the runtime SDK's
            configured environment, which the SDK sends on the recording
            request body).
    """

    id: UUID
    event_type: str
    resource_type: str
    resource_id: str
    occurred_at: datetime
    created_at: datetime
    actor_type: str | None = None
    actor_id: str | None = None
    actor_label: str | None = None
    category: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    idempotency_key: str = ""
    do_not_forward: bool = False
    environment: str | None = None

    @classmethod
    def _from_resource(cls, resource: dict[str, Any]) -> "Event":
        attrs = resource.get("attributes", {})
        return cls(
            id=UUID(resource["id"]),
            event_type=attrs["event_type"],
            resource_type=attrs["resource_type"],
            resource_id=attrs["resource_id"],
            actor_type=attrs.get("actor_type"),
            actor_id=attrs.get("actor_id"),
            actor_label=attrs.get("actor_label"),
            category=attrs.get("category"),
            occurred_at=_parse_iso(attrs["occurred_at"]),
            created_at=_parse_iso(attrs["created_at"]),
            data=attrs.get("data") or {},
            idempotency_key=attrs.get("idempotency_key") or "",
            do_not_forward=bool(attrs.get("do_not_forward", False)),
            environment=attrs.get("environment"),
        )


class HttpConfiguration:
    """Forwarder destination HTTP request shape — the base configuration.

    Attributes:
        url (str): Destination URL the audit service delivers each event to.
        method (HttpMethod): HTTP verb used for delivery. Defaults to
            ``HttpMethod.POST``.
        headers (dict[str, str]): Headers attached to every outbound request,
            as a name→value object (e.g. ``{"DD-API-KEY": "s3cr3t"}``). Use
            :meth:`set_header` / :meth:`get_header` to read and write
            individual headers. Values often carry credentials and are
            returned in plaintext on reads, so a get-mutate-put round-trip
            preserves them without re-entering secrets.
        success_status (str): Status the destination must return for delivery
            to count as success — either an exact code (``"200"``, ``"204"``)
            or a class (``"2xx"``, ``"4xx"``). Defaults to ``"2xx"``.
        tls_verify (bool): Whether to verify the destination's TLS certificate
            chain. Defaults to ``True``; flip to ``False`` only for short-lived
            testing against a destination that serves an untrusted certificate.
            Prefer pinning the issuing CA via ``ca_cert`` for long-lived
            self-signed setups.
        ca_cert (str | None): Optional PEM-encoded certificate (or bundle)
            trusted in addition to the system CA store. Ignored when
            ``tls_verify`` is ``False``. ``None`` (the default) means
            "use system CAs only".
    """

    def __init__(
        self,
        *,
        url: str = "",
        method: str = "POST",
        headers: Optional[dict[str, str]] = None,
        success_status: str = "2xx",
        tls_verify: bool = True,
        ca_cert: Optional[str] = None,
    ) -> None:
        self.url = url
        self.method = method
        self.headers: dict[str, str] = dict(headers or {})
        self.success_status = success_status
        self.tls_verify = tls_verify
        self.ca_cert = ca_cert

    def set_header(self, name: str, value: str) -> None:
        """Set (or replace) a single request header by name."""
        self.headers[name] = value

    def get_header(self, name: str) -> Optional[str]:
        """The value of header ``name``, or ``None`` if it is not set."""
        return self.headers.get(name)

    def _to_dict(self) -> dict[str, Any]:
        return {
            "method": HttpMethod(self.method).value,
            "url": self.url,
            "headers": dict(self.headers),
            "success_status": self.success_status,
            "tls_verify": self.tls_verify,
            "ca_cert": self.ca_cert,
        }

    @classmethod
    def _from_dict(cls, raw: dict[str, Any]) -> "HttpConfiguration":
        # Absent ``tls_verify`` on the wire means a forwarder persisted
        # before the field landed — default to verifying so its prior
        # secure behaviour is preserved.
        tls_verify_raw = raw.get("tls_verify")
        return cls(
            url=raw.get("url") or "",
            method=HttpMethod(raw.get("method") or HttpMethod.POST),
            headers=dict(raw.get("headers") or {}),
            success_status=raw.get("success_status") or "2xx",
            tls_verify=True if tls_verify_raw is None else bool(tls_verify_raw),
            ca_cert=raw.get("ca_cert"),
        )

    def __repr__(self) -> str:
        return f"HttpConfiguration(method={self.method!r}, url={self.url!r})"


# The request-config leaves an environment may override (everything except
# headers, which are addressed individually as ``headers.<name>``). These map
# 1:1 onto :class:`HttpConfiguration` fields and onto top-level overlay leaf
# paths.
_SCALAR_LEAVES = ("url", "method", "success_status", "tls_verify", "ca_cert")


class ForwarderEnvironment:
    """One environment's **sparse override** for a forwarder (ADR-056).

    A forwarder's :attr:`Forwarder.environments` map holds one of these per
    environment. Only the leaves you set are sent on save; everything you
    leave unset is inherited from the forwarder's base definition, and the
    server resolves base ⊕ overrides when an event is delivered. The base
    definition delivers nowhere, so a forwarder delivers in an environment
    only when that environment's override sets ``enabled=True``.

    Set overrides through :meth:`Forwarder.environment`, e.g.
    ``forwarder.environment("production").url = "https://prod.siem.example.com/in"``.

    **Reading a leaf returns this environment's override, or ``None`` when it
    does not override that leaf** — the SDK does not merge in the base value
    (forwarders resolve server-side). To see a base value, read the
    forwarder's base definition (``forwarder.configuration``).

    Attributes:
        enabled (bool): Whether the forwarder delivers events in this
            environment. Defaults to ``False``.
        url, method, success_status, tls_verify, ca_cert: Per-environment
            overrides of the corresponding base request field. ``None``
            inherits the base :attr:`Forwarder.configuration` value.
        headers (dict[str, str]): Per-environment header overrides, as a
            name→value object. Each entry overrides (or adds) that one header
            by name on top of the base headers, leaving the rest inherited.
            Use :meth:`set_header` / :meth:`get_header`.
    """

    def __init__(
        self,
        *,
        enabled: bool = False,
        url: Optional[str] = None,
        method: Optional[str] = None,
        success_status: Optional[str] = None,
        tls_verify: Optional[bool] = None,
        ca_cert: Optional[str] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        self.enabled = enabled
        self.url = url
        self.method = method
        self.success_status = success_status
        self.tls_verify = tls_verify
        self.ca_cert = ca_cert
        self.headers: dict[str, str] = dict(headers or {})

    def set_header(self, name: str, value: str) -> None:
        """Override (or add) a single header by name in this environment."""
        self.headers[name] = value

    def get_header(self, name: str) -> Optional[str]:
        """This environment's override for header ``name``, or ``None`` when it
        does not override that header."""
        return self.headers.get(name)

    @classmethod
    def _from_dict(cls, raw: dict[str, Any]) -> "ForwarderEnvironment":
        """Parse the flat leaf-path overlay the server returns (ADR-056).

        Header leaves arrive as ``headers.<name>`` (parsed on the first dot,
        so a dotted header name like ``X-Foo.Bar`` is preserved); every other
        leaf is a single top-level key. Unknown leaves are ignored for forward
        compatibility.
        """
        headers: dict[str, str] = {}
        scalars: dict[str, Any] = {}
        for key, value in (raw or {}).items():
            group, _, name = key.partition(".")
            if group == "headers" and name:
                headers[name] = value
            elif key in _SCALAR_LEAVES or key == "enabled":
                scalars[key] = value
        return cls(
            enabled=bool(scalars.get("enabled", False)),
            url=scalars.get("url"),
            method=scalars.get("method"),
            success_status=scalars.get("success_status"),
            tls_verify=scalars.get("tls_verify"),
            ca_cert=scalars.get("ca_cert"),
            headers=headers,
        )

    def _to_payload(self) -> dict[str, Any]:
        """Emit the flat sparse leaf-path overlay (ADR-056) — ``enabled`` plus
        only the leaves this environment overrides, with each header as a
        ``headers.<name>`` leaf."""
        payload: dict[str, Any] = {"enabled": self.enabled}
        for leaf in _SCALAR_LEAVES:
            value = getattr(self, leaf)
            if value is not None:
                payload[leaf] = value
        for name, value in self.headers.items():
            payload[f"headers.{name}"] = value
        return payload

    def __repr__(self) -> str:
        overridden = sorted(
            [leaf for leaf in _SCALAR_LEAVES if getattr(self, leaf) is not None]
            + [f"headers.{n}" for n in self.headers]
        )
        return f"ForwarderEnvironment(enabled={self.enabled!r}, overrides={overridden!r})"


class Forwarder:
    """A SIEM streaming forwarder configured on the customer's account.

    Active-record style: mutate fields directly and call :meth:`save` to
    persist, or :meth:`delete` to remove. Header values in
    ``configuration.headers`` are returned in plaintext on reads, so
    fetching a forwarder, mutating it, and calling :meth:`save` preserves
    its header values without re-entering secrets.

    Attributes:
        id (str | None): Caller-supplied unique identifier (key) for this
            forwarder. Unique within an account and immutable for the
            lifetime of the forwarder. ``None`` only while the dataclass
            represents an unsaved instance constructed without an id (which
            ``save()`` would then reject).
        name (str): Display name. Free-form.
        forwarder_type (ForwarderType): Destination type — see
            :class:`ForwarderType`.
        enabled (bool): Read-only roll-up: ``True`` when the forwarder is
            enabled in at least one environment. Derived from the
            :attr:`environments` map — there is no server-side top-level
            ``enabled`` field. Enable per environment via
            ``forwarder.environment(env).enabled = True``.
        environments (dict[str, ForwarderEnvironment]): Per-environment sparse
            overrides keyed by environment key (e.g. ``"production"``,
            ``"staging"``). A forwarder delivers in an environment only when
            ``environments[env].enabled`` is ``True``. Each entry overrides
            only the leaves it sets; omitted leaves inherit the base
            :attr:`configuration`. Reach one via :meth:`environment`. Every
            referenced environment must exist and be managed for the account.
        configuration (HttpConfiguration): Base destination request
            configuration.
        description (str | None): Optional free-text description.
        forward_smplkit_events (bool): When ``True``, this forwarder also
            receives platform change events that smplkit records about your
            own resources (flag, configuration, and similar changes). Each
            such event is delivered through every environment this forwarder
            is enabled in, using that environment's resolved configuration.
            Independent of the per-environment :attr:`environments` settings,
            since platform change events are not tied to a deployment
            environment. Defaults to ``False`` — platform change events are
            not forwarded unless you opt in.
        filter (dict[str, Any] | None): Optional JSON Logic expression
            evaluated per event. When set, events that don't match are recorded
            as ``filtered_out`` deliveries instead of being POSTed to the
            destination.
        transform (Any | None): Optional template applied to each event
            before delivery. Shape depends on :attr:`transform_type`; for
            :attr:`TransformType.JSONATA`, a string containing a JSONata
            expression. ``None`` delivers the event JSON as-is.
        transform_type (TransformType | None): Engine used to evaluate
            :attr:`transform`. Must be set whenever :attr:`transform` is set.
        created_at (datetime | None): When the audit service first persisted
            this forwarder. ``None`` for an unsaved instance.
        updated_at (datetime | None): When this forwarder was last mutated.
        deleted_at (datetime | None): Deletion timestamp; ``None`` for live
            forwarders.
        version (int | None): Monotonic version counter; bumped on every
            server-side write.
    """

    def __init__(
        self,
        client: ForwardersClient | None = None,
        *,
        id: str | None = None,
        name: str,
        forwarder_type: ForwarderType,
        configuration: HttpConfiguration,
        environments: dict[str, ForwarderEnvironment] | None = None,
        description: str | None = None,
        forward_smplkit_events: bool = False,
        filter: dict[str, Any] | None = None,
        transform: Any = None,
        transform_type: TransformType | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        deleted_at: datetime | None = None,
        version: int | None = None,
    ) -> None:
        self.id = id
        self.name = name
        self.forwarder_type = forwarder_type
        self.configuration = configuration
        # Per-environment sparse overrides ``{env_key: ForwarderEnvironment}``
        # (ADR-056). Reach one via :meth:`environment` and set its ``enabled``
        # / leaf overrides to make the forwarder deliver (and vary its request)
        # in that environment.
        self.environments: dict[str, ForwarderEnvironment] = environments if environments is not None else {}
        self.description = description
        self.forward_smplkit_events = forward_smplkit_events
        self.filter = filter
        self.transform = transform
        self.transform_type = transform_type
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at
        self.version = version
        self._client = client

    @property
    def enabled(self) -> bool:
        """Read-only roll-up: ``True`` when enabled in at least one environment.

        Derived from the :attr:`environments` map — the forwarder has no
        server-side top-level ``enabled`` field. Enable per environment via
        ``forwarder.environment(env).enabled = True``.
        """
        return any(env.enabled for env in self.environments.values())

    def __repr__(self) -> str:
        enabled_in = sorted(k for k, v in self.environments.items() if v.enabled)
        return f"Forwarder(id={self.id!r}, name={self.name!r}, enabled_in={enabled_in!r})"

    def environment(self, environment: str) -> ForwarderEnvironment:
        """The per-environment override for ``environment`` — the single place
        to read or set what this forwarder overrides there (ADR-056).

        Returns the :class:`ForwarderEnvironment` for ``environment``, creating
        an empty one (and inserting it into :attr:`environments`) on first
        access, so you can set overrides directly::

            forwarder.environment("production").enabled = True
            forwarder.environment("production").url = "https://prod.siem.example.com/in"
            forwarder.environment("production").set_header("DD-API-KEY", "prod-secret")

        Only the leaves you set are sent on save; everything else inherits the
        base definition (the server resolves base ⊕ overrides on delivery).
        """
        env = self.environments.get(environment)
        if env is None:
            env = ForwarderEnvironment()
            self.environments[environment] = env
        return env

    def save(self) -> None:
        """Create or update this forwarder on the server.

        Upsert behavior is driven by :attr:`created_at`: a forwarder with
        no ``created_at`` is created (POST); otherwise it's full-replace
        updated (PUT). After the call, every field is refreshed from the
        server response (including newly-assigned ``id``, ``created_at``,
        ``updated_at``, ``version``).
        """
        if self._client is None:
            raise RuntimeError("Forwarder was constructed without a client; cannot save")
        if self.created_at is None:
            other = self._client._create(self)
        else:
            other = self._client._update(self)
        self._apply(other)

    def delete(self) -> None:
        """Delete this forwarder on the server."""
        if self._client is None or self.id is None:
            raise RuntimeError("Forwarder was constructed without a client or id; cannot delete")
        self._client.delete(self.id)

    def _apply(self, other: Forwarder) -> None:
        """Copy every server-authoritative field from ``other`` onto self."""
        self.id = other.id
        self.name = other.name
        self.forwarder_type = other.forwarder_type
        self.configuration = other.configuration
        self.environments = other.environments
        self.description = other.description
        self.forward_smplkit_events = other.forward_smplkit_events
        self.filter = other.filter
        self.transform = other.transform
        self.transform_type = other.transform_type
        self.created_at = other.created_at
        self.updated_at = other.updated_at
        self.deleted_at = other.deleted_at
        self.version = other.version

    @classmethod
    def _from_resource(cls, resource: dict[str, Any], *, client: ForwardersClient | None = None) -> Forwarder:
        attrs = resource.get("attributes", {})
        tt_raw = attrs.get("transform_type")
        environments = {
            env_key: ForwarderEnvironment._from_dict(env_raw or {})
            for env_key, env_raw in (attrs.get("environments") or {}).items()
        }
        return cls(
            client,
            id=resource["id"],
            name=attrs.get("name") or "",
            # Server-side validation already enforces enum membership;
            # we still pass through ForwarderType() so callers get a
            # typed value (and identity-equality with enum members).
            forwarder_type=ForwarderType(attrs["forwarder_type"]),
            environments=environments,
            description=attrs.get("description"),
            # Absent on the wire (a forwarder persisted before the field
            # landed) reads back as false — the additive default.
            forward_smplkit_events=bool(attrs.get("forward_smplkit_events", False)),
            filter=attrs.get("filter"),
            transform=attrs.get("transform"),
            transform_type=TransformType(tt_raw) if tt_raw is not None else None,
            configuration=HttpConfiguration._from_dict(attrs.get("configuration") or {}),
            created_at=_parse_iso_or_none(attrs.get("created_at")),
            updated_at=_parse_iso_or_none(attrs.get("updated_at")),
            deleted_at=_parse_iso_or_none(attrs.get("deleted_at")),
            version=attrs.get("version"),
        )


class AsyncForwarder(Forwarder):
    """Async active-record forwarder — the async counterpart of :class:`Forwarder`.

    Identical fields and semantics; ``save()`` and ``delete()`` are
    coroutines (``await forwarder.save()``). Returned by the async forwarder
    surface (``AsyncAuditClient.forwarders``).
    """

    async def save(self) -> None:  # type: ignore[override]
        """Create or full-replace this forwarder on the server (async)."""
        if self._client is None:
            raise RuntimeError("Forwarder was constructed without a client; cannot save")
        if self.created_at is None:
            other = await self._client._create(self)
        else:
            other = await self._client._update(self)
        self._apply(other)

    async def delete(self) -> None:  # type: ignore[override]
        """Delete this forwarder on the server (async)."""
        if self._client is None or self.id is None:
            raise RuntimeError("Forwarder was constructed without a client or id; cannot delete")
        await self._client.delete(self.id)


@dataclass(frozen=True, slots=True)
class ResourceType:
    """A distinct resource_type slug seen for the account.

    The ``id`` and ``resource_type`` fields are the same value — JSON:API
    surfaces the customer-facing key as the resource id. The duplication
    keeps SDK consumers from having to dig into the id field when
    filtering UI controls; pick whichever name reads better in context.

    Attributes:
        id (str): The resource-type slug, surfaced as the JSON:API resource id.
        resource_type (str): Same value as :attr:`id`; provided for readability.
        created_at (datetime): Earliest sighting of this resource_type for the
            account.
    """

    id: str
    resource_type: str
    created_at: datetime

    @classmethod
    def _from_resource(cls, resource: dict[str, Any]) -> "ResourceType":
        attrs = resource.get("attributes", {})
        return cls(
            id=resource["id"],
            resource_type=attrs.get("resource_type") or resource["id"],
            created_at=_parse_iso(attrs["created_at"]),
        )


@dataclass(frozen=True, slots=True)
class EventType:
    """A distinct event_type slug seen for the account.

    Same shape as :class:`ResourceType` — ``id`` and ``event_type`` are
    the same value. When the parent list call filtered by
    ``resource_type``, ``created_at`` is the first sighting of that
    specific (event_type, resource_type) triple, not the event_type
    overall.

    Attributes:
        id (str): The event_type slug, surfaced as the JSON:API resource id.
        event_type (str): Same value as :attr:`id`; provided for readability.
        created_at (datetime): Earliest sighting of this event_type (or
            event_type/resource_type pair when the list call was filtered) for
            the account.
    """

    id: str
    event_type: str
    created_at: datetime

    @classmethod
    def _from_resource(cls, resource: dict[str, Any]) -> "EventType":
        attrs = resource.get("attributes", {})
        return cls(
            id=resource["id"],
            event_type=attrs.get("event_type") or resource["id"],
            created_at=_parse_iso(attrs["created_at"]),
        )


@dataclass(frozen=True, slots=True)
class Category:
    """A distinct ``category`` value seen for the account.

    Same shape as :class:`ResourceType` and :class:`EventType` — ``id``
    and ``category`` are the same value, surfaced as the JSON:API
    resource id. The duplication keeps SDK consumers from having to dig
    into the ``id`` field when populating filter UI controls; pick
    whichever name reads better in context.

    Attributes:
        id (str): The category value, surfaced as the JSON:API resource id.
        category (str): Same value as :attr:`id`; provided for readability.
        created_at (datetime): Earliest sighting of this category for the
            account.
    """

    id: str
    category: str
    created_at: datetime

    @classmethod
    def _from_resource(cls, resource: dict[str, Any]) -> "Category":
        attrs = resource.get("attributes", {})
        return cls(
            id=resource["id"],
            category=attrs.get("category") or resource["id"],
            created_at=_parse_iso(attrs["created_at"]),
        )


def _parse_iso(value: str) -> datetime:
    # Python's fromisoformat accepts an optional trailing 'Z' (treated as UTC)
    # in 3.11+. The audit service emits +00:00 anyway, but customers may pass
    # ``Z`` from JS-flavored timestamps.
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _parse_iso_or_none(value: str | None) -> datetime | None:
    if value is None:
        return None
    return _parse_iso(value)
