"""The ``report_item`` tool — emit a structured *item* during a run.

ONE tool, not one-per-type: ``item_type`` is a parameter, so built-in types
(``finding``, ``asset``) and capability-defined types all flow through the same
tool. This scales to user-defined types without adding a tool each.

Transport is **direct POST + span backup** (the chosen design): every emit
(1) logs the item to the current OTEL span via ``log_output`` — durable, always
works, reconciled platform-side — and (2) best-effort POSTs to the platform for
immediate UI visibility. POST failure → debug log; the span backup is the net.

Validation: built-ins and legacy declarations validate against local Pydantic
models. Identifier-only specialized types use the capability's exact platform
registry contract for both the tool schema and local validation.
"""

import json
import typing as t
from uuid import UUID, uuid4

from loguru import logger
from pydantic import BaseModel, Field, ValidationError

from dreadnode.agents.tools import Toolset, tool, tool_method
from dreadnode.items.models import (
    ASSET_TYPE,
    FINDING_TYPE,
    Asset,
    Finding,
    ItemSeverity,
)

# Registry of built-in type → local validation model.
BUILTIN_ITEM_SCHEMAS: dict[str, type[BaseModel]] = {
    FINDING_TYPE: Finding,
    ASSET_TYPE: Asset,
}


class ItemTypeRegistryUnavailableError(RuntimeError):
    """A platform-defined output cannot be typed without its pinned contract."""


def _trace_context() -> tuple[str | None, str | None, str | None]:
    """Best-effort (session_id, trace_id, span_id) from the current run context."""
    from dreadnode.tracing.span import current_session_id, current_task_span

    session_id = current_session_id.get()
    span = current_task_span.get()
    trace_id = span.trace_id if span is not None else None
    span_id = span.span_id if span is not None else None
    return session_id, trace_id, span_id


def _capability_context() -> tuple[str | None, str | None]:
    """The (capability_name, version) the current agent runs under, if any."""
    from dreadnode.tracing.span import current_capability

    cap = current_capability.get()
    if cap is None:
        return None, None
    name, version = cap
    return (name or None), (version or None)


def _resolve_identity() -> tuple[str, str, str] | None:
    """Resolve (org, workspace, project) from the configured profile, or None.

    Returns None in local mode / when unconfigured — callers fall back to the
    span backup alone.
    """
    from dreadnode import _get_default_instance

    instance = _get_default_instance()
    if instance._api is None or instance._profile is None:
        return None
    profile = instance._profile
    project = profile.project_key or profile.project_id
    if project is None:
        return None
    return profile.org_key, profile.workspace_key, project


