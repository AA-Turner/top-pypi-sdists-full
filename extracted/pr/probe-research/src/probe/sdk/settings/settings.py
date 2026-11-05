"""SDK credential + endpoint resolution.

Precedence (highest first): explicit argument -> environment -> config file.

Env vars:
  PROBE_BASE_URL      e.g. https://api.research.prbe.ai
  PROBE_TOKEN         a user API token (probe_pat_...) for /v1
  PROBE_MCP_TOKEN     a read-only token for the MCP surface (see mcp_token below)
  PROBE_MCP_URL       the Probe MCP to read from (default: the stock MCP, only beside
                      the stock API; see mcp_url)
  PROBE_SERVICE_TOKEN a read-only egress token (probe_svc_...) for the read-only Reader
  PROBE_INGEST_TOKEN  an ingest token (ros_ing_...) for /ingest
  PROBE_HMAC_SECRET   optional shared secret for the X-Signature body HMAC on /ingest
  PROBE_WORKSPACE     this computer's workspace (an id or a slug), overriding the context file
  PROBE_WORKSPACE_LIMIT  limit this process's reads to one workspace (an id or a slug), or
                      `team` for none, overriding the context's limit (`workspace_limit.py`)
  PROBE_WORKSPACE_LIMIT_TEAM_ITEMS  `show` (default) or `hide` team-wide items under that limit
  PROBE_PROJECT       the active project id/slug, overriding the context file
  PROBE_HEARTBEAT_SECONDS  run auto-heartbeat interval (default 60; <=0 disables —
                      see Run.start_heartbeat; env only, not read from this file)
  PROBE_MODE          what probe.init() does: `online` (default), `disabled` (a
                      no-op run, no network, no files; see sdk/run/disabled.py) or
                      `offline` (record with no network, `probe sync` later;
                      see sdk/delivery/offline/offline.py)
  PROBE_INIT_FALLBACK `offline`: when an online probe.init() runs out of its
                      budget, record offline instead of raising
  PROBE_INIT_TIMEOUT_SEC  how long probe.init() retries an unreachable or failing
                      API before raising (default 90; 0 = a few quick retries only)

Config file: $XDG_CONFIG_HOME/probe/config.json (default ~/.config/probe/config.json),
written by the Probe wizard's sign-in (``npx probe-research``), which captures the token
via the browser handoff; ``probe wizard --action login --token`` is the air-gap-friendly
paste path.

``mcp_token`` is a separate credential from ``token``: it is a ``scopes:['read']`` token
handed to an MCP client (wider blast radius than the CLI), so it cannot write if leaked.
Nothing falls back from one to the other; the wizard writes it.

Shape (v2)
----------
Named contexts, kubectl-style: one machine, several endpoints or tenants::

    {
      "version": 2,
      "current_context": "default",
      "contexts": {
        "default": {
          "base_url": "...", "token": "...", "mcp_token": "...",
          "workspace": {"id": "<uuid>", "project": "<uuid-or-slug>",
                        "limit": true, "team_items": "show", "name": "...", "slug": "..."}
        }
      }
    }

``limit`` / ``team_items`` / ``name`` / ``slug`` are this computer's WORKSPACE LIMIT
(`probe workspace limit`, `probe.sdk.settings.workspace_limit`): when ``limit`` is true
every request names ``id`` and the API narrows reads to it. Absent or false is the whole
team; ``id`` is the filing pin either way.

**The active project nests *inside* ``workspace``**, so "a project from workspace A while
B is active" is unrepresentable: ``workspace use`` replaces the whole object. Two
workspace+project pairs at once is what a second *context* is for.

v1 (a flat ``{base_url, token, ...}``) is migrated **in memory on read**, never written
back (the config may be symlinked into a dotfiles repo; ``save_file`` resolves symlinks
too). It becomes v2 on the next genuine save.
"""

from __future__ import annotations

import json
import os
import stat
import tempfile
import time
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING
from probe.foundation.compat.compat import StrEnum
from pathlib import Path

from ...foundation.durable import homedir
from .workspace_limit import LIMIT_ENV

if TYPE_CHECKING:
    from .workspace_limit import WorkspaceLimit

DEFAULT_BASE_URL = "https://api.research.prbe.ai"
#: The hosted Probe MCP that serves the stock API's tenants.
STOCK_MCP_URL = "https://mcp.research.prbe.ai/mcp"

