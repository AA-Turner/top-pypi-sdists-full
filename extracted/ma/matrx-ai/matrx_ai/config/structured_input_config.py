"""
Structured input content types for rich context injection into AI requests.

These types are sent by the client as part of a user message's content array.
Each type is stored as a typed block in the database (cx_message.content JSONB)
and converted to plain text before being forwarded to AI providers.

All types share four common control fields:
  - convert_to_text: bool  — when True, the fetched content is converted to
                             plain text and injected inline. Assumed True for
                             all types that involve a remote fetch.
  - optional_context: bool — when True, a fetch/resolve failure does not abort
                             the request; the block is silently dropped.
  - keep_fresh: bool       — when True, resolved content is injected for this
                             turn but stripped before the messages are persisted.
                             On the next turn the block is re-fetched automatically,
                             ensuring the model always sees current data.
  - editable: bool | None  — tri-state editability signal (default None):
                               * True  — EDITABLE. The relevant CRUD/patch tools
                                 for this content type are injected into the
                                 agent's tool list (winning over agent exclusions),
                                 so the model can read, update, or patch the item
                                 without the agent definition pre-configuring them.
                               * False — EXPLICIT READ-ONLY. No tools are injected,
                                 a concise READ-ONLY notice is appended to the
                                 resolved context, and edits to the resource's id
                                 are hard-blocked at the tool layer even if the
                                 agent already carries the tool.
                               * None  — UNSPECIFIED (default-locked). Nothing is
                                 injected, nothing is said, and an agent's own
                                 tools are left untouched.

Tool sets injected per type when editable=True:
  input_notes  → note
  input_task   → task
  input_table  → dataset
  input_list   → picklist
"""

from __future__ import annotations

import json

from matrx_graph.content_ir.directives import build_directive_slug
from matrx_graph.content_ir.envelope import KIND_KEY
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_utils import vcprint

# ---------------------------------------------------------------------------
# Bookmark normalization (input_table / input_list)
# ---------------------------------------------------------------------------


def _normalize_bookmarks(value: Any) -> list[dict[str, Any]]:
    """Coerce a client-supplied ``bookmarks`` field into a ``list[dict]``.

    The UI is the single source and has sent this field in shapes that crashed
    ``to_storage_dict`` (``[dict(b) for b in self.bookmarks]``) at persist time —
    killing the entire paid request BEFORE the first DB write. The observed
    failure (``dict(b)`` with a string ``b``) happens when ``bookmarks`` arrives
    as a single dict (iterating yields its string keys), a JSON-encoded string,
    or a list whose elements are JSON strings. Accept all of those; drop anything
    that still isn't a dict with a loud warning rather than crash the request.
    """
    if value is None:
        return []
    # Whole field serialized as a JSON string.
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            vcprint(
                "[structured_input] bookmarks was an unparseable string; dropping",
                color="yellow",
            )
            return []
    # A single bookmark dict not wrapped in a list.
    if isinstance(value, dict):
        return [value]
    if not isinstance(value, list | tuple):
        vcprint(
            f"[structured_input] bookmarks had unexpected type {type(value).__name__}; dropping",
            color="yellow",
        )
        return []
    out: list[dict[str, Any]] = []
    for b in value:
        if isinstance(b, str):
            try:
                b = json.loads(b)
            except (json.JSONDecodeError, ValueError):
                vcprint(
                    "[structured_input] skipping unparseable bookmark string",
                    color="yellow",
                )
                continue
        if isinstance(b, dict):
            out.append(b)
        else:
            vcprint(
                f"[structured_input] skipping non-dict bookmark of type {type(b).__name__}",
                color="yellow",
            )
    return out


# ---------------------------------------------------------------------------
# Shared base behaviour (mixin — not a registered content type itself)
# ---------------------------------------------------------------------------