class ItemReads(Toolset):
    """Compact, project-scoped reads over the durable Agent Output corpus."""

    project_key: str = Field(..., min_length=1, description="Active project key.")

    @tool_method(name="read_item")
    def read_item(
        self,
        item: t.Annotated[
            str,
            "The exact item ref assigned by an agent, or the item's UUID.",
        ],
        *,
        include_links: t.Annotated[
            bool,
            "Include readable incoming and outgoing item links.",
        ] = True,
    ) -> dict[str, t.Any]:
        """Read one complete structured item and its graph neighborhood."""
        try:
            api, org, workspace, project = self._resolve_context()
            payload = api.get_item(org, workspace, project, item)
            links: list[dict[str, t.Any]] = []
            if include_links:
                item_id = self._require_item_id(payload)
                links_payload = api.get_item_links(
                    org,
                    workspace,
                    project,
                    item_id,
                )
                raw_links = (
                    links_payload.get("links", []) if isinstance(links_payload, dict) else []
                )
                if isinstance(raw_links, list):
                    links = [link for link in raw_links if isinstance(link, dict)]
        except Exception as exc:
            return self._error_response("read_item", exc)
        return {
            "ok": True,
            "operation": "read_item",
            "project": project,
            "item": payload,
            "links": links,
            "error": None,
        }

    @staticmethod
    def _require_item_id(payload: t.Any) -> str:
        item_id = payload.get("id") if isinstance(payload, dict) else None
        if not isinstance(item_id, str) or not item_id:
            raise ValueError("Item response did not include an id")
        return item_id

    @tool_method(name="list_items")
    def list_items(
        self,
        *,
        item_type: t.Annotated[str | None, "Exact item type filter."] = None,
        severity: t.Annotated[
            list[str] | None,
            "Severity values to include (OR semantics).",
        ] = None,
        status: t.Annotated[
            list[str] | None,
            "Effective status values to include (OR semantics).",
        ] = None,
        min_severity: t.Annotated[
            str | None,
            "Minimum severity threshold, such as high.",
        ] = None,
        category: t.Annotated[str | None, "Exact category filter."] = None,
        capability: t.Annotated[
            list[str] | None,
            "Producing capability names to include.",
        ] = None,
        source: t.Annotated[
            list[str] | None,
            "Provenance values to include: api, runtime, or extracted.",
        ] = None,
        session_id: t.Annotated[str | None, "Exact originating session UUID."] = None,
        sort: t.Annotated[
            t.Literal["created_at", "severity", "status"],
            "Sort field.",
        ] = "created_at",
        order: t.Annotated[t.Literal["asc", "desc"], "Sort direction."] = "desc",
        page: t.Annotated[int, "Page number, starting at 1."] = 1,
        limit: t.Annotated[int, "Maximum summaries to return (1-200)."] = 50,
        include_facets: t.Annotated[
            bool,
            "Include filter-aware value counts in the response.",
        ] = False,
    ) -> dict[str, t.Any]:
        """List compact item summaries for iterative traversal."""
        return self._list(
            operation="list_items",
            query=None,
            item_type=item_type,
            severity=severity,
            status=status,
            min_severity=min_severity,
            category=category,
            capability=capability,
            source=source,
            session_id=session_id,
            sort=sort,
            order=order,
            page=page,
            limit=limit,
            include_facets=include_facets,
        )

    @tool_method(name="search_items")
    def search_items(
        self,
        query: t.Annotated[
            str,
            "Non-empty full-text query over item metadata and structured payloads.",
        ],
        *,
        item_type: t.Annotated[str | None, "Exact item type filter."] = None,
        severity: t.Annotated[list[str] | None, "Severity values to include."] = None,
        status: t.Annotated[list[str] | None, "Effective status values to include."] = None,
        min_severity: t.Annotated[str | None, "Minimum severity threshold."] = None,
        category: t.Annotated[str | None, "Exact category filter."] = None,
        capability: t.Annotated[
            list[str] | None,
            "Producing capability names to include.",
        ] = None,
        source: t.Annotated[list[str] | None, "Provenance values to include."] = None,
        session_id: t.Annotated[str | None, "Exact originating session UUID."] = None,
        sort: t.Annotated[
            t.Literal["created_at", "severity", "status", "relevance"],
            "Sort field.",
        ] = "relevance",
        order: t.Annotated[t.Literal["asc", "desc"], "Sort direction."] = "desc",
        page: t.Annotated[int, "Page number, starting at 1."] = 1,
        limit: t.Annotated[int, "Maximum summaries to return (1-200)."] = 50,
        include_facets: t.Annotated[
            bool,
            "Include filter-aware value counts in the response.",
        ] = False,
    ) -> dict[str, t.Any]:
        """Search items and return compact summaries with bounded match previews."""
        if not query.strip():
            return self._error_response("search_items", ValueError("query must not be empty"))
        return self._list(
            operation="search_items",
            query=query,
            item_type=item_type,
            severity=severity,
            status=status,
            min_severity=min_severity,
            category=category,
            capability=capability,
            source=source,
            session_id=session_id,
            sort=sort,
            order=order,
            page=page,
            limit=limit,
            include_facets=include_facets,
        )

    def _list(
        self,
        *,
        operation: str,
        query: str | None,
        item_type: str | None,
        severity: list[str] | None,
        status: list[str] | None,
        min_severity: str | None,
        category: str | None,
        capability: list[str] | None,
        source: list[str] | None,
        session_id: str | None,
        sort: str,
        order: str,
        page: int,
        limit: int,
        include_facets: bool,
    ) -> dict[str, t.Any]:
        try:
            api, org, workspace, project = self._resolve_context()
            payload = api.list_items(
                org,
                workspace,
                project,
                item_type=item_type,
                severity=severity,
                status=status,
                min_severity=min_severity,
                category=category,
                capability=capability,
                source=source,
                session_id=session_id,
                q=query,
                sort=sort,
                order=order,
                page=page,
                limit=limit,
            )
            raw_items = payload.get("items", []) if isinstance(payload, dict) else []
            if not isinstance(raw_items, list):
                raw_items = []
            summaries = [
                self._compact_item(item, query=query)
                for item in raw_items
                if isinstance(item, dict)
            ]
            facets = None
            if include_facets:
                facets = api.get_item_facets(
                    org,
                    workspace,
                    project,
                    item_type=item_type,
                    severity=severity,
                    status=status,
                    min_severity=min_severity,
                    category=category,
                    capability=capability,
                    source=source,
                    session_id=session_id,
                    q=query,
                )
        except Exception as exc:
            return self._error_response(operation, exc)

        current_page = int(payload.get("page", page))
        has_next = bool(payload.get("has_next", False))
        return {
            "ok": True,
            "operation": operation,
            "project": project,
            "items": summaries,
            "total": int(payload.get("total", len(summaries))),
            "page": current_page,
            "limit": int(payload.get("limit", limit)),
            "total_pages": int(payload.get("total_pages", 0)),
            "has_next": has_next,
            "next_page": current_page + 1 if has_next else None,
            "facets": facets,
            "error": None,
        }

    @staticmethod
    def _compact_item(item: dict[str, t.Any], *, query: str | None) -> dict[str, t.Any]:
        data = item.get("data")
        if not isinstance(data, dict):
            data = {}
        disposition = item.get("disposition")
        if not isinstance(disposition, dict):
            disposition = {}
        summary = {
            "id": item.get("id"),
            "ref": item.get("ref"),
            "item_type": item.get("item_type"),
            "title": item.get("title"),
            "severity": data.get("severity"),
            "category": data.get("category"),
            "effective_status": item.get("effective_status") or disposition.get("status"),
            "capability": item.get("capability"),
            "source": item.get("source"),
            "session_id": item.get("session_id"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
            "data_keys": sorted(str(key) for key in data)[:20],
        }
        if query is not None:
            payload_text = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
            start = payload_text.casefold().find(query.casefold())
            if start >= 0:
                left = max(0, start - 120)
                right = min(len(payload_text), start + len(query) + 120)
                summary["match_preview"] = payload_text[left:right]
        return summary

    def _resolve_context(self) -> tuple[t.Any, str, str, str]:
        from dreadnode import _get_default_instance

        instance = _get_default_instance()
        if not instance.can_sync:
            raise RuntimeError("Platform sync is disabled for this runtime session")
        profile = instance.profile
        return instance.api, profile.org_key, profile.workspace_key, self.project_key

    @staticmethod
    def _error_response(operation: str, exc: Exception) -> dict[str, t.Any]:
        return {
            "ok": False,
            "operation": operation,
            "items": [],
            "error": str(exc),
        }


def _is_payload_rejection(error: str | None) -> bool:
    """True only for a clear client request rejection (HTTP 400/404/422) — the agent
    must fix its data and retry.

    The platform's error strings are prefixed with the status code. Transport,
    auth, 5xx, conflict, and quota failures are transient or benign: the span
    backup + reconcile heal them, so the tool must NOT hard-fail on those — that
    would defeat the "direct POST + durable span backup" design.
    """
    if not error:
        return False
    code = error.split(":", 1)[0].strip()
    return code in ("400", "422") or (code == "404" and "Target " in error)


ReportItemOutcome = t.Literal["persisted", "trace_only", "rejected"]


def classify_report_item_outcome(
    *,
    item_id: str | None = None,
    post_error: str | None = None,
    result: str | None = None,
    error: str | None = None,
) -> ReportItemOutcome:
    """Classify a report_item emit or its string result without new metadata."""
    if error or _is_payload_rejection(post_error):
        return "rejected"
    if item_id:
        return "persisted"
    if result:
        details = result.rpartition("(")[2].removesuffix(")")
        if any(part.strip().startswith("id: ") for part in details.split(",")):
            return "persisted"
    return "trace_only"


def _report_item_result(
    *,
    item_type: str,
    title: str | None,
    ref: str | None,
    item_id: str | None,
    post_error: str | None,
) -> str:
    outcome = classify_report_item_outcome(item_id=item_id, post_error=post_error)
    if outcome == "rejected":
        raise ValueError(f"Item was not saved to the platform: {post_error}")
    if post_error is not None:
        return (
            f"Reported {item_type} '{title or '(untitled)'}' (recorded to "
            "trace; platform write deferred — will reconcile)"
        )
    if outcome == "trace_only":
        ref_text = f"ref: {ref}; " if ref else ""
        return (
            f"Reported {item_type} '{title or '(untitled)'}' ({ref_text}recorded to trace; "
            "id unavailable — platform write unconfirmed)"
        )
    handle = f"ref: {ref}, id: {item_id}" if ref else f"id: {item_id}"
    return f"Reported {item_type} '{title or '(untitled)'}' ({handle})"


def _check_registry_binding(item_type: str) -> None:
    """Discover the online contract; local model validation remains the fallback."""
    identity = _resolve_identity()
    if identity is None:
        return

    from dreadnode import _get_default_instance
    from dreadnode.app.api.client import NotFoundError

    org, _, _ = identity
    try:
        detail = _get_default_instance().api.get_organization_item_type(org, item_type)
    except NotFoundError:
        logger.warning(
            "Item type '{}' is missing or inactive in the platform registry; "
            "continuing with durable local validation",
            item_type,
        )
        return
    except Exception as exc:
        logger.warning(
            "Registry lookup for item_type '{}' failed ({}); using local model validation",
            item_type,
            exc,
        )
        return

    capability, capability_version = _capability_context()
    if capability is None and capability_version is None:
        return
    usage = detail.get("capability_usage")
    if not isinstance(usage, list) or not any(
        isinstance(entry, dict)
        and _matches_capability_name(entry.get("capability_name"), capability)
        and entry.get("capability_version") == capability_version
        for entry in usage
    ):
        logger.warning(
            "Item type '{}' is not bound to capability '{}' version '{}'; "
            "continuing with durable local validation",
            item_type,
            capability,
            capability_version,
        )


def _format_item_handle(item_id: str | None, ref: str | None) -> str:
    handles = [
        handle
        for handle in (f"id: {item_id}" if item_id else None, f"ref: {ref}" if ref else None)
        if handle is not None
    ]
    return ", ".join(handles) or "id unavailable"


def _emit_item(
    *,
    item_type: str,
    payload: dict[str, t.Any],
    title: str | None,
    status: str | None,
    notes: str | None,
    schema_ref: str | None,
    ref: str | None = None,
    links: list[dict[str, t.Any]] | None = None,
) -> tuple[str | None, str | None]:
    """Shared emit path: span backup (always) + best-effort direct POST.

    Returns ``(item_id, post_error)`` — the created id when the direct POST
    succeeds (so the agent can edit/link it later), and any POST error string so
    callers can surface a validation failure instead of silently swallowing it.
    """
    from dreadnode import log_output

    session_id, trace_id, span_id = _trace_context()
    capability, capability_version = _capability_context()

    # One idempotency key per emit, shared by BOTH paths so the direct POST and a
    # later span-extraction reconcile to a single row (never double-counted).
    dedupe_key = uuid4().hex

    # (1) Durable span backup. The output VALUE is a self-contained envelope so
    # platform-side extraction can rebuild the row without depending on log
    # attributes surviving. Attributes are duplicated for human filtering only.
    # severity is NOT a top-level field — it rides inside ``data``. status/notes
    # populate the platform-side disposition overlay; links ride along so a failed
    # direct POST still materializes the edges from the span backup (P1).
    envelope = {
        "item_type": item_type,
        "dedupe_key": dedupe_key,
        "ref": ref,
        "title": title,
        "status": status,
        "notes": notes,
        "schema_ref": schema_ref,
        "session_id": session_id,
        "trace_id": trace_id,
        "span_id": span_id,
        "capability": capability,
        "capability_version": capability_version,
        "data": payload,
        "links": links,
    }
    log_output(
        "item",
        envelope,
        label=title or item_type,
        attributes={
            "item_type": item_type,
            "severity": str(payload.get("severity") or ""),
            "status": status or "",
            "dedupe_key": dedupe_key,
        },
    )

    # session_id is a UUID string for platform sessions; only forward it as the
    # FK when it actually parses, otherwise the raw value rides along in data.
    session_uuid: str | None = None
    if session_id is not None:
        try:
            session_uuid = str(UUID(session_id))
        except (ValueError, TypeError):
            meta = payload.setdefault("metadata", {})
            if isinstance(meta, dict):
                meta["session_ref"] = session_id

    # (2) Best-effort direct POST for immediate UI visibility. Returns the
    # created id and any POST error (so callers can surface validation failures
    # to the agent instead of silently relying on the span backup).
    item_id: str | None = None
    post_error: str | None = None
    identity = _resolve_identity()
    if identity is not None:
        from dreadnode import _get_default_instance

        org, workspace, project = identity
        try:
            created = _get_default_instance().api.create_item(
                org,
                workspace,
                project,
                item_type=item_type,
                data=payload,
                ref=ref,
                title=title,
                status=status,
                notes=notes,
                session_id=session_uuid,
                trace_id=trace_id,
                span_id=span_id,
                capability=capability,
                capability_version=capability_version,
                schema_ref=schema_ref,
                source="runtime",
                dedupe_key=dedupe_key,
                links=links,
            )
            cid = created.get("id")
            item_id = str(cid) if cid is not None else None
        except Exception as exc:
            post_error = str(exc)
            logger.debug("report_item direct POST failed ({}); relying on span backup", exc)

    return item_id, post_error


def _validate_payload(
    item_type: str, data: dict[str, t.Any]
) -> tuple[dict[str, t.Any], str | None, str | None, str | None]:
    """Return (clean_data, title, severity, schema_ref) for an item.

    Built-in types validate against their model (and drop unknown keys);
    unknown/capability types pass through (validated platform-side in Phase 4).
    """
    schema = BUILTIN_ITEM_SCHEMAS.get(item_type)
    if schema is None:
        raise ValueError(
            f"Unknown item_type '{item_type}': custom types require a capability-defined model."
        )

    try:
        validated = schema.model_validate(data)
    except ValidationError as exc:
        # Surfaced to the agent as a tool error so it can correct and retry.
        raise ValueError(f"Invalid payload for item_type '{item_type}': {exc.errors()}") from exc

    return (
        validated.model_dump(mode="json"),
        getattr(validated, "title", None),
        getattr(validated, "severity", None),
        f"{item_type}@1",
    )


@tool(name="report_item")
def report_item(
    item_type: t.Annotated[
        str,
        (
            "The kind of structured output to report. Use 'finding' for a "
            "triageable observation or issue; use 'asset' for a host, service, "
            "file, account, endpoint, artifact, or other thing you observed or "
            "produced; use a capability-defined type when the capability "
            "declares one in produces."
        ),
    ],
    data: t.Annotated[
        dict[str, t.Any],
        (
            "The JSON payload for the chosen item_type. Include the required "
            "fields for that type; for custom types, follow the Pydantic model "
            "and field descriptions exposed in this tool schema."
        ),
    ],
    *,
    ref: t.Annotated[
        str | None,
        (
            "Optional short name you assign this item (e.g. 'web-1', 'finding-3'), "
            "unique within the project. Use it later to link or update this item "
            "without tracking its server id — preferred over passing raw ids."
        ),
    ] = None,
    title: t.Annotated[
        str | None,
        "Optional explicit title for listing/filtering (defaults to data.title).",
    ] = None,
    severity: t.Annotated[
        ItemSeverity | None,
        "Optional explicit severity for filtering (defaults to data.severity).",
    ] = None,
    links: t.Annotated[
        list[dict[str, str]] | None,
        (
            "Optional links to existing items, created with this one. Each entry is "
            "{'target_ref': <a ref you assigned earlier>, 'relationship': <label e.g. "
            "'affects'>}. You may use 'target_id' instead of 'target_ref'. E.g. report "
            "a finding linked to its asset's ref."
        ),
    ] = None,
) -> str:
    """Report a structured item back to the platform for the current run.

    Items are surfaced in the project UI, filterable by type and severity, and
    traceable to this session/span. Emit one call per distinct finding, asset, or
    capability-defined record. Do not use this for narrative summaries.

    Assign a ``ref`` so you can link/update this item later by name. Returns the
    item's ref and id.
    """
    clean_data, derived_title, _, schema_ref = _validate_payload(item_type, data)
    # An explicit severity override lands in ``data`` (severity is a data field,
    # not a promoted/disposition field).
    if severity is not None:
        clean_data = {**clean_data, "severity": severity}
    _check_registry_binding(item_type)
    api_links: list[dict[str, t.Any]] = []
    for link in links or []:
        if not link.get("relationship"):
            continue
        if link.get("target_ref"):
            api_links.append(
                {"target_ref": link["target_ref"], "relationship": link["relationship"]}
            )
        elif link.get("target_id"):
            api_links.append(
                {"target_item_id": link["target_id"], "relationship": link["relationship"]}
            )
    final_title = title or derived_title
    item_id, post_error = _emit_item(
        item_type=item_type,
        payload=clean_data,
        title=final_title,
        # A freshly reported item is untriaged — no disposition until someone
        # triages it. status/notes are set later via update_item.
        status=None,
        notes=None,
        schema_ref=schema_ref,
        ref=ref,
        links=api_links or None,
    )
    return _report_item_result(
        item_type=item_type,
        title=final_title,
        ref=ref,
        item_id=item_id,
        post_error=post_error,
    )


def _resolve_handle(api: t.Any, org: str, workspace: str, project: str, handle: str) -> str | None:
    """Resolve an item handle (a ref or a UUID id) to a concrete item id."""
    try:
        UUID(handle)
    except (ValueError, TypeError):
        return api.resolve_item_ref(org, workspace, project, handle)
    else:
        return handle  # already an id


@tool(name="update_item")
def update_item(
    item: t.Annotated[str, "The item to edit — the ref you assigned, or its id, from report_item."],
    *,
    data: t.Annotated[
        dict[str, t.Any] | None,
        "Replacement payload (re-validated against the item's type). Omit to keep.",
    ] = None,
    title: t.Annotated[str | None, "New title."] = None,
    severity: t.Annotated[
        ItemSeverity | None,
        "New severity (for findings). Folded into the item's data payload.",
    ] = None,
    status: t.Annotated[
        t.Literal["open", "triaged", "verified", "resolved", "dismissed"] | None,
        "New status: 'verified' (confirmed real), 'dismissed' (false positive), "
        "'triaged' (reviewed), 'resolved' (fixed). Recorded in the disposition overlay.",
    ] = None,
    notes: t.Annotated[
        str | None,
        "Free-form notes to record on the item — e.g. WHY you dismissed or "
        "verified a finding (the evidence and reasoning behind the status). "
        "Recorded in the disposition overlay alongside status. Notes alone do "
        "not change the status.",
    ] = None,
    clear_status: t.Annotated[
        bool,
        "Set true to remove a previously-set status, returning the finding to "
        "the untriaged 'needs review' queue (undoes a prior triage decision). "
        "Cannot be combined with status.",
    ] = False,
) -> str:
    """Edit an item you previously reported (correct data, change severity/status).

    ``status``/``notes`` update the triage overlay; ``clear_status`` un-triages.
    Only provided fields change. Address the item by its ref or id.
    """
    if clear_status and status is not None:
        # Surfaced to the agent as a tool error so it can correct and retry.
        raise ValueError("Pass either status or clear_status, not both.")
    identity = _resolve_identity()
    if identity is None:
        return "Cannot update item: no platform connection configured for this run."
    org, workspace, project = identity
    from dreadnode import _get_default_instance

    api = _get_default_instance().api
    item_id = _resolve_handle(api, org, workspace, project, item)
    if item_id is None:
        return f"Cannot update item: no item found for '{item}'."
    # severity lives in ``data`` now — fold an explicit override into the data
    # replace (re-validated server-side against the item's type).
    if severity is not None:
        data = {**(data or {}), "severity": severity}
    api.update_item(
        org,
        workspace,
        project,
        item_id,
        data=data,
        title=title,
        status=status,
        notes=notes,
        clear_status=clear_status,
    )
    return f"Updated item {item}"


@tool(name="link_items")
def link_items(
    source: t.Annotated[str, "The item the link starts from — its ref or id."],
    target: t.Annotated[str, "The item to link to — its ref or id."],
    relationship: t.Annotated[str, "Relationship label, e.g. 'affects', 'evidence_of', 'related'."],
) -> str:
    """Create a directed link between two existing items (same project).

    E.g. link a finding to the asset it affects. Address items by ref or id.
    """
    identity = _resolve_identity()
    if identity is None:
        return "Cannot link items: no platform connection configured for this run."
    org, workspace, project = identity
    from dreadnode import _get_default_instance

    api = _get_default_instance().api
    source_id = _resolve_handle(api, org, workspace, project, source)
    if source_id is None:
        return f"Cannot link: no item found for source '{source}'."
    # Target can stay a ref — the platform resolves it; only the source needs an id
    # for the URL path.
    try:
        UUID(target)
        api.create_item_link(
            org,
            workspace,
            project,
            source_id,
            target_item_id=target,
            relationship=relationship,
        )
    except (ValueError, TypeError):
        api.create_item_link(
            org,
            workspace,
            project,
            source_id,
            target_ref=target,
            relationship=relationship,
        )
    return f"Linked {source} -[{relationship}]-> {target}"


# ===========================================================================
# Dynamic, capability-aware report_item
#
# When a capability declares item production through `produces`, we generate a
# report_item whose argument schema reflects those types (plus selected
# built-ins) — so the model sees the exact fields per type instead of a
# free-form `data` blob. One type → flat args; multiple → an `item_type`
# discriminator + the union of fields, validated per-type in the handler (which
# raises a clear error the agent can correct).
# ===========================================================================


def _matches_capability_name(value: object, capability_name: str | None) -> bool:
    if not isinstance(value, str) or not capability_name:
        return False
    normalized_capability = capability_name.strip().strip("/").lower()
    normalized_binding = value.strip().strip("/").lower()
    if "/" in normalized_capability:
        return normalized_binding == normalized_capability
    return normalized_binding == normalized_capability or normalized_binding.endswith(
        f"/{normalized_capability}"
    )


def _resolve_registry_contracts(
    capability: t.Any, identifiers: t.Iterable[str]
) -> dict[str, dict[str, t.Any]]:
    selected = sorted(set(identifiers))
    if not selected:
        return {}
    identity = _resolve_identity()
    if identity is None:
        raise ItemTypeRegistryUnavailableError(
            "Platform-defined capability outputs require a platform connection to "
            f"load their pinned contracts: {', '.join(selected)}"
        )

    from dreadnode import _get_default_instance

    org, _, _ = identity
    api = _get_default_instance().api
    manifest = getattr(capability, "manifest", None)
    capability_name = getattr(capability, "name", None) or getattr(manifest, "name", None)
    capability_version = getattr(capability, "version", None) or getattr(manifest, "version", None)
    contracts: dict[str, dict[str, t.Any]] = {}
    for identifier in selected:
        try:
            detail = api.get_organization_item_type(org, identifier)
        except Exception as exc:
            raise ItemTypeRegistryUnavailableError(
                f"Could not load pinned platform contract for output {identifier!r}: {exc}"
            ) from exc
        usage = detail.get("capability_usage")
        binding = next(
            (
                entry
                for entry in usage or []
                if isinstance(entry, dict)
                and _matches_capability_name(entry.get("capability_name"), capability_name)
                and entry.get("capability_version") == capability_version
            ),
            None,
        )
        if binding is None:
            raise ItemTypeRegistryUnavailableError(
                f"Output {identifier!r} is not bound to capability "
                f"{capability_name!r} version {capability_version!r}"
            )
        contract = binding.get("contract")
        if not isinstance(contract, dict):
            current = detail.get("current_contract")
            if isinstance(current, dict) and binding.get("bound_version") == current.get("version"):
                contract = current
        if not isinstance(contract, dict) or not isinstance(contract.get("json_schema"), dict):
            raise ItemTypeRegistryUnavailableError(
                f"Platform did not return the pinned contract for output {identifier!r}"
            )
        contracts[identifier] = contract
    return contracts


def _resolve_produces_models(capability: t.Any) -> dict[str, type[BaseModel]]:
    """Import the capability's `produces` Pydantic classes from its on-disk code."""
    import importlib.util
    import sys
    from pathlib import Path

    from dreadnode.items.config import custom_item_type_refs

    produces = custom_item_type_refs(getattr(capability, "manifest", None))
    root = Path(getattr(capability, "path", "."))
    out: dict[str, type[BaseModel]] = {}
    for type_name, ref in produces.items():
        module_ref, sep, class_name = str(ref).partition(":")
        if not sep or not class_name:
            logger.warning("produces[{}] must be 'module:Class', got {!r}", type_name, ref)
            continue
        rel = module_ref if module_ref.endswith(".py") else f"{module_ref}.py"
        file_path = (root / rel).resolve()
        if not file_path.is_file():
            logger.warning("produces[{}] module not found: {}", type_name, rel)
            continue
        mod_name = f"_dn_produces_rt_{type_name}_{file_path.stem}"
        spec = importlib.util.spec_from_file_location(mod_name, file_path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        # Register in sys.modules before exec so a module that uses
        # `from __future__ import annotations` (PEP 563) can resolve its own
        # forward references. Pydantic defers forward-ref resolution until the
        # first model_json_schema()/model_rebuild(); without an importable
        # namespace that raises "not fully defined". We force resolution here,
        # while the module is registered, then remove it so we do not pollute
        # sys.modules for the rest of the process.
        sys.modules[mod_name] = module
        try:
            spec.loader.exec_module(module)
            cls = getattr(module, class_name, None)
            if isinstance(cls, type) and issubclass(cls, BaseModel):
                cls.model_rebuild()
                out[type_name] = cls
            else:
                logger.warning("produces[{}] -> {} is not a Pydantic model", type_name, ref)
        finally:
            sys.modules.pop(mod_name, None)
    return out


def _item_parameters_schema(
    types: dict[str, type[BaseModel] | dict[str, t.Any]],
) -> dict[str, t.Any]:
    """Build the report_item parameter schema from local or registry contracts.

    A JSON tool schema must be an object, so we encode `item_type` (enum) + the
    union of all types' fields. Single type → its required fields are required;
    multiple → only item_type is required and the handler enforces per-type.
    """
    from dreadnode.agents.tools import deref_json

    single = len(types) == 1
    field_schema: dict[str, dict[str, t.Any]] = {}
    field_owners: dict[str, list[str]] = {}
    type_required: dict[str, list[str]] = {}
    for tname, definition in types.items():
        raw_schema = (
            definition.model_json_schema()
            if isinstance(definition, type) and issubclass(definition, BaseModel)
            else definition["json_schema"]
        )
        sch = deref_json(raw_schema, is_json_schema=True)
        type_required[tname] = list(sch.get("required", []))
        for fname, fsch in (sch.get("properties") or {}).items():
            field_owners.setdefault(fname, []).append(tname)
            field_schema.setdefault(fname, dict(fsch))

    type_lines = []
    for name, definition in types.items():
        description = (
            (definition.__doc__ or "").strip().splitlines()[0]
            if isinstance(definition, type)
            and issubclass(definition, BaseModel)
            and (definition.__doc__ or "").strip()
            else str(definition.get("description") or "").strip()
            if isinstance(definition, dict)
            else ""
        )
        type_lines.append(f"'{name}'" + (f": {description}" if description else ""))

    properties: dict[str, t.Any] = {
        "item_type": {
            "type": "string",
            "enum": list(types),
            "description": (
                "Choose the schema that best matches one distinct structured "
                "output, then fill that type's fields using their descriptions "
                "as reporting instructions. " + "; ".join(type_lines)
            ),
        }
    }
    for fname, fsch in field_schema.items():
        s = dict(fsch)
        if not single and len(field_owners[fname]) < len(types):
            owners = ", ".join(field_owners[fname])
            s["description"] = (f"(for {owners}) " + str(s.get("description", ""))).strip()
        properties[fname] = s
    properties["ref"] = {
        "type": "string",
        "description": (
            "Optional short name to address this item later, unique within the "
            "project, for links or updates."
        ),
    }
    properties["links"] = {
        "type": "array",
        "description": (
            "Optional links to items you reported earlier by ref, such as a "
            "finding that affects an asset."
        ),
        "items": {
            "type": "object",
            "properties": {
                "target_ref": {"type": "string"},
                "relationship": {"type": "string"},
            },
            "required": ["target_ref", "relationship"],
        },
    }

    required = ["item_type"]
    if single:
        required += type_required[next(iter(types))]
    return {"type": "object", "properties": properties, "required": required}


def _make_item_handler(
    types: dict[str, type[BaseModel] | dict[str, t.Any]],
) -> t.Callable[..., str]:
    """Closure handler: validate the chosen type, emit, surface failures."""

    def report_item_dynamic(**kwargs: t.Any) -> str:
        item_type = kwargs.pop("item_type", None)
        if item_type is None and len(types) == 1:
            item_type = next(iter(types))
        if item_type not in types:
            raise ValueError(f"Unknown item_type {item_type!r}. Valid types: {list(types)}")
        ref = kwargs.pop("ref", None)
        links_in = kwargs.pop("links", None) or []

        definition = types[item_type]
        if isinstance(definition, type) and issubclass(definition, BaseModel):
            try:
                validated = definition.model_validate(kwargs)
            except ValidationError as exc:
                raise ValueError(f"Invalid {item_type} payload: {exc.errors()}") from exc
            payload = validated.model_dump(mode="json")
            title = getattr(validated, "title", None)
            schema_ref = (
                f"{item_type}@1" if item_type in BUILTIN_ITEM_SCHEMAS else f"{item_type}@produces"
            )
        else:
            from jsonschema import Draft202012Validator, FormatChecker

            validator = Draft202012Validator(
                definition["json_schema"], format_checker=FormatChecker()
            )
            errors = sorted(validator.iter_errors(kwargs), key=lambda error: list(error.path))
            if errors:
                error = errors[0]
                path = "/".join(str(part) for part in error.absolute_path) or "$"
                raise ValueError(f"Invalid {item_type} payload at {path}: {error.message}")
            payload = kwargs
            title = payload.get("title")
            schema_ref = f"{item_type}@{definition['version']['version']}"
        _check_registry_binding(item_type)

        api_links = [
            {"target_ref": link["target_ref"], "relationship": link["relationship"]}
            for link in links_in
            if isinstance(link, dict) and link.get("target_ref") and link.get("relationship")
        ]
        item_id, post_error = _emit_item(
            item_type=item_type,
            payload=payload,
            title=title,
            # Untriaged on report; severity (if any) is already in the payload.
            status=None,
            notes=None,
            schema_ref=schema_ref,
            ref=ref,
            links=api_links or None,
        )
        return _report_item_result(
            item_type=item_type,
            title=title,
            ref=ref,
            item_id=item_id,
            post_error=post_error,
        )

    return report_item_dynamic


def build_capability_report_item(
    capability: t.Any,
    *,
    builtin_types: t.Iterable[str] | None = None,
    registry_types: t.Iterable[str] | None = None,
) -> t.Any:
    """Build a typed report_item Tool for a capability's produced item types.

    Returns None if no built-in or capability-defined types are selected. When
    ``builtin_types`` is omitted, legacy callers get both built-ins whenever the
    capability declares custom produced types. Runtime capability loading passes
    the explicit built-ins the manifest opted into.
    """
    from dreadnode.agents.tools import Tool
    from dreadnode.items.config import selected_registry_item_types

    produces_models = _resolve_produces_models(capability)
    selected_registry_types = (
        set(registry_types)
        if registry_types is not None
        else selected_registry_item_types(getattr(capability, "manifest", None))
    )
    registry_contracts = _resolve_registry_contracts(capability, selected_registry_types)
    selected_builtin_types = set(builtin_types or [])
    if builtin_types is None and produces_models:
        selected_builtin_types = set(BUILTIN_ITEM_SCHEMAS)

    types: dict[str, type[BaseModel] | dict[str, t.Any]] = {
        name: model
        for name, model in BUILTIN_ITEM_SCHEMAS.items()
        if name in selected_builtin_types
    }
    types.update(produces_models)
    types.update(registry_contracts)
    if not types:
        return None

    return Tool(
        name="report_item",
        description=(
            "Report one structured output item for this run. Choose item_type, "
            "then fill only the fields that belong to that type, using the field "
            "descriptions as reporting instructions. Use finding for triageable "
            "observations, asset for observed or produced entities, and "
            "capability-defined types for their declared schemas. Assign a stable "
            "`ref` when you may link or update the item later."
        ),
        parameters_schema=_item_parameters_schema(types),
        fn=_make_item_handler(types),
    )
