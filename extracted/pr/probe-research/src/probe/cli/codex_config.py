"""The one table in ``$CODEX_HOME/config.toml`` this CLI owns.

Codex has no credential-helper hook. The Claude Code plugin ships a
``headersHelper`` that mints an ``Authorization`` header at connect time from the
token the wizard already holds, so Claude never sends anyone to a browser for
the MCP. A plugin-declared HTTP MCP under Codex can only say ``auth: "oauth"``,
which is a SECOND browser approval stacked on the one the wizard just ran --
and it is the step that fails, because it is a three-minute window on a page
nobody explained.

A user-level ``[mcp_servers.<name>]`` entry overrides the plugin-declared one
(same name, one row in ``codex mcp list``, ``auth_status`` flips from
``not_logged_in`` to ``bearer_token``), and it accepts a static header. So the
read token minted by the single approval can serve Codex exactly the way the
headers helper serves Claude Code, with the MCP still hosted by us.

Two Codex behaviours shape everything below, both verified against codex-cli
0.147.0:

* A literal ``bearer_token`` key is not ignored for a streamable HTTP server --
  Codex refuses to load its ENTIRE configuration ("bearer_token is not
  supported for streamable_http") and will not start. The supported spelling is
  ``http_headers``. Nothing here may ever emit ``bearer_token``.
* config.toml belongs to the user, and one syntax error in it takes Codex down
  the same way. Every write parses its own output before replacing anything,
  and a file that does not parse on the way IN is left alone -- a broken config
  is someone else's bug until we touch it, and ours forever after.
"""

from __future__ import annotations

import json
import os
import re
from probe._compat import tomllib
from dataclasses import dataclass
from pathlib import Path

from probe.sdk.agent_session import AGENT_HEADER, AGENT_SESSION_HEADER

#: What this host calls itself on the wire. A CONSTANT for a Codex install, so
#: it rides the static header where it works today -- pointing it at an env var
#: nothing exports would have shipped a header that never arrives.
CODEX_AGENT_LABEL = "codex"

#: What `codex mcp list --json` reports once a static header is in place. The
#: wizard treats it as "authenticated" and skips the OAuth flow.
BEARER_STATUS = "bearer_token"

#: The hosted MCP the SHIPPED plugin manifests declare (`.codex-plugin/
#: plugin.json`, `.mcp.json`, `probe-research-pi/mcp.json` all carry this exact
#: string). Named here because the deployment check in setup.py needs to ask
#: "is this the stock endpoint or a self-hosted one", and a fourth hand-written
#: copy of the literal is how that question starts being answered differently
#: in different files.
PRODUCTION_MCP_URL = "https://mcp.research.prbe.ai/mcp"


class ConfigError(Exception):
    """A refusal to write, carrying the reason for the caller to surface.

    Never a crash: every caller has a working fallback (Codex's own OAuth), so
    the shortcut declining is a slower install, not a failed one.
    """


@dataclass(frozen=True)
class WriteResult:
    path: Path
    changed: bool
    #: The file's exact contents before this write, or None when it did not
    #: exist. Kept so a caller that cannot CONFIRM the result can undo it: a
    #: config we broke is not something to leave behind and fall back from,
    #: because "Codex will not start" outlives whatever we were installing.
    previous: str | None = None


def codex_home() -> Path:
    """``$CODEX_HOME``, else ``~/.codex`` -- the same resolution Codex uses."""
    configured = os.environ.get("CODEX_HOME")
    return Path(configured).expanduser() if configured else Path.home() / ".codex"


def config_path() -> Path:
    return codex_home() / "config.toml"


