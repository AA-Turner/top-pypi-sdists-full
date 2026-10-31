"""Diagnostic reports to the Probe team: what broke on this machine, sent once.

ONE implementation for every sender (plan B1, B4, B9):

  * the Probe service, when a daemon worker, a recorder, a hook host or the
    service itself misbehaves: `python -I -m probe.core.run report` with
    `{"auto": true, "family", "reason", "sid", "env", "facts"}` on stdin
    (`ReportRequest`), one answer object on stdout (`Answer`);
  * `probe doctor --send` (the agent's command), in-process: a manual report,
    no consent gate, no dedupe;
  * `probe doctor --bundle [--send]` (the desktop app's "Send log"): the full
    debug log (`probe.core.debug_bundle`), from the same readers and the same
    scrubber, collected with `collect(Scope.LOCAL)`.

`collect(Scope.STAFF)` is the small report: allowlisted fields, log TAILS, this
machine's home and login name removed, each source in its own 2 s budget, the
whole object at most `REPORT_MAX_BYTES`. It never copies `probe daemon status
--json` or a status snapshot, opens no database and reads no approvals (they
carry the agent's unapproved text).

WHOSE DATA. Per-session data (its worker logs, its tap log) is included only
for a session whose daemon trace folder is bound to THIS server and THIS
daemon key (the trace shipper's rule, read-only): another account's session on
the same machine is withheld, and the report says so. The shared logs
(`service.log`, `daemon-errors.log`) keep only the service's own lines, and of
those a line naming a session only for the report's own session (or, for a
machine report, a bound one).

GATE (automatic reports only). `probe._shared.report_policy`: `PROBE_TELEMETRY`
or `PROBE_DIAGNOSTICS` off in the consenting environment, or a backend that is
not Probe's hosted service, stops it. Then one report per (family, session or
machine) per `DEDUPE_WINDOW_S`, claimed with an `O_CREAT|O_EXCL` stamp so two
reporters racing for the same incident send one. A manual report is the
person's own choice and skips both.

SENDING. `POST /v1/diagnostics/reports` through the SDK transport (so
`X-Probe-Device` rides along), with the CLI's token, then the daemon key, in
`UPLOAD_TIMEOUT_S`. Every answer is final: no retry loop (offline, 404, 413,
422, 429 and 5xx included). An automatic send that failed offline, on the
server or its rate limit gives its dedupe window back (`release`,
`RELEASED_ON`), so the caller's own later try (the Probe service retries a
report it did not land) is not answered `deduped`; too large or unauthorized keeps
it (the same report fails the same way). The newest `KEEP_REPORTS` reports stay in
`<state>/probe/daemon/reports/` with what came of them, so "what did it send?"
has an answer on the machine.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import re
import shlex
import threading
import time
import uuid
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path

from probe._compat import StrEnum

ROUTE = "/v1/diagnostics/reports"
SCHEMA = 1
#: The report object's own cap (the server takes 640 KiB of body).
REPORT_MAX_BYTES = 512 * 1024
#: The service's facts, as the `report` read's contract caps them.
FACTS_MAX_BYTES = 64 * 1024
DEDUPE_WINDOW_S = 6 * 3600
KEEP_REPORTS = 5
UPLOAD_TIMEOUT_S = 10.0
#: Each STAFF source's own budget: a hung read costs the report one source.
STAFF_SOURCE_BUDGET_S = 2.0
#: Device logs older than this say nothing about the incident.
LOG_MAX_AGE_S = 24 * 3600
#: The contract's bounds on the wire fields.
MAX_HARNESSES = 8
MAX_SESSION_IDS = 50
VERSION_MAX_CHARS = 32
OS_MAX_CHARS = 128

#: `family` and `reason`: the server's slug rule (no enum on its side).
SLUG = re.compile(r"^[a-z0-9_:.-]{1,64}$")
UUID = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
_UUID_EXACT = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
_HARNESS = re.compile(r"^[a-z][a-z0-9_]{0,31}$")

#: A config key or an environment variable whose value is a credential (plan
#: B9): its value never leaves the machine, whatever it looks like. A container
#: under such a key (an OAuth or account block: `oauthAccount`) is dropped whole.
#: `PASS` ends a name (`DB_PASS`) or a word in it; `_PWD`/`_PAT` end one
#: (`MYSQL_PWD`, `GH_PAT`) so the working directory (`PWD`) and `PATH` stay.
CREDENTIAL_NAME = re.compile(
    r"TOKEN|KEY|SECRET|PASS(?:W|PHRASE|_|\b)|_PWD$|_PAT$|DSN|PRIVATE|BEARER|JWT|CREDENTIAL|AUTH|COOKIE|ACCOUNT",
    re.IGNORECASE,
)
#: Keys whose value is a command line (an MCP server's `command` and `args`,
#: a process's `argv`): reduced to the program and flag names (`redact_argv`).
ARGV_KEYS = frozenset({"args", "argv", "cmdline", "command", "cmd", "notify"})
#: Keys whose values are a person's own words, not settings: an older Claude
#: Code keeps each project's prompt history in `~/.claude.json`.
CONTENT_KEYS = frozenset({"history", "pastedContents"})
REDACTED = "<redacted>"
DROPPED = "<dropped: conversation content>"

#: The service's own log lines (`service.log`): everything else in that file
#: is a hook host's raw stderr, or another tool's.
_SERVICE_LINE = re.compile(r"^\[[0-9TZ:-]+\] probe-service(?:-guard|-keeper)?\[\d+\]:")
_SERVICE_STAMP = re.compile(r"^\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})Z\]")
_DEVICE_STAMP = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}) ")


class Scope(StrEnum):
    #: The small allowlisted report the service and `probe doctor --send` send.
    STAFF = "staff"
    #: The full debug log (`probe doctor --bundle`): whole files, more sources.
    LOCAL = "local"


class Kind(StrEnum):
    AUTO = "auto"
    MANUAL = "manual"


class Failure(StrEnum):
    """Why a send did not land: the contract's error kinds (and the `report`
    read's `skipped` words)."""

    OFFLINE = "offline"
    RATE_LIMITED = "rate_limited"
    TOO_LARGE = "too_large"
    SERVER = "server"
    UNAUTHORIZED = "unauthorized"


#: `skipped` when a report of this family was already sent in this window.
DEDUPED = "deduped"
#: `skipped` prefix when the gate stops an automatic report.
DISABLED = "disabled:"
#: A manual report's family and reason (`probe doctor --send`).
MANUAL_FAMILY = "manual"
MANUAL_REASON = "doctor_send"


@dataclass(frozen=True)
class Answer:
    """The `report` read's one answer object (the contract's shape, exactly)."""

    sent: bool
    id: str | None = None
    skipped: str | None = None
    path: str | None = None

    def as_json(self) -> dict:
        return {"sent": self.sent, "id": self.id, "skipped": self.skipped, "path": self.path}


