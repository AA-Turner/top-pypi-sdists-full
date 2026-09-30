"""Structured lists (picklists) AS THE PERSON — the one service every door uses.

RLS OWNS ACCESS (chair ruling 2026-09-27). Every read and write of
``workbench.udt_structured_lists`` / ``workbench.udt_structured_list_items`` here runs
inside the caller's RLS session (``matrx_ai.tools.person_session.as_the_person`` →
host ``acting_as_caller`` → ``rls_session``), through the registered ORM models. The
tables' policies and governance trigger decide: a list or choice RLS hides reads as
absent; a visible one the database will not change answers ``no_access``. No owner
comparison and no ``user_id = caller`` filter decides access anywhere in this module —
the only ``user_id`` filter left is the "my lists" LIST scope, which never gates a
record.

Consumers: the ``picklist`` agent tool (matrx-ai) and aidream's ``/picklists`` router.

TWO HOMES, ONE SERVICE. A list that moved to the record store (its organization switched
its Data tables) is read and changed through the host's record-store arm — the same
``picklist_store_arm`` the tool's writes already use (matrx_records ``PicklistStoreArm``:
``custom.pick_list_index_everywhere`` + ``RecordStore.record_query`` / ``record_propose`` /
``record_delete``, all in the person's seat), so the STORE decides what the person may see
and change. The live views are server-lane only and are never read on anyone's behalf.

Answers are small words, so each door phrases its own refusal:
``updated`` / ``archived`` · ``not_found`` (hidden or missing) · ``no_access``
(visible, refused) · ``nothing`` (no writable value given).
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from matrx_utils.row_access import publish_columns

from matrx_ai.db._registry import get_model

#: Choice columns a person may set.
WRITABLE_CHOICE_COLUMNS = (
    "label", "description", "help_text", "group_name", "is_public", "public_read", "icon_name",
)
#: List columns a person may set (the API calls ``list_name`` "name").
WRITABLE_LIST_COLUMNS = ("list_name", "description", "is_public", "public_read")

_RLS_REFUSAL_MARKERS = ("row-level security", "permission denied", "42501")

_LIST_FIELDS = (
    "id", "list_name", "description", "user_id", "organization_id", "is_public",
    "public_read", "created_at", "updated_at",
)
_CHOICE_FIELDS = ("id", "label", "description", "help_text", "group_name", "icon_name")


def _lists() -> Any:
    return get_model("UdtStructuredLists")


def _choices() -> Any:
    return get_model("UdtStructuredListItems")


def _refused(exc: Exception) -> bool:
    return any(marker in str(exc) for marker in _RLS_REFUSAL_MARKERS)


def _row(obj: Any, fields: tuple[str, ...]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name in fields:
        value = getattr(obj, name, None)
        if hasattr(value, "isoformat"):
            value = value.isoformat()  # JSON-safe, the shape the named queries returned
        out[name] = str(value) if name.endswith("id") and value is not None else value
    return out


def _store_arm() -> Any | None:
    """The host's record-store arm for lists, or None on a host without a record store."""
    from matrx_ai._ext import get_ext, has_ext

    return get_ext("picklist_store_arm") if has_ext("picklist_store_arm") else None


async def _store_list(list_id: str) -> dict[str, Any] | None:
    arm = _store_arm()
    if arm is None or not hasattr(arm, "read_list"):
        return None
    return await arm.read_list(str(list_id))


def _person(app_ctx: Any = None):
    from matrx_ai.tools.person_session import as_the_person

    return as_the_person(app_ctx)


# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------


async def list_open_to_person(list_id: str, *, store_arm: Any = None, app_ctx: Any = None) -> str:
    """``visible`` / ``hidden`` / ``in_store`` for ``list_id``, decided by the database.

    ``in_store``: the older row does not answer and the record-store arm (in the
    person's seat) says the id lives there — a door that cannot read the store as the
    person says so honestly instead of reading it privileged.
    """
    async with _person(app_ctx):
        row = await _lists().get_or_none(use_cache=False, id=str(list_id))
    if row is not None and getattr(row, "deleted_at", None) is None:
        return "visible"
    if store_arm is not None:
        try:
            if await store_arm.list_lives_in(str(list_id)) == "record":
                return "in_store"
        except Exception:  # noqa: BLE001 — an unanswered home is not a visible list
            return "hidden"
    return "hidden"


async def read_list_as_the_person(list_id: str, *, app_ctx: Any = None) -> dict[str, Any] | None:
    """The list and its live choices as the person sees them, or None (hidden/missing)."""
    async with _person(app_ctx):
        row = await _lists().get_or_none(use_cache=False, id=str(list_id))
        items = (
            await _choices().filter(list_id=str(list_id), deleted_at__isnull=True).all()
            if row is not None and getattr(row, "deleted_at", None) is None
            else None
        )
    if items is None:
        # Not an older list this person can see: ask the record store, as the person.
        return await _store_list(list_id)
    choices = sorted(
        (_row(i, (*_CHOICE_FIELDS, "created_at")) for i in items),
        key=lambda c: (c.get("group_name") or "", str(c.get("created_at") or "")),
    )
    listing = _row(row, _LIST_FIELDS)
    listing["item_count"] = len(choices)
    listing["items"] = [{k: c[k] for k in _CHOICE_FIELDS} for c in choices]
    return listing


