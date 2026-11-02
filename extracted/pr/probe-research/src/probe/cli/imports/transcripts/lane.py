"""the interactive past-sessions lane: choose sources, show the gate before anything leaves, run with progress."""

from __future__ import annotations

import contextlib
import time
from collections.abc import Iterable
from pathlib import Path


def _date_range(census: Census) -> str:
    if not census.candidates:
        return ""
    stamps = sorted(t.mtime for t in census.candidates)
    first = time.strftime("%Y-%m-%d", time.localtime(stamps[0]))
    last = time.strftime("%Y-%m-%d", time.localtime(stamps[-1]))
    return first if first == last else f"{first} to {last}"


def gate_lines(
    census: Census, assignments: dict[str, str], *, sources: Iterable[str] | None = None,
) -> list[str]:
    """What the reviewer sees before any session leaves the machine.

    THE CONSENT SURFACE. There is no server-side redaction gate any more (it was
    removed in 0.104.9.0 for quarantining whole sessions on false positives), so
    what this screen says is the only thing standing between a person and a
    surprise. It therefore names the true scope -- the whole machine, not the
    folder -- the byte total, the date range, and how many sessions are skipped
    and why.

    It no longer says anything about summaries: the digest lane was retired
    server-side, so this run writes none and promising them here would describe
    work that cannot happen.
    """
    from ... import wizard as setup

    selected = tuple(sources) if sources is not None else tuple(
        dict.fromkeys(transcript.agent for transcript in census.candidates)
    )
    label = setup.agent_label(selected) if selected else "coding-agent"
    lines = [
        "Agent sessions on this machine",
        "",
        f"  {census.sessions} sessions · {_human_bytes(census.bytes)}"
        + (f" · {_date_range(census)}" if census.candidates else ""),
        "",
        f"  Your local {label} logs from the whole machine.",
        "  They are sanitized here before upload:",
        "  tool output and file contents never leave.",
        "",
        "  Each imports on its own, with no project or experiment attached.",
    ]
    skipped = []
    if census.captured_live:
        skipped.append(f"{census.captured_live} already captured live")
    if census.already_in_probe:
        skipped.append(f"{census.already_in_probe} already in Probe")
    if census.sidechains:
        skipped.append(f"{census.sidechains} subagent sidechains")
    if census.switched_off:
        skipped.append(f"{census.switched_off} switched off, or with a stretch written while off")
    if skipped:
        lines += ["", "  Skipped: " + ", ".join(skipped)]
    if census.unreadable:
        lines += [f"  {census.unreadable} could not be read"]
    if census.identity_unverified or census.identity_conflicts:
        lines += [
            f"  {census.identity_unverified} identities unverified · "
            f"{census.identity_conflicts} conflicting copies need reconciliation"
        ]
    if census.known_no_transcript:
        # Not a failure and not uploadable -- there is no file. Shown because
        # the alternative is a total that reads as the whole population.
        lines += [
            f"  {census.known_no_transcript} more recent session(s) have no transcript "
            "on disk — nothing to import for those"
        ]
    return lines


# --- the CLI entry point -----------------------------------------------------


def saved_session_sources(
    sources: Iterable[str], *, plugin_dirs: dict[str, Path]
) -> tuple[str, ...]:
    """Sources with saved session files, independent of installed CLIs or pairing.

    Use the same roots and filename rules as discovery. An empty directory,
    prompt history without transcripts, or only subagent sidechains is not a
    saved history to offer. The full identity check and census run only after
    the source selection; deselected histories are excluded from that import.
    """
    return tuple(
        source for source in sources
        if any(
            session_id_for(path, source) is not None and path.is_file()
            for root in transcript_roots(source, plugin_dirs.get(source))
            for path in _walk(root, source)
        )
    )


