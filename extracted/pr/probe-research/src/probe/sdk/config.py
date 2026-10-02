"""SDK credential + endpoint resolution.

Precedence (highest first): explicit argument -> environment -> config file.

Env vars:
  PROBE_BASE_URL      e.g. https://api.research.prbe.ai
  PROBE_TOKEN         a user API token (probe_pat_...) for /v1
  PROBE_MCP_TOKEN     a read-only token for the MCP surface (see mcp_token below)
  PROBE_SERVICE_TOKEN a read-only egress token (probe_svc_...) for the read-only Reader
  PROBE_INGEST_TOKEN  an ingest token (ros_ing_...) for /ingest
  PROBE_HMAC_SECRET   optional shared secret for the X-Signature body HMAC on /ingest
  PROBE_WORKSPACE     the active workspace id, overriding the context file
  PROBE_PROJECT       the active project id/slug, overriding the context file
  PROBE_HEARTBEAT_SECONDS  run auto-heartbeat interval (default 60; <=0 disables —
                      see Run.start_heartbeat; env only, not read from this file)
  PROBE_MODE          what probe.init() does: `online` (default), `disabled` (a
                      no-op run, no network, no files; see sdk/disabled.py) or
                      `offline` (record with no network, `probe sync` later;
                      see sdk/offline.py)
  PROBE_INIT_FALLBACK `offline`: when an online probe.init() runs out of its
                      budget, record offline instead of raising
  PROBE_INIT_TIMEOUT_SEC  how long probe.init() retries an unreachable or failing
                      API before raising (default 90; 0 = a few quick retries only)

Config file: $XDG_CONFIG_HOME/probe/config.json (default ~/.config/probe/config.json),
written by the Probe wizard's sign-in (``npx probe-research``), which captures the token
via the browser handoff; ``probe wizard --action login --token`` is the air-gap-friendly
paste path.

``mcp_token`` is deliberately a separate credential from ``token``: the MCP surface is
read-only, so it holds a ``scopes:['read']`` token that cannot write even if it leaks
(it is handed to an MCP client, which is a wider blast radius than the CLI). Nothing
falls back from one to the other — the wizard writes it.

Shape (v2)
----------
The file holds *named contexts*, kubectl-style, so one machine can address several
endpoints or tenants without re-running ``login``::

    {
      "version": 2,
      "current_context": "default",
      "contexts": {
        "default": {
          "base_url": "...", "token": "...", "mcp_token": "...",
          "workspace": {"id": "<uuid>", "project": "<uuid-or-slug>"}
        }
      }
    }

**The active project nests *inside* ``workspace`` rather than sitting beside it.** That
makes "a project from workspace A while workspace B is active" unrepresentable instead of
merely invalid: ``workspace use`` replaces the whole object, so a project cannot outlive
the workspace it belongs to. No validation code, because the bad state has no encoding.
Two workspace+project pairs at once? That is what a second *context* is for.

v1 (a flat ``{base_url, token, ...}``) is migrated **in memory on read**. Reads never
write the file back: a read-only command must not rewrite a config that may be symlinked
into a dotfiles repo (``save_file`` resolves symlinks for the same reason). The file is
rewritten in v2 the next time something genuinely saves.
"""

from __future__ import annotations

import json
import os
import stat
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from probe._compat import StrEnum
from pathlib import Path

from . import homedir

DEFAULT_BASE_URL = "https://api.research.prbe.ai"

# Repository configs contain preferences, never data blobs. Their bound prevents a
# repository symlink to a device or an accidental giant file from exhausting a hook/CLI
# process before JSON validation gets a chance to fail. Machine configs predate this
# feature and remain size-unbounded for compatibility.
FOLDER_CONFIG_MAX_BYTES = 64 * 1024

CONFIG_VERSION = 2
DEFAULT_CONTEXT = "default"

# Per-context credential/endpoint keys. Used to migrate a v1 file and to decide what
# `clear_context` strips — anything outside this set is somebody else's key and is left
# alone rather than silently dropped on the floor.
_CONTEXT_KEYS = (
    "base_url",
    "token",
    "mcp_token",
    "service_token",
    "ingest_token",
    "hmac_secret",
    "workspace",
)



#: The config path the Probe daemon's shell runs with: a file that never exists, so
#: a `probe` started from that shell has no key (`probe.daemon.shell.minimal_env`).
DAEMON_SHELL_CONFIG = "/nonexistent/probe-daemon-shell/config.json"

