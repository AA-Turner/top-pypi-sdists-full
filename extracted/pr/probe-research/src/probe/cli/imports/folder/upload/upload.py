"""hand every unit's manifest to `artifact add --from-manifest` and watch the outbox drain."""

from __future__ import annotations
import json
import sys
import time
from pathlib import Path

from ... import folder as bf
from . import ledger as ledger_mod
from .manifest import validate_manifest


def _ingest_summary(stdout: str) -> dict | None:
    """The `{"enqueued": N, ...}` object out of `artifact add`'s output.

    NOT `splitlines()[-1]`. That is what shipped, and the command prints
    PRETTY-PRINTED JSON, so the last line is `}` -- which parses as nothing.
    Every manifest then reported "could not read the ingest summary (['}'])"
    and the run said "0 queued for upload" while all 204 rows sat in the outbox
    delivering perfectly well. A reporting bug that reads exactly like total
    data loss, on the step where bytes finally move.

    Scanning for a balanced brace run instead also survives what else lands on
    stdout: the version-update nudge prints there, and so does anything a
    future release decides to say first.
    """
    best: dict | None = None
    for data in bf._embedded_summaries(stdout, key="failures"):
        best = data
    if best is not None:
        return best
    # `failures` is absent when nothing failed, so fall back to the count --
    # which is the field this is really after.
    depth = 0
    start = -1
    for i, ch in enumerate(stdout):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}" and depth:
            depth -= 1
            if depth == 0 and start >= 0:
                try:
                    data = json.loads(stdout[start : i + 1])
                except ValueError:
                    continue
                if isinstance(data, dict) and "enqueued" in data:
                    best = data
    return best


def enqueue_manifests(
    folder: Path, outcomes: list[UnitOutcome], *, project_of: dict[str, str],
    ledger: ledger_mod.Ledger | None = None,
) -> tuple[int, list[str]]:
    """Hand every unit's manifest to `artifact add --from-manifest`.

    THE CWD IS LOAD-BEARING. A manifest row's `path` is relative to the imported
    folder and the reader resolves it against the process working directory, so
    this runs with `cwd=folder`. Anywhere else, every row fails "is not a regular
    file" -- or worse, a same-named file under the wrong cwd uploads the wrong
    bytes under the right name.

    THE ANCHOR IS PASSED EXPLICITLY. Rows carry no anchor key, so without
    `--project` every row is rejected for want of one and the command exits 1
    having enqueued nothing -- a zero-import wearing a well-formed error.
    """
    import subprocess
    import sys

    enqueued = 0
    problems: list[str] = []
    for out in outcomes:
        if not out.manifest or not out.rows:
            continue
        checked = validate_manifest(out.manifest, out.unit.paths, root=folder)
        manifest = out.manifest
        if not checked.complete:
            problems.append(f"{manifest.name}: {checked.describe()}")
            if ledger is not None:
                ledger.finish_unit(out.unit.unit_id, ok=False, enqueued=len(checked.rows),
                                   error=checked.describe())
            if not checked.rows:
                continue
            # Retain the original for diagnosis. Only validated, confined rows
            # can cross the upload boundary, even on legacy/recovery paths.
            from .....foundation.durable.durable import write_text_atomic

            manifest = manifest.with_suffix(".validated.jsonl")
            write_text_atomic(manifest, "".join(json.dumps(row) + "\n" for row in checked.rows))
        project = project_of.get(out.unit.unit_id, out.unit.project)
        proc = subprocess.run(  # noqa: S603 - fixed argv, no shell
            [
                sys.executable, "-c",
                "import sys; from probe.cli import main; sys.exit(main(sys.argv[1:]))",
                # NO write-mode flag, and none is needed: `--from-manifest`
                # queues to the outbox and lets the drainer deliver whichever
                # way the flag points -- that is the point of the verb.
                #
                # It was once dropped for a second reason that no longer holds.
                # `--async` used to be ROOT-only, so placing it here produced
                # "Error: No such option: --async" and every manifest silently
                # failed to enqueue while all six units reported success: 204
                # files read, described and manifested, 0 uploaded. The flag is
                # accepted in both positions now (see `write_mode_opt`), so that
                # trap is gone; the first reason is the one that keeps it out.
                "artifact", "add", "--from-manifest", str(manifest),
                "--project", project,
            ],
            cwd=str(folder), capture_output=True, text=True,
        )
        summary = _ingest_summary(proc.stdout)
        if summary is not None:
            landed = int(summary.get("enqueued") or 0)
            enqueued += landed
            # RECORDED SEPARATELY from the unit's DONE. A unit is done when its
            # manifest exists; this is the only record that its rows reached
            # the queue, and the gap between the two is where a dropped
            # connection lands.
            if ledger is not None:
                ledger.record_enqueued(out.unit.unit_id, landed)
            for failure in summary.get("failures") or []:
                problems.append(f"{out.manifest.name} line {failure.get('line')}: "
                                f"{failure.get('error')}")
        else:
            problems.append(
                f"{out.manifest.name}: could not read the ingest summary "
                f"({(proc.stderr or proc.stdout or '').strip().splitlines()[-1:] or ['no output']})"
            )
    return enqueued, problems


