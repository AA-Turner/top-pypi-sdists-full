"""the --add-tag/--remove-tag/--set-tags flow every noun's tag and set verbs share."""

from __future__ import annotations
from typing import Any

import typer
from ...sdk.values.tags import canonical_tags


def _apply_tag_ops(
    current: list[str],
    add: list[str],
    remove: list[str],
    replace: list[str] | None,
) -> list[str]:
    """Compute a ``tag`` verb's replacement list (read-modify-write over the
    server's whole-list-replace PATCH, CONTRACT.md "tags"). ``--set`` wins
    outright; otherwise positional adds append (canonical, deduped) and
    ``--remove`` drops. The same tag in add AND remove is a caller bug — error,
    never a silent tie-break."""
    if replace is not None:
        if add or remove:
            raise typer.BadParameter("--set replaces outright; don't combine it with adds/--remove")
        return canonical_tags(replace)
    add_c = canonical_tags(add)
    remove_c = set(canonical_tags(remove))
    both = [t for t in add_c if t in remove_c]
    if both:
        raise typer.BadParameter(f"tag(s) both added and removed: {', '.join(both)}")
    out = [t for t in canonical_tags(current) if t not in remove_c]
    out.extend(t for t in add_c if t not in out)
    return out


def _tag_flags_given(add, remove, replace) -> bool:
    """Did a `set` verb get any of --add-tag/--remove-tag/--set-tags?"""
    return bool(add) or bool(remove) or replace is not None


def _set_verb_tags(current, add, remove, replace) -> tuple[list[str], bool]:
    """The tag list a `set` verb sends beside its other fields, and whether it
    differs from the stored one -- the `tag` verb's arithmetic, one write.

    The list goes in the body whenever a tag flag was given, changed or not:
    a retried command (the daemon's Idempotency-Key) then sends the same body
    it sent the first time and replays instead of being refused as a
    different request."""
    if replace is not None and (add or remove):
        raise typer.BadParameter(
            "--set-tags replaces the whole list; don't combine it with --add-tag/--remove-tag"
        )
    stored = list(current or [])
    wanted = _apply_tag_ops(stored, add or [], remove or [], replace)
    return wanted, wanted != stored


def _tag_verb_flow(entity_id, current, add, remove, replace, write) -> dict:
    """Shared flow for the three ``tag`` verbs: bare invocation lists, anything
    else is read-modify-write. The changed-check compares against the RAW
    stored list (not its canonical form) so re-tagging a pre-0066 row with its
    own canonical name still writes once and heals the stored form; the write
    callbacks verify the server actually persisted tags (0066 guard)."""
    current = list(current or [])
    if not add and not remove and replace is None:
        return {"id": entity_id, "tags": current}
    wanted = _apply_tag_ops(current, add or [], remove or [], replace)
    if wanted == current:
        return {"id": entity_id, "tags": current}
    result = write(wanted) or {}
    return {"id": result.get("id", entity_id), "tags": result.get("tags", wanted)}


#: Tag changes on a `set` verb: the `tag` verb's add / --remove / --set, spelled
#: so they cannot be mistaken for the other fields `set` takes. They ride in the
#: SAME PATCH as those fields, so an edit that renames and retags is one write
#: that cannot land half.
def add_tag_opt() -> Any:
    return typer.Option(None, "--add-tag", help="add a tag (repeatable)")


def remove_tag_opt() -> Any:
    return typer.Option(None, "--remove-tag", help="remove a tag (repeatable)")


def set_tags_opt() -> Any:
    return typer.Option(
        None, "--set-tags", help="replace the whole tag list (repeatable; --set-tags '' clears)"
    )