def plugin_mcp_url(name: str, *, marketplace: str) -> str | None:
    """The URL the installed Codex plugin declares for `name`, if it can be read.

    Taken from the plugin's own cached manifest rather than a constant here, so
    the entry we register points at whatever that install actually uses -- a
    self-hosted deployment included. No manifest means no shortcut: registering
    a guessed URL would point Codex at the wrong server with a valid token.
    """
    root = codex_home() / "plugins" / "cache" / marketplace / name
    if not root.is_dir():
        return None
    for version_dir in sorted(root.iterdir(), reverse=True):
        manifest = version_dir / ".codex-plugin" / "plugin.json"
        try:
            declared = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        servers = declared.get("mcpServers")
        if not isinstance(servers, dict):
            continue
        entry = servers.get(name)
        if isinstance(entry, dict) and isinstance(entry.get("url"), str):
            return entry["url"]
    return None


def configured_bearer(name: str, *, path: Path | None = None) -> str | None:
    """The token currently in the header we wrote, or None if there is no entry.

    Rotation is the reason this exists. `codex mcp list` reports `bearer_token`
    for ANY header, valid or not, so Codex's own view cannot tell a current
    credential from one revoked a week ago -- it says "authenticated" either
    way, right up until every call 401s.
    """
    target = path or config_path()
    try:
        parsed = tomllib.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    entry = (parsed.get("mcp_servers") or {}).get(name)
    if not isinstance(entry, dict):
        return None
    header = (entry.get("http_headers") or {}).get("Authorization")
    if not isinstance(header, str) or not header.startswith("Bearer "):
        return None
    return header[len("Bearer ") :].strip() or None


def _toml_string(value: str) -> str:
    """A TOML basic string. `json.dumps` escapes exactly what TOML needs here."""
    return json.dumps(value)


def needs_header_migration(name: str, *, path: Path | None = None) -> bool:
    """Is `name`'s table written in the pre-`env_http_headers` shape?

    The token-rotation path in setup.py returns early when the stored token
    still matches, which is right for a rotation and WRONG for a shape change:
    an install whose token never rotates would keep the old table forever and
    never gain the agent-session header. This is the second reason to rewrite.
    """
    target = path or config_path()
    try:
        parsed = tomllib.loads(target.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        # Unreadable or broken is NOT "needs migration": the writer refuses a
        # broken file anyway, and claiming otherwise would make every run try
        # and fail to rewrite it.
        return False
    entry = (parsed.get("mcp_servers") or {}).get(name)
    if not isinstance(entry, dict):
        return False
    return not isinstance(entry.get("env_http_headers"), dict)


def _header_patterns(name: str) -> tuple[re.Pattern[str], re.Pattern[str]]:
    """Match `[mcp_servers.name]` and its sub-tables, quoted or bare.

    `codex mcp add` writes the bare spelling; a hand-edited file may quote it.
    Missing the quoted form would append a SECOND table for the same server.
    """
    escaped = re.escape(name)
    key = rf'(?:{escaped}|"{escaped}")'
    exact = re.compile(rf"^\s*\[\s*mcp_servers\s*\.\s*{key}\s*\]\s*(?:#.*)?$")
    child = re.compile(rf"^\s*\[\s*mcp_servers\s*\.\s*{key}\s*\.")
    return exact, child


def _table_span(lines: list[str], name: str) -> tuple[int, int] | None:
    """The half-open line range holding `name`'s table and any sub-tables."""
    exact, child = _header_patterns(name)
    start = next((i for i, line in enumerate(lines) if exact.match(line)), None)
    if start is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].lstrip()
        if stripped.startswith("[") and not child.match(lines[index]):
            end = index
            break
    return start, end


def _validated(text: str, *, what: str) -> None:
    try:
        tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"{what} is not valid TOML ({exc})") from exc


def _replace_span(text: str, span: tuple[int, int] | None, block: str) -> str:
    lines = text.splitlines(keepends=True)
    if span is None:
        prefix = text if not text or text.endswith("\n") else text + "\n"
        separator = "\n" if prefix.strip() else ""
        return f"{prefix}{separator}{block}"
    start, end = span
    return "".join(lines[:start]) + block + "".join(lines[end:])


