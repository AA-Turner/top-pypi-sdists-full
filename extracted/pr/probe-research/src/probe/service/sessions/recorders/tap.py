"""find the tap a session's agent installed (through its HarnessIntegration facet), pin a private copy, load it once, and check a session may be recorded with it."""

from __future__ import annotations
import contextlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any


from .. import capture_gate
from ....foundation.service_api import paths
from ...watch.incident import Family
from probe.service.sessions.recorders.recording import DEFERRED_KEY
MAX_ENV = 200
_VERSION = re.compile(r"^\d+(\.\d+)*$")
#: A plugin cache's version folder name (the hooks' `[0-9]*.[0-9]*`, stricter).
_SIBLING = re.compile(r"^\d+(\.\d+)+$")
#: Kimi Code's folder of one tap version (`probe.shared.harness.harnesses.kimi_code.config`): `managed/<id>@<version>`.
_KIMI_TAP = re.compile(r"^probe-research-tap@(\d+(\.\d+)+)$")
KIMI_MANAGED = "managed"
KIMI_LIST = "installed.json"
#: The tap's own floor (`tap.start.MIN_PYTHON`).
MIN_PYTHON = (3, 11)


def _numbers(version: str) -> tuple:
    return tuple(int(p) for p in version.split(".")) if _VERSION.match(version or "") else ()


def _codex_cache(env: dict) -> Path:
    """Codex's plugin cache for a session's environment (as the hooks'
    `dispatch._codex_cache` reads it)."""
    home = (env.get("CODEX_HOME") or "").strip()
    base = Path(os.path.expanduser(home)) if home else Path(env.get("HOME") or os.path.expanduser("~")) / ".codex"
    return base / "plugins" / "cache"


#: A Codex version folder written within this long (its own, `tap/`'s or
#: `hooks/`'s time) may still be being written by Codex: not taken as the
#: installed tap yet (the tap hooks' rule, `installed-tap.sh` TAP_SETTLE_S).
SETTLE_S = 5.0


def _settled(folder: Path, now: float | None = None) -> bool:
    """Were `folder`, its `tap/` and its `hooks/` (those that exist) last
    written at least SETTLE_S ago? False when one cannot be read."""
    now = time.time() if now is None else now
    try:
        for part in (folder, folder / "tap", folder / "hooks"):
            if part.exists() and now - part.stat().st_mtime < SETTLE_S:
                return False
    except (OSError, ValueError):
        return False
    return True


def installed_tap(session: dict, unsettled: list | None = None) -> tuple[str, str] | None:
    """`(root, version)` of the tap folder the session's coding agent has
    installed NOW, beside the version folder the session named (its plugin
    cache's `<marketplace>/<plugin>/<version>/`); None when there is none to
    tell or it cannot be told.

    Claude Code: the one folder its install ledger keeps under the plugin's
    `<plugin>@<marketplace>` (`followup.read_ledger`), never another copy:
    it follows a rollback too. Codex, which records no install and keeps only
    the version folder it installed: the highest version-shaped sibling that
    carries a tap, inside Codex's own cache, and that Codex has stopped
    writing (`_settled`: it picks by listing, and the newest folder may be one
    Codex is still copying; each one skipped for that goes in `unsettled`).
    Kimi Code: the one tap folder its plugin list (`installed.json`) records,
    beside the `managed/probe-research-tap@<version>` folder the session named
    (`_kimi_installed`). A folder elsewhere (a developer's checkout, pi's own
    copy): None."""
    from ...updater import followup

    try:
        here = Path(session["tap_root"]).resolve()
    except (KeyError, TypeError, ValueError, OSError):
        return None
    if _KIMI_TAP.match(here.name):
        return _kimi_installed(here)
    if not _SIBLING.match(here.name):
        return None
    plugin = here.parent
    env = session.get("env") if isinstance(session.get("env"), dict) else {}
    plugins = followup.read_ledger(env)
    key = f"{plugin.name}@{plugin.parent.name}"
    if plugins is not None and key in plugins:
        listed = followup.installed_paths(plugins.get(key))
        if listed is None or len(listed) != 1:
            return None
        target = listed.pop()
        if target.parent != plugin or not _SIBLING.match(target.name) or not _has_tap(target):
            return None
        return str(target), target.name
    try:
        if plugin.parent.parent != _codex_cache(env).resolve():
            return None
        found = [(_numbers(p.name), p) for p in plugin.iterdir() if _SIBLING.match(p.name) and _has_tap(p)]
    except (OSError, ValueError):
        return None
    fresh = [p for _key, p in found if not _settled(p)]
    if unsettled is not None:
        unsettled.extend(str(p) for p in fresh)
    found = [(key, p) for key, p in found if p not in fresh]
    if not found:
        return None
    best = max(found)[1]
    return str(best), best.name


