"""What `probe uninstall` owns on this computer, as exact paths (clean-uninstall plan U-T1).

The plan is computed once, before anything is touched, and written to
`S/uninstall/plan.json` (S = `~/.local/state/probe`): a rerun of an
interrupted uninstall works from it, and the finisher (`probe/_shared/
finisher.py`) deletes from it, generation-bound (a path is deleted only while
it is still what the plan saw). Shape (the build contract; `stage`,
`empty_only`, `witness`, `install_lock`, `contexts` and `kept` are additions):

    {"v": 1, "created_at", "machine_key",
     "paths": [{"path", "kind": "file|dir|link", "inode", "mtime", "owner": "probe",
                "stage": "state|finish", "empty_only"?, "witness"?: {"path", "inode", "mtime"}}],
     "agent_edits": [{"agent", "traces": {trace: [what]}}],
     "server": {"device_ids": [device instance ids], "installation_ids": [uuid],
                "contexts": {name: {"base_url", "installation_ids"}}},
     "env_generations": [abs paths], "shims": [abs paths],
     "install_lock", "config", "kept": [what is left on purpose, and why]}

What is Probe's, exactly:

    the CLI       every env generation (the uv tool path when it is a folder,
                  every `probe-versions/<v>/`), the tool path's link, the
                  `probe-versions/` bookkeeping, and the shims uv's receipts
                  name, only while they still point into those envs: never a
                  `probe*` glob, never a file another tool made in the bin dir.
                  Every recorded tool dir: UV_TOOL_DIR, `uv tool dir`, the
                  versions record's `tools`, and the one this CLI runs from.
    state         every child of Probe's state folders (`~/.local/state/probe`,
                  the XDG one, those live sessions named), except another
                  machine's service folder in a shared home and `uninstall/`
                  itself; `probe-telemetry` (identity), the cache, the
                  transcript journal, the `$TMPDIR` fallback outboxes, the tap
                  state folders, the keeper's units, and on macOS the desktop
                  app's data and (where writable) its bundle
    agents        each agent's traces (`uninstall_agents.traces`)

Kept, and said so: an outbox root `PROBE_OUTBOX_DIR` names outside those
folders (it may be a folder of the researcher's), a researcher's
`.probe.config` files, project venvs, uv itself.
"""

from __future__ import annotations

import json
import os
import re
import stat
import sys
import time
from pathlib import Path

PLAN_VERSION = 1
STAGE_STATE = "state"
STAGE_FINISH = "finish"
KIND_FILE = "file"
KIND_LINK = "link"
KIND_DIR = "dir"
#: A machine's service folder name (`paths.machine_key`).
MACHINE_KEY = re.compile(r"^[0-9a-f]{16}$")
#: The desktop app (prbe-ai/desktop): its bundle id, its data and logs (macOS).
DESKTOP_BUNDLE_ID = "ai.prbe.desktop"
DESKTOP_APP = "Probe.app"


def with_witness(record: dict | None, witness: Path) -> dict | None:
    """`record` (a folder's) with the file made once with it (an env's
    `pyvenv.cfg`): the finisher keeps a folder made again with the old inode."""
    if record is None:
        return None
    try:
        st = os.lstat(witness)
    except OSError:
        return record
    return {**record, "witness": {"path": str(witness), "inode": st.st_ino, "mtime": st.st_mtime}}


def entry(path: Path | str, *, stage: str, empty_only: bool = False) -> dict | None:
    """The plan's record of one path as it is now; None when it is not there
    or is not this user's."""
    try:
        st = os.lstat(path)
    except OSError:
        return None
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        return None
    if stat.S_ISLNK(st.st_mode):
        kind = KIND_LINK
    elif stat.S_ISDIR(st.st_mode):
        kind = KIND_DIR
    else:
        kind = KIND_FILE
    record = {"path": str(path), "kind": kind, "inode": st.st_ino, "mtime": st.st_mtime, "owner": "probe",
              "stage": stage}
    if empty_only:
        record["empty_only"] = True
    return record


# -- the CLI ------------------------------------------------------------------------


