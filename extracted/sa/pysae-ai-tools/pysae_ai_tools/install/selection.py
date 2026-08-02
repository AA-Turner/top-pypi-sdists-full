"""Interactive tool-selection logic for the meta-installer.

The first-run / re-configure checklist: which tools are pre-checked, how
newly-added tools (since the last saved selection) are surfaced as ``NEW``,
and the grouped-by-category prompt itself.
"""

from .registry import CATEGORY_ORDER, TOOLS, Mode, Tool, _tools_by_category
from .render import CATEGORY_HEADER, CATEGORY_ICON


def _checklist_label(tool: Tool) -> str:
    """Compose the dim-grey suffix shown next to each item in the checklist.

    The ``(NEW)`` marker is *not* part of this label — it's rendered
    separately (red + bold) via :attr:`Item.is_new` for visibility.
    """
    parts: list[str] = []
    if tool.description:
        parts.append(tool.description)
    if tool.mode is Mode.REQUIRED:
        parts.append("(required)")
    return " ".join(parts)


def _effective_known(initial: list[str] | None, known: list[str] | None) -> list[str] | None:
    """Resolve ``tools_known_at_save`` with a sensible legacy fallback.

    Pre-snapshot users only persisted ``tools_to_install`` — they're missing
    the ``tools_known_at_save`` snapshot introduced afterwards. To avoid
    flagging zero new tools forever for those users, treat the saved
    selection as the implicit snapshot: tools currently in ``TOOLS`` but
    absent from it are surfaced as NEW. This may falsely flag tools the
    user had explicitly deselected as NEW once, but the alternative
    (silently auto-extending or hiding new tools) is worse.
    """
    if known is not None:
        return known
    if initial is not None:
        return list(initial)
    return None


def _initial_selected_set(initial: list[str] | None, known: list[str] | None) -> set[str]:
    """Compute the pre-checked set for the configure checklist.

    Logic per tool:

    - REQUIRED → always checked (locked elsewhere).
    - First-time configure (``initial is None``) → use ``default_selected``.
    - Tool present in saved selection → checked (explicit yes).
    - Tool absent from saved selection but present in ``known`` (was visible
      at last save) → unchecked (explicit no).
    - Tool absent from both → **new tool** added in a newer version of the
      package: fall back to ``default_selected`` rather than silently
      treating it as deselected.
    """
    if initial is None:
        return {t.name for t in TOOLS if t.default_selected}

    saved = set(initial)
    effective_known = _effective_known(initial, known)
    known_set: set[str] | None = set(effective_known) if effective_known is not None else None

    selected: set[str] = set()
    for t in TOOLS:
        if t.name in saved:
            selected.add(t.name)
            continue
        if known_set is not None and t.name not in known_set and t.default_selected:
            selected.add(t.name)
    return selected


def _prompt_tool_selection(
    initial: list[str] | None,
    known: list[str] | None,
) -> list[str] | None:
    """Show the interactive checklist, grouped by category. Returns the
    chosen names, or ``None`` if the prompt cannot run.

    ``initial`` is the previously-saved selection (None → first run).
    ``known`` is the snapshot of tools that existed at that save — used
    to identify newly-added tools and apply their ``default_selected``.
    """
    from .common.checklist import Item
    from .common.checklist import prompt as checklist_prompt

    initial_set = _initial_selected_set(initial, known)
    grouped = _tools_by_category()
    effective_known = _effective_known(initial, known)
    new_tools: set[str] = (
        {t.name for t in TOOLS if t.name not in effective_known} if effective_known is not None else set()
    )

    items: list[Item] = []
    for cat in CATEGORY_ORDER:
        bucket = grouped.get(cat) or []
        if not bucket:
            continue
        section_label = f"{CATEGORY_ICON[cat]} {CATEGORY_HEADER[cat]}"
        for idx, t in enumerate(bucket):
            items.append(
                Item(
                    name=t.name,
                    label=_checklist_label(t),
                    selected=t.name in initial_set or t.mode is Mode.REQUIRED,
                    locked=t.mode is Mode.REQUIRED,
                    is_new=t.name in new_tools,
                    # Section header rendered just above the first item of each group.
                    header_above=section_label if idx == 0 else "",
                )
            )

    result = checklist_prompt(items, header="  Sélectionne les outils à installer :")
    if result is None:
        return None
    return [it.name for it in result if it.selected]