# Repository configs are preferences, so they are size-bounded: a repo symlink to a device or
# a giant file must not exhaust a hook/CLI process. Machine configs stay unbounded (compat).
FOLDER_CONFIG_MAX_BYTES = 64 * 1024

CONFIG_VERSION = 2
DEFAULT_CONTEXT = "default"

# Environment variables the settings read.
BASE_URL_ENV = "PROBE_BASE_URL"
TOKEN_ENV = "PROBE_TOKEN"
SERVICE_TOKEN_ENV = "PROBE_SERVICE_TOKEN"
MCP_TOKEN_ENV = "PROBE_MCP_TOKEN"
MCP_URL_ENV = "PROBE_MCP_URL"
INGEST_TOKEN_ENV = "PROBE_INGEST_TOKEN"
HMAC_SECRET_ENV = "PROBE_HMAC_SECRET"
WORKSPACE_ENV = "PROBE_WORKSPACE"
PROJECT_ENV = "PROBE_PROJECT"
RUN_ID_ENV = "PROBE_RUN_ID"
CONFIG_PATH_ENV = "PROBE_CONFIG_PATH"
XDG_CONFIG_HOME_ENV = "XDG_CONFIG_HOME"

# Config-file keys: per-context credentials, then the file's top-level keys.
BASE_URL_KEY = "base_url"
TOKEN_KEY = "token"
MCP_TOKEN_KEY = "mcp_token"
SERVICE_TOKEN_KEY = "service_token"
INGEST_TOKEN_KEY = "ingest_token"
HMAC_SECRET_KEY = "hmac_secret"
WORKSPACE_KEY = "workspace"
PROJECT_KEY = "project"
ID_KEY = "id"
VERSION_KEY = "version"
CURRENT_CONTEXT_KEY = "current_context"
CONTEXTS_KEY = "contexts"
DEFAULTS_KEY = "defaults"

# Per-context credential/endpoint keys: migrate v1 and decide what a top-level strip removes.
_CONTEXT_KEYS = (
    BASE_URL_KEY,
    TOKEN_KEY,
    MCP_TOKEN_KEY,
    SERVICE_TOKEN_KEY,
    INGEST_TOKEN_KEY,
    HMAC_SECRET_KEY,
    WORKSPACE_KEY,
)

#: Context key, LEGACY: the old one-time handover and the old `probe workspace use --clear`
#: both wrote it. Nothing writes it now; with no pin it still reads as cleared.
WORKSPACE_HANDOVER = "workspace_handover"

#: Context key: the person ran `probe workspace use --clear`, so nothing re-pins their
#: home workspace on this computer (`Client._pin_home_workspace`, the setup wizard).
WORKSPACE_CLEARED = "workspace_cleared"


def is_workspace_cleared(context: dict) -> bool:
    """Whether this computer's workspace was cleared on purpose (the new key or the legacy one).

    Only means something while the context has no pin: a later pick wins over a clear."""
    return bool(context.get(WORKSPACE_CLEARED) or context.get(WORKSPACE_HANDOVER))


#: Context updates that end an earlier clear: merged into every pin pick or loss that is
#: not `probe workspace use --clear`, so a stale flag never refuses a later create.
WORKSPACE_CLEAR_RESET = {WORKSPACE_CLEARED: None, WORKSPACE_HANDOVER: None}


class WorkspaceSource(StrEnum):
    """Where `Settings.workspace` came from (`resolve`): only a PIN is this computer's to drop."""

    EXPLICIT = "explicit"  # resolve(workspace=...)
    ENV = "env"  # PROBE_WORKSPACE
    LIMIT = "limit"  # PROBE_WORKSPACE_LIMIT, filing where it can see
    PIN = "pin"  # the context's saved pin (`probe workspace use`, the setup wizard)


class ProjectSource(StrEnum):
    """Where `Settings.project` came from (`resolve`): a run opens in this session's
    project ahead of a CONTEXT one, never ahead of the other two (`runs/home.py`)."""

    EXPLICIT = "explicit"  # resolve(project=...)
    ENV = "env"  # PROBE_PROJECT
    CONTEXT = "context"  # the context's saved project (`probe project use`)


#: Config path for the daemon's shell: never exists, so its `probe` has no key (`probe.daemon.shell.runner.minimal_env`).
DAEMON_SHELL_CONFIG = "/nonexistent/probe-daemon-shell/config.json"