def tool_dirs() -> list[Path]:
    """Every uv tool folder Probe's CLI may be installed in."""
    from probe._shared import installs

    found: list[Path] = []

    def add(path) -> None:
        if path is None:
            return
        path = Path(path)
        if path not in found and (path.is_dir() or os.path.lexists(path / installs.DIST)):
            found.append(path)

    try:
        primary = installs.tool_dir()
    except Exception:  # noqa: BLE001
        primary = None
    add(primary)
    if primary is not None:
        recorded = installs.record(primary).get("tools")
        if isinstance(recorded, str) and recorded:
            add(recorded)
    running = installs.versions_root_of()
    if running is not None:
        add(running.parent / "tools")
        recorded = installs.record(running.parent / "tools").get("tools")
        if isinstance(recorded, str) and recorded:
            add(recorded)
    prefix = Path(sys.prefix)
    if prefix.name == installs.DIST and prefix.parent.name == "tools":
        add(prefix.parent)
    return found


def primary_versions_root() -> Path:
    """The versions folder whose install lock the uninstall holds: the one
    this CLI runs from, else the uv tool folder's."""
    from probe._shared import installs

    running = installs.versions_root_of()
    if running is not None:
        return running
    dirs = tool_dirs()
    return installs.versions_root(dirs[0] if dirs else None)


def _receipt_shims(env: Path) -> list[Path]:
    from probe._compat import tomllib

    try:
        tool = tomllib.loads((env / "uv-receipt.toml").read_text(encoding="utf-8")).get("tool") or {}
    except (OSError, ValueError):
        return []
    out = []
    for point in tool.get("entrypoints") or []:
        where = point.get("install-path") if isinstance(point, dict) else None
        if isinstance(where, str) and os.path.isabs(where):
            out.append(Path(where))
    return out


def _points_into(link: Path, roots: list[Path]) -> bool:
    try:
        target = os.readlink(link)
    except OSError:
        return False
    target = os.path.normpath(os.path.join(os.path.dirname(link), target))
    for root in roots:
        for spelling in {str(root), os.path.realpath(root)}:
            if target == spelling or target.startswith(spelling.rstrip(os.sep) + os.sep):
                return True
    return False


def cli_layout() -> dict:
    """The CLI's own files: `paths` (stage finish), `env_generations`, `shims`."""
    from probe._shared import handoff, installs

    paths: list[dict] = []
    envs: list[Path] = []
    shims: list[Path] = []
    for tools in tool_dirs():
        env = installs.tool_env(tools)
        versions = installs.versions_root(tools)
        roots = [env, versions]
        receipts = []
        if installs.is_link(env):
            paths.append(entry(env, stage=STAGE_FINISH))
            receipts.append(env)  # the active env's receipt, through the link
        elif env.is_dir():
            envs.append(env)
            receipts.append(env)
            paths.append(with_witness(entry(env, stage=STAGE_FINISH), env / "pyvenv.cfg"))
        if versions.is_dir() and not versions.is_symlink():
            for child in sorted(versions.iterdir()):
                if child.is_symlink() or not child.is_dir():
                    record = entry(child, stage=STAGE_FINISH)
                    if record is not None and child.name in (handoff.LOCK_NAME, handoff.LOCK_RECORD_NAME):
                        # The install lock's own files: every holder rewrites
                        # them, this uninstall's own rerun included.
                        record.update(inode=None, mtime=None)
                    paths.append(record)
                    continue
                generation = child / installs.DIST
                paths.append(with_witness(entry(child, stage=STAGE_FINISH), generation / "pyvenv.cfg"))
                if generation.is_dir():
                    envs.append(generation)
                    receipts.append(generation)
            paths.append(entry(versions, stage=STAGE_FINISH, empty_only=True))
        for env_dir in receipts:
            for shim in _receipt_shims(env_dir):
                if shim in shims or any(shim == e or e in shim.parents for e in roots):
                    continue  # one inside an env goes with the env
                if (shim.is_symlink() and _points_into(shim, roots)) or (os.name == "nt" and shim.is_file()):
                    shims.append(shim)
                    paths.append(entry(shim, stage=STAGE_FINISH))
    return {
        "paths": [p for p in paths if p is not None],
        "env_generations": [str(e) for e in dict.fromkeys(envs)],
        "shims": [str(s) for s in shims],
        "install_lock": str(handoff.lock_path(primary_versions_root())),
    }


