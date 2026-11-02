"""probe edge add/remove: lineage edges between entities, with session-event evidence."""

from __future__ import annotations
import os
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from .... import errors
# The option enums only, from `_generated.enums` rather than `probe.models`: that
# seam builds every wire model, ~0.5 s that every command paid at startup -- the
# wizard, the hooks and the status line included -- whether or not it sent one.
# `tests/test_cli_startup_imports.py` holds the CLI to this.
from ....generated.enums import (
    LineageEntityType,
    LineageRelation)
from ....sdk import agent_session
from .. import ref_syntax as refs


# -- lineage edges (fold #2) ------------------------------------------------
#: `edge add` end types named by slug (or `id:<uuid>`), resolved like `run move
#: --to`. An experiment IS a `projects` row, so the server stores both as the
#: one end type `project` (0278); the CLI keeps both words so a person can say
#: which they mean.
_PROJECT_END_TYPES = ("experiment", "project")

#: What `--source`/`--target` accept, in the order the help lists them.
_EDGE_END_TYPES = " | ".join(
    [*(t.value for t in LineageEntityType if t.value not in _PROJECT_END_TYPES), *_PROJECT_END_TYPES]
)

edge_app = typer.Typer(
    no_args_is_help=True,
    help=f"lineage edges ({_EDGE_END_TYPES.replace(' | ', '/')})",
)


def _edge_end(client: Client, end_type: str, ref: str) -> tuple[str, str]:
    """One `edge add` end as the server takes it: `experiment:`/`project:` by
    slug or `id:<uuid>` -> (`project`, its id); `run:` by id or petname -> its
    id; every other type's id as typed."""
    if end_type in _PROJECT_END_TYPES:
        return LineageEntityType.project.value, _ref(client, end_type, ref).id
    if end_type == LineageEntityType.run.value:
        # A run is named by petname as often as by id (`run get` takes either),
        # but `POST /v1/edges` takes only the id: a petname reached it as a 422
        # and the caller had to look the id up and try again. An id costs no
        # lookup; anything else resolves like `run get`, a `name:` selector
        # included even when the name itself looks like an id.
        bare, how = refs.split_selector(ref)
        if (how == "id" or bare == ref) and refs.is_uuid(bare):
            return end_type, bare
        return end_type, _ref(client, "run", ref).id
    return end_type, ref