@dataclass(frozen=True)
class Reply:
    """One API call's outcome: its JSON on success, else why not."""

    status: int | None
    body: dict | None = None
    failure: Failure | None = None
    retry_after: float | None = None
    token: str | None = None

    @property
    def ok(self) -> bool:
        return self.failure is None


# ---------------------------------------------------------------------------
# The scrubber (one for both scopes)
# ---------------------------------------------------------------------------


def scrub_for(text: str, scope: Scope) -> str:
    """Every credential out of `text`. STAFF also loses this machine's home and
    login name and every other home folder (`probe._shared.scrub`); LOCAL keeps
    paths: the debug log is the person's own, and paths are the diagnosis.
    Raises when the scrubber does: the caller withholds the text then."""
    if scope is Scope.STAFF:
        from probe._shared import scrub

        return scrub.scrub(text)
    from probe.sdk.redaction import scrub_string

    return scrub_string(text)


def credential_name(name: object) -> bool:
    return isinstance(name, str) and bool(CREDENTIAL_NAME.search(name))


def header_name(name: object) -> bool:
    """A name whose value is a set of HTTP headers (`ANTHROPIC_CUSTOM_HEADERS`,
    `OTEL_EXPORTER_OTLP_HEADERS`, an MCP server's `headers`). A name that is
    also credential-like (`AUTH_HEADER_VALUE`) is a credential: callers check
    `credential_name` first."""
    return isinstance(name, str) and "HEADER" in name.upper()


#: A header's name, its separator and its value, in a line or a
#: comma-separated piece (`X-Team: research`, `x-honeycomb-team=hc`).
_HEADER = re.compile(r"^[ \t]*([^:=]*?)([ \t]*[:=][ \t]*)(.*)$", re.DOTALL)
#: What a real header name looks like.
_HEADER_TOKEN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")


def plain_header_name(name: str) -> bool:
    """A header name that may be shown: a plain token, not credential-like
    (`X-Api-Key`), unchanged by the scrubber (`sk-ant-...`), and not an opaque
    run of mixed case or digits with no separator (`dXNlcjpwYXNzd29yZA`, base64
    that only looks like a name before its `=` padding)."""
    if not _HEADER_TOKEN.match(name) or credential_name(name):
        return False
    if "-" not in name and "_" not in name and (any(c.isdigit() for c in name) or any(c.isupper()
                                                                                     for c in name[1:])):
        return False
    try:
        return scrub_for(name, Scope.LOCAL) == name
    except Exception:  # noqa: BLE001 -- unscrubbable: not shown
        return False


def _redact_header_line(line: str) -> str | None:
    """One line of headers. Every header keeps its name when it is a plain
    header name and loses everything after it to the end of the line;
    comma-separated pairs (`a=1,b=2`, OTLP's form) keep every name only when
    every piece is such a pair. A line whose name is not plain is replaced
    whole; a line with no `:` or `=` at all is dropped (None)."""
    pieces = line.split(",")
    if len(pieces) > 1:
        parsed = [_HEADER.match(piece) for piece in pieces]
        if all(m and plain_header_name(m.group(1)) for m in parsed):
            return ",".join(f"{m.group(1)}{m.group(2)}{REDACTED}" for m in parsed)
    match = _HEADER.match(line)
    if not match:
        return None
    if not plain_header_name(match.group(1)):
        return REDACTED
    return f"{match.group(1)}{match.group(2)}{REDACTED}"


def redact_headers(value: object) -> object:
    """Every header VALUE replaced and every header name kept when it is a
    plain header name (`X-Team: research` becomes `X-Team: <redacted>`); a name
    that is not is replaced too. Text that holds no header is replaced whole."""
    if isinstance(value, dict):
        out: dict = {}
        for key, item in value.items():
            name = str(key) if plain_header_name(str(key)) else REDACTED
            while name in out:
                name += "'"
            out[name] = item if item is None or isinstance(item, bool) else REDACTED
        return out
    if isinstance(value, (list, tuple)):
        return [redact_headers(item) for item in value]
    if not isinstance(value, str):
        return value
    lines = [kept for kept in map(_redact_header_line, value.splitlines()) if kept is not None]
    return "\n".join(lines) if lines else REDACTED


#: `redact_tree` calls its `check` once per this many nodes: a walk of a huge
#: config can be stopped there (`debug_bundle.Sink.check`).
CHECK_EVERY = 1000


def redact_tree(value: object, scope: Scope, *, key: str = "", check: Callable[[], None] | None = None) -> object:
    """A parsed config (JSON, TOML) with every value under a credential-like key
    replaced, containers under one dropped whole (an OAuth or account block), a
    person's prompt history dropped, header values replaced, command lines
    reduced by the argv rule (`ARGV_KEYS`, `redact_argv`), and every other
    string scrubbed. Booleans, numbers and nulls under a credential-like key
    stay: `max_tokens: 4096` is a setting, and no credential is a number.
    `check()` runs every `CHECK_EVERY` nodes and may raise to stop the walk."""
    seen = [0]

    def walk(value: object, key: str) -> object:
        seen[0] += 1
        if check is not None and seen[0] % CHECK_EVERY == 0:
            check()
        if key and credential_name(key):
            if value is None or isinstance(value, (bool, int, float)):
                return value
            return REDACTED
        if key and header_name(key):
            return redact_headers(value)
        if key in ARGV_KEYS and isinstance(value, (str, list, tuple)):
            return redact_command(value, program=key != "args", scope=scope)
        if isinstance(value, dict):
            out: dict = {}
            for item_key, item in value.items():
                name = str(item_key)
                if name in CONTENT_KEYS:
                    out[scrub_for(name, scope)] = DROPPED
                    continue
                out[scrub_for(name, scope)] = walk(item, name)
            return out
        if isinstance(value, (list, tuple)):
            return [walk(item, "") for item in value]
        if isinstance(value, str):
            return scrub_for(value, scope)
        return value

    return walk(value, key)


def redact_env(env: Mapping[str, str], scope: Scope) -> dict[str, str]:
    """An environment: a credential-named variable's value never leaves, a
    headers variable keeps only its plain header names, and every other value
    is scrubbed (`HTTPS_PROXY=http://user:pass@host` included)."""
    out: dict[str, str] = {}
    for name, value in sorted(env.items()):
        name = str(name)
        if credential_name(name):
            out[name] = REDACTED
        elif header_name(name):
            out[name] = str(redact_headers(str(value)))
        else:
            out[name] = scrub_for(str(value), scope)
    return out