def config_path() -> Path:
    """`PROBE_CONFIG_PATH`, then `XDG_CONFIG_HOME`, then `~/.config`.

    THE OVERRIDE IS HONOURED HERE BECAUSE IT IS HONOURED EVERYWHERE ELSE. Four
    other readers already take `PROBE_CONFIG_PATH` first -- `version_policy`,
    `capabilities`, `_telemetry_core` and `sdk.session_marker` -- and this
    module, which is the one that WRITES the file, was the lone holdout. The two
    sets agreed only in production, so a value written here landed in
    `~/.config` while every reader that honours the override looked somewhere
    else: the setting worked in the field and silently vanished under any test
    or dev environment that set it. `version_policy.base_url` documented that
    divergence rather than fixing it; this is the fix.
    """
    override = os.environ.get("PROBE_CONFIG_PATH")
    if override:
        return Path(override)
    base = os.environ.get("XDG_CONFIG_HOME")
    root = Path(base) if base else homedir.home() / ".config"
    return root / "probe" / "config.json"


def _migrate(data: dict) -> dict:
    """Return ``data`` in v2 shape. Pure — never touches disk."""
    if not data:
        return {}
    if isinstance(data.get("contexts"), dict):
        data.setdefault("version", CONFIG_VERSION)
        data.setdefault("current_context", DEFAULT_CONTEXT)
        return data
    # v1: a flat credential blob. Everything in it belongs to one context. Carry
    # unrecognized keys across too — a key we do not know about is more likely a newer
    # client's than junk, and dropping credentials on read would be unrecoverable.
    #
    # EXCEPT `defaults`, which is hoisted back to the top level. It mirrors
    # session_marker.DEFAULTS_KEY and is machine-wide BY CONTRACT — never a
    # context's. CLIs through 0.95.1 wrote it into v1-shaped files raw, so
    # wrapping it into the context here would bury the preference where
    # `default_tracking` never looks, and a researcher's explicit "off"
    # would silently become "on" at the next canonical write.
    flat = dict(data)
    defaults = flat.pop("defaults", None)
    migrated = {
        "version": CONFIG_VERSION,
        "current_context": DEFAULT_CONTEXT,
        "contexts": {DEFAULT_CONTEXT: flat},
    }
    if isinstance(defaults, dict):
        migrated["defaults"] = defaults
    elif defaults is not None:
        # Not ours if it is not a dict — leave it where it was found.
        flat["defaults"] = defaults
    return migrated


class ConfigUnreadable(Exception):
    """The config file exists but could not be parsed.

    Distinct from "no config yet" on purpose: the two look identical to a reader but
    must never look identical to a WRITER. See :func:`load_file`.
    """


def _read_config_text(
    path: Path,
    *,
    require_regular: bool = False,
    max_bytes: int | None = None,
) -> str:
    """Read one config, optionally applying the repository-file safety policy.

    Machine configs keep their established ``Path.read_text`` semantics. Folder configs
    pass ``require_regular=True`` and a byte limit: ``O_NONBLOCK`` then makes opening a
    FIFO/device fail fast, and ``fstat`` validates the same fd that is read. Symlinks to
    ordinary files remain supported.
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

    Readers get ``{}`` for an unreadable file too — degrading to "unconfigured" is
    the right call for a read, and ``mcp/server.py`` calls ``.get()`` on this
    unguarded. Writers must pass ``strict=True``: they read-modify-write the whole
    file, so treating a corrupt file as empty would REPLACE every stored context
    with whatever is being saved. One truncated byte would otherwise take every
    token for every endpoint on the machine, and exit 0 doing it.
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
    return data.get("current_context") or DEFAULT_CONTEXT


def load_context(name: str | None = None) -> dict:
    """The flat credential dict for one context. ``{}`` when it does not exist.

    This is what callers that used to read ``load_file()`` for a credential want;
    ``load_file()`` now means "the whole file, every context".
    """
    data = load_file()
    contexts = data.get("contexts")
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

    ``os.replace`` gives atomicity, not isolation: two ``probe`` processes can both
    read the file, each add their own context, and the second write silently drops
    the first — while both report success. That is reachable from ordinary use (a CI
    matrix, two worktree sessions, `project use` racing an auto-login), and losing a
    context means losing its token.

    An O_EXCL lockfile, best-effort: a stale lock from a killed process must never
    brick the CLI, so an old one is broken rather than waited on forever.
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
    # Write a complete file then swap it in: a crash mid-write would otherwise leave
    # truncated JSON, which load_file() reads as {} — silently losing every credential.
    # Follow a symlink first: os.replace would swap the *link* for a regular file, so a
    # config symlinked into a dotfiles repo would silently stop tracking. The temp file
    # is created 0600 and must share the target's directory for os.replace to be atomic.
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

    Read-modify-write of the *file*, so saving one context never drops another. A key
    set to None is removed, which is how a credential gets cleared without clearing
    its neighbours.
    """
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True) or {
            "version": CONFIG_VERSION,
            "current_context": DEFAULT_CONTEXT,
            "contexts": {},
        }
        data.setdefault("contexts", {})
        target = name or current_context_name(data)
        ctx = dict(data["contexts"].get(target) or {})
        for key, value in updates.items():
            if value is None:
                ctx.pop(key, None)
            else:
                ctx[key] = value
        data["contexts"][target] = ctx
        data["current_context"] = data.get("current_context") or target
        data["version"] = CONFIG_VERSION
        _save_json_file(target_path, data, private=True, _resolved=True)
        return path