#: A per-run token (app/auth/run_tokens.py) records ONE run; the prefix names the kind, the server verifies.
RUN_TOKEN_PREFIX = "probe_run_"


def run_token_run_id(token: str | None) -> str | None:
    """The run a per-run token records (its `rid` claim), else None. Read WITHOUT verifying:
    this only routes the attach; the server checks signature, run and expiry per request."""
    if not token or not token.startswith(RUN_TOKEN_PREFIX):
        return None
    import base64

    try:
        payload = token[len(RUN_TOKEN_PREFIX):].split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(payload + "=" * (-len(payload) % 4)))
    except (IndexError, ValueError, UnicodeDecodeError):
        return None
    rid = claims.get("rid") if isinstance(claims, dict) else None
    return rid if isinstance(rid, str) and rid else None


def env_run_id() -> str:
    """The run this process must join: PROBE_RUN_ID, else the one a per-run PROBE_TOKEN records ("" for neither)."""
    return os.environ.get(RUN_ID_ENV, "").strip() or (
        run_token_run_id(os.environ.get(TOKEN_ENV)) or ""
    )


def mcp_url(base_url: str) -> str | None:
    """The MCP for a credential belonging to `base_url`: `PROBE_MCP_URL`, else the stock MCP
    beside the stock API, else none (a key must never go to a deployment that did not mint
    it). Used by the daemon's reader and `probe mcp tools|call`."""
    explicit = os.environ.get(MCP_URL_ENV)
    if explicit:
        return explicit
    from urllib.parse import urlparse

    return STOCK_MCP_URL if urlparse(base_url).netloc == urlparse(DEFAULT_BASE_URL).netloc else None


def config_path() -> Path:
    """`PROBE_CONFIG_PATH`, then `XDG_CONFIG_HOME`, then `~/.config`.

    The override must be honoured HERE because `version_policy`, `capabilities`,
    `_telemetry_core` and `sdk.session_marker` honour it: when only this writer ignored
    it, values landed in `~/.config` while readers looked elsewhere, so settings
    vanished under any test/dev environment that set it.
    """
    override = os.environ.get(CONFIG_PATH_ENV)
    if override:
        return Path(override)
    base = os.environ.get(XDG_CONFIG_HOME_ENV)
    root = Path(base) if base else homedir.home() / ".config"
    return root / "probe" / "config.json"


def _migrate(data: dict) -> dict:
    """Return ``data`` in v2 shape. Pure — never touches disk."""
    if not data:
        return {}
    if isinstance(data.get(CONTEXTS_KEY), dict):
        data.setdefault(VERSION_KEY, CONFIG_VERSION)
        data.setdefault(CURRENT_CONTEXT_KEY, DEFAULT_CONTEXT)
        return data
    # v1: a flat credential blob; all of it is one context. Unknown keys are carried across
    # too (likelier a newer client's than junk; dropping credentials on read is unrecoverable).
    #
    # EXCEPT `defaults`, hoisted to the top level: it mirrors session_marker.DEFAULTS_KEY and
    # is machine-wide BY CONTRACT. CLIs through 0.95.1 wrote it raw into v1 files; wrapping it
    # in the context would bury it where `default_tracking` never looks and turn an explicit
    # "off" into "on" at the next write.
    flat = dict(data)
    defaults = flat.pop(DEFAULTS_KEY, None)
    migrated = {
        VERSION_KEY: CONFIG_VERSION,
        CURRENT_CONTEXT_KEY: DEFAULT_CONTEXT,
        CONTEXTS_KEY: {DEFAULT_CONTEXT: flat},
    }
    if isinstance(defaults, dict):
        migrated[DEFAULTS_KEY] = defaults
    elif defaults is not None:
        # Not ours if it is not a dict — leave it where it was found.
        flat[DEFAULTS_KEY] = defaults
    return migrated


class ConfigUnreadable(Exception):
    """The config file exists but could not be parsed.

    Distinct from "no config yet": identical to a reader, never to a WRITER. See :func:`load_file`.
    """