# ---------------------------------------------------------------------------
# The argv rule: a command line keeps its program and its flag names
# ---------------------------------------------------------------------------
# One rule for every command line a report or the debug log carries -- a
# process's argv, a config's `command`/`args`/`notify`, the service's facts:
#
#   * leading `NAME=value` words      -> `NAME=<arg>`
#   * the program (argv[0])           -> its basename, scrubbed; not a string -> `<arg>`
#   * a flag                          -> its NAME (`--json`, `-p`); `--x=v` -> `--x=<arg>`, `-pv` -> `-p<arg>`
#   * EVERY flag value and positional -> `<arg>`
#   * except, for a Python program, `-m probe` / `-m probe.<x>` (the module),
#     and ONE subcommand word: the first positional after the program (or after
#     a Probe module) with no flag before it, and only when it is one of
#     `PROBE_SUBCOMMANDS`.
#
# Nothing else is kept: a prompt (`claude -p "..."`, `probe ask "..."`), a
# password (`mysql -phunter2`), a model name alike.

#: What replaces every positional argument and flag value of a command line.
ARG = "<arg>"
#: The words a Probe command line may keep as its subcommand: the CLI's
#: top-level commands (`probe.cli.main.app`) and `probe.core.run`'s actions
#: (`ActionName`). `tests/test_core_report.py` derives the set from the code and
#: holds this copy to it (importing the CLI here would load all of it).
PROBE_SUBCOMMANDS = frozenset({
    "access-group", "agent-rules", "approvals", "artifact", "ask", "backfill", "bundle", "capy", "checkpoint",
    "codex_trust", "commits", "companion", "configure", "context", "coordinates", "daemon", "dataset", "deny", "desktop",
    "docs", "doctor", "draft", "edge", "events", "exec", "experiment", "feedback", "file", "flush", "get", "group",
    "ignore", "import", "install", "link", "log", "login", "logout", "mcp", "metrics", "notes", "outbox", "paper",
    "project", "provenance", "recorder", "repair", "report", "run", "series", "service", "session", "session_default",
    "setup", "shared", "snapshot", "snapshot-prune-refs", "snapshot-restore", "snapshot-show", "source", "span",
    "status", "statusline", "summary", "sync", "token", "trial", "uninstall", "update", "version", "views",
    "visuals", "wandb", "whoami", "wizard", "workspace", "workspace_limit",
})
#: `python`, `python3.12`, `pythonw.exe`: whose `-m <module>` names the program run.
_PYTHON = re.compile(r"^python[0-9.]*w?(\.exe)?$", re.IGNORECASE)
#: `-m probe` or `-m probe.<module>`.
_PROBE_MODULE = re.compile(r"^probe(\.[a-z_][a-z0-9_]*)*$")
#: A leading `NAME=value` word: an environment assignment before the program.
_ASSIGNMENT = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=")


def program_name(arg0: object, scope: Scope = Scope.LOCAL) -> str:
    """argv[0] as its program's basename, scrubbed: `/usr/local/bin/claude` ->
    `claude`, `C:\\Program Files\\nodejs\\node.exe` -> `node.exe` (one path,
    spaces and all). Not a string: `<arg>`."""
    if not isinstance(arg0, str):
        return ARG
    return re.split(r"[\\/]", scrub_for(arg0.strip(), scope))[-1] or ARG


def redact_argv(argv: list | tuple, scope: Scope | None = None) -> list[str]:
    """A command line by the argv rule (above). A one-word argv with spaces (a
    rewritten process title) is split; a real argv[0] never is."""
    scope = scope or Scope.LOCAL
    words = list(argv)
    if len(words) == 1 and isinstance(words[0], str) and len(words[0].split()) > 1:
        words = words[0].split()
    out = _leading_assignments(words)
    rest = words[len(out):]
    if not rest:
        return out
    program = program_name(rest[0], scope)
    return [*out, program, *redact_args(rest[1:], program=program)]


def redact_args(args: list | tuple, *, program: str = "") -> list[str]:
    """The arguments after the program by the argv rule; `program` is its name
    ("" for an MCP server's `args`, which keeps no subcommand)."""
    python = bool(_PYTHON.match(program))
    slot = program.lower() in ("probe", "probe.exe")  # the subcommand slot is open
    module_next = False
    out: list[str] = []
    for arg in args:
        if not isinstance(arg, str):
            out.append(ARG)
            slot = module_next = False
            continue
        if module_next:  # the word after a Python program's `-m`
            module_next = False
            if _PROBE_MODULE.match(arg):
                out.append(arg)
                slot = True
            else:
                out.append(ARG)
            continue
        if arg == "--":
            out.append(arg)
            slot = False
        elif arg.startswith("--"):
            name, eq, _value = arg.partition("=")
            out.append(f"{name}={ARG}" if eq else name)
            slot = False
        elif arg.startswith("-") and len(arg) > 1:
            out.append(arg[:2] if len(arg) == 2 else arg[:2] + ARG)  # `-phunter2`: a glued value
            module_next = python and arg == "-m"
            slot = False
        else:
            out.append(arg if slot and arg in PROBE_SUBCOMMANDS else ARG)
            slot = False
    return out


def _leading_assignments(words: list) -> list[str]:
    out = []
    for word in words:
        match = _ASSIGNMENT.match(word) if isinstance(word, str) else None
        if not match:
            break
        out.append(f"{match.group(1)}={ARG}")
    return out


def redact_command(value: str | list | tuple, *, program: bool, scope: Scope = Scope.LOCAL) -> str | list[str]:
    """A command in a config (`command`, `args`, Codex's `notify`) by the argv
    rule: a list keeps its shape (every item counts, numbers included); a
    string is split like a shell would (`shlex`, so a quoted value is one
    word) and rejoined. `args` (`program` False) has no program word."""
    if isinstance(value, str):
        try:
            words: list = shlex.split(value)
        except ValueError:
            words = value.split()
    else:
        words = list(value)
    if program:
        out = redact_argv(words, scope) if words else []
    else:
        out = redact_args(words)
    return " ".join(out) if isinstance(value, str) else out


#: The most of a config file parsed (WHOLE, never tailed: a tail of
#: `~/.claude.json` is not JSON, and text scrubbing alone would let its account
#: block and prompt history through). Bigger is listed with its size: parsing
#: and walking 13 MiB took 15 s on a loaded machine.
CONFIG_MAX_BYTES = 8 * 1024 * 1024


def read_config(path: Path, *, check: Callable[[], None] | None = None) -> tuple[str | None, str | None]:
    """`(redacted text, None)` for a JSON or TOML config parsed WHOLE, or
    `(None, why)` when it is too big, unreadable or does not parse: then only a
    listing of it may be written, never its text. A UTF-8 byte order mark is
    allowed. `check` is `redact_tree`'s."""
    try:
        if not path.is_file():
            return None, "not a regular file"
        size = path.stat().st_size
        if size > CONFIG_MAX_BYTES:
            return None, f"{size} bytes, over {CONFIG_MAX_BYTES / (1024 * 1024):g} MiB: not parsed"
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        return None, f"unreadable ({type(exc).__name__})"
    if path.name.lower().endswith(".toml"):
        clean = redact_toml_text(text, Scope.LOCAL, check=check)
    else:
        clean = redact_json_text(text, Scope.LOCAL, check=check)
    return (clean, None) if clean is not None else (None, "not parsed")