def use_context(name: str) -> Path:
    """Make ``name`` active, creating it empty if it does not exist yet."""
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True) or {
            "version": CONFIG_VERSION,
            "contexts": {},
        }
        data.setdefault("contexts", {}).setdefault(name, {})
        data["current_context"] = name
        data["version"] = CONFIG_VERSION
        _save_json_file(target_path, data, private=True, _resolved=True)
        return path


def delete_context(name: str) -> Path:
    """Drop a context. Clearing the active one leaves ``current_context`` dangling,
    so fall back to whatever remains (or the default name) to keep the file coherent."""
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True)
        contexts = data.get("contexts") or {}
        contexts.pop(name, None)
        data["contexts"] = contexts
        if data.get("current_context") == name:
            data["current_context"] = next(iter(contexts), DEFAULT_CONTEXT)
        _save_json_file(target_path, data, private=True, _resolved=True)
        return path


def clear_context(name: str | None = None) -> Path:
    """Strip credentials from one context, leaving other contexts untouched.

    Signing out used to delete the whole file. With named contexts that is wrong:
    logging out of staging would silently sign you out of prod too.
    """
    path = config_path()
    target_path = _write_target(path)
    with _config_lock(target_path, _resolved=True):
        data = _load_json_file(target_path, strict=True, migrate=True)
        contexts = data.get("contexts")
        if not isinstance(contexts, dict):
            return path
        target = name or current_context_name(data)
        if target in contexts:
            # Wipe, do not subtract known keys. Removing only what `_CONTEXT_KEYS` lists
            # would fail OPEN: `_migrate` deliberately carries unrecognized keys across
            # (they are more likely a newer client's than junk), so a credential this
            # version has never heard of would survive every logout.
            contexts[target] = {}
        data["contexts"] = contexts
        # Strip stray TOP-LEVEL credentials too. `_migrate` returns a v2 file untouched,
        # so a hybrid written by an OLDER probe (which read v2, saw no top-level keys,
        # and wrote `token` at the root) keeps that key forever — and it would outlive
        # every logout while still authenticating an old client.
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
) -> Settings:
    """Merge explicit args, env, and the config file into one Settings object."""
    file = load_context(context)
    anchor = file.get("workspace") if isinstance(file.get("workspace"), dict) else {}
    return Settings(
        # PROBE_BASE_URL outranks the context file and must keep doing so: the hosted
        # MCP pods set it (deploy/mcp/k8s.yaml) to the in-cluster service, and a context
        # that could outrank it would point production at the wrong API — while /healthz
        # still returned 200. tests/test_config_contexts.py guards this ordering.
        base_url=(
            base_url or os.environ.get("PROBE_BASE_URL") or file.get("base_url") or DEFAULT_BASE_URL
        ).rstrip("/"),
        token=token or os.environ.get("PROBE_TOKEN") or file.get("token"),
        # A read-only egress credential (probe_svc_) for an external product. Like
        # mcp_token it can never write; unlike it, it is team-scoped and userless.
        service_token=(
            service_token or os.environ.get("PROBE_SERVICE_TOKEN") or file.get("service_token")
        ),
        # Env first keeps every shell that already exports PROBE_MCP_TOKEN working
        # unchanged. Never falls back to `token`: that one can write.
        mcp_token=mcp_token or os.environ.get("PROBE_MCP_TOKEN") or file.get("mcp_token"),
        ingest_token=(
            ingest_token or os.environ.get("PROBE_INGEST_TOKEN") or file.get("ingest_token")
        ),
        hmac_secret=(hmac_secret or os.environ.get("PROBE_HMAC_SECRET") or file.get("hmac_secret")),
        # Ambient anchors are a convenience, never a requirement: an explicit flag or an
        # env var always wins, so scripts and CI never depend on a developer's context.
        workspace=workspace or os.environ.get("PROBE_WORKSPACE") or anchor.get("id"),
        project=project or os.environ.get("PROBE_PROJECT") or anchor.get("project"),
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


def resolve_mode(explicit: str | None = None) -> Mode:
    """``probe.init(mode=)``, else ``PROBE_MODE``, else online.

    An unknown value RAISES rather than falling back to online: someone who
    typed ``PROBE_MODE=disable`` to keep a job off the network must not have it
    quietly go on the network."""
    raw = explicit if explicit is not None else os.environ.get(MODE_ENV, "")
    value = str(raw).strip().lower() or Mode.ONLINE.value
    try:
        return Mode(value)
    except ValueError:
        from .errors import ValidationError

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
        from . import safe_warn

        safe_warn.warn(
            f"{INIT_TIMEOUT_ENV}={raw!r} is not a number of seconds; "
            f"using {DEFAULT_INIT_TIMEOUT_SEC:g}"
        )
        return DEFAULT_INIT_TIMEOUT_SEC