# -- state --------------------------------------------------------------------------


def session_state_dirs() -> list[Path]:
    """The state folders live sessions named to this machine's service."""
    from probe.service import paths

    try:
        data = json.loads(paths.registry_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    out = []
    for session in (data.get("sessions") or []) if isinstance(data, dict) else []:
        named = session.get("state_dir") if isinstance(session, dict) else None
        if isinstance(named, str) and os.path.isabs(named) and Path(named).name == "probe":
            out.append(Path(named))
    return out


def state_roots() -> list[Path]:
    """Probe's state folders: the service's (`~/.local/state/probe`, fixed),
    this process's XDG one, and any a live session named."""
    from probe import version_policy
    from probe.service import paths

    roots: list[Path] = []
    for folder in (paths.state_dir(), *version_policy.known_state_dirs(session_state_dirs())):
        folder = Path(folder)
        if folder not in roots and folder.name == "probe" and folder.is_dir() and not folder.is_symlink():
            roots.append(folder)
    return roots


def other_machine_dirs() -> list[Path]:
    """Other machines' service folders in a shared home: never ours to remove."""
    from probe.service import paths

    mine = paths.machine_key()
    try:
        children = sorted(paths.root_dir().iterdir())
    except OSError:
        return []
    return [c for c in children if c.is_dir() and MACHINE_KEY.match(c.name) and c.name != mine]


def _telemetry_dirs() -> list[Path]:
    base = os.environ.get("XDG_STATE_HOME")
    out = [Path.home() / ".local" / "state" / "probe-telemetry"]
    if base:
        out.insert(0, Path(base) / "probe-telemetry")
    return list(dict.fromkeys(out))


def _keeper_units() -> list[Path]:
    from probe.service import keeper

    units = [keeper._systemd_dir() / f"{keeper.NAME}.{suffix}" for suffix in ("service", "timer")]  # noqa: SLF001
    units.append(keeper._plist_path())  # noqa: SLF001
    return units


def desktop_paths() -> list[Path]:
    """The desktop app's data, logs and (where this user may remove it) its
    bundle. macOS only: the app ships nowhere else."""
    if sys.platform != "darwin":
        return []
    home = Path.home()
    out = [
        home / "Library" / "Application Support" / DESKTOP_BUNDLE_ID,
        home / "Library" / "Logs" / "Probe",
        home / "Library" / "Caches" / DESKTOP_BUNDLE_ID,
        home / "Library" / "Preferences" / f"{DESKTOP_BUNDLE_ID}.plist",
        home / "Library" / "Saved Application State" / f"{DESKTOP_BUNDLE_ID}.savedState",
        home / "Library" / "WebKit" / DESKTOP_BUNDLE_ID,
    ]
    for folder in (home / "Applications", Path("/Applications")):
        bundle = folder / DESKTOP_APP
        if bundle.is_dir() and os.access(folder, os.W_OK):
            out.append(bundle)
    return out


def desktop_bundle_left() -> Path | None:
    """The app's bundle, when it is there and this user cannot remove it."""
    if sys.platform != "darwin":
        return None
    for folder in (Path.home() / "Applications", Path("/Applications")):
        bundle = folder / DESKTOP_APP
        if bundle.is_dir() and not os.access(folder, os.W_OK):
            return bundle
    return None


def state_layout() -> dict:
    """Probe's state on this computer (stage state), what is kept and why."""
    from probe.cli import uninstall_agents
    from probe.sdk import journal
    from probe.sdk.config import config_path
    from probe.service import paths

    out: list[dict] = []
    kept: list[str] = []
    others = set(other_machine_dirs())
    fixed = paths.state_dir()
    for root in state_roots():
        for child in sorted(root.iterdir()):
            if root == fixed and child.name == paths.UNINSTALL_DIRNAME:
                continue  # the finisher's, last of all
            if child.name == paths.SERVICE_DIRNAME and child.is_dir() and not child.is_symlink():
                for sub in sorted(child.iterdir()):
                    if sub in others:
                        continue
                    out.append(entry(sub, stage=STAGE_STATE))
                out.append(entry(child, stage=STAGE_STATE, empty_only=True))
                continue
            out.append(entry(child, stage=STAGE_STATE))
        if root != fixed:
            out.append(entry(root, stage=STAGE_STATE, empty_only=True))
    if others:
        kept.append(f"{len(others)} other machine(s)' Probe service folder(s) in this shared home "
                    f"({', '.join(str(o) for o in sorted(others))})")
    for folder in _telemetry_dirs():
        out.append(entry(folder, stage=STAGE_STATE))
    try:
        from probe import version_policy

        cache = version_policy.cache_path()
        if os.environ.get("PROBE_VERSION_CACHE"):
            out.append(entry(cache, stage=STAGE_STATE))
        else:
            out.append(entry(cache.parent, stage=STAGE_STATE))
    except Exception:  # noqa: BLE001
        pass
    try:
        from probe.tap_core import session_journal

        transcripts = session_journal.state_root()
        out.append(entry(transcripts, stage=STAGE_STATE))
        if transcripts.parent == Path.home() / ".probe":
            out.append(entry(transcripts.parent, stage=STAGE_STATE, empty_only=True))
    except Exception:  # noqa: BLE001
        pass
    roots = state_roots()
    try:
        outbox = journal.default_root()
        if not any(outbox == r or r in outbox.parents for r in roots) and outbox.exists():
            kept.append(f"the outbox PROBE_OUTBOX_DIR names ({outbox}): it may be a folder of yours, "
                        "so it is left; delete it yourself once it is empty")
    except Exception:  # noqa: BLE001
        pass
    for fallback in journal._fallback_roots():  # noqa: SLF001
        out.append(entry(fallback, stage=STAGE_STATE))
    for folder in uninstall_agents.tap_dirs():
        out.append(entry(folder, stage=STAGE_STATE))
    for unit in _keeper_units():
        out.append(entry(unit, stage=STAGE_STATE))
    for path in desktop_paths():
        out.append(entry(path, stage=STAGE_STATE))
    left = desktop_bundle_left()
    if left is not None:
        kept.append(f"{left}: macOS does not let this user remove it; drag Probe to the Trash")
    config = config_path()
    lock = config.with_suffix(".lock")
    out.append(entry(lock, stage=STAGE_STATE))
    if config.parent.name == "probe":
        out.append(entry(config.parent, stage=STAGE_STATE, empty_only=True))
    seen: set = set()
    unique = []
    for item in out:
        if item is not None and item["path"] not in seen:
            seen.add(item["path"])
            unique.append(item)
    return {"paths": unique, "kept": kept, "config": str(config)}


# -- server ids ------------------------------------------------------------------------


def device_instance_id() -> str | None:
    """This machine's device instance id, READ (never minted: an uninstall
    must not give the machine a new identity)."""
    from probe.sdk import device_identity

    try:
        data = json.loads(device_identity.device_file().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    value = data.get("device_instance_id") if isinstance(data, dict) else None
    return value if isinstance(value, str) and value else None


class Offline(Exception):
    """A context's server could not be reached: nothing may be destroyed yet."""


def contexts() -> dict[str, dict]:
    """Every saved context that holds a credential: {name: its dict}."""
    from probe.sdk.config import load_file

    try:
        data = load_file()
    except Exception:  # noqa: BLE001 - an unreadable config holds nothing we can use
        return {}
    table = data.get("contexts") if isinstance(data, dict) else None
    out = {}
    for name, ctx in (table or {}).items() if isinstance(table, dict) else []:
        if isinstance(ctx, dict) and any(ctx.get(k) for k in ("token", "mcp_token", "companion_token", "ingest_token")):
            out[str(name)] = ctx
    return out


def _base_url(ctx: dict) -> str:
    from probe.sdk.config import DEFAULT_BASE_URL

    return str(ctx.get("base_url") or DEFAULT_BASE_URL).rstrip("/")


def server_ids(*, device_id: str | None = None) -> dict:
    """This device's installation rows in every context's tenant: the rows
    whose `device_instance_id` is this machine's (a device row retires the
    legacy installation it adopted with it). Raises Offline when a server
    cannot be reached; a context whose credentials no longer authenticate
    has nothing left to retire."""
    from probe.sdk import errors
    from probe.sdk.client import Client
    from probe.sdk.config import Settings
    from probe.sdk.surface import Surface

    device_id = device_id if device_id is not None else device_instance_id()
    out: dict = {"device_ids": [device_id] if device_id else [], "installation_ids": [], "contexts": {}}
    for name, ctx in contexts().items():
        token = ctx.get("token") or ctx.get("companion_token")
        base_url = _base_url(ctx)
        entry_ = {"base_url": base_url, "installation_ids": []}
        out["contexts"][name] = entry_
        if not token or not device_id:
            continue
        try:
            with Client(settings=Settings(base_url=base_url, token=str(token)), async_writes=False,
                        surface=Surface.CLI.value) as client:
                listing = client.list_client_installations()
        except (errors.AuthError, errors.NotFoundError):
            entry_["dead"] = True
            continue
        except errors.RosError as exc:
            if _transient(exc):
                raise Offline(f"{base_url}: {exc}") from exc
            entry_["error"] = str(exc)
            continue
        except Exception as exc:  # noqa: BLE001 - a connection that failed in some other way
            raise Offline(f"{base_url}: {type(exc).__name__}: {exc}") from exc
        for row in (listing.get("installations") or []) if isinstance(listing, dict) else []:
            if isinstance(row, dict) and row.get("device_instance_id") == device_id and row.get("id"):
                entry_["installation_ids"].append(str(row["id"]))
                out["installation_ids"].append(str(row["id"]))
    return out


def transient(exc: BaseException) -> bool:
    """A failure that may go away: no connection, a timeout, a 5xx, a 429."""
    from probe.sdk import errors

    if isinstance(exc, (errors.TransportError, errors.ServerError)):
        return True
    status = getattr(exc, "status", None)
    if isinstance(status, int):
        return status >= 500 or status in (408, 425, 429)
    return not isinstance(exc, errors.RosError)


_transient = transient


# -- the plan -----------------------------------------------------------------------------


def compute(*, server: dict | None, machine_key: str | None = None) -> dict:
    """The whole plan (see the module docstring). `server`: `server_ids()`'s
    answer, or None (`--offline`)."""
    from probe.cli import uninstall_agents
    from probe.service import paths

    cli = cli_layout()
    state = state_layout()
    finish_paths = {p["path"] for p in cli["paths"]}
    merged = cli["paths"] + [p for p in state["paths"] if p["path"] not in finish_paths]
    agents = uninstall_agents.all_traces()
    return {
        "v": PLAN_VERSION,
        "created_at": time.time(),
        "machine_key": machine_key or paths.machine_key(),
        "paths": merged,
        "agent_edits": [{"agent": agent, "traces": found} for agent, found in agents.items()],
        "server": server or {"device_ids": [], "installation_ids": [], "contexts": {}, "offline": True},
        "env_generations": cli["env_generations"],
        "shims": cli["shims"],
        "install_lock": cli["install_lock"],
        "config": state["config"],
        "kept": state["kept"],
    }


def write(plan: dict) -> Path:
    """`S/uninstall/plan.json`, atomically, 0600 in a 0700 folder."""
    from probe.service import paths

    target = paths.uninstall_plan_path()
    paths.private_dir(target.parent)
    tmp = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    with open(os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w", encoding="utf-8") as handle:
        json.dump(plan, handle, indent=1)
    os.replace(tmp, target)
    return target


def read() -> dict | None:
    from probe.service import paths

    try:
        data = json.loads(paths.uninstall_plan_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) and data.get("v") == PLAN_VERSION else None