def redact_toml_text(text: str, scope: Scope, *, check: Callable[[], None] | None = None) -> str | None:
    """A TOML file (Codex's `config.toml`), redacted as a tree (`redact_tree`)
    and written back as TOML; comments are dropped (a commented-out key is
    still a key). None when it does not parse."""
    from probe._compat import tomllib

    try:
        parsed = tomllib.loads(text)
        clean = redact_tree(parsed, scope, check=check)
    except (ValueError, TypeError, RecursionError):
        return None
    try:
        import tomlkit

        return tomlkit.dumps(clean)
    except Exception:  # noqa: BLE001 -- the same tree, as JSON, when TOML cannot hold it
        return json.dumps(clean, indent=2, ensure_ascii=False, default=str) + "\n"


def redact_json_text(text: str, scope: Scope, *, check: Callable[[], None] | None = None) -> str | None:
    """A JSON file's text, redacted as a tree (`redact_tree`). None when it is
    not JSON: its text is never written then."""
    try:
        parsed = json.loads(text)
        return json.dumps(redact_tree(parsed, scope, check=check), indent=2, ensure_ascii=False) + "\n"
    except (ValueError, RecursionError):
        return None


# ---------------------------------------------------------------------------
# Reading files: tails, never whole logs
# ---------------------------------------------------------------------------


