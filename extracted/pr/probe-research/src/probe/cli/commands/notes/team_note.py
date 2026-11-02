"""the team note's commands: probe notes team (print it), audit-advisory (for hooks) and sync (reconcile the local file)."""

from __future__ import annotations
import os
import sys

import typer
from ....sdk.settings.settings import resolve
from ....sdk import session_marker
from probe.cli.commands.notes.notes import notes_app


@notes_app.command("team")
def notes_team(
    brief: bool = typer.Option(
        False, "--brief", help="the bounded slice a session is briefed with"
    ),
) -> None:
    """Print the team's shared note -- the working memory every session starts with.

    `--brief` prints the injected slice instead of the document: the curated head
    plus the newest appends, which is what an agent session actually receives.
    """
    with _client() as c:
        payload = c.get_team_note_brief() if brief else c.get_team_note()
    text = payload.get("text" if brief else "body") or ""
    if not text:
        print("the team note is empty", file=sys.stderr)
        return
    sys.stdout.write(text if text.endswith("\n") else text + "\n")


@notes_app.command("audit-advisory")
def notes_audit_advisory(
    source: str = typer.Option(
        "claude_code", "--source", help="which harness's block to measure against"
    ),
    force: bool = typer.Option(False, "--force", help="answer even in an automated session"),
    peek: bool = typer.Option(
        False, "--peek", help="print the line without claiming this machine's audit"
    ),
) -> None:
    """Print the team note's audit line, or nothing. FOR HOOKS, not for humans.

    THE PROMPT IS THE CHANNEL. This line used to be written into the rendered
    block in `CLAUDE.md` / `AGENTS.md`, where every session of that harness read
    it -- including the ones nobody is sitting in. An audit dispatched into
    `claude -p` or `codex exec` asks for a background agent that run cannot
    spawn, on behalf of a researcher who is not there to see the result. So the
    line moved to the UserPromptSubmit hook, which fires only when a prompt is
    submitted, and this command is what that hook calls.

    LOCAL ONLY, because it runs on a prompt-submit budget: the note off disk and
    the LAST render's measurements out of `health.json`. No network, no render.

    Silent unless the note is actually due, and silent in an automated session
    (`--force` overrides, for testing). Exit status is 0 either way: a hook that
    saw a non-zero exit would report a failure where the answer is just "no".

    ONE SESSION PER MACHINE. Printing the line claims the machine's audit lease
    (`claim_audit_dispatch`), and while another session holds it this prints
    nothing -- otherwise every session on the box spawns its own auditor before
    the first one stamps the note. The hook names its session in
    `PROBE_NOTE_AUDIT_SESSION`, which lets the holder be told again if the first
    telling never arrived. `--peek` looks without claiming, so a person checking
    the line does not silence the next real dispatch.
    """
    from ....sdk.settings.settings import resolve
    from ....shared.notes import team_note as team_note_file

    if not force and team_note_file.session_is_automated():
        return
    advisory = team_note_file.advisory_for_source(source, settings=resolve(base_url=_conn.base_url))
    holder = os.environ.get(team_note_file.AUDIT_SESSION_ENV) or None
    if advisory and holder and _daemon_records(holder):
        # The daemon audits a session it records (`probe.daemon.lanes.audit`): a line here
        # would start a second auditor, from any plugin version.
        return
    if advisory and not peek and not team_note_file.claim_audit_dispatch(holder=holder):
        return
    if advisory:
        sys.stdout.write(advisory if advisory.endswith("\n") else advisory + "\n")


def _daemon_records(session_id: str) -> bool:
    """Does the daemon record this session (its switch reads `daemon`)? Unreadable: no."""
    try:
        from probe.sdk import session_marker

        return (session_marker.valid_session_id(session_id)
                and session_marker.session_state(session_id) == session_marker.STATE_DAEMON)
    except Exception:  # noqa: BLE001 - the advisory is fail-open
        return False