def _read_config_text(
    path: Path,
    *,
    require_regular: bool = False,
    max_bytes: int | None = None,
) -> str:
    """Read one config; folder configs pass ``require_regular=True`` and a byte limit
    (``O_NONBLOCK`` fails fast on a FIFO/device; ``fstat`` validates the fd that is read;
    symlinks to regular files work). Machine configs keep plain ``Path.read_text``.
    """
    if not require_regular:
        return path.read_text(encoding="utf-8")

    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_BINARY", 0)
    fd = os.open(path, flags)
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise ValueError(f"{path} is not a regular file")
        if max_bytes is not None and info.st_size > max_bytes:
            raise ValueError(f"{path} exceeds the {max_bytes}-byte size limit")
        chunks: list[bytes] = []
        remaining = None if max_bytes is None else max_bytes + 1
        while remaining is None or remaining:
            chunk = os.read(fd, 16 * 1024 if remaining is None else min(16 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            if remaining is not None:
                remaining -= len(chunk)
        raw = b"".join(chunks)
        if max_bytes is not None and len(raw) > max_bytes:
            raise ValueError(f"{path} exceeds the {max_bytes}-byte size limit")
        return raw.decode("utf-8")
    finally:
        os.close(fd)


def _load_json_file(
    path: Path,
    *,
    strict: bool = False,
    migrate: bool = False,
    require_regular: bool = False,
    max_bytes: int | None = None,
) -> dict:
    """Read one JSON-object config, optionally migrating the machine shape.

    Readers get ``{}`` for an unreadable file too (``mcp/server/server.py`` calls ``.get()``
    unguarded). Writers must pass ``strict=True``: a corrupt file read as empty would
    REPLACE every stored context, so one truncated byte would drop every token on the
    machine and exit 0.
    """
    try:
        raw = _read_config_text(
            path,
            require_regular=require_regular,
            max_bytes=max_bytes,
        )
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as exc:
        if strict:
            raise ConfigUnreadable(
                f"{path} exists but could not be read ({exc}). Refusing to overwrite it "
                "— move it aside if you meant to start fresh."
            ) from exc
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        if strict:
            raise ConfigUnreadable(
                f"{path} exists but could not be read ({exc}). Refusing to overwrite it "
                "— move it aside if you meant to start fresh."
            ) from exc
        return {}
    if not isinstance(data, dict):
        if strict:
            raise ConfigUnreadable(
                f"{path} is not a JSON object. Refusing to overwrite it — move it aside "
                "if you meant to start fresh."
            )
        return {}
    return _migrate(data) if migrate else data


def load_file(*, strict: bool = False) -> dict:
    """The raw machine config, migrated to v2 in memory. ``{}`` when absent."""
    return _load_json_file(config_path(), strict=strict, migrate=True)


def current_context_name(data: dict | None = None) -> str:
    data = load_file() if data is None else data
    return data.get(CURRENT_CONTEXT_KEY) or DEFAULT_CONTEXT


def normalize_endpoint(url: str | None) -> str:
    """`url` as two endpoints compare: stripped, no trailing slash, the scheme and host lower
    case, and https's default port (`:443`) dropped. `""` for none; a string that is not a URL
    comes back stripped. The one rule for "is this the address a key was stored for"
    (`probe.service.actions.caller.known_endpoint`, the wizard's checks)."""
    from urllib.parse import urlsplit, urlunsplit

    text = (url or "").strip().rstrip("/")
    try:
        parts = urlsplit(text)
    except ValueError:
        return text
    if not parts.scheme or not parts.netloc:
        return text
    scheme = parts.scheme.lower()
    userinfo, at, hostport = parts.netloc.rpartition("@")
    hostport = hostport.lower()
    if scheme == "https" and hostport.endswith(":443"):
        hostport = hostport[: -len(":443")]
    return urlunsplit((scheme, f"{userinfo}{at}{hostport}", parts.path.rstrip("/"), parts.query, parts.fragment))


def load_context(name: str | None = None) -> dict:
    """The flat credential dict for one context. ``{}`` when it does not exist.

    ``load_file()`` is the whole file, every context.
    """
    data = load_file()
    contexts = data.get(CONTEXTS_KEY)
    if not isinstance(contexts, dict):
        return {}
    ctx = contexts.get(name or current_context_name(data))
    return ctx if isinstance(ctx, dict) else {}


def _write_target(path: Path) -> Path:
    """Canonical target shared by a write's lock, strict read and replacement."""
    return path.resolve()


@contextmanager
def _config_lock(path: Path | None = None, *, _resolved: bool = False):
    """Serialize read-modify-write of the config across processes.

    ``os.replace`` is atomic, not isolated: two processes (CI matrix, two worktree sessions,
    `project use` racing auto-login) can each add a context and the second write silently
    drops the first, losing its token.

    An O_EXCL lockfile, best-effort: a stale lock from a killed process is broken, never waited on forever.
    """
    requested = config_path() if path is None else path
    target = requested if _resolved else _write_target(requested)
    lock = target.with_suffix(".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    acquired = False
    for _ in range(50):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(fd)
            acquired = True
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > 30:
                    lock.unlink(missing_ok=True)  # stale: holder died
                    continue
            except OSError:
                pass
            time.sleep(0.1)
    try:
        yield
    finally:
        if acquired:
            lock.unlink(missing_ok=True)


def _save_json_file(
    path: Path,
    data: dict,
    *,
    private: bool,
    _resolved: bool = False,
    max_bytes: int | None = None,
) -> Path:
    """Atomically replace one JSON config, optionally enforcing its output size."""
    target = path if _resolved else _write_target(path)
    payload = json.dumps(data, indent=2, sort_keys=True).encode("utf-8")
    if max_bytes is not None and len(payload) > max_bytes:
        raise ConfigUnreadable(
            f"{path} would exceed the {max_bytes}-byte size limit. Refusing to overwrite it."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    # Write a whole file then swap: a crash mid-write would leave truncated JSON, read as {}
    # (every credential lost). The target is symlink-resolved first (os.replace would swap the
    # *link* and stop tracking a dotfiles symlink); the 0600 temp file shares its directory so the replace is atomic.
    try:
        existing_mode = target.stat().st_mode & 0o777
    except OSError:
        existing_mode = None
    fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=".config-", suffix=".json")
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
        if not private:
            os.chmod(tmp, existing_mode if existing_mode is not None else 0o644)
        os.replace(tmp, target)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    if private:
        # tokens live in the machine config; keep it user-only.
        try:
            target.chmod(0o600)
        except OSError:
            pass
    return path


def save_file(data: dict) -> Path:
    path = config_path()
    _save_json_file(_write_target(path), data, private=True, _resolved=True)
    return path


def save_context(updates: dict, *, name: str | None = None) -> Path:
    """Merge ``updates`` into one context and persist the whole file.

    Read-modify-write of the *file*, so one context never drops another. A key set to None
    is removed (clears a credential without its neighbours).
    """
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True) or {
            VERSION_KEY: CONFIG_VERSION,
            CURRENT_CONTEXT_KEY: DEFAULT_CONTEXT,
            CONTEXTS_KEY: {},
        }
        data.setdefault(CONTEXTS_KEY, {})
        target = name or current_context_name(data)
        ctx = dict(data[CONTEXTS_KEY].get(target) or {})
        for key, value in updates.items():
            if value is None:
                ctx.pop(key, None)
            else:
                ctx[key] = value
        data[CONTEXTS_KEY][target] = ctx
        data[CURRENT_CONTEXT_KEY] = data.get(CURRENT_CONTEXT_KEY) or target
        data[VERSION_KEY] = CONFIG_VERSION
        _save_json_file(target_path, data, private=True, _resolved=True)
        return path


def use_context(name: str) -> Path:
    """Make ``name`` active, creating it empty if it does not exist yet."""
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True) or {
            VERSION_KEY: CONFIG_VERSION,
            CONTEXTS_KEY: {},
        }
        data.setdefault(CONTEXTS_KEY, {}).setdefault(name, {})
        data[CURRENT_CONTEXT_KEY] = name
        data[VERSION_KEY] = CONFIG_VERSION
        _save_json_file(target_path, data, private=True, _resolved=True)
        return path


def delete_context(name: str) -> Path:
    """Drop a context; if it was active, ``current_context`` falls back to a remaining one (or the default name)."""
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True)
        contexts = data.get(CONTEXTS_KEY) or {}
        contexts.pop(name, None)
        data[CONTEXTS_KEY] = contexts
        if data.get(CURRENT_CONTEXT_KEY) == name:
            data[CURRENT_CONTEXT_KEY] = next(iter(contexts), DEFAULT_CONTEXT)
        _save_json_file(target_path, data, private=True, _resolved=True)
        return path


