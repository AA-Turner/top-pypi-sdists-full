from __future__ import annotations

import textwrap
from typing import Any

from matrx_utils.row_access import publish_columns

from matrx_ai.db._registry import get_base, get_model
from matrx_ai.db.content_types.patch_utils import PatchError, apply_patch

NotesBase = get_base("NotesBase")
Notes = get_model("Notes")

# ---------------------------------------------------------------------------
# XML rendering templates — edit these to change how notes are sent to LLMs.
# ---------------------------------------------------------------------------

XML_TEMPLATE_FULL = """\
<note>
  <id>{id}</id>
  <label>{label}</label>
  <folder_name>{folder_name}</folder_name>
  <content>
{content}
  </content>
</note>"""

XML_TEMPLATE_COMPACT = """\
<note>
  <id>{id}</id>
  <label>{label}</label>
  <content>{content}</content>
</note>"""

XML_TEMPLATE_MINIMAL = """\
<note id="{id}">
  <label>{label}</label>
  <content>{content}</content>
</note>"""

DEFAULT_XML_TEMPLATE = "full"

_XML_TEMPLATES: dict[str, str] = {
    "full": XML_TEMPLATE_FULL,
    "compact": XML_TEMPLATE_COMPACT,
    "minimal": XML_TEMPLATE_MINIMAL,
}


def render_note_snapshot_xml(data: dict[str, Any], template: str = DEFAULT_XML_TEMPLATE) -> str:
    """Render an LLM-friendly note XML block from a client-supplied dict.

    The "snapshot" / attach-by-value path: the caller hands us the note fields
    directly and we render them verbatim without any database fetch. Mirrors
    NotesManager._to_llm_xml but reads from a plain dict instead of a model.
    """
    tmpl = _XML_TEMPLATES.get(template, XML_TEMPLATE_FULL)
    content = textwrap.indent(str(data.get("content") or "").strip(), "    ")
    return tmpl.format(
        id=data.get("id") or "",
        label=data.get("label") or "",
        folder_name=data.get("folder_name") or "",
        content=content,
    )


# ---------------------------------------------------------------------------
# Fields the LLM must never touch — stripped before any write reaches the DB.
# ---------------------------------------------------------------------------
_IMMUTABLE_FIELDS = frozenset(
    {
        "id",
        "created_by",
        "created_at",
        "updated_at",
        "sync_version",
        "version",
        "deleted_at",
        "dto",
    }
)

# Fields the LLM is allowed to set/update. ``published_to_web`` (+ its stamps) is
# the canonical replacement for the dropped ``is_public`` boolean; ``shown_to`` is
# the list filter. The ``is_public`` create/update affordance is translated in this
# module so the agent-facing tool contract stays stable.
_MUTABLE_FIELDS = frozenset(
    {
        "label",
        "content",
        "folder_name",
        "tags",
        "metadata",
        "published_to_web",
        "published_to_web_at",
        "published_to_web_by",
        "shown_to",
        "position",
    }
)


# ---------------------------------------------------------------------------
# Result / error helpers
# ---------------------------------------------------------------------------


def _ok(note: Notes) -> dict[str, Any]:
    return {"success": True, "note": note.to_dict()}


def _err(operation: str, note_id: str, error: Exception, **extra: Any) -> dict[str, Any]:
    return {
        "success": False,
        "operation": operation,
        "note_id": note_id,
        "error_type": type(error).__name__,
        "error": str(error),
        **extra,
    }


def _not_visible(operation: str, note_id: str) -> dict[str, Any]:
    """The note does not exist FOR THIS CALLER — missing, archived, and hidden
    read the same. Under the caller's RLS session a row they may not see is
    simply absent, so this one honest answer names the id and leaks nothing."""
    return {
        "success": False,
        "operation": operation,
        "note_id": note_id,
        "error_type": "not_found",
        "error": f"Note {note_id} was not found, or you do not have access to it.",
    }


def _no_write_access(operation: str, note_id: str, **extra: Any) -> dict[str, Any]:
    """The caller can see the note but the database refused the change."""
    return {
        "success": False,
        "operation": operation,
        "note_id": note_id,
        "error_type": "no_access",
        "error": f"You can view note {note_id} but you do not have permission to change it.",
        **extra,
    }