@notes_app.command("sync")
def notes_sync(
    push_only: bool = typer.Option(
        False, "--push-only", help="send local edits and stop; do not refresh the file"
    ),
    pull_only: bool = typer.Option(
        False,
        "--pull-only",
        help="refresh the file only; send nothing",
    ),
) -> None:
    """Reconcile the local team-note file with the server.

    THIS IS HOW AGENTS WRITE THE TEAM NOTE NOW. The session-start hook seeds
    `~/.local/state/probe/team-note/probe-team-note.md` -- ONE file per machine,
    shared by every harness on it, NOT a `memory/` directory -- you edit it like
    any other markdown, and this command sends the result. The session hooks call
    it for you; running it by hand is for when you want the round trip immediately.

    It reconciles like git: fetch the server's head, MERGE it into the file
    (markers on a real conflict), then push what came out. Merging is what lets
    a session that could not push earlier catch up without either side's text
    being dropped -- overwriting the file and refusing to sync are both losses.

    Copies that are not ours to send -- a leftover per-harness document from the
    old layout, or one written under another credential -- are parked beside
    where they were found, never deleted and never uploaded, and named in the
    output.

    Exit status is 0 for anything that settled and 2 for a conflict, so a hook
    can tell "nothing to do" from "a human needs to look at this".
    """
    from ....sdk.settings.settings import resolve
    from ....shared.notes import team_note as team_note_file

    settings = resolve(base_url=_conn.base_url)
    where = team_note_file.paths_for(settings)
    text: str | None = None
    if team_note_file.hidden_by_limit(settings):
        # This computer's workspace limit hides team-wide items, the note among
        # them: nothing is fetched or sent (local edits stay on disk and sync once
        # they show), and the block comes out of the instruction files.
        hidden = team_note_file.remove_blocks()
        _print_json(
            {
                "document": str(where.document),
                "version": None,
                "pushed": False,
                "pulled": False,
                "merged": False,
                "conflicted": False,
                "detail": team_note_file.HIDDEN_DETAIL,
                "rendered": [],
                "rendered_pointer_only": [],
                "render_unchanged": [],
                "render_opted_out": [],
                "render_failures": [],
                "render_hidden_by_limit": hidden,
            }
        )
        return
    with _client() as c:
        if push_only:
            report = team_note_file.push(c, where)
        elif pull_only:
            # Refresh without sending. No hook uses this any more -- the session
            # hooks reconcile or push unconditionally -- but it stays as the
            # manual escape hatch for taking the team's copy without offering
            # your own, e.g. when a local file is known to be junk.
            report, text = team_note_file.pull(c, where)
        else:
            report, text = team_note_file.reconcile(c, where)

    # RENDER AFTER THE NETWORK, OUTSIDE THE CLIENT. This is what actually puts
    # the note in front of an agent: the instruction files are read by the
    # harness before any hook of ours runs, so the copy a session sees is the
    # one the PREVIOUS sync left behind. Rendering here, from the text we just
    # fetched, is what keeps both harnesses saying the same thing.
    #
    # A fetch that failed leaves `text` None, and then we render NOTHING rather
    # than re-rendering a local copy that may be older than the block already
    # installed. Replacing current content with staler content is the one
    # irreversible mistake available here.
    render = team_note_file.RenderReport()
    if text is not None:
        render = team_note_file.render_blocks(text, settings=settings)

    _print_json(
        {
            "document": str(where.document),
            "version": report.version,
            "pushed": report.pushed,
            "pulled": report.pulled,
            "merged": report.merged,
            "conflicted": report.conflicted,
            "detail": report.detail,
            "rendered": list(render.written),
            "rendered_pointer_only": list(render.pointer_only),
            "render_unchanged": list(render.unchanged),
            "render_opted_out": [*render.opted_out, *render.removed],
            "render_failures": list(render.failures),
            "render_hidden_by_limit": list(render.hidden),
        }
    )
    for failure in render.failures:
        print(f"team-note block: {failure}", file=sys.stderr)
    if report.conflicted:
        print(report.detail, file=sys.stderr)
        raise typer.Exit(2)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client, _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