def clear_context(name: str | None = None) -> Path:
    """Strip credentials from one context, leaving other contexts untouched.

    Not the whole file: logging out of staging must not sign you out of prod.
    """
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True)
        contexts = data.get(CONTEXTS_KEY)
        if not isinstance(contexts, dict):
            return path
        target = name or current_context_name(data)
        if target in contexts:
            # Wipe, do not subtract known keys: removing only `_CONTEXT_KEYS` would fail OPEN
            # (`_migrate` carries unknown keys, so an unfamiliar credential would survive logout).
            contexts[target] = {}
        data[CONTEXTS_KEY] = contexts
        # Strip stray TOP-LEVEL credentials too: an OLDER probe could write `token` at the root
        # of a v2 file (`_migrate` leaves it), outliving every logout and still authenticating.
        for key in _CONTEXT_KEYS:
            data.pop(key, None)
        _save_json_file(target_path, data, private=True, _resolved=True)
        return path


def clear_file() -> None:
    path = config_path()
    try:
        path.unlink()
    except FileNotFoundError:
        pass


@dataclass
class Settings:
    base_url: str
    token: str | None = None
    mcp_token: str | None = None
    service_token: str | None = None
    ingest_token: str | None = None
    hmac_secret: str | None = None
    workspace: str | None = None
    project: str | None = None
    #: This computer's workspace limit (`workspace_limit`), None for the whole team. Only
    #: `resolve()` fills it: hand-built `Settings` (sign-in, key checks, logout) carry none.
    workspace_limit: "WorkspaceLimit | None" = None
    #: Where `workspace` came from; only `resolve()` fills it (None: hand-built, never dropped).
    workspace_source: WorkspaceSource | None = None
    #: Where `project` came from; only `resolve()` fills it (None: hand-built, read as explicit).
    project_source: ProjectSource | None = None