def choose_sources(available: tuple[str, ...], *, selected: tuple[str, ...] | None = None):
    """Choose saved histories; every detected source starts selected."""
    import questionary

    from ... import wizard as setup
    from ...wizard import terminal as tui

    title = "Import past coding sessions"
    body = tui.wrap("Saved sessions were found for these agents.")
    prompt = "Which ones should be imported?"
    message = tui.framed(title, body, prompt)
    instruction = "enter or space toggle · ↑↓ choose · → next · ctrl+s skip · esc back"
    tui.use_checkmarks()
    checked = set(available if selected is None else selected)
    rows = {
        source: questionary.Choice(
            title=setup._menu_row(
                setup.AGENT_LABELS[source], (), checked=source in checked, indent=tui.body_indent()
            ),
            value=source,
            checked=source in checked,
        )
        for source in available
    }
    # Each border needs its own separator. Roomier screens also keep a blank
    # line outside the border; the shared layout drops that extra air to fit.
    first_border = questionary.Separator(" ")
    choices: list = [questionary.Separator(" "), first_border]
    compact_choices: list = [first_border]
    for row in rows.values():
        if len(compact_choices) > 1:
            border = questionary.Separator(" ")
            choices.extend([questionary.Separator(" "), border])
            compact_choices.append(border)
        choices.append(row)
        compact_choices.append(row)
    footer = setup.nav_footer(skip_title="Skip sessions")
    choices.extend([questionary.Separator(" "), *footer])
    compact_choices.extend(footer)

    def make_question(options, hint):
        return questionary.checkbox(
            message, choices=options, instruction=hint, style=tui.style(),
            qmark=tui.qmark(), pointer=tui.pointer(),
            validate=lambda answer: any(value in rows for value in answer)
            or "Choose at least one coding-agent history.",
        )

    question = make_question(choices, instruction)
    own_boxes = tui.draw_own_boxes(question)

    def redraw(control):
        for source, row in rows.items():
            row.title = setup._menu_row(
                setup.AGENT_LABELS[source], (),
                checked=source in control.selected_options, indent=tui.body_indent(),
            )
        control.error_message = (
            None if any(value in rows for value in control.selected_options)
            else "Choose a history, or Skip sessions."
        )

    control = setup._wire_picker(
        question, redraw=redraw,
        can_submit=lambda control: any(value in rows for value in control.selected_options),
        on_leave=lambda control: [value for value in control.selected_options if value in rows],
    )
    if control is None:
        choices = setup.without_nav(choices)
        compact_choices = None
        for source, row in rows.items():
            row.title = setup.AGENT_LABELS[source]
        instruction = "space toggle · ↑↓ choose · enter continue · esc back"
        question = make_question(choices, instruction)
    elif not own_boxes:
        for source, row in rows.items():
            row.title = setup.AGENT_LABELS[source]
    tui.point_at(control, lambda value: value == setup.NAV_BAND)
    setup.dress_band(question, control)
    @question.application.key_bindings.add("c-s", eager=True)
    def skip(event):
        event.app.exit(result=tui.SKIP)

    tui.sectioned(
        question, title=title, lines=body, prompt=prompt, instruction=instruction,
        compact_choices=compact_choices,
    )
    picked = tui.ask(question, height=tui.content_height(message, choices))
    if picked is None or picked is tui.BACK or picked is tui.SKIP:
        return picked
    return tuple(source for source in available if source in picked) or tui.BACK


@contextlib.contextmanager
def _import_progress(total: int, *, enabled: bool):
    """Keep session counts and the active phase visible during long agent calls."""
    from ... import wizard as setup
    from ...wizard import terminal as tui

    if not enabled or not tui.interactive():
        yield None
        return
    import threading

    board = tui.Board("Importing past coding sessions", ["", "", "", ""])
    board.open()
    stop = threading.Event()
    lock = threading.Lock()
    state = {"completed": 0, "phase": "Preparing import", "session": "", "started": time.monotonic()}

    def paint():
        with lock:
            completed = state["completed"]
            phase = state["phase"]
            session = state["session"]
            elapsed = int(time.monotonic() - state["started"])
        board.update(0, f"{tui.progress_bar(completed / max(1, total))}  {completed}/{total} processed")
        board.update(1, f"{phase} · {elapsed}s")
        board.update(2, session)
        board.update(3, "ctrl+c stop · re-run to resume")

    def update(completed: int, _total: int, transcript: Transcript, phase: str):
        with lock:
            state.update(
                completed=completed, phase=phase,
                session=f"{setup.AGENT_LABELS[transcript.agent]} · {transcript.session_id}",
                started=time.monotonic(),
            )
        paint()

    def heartbeat():
        while not stop.wait(1):
            paint()

    thread = threading.Thread(target=heartbeat, daemon=True)
    paint()
    thread.start()
    try:
        yield update
    finally:
        stop.set()
        thread.join(timeout=0.5)
        board.close()