def read_tail(path: Path, cap: int) -> str | None:
    """The last `cap` bytes of `path` as text, None when it cannot be read. A
    tail that starts mid-line loses that clipped first line: half a record can
    hide half a credential from the scrubber. Only a regular file is opened: a
    FIFO where a log should be would block the reader forever."""
    try:
        if not Path(path).is_file():
            return None
        with open(path, "rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            start = max(0, size - cap)
            handle.seek(start)
            data = handle.read(cap)
    except OSError:
        return None
    if start > 0:
        newline = data.find(b"\n")
        data = data[newline + 1:] if newline >= 0 else b""
    return data.decode("utf-8", errors="replace")


def read_json(path: Path) -> object | None:
    try:
        if not Path(path).is_file():
            return None
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _stamp_age_s(line: str, now: float) -> float | None:
    """How old a log line is, from its own leading timestamp; None when it has none."""
    import calendar

    match = _SERVICE_STAMP.match(line)
    if match:
        try:
            return now - calendar.timegm(time.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S"))
        except ValueError:
            return None
    match = _DEVICE_STAMP.match(line)
    if match:  # `daemon-errors.log` writes local time (`worker._device_error`)
        try:
            return now - time.mktime(time.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S"))
        except (ValueError, OverflowError):
            return None
    return None


def keep_lines(text: str, *, allowed_sessions: set[str], service_only: bool, now: float,
               max_age_s: float | None = LOG_MAX_AGE_S) -> str:
    """The lines of a SHARED log a report may carry: the service's own lines
    only (`service_only`), none older than `max_age_s`, and a line naming a
    session only when that session is one of `allowed_sessions`."""
    kept: list[str] = []
    home = str(Path.home())
    for line in text.splitlines():
        if not line.strip():
            continue
        if service_only and not _SERVICE_LINE.match(line):
            continue
        if max_age_s is not None:
            age = _stamp_age_s(line, now)
            if age is not None and age > max_age_s:
                continue
        # A UUID in this machine's home folder's path (a scratchpad, a CI job's
        # folder) names no session.
        named = {match.lower() for match in UUID.findall(line.replace(home, "~") if len(home) > 1 else line)}
        if named and not named <= allowed_sessions:
            continue
        kept.append(line)
    return "\n".join(kept) + ("\n" if kept else "")


# ---------------------------------------------------------------------------
# Where things are
# ---------------------------------------------------------------------------


def state_root() -> Path:
    """`$XDG_STATE_HOME/probe` (or `~/.local/state/probe`): this process's own."""
    from probe.sdk import session_marker

    return session_marker.state_dir()


def reports_dir() -> Path:
    return state_root() / "daemon" / "reports"


def _safe(session_id: str) -> str:
    """A session id as the daemon names its files (`daemon.store.store_path`)."""
    return "".join(c for c in session_id if c.isalnum() or c in "-_") or "session"


def service_dir() -> Path | None:
    try:
        from probe.service import paths

        return paths.service_dir()
    except Exception:  # noqa: BLE001 -- no service folder: its sources are skipped
        return None


def registry_sessions() -> list[dict]:
    """The Probe service's registered sessions (`sessions.json`), as stored."""
    folder = service_dir()
    if folder is None:
        return []
    data = read_json(folder / "sessions.json")
    sessions = data.get("sessions") if isinstance(data, dict) else None
    return [s for s in sessions if isinstance(s, dict) and isinstance(s.get("sid"), str)] if isinstance(
        sessions, list) else []


def live_sessions() -> list[dict]:
    """Registered sessions that are not off and whose owner still runs (or, with
    no owner, whose registrant re-registered within the heartbeat TTL)."""
    try:
        from probe.service import procid
        from probe.service.registry import HEARTBEAT_TTL_S
    except Exception:  # noqa: BLE001
        return []
    now = time.time()
    live = []
    for session in registry_sessions():
        if session.get("mode") == "off":
            continue
        owner = session.get("owner")
        if isinstance(owner, dict):
            try:
                if procid.alive(int(owner.get("pid") or 0), str(owner.get("start_time") or "")) is False:
                    continue
            except Exception:  # noqa: BLE001 -- unreadable: counted live, as the registry does
                pass
        elif now - float(session.get("heartbeat_at") or 0) >= HEARTBEAT_TTL_S:
            continue
        live.append(session)
    return live


def session_state_root(sid: str) -> Path:
    """The state folder a session registered with the service (plan D13), else
    this process's own."""
    for session in registry_sessions():
        if session.get("sid") == sid and isinstance(session.get("state_dir"), str):
            return Path(session["state_dir"])
    return state_root()


def daemon_key() -> str | None:
    try:
        from probe.sdk.config import load_context

        key = (load_context() or {}).get("companion_token")
    except Exception:  # noqa: BLE001 -- an unreadable config holds no key
        return None
    return key if isinstance(key, str) and key else None


def base_url() -> str | None:
    try:
        from probe.sdk.config import resolve

        return resolve().base_url
    except Exception:  # noqa: BLE001
        return None


def bound(sid: str, root: Path | None = None) -> bool:
    """Is this session's daemon trace folder recorded under THIS server and THIS
    daemon key? The trace shipper's rule (`daemon.shipper.bound_here`), read
    only: a session another account recorded on this machine is not."""
    key, url = daemon_key(), base_url()
    if not key or not url:
        return False
    folder = (root or session_state_root(sid)) / "daemon" / "sessions" / _safe(sid)
    meta = read_json(folder / "meta.json")
    key_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
    return isinstance(meta, dict) and meta.get("base_url") == url.rstrip("/") and meta.get("key") == key_id


def tap_log_paths(sid: str) -> list[tuple[str, Path]]:
    """Each coding agent's tap log for this session, with the agent's id
    (recorder and supervisor; hosted recorder threads write there too)."""
    found = []
    try:
        from probe.harness import get_registry

        for harness in get_registry().captured():
            if harness.capture is None:
                continue
            path = harness.capture.state_dir() / "logs" / f"{_safe(sid)}.log"
            if path.is_file():
                found.append((harness.id, path))
    except Exception:  # noqa: BLE001 -- no registry: no tap logs
        pass
    return found


# ---------------------------------------------------------------------------
# Sources, each in its own budget
# ---------------------------------------------------------------------------


def run_source(name: str, fn: Callable[[], object], budget_s: float,
               skipped: dict[str, str]) -> object | None:
    """`fn()` within `budget_s` seconds of wall-clock time, or None with the
    reason in `skipped`. A source that hangs (a stale network mount, a CLI that
    never answers) is abandoned on its daemon thread: it costs its own source,
    never the report."""
    result: list[object] = []
    error: list[BaseException] = []

    def target() -> None:
        try:
            result.append(fn())
        except BaseException as exc:  # noqa: BLE001 -- recorded as the source's reason
            error.append(exc)

    worker = threading.Thread(target=target, name=f"probe-report-{name}", daemon=True)
    worker.start()
    worker.join(budget_s)
    if worker.is_alive():
        skipped[name] = f"timed out after {budget_s:g} s"
        return None
    if error:
        exc = error[0]
        skipped[name] = f"failed: {type(exc).__name__}"
        return None
    return result[0] if result else None


def _cli_version() -> str:
    try:
        from probe.cli import versions

        return versions.cli_version()
    except Exception:  # noqa: BLE001
        from probe import __version__

        return __version__


def install_facts() -> dict:
    """Versions, how the CLI was installed, the side-by-side installs (active
    and rejected), the daemon's AI libraries and whether the daemon key is held."""
    facts: dict = {}
    try:
        from probe.cli import versions

        facts["versions"] = versions.local_versions()
    except Exception as exc:  # noqa: BLE001
        facts["versions"] = {"cli": _cli_version(), "error": type(exc).__name__}
    try:
        from probe.cli import updater

        facts["install_method"] = updater.detect_install().method
    except Exception:  # noqa: BLE001
        facts["install_method"] = None
    try:
        from probe._shared import installs

        active = installs.active()
        facts["installs"] = {
            "active": active.name if active is not None else None,
            "rejected": sorted(installs.rejected()),
        }
    except Exception:  # noqa: BLE001
        facts["installs"] = None
    try:
        from probe.cli.daemon_cli import located_ai_libraries

        facts["ai_libraries"] = located_ai_libraries() or "missing"
    except Exception:  # noqa: BLE001
        facts["ai_libraries"] = None
    facts["daemon_key_held"] = daemon_key() is not None
    facts["python"] = platform.python_version()
    return facts


#: The service's own records a report carries whole (small JSON files).
SERVICE_RECORDS = ("guard.json", "last-stop.json", "last-crash.json", "service.run", "starts.json", "update.json")


def service_facts(scope: Scope) -> dict:
    """The Probe service's records: the guard's verdict, how it last stopped
    (and crashed), its recent starts, the updater's record, and whether the
    keeper that restarts it is installed."""
    folder = service_dir()
    facts: dict = {"folder_exists": bool(folder and folder.is_dir())}
    if folder is None:
        return facts
    for name in SERVICE_RECORDS:
        data = read_json(folder / name)
        if data is not None:
            facts[name] = redact_tree(data, scope)
    facts["keeper"] = keeper_installed()
    return facts


def keeper_installed() -> bool | None:
    try:
        from probe.service import keeper

        return bool(
            keeper._plist_path().exists()  # noqa: SLF001 -- the keeper's own install paths
            or (keeper._systemd_dir() / f"{keeper.NAME}.timer").exists()  # noqa: SLF001
            or keeper._task_marker().exists()  # noqa: SLF001
        )
    except Exception:  # noqa: BLE001
        return None


def session_facts(sid: str, scope: Scope) -> dict:
    """One session, from its registered state folder: its write lease, its
    switch, whether its worker's lock file is there, and its trace folder's
    reader cursors. Small records only."""
    root = session_state_root(sid)
    facts: dict = {"sid": sid, "state_dir_registered": root != state_root()}
    sessions = root / "sessions"
    facts["lease"] = redact_tree(read_json(sessions / f"{sid}.writer"), scope)
    try:
        facts["state"] = (sessions / f"{sid}.state").read_text(encoding="utf-8").strip()[:32] or None
    except OSError:
        facts["state"] = None
    daemon = root / "daemon"
    facts["worker_lock"] = (daemon / f"{_safe(sid)}.lock").exists()
    trace = daemon / "sessions" / _safe(sid)
    cursors = {}
    for name in ("reader.cursor", "writer.cursor"):
        try:
            cursors[name] = (trace / name).read_text(encoding="utf-8").strip()[:32]
        except OSError:
            continue
    facts["cursors"] = cursors
    for session in registry_sessions():
        if session.get("sid") == sid:
            facts["registered"] = {k: session.get(k) for k in ("harness", "mode", "generation", "registered_at",
                                                                 "heartbeat_at")}
    folder = service_dir()
    recorders = read_json(folder / "recorders.json") if folder else None
    hosted = recorders.get("sessions") if isinstance(recorders, dict) else None
    facts["hosted_recorder"] = bool(
        isinstance(hosted, list) and any(isinstance(s, dict) and s.get("sid") == sid for s in hosted)
    )
    return facts


#: STAFF log tails: name -> cap (plan B1's table).
_TAIL_CAPS = {
    "daemon_errors": 32 * 1024,
    "tap_log": 64 * 1024,
    "worker_output": 64 * 1024,
    "worker_log": 128 * 1024,
    "service_log": 64 * 1024,
    "service_log_1": 32 * 1024,
    "update_log": 32 * 1024,
}


def staff_logs(sid: str | None, allowed: set[str], include_session: bool, now: float,
               skipped: dict[str, str]) -> dict[str, str]:
    """The log tails a STAFF report carries, each scrubbed as one text."""
    logs: dict[str, str] = {}

    def add(name: str, text: str | None) -> None:
        if not text:
            return
        try:
            logs[name] = scrub_for(text, Scope.STAFF)
        except Exception as exc:  # noqa: BLE001 -- withheld, never sent raw
            skipped[name] = f"could not be scrubbed ({type(exc).__name__})"

    errors = read_tail(state_root() / "daemon-errors.log", _TAIL_CAPS["daemon_errors"] * 4)
    if errors:
        add("daemon_errors", _tail_text(keep_lines(errors, allowed_sessions=allowed, service_only=False, now=now),
                                        _TAIL_CAPS["daemon_errors"]))
    folder = service_dir()
    if folder is not None:
        for name, file in (("service_log", "service.log"), ("service_log_1", "service.log.1")):
            text = read_tail(folder / file, _TAIL_CAPS[name] * 4)
            if text:
                add(name, _tail_text(keep_lines(text, allowed_sessions=allowed, service_only=True, now=now),
                                     _TAIL_CAPS[name]))
        add("update_log", read_tail(folder / "update.log", _TAIL_CAPS["update_log"]))
    if sid and include_session:
        root = session_state_root(sid)
        add("worker_output", read_tail(root / "daemon" / f"{_safe(sid)}.log", _TAIL_CAPS["worker_output"]))
        add("worker_log", read_tail(root / "daemon" / "sessions" / _safe(sid) / "worker.log",
                                    _TAIL_CAPS["worker_log"]))
        for index, (_harness, path) in enumerate(tap_log_paths(sid)):
            add("tap_log" if index == 0 else f"tap_log_{index}", read_tail(path, _TAIL_CAPS["tap_log"]))
    return logs


def _tail_text(text: str, cap: int) -> str:
    data = text.encode("utf-8")
    if len(data) <= cap:
        return text
    cut = data[-cap:]
    newline = cut.find(b"\n")
    return cut[newline + 1:].decode("utf-8", errors="replace") if newline >= 0 else ""


def os_label() -> str:
    """`darwin 24.1 arm64`: the system, its release, the machine."""
    label = f"{platform.system().lower()} {platform.release()} {platform.machine()}".strip()
    return label[:OS_MAX_CHARS]


def _harness_slug(value: object) -> str | None:
    return value if isinstance(value, str) and _HARNESS.match(value) else None


# ---------------------------------------------------------------------------
# collect(scope)
# ---------------------------------------------------------------------------


@dataclass
class StaffReport:
    """`collect(Scope.STAFF)`: the report object and what the wire body names."""

    report: dict
    harnesses: list[str] = field(default_factory=list)
    session_ids: list[str] = field(default_factory=list)


def collect(scope: Scope, *, family: str = MANUAL_FAMILY, reason: str = MANUAL_REASON, sid: str | None = None,
            facts: dict | None = None, kind: Kind = Kind.MANUAL, deadline_s: float | None = None):
    """What this machine says about itself, for `scope`.

    STAFF: a `StaffReport` (B1: allowlisted, bound, tail-capped, scrubbed with
    this machine's identity removed). LOCAL: the debug log's files
    (`probe.core.debug_bundle.Collection`, B9: whole files, more sources, home
    paths kept). Same readers, same scrubber."""
    if scope is Scope.LOCAL:
        from probe.core import debug_bundle

        return debug_bundle.collect(deadline_s=deadline_s)
    return _collect_staff(family=family, reason=reason, sid=sid, facts=facts or {}, kind=kind)


def _collect_staff(*, family: str, reason: str, sid: str | None, facts: dict, kind: Kind) -> StaffReport:
    now = time.time()
    skipped: dict[str, str] = {}
    live = run_source("live_sessions", live_sessions, STAFF_SOURCE_BUDGET_S, skipped) or []
    include_session = bool(sid) and bool(run_source("binding", lambda: bound(sid), STAFF_SOURCE_BUDGET_S, skipped))
    if sid:
        allowed = {sid.lower()} if include_session else set()
    else:
        # A machine report: lines naming a live session bound to this account.
        allowed = {
            s["sid"].lower() for s in live
            if run_source(f"binding_{s['sid'][:8]}", lambda s=s: bound(s["sid"]), STAFF_SOURCE_BUDGET_S, skipped)
        }
    report: dict = {
        "scope": Scope.STAFF.value,
        "kind": kind.value,
        "family": family,
        "reason": reason,
        "created_at": int(now),
        "install": run_source("install", install_facts, STAFF_SOURCE_BUDGET_S, skipped),
        "service": run_source("service", lambda: service_facts(Scope.STAFF), STAFF_SOURCE_BUDGET_S, skipped),
        "session": (run_source("session", lambda: session_facts(sid, Scope.STAFF), STAFF_SOURCE_BUDGET_S, skipped)
                    if sid else None),
        "facts": _scrubbed_facts(facts),
        "live_sessions": len(live),
    }
    if kind is Kind.MANUAL:
        report["service_view"] = run_source("service_view", _service_view, STAFF_SOURCE_BUDGET_S, skipped)
        report["codex_hooks"] = run_source("codex_hooks", lambda: _codex_hooks(allowed), STAFF_SOURCE_BUDGET_S * 2,
                                           skipped)
    logs = run_source("logs", lambda: staff_logs(sid, allowed, include_session, now, skipped),
                      STAFF_SOURCE_BUDGET_S * 2, skipped) or {}
    report["logs"] = logs
    if sid and not include_session:
        report["withheld"] = ("this session's logs: its daemon trace folder is not recorded under this "
                              "server and daemon key")
    report["skipped"] = skipped
    _fit(report, REPORT_MAX_BYTES)

    harnesses: list[str] = []
    session_ids: list[str] = []
    if sid:
        session_ids.append(sid)
        harnesses.extend(s.get("harness") for s in registry_sessions() if s.get("sid") == sid)
    elif kind is Kind.MANUAL:
        from probe.sdk import agent_session

        own = agent_session.session_id_from_env()
        if own:
            session_ids.append(own)
        harnesses.extend(s.get("harness") for s in live)
    else:
        session_ids.extend(s["sid"] for s in live)
        harnesses.extend(s.get("harness") for s in live)
    return StaffReport(
        report=report,
        harnesses=list(dict.fromkeys(h for h in map(_harness_slug, harnesses) if h))[:MAX_HARNESSES],
        session_ids=list(dict.fromkeys(s.lower() for s in session_ids if _UUID_EXACT.match(s)))[:MAX_SESSION_IDS],
    )


def _scrubbed_facts(facts: dict) -> dict:
    if not facts:
        return {}
    try:
        return redact_tree(facts, Scope.STAFF)
    except Exception:  # noqa: BLE001 -- withheld, never sent raw
        return {"dropped": "the service's facts could not be scrubbed"}


def _service_view() -> dict:
    """The service's own allowlisted summary (`probe doctor`'s, `service_calls.view`)."""
    from probe.cli import service_calls

    return redact_tree(service_calls.view(timeout=STAFF_SOURCE_BUDGET_S), Scope.STAFF)


def _codex_hooks(allowed: set[str]) -> dict:
    """Which of Probe's hooks Codex runs, as `probe status` reads it (`codex_hooks`):
    a session unknown to the service may be one whose hooks Codex skips. The
    session that never heard them is named only when it is in `allowed`."""
    from probe.cli import codex_hooks

    snapshot = codex_hooks.status_snapshot()
    unheard = snapshot.get("unheard_session")
    if unheard and unheard.lower() not in allowed:
        snapshot["unheard_session"] = "withheld"
    return redact_tree(snapshot, Scope.STAFF)


def _size(value: object) -> int:
    """Bytes as the SDK transport sends them (`json.dumps` with its default
    ASCII escapes): non-ASCII text takes 6 bytes a character there."""
    return len(json.dumps(value).encode("utf-8"))


def _fit(report: dict, cap: int) -> None:
    """Past `cap`, the largest log tail loses its oldest lines first, then the
    facts are cut."""
    logs = report.get("logs") or {}
    while _size(report) > cap and logs:
        name = max(logs, key=lambda key: len(logs[key]))
        lines = logs[name].splitlines(keepends=True)
        if len(lines) <= 1:
            del logs[name]
            continue
        logs[name] = "".join(lines[max(1, len(lines) // 10):])
        report["trimmed"] = True
    if _size(report) > cap:
        report["facts"] = {"dropped": "the report was over its size cap"}
        report["trimmed"] = True


# ---------------------------------------------------------------------------
# Consent and dedupe (automatic reports)
# ---------------------------------------------------------------------------


def disabled(env: Mapping[str, str]) -> str | None:
    """Why an automatic report may not be sent for this consenting environment."""
    from probe._shared import report_policy

    return report_policy.staff_reports_disabled(env, base_url())


def _stamp_path(family: str, scope_key: str, at: float) -> Path:
    window = int(at // DEDUPE_WINDOW_S)
    tag = f"{family}-{scope_key}".replace(":", "~").replace("/", "_")
    return reports_dir() / "stamps" / f"report-{tag}-{window}.stamp"


#: A send that failed on one of these gives its window back (`release`): a
#: later try can land (the network is back, the server too, the rate limit
#: lifted). A report too large, or refused for its credentials, keeps it: the
#: same report would fail the same way.
RELEASED_ON = frozenset({Failure.OFFLINE, Failure.SERVER, Failure.RATE_LIMITED})


def release(family: str, scope_key: str, *, now: float) -> None:
    """Give back the window `claim` took at `now`: its send did not land and a
    retry (the Probe service tries a report it did not land again) may. Never raises."""
    with contextlib.suppress(OSError):
        _stamp_path(family, scope_key, now).unlink()


def claim(family: str, scope_key: str, *, now: float | None = None) -> bool:
    """The one report of `family` for `scope_key` (a session or "machine") in
    this `DEDUPE_WINDOW_S` window, claimed atomically: True for the caller that
    created the window's stamp, False for every other."""
    at = time.time() if now is None else now
    window = int(at // DEDUPE_WINDOW_S)
    path = _stamp_path(family, scope_key, at)
    folder = path.parent
    folder.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        return False
    os.close(fd)
    _prune_stamps(folder, window)
    return True


def _prune_stamps(folder: Path, window: int) -> None:
    for stamp in folder.glob("report-*.stamp"):
        try:
            if int(stamp.stem.rsplit("-", 1)[1]) < window - 1:
                stamp.unlink()
        except (ValueError, IndexError, OSError):
            continue


# ---------------------------------------------------------------------------
# Local copies
# ---------------------------------------------------------------------------


def _write_private(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(tmp)


def newest_first(paths: Iterable[Path]) -> list[Path]:
    """`paths`, the newest modified first (a tie: the later name first). One deleted since it was
    listed (an agent pruning its sessions, another report pruning its copies) is left out: it
    costs only itself, never the caller's whole listing."""
    dated = []
    for path in paths:
        try:
            dated.append((path.stat().st_mtime, path.name, path))
        except OSError:
            continue
    dated.sort(key=lambda row: row[:2], reverse=True)
    return [row[2] for row in dated]


def keep_copy(body: dict, outcome: dict, path: Path | None = None) -> Path:
    """Write (or rewrite) this report's local copy, 0600, and keep only the
    newest `KEEP_REPORTS`."""
    folder = reports_dir()
    if path is None:
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        unique = uuid.uuid4().hex[:8]  # two reports in one second keep two copies
        path = folder / f"report-{stamp}-{unique}-{body.get('family', 'report').replace(':', '~')}.json"
    _write_private(path, json.dumps({"at": int(time.time()), "outcome": outcome, "body": body}, indent=1,
                                    ensure_ascii=False) + "\n")
    copies = newest_first(folder.glob("report-*.json"))
    for old in copies[KEEP_REPORTS:]:
        with contextlib.suppress(OSError):
            old.unlink()
    return path


def last_sent() -> tuple[float, str] | None:
    """When the newest report that reached the Probe team was sent, and its id."""
    best: tuple[float, str] | None = None
    try:
        copies = list(reports_dir().glob("report-*.json"))
    except OSError:
        return None
    for path in copies:
        data = read_json(path)
        outcome = data.get("outcome") if isinstance(data, dict) else None
        if isinstance(outcome, dict) and outcome.get("id") and isinstance(data.get("at"), (int, float)):
            if best is None or data["at"] > best[0]:
                best = (float(data["at"]), str(outcome["id"]))
    return best


# ---------------------------------------------------------------------------
# The wire
# ---------------------------------------------------------------------------


def credentials() -> list[str]:
    """The CLI's token, then the daemon key (the same config context)."""
    tokens: list[str] = []
    try:
        from probe.sdk.config import resolve

        token = resolve().token
        if token:
            tokens.append(token)
    except Exception:  # noqa: BLE001
        pass
    key = daemon_key()
    if key and key not in tokens:
        tokens.append(key)
    return tokens


def failure_for(status: int | None) -> Failure:
    """The contract's error kind for an HTTP status (None: no answer at all)."""
    if status is None:
        return Failure.OFFLINE
    if status in (401, 403):
        return Failure.UNAUTHORIZED
    if status == 413:
        return Failure.TOO_LARGE
    if status == 429:
        return Failure.RATE_LIMITED
    return Failure.SERVER


def api_call(call: Callable, *, timeout: float = UPLOAD_TIMEOUT_S, tokens: list[str] | None = None) -> Reply:
    """One call to the API through the SDK transport (`X-Probe-Device` and the
    CLI's version headers ride along), with each credential in turn: a 401 or
    403 tries the next one. Never retried otherwise, never raises.

    `call(transport)` makes the request with a literal method and path
    (`transport.request("POST", ROUTE, ...)`), so the client/server parity
    check (`tests/test_parity.py`) sees every route this module reaches."""
    from probe.client_headers import client_version_headers
    from probe.sdk import errors
    from probe.sdk.config import Settings, resolve
    from probe.sdk.surface import Surface
    from probe.sdk.transport import Transport

    try:
        url = resolve().base_url
    except Exception:  # noqa: BLE001
        return Reply(status=None, failure=Failure.UNAUTHORIZED)
    tokens = credentials() if tokens is None else tokens
    if not tokens:
        return Reply(status=None, failure=Failure.UNAUTHORIZED)
    last = Reply(status=None, failure=Failure.UNAUTHORIZED)
    for token in tokens:
        try:
            with Transport(
                Settings(base_url=url, token=token),
                timeout=timeout,
                max_retries=0,
                surface=Surface.CLI.value,
                client_headers=client_version_headers(Surface.CLI.value, _cli_version()),
            ) as transport:
                response = call(transport)
            try:
                parsed = response.json()
            except ValueError:
                parsed = None
            return Reply(status=response.status_code, body=parsed if isinstance(parsed, dict) else {}, token=token)
        except errors.RosError as exc:
            status = exc.status if isinstance(exc.status, int) else None
            retry = getattr(exc, "retry_after", None)
            last = Reply(status=status, failure=failure_for(status),
                         retry_after=float(retry) if isinstance(retry, (int, float)) else None)
            if status in (401, 403):
                continue
            return last
        except Exception:  # noqa: BLE001 -- anything else never reached an answer
            return Reply(status=None, failure=Failure.OFFLINE)
    return last


def wire_body(staff: StaffReport, *, kind: Kind, family: str, reason: str) -> dict:
    """The `POST /v1/diagnostics/reports` body (contract, exactly)."""
    try:
        from probe.cli import versions

        local = versions.local_versions()
    except Exception:  # noqa: BLE001
        local = {"cli": _cli_version()}
    body = {
        "schema": SCHEMA,
        "kind": kind.value,
        "family": family,
        "reason": reason,
        "cli_version": str(local.get("cli") or _cli_version())[:VERSION_MAX_CHARS],
        "os": os_label(),
        "harnesses": staff.harnesses,
        "session_ids": staff.session_ids,
        "report": staff.report,
    }
    for name, wire in (("plugin", "plugin_version"), ("tap", "tap_version")):
        if isinstance(local.get(name), str) and local[name]:
            body[wire] = local[name][:VERSION_MAX_CHARS]
    return body


# ---------------------------------------------------------------------------
# One report, end to end
# ---------------------------------------------------------------------------


def send(*, auto: bool, family: str, reason: str, sid: str | None = None, env: Mapping[str, str] | None = None,
         facts: dict | None = None, now: float | None = None) -> Answer:
    """Gate (automatic only), dedupe (automatic only), collect, keep the local
    copy, upload. Never raises on the network's account."""
    kind = Kind.AUTO if auto else Kind.MANUAL
    at = time.time() if now is None else now
    if auto:
        try:
            why = disabled(dict(env or {}))
        except Exception:  # noqa: BLE001 -- consent that cannot be read is no consent
            why = "unreadable"
        if why:
            return Answer(sent=False, skipped=f"{DISABLED}{why}")
        try:
            claimed = claim(family, sid or "machine", now=at)
        except OSError:
            # No stamp, no dedupe: an automatic report is not sent without one.
            return Answer(sent=False, skipped=Failure.SERVER.value)
        if not claimed:
            return Answer(sent=False, skipped=DEDUPED)
    try:
        staff = collect(Scope.STAFF, family=family, reason=reason, sid=sid, facts=facts, kind=kind)
        body = wire_body(staff, kind=kind, family=family, reason=reason)
    except Exception:  # noqa: BLE001 -- a bug here still answers; nothing unscrubbed is sent
        if auto:
            release(family, sid or "machine", now=at)
        return Answer(sent=False, skipped=Failure.SERVER.value)
    path: Path | None
    try:
        path = keep_copy(body, {"sent": False, "id": None, "skipped": "sending"})
    except OSError:
        path = None  # the report is still sent; only the local copy is lost
    reply = api_call(lambda transport: transport.request("POST", ROUTE, json_body=body, idempotent=False))
    report_id = reply.body.get("id") if reply.ok and isinstance(reply.body, dict) else None
    shown = str(path) if path is not None else None
    if reply.ok and isinstance(report_id, str) and report_id:
        answer = Answer(sent=True, id=report_id, path=shown)
    else:
        failure = reply.failure or Failure.SERVER
        answer = Answer(sent=False, skipped=failure.value, path=shown)
        if auto and failure in RELEASED_ON:
            release(family, sid or "machine", now=at)
        if auto and failure is Failure.UNAUTHORIZED and reply.status in (401, 403):
            # A key was tried and refused (a signed-out machine holds none: no alert).
            undeliverable(family, reason, now=at)
    if path is not None:
        with contextlib.suppress(OSError):
            keep_copy(body, {**answer.as_json(), "status": reply.status}, path)
    return answer


def undeliverable(family: str, reason: str, *, now: float | None = None) -> None:
    """Every credential here was refused, so the report cannot reach us: say
    so the one way left, a telemetry event a PostHog destination posts to
    #eng-alerts (`service.report_undeliverable`). Once per family per machine
    per dedupe window (its own claim: the report's is per session, and one
    outage fails every session's). Never raises."""
    try:
        if not claim(f"{family}.undeliverable", "machine", now=now):
            return
        from probe._shared import telemetry

        telemetry.emit_report_undeliverable(family=family, reason=reason, base_url=base_url())
    except Exception:  # noqa: BLE001 -- telemetry never costs the report anything
        pass


def run(request) -> Answer:
    """The `report` read (`probe.core.requests.ReportRequest`)."""
    return send(auto=request.auto, family=request.family, reason=request.reason, sid=request.sid,
                env=request.env or {}, facts=request.facts)


def doctor_row() -> str:
    """`probe doctor`'s row: on (and the last one sent), or off and why."""
    from probe._shared import report_policy

    why = report_policy.staff_reports_disabled(os.environ, base_url())
    if why:
        label = {
            "telemetry_off": "PROBE_TELEMETRY is off",
            "diagnostics_off": "PROBE_DIAGNOSTICS is off",
            "not_hosted": "this server is not Probe's hosted service",
        }.get(why, why)
        return f"off ({label})"
    last = last_sent()
    if last is None:
        return "on · none sent yet"
    when = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(last[0]))
    return f"on · last sent {when} ({last[1]})"