def write_mcp_bearer(name: str, *, url: str, token: str, path: Path | None = None) -> WriteResult:
    """Point Codex's `name` MCP at `url` with a static Authorization header.

    Replaces the whole table rather than patching keys inside it: a leftover
    `bearer_token_env_var` from an earlier shape would otherwise sit alongside
    the header, and a leftover `oauth` key would keep Codex asking to log in.
    """
    target = path or config_path()
    existed = True
    try:
        original = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        original, existed = "", False
    except OSError as exc:
        raise ConfigError(f"could not read {target}: {exc}") from exc

    if original.strip():
        # Refuse a file that is already broken. Rewriting part of it would make
        # us the author of a config Codex cannot load.
        _validated(original, what=str(target))

    # `env_http_headers` reads the named environment variables at CONNECT time
    # and omits a header whose variable is unset -- verified against codex-cli
    # 0.151.0, which sends `x-probe-agent-session` when CODEX_THREAD_ID is
    # exported and simply leaves it out when it is not.
    #
    # Codex does not populate CODEX_THREAD_ID in the parent today: MCP servers
    # connect before a thread exists. This is written anyway, because it costs a
    # line and starts working the day that changes -- and because the alternative
    # reading, that the transport cannot carry the id, is false and would have
    # sent us building a worse fix. The agent's own shell DOES see the variable,
    # which is what `search_knowledge(exclude_session=...)` is for meanwhile.
    block = (
        f"[mcp_servers.{name}]\n"
        f"url = {_toml_string(url)}\n"
        f"http_headers = {{ Authorization = {_toml_string(f'Bearer {token}')}, "
        f"{_toml_string(AGENT_HEADER)} = {_toml_string(CODEX_AGENT_LABEL)} }}\n"
        f"env_http_headers = {{ "
        f"{_toml_string(AGENT_SESSION_HEADER)} = \"CODEX_THREAD_ID\" }}\n"
    )
    span = _table_span(original.splitlines(keepends=True), name)
    updated = _replace_span(original, span, block)
    previous = original if existed else None
    if updated == original:
        return WriteResult(path=target, changed=False, previous=previous)

    _validated(updated, what="the updated Codex config")

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".probe.tmp")
    try:
        temporary.write_text(updated, encoding="utf-8")
        # The file now holds a credential. It may not have before.
        temporary.chmod(0o600)
        os.replace(temporary, target)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise ConfigError(f"could not write {target}: {exc}") from exc
    return WriteResult(path=target, changed=True, previous=previous)


def restore(result: WriteResult) -> None:
    """Undo a `write_mcp_bearer`, byte for byte.

    The verification after a write is not decoration: `codex mcp list` failing
    is exactly what a config Codex cannot load looks like, and at that point we
    are one step away from having bricked its CLI. Restoring is unconditional
    and best-effort -- an exception here would replace a recoverable state with
    a traceback over the top of it.
    """
    try:
        if result.previous is None:
            result.path.unlink(missing_ok=True)
        else:
            result.path.write_text(result.previous, encoding="utf-8")
    except OSError:
        pass


def remove_mcp_server(name: str, *, path: Path | None = None) -> WriteResult:
    """Drop the table again, for uninstall.

    Leaving it behind would point Codex at the hosted MCP with a token the
    uninstall just orphaned -- a server that reads as installed and answers 401.
    """
    target = path or config_path()
    try:
        original = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return WriteResult(path=target, changed=False)
    except OSError as exc:
        raise ConfigError(f"could not read {target}: {exc}") from exc

    if not original.strip():
        return WriteResult(path=target, changed=False)
    _validated(original, what=str(target))

    span = _table_span(original.splitlines(keepends=True), name)
    if span is None:
        return WriteResult(path=target, changed=False)
    lines = original.splitlines(keepends=True)
    updated = "".join(lines[: span[0]]) + "".join(lines[span[1] :])
    _validated(updated, what="the updated Codex config")

    temporary = target.with_name(target.name + ".probe.tmp")
    try:
        temporary.write_text(updated, encoding="utf-8")
        temporary.chmod(0o600)
        os.replace(temporary, target)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise ConfigError(f"could not write {target}: {exc}") from exc
    return WriteResult(path=target, changed=True)


