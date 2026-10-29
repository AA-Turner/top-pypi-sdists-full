"""The first write a session makes to a project, experiment or run prints the
opening of that entity's note and its Open and Don't repeat lines (notes parity
N2), so whoever records -- the daemon's writer or an inline agent, both run
these commands -- reads what the note already says before adding to it. An
entity with no note prints nothing.

Once per session per entity and per writer (the daemon's and the agent's
contexts are apart), recorded beside the summary reminder's own
(`summary_cli._loaded_file`, key `noted`) BEFORE the read, so a failed read is
not tried again on every write. Bounded (`READ_S`, one attempt) and silent on
any error: the write it follows already landed.
"""

from __future__ import annotations

import os
import re
import sys
import time

#: At most this many characters are printed, header included.
MAX_CHARS = 600
#: The read gets this long, with no retry.
READ_S = 3.0
HEADER = "Note on {kind} {label} (all of it: probe notes show --{kind} {label}):"
#: The sections printed after the opening, as edit-notes names them.
SECTIONS = (("don't repeat", "Don't repeat"), ("open", "Open"))
#: Creates: the entity is new, so it has no note to read.
_CREATES = {"project create": "project", "experiment create": "experiment"}
_HEADING = re.compile(r"^\s*(?:#{1,6}\s+(?P<hash>.+?)\s*#*|\*\*(?P<bold>[^*]+?)\*\*(?P<rest>.*))\s*$")


def target(args: list[str]) -> tuple[str, str, bool] | None:
    """`(kind, ref, new)` of the entity a `probe` write lands on, from the CLI's
    own parse: the run it names, else the experiment, else the project (a
    create's own slug, `new`). None for a read or an unscoped write."""
    from probe.daemon import precheck

    from ..sdk import session_marker

    kind, _ = session_marker.classify_probe_args(list(args))
    if kind != "write":
        return None
    try:
        parsed = precheck.parse(list(args))
    except precheck.ParseError:
        return None

    def first(*names: str) -> str | None:
        for name in names:
            value = next((v for v in precheck._strings(parsed.params.get(name)) if v.strip()), None)
            if value:
                return value
        return None

    if parsed.path in _CREATES:
        slug = first("slug")
        return (_CREATES[parsed.path], slug, True) if slug else None
    for kind, names in (("run", ("run",)), ("experiment", ("experiment", "experiment_id")),
                        ("project", ("project", "project_id"))):
        found = first(*names)
        if found:
            return kind, found, False
    return None


def _name(heading: str) -> str:
    return heading.strip().rstrip(":").strip().lower().replace("’", "'").replace("do not", "don't")


def excerpt(text: str) -> dict[str, list[str]]:
    """The note's first paragraph (`""`) and the lines under each of SECTIONS,
    by heading (`## Open`) or bold label (`**Open**`, `**Open:** text`)."""
    out: dict[str, list[str]] = {"": []}
    current: str | None = ""
    opened = False
    for line in text.split("\n"):
        found = _HEADING.match(line)
        if found:
            name = _name(found.group("hash") or found.group("bold"))
            current = next((key for key, _ in SECTIONS if name.startswith(key)), None)
            rest = (found.group("rest") or "").strip(" :")
            if current is not None:
                out.setdefault(current, [])
                if rest:
                    out[current].append(rest)
            continue
        if not line.strip():
            if current == "" and opened:
                current = None  # the opening is one paragraph
            continue
        if current == "":
            opened = True
        if current is not None:
            out.setdefault(current, []).append(line.strip())
    return out


def render(kind: str, label: str, text: str | None) -> str | None:
    """What is printed for the note `text` of `kind` `label`, or None when it
    has none. At most MAX_CHARS."""
    if not text or not text.strip():
        return None
    parts = excerpt(text)
    lines = [HEADER.format(kind=kind, label=label)]
    if parts[""]:
        lines.append(" ".join(parts[""]))
    for key, title in SECTIONS:
        if parts.get(key):
            lines.append(f"{title}: " + " / ".join(parts[key]))
    if len(lines) == 1:
        lines.append(text.strip().split("\n", 1)[0])
    out = "\n".join(lines)
    return out if len(out) <= MAX_CHARS else out[: MAX_CHARS - 1].rstrip() + "…"


def _read(kind: str, ref: str) -> str | None:
    """The entity's note, or None. Bounded by READ_S whatever stalls -- a name
    lookup included, which no socket timeout covers: the read runs on a
    daemon thread this waits on, and one still running when the time is up is
    left behind (it holds nothing the process needs to exit)."""
    import threading

    from ..sdk.transport import deadline_scope
    from .summary_cli import _main

    main = _main()  # the module: the package re-exports its `main()` under the same name
    got: dict[str, str | None] = {}

    def read() -> None:
        try:
            with deadline_scope(time.monotonic() + READ_S), main._client() as client:
                transport = getattr(client, "transport", None)
                if transport is not None:
                    transport.max_retries = 0
                    transport.timeout = min(float(getattr(transport, "timeout", READ_S)), READ_S)
                flags = {"project": None, "experiment": None, "run": None, kind: ref}
                found, entity_id, _ = main._note_target(client, **flags)
                got["notes"] = main._entity_notes_row(client, found, entity_id).get("notes")
        except BaseException:  # noqa: BLE001 -- silent: a thread's error would print a traceback
            return

    worker = threading.Thread(target=read, name="probe-first-touch", daemon=True)
    worker.start()
    worker.join(READ_S)
    return got.get("notes")


def show(args: list[str]) -> None:
    """After a `probe` write exited 0: the first one this session makes to an
    entity prints its note (`render`) on stderr. Never raises."""
    try:
        from . import owed, summary_cli

        sid = summary_cli.session_id()
        if sid is None or os.environ.get(summary_cli.RUN_ID_ENV):
            return  # no session, or a run recording its own data (`probe exec`, the SDK)
        head = args[: args.index("--")] if "--" in args else list(args)
        if "--help" in head:
            return
        found = target(list(args))
        if found is None:
            return
        kind, ref, new = found
        key = f"{owed.writer()}:{kind}:{ref}"
        if key in summary_cli._read_loaded(sid)["noted"]:
            return
        summary_cli._write_loaded(sid, lambda d: d.update(noted=sorted(set(d["noted"]) | {key})))
        if new:
            return
        text = render(kind, ref, _read(kind, ref))
        if text:
            print(text, file=sys.stderr)
    except (Exception, SystemExit):  # noqa: BLE001 -- a hint, never a failed write
        return