@dataclass
class _StructuredInputBase:
    convert_to_text: bool = True
    optional_context: bool = False
    keep_fresh: bool = False
    # Tri-state editability (see the module docstring): True = inject CRUD tools
    # (wins over agent exclusions); False = explicit read-only (no tools, a
    # READ-ONLY notice + a hard block on the resource id); None = unspecified
    # (inject nothing, say nothing, leave the agent's own tools untouched).
    editable: bool | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # Subclasses declare the tool names to inject when editable is True.
    # The resolver unions editable_tools() across all blocks and injects the
    # set once (deduped) via the single tool write-path.
    _editable_tools: frozenset[str] = field(
        default=frozenset(), init=False, repr=False, compare=False
    )

    def editable_tools(self) -> frozenset[str]:
        """Return the set of tool names to inject for this block.

        Only an EXPLICIT editable=True injects tools. An unspecified (None) or
        explicit read-only (False) attachment injects nothing — the agent's own
        tools, if any, are left untouched.
        """
        return self._editable_tools if self.editable is True else frozenset()

    def resource_ids(self) -> frozenset[str]:
        """Live resource ids whose latest explicit editability decision applies."""
        return frozenset()

    def read_only_resource_ids(self) -> frozenset[str]:
        """Live resource ids this block locks to read-only (editable is False).

        Reference-aware types (notes, tasks) override this to return the ids of
        their fetch-from-DB attachments so the tool layer can hard-block any
        write to them — even via a generic data tool or an agent that already
        carries the edit tool. Snapshot (by-value) items have no live id and are
        inert text, so they are never included. Empty for every other case.
        """
        return self.resource_ids() if self.editable is False else frozenset()

    def get_output(self) -> str:
        return self.metadata.get("resolved_text", "")

    def _provider_text(self) -> str | None:
        """Return resolved text if available, else None (block will be skipped)."""
        return self.metadata.get("resolved_text") or None

    async def resolve(self) -> None:
        """Fetch the referenced data and store the result in metadata["resolved_text"].

        Each subclass implements this method with its own fetch logic.
        On success, sets self.metadata["resolved_text"] to the fetched text.
        On failure:
          - If optional_context=True, logs and returns without raising.
          - If optional_context=False, raises so the executor can surface it.
        """
        raise NotImplementedError(f"{type(self).__name__} has no resolve() implementation yet.")

    def to_openai(self) -> dict[str, Any] | None:
        text = self._provider_text()
        if text is None:
            vcprint(
                {
                    "type": getattr(self, "type", "unknown"),
                    "optional_context": self.optional_context,
                    "resolved_text_present": "resolved_text" in self.metadata,
                    "metadata_keys": list(self.metadata.keys()),
                },
                "StructuredInput to_openai: block has no resolved_text — resolve() was not called or failed\n\n Temporarily not raising an error, but dropping the content block",
                color="yellow",
            )
            return None
        return {"type": "input_text", "text": text}

    def to_anthropic(self) -> dict[str, Any] | None:
        text = self._provider_text()
        if text is None:
            vcprint(
                {
                    "type": getattr(self, "type", "unknown"),
                    "optional_context": self.optional_context,
                    "resolved_text_present": "resolved_text" in self.metadata,
                    "metadata_keys": list(self.metadata.keys()),
                },
                "StructuredInput to_anthropic: block has no resolved_text — resolve() was not called or failed\n\n Temporarily not raising an error, but dropping the content block",
                color="yellow",
            )
            return None
        return {"type": "text", "text": text}

    def to_google(self) -> dict[str, Any] | None:
        text = self._provider_text()
        if text is None:
            vcprint(
                {
                    "type": getattr(self, "type", "unknown"),
                    "optional_context": self.optional_context,
                    "resolved_text_present": "resolved_text" in self.metadata,
                    "metadata_keys": list(self.metadata.keys()),
                },
                "StructuredInput to_google: block has no resolved_text — resolve() was not called or failed\n\n Temporarily not raising an error, but dropping the content block",
                color="yellow",
            )
            return None
        return {"text": text}


# ---------------------------------------------------------------------------
# input_webpage
# One or more URLs to scrape, or pre-fetched webpage content.
#
# Two accepted forms for each entry in `urls`:
#   - str  — a plain URL; the server scrapes it before sending to the model.
#   - dict — a pre-fetched entry; must contain "url" (str) and "textContent"
#            (str). Optional: "title" (str). The server uses the supplied
#            content as-is and skips scraping for that entry.
#
# Mixed lists are fine: pre-fetched entries skip the scraper, plain-URL
# entries are scraped normally, all results are assembled into one XML block.
#
# Failed scrapes produce a visible failure notice in the XML so the model
# knows the attempt was made. Failures are also recorded in metadata.
# ---------------------------------------------------------------------------


def _webpage_to_xml(url: str, title: str | None, content: str) -> str:
    title_attr = f' title="{title}"' if title else ""
    return f'<webpage url="{url}"{title_attr}>\n{content}\n</webpage>'


def _webpage_failure_xml(url: str, reason: str) -> str:
    return (
        f'<webpage url="{url}" status="failed">\n'
        f"  <note>The webpage could not be retrieved. Reason: {reason}. "
        f"Do not assume the content — acknowledge to the user that the page was unavailable.</note>\n"
        f"</webpage>"
    )


