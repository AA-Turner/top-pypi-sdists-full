from __future__ import annotations

import textwrap
from typing import Any

from matrx_ai.db._registry import get_base, get_model

NotesBase = get_base("NotesBase")
Notes = get_model("Notes")

from matrx_ai.db.content_types.patch_utils import PatchError, apply_patch

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

# Fields the LLM is allowed to set/update. ``visibility`` is the canonical
# replacement for the dropped ``is_public`` boolean (enum: 'public' is public,
# default 'internal'); the ``is_public`` create/update affordance is translated
# to it in this module so the agent-facing tool contract stays stable.
_MUTABLE_FIELDS = frozenset(
    {
        "label",
        "content",
        "folder_name",
        "tags",
        "metadata",
        "visibility",
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
    # Read
    # ------------------------------------------------------------------

    async def get_note(self, note_id: str) -> dict[str, Any]:
        """Return the full note dict, or a structured error."""
        try:
            note = await self.load_notes_by_id(note_id)
            return _ok(note)
        except Exception as e:
            return _err("get_note", note_id, e)

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
            notes = await self._get_items(order_by="-created_at", created_by=user_id)
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
        ``is_public`` affordance maps to ``visibility`` ('public' vs the
        default 'internal').
        """
        try:
            note = await self.create_notes(
                created_by=user_id,
                label=label,
                content=content,
                folder_name=folder_name,
                tags=tags or [],
                metadata=metadata or {},
                visibility="public" if is_public else "internal",
            )
            return _ok(note)
        except Exception as e:
            return {"success": False, "operation": "create_note", "error": str(e)}

    # ------------------------------------------------------------------
    # Update (full field replacement — strips immutable fields automatically)
    # ------------------------------------------------------------------

    async def update_note(self, note_id: str, **updates: Any) -> dict[str, Any]:
        """
        Update any combination of mutable fields on a note.

        Immutable fields (id, created_by, created_at, updated_at, version,
        sync_version, deleted_at, dto) are silently stripped so the LLM
        cannot accidentally corrupt them.

        Unknown fields are also stripped and reported in the response so
        the caller knows what was ignored.

        The legacy ``is_public`` boolean affordance is translated to the
        canonical ``visibility`` enum ('public' when true, 'internal' when
        false) — unless ``visibility`` was passed explicitly, which wins.
        """
        if "is_public" in updates and "visibility" not in updates:
            updates["visibility"] = "public" if updates.pop("is_public") else "internal"
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

        try:
            note = await self.update_notes(note_id, **safe)
            result = _ok(note)
            if stripped_immutable:
                result["warning_stripped_immutable"] = stripped_immutable
            if unknown:
                result["warning_unknown_fields"] = unknown
            return result
        except Exception as e:
            return _err(
                "update_note",
                note_id,
                e,
                stripped_immutable=stripped_immutable,
                unknown_fields=unknown,
            )

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
            note = await self.load_notes_by_id(note_id)
        except Exception as e:
            return _err("patch_note_content", note_id, e)

        try:
            patch_result = apply_patch(
                content=note.content,
                search_text=search_text,
                replacement_text=replacement_text,
                note_id=note_id,
            )
        except PatchError as pe:
            return {"success": False, **pe.to_dict()}

        try:
            updated_note = await self.update_notes(note_id, content=patch_result.new_content)
            return {
                "success": True,
                "matched_at_pass": patch_result.matched_at.value,
                "original_snippet": patch_result.original_snippet,
                "note": updated_note.to_dict(),
            }
        except Exception as e:
            return _err(
                "patch_note_content", note_id, e, matched_at_pass=patch_result.matched_at.value
            )

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
        """Permanently delete a note."""
        try:
            success = await self.delete_notes(note_id)
            return {"success": success, "note_id": note_id}
        except Exception as e:
            return _err("delete_note", note_id, e)

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