def resolve(
    *,
    base_url: str | None = None,
    token: str | None = None,
    mcp_token: str | None = None,
    service_token: str | None = None,
    ingest_token: str | None = None,
    hmac_secret: str | None = None,
    workspace: str | None = None,
    project: str | None = None,
    context: str | None = None,
    env: Mapping[str, str] | None = None,
) -> Settings:
    """Merge explicit args, env, and the config file into one Settings object.

    `env`: variables to read instead of this process's (the daemon host answers a session's
    read with that session's key and URL: `probe.daemon.host.reads`). The config file is found as always."""
    from .workspace_limit import Source, resolve_limit

    env = os.environ if env is None else env
    file = load_context(context)
    anchor = file.get(WORKSPACE_KEY) if isinstance(file.get(WORKSPACE_KEY), dict) else {}
    limit = resolve_limit(file, env)
    # A job limited by `PROBE_WORKSPACE_LIMIT` files into that workspace too unless
    # PROBE_WORKSPACE says otherwise (else it would create work it cannot see).
    env_limited = limit.ref if limit is not None and limit.source is Source.ENV and env.get(
        LIMIT_ENV, ""
    ).strip() else None
    sources = (
        (workspace, WorkspaceSource.EXPLICIT),
        (env.get(WORKSPACE_ENV), WorkspaceSource.ENV),
        (env_limited, WorkspaceSource.LIMIT),
        (anchor.get(ID_KEY), WorkspaceSource.PIN),
    )
    workspace_source = next((source for value, source in sources if value), None)
    projects = (
        (project, ProjectSource.EXPLICIT),
        (env.get(PROJECT_ENV), ProjectSource.ENV),
        (anchor.get(PROJECT_KEY), ProjectSource.CONTEXT),
    )
    project, project_source = next(((value, source) for value, source in projects if value), (None, None))
    return Settings(
        # PROBE_BASE_URL must outrank the context file: hosted MCP pods set it
        # (deploy/mcp/k8s.yaml) to the in-cluster service, and a context outranking it would
        # point production at the wrong API while /healthz stays 200 (tests/test_config_contexts.py).
        base_url=(
            base_url or env.get(BASE_URL_ENV) or file.get(BASE_URL_KEY) or DEFAULT_BASE_URL
        ).rstrip("/"),
        token=token or env.get(TOKEN_ENV) or file.get(TOKEN_KEY),
        # Read-only egress credential (probe_svc_) for an external product: team-scoped, userless.
        service_token=(
            service_token or env.get(SERVICE_TOKEN_ENV) or file.get(SERVICE_TOKEN_KEY)
        ),
        # Env first keeps shells exporting PROBE_MCP_TOKEN working. Never falls back to `token` (writable).
        mcp_token=mcp_token or env.get(MCP_TOKEN_ENV) or file.get(MCP_TOKEN_KEY),
        ingest_token=(
            ingest_token or env.get(INGEST_TOKEN_ENV) or file.get(INGEST_TOKEN_KEY)
        ),
        hmac_secret=(hmac_secret or env.get(HMAC_SECRET_ENV) or file.get(HMAC_SECRET_KEY)),
        # Ambient anchors are a convenience: an explicit flag or env var wins, so CI never depends on a developer's context.
        workspace=workspace or env.get(WORKSPACE_ENV) or env_limited or anchor.get(ID_KEY),
        project=project,
        workspace_limit=limit,
        workspace_source=workspace_source,
        project_source=project_source,
    )