@dataclass
class WebpageInputContent(_StructuredInputBase):
    type: Literal["input_webpage"] = "input_webpage"
    # Each entry is either a plain URL string or a pre-fetched dict with
    # at least {"url": str, "textContent": str}. Both forms are valid.
    urls: list[str | dict[str, Any]] = field(default_factory=list)
    # No editable tools — web content is external and read-only.

    async def resolve(self) -> None:
        from matrx_scraper import scrape_many
        from matrx_utils import vcprint

        if not self.urls:
            return

        parts: list[str] = []
        failed: list[dict[str, str]] = []

        # Partition entries: pre-fetched dicts go straight to XML;
        # plain URL strings are collected for a single scrape_many call.
        urls_to_scrape: list[str] = []
        for entry in self.urls:
            if isinstance(entry, dict):
                url = entry.get("url", "")
                text = entry.get("textContent") or entry.get("ai_content") or entry.get("text", "")
                title = entry.get("title")
                if url and text:
                    vcprint(
                        f"[WebpageInputContent] Using pre-fetched content for: {url!r}",
                        color="cyan",
                    )
                    parts.append(_webpage_to_xml(url, title, text))
                elif url:
                    # Dict present but no content — fall back to scraping
                    vcprint(
                        f"[WebpageInputContent] Pre-fetched entry missing content, will scrape: {url!r}",
                        color="yellow",
                    )
                    urls_to_scrape.append(url)
                else:
                    vcprint(
                        f"[WebpageInputContent] Skipping malformed entry (no url): {entry!r}",
                        color="yellow",
                    )
            elif isinstance(entry, str):
                urls_to_scrape.append(entry)
            else:
                vcprint(
                    f"[WebpageInputContent] Skipping unexpected entry type {type(entry).__name__!r}: {entry!r}",
                    color="yellow",
                )

        # Scrape any plain URLs
        if urls_to_scrape:
            results = await scrape_many(urls_to_scrape, use_proxy=True)
            for result in results:
                if result.success and result.ai_content:
                    parts.append(_webpage_to_xml(result.url, result.title, result.ai_content))
                else:
                    reason = result.failure_reason or "unknown"
                    vcprint(
                        f"[WebpageInputContent] Scrape failed: {result.url!r} — {reason}",
                        color="yellow",
                    )
                    failed.append({"url": result.url, "reason": reason})
                    parts.append(_webpage_failure_xml(result.url, reason))

        if failed and not self.optional_context and len(failed) == len(urls_to_scrape):
            raise RuntimeError(f"All webpage scrapes failed: {', '.join(f['url'] for f in failed)}")

        if parts:
            self.metadata["resolved_text"] = (
                "<web_context>\n\n" + "\n\n".join(parts) + "\n\n</web_context>"
            )

        if failed:
            self.metadata["scrape_failures"] = failed

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_webpage",
            "urls": list(self.urls),
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# Shared failure notice — every list-of-resources input renders a visible,
# model-readable marker when an individual item can't be resolved, instead of
# letting one bad item abort the whole request.
# ---------------------------------------------------------------------------


def _resource_failure_xml(tag: str, identifier: str, reason: str) -> str:
    return (
        f'<{tag} id="{identifier}" status="failed">\n'
        f"  <note>This {tag} could not be loaded. Reason: {reason}. "
        f"Do not assume its contents — acknowledge to the user that it was unavailable.</note>\n"
        f"</{tag}>"
    )


# Concise, model-readable marker appended to an explicitly read-only block. Kept
# to one line to avoid inflating the context window — its only job is to stop the
# model from burning tool calls trying to edit a locked resource (and to protect
# us from a user asking an agent to mutate something they marked reference-only).
def _read_only_notice_xml(tag: str) -> str:
    return (
        f'<{tag}_access mode="read_only">READ ONLY - if asked to edit this {tag}, '
        f"do not attempt it; tell the user to enable 'editable' on the attachment."
        f"</{tag}_access>"
    )


_SNAPSHOT_BODY_KEYS = ("content", "text", "body", "description", "value")


def _canonical_snapshot_body(snapshot: dict[str, Any], target_key: str) -> dict[str, Any]:
    """Map ResourceRef's five accepted prose keys onto a renderer's body key."""
    normalized = dict(snapshot)
    if isinstance(normalized.get(target_key), str) and normalized[target_key]:
        return normalized
    for key in _SNAPSHOT_BODY_KEYS:
        value = normalized.get(key)
        if isinstance(value, str) and value:
            normalized[target_key] = value
            return normalized
    return normalized


# ---------------------------------------------------------------------------
# input_notes
# One or more user notes. Each entry is either a note ID (fetched live from the
# DB — "reference" mode) or an inline snapshot dict (rendered verbatim — see
# resource_ref.py for the full contract). All resolved notes are injected as XML.
# ---------------------------------------------------------------------------