def _kimi_installed(here: Path) -> tuple[str, str] | None:
    """`(root, version)` of the tap Kimi's plugin list records, when it is a
    whole tap folder beside `here` in Kimi's `managed/`; None otherwise (no
    list, none or several recorded, another folder, a tap still incomplete)."""
    managed = here.parent
    if managed.name != KIMI_MANAGED:
        return None
    try:
        records = json.loads((managed.parent / KIMI_LIST).read_text(encoding="utf-8"))["plugins"]
        roots = {Path(r["root"]).resolve() for r in records
                 if isinstance(r, dict) and r.get("id") == "probe-research-tap" and isinstance(r.get("root"), str)}
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None
    if len(roots) != 1:
        return None
    target = roots.pop()
    found = _KIMI_TAP.match(target.name)
    if target.parent != managed or found is None or not _has_tap(target):
        return None
    return str(target), found.group(1)


def _has_tap(root: Path) -> bool:
    """Does `root` hold a tap? False for a folder that cannot be read, or a
    saved path no filesystem call accepts (a NUL byte): one session's bad root
    must never stop another's resume."""
    tap_dir = root / "tap"
    try:
        return (tap_dir / "hosted.py").is_file() and (tap_dir / "main.py").is_file()
    except (OSError, ValueError):
        return False


#: The service's own copies of the taps it loaded (`_pin`), in its machine folder.
TAPS_NAME = "taps"

def _pin(root: str, version: str) -> Path:
    """A copy of the tap package at `root` that only this service writes or
    removes, to import from instead of `root` (plan C7): `<machine folder>/taps/
    <version>-<fingerprint>/tap/`. Raises OSError (the caller loads in place).

    The service imports the tap once and keeps running it for hours or days,
    and the tap reads its own files long after that import: modules it imports
    only when first needed (`from tap import ...` inside functions), data files
    beside them (`harnesses.json`, the companion's rules). A coding agent's
    plugin cache is not the service's to rely on for that long: Codex keeps one
    version folder of a plugin and deletes it when it installs the next
    (audit #14), Claude Code removes old version folders some time after an
    update, Probe prunes Kimi's. Under a tap imported from such a folder, the
    first lazy import after the update failed. A copy is made once per tap
    version and files (a later load of the same files reuses it); old copies are
    removed at a later load, never the one in use (`probe.shared.updates.pins`)."""
    from probe.shared.updates import pins  # noqa: PLC0415 -- only when a tap loads: the start path stays the service's

    store = paths.service_dir() / TAPS_NAME
    target = pins.make(store, version if _VERSION.match(version or "") else None, {"tap": Path(root) / "tap"},
                       default="tap", meta={"from": root})
    pins.prune(store, keep={target})
    return target


def _replacement(root: str) -> tuple[str, str] | None:
    """`(root, version)` of the tap folder that replaced `root`, when `root` is
    a version folder that no longer carries a tap: Codex installs a plugin at
    `<cache>/<marketplace>/<plugin>/<version>/` and REMOVES the old version
    folder when it installs a new one (tests/test_codex_stale_plugin_root.py).
    The highest-numbered version-shaped sibling that carries a tap. (The Codex
    hooks re-resolve their own `$PLUGIN_ROOT` to the newest-modified sibling;
    with the one version folder Codex keeps, both pick the same.) Only
    version-shaped siblings, so a plugin folder beside other plugins is never
    scanned. None otherwise."""
    path = Path(root)
    if not _SIBLING.match(path.name) or _has_tap(path):
        return None
    try:
        found = [(_numbers(p.name), p) for p in path.parent.iterdir() if _SIBLING.match(p.name) and _has_tap(p)]
    except (OSError, ValueError):
        return None
    if not found:
        return None
    best = max(found)[1]
    return str(best), best.name