#: How often the drain watcher re-counts the outbox. The queue is a directory
#: of files, so this is a cheap listdir -- but not free, and nobody reads a
#: number that changes faster than they can look at it.
WATCH_POLL_S = 1.0


def watch_outbox(total: int, *, stream=None, poll: float = WATCH_POLL_S) -> list[str]:
    """Sit and watch the queue drain. Returns the closing lines.

    OPTIONAL, and it has to be: the outbox is a background drainer precisely so
    an import does not hold anyone's terminal, and on a big folder this runs for
    a long time. Ctrl-C leaves the queue exactly where it was -- nothing here
    touches it, it only counts -- so stopping the watch is not stopping the
    upload, and the closing line says so rather than leaving that to be
    guessed.

    Reuses `bf.Activity` deliberately: this is the same question the import
    screen answers ("how far along, how much longer") and a second progress
    idiom for it would be a second thing to learn.
    """
    import time

    from probe.cli.wizard import terminal as tui

    from .....sdk.delivery.journal.journal import Journal
    from ....connection import _conn

    journal = Journal(_conn.spool_dir)
    out = stream if stream is not None else sys.stdout
    live = hasattr(out, "isatty") and out.isatty()
    state = bf.Activity(total=max(1, total), doing="draining")
    started = time.monotonic()

    def counts() -> tuple[int, int]:
        # Every queue: a PROBE_TOKEN or in-code credential's uploads queue in
        # their own folder (#2035).
        queues = journal.namespaces()
        return sum(len(q.pending()) for q in queues), sum(len(q.failed()) for q in queues)

    pending, failed = counts()
    board = tui.Board(f"Uploading {total:,} file(s)", [""], out=out) if live else None
    if board is not None:
        board.open()
    try:
        while pending:
            # `done` reads from `seen`, and the outbox counts DOWN -- so the
            # delivered set is synthesised from the difference rather than
            # tracked per item. Nothing else needs the paths.
            delivered = max(0, total - pending)
            state.seen = set(range(delivered))
            state.doing = f"{pending:,} left" + (f" · {failed:,} failed" if failed else "")
            if board is not None:
                state.ticks += 1
                board.update(0, state.line(time.monotonic() - started))
            time.sleep(poll)
            pending, failed = counts()
    except KeyboardInterrupt:
        return [f"Stopped watching. {pending:,} file(s) still queued — the drainer "
                "keeps going in the background.",
                "`probe outbox status` shows where it got to."]
    finally:
        if board is not None:
            board.close(erase=True)

    if failed:
        return [f"{total - failed:,} of {total:,} delivered · {failed:,} failed.",
                "`probe outbox status --verbose` lists them; re-running the "
                "import retries."]
    return [f"All {total:,} file(s) delivered."]
from probe.cli.imports.folder.upload.units import UnitOutcome  # noqa: E402 -- pieces need each other; the front door loads this one first