def run_lane(**kwargs):
    """Run the past-sessions lane and report its verdict exactly once.

    The lane RETURNS EARLY from seven places, and every one of them renders as
    a short message the wizard prints and moves on from. That made the whole
    half of the import offer invisible: a machine where session capture was
    never paired and a person who read the review and said no are the same
    silence from the outside.

    The outcome is set explicitly at each of those returns rather than inferred
    from the prose, and the emit lives here so a new early return that forgets
    to name itself still reports SOMETHING rather than nothing.
    """
    import time as _time

    from probe import analytics as tm

    tel = tm.current()
    summary: dict = {}
    started = _time.monotonic()

    def report(outcome):
        try:
            tel.emit(
                tm.EVENT_TRANSCRIPTS_SUMMARY,
                outcome=str(outcome),
                duration_seconds=round(_time.monotonic() - started, 3),
                background=bool(kwargs.get("background")),
                interactive=bool(kwargs.get("interactive", True)),
                **{key: value for key, value in summary.items() if key != "outcome"},
            )
        except Exception:
            pass  # observability must never become observable

    try:
        result = _run_lane(summary=summary, **kwargs)
    except KeyboardInterrupt:
        report(tm.TranscriptsOutcome.ABORTED)
        raise
    except BaseException:
        report(tm.TranscriptsOutcome.ERROR)
        raise
    report(summary.get("outcome") or tm.TranscriptsOutcome.COMPLETED)
    return result