@dataclass
class NotesInputContent(_StructuredInputBase):
    type: Literal["input_notes"] = "input_notes"
    # Each entry is a bare note-id string OR a dict carrying at least an "id"
    # (reference mode) or inline content with mode="snapshot" (value mode).
    note_ids: list[str | dict[str, Any]] = field(default_factory=list)
    template: str = "full"
    # Full CRUD set — injected when editable=True is explicitly requested.
    _editable_tools: frozenset[str] = field(
        default=frozenset({"note"}),
        init=False,
        repr=False,
        compare=False,
    )

    def resource_ids(self) -> frozenset[str]:
        from matrx_ai.config.resource_ref import normalize_resource_refs

        return frozenset(
            r.id for r in normalize_resource_refs(self.note_ids) if r.mode == "reference" and r.id
        )

    async def resolve(self) -> None:
        # Ownership-gated fetch: a note the requesting user neither owns nor may read
        # (RLS: owner / assignee / org / project / has_permission sharing / public)
        # resolves to a failure notice, NEVER another user's note. `load_referenceable_record`
        # runs the read inside `acting_as_user()` (Supabase `authenticated` role, RLS enforced)
        # with `use_cache=False` — the SAME gated primitive the reference `record` resolver
        # uses — replacing the unscoped, RLS-bypassing `postgres`-pool `get_note_as_xml` path
        # (FOUND_DEFECTS AID-NOTE-XREAD, sibling of AID-BOOKMARK-XREAD). `user_id` comes from
        # the per-run app context, exactly as the bookmark stager does. The snapshot
        # (attach-by-value) branch is inert client text and needs no gate. The XML shape is
        # preserved exactly via the existing `render_note_snapshot_xml` renderer (identical
        # output to `_to_llm_xml`), so the `<id>` the edit tool needs stays intact — which is
        # why this reuses the gated LOADER rather than the record resolver (that strips the id).
        # A forged/foreign id degrades quietly rather than hard-failing a paid turn. Lazy
        # cross-layer import (matrx-ai → aidream service) matches the `resolve_bookmarks` /
        # user_secrets_tool precedent.
        # HOST-INJECTED loader (matrx-ai must not import aidream — the package
        # boundary gate; a lazy import is still a violation). Unconfigured
        # (standalone matrx-ai) → None → referenced records resolve to a failure
        # notice via the rec-is-None path below.
        from matrx_connect.context.app_context import try_get_app_context
        from matrx_utils import vcprint

        from matrx_ai._ext import get_referenceable_record_loader

        load_referenceable_record = get_referenceable_record_loader()

        from matrx_ai.config.resource_ref import normalize_resource_refs
        from matrx_ai.db.content_types.notes import render_note_snapshot_xml

        _ctx = try_get_app_context()
        user_id = (_ctx.user_id or None) if _ctx is not None else None

        refs = normalize_resource_refs(self.note_ids)
        parts: list[str] = []
        failures: list[dict[str, str]] = []

        for ref in refs:
            if ref.mode == "snapshot" and ref.has_inline_content:
                snapshot = _canonical_snapshot_body(ref.inline, "content")
                parts.append(render_note_snapshot_xml(snapshot, template=self.template))
                continue
            if not ref.id:
                reason = "no usable note id and no inline content"
                vcprint(
                    f"[NotesInputContent] Unresolvable note ref: {ref.inline!r}", color="yellow"
                )
                failures.append({"ref": "", "reason": reason})
                parts.append(_resource_failure_xml("note", "", reason))
                continue
            rec = None
            if user_id and load_referenceable_record is not None:
                try:
                    rec = await load_referenceable_record("note", ref.id)
                except Exception as exc:  # noqa: BLE001 — a reference must never break the run
                    vcprint(
                        f"[NotesInputContent] Note fetch failed: {ref.id!r} — "
                        f"{type(exc).__name__}: {exc}",
                        color="yellow",
                    )
            if rec:
                parts.append(render_note_snapshot_xml(rec, template=self.template))
            else:
                reason = "not found or not readable"
                vcprint(
                    f"[NotesInputContent] Note not readable: {ref.id!r}", color="yellow"
                )
                failures.append({"ref": ref.id, "reason": reason})
                parts.append(_resource_failure_xml("note", ref.id, reason))

        # Only abort the turn when EVERYTHING failed on a required block. A
        # single bad note degrades to an inline failure notice + client warning.
        if failures and not self.optional_context and len(failures) == len(refs):
            raise RuntimeError(
                f"Failed to load all {len(failures)} attached note(s): "
                + "; ".join(f"{f['ref'] or '<no id>'} ({f['reason']})" for f in failures)
            )

        if parts:
            if self.editable is False:
                parts.append(_read_only_notice_xml("note"))
            self.metadata["resolved_text"] = "\n".join(parts)
        if failures:
            self.metadata["resource_failures"] = failures

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_notes",
            "note_ids": list(self.note_ids),
            "template": self.template,
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# input_task
# One or more tasks. Each entry is either a task ID (fetched live from the DB —
# "reference" mode) or an inline snapshot dict (rendered verbatim — see
# resource_ref.py for the full contract). All resolved tasks are injected as XML.
# ---------------------------------------------------------------------------