@edge_app.command("add")
def edge_add(
    source: str = typer.Option(
        ..., "--source", metavar="type:ref", help=f"type: {_EDGE_END_TYPES}"
    ),
    relation: str = typer.Option(
        ..., "--relation", help=" | ".join(r.value for r in LineageRelation)
    ),
    target: str = typer.Option(
        ..., "--target", metavar="type:ref", help=f"type: {_EDGE_END_TYPES}"
    ),
    provenance: str = typer.Option(
        None,
        "--provenance",
        help=(
            "how the edge is known: observed_call | human | inferred, plus, on a "
            "paper edge (where it is required), provider_citation: you found the "
            "paper in a reference list. Whether one paper's bibliography names "
            "another is a `cites` link (`probe paper citations`), not an edge."
        ),
    ),
    reason: str = typer.Option(None, "--reason", help="1-2 short sentences, in your own words, on why this edge exists"),
    evidence: list[str] = typer.Option(
        None,
        "--evidence",
        metavar="EVENT_ID",
        help="repeatable: the id of a session event this edge rests on "
        "(<stream>:<offset>:<index>, as the transcript shows it)",
    ),
) -> None:
    """Add a lineage edge.

    --source/--target are `type:ref`, with type in
    run|artifact|artifact_version|paper|experiment|project. A run is named by
    its id or petname; a file or paper by its id; an experiment or project by
    its slug, or `id:<uuid>` (as `run move --to` takes it). Both are stored as
    the end type `project`: an experiment IS a project.

    A run may have more than one parent (forked_from, resumed_from,
    retried_from, branched_from): the first stays the run's parent, the others
    are added as edges. `supersedes` (between runs, projects and experiments)
    says the source's result replaces the target's; it is not a parent.

    A project or experiment end takes `derived_from` or `supersedes` (to or
    from a run, project or experiment) or `informed_by` (-> a paper), never a
    run's parent or a file relation.

    A PAPER edge REQUIRES --provenance: `discovered_via` (paper -> paper: source
    is the paper that was found, target the one it was found from) or
    `informed_by` (run, artifact or project -> the paper it drew on). Most of the time
    you want `probe paper add --via` instead, which records the paper and its
    discovery edge in one call; this verb is for correcting the graph
    afterwards.

    An edge that already exists is not an error: it prints that edge's id with
    `"already_linked": true` and exits 0. Any other refusal exits 1 with the
    server's reason.
    """
    st, _, sid = source.partition(":")
    tt, _, tid = target.partition(":")
    if not sid or not tid:
        raise typer.BadParameter("source/target must be `type:ref`")
    # Checked here so the failure names the flag rather than arriving as a 422
    # from the server. The server refuses it too -- this is the friendlier copy
    # of the same rule, never the only one.
    if (st == "paper" or tt == "paper") and not provenance:
        raise typer.BadParameter(
            "a paper edge needs --provenance: an edge you watched a tool make "
            "and one a model guessed are different claims, and the reader has "
            "to be able to tell them apart. Use one of: observed_call, "
            "provider_citation, human, inferred.",
            param_hint="--provenance",
        )
    meta = {"evidence": _edge_evidence(evidence)} if evidence else None
    with _client() as c:
        st, sid = _edge_end(c, st, sid)
        tt, tid = _edge_end(c, tt, tid)
        try:
            result = c.add_edge(
                source_type=st,
                source_id=sid,
                relation=relation,
                target_type=tt,
                target_id=tid,
                meta=meta,
                provenance=provenance,
                reason=reason,
            )
        except errors.ConflictError as exc:
            # The same edge (same ends, same relation) is already there: what
            # the caller wanted holds, so it is not a failure -- but it says so
            # and names the edge, rather than printing a row it did not write.
            # Any other 409 (a second genealogy parent) is a refusal: exit 1.
            from ....sdk.delivery.ops.classify import edge_already_exists

            if not (exc.existing_id and edge_already_exists(exc)):
                raise
            linked: dict[str, Any] = {"already_linked": True, "id": exc.existing_id}
            # What this call carried beyond the edge itself stays on neither
            # edge: the one there keeps its own (the outbox's rule too).
            unapplied = [flag for flag, value in (("--reason", reason), ("--evidence", evidence),
                                                  ("--provenance", provenance)) if value]
            if unapplied:
                linked["applied"] = False
                typer.echo(f"probe: the edge already existed; its {', '.join(unapplied)} "
                           f"{'was' if len(unapplied) == 1 else 'were'} not applied to it", err=True)
            _print_json(linked)
            return
    _print_json(result)


#: A session event id as the Probe daemon's transcript shows it:
#: `<stream>:<offset>:<index>` (`probe/shared/harness/events.py`).
_EVENT_ID = re.compile(r"\S+:\d+:\d+")


def _edge_evidence(events: list[str]) -> list[dict]:
    """`--evidence` as `meta.evidence`: `{session, event}` per event id.

    An event id is local to one session's transcript, so it is stored with the
    session it came from, or the audit could not open it (lineage plan R7):
    the daemon's session (`PROBE_DAEMON_SESSION`), else the coding agent's own.
    With neither, the id names nothing anyone can open: a usage error."""
    session = os.environ.get("PROBE_DAEMON_SESSION") or agent_session.session_id_from_env()
    if not session:
        raise typer.BadParameter(
            "an event id is only meaningful with the session it came from, and this shell names "
            "none (no PROBE_DAEMON_SESSION, no coding-agent session): drop --evidence, or run it "
            "from the session",
            param_hint="--evidence",
        )
    out: list[dict] = []
    for raw in events:
        event = raw.strip()
        if not _EVENT_ID.fullmatch(event):
            raise typer.BadParameter(
                f"{raw!r} is not an event id: <stream>:<offset>:<index>, as the transcript shows it",
                param_hint="--evidence",
            )
        out.append({"session": session, "event": event})
    return out


@edge_app.command("remove")
def edge_remove(
    edge_id: str = typer.Argument(..., help="the edge id"),
) -> None:
    """Remove one lineage edge.

    The correction half of `edge add`. Matters most for paper discovery edges:
    they record how a reader got from one paper to another, so being wrong is an
    ordinary outcome, and a chain nobody can fix stops being believed.

    A run's PARENT is an edge too (forked_from, resumed_from, retried_from,
    branched_from), and a run may have several: removing its first parent makes
    the next-oldest one its parent, or clears it when none is left. A wrong
    parent is fixed by removing it and adding the right one. So is a wrong data
    link (`probe dataset use` / `probe checkpoint use`), or a wrong role on one.
    """
    with _client() as c:
        result = c.remove_edge(edge_id)
    _print_json(result)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.runs.reads import events  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