_RLS_REFUSAL_MARKERS = ("row-level security", "permission denied", "42501")


class NotesManager(NotesBase):
    _instance: NotesManager | None = None

    def __new__(cls, *args: Any, **kwargs: Any) -> NotesManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        super().__init__()

    async def _initialize_runtime_data(self, item: Notes) -> None:
        pass

    # ------------------------------------------------------------------
    # ACCESS IS NOT DECIDED HERE. Callers acting for a person run these
    # methods inside that person's RLS session
    # (``matrx_ai.tools.person_session.as_the_person``); Postgres RLS decides
    # what exists and what may change. Every by-id read is AUTHORITATIVE
    # (``use_cache=False``): the ORM's identity cache is shared across callers
    # and knows nothing about who is asking.
    # ------------------------------------------------------------------

    async def _read_live(self, note_id: str) -> Notes | None:
        """The note as the current connection sees it — None when missing,
        archived, or hidden from the caller by RLS."""
        note = await self.load_item_or_none(use_cache=False, **self._pk_filter(note_id))
        if note is None or getattr(note, "deleted_at", None) is not None:
            return None
        return note

    async def _explain_refused_write(
        self, operation: str, note_id: str, version_before: Any, error: Exception, **extra: Any
    ) -> dict[str, Any]:
        """Name why a write to a note the caller could SEE did not land.

        RLS refuses an UPDATE silently (0 rows) or, for a WITH CHECK breach,
        with 42501. Either way the note is still there, unchanged, for this
        caller — a permission refusal, not a conflict. The database decided;
        this only reports it.
        """
        if any(marker in str(error) for marker in _RLS_REFUSAL_MARKERS):
            return _no_write_access(operation, note_id, **extra)
        try:
            now = await self._read_live(note_id)
        except Exception:
            return _err(operation, note_id, error, **extra)
        if now is None:
            return _not_visible(operation, note_id)
        if getattr(now, "version", None) == version_before:
            return _no_write_access(operation, note_id, **extra)
        return _err(operation, note_id, error, **extra)

    async def _write_visible(
        self, operation: str, note_id: str, updates: dict[str, Any], **extra: Any
    ) -> tuple[Notes | None, dict[str, Any] | None]:
        """Read the note as the caller, then write to exactly that row.

        Returns ``(note, None)`` on success or ``(None, error_dict)``.
        """
        try:
            note = await self._read_live(note_id)
        except Exception as e:
            return None, _err(operation, note_id, e, **extra)
        if note is None:
            return None, _not_visible(operation, note_id)
        return await self._write_row(operation, note, updates, **extra)

    async def _write_row(
        self, operation: str, note: Notes, updates: dict[str, Any], **extra: Any
    ) -> tuple[Notes | None, dict[str, Any] | None]:
        note_id = str(note.id)
        version_before = getattr(note, "version", None)
        try:
            async with self._governed_write():
                note = await self._update_item(note, **updates)
        except Exception as e:
            return None, await self._explain_refused_write(
                operation, note_id, version_before, e, **extra
            )
        return note, None

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    async def get_note(self, note_id: str) -> dict[str, Any]:
        """Return the full note dict, or a structured error.

        A note the caller may not see is ``error_type='not_found'`` naming the id.
        """
        try:
            note = await self._read_live(note_id)
        except Exception as e:
            return _err("get_note", note_id, e)
        if note is None:
            return _not_visible("get_note", note_id)
        return _ok(note)

    async def get_note_as_xml(
        self, note_id: str, template: str = DEFAULT_XML_TEMPLATE
    ) -> dict[str, Any]:
        """Return the note rendered as LLM-friendly XML."""
        try:
            note = await self.load_notes_by_id(note_id)
            return {"success": True, "xml": self._to_llm_xml(note, template=template)}
        except Exception as e:
            return _err("get_note_as_xml", note_id, e)

    async def list_notes_for_user(self, user_id: str) -> dict[str, Any]:
        """Return all notes belonging to a user (owner = created_by), newest
        first — callers count-cap the list, so ordering decides WHICH rows survive."""
        try:
            notes = await self._get_items(order_by="-created_at", created_by=user_id, deleted_at__isnull=True)
            return {"success": True, "notes": [n.to_dict() for n in notes if n]}
        except Exception as e:
            return {
                "success": False,
                "operation": "list_notes_for_user",
                "user_id": user_id,
                "error": str(e),
            }

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    async def create_note(
        self,
        user_id: str,
        label: str,
        *,
        organization_id: str,
        content: str,
        folder_name: str = "",
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        is_public: bool = False,
    ) -> dict[str, Any]:
        """
        Create a new note.  Only explicit parameters are accepted so an LLM
        cannot accidentally pass immutable fields like id or created_at.

        ``user_id`` stamps the canonical owner column ``created_by``; the
        ``is_public`` affordance maps to ``published_to_web``, always written
        explicitly (never the table default).

        ``organization_id`` is required — workbench.notes.organization_id is NOT
        NULL and only a folder supplies one by trigger. The caller passes the
        organization its request carries (``ToolContext.organization_id``); it is
        never looked up or defaulted here.
        """
        if not organization_id:
            return {
                "success": False,
                "operation": "create_note",
                "error": "organization_id is required to create a note; none was carried.",
            }
        try:
            note = await self.create_notes(
                created_by=user_id,
                organization_id=organization_id,
                label=label,
                content=content,
                folder_name=folder_name,
                tags=tags or [],
                metadata=metadata or {},
                **publish_columns(is_public, user_id),
            )
            return _ok(note)
        except Exception as e:
            return {"success": False, "operation": "create_note", "error": str(e)}

    # ------------------------------------------------------------------
    # Update (full field replacement — strips immutable fields automatically)
    # ------------------------------------------------------------------

    async def update_note(
        self, note_id: str, *, actor_id: str | None = None, **updates: Any
    ) -> dict[str, Any]:
        """
        Update any combination of mutable fields on a note.

        Immutable fields (id, created_by, created_at, updated_at, version,
        sync_version, deleted_at, dto) are silently stripped so the LLM
        cannot accidentally corrupt them.

        Unknown fields are also stripped and reported in the response so
        the caller knows what was ignored.

        The ``is_public`` boolean affordance is translated to ``published_to_web``
        (+ its ``_at`` / ``_by`` stamps, ``actor_id`` = the acting person) —
        unless ``published_to_web`` was passed explicitly, which wins.
        """
        if "is_public" in updates and "published_to_web" not in updates:
            updates.update(publish_columns(bool(updates.pop("is_public")), actor_id))
        else:
            updates.pop("is_public", None)

        safe = {k: v for k, v in updates.items() if k in _MUTABLE_FIELDS}
        stripped_immutable = [k for k in updates if k in _IMMUTABLE_FIELDS]
        unknown = [k for k in updates if k not in _MUTABLE_FIELDS and k not in _IMMUTABLE_FIELDS]

        if not safe:
            return {
                "success": False,
                "operation": "update_note",
                "note_id": note_id,
                "error": "No mutable fields provided.",
                "stripped_immutable": stripped_immutable,
                "unknown_fields": unknown,
            }

        note, error = await self._write_visible(
            "update_note",
            note_id,
            safe,
            stripped_immutable=stripped_immutable,
            unknown_fields=unknown,
        )
        if error is not None:
            return error
        result = _ok(note)
        if stripped_immutable:
            result["warning_stripped_immutable"] = stripped_immutable
        if unknown:
            result["warning_unknown_fields"] = unknown
        return result

    # ------------------------------------------------------------------
    # Convenience single-field updaters (LLM tools often prefer these)
    # ------------------------------------------------------------------

    async def update_note_content(self, note_id: str, content: str) -> dict[str, Any]:
        """Replace the entire content of a note."""
        return await self.update_note(note_id, content=content)

    async def update_note_label(self, note_id: str, label: str) -> dict[str, Any]:
        """Rename a note."""
        return await self.update_note(note_id, label=label)

    async def update_note_tags(self, note_id: str, tags: list[str]) -> dict[str, Any]:
        """Replace the tag list on a note."""
        return await self.update_note(note_id, tags=tags)

    async def move_note_to_folder(self, note_id: str, folder_name: str) -> dict[str, Any]:
        """Move a note to a different folder."""
        return await self.update_note(note_id, folder_name=folder_name)

    # ------------------------------------------------------------------
    # Patch (fuzzy find-and-replace inside content)
    # ------------------------------------------------------------------

    async def patch_note_content(
        self,
        note_id: str,
        search_text: str,
        replacement_text: str,
    ) -> dict[str, Any]:
        """
        Find `search_text` inside the note's content and replace it with
        `replacement_text`.  Uses fuzzy matching across four levels:

          1. Exact match
          2. Whitespace-normalized
          3. Blank-lines-stripped
          4. Lenient  (unicode/punctuation normalized, case-insensitive)

        Returns a structured error if no level produces a match.
        """
        try:
            note = await self._read_live(note_id)
        except Exception as e:
            return _err("patch_note_content", note_id, e)
        if note is None:
            return _not_visible("patch_note_content", note_id)

        try:
            patch_result = apply_patch(
                content=note.content,
                search_text=search_text,
                replacement_text=replacement_text,
                note_id=note_id,
            )
        except PatchError as pe:
            return {"success": False, **pe.to_dict()}

        updated_note, error = await self._write_row(
            "patch_note_content",
            note,
            {"content": patch_result.new_content},
            matched_at_pass=patch_result.matched_at.value,
        )
        if error is not None:
            return error
        return {
            "success": True,
            "matched_at_pass": patch_result.matched_at.value,
            "original_snippet": patch_result.original_snippet,
            "note": updated_note.to_dict(),
        }

    # ------------------------------------------------------------------
    # Append / prepend helpers (common LLM operations)
    # ------------------------------------------------------------------

    async def append_to_note(
        self, note_id: str, text: str, separator: str = "\n\n"
    ) -> dict[str, Any]:
        """Add text to the end of a note's content."""
        try:
            note = await self.load_notes_by_id(note_id)
            new_content = note.content.rstrip() + separator + text
            updated = await self.update_notes(note_id, content=new_content)
            return _ok(updated)
        except Exception as e:
            return _err("append_to_note", note_id, e)

    async def prepend_to_note(
        self, note_id: str, text: str, separator: str = "\n\n"
    ) -> dict[str, Any]:
        """Add text to the beginning of a note's content."""
        try:
            note = await self.load_notes_by_id(note_id)
            new_content = text + separator + note.content.lstrip()
            updated = await self.update_notes(note_id, content=new_content)
            return _ok(updated)
        except Exception as e:
            return _err("prepend_to_note", note_id, e)

    # ------------------------------------------------------------------
    # Delete
    # ------------------------------------------------------------------

    async def delete_note(self, note_id: str) -> dict[str, Any]:
        """ARCHIVE a note (sets ``deleted_at``; the row and its history survive).

        Arman's law: soft-delete everything important — an agent never destroys a
        person's note. There is deliberately no hard-delete path on this manager.
        """
        try:
            from matrx_ai.tools.soft_delete import archive_where

            if await self._read_live(note_id) is None:
                return _not_visible("delete_note", note_id)
            archived = await archive_where(Notes, {"id": note_id})
        except Exception as e:
            if any(marker in str(e) for marker in _RLS_REFUSAL_MARKERS):
                return _no_write_access("delete_note", note_id)
            return _err("delete_note", note_id, e)
        if archived == 0:
            # The caller could see the live note, and RLS let no row change.
            return _no_write_access("delete_note", note_id)
        return {"success": True, "note_id": note_id, "archived": True}

    # ------------------------------------------------------------------
    # XML rendering (internal)
    # ------------------------------------------------------------------

    async def load_note_as_llm_xml(self, note_id: str, template: str = DEFAULT_XML_TEMPLATE) -> str:
        note = await self.load_notes_by_id(note_id)
        return self._to_llm_xml(note, template=template)

    def _to_llm_xml(self, note: Notes, template: str = DEFAULT_XML_TEMPLATE) -> str:
        tmpl = _XML_TEMPLATES.get(template, XML_TEMPLATE_FULL)
        content = textwrap.indent(note.content.strip(), "    ")
        return tmpl.format(
            id=note.id,
            label=note.label,
            folder_name=getattr(note, "folder_name", ""),
            content=content,
        )


notes_manager_instance = NotesManager()