@dataclass
class TaskInputContent(_StructuredInputBase):
    type: Literal["input_task"] = "input_task"
    # Each entry is a bare task-id string OR a dict carrying at least an "id"
    # (reference mode) or inline content with mode="snapshot" (value mode).
    task_ids: list[str | dict[str, Any]] = field(default_factory=list)
    template: str = "full"
    # Full CRUD set — injected when editable=True is explicitly requested.
    _editable_tools: frozenset[str] = field(
        default=frozenset({"task"}),
        init=False,
        repr=False,
        compare=False,
    )

    def resource_ids(self) -> frozenset[str]:
        from matrx_ai.config.resource_ref import normalize_resource_refs

        return frozenset(
            r.id for r in normalize_resource_refs(self.task_ids) if r.mode == "reference" and r.id
        )

    async def resolve(self) -> None:
        # Ownership-gated fetch — see NotesInputContent.resolve for the full rationale.
        # A task the requesting user may not read (RLS: owner / assignee / org / project /
        # has_permission sharing / public) resolves to a failure notice, never another
        # user's task. Replaces the unscoped, RLS-bypassing `postgres`-pool `get_task_as_xml`
        # path (FOUND_DEFECTS AID-TASK-XREAD). XML shape preserved via the existing
        # `render_task_snapshot_xml` renderer (identical output to `_to_llm_xml`, keeps the id).
        # HOST-INJECTED loader (matrx-ai must not import aidream — the package
        # boundary gate; a lazy import is still a violation). Unconfigured
        # (standalone matrx-ai) → None → referenced records resolve to a failure
        # notice via the rec-is-None path below.
        from matrx_connect.context.app_context import try_get_app_context
        from matrx_utils import vcprint

        from matrx_ai._ext import get_referenceable_record_loader

        load_referenceable_record = get_referenceable_record_loader()

        from matrx_ai.config.resource_ref import normalize_resource_refs
        from matrx_ai.db.content_types.tasks import render_task_snapshot_xml

        _ctx = try_get_app_context()
        user_id = (_ctx.user_id or None) if _ctx is not None else None

        refs = normalize_resource_refs(self.task_ids)
        parts: list[str] = []
        failures: list[dict[str, str]] = []

        for ref in refs:
            if ref.mode == "snapshot" and ref.has_inline_content:
                snapshot = _canonical_snapshot_body(ref.inline, "description")
                parts.append(render_task_snapshot_xml(snapshot, template=self.template))
                continue
            if not ref.id:
                reason = "no usable task id and no inline content"
                vcprint(f"[TaskInputContent] Unresolvable task ref: {ref.inline!r}", color="yellow")
                failures.append({"ref": "", "reason": reason})
                parts.append(_resource_failure_xml("task", "", reason))
                continue
            rec = None
            if user_id and load_referenceable_record is not None:
                try:
                    rec = await load_referenceable_record("task", ref.id)
                except Exception as exc:  # noqa: BLE001 — a reference must never break the run
                    vcprint(
                        f"[TaskInputContent] Task fetch failed: {ref.id!r} — "
                        f"{type(exc).__name__}: {exc}",
                        color="yellow",
                    )
            if rec:
                parts.append(render_task_snapshot_xml(rec, template=self.template))
            else:
                reason = "not found or not readable"
                vcprint(f"[TaskInputContent] Task not readable: {ref.id!r}", color="yellow")
                failures.append({"ref": ref.id, "reason": reason})
                parts.append(_resource_failure_xml("task", ref.id, reason))

        # Only abort the turn when EVERYTHING failed on a required block. A
        # single bad task degrades to an inline failure notice + client warning.
        if failures and not self.optional_context and len(failures) == len(refs):
            raise RuntimeError(
                f"Failed to load all {len(failures)} attached task(s): "
                + "; ".join(f"{f['ref'] or '<no id>'} ({f['reason']})" for f in failures)
            )

        if parts:
            if self.editable is False:
                parts.append(_read_only_notice_xml("task"))
            self.metadata["resolved_text"] = "\n".join(parts)
        if failures:
            self.metadata["resource_failures"] = failures

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_task",
            "task_ids": list(self.task_ids),
            "template": self.template,
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# input_table
# One or more table bookmarks from the UI. Each bookmark is a dict with a
# 'type' field (full_table | table_column | table_row | table_cell) plus the
# IDs needed for that scope. See TABLE_REFERENCE_FETCH.md for shapes.
# ---------------------------------------------------------------------------