def _run_lane(
    *,
    summary: dict,
    client,
    assignments: dict[str, str] | None = None,
    include_codex: bool = True,
    include_pi: bool = True,
    interactive: bool = True,
    yes: bool = False,
    budget_bytes: int | None = None,
    sources: Iterable[str] | None = None,
    background: bool = False,
    back_to_selection: bool = False,
):
    """Discover, gate, and import this machine's transcripts. Returns report lines.

    With ``back_to_selection``, review Back reopens the source selection and
    the source selection returns ``tui.BACK``; Skip advances with a report.

    Returns EARLY, with an explanation, for every reason the lane cannot run --
    no capture credential, no sessions, a declined gate. None of them is an
    error: a machine with capture never paired simply has no way to upload, and
    saying so beats a stack trace.

    Uploads go through the capture credential's own Wire; `client` is for the
    per-session server check and for pinning the account a background import
    runs under. The local digest stage that also used it went with the
    server-side digest lane, and no scratch dir is taken any more.
    """
    from ...wizard import state as capabilities, terminal as tui
    from ... import wizard as setup

    # Every agent the registry captures whose sessions live on this machine
    # (IMPORTABLE), so a new harness is offered here without another edit.
    wanted = list(dict.fromkeys(sources)) if sources is not None else [
        source for source in IMPORTABLE
        if (include_codex or source != CODEX) and (include_pi or source != PI)
    ]
    unknown = [source for source in wanted if source not in IMPORTABLE]
    if unknown:
        raise ValueError(f"Unknown coding-agent history source: {', '.join(unknown)}")
    if not wanted:
        summary["outcome"] = "no_sources"
        return ["No coding-agent histories selected; nothing was uploaded."]
    plugin_dirs = {source: capabilities.tap_plugin_dir(source) for source in wanted}
    if interactive and not yes:
        with tui.working("Looking for saved coding-agent sessions"):
            available = saved_session_sources(wanted, plugin_dirs=plugin_dirs)
        if not available:
            summary["outcome"] = "no_saved_sessions"
            return ["No saved coding-agent sessions were found on this machine."]
    previous_selection = None
    prepared = {}
    while True:
        if interactive and not yes:
            selected = (choose_sources(available, selected=previous_selection)
                        if previous_selection is not None else choose_sources(available))
            if selected is None:
                raise KeyboardInterrupt
            if selected is tui.BACK and back_to_selection:
                summary["outcome"] = "back"
                return tui.BACK
            if selected is tui.BACK or selected is tui.SKIP:
                summary["outcome"] = "skipped"
                summary["declined_at"] = "sources"
                return ["Skipped the agent sessions."]
            wanted = list(selected)
            previous_selection = tuple(selected)

        key = tuple(wanted)
        if key in prepared:
            posters, devices, unpaired, agents, census, ledger, assignments, approved_payload = prepared[key]
        else:
            # ONE CREDENTIAL PER AGENT, resolved BEFORE the walk. A device token is
            # bound to its source, so an agent with no pairing has no way to upload at
            # all -- and discovering its sessions only to fail every one of them would
            # report a fleet of errors for a machine that is simply not set up for it.
            posters: dict[str, Poster] = {}
            devices: dict[str, str] = {}
            unpaired: list[str] = []
            for source in wanted:
                resolved = capabilities.resolved_capture_credential(source)
                if resolved is None:
                    unpaired.append(source)
                    continue
                token, base_url = resolved
                posters[source] = Poster(base_url=base_url, token=token)
                devices[source] = capabilities.capture_device_id(source) or ""

            agents = [source for source in wanted if source in posters]
            if not agents:
                summary["outcome"] = "not_paired"
                summary["unpaired"] = len(unpaired)
                from probe.sdk.session_marker import WIZARD_HINT

                return [
                    "Session capture is not paired on this machine, so there is no "
                    "credential to upload sessions with.",
                    f"Pair it with the wizard's Install, then re-run ({WIZARD_HINT}).",
                ]

            with tui.working("Counting the selected coding-agent sessions"):
                census = discover(
                    agents=agents,
                    tracked=set(),
                    plugin_dirs={source: plugin_dirs[source] for source in agents},
                )
            if not census.candidates:
                # NAME THE DIRECTORIES. "None found" on a machine whose config dir was
                # relocated is a confident zero and indistinguishable from a machine
                # that genuinely has none -- which is the whole failure this census
                # exists to prevent.
                looked = ", ".join(str(root) for root in census.roots) or "no readable directory"
                found = (
                    f" {census.known_no_transcript} recent session(s) have no transcript on disk."
                    if census.known_no_transcript
                    else ""
                )
                summary["outcome"] = "no_candidates"
                summary["agents"] = len(agents)
                summary["identity_unverified"] = census.identity_unverified
                summary["identity_conflicts"] = census.identity_conflicts
                summary["known_no_transcript"] = census.known_no_transcript
                return [
                    "No verified agent sessions are available to import.",
                    f"Looked in: {looked}.{found}",
                    f"{census.identity_unverified} identities unverified; {census.identity_conflicts} conflicting copies.",
                ]

            ledger = TranscriptLedger.for_device()
            assignments = {}  # Historical transcripts are always standalone.
            approved_payload = None
            if background and interactive:
                with tui.working("Preparing selected sessions for background import"):
                    approved_payload = _background_payload(
                        census, client=client, posters=posters, devices=devices,
                        budget_bytes=budget_bytes, unpaired=unpaired,
                    )
            prepared[key] = (posters, devices, unpaired, agents, census, ledger, assignments, approved_payload)
        if interactive and not yes:
            lines = gate_lines(census, assignments, sources=agents)
            if unpaired:
                from probe.sdk.session_marker import WIZARD_HINT

                lines += [
                    "",
                    f"  {setup.agent_label(unpaired)} histories cannot be imported yet:",
                    f"  session capture is not paired. Pair it with the wizard's Install ({WIZARD_HINT}).",
                ]
            answer = tui.review(
                lines[0], lines[2:],
                [("Import these sessions", "import"), ("Skip agent sessions", "skip")],
            )
            if answer is None:
                raise KeyboardInterrupt
            if answer is tui.BACK and back_to_selection:
                continue
            if answer != "import":
                summary["outcome"] = "skipped"
                summary["declined_at"] = "review"
                summary["sessions"] = census.sessions
                summary["agents"] = len(agents)
                return ["Skipped the agent sessions."]

        break

    summary["sessions"] = census.sessions
    summary["candidates"] = len(census.candidates)
    summary["agents"] = len(agents)
    summary["unpaired"] = len(unpaired)
    if approved_payload is not None:
        from .. import jobs as import_jobs
        from ..jobs import ui as import_jobs_ui
        from ..jobs.messages import enqueue_report

        job = import_jobs.enqueue(
            "transcripts", approved_payload,
            f"{census.sessions} sessions from {setup.agent_label(agents)}",
        )
        # Handed off, NOT finished. Whether it lands is `import_job.finished`,
        # which the detached worker emits under this same session id.
        summary["outcome"] = "enqueued"
        summary["job_state"] = str(job.get("state") or "")
        if not yes:
            job = import_jobs_ui.show_started_import(job)
        return enqueue_report(job, "Session import")

    summary["outcome"] = "completed"
    return _execute_census(
        census, client=client, posters=posters, devices=devices,
        ledger=ledger, interactive=interactive,
        budget_bytes=budget_bytes, unpaired=unpaired,
    )
from probe.cli.imports.transcripts.background import _background_payload, _execute_census  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.discovery import Census, Transcript, _walk, discover, session_id_for  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.ledger import TranscriptLedger  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.roots import CODEX, IMPORTABLE, PI, transcript_roots  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.transcripts import _human_bytes  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.transcripts.upload import Poster  # noqa: E402 -- pieces need each other; the front door loads this one first
