"""the project a folder imports into: a named slug/id or one derived from the folder."""

from __future__ import annotations
from pathlib import Path

from .....sdk.errors import NotFoundError


def slug_for(folder: Path) -> str:
    """A project slug derived from the folder name, deterministically.

    Derived rather than asked because the same folder must resolve to the same
    project on a re-run. A prompt would let a typo fork the identity, which is
    the one failure this flow cannot recover from.
    """
    raw = folder.resolve().name.lower()
    cleaned = "".join(ch if ch.isalnum() else "-" for ch in raw).strip("-")
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned or "backfill"


def resolve_anchor(client, folder: Path, *, requested: str | None = None) -> tuple[str, str]:
    """The project this folder imports into, as ``(project_id, slug)``.

    Returns the UUID, never the slug, because that is what the agent's commands
    need: every ``/v1/projects/{project_id}`` route types the path param as a
    UUID, so a slug arrives as a 422 about UUID parsing rather than a lookup.
    The slug rides along only to be shown to a human.

    THE FOLDER DECIDES, unless someone names a project on this command.

    The AMBIENT active project (`probe project use`, `PROBE_PROJECT`) is
    deliberately NOT consulted. It used to win, on the reasoning that whoever
    set it had already answered this question -- but it answers a different
    one. `project use` sets where new RUNS go by default; it is not a statement
    that every folder imported from here on belongs there. Honouring it meant
    pointing at `anthrogen-backfill-test` and watching 37 artifacts land in
    whatever project happened to be active, which is a surprising place to have
    to go looking for them.

    `requested` is an explicit `--project` on this invocation -- a slug, or an
    id written `id:<uuid>` -- and it still wins.

    Creation goes through ``ensure_project``, whose near-miss guard refuses a
    slug that looks like a typo of one already there. A folder called
    `odyssey-v2` sitting next to an existing `odyssey_v2` should stop, not
    quietly open a second identity for the same work.
    """
    if requested:
        return _resolve_ref(client, requested)
    proj = client.ensure_project(slug_for(folder), name=folder.resolve().name)
    return str(proj["id"]), proj.get("slug") or slug_for(folder)


def _resolve_ref(client, ref: str) -> tuple[str, str]:
    """An explicitly named project slug (or ``id:<uuid>``) -> ``(project_id, slug)``.

    Shares :mod:`probe.cli.commands.ref_syntax` with the project verbs so an anchor cannot mean
    one project here and another one there -- this names every artifact the
    import uploads, and getting it wrong files someone's whole folder into a
    stranger's project.
    """
    from ....commands import ref_syntax as refs

    try:
        found = refs.resolve(client, "project", ref)
    except NotFoundError as exc:
        raise ValueError(str(exc)) from None
    return found.id, found.row.get("slug") or ref