async def read_choice_as_the_person(
    list_id: str, item_id: str, *, app_ctx: Any = None
) -> dict[str, Any] | None:
    """One live choice of ``list_id`` as the person sees it, or None."""
    async with _person(app_ctx):
        row = await _choices().get_or_none(use_cache=False, id=str(item_id))
    if (
        row is not None
        and getattr(row, "deleted_at", None) is None
        and str(getattr(row, "list_id", "")) == str(list_id)
    ):
        return _row(row, _CHOICE_FIELDS)
    listing = await _store_list(list_id)
    for choice in (listing or {}).get("items") or []:
        if str(choice.get("id")) == str(item_id):
            return choice
    return None


async def lists_for_person(
    user_id: str, *, search: str | None = None, limit: int = 50, offset: int = 0, app_ctx: Any = None
) -> list[dict[str, Any]]:
    """The person's own live lists ("my lists" scope), each with its live choice count.

    Read in the person's session; the ``user_id`` filter is the LIST scope only.
    """
    async with _person(app_ctx):
        rows = await _lists().filter(user_id=str(user_id), deleted_at__isnull=True).all()
        out = []
        for r in rows:
            name = (getattr(r, "list_name", "") or "").lower()
            desc = (getattr(r, "description", "") or "").lower()
            if search and search.lower() not in name and search.lower() not in desc:
                continue
            listing = _row(r, _LIST_FIELDS)
            listing["item_count"] = len(
                await _choices().filter(list_id=str(r.id), deleted_at__isnull=True).all()
            )
            out.append(listing)
    arm = _store_arm()
    if arm is not None and hasattr(arm, "list_index"):
        seen = {str(r["id"]) for r in out}
        for r in await arm.list_index():
            if r.get("lives_in") != "record" or str(r.get("id")) in seen:
                continue
            if str(r.get("created_by") or "") != str(user_id):
                continue  # the "my lists" scope, the same one the older half keeps
            name = (r.get("list_name") or "").lower()
            desc = (r.get("description") or "").lower()
            if search and search.lower() not in name and search.lower() not in desc:
                continue
            out.append({
                "id": str(r["id"]), "list_name": r.get("list_name"),
                "description": r.get("description"), "user_id": str(r.get("created_by")),
                "organization_id": str(r.get("organization_id") or "") or None,
                "is_public": False, "public_read": False, "created_at": None,
                "updated_at": r.get("updated_at"), "item_count": int(r.get("item_count") or 0),
            })
    out.sort(key=lambda r: str(r.get("updated_at") or r.get("created_at") or ""), reverse=True)
    return out[offset : offset + limit]