@dataclass
class TableInputContent(_StructuredInputBase):
    type: Literal["input_table"] = "input_table"
    bookmarks: list[dict[str, Any]] = field(default_factory=list)
    _editable_tools: frozenset[str] = field(
        default=frozenset({"dataset"}),
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        # Single chokepoint: a malformed client `bookmarks` shape must never reach
        # `to_storage_dict`/`resolve` and crash a paid request at persist time.
        self.bookmarks = _normalize_bookmarks(self.bookmarks)

    def resource_ids(self) -> frozenset[str]:
        return frozenset(
            value.strip()
            for bookmark in self.bookmarks
            for key in ("table_id", "row_id")
            if isinstance((value := bookmark.get(key)), str) and value.strip()
        )

    async def resolve(self) -> None:
        # Ownership-gated via the ONE ReferenceOrchestrator bridge (`resolve_bookmarks`):
        # a bookmark for a table the requesting user neither owns nor may read publicly
        # resolves to NOTHING (fail-closed) — never another user's rows. This replaces
        # the unscoped `bookmark_as_xml` cross-user-read path (FOUND_DEFECTS
        # AID-BOOKMARK-XREAD). `user_id` comes from the per-run app context, exactly as
        # the `matrx` reference-fence stager does. A forged/foreign id degrades quietly
        # rather than hard-failing a paid turn (the correct posture: don't leak, and
        # don't hand a client a way to probe existence).
        #
        # The resolver is HOST-INJECTED (matrx-ai must not import aidream — the
        # package-boundary gate; a lazy import is still a violation). Unconfigured
        # (standalone matrx-ai) → no bookmark store → resolve to nothing.
        from matrx_connect.context.app_context import try_get_app_context

        from matrx_ai._ext import get_bookmark_resolver

        resolve_bookmarks = get_bookmark_resolver()
        if resolve_bookmarks is None:
            return

        _ctx = try_get_app_context()
        user_id = (_ctx.user_id or None) if _ctx is not None else None

        parts = await resolve_bookmarks(list(self.bookmarks), user_id=user_id)
        if parts:
            self.metadata["resolved_text"] = "\n".join(parts)

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_table",
            "bookmarks": [dict(b) for b in self.bookmarks],
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# input_list
# One or more list bookmarks from the UI. Each bookmark is a dict with a
# 'type' field (full_list | list_group | list_item) plus the IDs needed for
# that scope. See TABLE_REFERENCE_FETCH.md for shapes.
# ---------------------------------------------------------------------------


@dataclass
class ListInputContent(_StructuredInputBase):
    type: Literal["input_list"] = "input_list"
    bookmarks: list[dict[str, Any]] = field(default_factory=list)
    _editable_tools: frozenset[str] = field(
        default=frozenset({"picklist"}),
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        # Single chokepoint: a malformed client `bookmarks` shape must never reach
        # `to_storage_dict`/`resolve` and crash a paid request at persist time.
        self.bookmarks = _normalize_bookmarks(self.bookmarks)

    def resource_ids(self) -> frozenset[str]:
        return frozenset(
            value.strip()
            for bookmark in self.bookmarks
            for key in ("list_id", "item_id")
            if isinstance((value := bookmark.get(key)), str) and value.strip()
        )

    async def resolve(self) -> None:
        # Ownership-gated via the ONE ReferenceOrchestrator bridge (`resolve_bookmarks`):
        # a bookmark for a list the requesting user neither owns nor may read publicly
        # resolves to NOTHING (fail-closed) — never another user's items. This replaces
        # the unscoped `bookmark_as_xml` cross-user-read path (FOUND_DEFECTS
        # AID-BOOKMARK-XREAD). `user_id` comes from the per-run app context, exactly as
        # the `matrx` reference-fence stager does. A forged/foreign id degrades quietly
        # rather than hard-failing a paid turn.
        #
        # The resolver is HOST-INJECTED (matrx-ai must not import aidream — the
        # package-boundary gate; a lazy import is still a violation). Unconfigured
        # (standalone matrx-ai) → no bookmark store → resolve to nothing.
        from matrx_connect.context.app_context import try_get_app_context

        from matrx_ai._ext import get_bookmark_resolver

        resolve_bookmarks = get_bookmark_resolver()
        if resolve_bookmarks is None:
            return

        _ctx = try_get_app_context()
        user_id = (_ctx.user_id or None) if _ctx is not None else None

        parts = await resolve_bookmarks(list(self.bookmarks), user_id=user_id)
        if parts:
            self.metadata["resolved_text"] = "\n".join(parts)

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_list",
            "bookmarks": [dict(b) for b in self.bookmarks],
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# input_data
# One or more DataRef objects — universal references to system table data.
# Each ref is a dict with ref_type ∈ {db_record, db_query, db_field}.
# See matrx_ai.db.content_types.data_ref for the full spec.
# ---------------------------------------------------------------------------


@dataclass
class DataInputContent(_StructuredInputBase):
    type: Literal["input_data"] = "input_data"
    refs: list[dict[str, Any]] = field(default_factory=list)

    async def resolve(self) -> None:
        from matrx_utils import vcprint

        from matrx_ai.db.content_types.data_ref import resolve_data_refs

        xml_block, errors = await resolve_data_refs(self.refs)

        if errors and not self.optional_context:
            raise RuntimeError(f"DataRef resolution errors: {'; '.join(errors)}")

        if errors:
            vcprint(f"[DataInputContent] Optional errors: {errors}", color="yellow")

        if xml_block:
            self.metadata["resolved_text"] = xml_block

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_data",
            "refs": [dict(r) for r in self.refs],
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# input_context
# A named by-value context snapshot. The frontend renders these same three
# fields (id, name, data); the provider receives the exact snapshot as JSON.
# ---------------------------------------------------------------------------


@dataclass
class ContextInputContent(_StructuredInputBase):
    type: Literal["input_context"] = "input_context"
    context_id: str = ""
    context_name: str = ""
    context_data: dict[str, Any] = field(default_factory=dict)

    async def resolve(self) -> None:
        snapshot = {
            "id": self.context_id or None,
            "name": self.context_name or None,
            "data": self.context_data,
        }
        self.metadata["resolved_text"] = (
            "<context_snapshot>\n"
            f"{json.dumps(snapshot, ensure_ascii=False, indent=2)}\n"
            "</context_snapshot>"
        )

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_context",
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.context_id:
            result["context_id"] = self.context_id
        if self.context_name:
            result["context_name"] = self.context_name
        if self.context_data:
            result["context_data"] = {**self.context_data}
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# ID-backed entity inputs
#
# These blocks persist pure ids, then emit the platform's canonical ``matrx``
# reference envelope into model context. The host's per-send reference stager
# resolves each record through the ONE RLS-scoped reference registry. Keeping the
# envelope construction here (rather than importing aidream) preserves matrx-ai's
# package boundary while ensuring every accepted attachment reaches the model.
#
# Workbook/document are slightly richer: their record reference resolves metadata,
# while the adjacent instruction points the model at the dedicated content tool for
# the potentially huge opaque Univer snapshot.
# ---------------------------------------------------------------------------


def _record_reference_fence(resource_type: str, ids: list[str]) -> str:
    """Serialize record ids as the canonical persisted/in-content reference shape.

    Emits the Kind Directives two-key shell (`__kind` first — the streaming
    detector reads the first key). The retired 4-key `matrx_version` shell is
    READ-ONLY platform-wide; minting it here was adversarial finding F2 of the
    kind-directives merge review.
    """
    envelope = {
        KIND_KEY: build_directive_slug("reference", resource_type),
        "items": [{"id": rid} for rid in ids],
    }
    return f"```matrx\n{json.dumps(envelope, separators=(',', ':'))}\n```"


def _content_tool_instruction(tag: str, ids: list[str], editable: bool | None) -> str:
    """Tell the model how to load opaque workbook/document content on demand."""
    quoted_ids = ", ".join(json.dumps(rid) for rid in ids)
    if editable is False:
        action = f"Use the {tag} tool with action=read for ids [{quoted_ids}]. Attached READ ONLY."
    elif editable is True:
        action = (
            f"Use the {tag} tool with action=read for ids [{quoted_ids}], "
            "and action=edit to change them."
        )
    else:
        action = f"Use the {tag} tool with action=read for ids [{quoted_ids}]."
    return f"Attached {tag} content is available on demand. {action}"


@dataclass
class _RecordReferenceInputContent(_StructuredInputBase):
    """Shared resolution/storage behavior for simple id-backed record inputs."""

    template: str = "full"

    # Subclasses use class variables because these describe the wire contract,
    # not per-instance state. They intentionally stay out of dataclass storage.
    _resource_type = ""
    _ids_field = ""

    def _ids(self) -> list[str]:
        raw = getattr(self, self._ids_field, [])
        return [value.strip() for value in raw if isinstance(value, str) and value.strip()]

    def resource_ids(self) -> frozenset[str]:
        return frozenset(self._ids())

    async def resolve(self) -> None:
        ids = self._ids()
        if ids:
            self.metadata["resolved_text"] = _record_reference_fence(self._resource_type, ids)

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": getattr(self, "type"),
            self._ids_field: list(getattr(self, self._ids_field)),
            "template": self.template,
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


@dataclass
class AgentInputContent(_RecordReferenceInputContent):
    type: Literal["input_agent"] = "input_agent"
    agent_ids: list[str] = field(default_factory=list)
    _resource_type = "agent"
    _ids_field = "agent_ids"


@dataclass
class ProjectInputContent(_RecordReferenceInputContent):
    type: Literal["input_project"] = "input_project"
    project_ids: list[str] = field(default_factory=list)
    _resource_type = "project"
    _ids_field = "project_ids"
    _editable_tools: frozenset[str] = field(
        default=frozenset({"data"}), init=False, repr=False, compare=False
    )


@dataclass
class AgentAppInputContent(_RecordReferenceInputContent):
    type: Literal["input_agent_app"] = "input_agent_app"
    agent_app_ids: list[str] = field(default_factory=list)
    _resource_type = "agent_app"
    _ids_field = "agent_app_ids"


@dataclass
class TranscriptInputContent(_RecordReferenceInputContent):
    type: Literal["input_transcript"] = "input_transcript"
    transcript_ids: list[str] = field(default_factory=list)
    _resource_type = "transcript"
    _ids_field = "transcript_ids"
    _editable_tools: frozenset[str] = field(
        default=frozenset({"data"}), init=False, repr=False, compare=False
    )


@dataclass
class TranscriptSessionInputContent(_RecordReferenceInputContent):
    type: Literal["input_transcript_session"] = "input_transcript_session"
    transcript_session_ids: list[str] = field(default_factory=list)
    _resource_type = "transcript_session"
    _ids_field = "transcript_session_ids"


@dataclass
class WorkbookInputContent(_StructuredInputBase):
    type: Literal["input_workbook"] = "input_workbook"
    # Each entry is a bare workbook-id string OR a dict carrying at least an "id".
    workbook_ids: list[str | dict[str, Any]] = field(default_factory=list)
    _editable_tools: frozenset[str] = field(
        default=frozenset({"workbook"}),
        init=False,
        repr=False,
        compare=False,
    )

    def _ref_ids(self) -> list[str]:
        from matrx_ai.config.resource_ref import normalize_resource_refs

        return [r.id for r in normalize_resource_refs(self.workbook_ids) if r.id]

    def resource_ids(self) -> frozenset[str]:
        return frozenset(self._ref_ids())

    async def resolve(self) -> None:
        ids = self._ref_ids()
        if ids:
            self.metadata["resolved_text"] = "\n".join(
                (
                    _record_reference_fence("workbook", ids),
                    _content_tool_instruction("workbook", ids, self.editable),
                )
            )

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_workbook",
            "workbook_ids": list(self.workbook_ids),
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


@dataclass
class DocumentInputContent(_StructuredInputBase):
    type: Literal["input_document"] = "input_document"
    document_ids: list[str | dict[str, Any]] = field(default_factory=list)
    _editable_tools: frozenset[str] = field(
        default=frozenset({"document"}),
        init=False,
        repr=False,
        compare=False,
    )

    def _ref_ids(self) -> list[str]:
        from matrx_ai.config.resource_ref import normalize_resource_refs

        return [r.id for r in normalize_resource_refs(self.document_ids) if r.id]

    def resource_ids(self) -> frozenset[str]:
        return frozenset(self._ref_ids())

    async def resolve(self) -> None:
        ids = self._ref_ids()
        if ids:
            self.metadata["resolved_text"] = "\n".join(
                (
                    _record_reference_fence("document", ids),
                    _content_tool_instruction("document", ids, self.editable),
                )
            )

    def to_storage_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": "input_document",
            "document_ids": list(self.document_ids),
            "convert_to_text": self.convert_to_text,
            "optional_context": self.optional_context,
            "keep_fresh": self.keep_fresh,
        }
        if self.editable is not None:
            result["editable"] = self.editable
        if self.metadata:
            result["metadata"] = {**self.metadata}
        return result


# ---------------------------------------------------------------------------
# Union type for all structured input content
# ---------------------------------------------------------------------------

StructuredInputContent = (
    WebpageInputContent
    | NotesInputContent
    | TaskInputContent
    | TableInputContent
    | ListInputContent
    | DataInputContent
    | ContextInputContent
    | AgentInputContent
    | ProjectInputContent
    | AgentAppInputContent
    | TranscriptInputContent
    | TranscriptSessionInputContent
    | WorkbookInputContent
    | DocumentInputContent
)

# Canonical type string → class mapping (used by parse_content and reconstruct)
STRUCTURED_INPUT_TYPE_MAP: dict[str, type] = {
    "input_webpage": WebpageInputContent,
    "input_notes": NotesInputContent,
    "input_task": TaskInputContent,
    "input_table": TableInputContent,
    "input_list": ListInputContent,
    "input_data": DataInputContent,
    "input_context": ContextInputContent,
    "input_agent": AgentInputContent,
    "input_project": ProjectInputContent,
    "input_agent_app": AgentAppInputContent,
    "input_transcript": TranscriptInputContent,
    "input_transcript_session": TranscriptSessionInputContent,
    "input_workbook": WorkbookInputContent,
    "input_document": DocumentInputContent,
}


def reconstruct_structured_input(block: dict[str, Any]) -> StructuredInputContent | None:
    """Reconstruct a structured input content object from a stored JSONB block.

    Returns None if the block type is not a known structured input type.
    """
    block_type = block.get("type", "")
    cls = STRUCTURED_INPUT_TYPE_MAP.get(block_type)
    if cls is None:
        return None

    meta = block.get("metadata", {})
    common = {
        "convert_to_text": block.get("convert_to_text", True),
        "optional_context": block.get("optional_context", False),
        "keep_fresh": block.get("keep_fresh", False),
        # Tri-state: absent stays None (unspecified). True = editable, False =
        # explicit read-only. Never coerce a missing key to False.
        "editable": block.get("editable"),
        "metadata": meta,
    }

    if block_type == "input_webpage":
        # urls may be:
        #   - a list of plain URL strings (server scrapes them)
        #   - a list of pre-fetched dicts {"url", "textContent", ...} (server skips scrape)
        #   - a mix of both
        # Legacy: some old blocks stored a single "url" string instead of a "urls" list.
        urls = block.get("urls")
        if urls is None:
            legacy_url = block.get("url", "")
            urls = [legacy_url] if legacy_url else []
        return WebpageInputContent(urls=urls, **common)

    if block_type == "input_notes":
        return NotesInputContent(
            note_ids=block.get("note_ids", []),
            template=block.get("template", "full"),
            **common,
        )

    if block_type == "input_task":
        return TaskInputContent(
            task_ids=block.get("task_ids", []),
            template=block.get("template", "full"),
            **common,
        )

    if block_type == "input_table":
        return TableInputContent(
            bookmarks=block.get("bookmarks", []),
            **common,
        )

    if block_type == "input_list":
        return ListInputContent(
            bookmarks=block.get("bookmarks", []),
            **common,
        )

    if block_type == "input_data":
        # Support both old "query" dict (legacy) and new "refs" list
        refs = block.get("refs")
        if refs is None:
            legacy_query = block.get("query")
            refs = [legacy_query] if legacy_query else []
        return DataInputContent(refs=refs, **common)

    if block_type == "input_context":
        return ContextInputContent(
            context_id=block.get("context_id", ""),
            context_name=block.get("context_name", ""),
            context_data=block.get("context_data", {}),
            **common,
        )

    record_id_fields = {
        "input_agent": "agent_ids",
        "input_project": "project_ids",
        "input_agent_app": "agent_app_ids",
        "input_transcript": "transcript_ids",
        "input_transcript_session": "transcript_session_ids",
    }
    if ids_field := record_id_fields.get(block_type):
        return cls(
            **{ids_field: block.get(ids_field, [])},
            template=block.get("template", "full"),
            **common,
        )

    if block_type == "input_workbook":
        return WorkbookInputContent(workbook_ids=block.get("workbook_ids", []), **common)

    if block_type == "input_document":
        return DocumentInputContent(document_ids=block.get("document_ids", []), **common)

    return None


def structured_input_editable_tool_names() -> frozenset[str]:
    """Every tool name ``inject_editable_tools`` would add when ``editable=True``."""
    tools: set[str] = set()
    for cls in STRUCTURED_INPUT_TYPE_MAP.values():
        tools.update(cls(editable=True).editable_tools())
    return frozenset(tools)