class TapMixin:
    """Part of RecorderHost: its methods run with `self` the RecorderHost; compose() folds them into RecorderHost."""

    # -- the tap -----------------------------------------------------------------

    def _load(self, root: str, version: str) -> bool:
        """Import `tap` from `root` (once), through the service's own copy of it
        (`_pin`): a plugin cache that deletes the folder later never takes the
        tap's lazy imports and data files with it. False when it cannot be."""
        if self.hosted is not None:
            return True
        if not _has_tap(Path(root)):
            return False
        if sys.version_info < MIN_PYTHON:
            # The tap needs 3.11 (StrEnum); the CLI, and so this service, runs on
            # 3.10 too. `tap watch` then records, on the system python3.
            return False
        source = root
        try:
            root = str(_pin(source, version))
        except (OSError, ValueError) as exc:
            # Loaded in place, as before the copy: a folder that stays works.
            self.log(f"recorder: cannot copy the tap from {source}, loading it in place: {exc!r}")
        if root not in sys.path:
            sys.path.insert(0, root)
        try:
            import importlib

            module = importlib.import_module("tap.hosted")
            importlib.import_module("tap.main")  # the recorder itself: what fails, fails here
            import tap  # noqa: F401

            loaded = getattr(sys.modules.get("tap"), "__version__", "")
        except Exception as exc:  # noqa: BLE001
            self.log(f"cannot load the tap from {source}: {exc!r}")
            # A `tap_load` report, once per tap version (plan B2): its sessions
            # are recorded by their own `tap watch` meanwhile.
            self.incident(Family.TAP_LOAD, "import_failed", None, {"tap_version": version, "error": repr(exc)[:500]},
                          once=f"tap_load:{version}")
            with contextlib.suppress(ValueError):
                sys.path.remove(root)
            # What it imported before failing stays cached otherwise, and the
            # next load (another tap folder) would get this broken one.
            for name in [n for n in sys.modules if n == "tap" or n.startswith("tap.")]:
                sys.modules.pop(name, None)
            return False
        self.hosted, self.tap_root, self.tap_version = module, source, loaded or version
        #: Where it was imported from: the service's copy (`_pin`), or `source` itself.
        self.tap_copy = root
        self.log(f"recorder: tap {self.tap_version} loaded from {source}" + (f" (its copy {root})" if root != source else ""))
        try:
            self.gated = capture_gate.install(self._tap(), self.log)
        except Exception as exc:  # noqa: BLE001 -- a tap without the gate's modules records as before
            self.gated = False
            self.log(f"capture gate: not with tap {self.tap_version} ({type(exc).__name__}: {str(exc)[:200]})")
        try:
            # A refused key stamped where the status line and doctor read it.
            from .. import keylatch

            keylatch.install(self._tap(), self.log)
        except Exception as exc:  # noqa: BLE001 -- never a reason not to record
            self.log(f"key latch: not with tap {self.tap_version} ({type(exc).__name__}: {str(exc)[:200]})")
        return True

    def _tap(self) -> Any:
        """The loaded tap's modules the capture gate works with."""
        if self._tapns is None:
            import importlib
            import types

            names = ("session_journal", "reconcile", "config", "threadenv", "main", "session_identity",
                     "record_client")
            space = types.SimpleNamespace(**{n: importlib.import_module(f"tap.{n}") for n in names})
            try:
                # The tap's own gate, from 0.10.19 (`capture_gate.native`).
                space.capture_gate = importlib.import_module("tap.capture_gate")
            except ImportError:
                space.capture_gate = None
            self._tapns = space
        return self._tapns

    # -- requests -----------------------------------------------------------------

    def _valid(self, params: dict) -> dict:
        from ....foundation.service_api.wire import invalid_params

        sid = params.get("sid")
        if not isinstance(sid, str) or not sid or len(sid) > 128 or "/" in sid:
            raise invalid_params("sid must be a session id")
        for key in ("cwd", "tap_root"):
            value = params.get(key)
            if not isinstance(value, str) or not os.path.isabs(value) or len(value) > 4096:
                raise invalid_params(f"{key} must be an absolute path")
        transcript, folder = params.get("transcript"), params.get("transcript_dir")
        if not (isinstance(transcript, str) and os.path.isabs(transcript)) and not (
            isinstance(folder, str) and os.path.isabs(folder)
        ):
            raise invalid_params("transcript or transcript_dir must be an absolute path")
        env = params.get("env")
        if not isinstance(env, dict) or len(env) > MAX_ENV or not all(
            isinstance(k, str) and isinstance(v, str) and len(v) <= 8192 and "\0" not in v for k, v in env.items()
        ):
            raise invalid_params("env must be an object of at most 200 string variables")
        version = params.get("tap_version")
        if not isinstance(version, str) or not _VERSION.match(version):
            raise invalid_params("tap_version must be a version")
        session = {
            "sid": sid, "cwd": params["cwd"], "transcript": transcript if isinstance(transcript, str) else None,
            "transcript_dir": folder if isinstance(folder, str) else None, "tap_root": params["tap_root"],
            "tap_version": version, "env": dict(env), "owner": params.get("owner"),
        }
        # What `session.register` reads (checked there), kept to register it
        # again after a restart.
        for key in ("harness", "mode", "generation", "state_dir"):
            if key in params:
                session[key] = params[key]
        gaps = capture_gate.gaps_of(params)
        if gaps:
            # Its off stretches (`capture_gate`), kept across restarts.
            session[capture_gate.GAPS_KEY] = gaps
        if params.get(DEFERRED_KEY) is True:
            # Ended while off, not finished yet: a later service retries it slowly.
            session[DEFERRED_KEY] = True
        return session