def grouped_choices(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Choices grouped by ``group_name`` — the shape the grouped query used to answer."""
    groups: dict[str | None, list[dict[str, Any]]] = {}
    for item in items:
        groups.setdefault(item.get("group_name"), []).append(
            {k: item.get(k) for k in ("id", "label", "description", "help_text", "icon_name")}
        )
    return [
        {"group_name": name, "items": sorted(members, key=lambda m: m.get("label") or "")}
        for name, members in sorted(groups.items(), key=lambda kv: kv[0] or "")
    ]


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------


async def _update_as_the_person(model: Any, where: dict[str, Any], values: dict[str, Any],
                                row_id: str, app_ctx: Any) -> str:
    async with _person(app_ctx):
        try:
            result = await model.update_where({**where, "deleted_at__isnull": True}, **values)
        except Exception as exc:
            if _refused(exc):
                return "no_access"
            raise
        if int(getattr(result, "rows_affected", 0) or 0):
            return "updated"
        seen = await model.get_or_none(use_cache=False, id=str(row_id))
    return "no_access" if seen is not None and getattr(seen, "deleted_at", None) is None else "not_found"


async def update_choice_as_the_person(
    item_id: str, fields: dict[str, Any], *, list_id: str | None = None, app_ctx: Any = None
) -> str:
    """Change one choice; ``workbench.udt_structured_list_items``' UPDATE policy decides.

    With ``list_id`` and a list that lives in the record store, the change goes through the
    store arm as the person (``record_propose`` — the organization's approval setting
    applies; ``waiting`` when it waits for a person).
    """
    values = {k: v for k, v in fields.items() if k in WRITABLE_CHOICE_COLUMNS and v is not None}
    if not values:
        return "nothing"
    answer = await _update_as_the_person(_choices(), {"id": str(item_id)}, values, str(item_id), app_ctx)
    if answer != "not_found" or list_id is None:
        return answer
    return await _in_store(list_id, item_id, lambda arm: arm.update_choice(str(item_id), values))


async def _in_store(list_id: str, item_id: str, change: Any) -> str:
    """Run a change on a record-store choice, as the person, after the store says they see it."""
    listing = await _store_list(list_id)
    if listing is None or not any(str(c.get("id")) == str(item_id) for c in listing["items"]):
        return "not_found"
    try:
        await change(_store_arm())
    except Exception as exc:
        name = type(exc).__name__
        if name == "ChangeWaits":
            return "waiting"
        if name == "StoreRefusal" or _refused(exc):
            return "no_access"
        raise
    return "updated"


async def update_list_as_the_person(list_id: str, fields: dict[str, Any], *, app_ctx: Any = None) -> str:
    """Change a list's own columns; the list's UPDATE policy decides."""
    values = {k: v for k, v in fields.items() if k in WRITABLE_LIST_COLUMNS and v is not None}
    if not values:
        return "nothing"
    return await _update_as_the_person(_lists(), {"id": str(list_id)}, values, str(list_id), app_ctx)


async def archive_list_as_the_person(list_id: str, *, app_ctx: Any = None) -> str:
    """Archive (soft-delete) a list; trashing is admin-level and the governance trigger decides."""
    answer = await _update_as_the_person(
        _lists(), {"id": str(list_id)}, {"deleted_at": datetime.now(UTC)}, str(list_id), app_ctx
    )
    return "archived" if answer == "updated" else answer


async def archive_choice_as_the_person(
    item_id: str, *, list_id: str | None = None, app_ctx: Any = None
) -> str:
    answer = await _update_as_the_person(
        _choices(), {"id": str(item_id)}, {"deleted_at": datetime.now(UTC)}, str(item_id), app_ctx
    )
    if answer == "not_found" and list_id is not None:
        answer = await _in_store(
            list_id, item_id, lambda arm: arm.archive_choice(str(list_id), str(item_id))
        )
    return "archived" if answer == "updated" else answer


async def lives_in_store(list_id: str) -> bool:
    """True when this person sees ``list_id`` as a record-store list (a list-level change to it
    — rename, archive, add choices — is made on the Lists page, not here)."""
    return await _store_list(list_id) is not None


async def archive_all_choices_as_the_person(list_id: str, *, app_ctx: Any = None) -> int:
    """Archive every live choice of ``list_id`` the person may change; returns how many."""
    async with _person(app_ctx):
        result = await _choices().update_where(
            {"list_id": str(list_id), "deleted_at__isnull": True}, deleted_at=datetime.now(UTC)
        )
    return int(getattr(result, "rows_affected", 0) or 0)


async def add_choices_as_the_person(
    list_id: str, items: list[dict[str, Any]], *, user_id: str, organization_id: str, app_ctx: Any = None
) -> list[str] | str:
    """Add choices to a list; the items table's INSERT policy (editor on the list) decides.

    Returns the new ids, or ``no_access`` when the database refused.
    """
    ids: list[str] = []
    async with _person(app_ctx):
        try:
            for item in items:
                values = {k: v for k, v in item.items() if k in WRITABLE_CHOICE_COLUMNS and v is not None}
                created = await _choices().create_item(
                    list_id=str(list_id),
                    user_id=str(user_id),
                    created_by=str(user_id),
                    organization_id=str(organization_id),
                    **values,
                )
                ids.append(str(created.id))
        except Exception as exc:
            if _refused(exc):
                return "no_access"
            raise
    return ids


async def create_list_as_the_person(
    *,
    user_id: str,
    organization_id: str,
    list_name: str,
    description: str | None = None,
    is_public: bool = False,
    public_read: bool = False,
    items: list[dict[str, Any]] | None = None,
    app_ctx: Any = None,
) -> str:
    """Create a list (and its first choices) as the person; the INSERT policies decide.

    Born not published to the web (written explicitly, never the table default); the
    type's ``shown_to`` knob decides who sees it in lists.
    Returns the new list id; a refusal raises ``PermissionError`` naming the organization.
    """
    async with _person(app_ctx):
        try:
            created = await _lists().create_item(
                list_name=list_name,
                description=description,
                user_id=str(user_id),
                created_by=str(user_id),
                organization_id=str(organization_id),
                is_public=is_public,
                public_read=public_read,
                **publish_columns(False, str(user_id)),
            )
            for item in items or []:
                values = {k: v for k, v in item.items() if k in WRITABLE_CHOICE_COLUMNS and v is not None}
                await _choices().create_item(
                    list_id=str(created.id),
                    user_id=str(user_id),
                    created_by=str(user_id),
                    organization_id=str(organization_id),
                    **values,
                )
        except Exception as exc:
            if _refused(exc):
                raise PermissionError(
                    f"You may not create a list in organization {organization_id}; nothing was created."
                ) from exc
            raise
    return str(created.id)