# -- probe.init() behaviour (plan 2.5) ----------------------------------------
MODE_ENV = "PROBE_MODE"
INIT_TIMEOUT_ENV = "PROBE_INIT_TIMEOUT_SEC"
DEFAULT_INIT_TIMEOUT_SEC = 90.0


class Mode(StrEnum):
    """What ``probe.init()`` does. W&B's ``WANDB_MODE`` vocabulary."""

    #: Talk to the API (the default).
    ONLINE = "online"
    #: Return a run that does nothing: no client, no network, no outbox.
    DISABLED = "disabled"
    #: Train with no API and deliver later with `probe sync` (plan 2.12).
    OFFLINE = "offline"


def keep_stored_keys_home(settings: Settings, stored: Mapping, context_name: str | None = None) -> Settings:
    """Plan D26: a stored key is only ever sent to the address it was stored for. Where `settings`
    aim elsewhere (an address from the environment, a registry entry, a pinned op), only the
    environment's own keys go there: the stored login's that `resolve` may have paired with it are
    dropped. AuthError when no key is left. The one rule for the drain and the box watcher."""
    from .. import errors
    from ..session_marker import WIZARD_HINT

    stored_base = normalize_endpoint(stored.get("base_url") or DEFAULT_BASE_URL)
    if stored_base == normalize_endpoint(settings.base_url):
        return settings
    if settings.token and settings.token == stored.get("token") and not os.environ.get("PROBE_TOKEN"):
        settings.token = None
    if (settings.ingest_token and settings.ingest_token == stored.get("ingest_token")
            and not os.environ.get("PROBE_INGEST_TOKEN")):
        settings.ingest_token = None
    if not (settings.token or settings.ingest_token):
        raise errors.AuthError(
            f"the login stored for context {context_name or '<default>'} is {stored_base}'s, never sent to "
            f"{settings.base_url}; set PROBE_TOKEN for that address ({WIZARD_HINT})"
        )
    return settings


def resolve_mode(explicit: str | None = None) -> Mode:
    """``probe.init(mode=)``, else ``PROBE_MODE``, else online.

    An unknown value RAISES, not falls back to online: ``PROBE_MODE=disable`` must not quietly go online."""
    raw = explicit if explicit is not None else os.environ.get(MODE_ENV, "")
    value = str(raw).strip().lower() or Mode.ONLINE.value
    try:
        return Mode(value)
    except ValueError:
        from ..errors import ValidationError

        choices = ", ".join(mode.value for mode in Mode)
        raise ValidationError(
            f"{MODE_ENV}={raw!r} is not a mode; use one of: {choices}"
        ) from None


def init_timeout_seconds() -> float:
    """``PROBE_INIT_TIMEOUT_SEC`` (default 90). 0 keeps the old quick-fail behaviour;
    an unreadable value warns and keeps the default."""
    raw = os.environ.get(INIT_TIMEOUT_ENV, "").strip()
    if not raw:
        return DEFAULT_INIT_TIMEOUT_SEC
    try:
        return max(0.0, float(raw))
    except ValueError:
        from ...foundation.safe_warn import safe_warn

        safe_warn.warn(
            f"{INIT_TIMEOUT_ENV}={raw!r} is not a number of seconds; "
            f"using {DEFAULT_INIT_TIMEOUT_SEC:g}"
        )
        return DEFAULT_INIT_TIMEOUT_SEC