def read_top_level(key: str, *, path: Path | None = None) -> tuple[bool, object]:
    """`(readable, value)` of a top-level `key`, value None when absent. A file
    that does not parse is `(False, None)`: never guessed at, never rewritten."""
    target = path or config_path()
    try:
        original = target.read_text(encoding="utf-8")
    except FileNotFoundError:
        return True, None
    except (OSError, UnicodeDecodeError):
        return False, None
    try:
        return True, tomllib.loads(original).get(key)
    except tomllib.TOMLDecodeError:
        return False, None


def _first_table(lines: list[str]) -> int:
    """Index of the first REAL table header, or len(lines). A line opening with
    `[` counts only when the text above it parses on its own: inside a
    multi-line string or array (a markdown link in a prompt, a nested list) it
    is part of a value, and a key put above it would land inside that value."""
    for index, line in enumerate(lines):
        if not line.lstrip().startswith("["):
            continue
        try:
            tomllib.loads("".join(lines[:index]))
        except tomllib.TOMLDecodeError:
            continue
        return index
    return len(lines)


def write_top_level(key: str, value: str | None, *, path: Path | None = None) -> WriteResult:
    """Set ONE top-level string key, or remove it with None, touching no other line.

    A top-level key must come before the first table header, so a new one goes
    right above it and an existing one is replaced in place. A key of the same
    name inside a table (a profile's own) is not top-level and is left alone.
    The same rules as `write_mcp_bearer`: a file that does not parse is refused,
    and the result must parse AND read back as `value` -- checked even when
    nothing changed, so a removal that found no line to remove is an error,
    never a silent success. A symlinked file (a dotfile manager's) is written
    through, and its line endings and mode are kept (0600 when new: it holds
    MCP tokens)."""
    target = path or config_path()
    if target.is_symlink():
        target = Path(os.path.realpath(target))
    try:
        # Bytes, not `read_text`: that would turn a CRLF file into LF on write.
        original = target.read_bytes().decode("utf-8")
        existed = True
    except FileNotFoundError:
        original, existed = "", False
    except (OSError, UnicodeDecodeError) as exc:
        raise ConfigError(f"could not read {target}: {exc}") from exc
    if original.strip():
        _validated(original, what=str(target))

    newline = "\r\n" if "\r\n" in original else "\n"
    lines = original.splitlines(keepends=True)
    first_table = _first_table(lines)
    pattern = re.compile(rf'^\s*(?:{re.escape(key)}|"{re.escape(key)}")\s*=')
    found = next((i for i in range(first_table) if pattern.match(lines[i])), None)
    new_line = None if value is None else f"{key} = {_toml_string(value)}{newline}"
    if found is not None:
        lines[found:found + 1] = [] if new_line is None else [new_line]
    elif new_line is not None:
        if first_table and not lines[first_table - 1].endswith("\n"):
            lines[first_table - 1] += newline
        spacer = [newline] if first_table < len(lines) else []
        lines[first_table:first_table] = [new_line, *spacer]
    updated = "".join(lines)
    previous = original if existed else None

    if updated != original:
        _validated(updated, what="the updated Codex config")
    if tomllib.loads(updated).get(key) != value:
        raise ConfigError(f"could not set {key} in {target}: it would not read back as written")
    if updated == original:
        return WriteResult(path=target, changed=False, previous=previous)

    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".probe.tmp")
    try:
        mode = target.stat().st_mode & 0o7777 if existed else 0o600
        temporary.write_bytes(updated.encode("utf-8"))
        temporary.chmod(mode)
        os.replace(temporary, target)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise ConfigError(f"could not write {target}: {exc}") from exc
    return WriteResult(path=target, changed=True, previous=previous)
