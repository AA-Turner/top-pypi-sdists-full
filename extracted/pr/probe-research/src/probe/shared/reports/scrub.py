"""redact credentials from text, HTTP headers, parsed config files and environments, per Scope."""

from __future__ import annotations
import json
import re
from collections.abc import Callable, Mapping
from pathlib import Path

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
    from probe.foundation.compat.compat import tomllib

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
from probe.shared.reports.argv import redact_command  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.reports.reports import Scope  # noqa: E402 -- pieces need each other; the front door loads this one first
