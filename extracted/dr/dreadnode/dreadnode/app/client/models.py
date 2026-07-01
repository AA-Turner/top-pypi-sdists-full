import typing as t
from dataclasses import dataclass, field


@dataclass(slots=True)
class CapabilityAgentInfo:
    """Agent metadata returned by the runtime API."""

    name: str
    description: str
    model: str
    capability: str

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "CapabilityAgentInfo":
        return cls(
            name=str(data.get("name", "")),
            description=str(data.get("description", "")),
            model=str(data.get("model", "inherit")),
            capability=str(data.get("capability", "")),
        )


@dataclass(slots=True)
class CapabilityInfo:
    """Capability metadata returned by the runtime API."""

    name: str
    display_name: str
    canonical_name: str | None = None
    local_path: str | None = None
    entry_agent: str | None = None
    skills_paths: list[str] = field(default_factory=list)
    agents: list[CapabilityAgentInfo] = field(default_factory=list)
    source: str | None = None
    provenance: str | None = None
    version: str | None = None
    description: str | None = None
    author: dict[str, t.Any] | None = None
    license: str | None = None
    origin: dict[str, t.Any] | None = None
    enabled: bool = True
    binding_id: str | None = None
    components: list[dict[str, t.Any]] = field(default_factory=list)
    update_available: str | None = None
    dependencies: dict[str, t.Any] | None = None
    checks: list[dict[str, t.Any]] | None = None
    flags: list[dict[str, t.Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "CapabilityInfo":
        return cls(
            name=str(data.get("name", "")),
            display_name=str(data.get("display_name") or data.get("name", "")),
            canonical_name=(
                str(data["canonical_name"]) if data.get("canonical_name") is not None else None
            ),
            local_path=(str(data["local_path"]) if data.get("local_path") is not None else None),
            entry_agent=str(data["entry_agent"]) if data.get("entry_agent") else None,
            skills_paths=[str(path) for path in data.get("skills_paths", [])],
            agents=[
                CapabilityAgentInfo.from_dict(item)
                for item in data.get("agents", [])
                if isinstance(item, dict)
            ],
            source=data.get("source"),
            provenance=(str(data["provenance"]) if data.get("provenance") is not None else None),
            version=data.get("version"),
            description=str(data["description"]) if data.get("description") is not None else None,
            author=data.get("author") if isinstance(data.get("author"), dict) else None,
            license=str(data["license"]) if data.get("license") is not None else None,
            origin=data.get("origin") if isinstance(data.get("origin"), dict) else None,
            enabled=data.get("enabled", True),
            binding_id=data.get("binding_id"),
            components=data.get("components", []),
            update_available=data.get("update_available"),
            dependencies=data.get("dependencies"),
            checks=data.get("checks"),
            flags=[item for item in data.get("flags", []) if isinstance(item, dict)],
        )


@dataclass(slots=True)
class SkillInfo:
    """Skill metadata from the server.

    ``qualified_id`` is the user-facing identifier projected through the
    skill ``:`` separator (see CAP-IDENT-009). ``source`` is the skill
    origin and ``capability`` is the owning capability, if any.
    """

    name: str
    description: str
    qualified_id: str | None = None
    source: str | None = None
    capability: str | None = None

    @staticmethod
    def from_dict(data: dict[str, t.Any]) -> "SkillInfo":
        qualified = data.get("qualified_id")
        source = data.get("source")
        capability = data.get("capability")
        return SkillInfo(
            name=str(data["name"]),
            description=str(data.get("description", "")),
            qualified_id=str(qualified) if qualified else None,
            source=str(source) if source else None,
            capability=str(capability) if capability else None,
        )


@dataclass(slots=True)
class ToolInfo:
    """Tool metadata from the runtime ``/api/tools`` endpoint.

    ``capability`` is the source group the runtime reports: ``built-in``
    for the default toolset, ``mcp`` for MCP-server tools, ``session``
    for session-scoped helpers like ``load_skill``/``spawn_agent``, or
    a loaded capability name for capability-provided tools.

    ``parameters_schema`` is the tool's JSON Schema (if available) —
    used by :mod:`dreadnode.app.tui.tool_format` to derive the key
    argument for a compact label.
    """

    name: str
    wire_name: str | None = None
    source: str | None = None
    server: str | None = None
    description: str = ""
    capability: str = ""
    parameters_schema: dict[str, t.Any] | None = None

    @staticmethod
    def from_dict(data: dict[str, t.Any]) -> "ToolInfo":
        schema = data.get("parameters_schema")
        wire = data.get("wire_name")
        source = data.get("source")
        server = data.get("server")
        return ToolInfo(
            name=str(data.get("name", "")),
            wire_name=str(wire) if wire is not None else None,
            source=str(source) if source is not None else None,
            server=str(server) if server is not None else None,
            description=str(data.get("description", "") or ""),
            capability=str(data.get("capability", "") or ""),
            parameters_schema=schema if isinstance(schema, dict) else None,
        )


@dataclass(slots=True)
class RuntimeInfo:
    """Summary of the connected server runtime."""

    status: str
    version: str
    runtime_id: str | None = None
    host_type: str = "local"
    working_dir: str = ""
    default_capability: str | None = None
    capabilities: list[CapabilityInfo] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "RuntimeInfo":
        return cls(
            status=str(data.get("status", "unknown")),
            version=str(data.get("version", "unknown")),
            runtime_id=(str(data["runtime_id"]) if data.get("runtime_id") else None),
            host_type=str(data.get("host_type", "local")),
            working_dir=str(data.get("working_dir", "")),
            default_capability=(
                str(data["default_capability"]) if data.get("default_capability") else None
            ),
            capabilities=[
                CapabilityInfo.from_dict(item)
                for item in data.get("capabilities", [])
                if isinstance(item, dict)
            ],
        )


@dataclass(slots=True)
class SessionCreator:
    """Denormalized session-owner view (matches platform `created_by` block).

    Populated for platform-sourced sessions; left as ``None`` on rows that
    only ever exist in the runtime's in-process set. The platform omits the
    block entirely when the user row was hard-deleted.
    """

    id: str
    email: str | None = None
    username: str | None = None
    full_name: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "SessionCreator":
        return cls(
            id=str(data.get("id", "")),
            email=str(data["email"]) if data.get("email") else None,
            username=str(data["username"]) if data.get("username") else None,
            full_name=str(data["full_name"]) if data.get("full_name") else None,
        )


@dataclass(slots=True)
class SessionInfo:
    """Server-side session metadata."""

    session_id: str
    project: str | None
    created_at: str
    updated_at: str | None = None
    message_count: int = 0
    session_dir: str | None = None
    capability: str | None = None
    agent: str | None = None
    title: str | None = None
    preview: str | None = None
    policy_name: str = "interactive"
    policy_is_autonomous: bool = False
    policy_display_label: str = ""
    # Platform-sourced fields. Defaulted so in-process rows constructed
    # from a SessionRuntime (which doesn't know these) still validate.
    visibility: str = "private"
    origin: str = "user"
    archived_at: str | None = None
    frozen_at: str | None = None
    frozen_by: str | None = None
    labels: dict[str, list[str]] = field(default_factory=dict)
    created_by: SessionCreator | None = None
    user_id: str | None = None
    # Cumulative usage roll-ups computed at the source (runtime trajectory or
    # platform aggregation). ``total_cost_usd`` is ``None`` when at least one
    # generation in scope had no cost rate available — partial sums sold as
    # totals would diverge from the platform's null-propagating contract.
    total_tokens: int = 0
    total_tool_call_count: int = 0
    total_cost_usd: float | None = None
    # ``input_tokens`` from the most recent generation — "context the model
    # last saw", used by the TUI's context-window gauge. Mirrors the
    # platform's ``SessionUsageResponse.last_generation_input_tokens``.
    last_generation_input_tokens: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "SessionInfo":
        created_by_raw = data.get("created_by")
        created_by = (
            SessionCreator.from_dict(created_by_raw) if isinstance(created_by_raw, dict) else None
        )
        labels_raw = data.get("labels") or {}
        labels: dict[str, list[str]] = {}
        if isinstance(labels_raw, dict):
            for key, values in labels_raw.items():
                if isinstance(values, list):
                    labels[str(key)] = [str(v) for v in values]
        return cls(
            session_id=str(data.get("session_id", "")),
            project=str(data["project"]) if data.get("project") else None,
            created_at=str(data.get("created_at", "")),
            updated_at=str(data["updated_at"]) if data.get("updated_at") else None,
            message_count=int(data.get("message_count", 0)),
            session_dir=str(data["session_dir"]) if data.get("session_dir") else None,
            capability=str(data["capability"]) if data.get("capability") else None,
            agent=str(data["agent"]) if data.get("agent") else None,
            title=str(data["title"]) if data.get("title") else None,
            preview=str(data["preview"]) if data.get("preview") else None,
            policy_name=str(data.get("policy_name", "interactive")),
            policy_is_autonomous=bool(data.get("policy_is_autonomous", False)),
            policy_display_label=str(data.get("policy_display_label", "") or ""),
            visibility=str(data.get("visibility", "private")),
            origin=str(data.get("origin", "user")),
            archived_at=str(data["archived_at"]) if data.get("archived_at") else None,
            frozen_at=str(data["frozen_at"]) if data.get("frozen_at") else None,
            frozen_by=str(data["frozen_by"]) if data.get("frozen_by") else None,
            labels=labels,
            created_by=created_by,
            user_id=str(data["user_id"]) if data.get("user_id") else None,
            total_tokens=int(data.get("total_tokens", 0)),
            total_tool_call_count=int(data.get("total_tool_call_count", 0)),
            total_cost_usd=(
                float(data["total_cost_usd"]) if data.get("total_cost_usd") is not None else None
            ),
            last_generation_input_tokens=(
                int(data["last_generation_input_tokens"])
                if data.get("last_generation_input_tokens") is not None
                else None
            ),
        )


@dataclass(slots=True)
class SessionListResult:
    """Paginated session list returned by the platform-browse path.

    Mirrors the platform's `SessionListResponse` envelope so consumers don't
    need to know whether the data came directly from the platform or via
    the runtime pass-through.
    """

    sessions: list[SessionInfo]
    total: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "SessionListResult":
        items_raw = data.get("sessions") or []
        items: list[SessionInfo] = []
        if isinstance(items_raw, list):
            items = [SessionInfo.from_dict(item) for item in items_raw if isinstance(item, dict)]
        return cls(
            sessions=items,
            total=int(data.get("total", len(items))),
            page=int(data.get("page", 1)),
            limit=int(data.get("limit", len(items))),
            total_pages=int(data.get("total_pages", 1)),
            has_next=bool(data.get("has_next", False)),
            has_previous=bool(data.get("has_previous", False)),
        )


@dataclass(slots=True)
class LabelFacetEntry:
    """One (value, count) pair inside a label facet group."""

    value: str
    count: int

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "LabelFacetEntry":
        return cls(value=str(data.get("value", "")), count=int(data.get("count", 0)))


@dataclass(slots=True)
class SessionFacets:
    """Per-key value counts for sessions matching the caller's filter.

    Mirrors the platform's ``SessionFacetsResponse`` envelope. Keys with
    zero matching sessions are omitted by the platform (SES-LBL-061).
    """

    labels: dict[str, list[LabelFacetEntry]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "SessionFacets":
        labels_raw = data.get("labels") or {}
        labels: dict[str, list[LabelFacetEntry]] = {}
        if isinstance(labels_raw, dict):
            for key, entries in labels_raw.items():
                if not isinstance(entries, list):
                    continue
                labels[str(key)] = [
                    LabelFacetEntry.from_dict(entry) for entry in entries if isinstance(entry, dict)
                ]
        return cls(labels=labels)
