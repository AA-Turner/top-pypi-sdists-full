"""One line that says whether a kind is FINISHED — read from the database, never remembered.

A kind made for a table's rows is three things: the kind, its output component, and the table
showing its rows as it (``custom.table_kind_set``, the ``tables_shape`` action ``show_rows_as``).
A kind with only the first part is a dead end: the records still draw as the plain table card
(2026-11-03, a grooming business's ``grooming_appointment_card``). ``kind_create``, ``kind_get``
and every ``kindcomp_*`` write end with this line, naming what is still missing and the next
call. It never refuses anything (Law 6: validation offers, never blocks).

Tables come from the host (``KIND_TABLES_EXT_KEY``: every table the asking person can see in
the request's organization, each with the kind its rows show as — aidream registers
matrx-records' reader). matrx-ai never imports matrx-records. A host without it, or a read that
fails, says so in the line — never a silent "no table".
"""

from __future__ import annotations

import re
from typing import Any

from matrx_ai.db._registry import get_model as get_db_model

#: Host seam: ``async () -> list[{"table_id", "name", "kind"}]`` as the asking person.
KIND_TABLES_EXT_KEY = "kind_tables_with_kinds"

GENERIC_INPUT_KEY = "generic_structured"

# Words that name a shape's form, not its subject: "grooming_appointment_card" is about
# grooming appointments, so the Grooming Appointments table is its likely home.
_FORM_WORDS = frozenset(
    {"card", "cards", "item", "items", "entry", "entries", "row", "rows", "record", "records",
     "view", "summary", "detail", "details", "list", "tile", "block", "kind", "shape"}
)


def _words(text: str) -> set[str]:
    out: set[str] = set()
    for w in re.split(r"[^a-z0-9]+", (text or "").lower()):
        if len(w) < 3 or w in _FORM_WORDS or re.fullmatch(r"v\d+", w):
            continue
        out.add(w[:-1] if w.endswith("s") and len(w) > 4 else w)
    return out


def looks_like_home(kind_slug: str, table_name: str) -> bool:
    """More than half of the kind's subject words are words of the table's name."""
    kind_words = _words(kind_slug)
    if not kind_words:
        return False
    overlap = len(kind_words & _words(table_name))
    return overlap * 2 > len(kind_words)


def _overlap(kind_slug: str, table_name: str) -> int:
    return len(_words(kind_slug) & _words(table_name))


async def _output_components(kind_definition_id: str) -> list[Any]:
    KindComponent = get_db_model("KindComponent")
    rows = await KindComponent.filter(kind_definition_id=kind_definition_id).all()
    return [
        c
        for c in rows
        if getattr(c, "deleted_at", None) is None
        and getattr(c, "is_active", True)
        and getattr(c, "role", "output") == "output"
        and getattr(c, "component_key", "") != GENERIC_INPUT_KEY
    ]


async def _tables() -> tuple[list[dict[str, Any]] | None, str | None]:
    from matrx_ai._ext import get_ext, has_ext

    if not has_ext(KIND_TABLES_EXT_KEY):
        return None, "this server cannot read tables here"
    try:
        return list(await get_ext(KIND_TABLES_EXT_KEY)() or []), None
    except Exception as exc:  # noqa: BLE001 — the line reports it; the tool's own answer stands
        return None, f"the tables could not be read: {exc}"


async def kind_completeness(kd: Any) -> str:
    """The completeness line for one kind row (needs ``id`` and ``kind``)."""
    slug = str(getattr(kd, "kind", "") or "")
    try:
        components = await _output_components(str(kd.id))
        component_part: str | None = None
    except Exception as exc:  # noqa: BLE001
        components, component_part = [], f"component: unknown ({exc})"
    default = next((c for c in components if getattr(c, "is_default", False)), None) or (
        components[0] if components else None
    )
    missing: list[str] = []
    unbound_note = False
    if component_part is None:
        if default is not None:
            component_part = f"component '{default.component_key}' draws it"
        else:
            component_part = (
                "NO component yet, so it draws as the plain card "
                f"(next: kindcomp_create_component kind='{slug}')"
            )
            missing.append("component")

    tables, why = await _tables()
    if tables is None:
        table_part = f"table binding: unknown ({why})"
    else:
        bound = [t for t in tables if str(t.get("kind") or "") == slug]
        homes = [
            t for t in tables
            if not t.get("kind") and looks_like_home(slug, str(t.get("name") or ""))
        ][:3]
        if bound:
            table_part = "shown by " + ", ".join(f"table '{t.get('name')}'" for t in bound[:5])
        elif homes:
            names = ", ".join(f"'{t.get('name')}' (table_id={t.get('table_id')})" for t in homes)
            table_part = (
                f"NO table shows its rows as this kind yet; {names} looks like its home, and its "
                "records still draw as the plain table card (next: tables_shape "
                f"action='show_rows_as' table_id=<that table> kind='{slug}' "
                "fields={<kind field>: <column key>})"
            )
            missing.append("table binding")
        else:
            unbound = sorted(
                (t for t in tables if not t.get("kind")),
                key=lambda t: -_overlap(slug, str(t.get("name") or "")),
            )[:5]
            listing = ""
            if unbound:
                listing = " Tables with no kind yet (best word match first): " + ", ".join(
                    f"'{t.get('name')}' (table_id={t.get('table_id')}"
                    + (", shares words with the kind" if _overlap(slug, str(t.get("name") or "")) else "")
                    + ")"
                    for t in unbound
                ) + "."
            table_part = (
                "no table shows its rows as this kind — if this kind draws a table's rows, bind it with "
                f"tables_shape action='show_rows_as' kind='{slug}'.{listing}"
            )
            unbound_note = True

    if missing:
        head = "Completeness: INCOMPLETE (missing " + " and ".join(missing) + ")"
        tail = (
            " A kind for a table is one step with three parts — kind, component, table binding — "
            "finished when a read-back shows the card draws."
        )
    elif unbound_note or tables is None:
        # A component with no table binding is NOT finished: only a kind clearly not for a table's rows
        # is done without one, and that is for the person to say (Law 6), not for this line to assume.
        head = "Completeness: component ready; no table shows its rows as this kind"
        tail = " Finished = kind_get names the bound table and page_check shows the card."
    else:
        head = "Completeness: complete"
        tail = " Confirm the card draws with page_check on the page that shows it."
    return f"{head} — {component_part}; {table_part}.{tail}"


async def kind_completeness_by_id(kind_definition_id: str) -> str | None:
    KindDefinition = get_db_model("KindDefinition")
    rows = await KindDefinition.filter(id=kind_definition_id).all()
    return await kind_completeness(rows[0]) if rows else None


async def component_kind_completeness(component_id: str) -> str | None:
    KindComponent = get_db_model("KindComponent")
    comp = await KindComponent.get_or_none(use_cache=False, id=component_id)
    if comp is None:
        return None
    return await kind_completeness_by_id(str(comp.kind_definition_id))


__all__ = [
    "KIND_TABLES_EXT_KEY",
    "component_kind_completeness",
    "kind_completeness",
    "kind_completeness_by_id",
    "looks_like_home",
]
