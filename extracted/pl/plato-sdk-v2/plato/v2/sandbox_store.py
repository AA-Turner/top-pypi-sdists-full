"""Local sandbox slots and the cross-directory sandbox registry.

Historically a working directory held exactly one sandbox: ``plato sandbox
start`` wrote ``.plato/state.json`` and every other command read its arguments
back out of it. Starting a second sandbox in the same directory overwrote that
file, which orphaned the first one — its session id, job id and heartbeat pid
were gone, so the CLI could no longer stop it and the VM stayed alive on a
heartbeat nobody could find. The only workaround was one working directory per
sandbox.

This module replaces the single slot with named slots under
``.plato/sandboxes/<name>.json`` plus a ``.plato/current`` pointer, and keeps
``.plato/state.json`` as a symlink to the current slot so every existing
consumer (``plato pm``, the sim-* skills, ``SandboxClient.sync``) keeps working
untouched.

The slot files are the *single source of truth*. Everything else — the
``current`` pointer, the fixed-name links, per-slot SSH material, the
machine-wide directory index at ``~/.plato/sandboxes.json``, and the heartbeat
process — is derived from them and converged by :meth:`SandboxStore.reconcile`,
which every CLI command runs. A command that dies half-way leaves debris the
next command repairs, instead of debris that needs its own cleanup path.
"""

from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from pathlib import Path
from typing import Any

PLATO_DIR = ".plato"
SANDBOXES_SUBDIR = "sandboxes"
CURRENT_FILE = "current"
STATE_FILE = "state.json"
SSH_CONFIG_FILE = "ssh_config"

#: Pins a sandbox for a whole shell without touching any file, so two terminals
#: can drive two sandboxes from the same directory.
NAME_ENV_VAR = "PLATO_SANDBOX"

#: Slot used when a pre-existing single-slot ``.plato/state.json`` is migrated.
LEGACY_NAME = "default"

#: How long an empty reservation is presumed to be mid-write rather than
#: abandoned. Only reachable on filesystems without hard links.
_EMPTY_CLAIM_GRACE_SECONDS = 30.0

DEFAULT_REGISTRY_PATH = Path.home() / PLATO_DIR / "sandboxes.json"
#: Redirects the machine-wide directory index, so a test run (or a throwaway
#: experiment) does not append entries to the developer's real one.
REGISTRY_ENV_VAR = "PLATO_SANDBOX_REGISTRY"


def registry_path() -> Path:
    override = os.environ.get(REGISTRY_ENV_VAR)
    return Path(override) if override else DEFAULT_REGISTRY_PATH


_SLUG_STRIP = re.compile(r"[^a-z0-9._-]+")


def slugify(raw: str) -> str:
    """Reduce ``raw`` to a safe slot name (filename and SSH host alias)."""
    slug = _SLUG_STRIP.sub("-", raw.strip().lower()).strip("-._")
    return slug or "sandbox"


class SandboxStore:
    """The ``.plato/`` directory of one working directory, as named slots."""

    def __init__(self, working_dir: Path | str):
        self.working_dir = Path(working_dir)

    # -- paths ---------------------------------------------------------------

    @property
    def plato_dir(self) -> Path:
        return self.working_dir / PLATO_DIR

    @property
    def sandboxes_dir(self) -> Path:
        return self.plato_dir / SANDBOXES_SUBDIR

    @property
    def current_file(self) -> Path:
        return self.plato_dir / CURRENT_FILE

    @property
    def state_file(self) -> Path:
        """The back-compat ``.plato/state.json`` (a symlink to the current slot)."""
        return self.plato_dir / STATE_FILE

    @property
    def ssh_config_file(self) -> Path:
        """The fixed ``.plato/ssh_config`` (a symlink to the current slot's)."""
        return self.plato_dir / SSH_CONFIG_FILE

    def path(self, name: str) -> Path:
        return self.sandboxes_dir / f"{name}.json"

    def ssh_config_path(self, name: str) -> Path:
        return self.plato_dir / f"{SSH_CONFIG_FILE}_{name}"

    # -- legacy migration ----------------------------------------------------

    def migrate_legacy(self) -> str | None:
        """Fold a pre-slots ``.plato/state.json`` into a named slot.

        Idempotent and silent: once the file is a symlink into ``sandboxes/``
        there is nothing left to do. Returns the slot name if one was created.
        """
        state = self.state_file
        if not state.exists() or state.is_symlink():
            return None
        try:
            data = json.loads(state.read_text())
        except Exception:
            return None
        if not isinstance(data, dict) or not data.get("session_id"):
            return None
        if data.get("name") and self.path(str(data["name"])).exists():
            # Not a pre-slots file: a symlink-fallback *copy* of a slot we
            # already have. Migrating it would fork a new slot on every read
            # (alpha, alpha-2, alpha-2-2, …) wherever symlinks are unavailable.
            return None

        name = data.get("name") or slugify(str(data.get("simulator_name") or LEGACY_NAME))
        if self.path(name).exists():
            name = self.unique_name(name)
        data["name"] = name
        self.sandboxes_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        self._write_slot(self.path(name), data)
        state.unlink()
        self.set_current(name)
        register_dir(self.working_dir)
        return name

    # -- slots ---------------------------------------------------------------

    def names(self) -> list[str]:
        """Slots holding an actual sandbox.

        Reservations (see :meth:`claim`) are deliberately excluded: they are
        not sandboxes, so they must not show up in `list`, be picked as the
        current slot, or be counted as siblings.
        """
        self.migrate_legacy()
        if not self.sandboxes_dir.exists():
            return []
        return sorted(p.stem for p in self.sandboxes_dir.glob("*.json") if not self._is_reservation(p))

    def _is_reservation(self, path: Path) -> bool:
        """True if ``path`` is a claimed-but-unfilled slot rather than a sandbox."""
        try:
            text = path.read_text()
        except OSError:
            return False
        if not text.strip():
            return True
        try:
            data = json.loads(text)
        except ValueError:
            return False  # corrupt, but not ours to reclaim
        return isinstance(data, dict) and not data.get("session_id")

    def _is_stale_reservation(self, path: Path) -> bool:
        """True if ``path`` reserves a name for a process that is no longer running.

        Recorded by pid rather than by age: a start that takes 20 minutes to
        boot a large artifact must keep its name, while one that was SIGKILLed
        must not hold a name forever.
        """
        if not self._is_reservation(path):
            return False
        try:
            text = path.read_text()
        except OSError:
            return False
        if not text.strip():
            # Only reachable on the no-hard-link path, between the create and
            # the write. Give that a moment before declaring it abandoned, or
            # a concurrent claimer would steal a name mid-reservation.
            with suppress(OSError):
                if time.time() - path.stat().st_mtime < _EMPTY_CLAIM_GRACE_SECONDS:
                    return False
            return True
        try:
            data = json.loads(text)
        except ValueError:
            return True
        pid = data.get("claimed_by_pid") if isinstance(data, dict) else None
        if not pid:
            return True  # no owner recorded — nothing is coming back for it
        try:
            os.kill(int(pid), 0)
        except (ProcessLookupError, ValueError, TypeError):
            return True
        except PermissionError:
            return False
        return False

    def unique_name(self, base: str) -> str:
        """``base``, or ``base-2``/``base-3``/… if that slot is taken.

        Advisory only — it can go stale the moment it returns. Anything about
        to *write* a slot must use :meth:`claim`.
        """
        for candidate in self._candidates(base):
            if not self.path(candidate).exists():
                return candidate
        raise RuntimeError(f"could not find a free sandbox name for '{base}'")

    def claim(self, base: str) -> str:
        """Atomically reserve a free slot name, starting from ``base``.

        Two ``plato sandbox start`` runs in one working directory pick their
        slot names independently, and pick them *before* the sandbox is saved.
        A check-then-write would let both land on the same name and the second
        save would overwrite the first — losing a running sandbox exactly the
        way the single-state-file layout used to. ``O_CREAT | O_EXCL`` makes
        the reservation and the uniqueness check one step, so concurrent
        starts get ``sandbox`` and ``sandbox-2`` instead of one survivor.

        The reservation records the claiming pid; :meth:`save` fills it in,
        :meth:`release` drops it if the start never gets that far, and a
        reservation whose process died is taken over rather than blocking the
        name forever.
        """
        self.sandboxes_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        # Fill the reservation in *before* it is visible under its real name,
        # then link it into place. Creating an empty file and writing the pid
        # afterwards leaves a window where a concurrent claimer sees an
        # ownerless reservation, decides it is abandoned, and takes the same
        # name — the collision this whole mechanism exists to prevent.
        scratch = self.sandboxes_dir / f".claim-{os.getpid()}-{threading.get_ident()}.tmp"
        scratch.write_text(json.dumps({"claimed_by_pid": os.getpid()}))
        try:
            for candidate in self._candidates(base):
                path = self.path(candidate)
                if self._link_into_place(scratch, path):
                    return candidate
                if self._is_stale_reservation(path):
                    # Its owner is gone. Unlink and retry the link, so that if
                    # another process is doing the same only one of us wins.
                    with suppress(FileNotFoundError, OSError):
                        path.unlink()
                    if self._link_into_place(scratch, path):
                        return candidate
            raise RuntimeError(f"could not find a free sandbox name for '{base}'")
        finally:
            with suppress(FileNotFoundError, OSError):
                scratch.unlink()

    @staticmethod
    def _link_into_place(scratch: Path, path: Path) -> bool:
        """Put the reservation at ``path``; False if the name is taken.

        ``os.link`` is atomic and fails when the target exists, so the slot
        appears complete or not at all. Where hard links are unsupported, fall
        back to an exclusive create plus an immediate write — the *name* is
        still claimed atomically, only its contents lag by a syscall, which
        :meth:`_is_stale_reservation` allows for.
        """
        try:
            os.link(scratch, path)
            return True
        except FileExistsError:
            return False
        except OSError:
            try:
                fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            except FileExistsError:
                return False
            try:
                os.write(fd, scratch.read_bytes())
            finally:
                os.close(fd)
            return True

    def release(self, name: str) -> None:
        """Drop a :meth:`claim` that was never filled in (a failed start)."""
        path = self.path(name)
        if path.exists() and self._is_reservation(path):
            with suppress(FileNotFoundError, OSError):
                path.unlink()

    @staticmethod
    def _candidates(base: str) -> Iterator[str]:
        yield base
        for suffix in range(2, 1000):
            yield f"{base}-{suffix}"

    def current(self) -> str | None:
        self.migrate_legacy()
        if not self.current_file.exists():
            return None
        name = self.current_file.read_text().strip()
        return name if name and self.path(name).exists() else None

    def set_current(self, name: str) -> None:
        self.plato_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.current_file.write_text(name)
        self.refresh_links()

    def resolve(self, explicit: str | None = None) -> str | None:
        """Which slot a command should act on.

        Precedence: explicit ``--name`` > ``$PLATO_SANDBOX`` > ``.plato/current``.
        An explicit name is returned even when its slot does not exist, so the
        caller can report *that* name rather than a confusing fallback.
        """
        if explicit:
            return slugify(explicit)
        env_name = os.environ.get(NAME_ENV_VAR)
        if env_name:
            return slugify(env_name)
        return self.current()

    def load(self, name: str | None = None) -> dict[str, Any] | None:
        self.migrate_legacy()
        slot = name or self.current()
        if not slot:
            return None
        path = self.path(slot)
        if not path.exists():
            return None
        if self._is_reservation(path):
            # An unfilled :meth:`claim` — a start still provisioning, or one
            # that died before saving. Reserved is not the same as corrupt.
            return None
        try:
            return json.loads(path.read_text())
        except Exception as exc:
            raise RuntimeError(f"failed to read sandbox state {path}: {exc}") from exc

    def save(self, name: str, data: dict[str, Any], make_current: bool = True) -> Path:
        self.sandboxes_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        data = {**data, "name": name}
        path = self.path(name)
        self._write_slot(path, data)
        if make_current:
            self.set_current(name)
        elif self.current() == name:
            # A background update to the current slot (a lease renewal, an
            # artifact_id recorded by snapshot) must reach `.plato/state.json`
            # even where that is a copy rather than a symlink.
            self.refresh_links()
        register_dir(self.working_dir)
        return path

    def _write_slot(self, path: Path, data: dict[str, Any]) -> None:
        """Write a slot file atomically (write-then-rename).

        The heartbeat process reads its slot file on every beat and treats
        "definitively absent or stopped" as its exit signal — so a reader must
        never observe a half-written file where a truncate-then-write would
        expose one.
        """
        tmp = path.with_name(f".{path.name}.{os.getpid()}-{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps(data, indent=2))
        os.replace(tmp, path)

    def update(self, name: str, **fields: Any) -> dict[str, Any] | None:
        """Merge ``fields`` into an existing slot. No-op if it is gone."""
        data = self.load(name)
        if data is None:
            return None
        data.update(fields)
        self.save(name, data, make_current=False)
        return data

    def remove(self, name: str) -> None:
        """Delete a slot and repoint ``current``/``state.json`` off it."""
        was_current = self.current_file.exists() and self.current_file.read_text().strip() == name
        if was_current:
            # Clear the fixed-name pointers *before* the slot goes. Where
            # symlinks are unavailable they are copies, and once the slot they
            # copy is gone a copy is indistinguishable from a pre-slots state
            # file — the next read would migrate it back into a fresh slot.
            self._link(self.state_file, None)
            self._link(self.ssh_config_file, None)
        with suppress(FileNotFoundError):
            self.path(name).unlink()
        if was_current:
            remaining = self.names()
            if remaining:
                self.set_current(remaining[0])
            else:
                with suppress(FileNotFoundError):
                    self.current_file.unlink()
        self.refresh_links()

    def refresh_links(self) -> None:
        """Point the fixed-name files at the current slot.

        ``.plato/state.json`` and ``.plato/ssh_config`` are the paths every
        pre-slots consumer and every doc uses, so they must always mean "the
        selected sandbox" — including after a `use` switch or after the slot
        they pointed at was stopped. A link with no slot behind it is removed
        rather than left dangling.
        """
        name = self.current()
        self._link(self.state_file, self.path(name) if name else None)
        self._link(self.ssh_config_file, self.ssh_config_path(name) if name else None)

    def _link(self, link: Path, target: Path | None) -> None:
        """Point ``link`` at ``target``, or clear it when there is nothing to point at.

        A symlink rather than a copy so that consumers which *write* through it
        (``plato sandbox snapshot`` recording an artifact_id, ``plato pm``) land
        in the slot itself. Falls back to a copy where symlinks are unavailable.
        """
        if target is None or not target.exists():
            # Never leave a stale pointer behind: `ssh -F .plato/ssh_config`
            # failing outright beats it resolving to a sandbox that is gone.
            # Where symlinks are unavailable this is a copy we wrote, so clear
            # that too — but only if it is recognisably ours.
            if link.is_symlink() or self._is_our_copy(link):
                with suppress(FileNotFoundError, OSError):
                    link.unlink()
            return
        relative_target = target.relative_to(self.plato_dir) if target.is_relative_to(self.plato_dir) else target
        if link.is_symlink():
            # Already pointing at the right slot: recreating it would open a
            # brief no-file window for concurrent readers, for nothing — and
            # this runs on every lease renewal.
            with suppress(OSError):
                if link.readlink() == relative_target:
                    return
        with suppress(FileNotFoundError):
            link.unlink()
        try:
            link.symlink_to(relative_target)
        except (OSError, ValueError):
            link.write_text(target.read_text())

    def _is_our_copy(self, link: Path) -> bool:
        """True if ``link`` is a symlink-fallback copy this store wrote.

        Deliberately narrow: a file we do not recognise is left alone rather
        than deleted, since ``.plato/`` is the user's directory too.
        """
        if link.is_symlink() or not link.is_file():
            return False
        try:
            text = link.read_text()
        except OSError:
            return False
        if link.name == SSH_CONFIG_FILE:
            return text.startswith("# Plato Sandbox SSH Config")
        if link.name == STATE_FILE:
            try:
                data = json.loads(text)
            except ValueError:
                return False
            return isinstance(data, dict) and bool(data.get("session_id")) and bool(data.get("name"))
        return False

    # -- reconciliation ------------------------------------------------------

    def reconcile(self) -> None:
        """Converge everything derived in ``.plato/`` onto the slot files.

        The slot files are the single source of truth; the ``current`` pointer,
        the fixed-name links, per-slot SSH material, recorded heartbeat pids and
        the machine-wide directory index are all derived. Instead of every
        command maintaining each of those on every code path — and leaving them
        inconsistent whenever it dies half-way — this runs at the start of every
        CLI command, is idempotent, and repairs whatever the last crash left:

        - reservations and scratch files whose owning process is gone
        - a ``current`` pointer at a slot that no longer exists
        - ``state.json``/``ssh_config`` links pointing at the wrong slot
        - SSH keys/configs positively attributable to a deleted slot
        - heartbeat pids recorded on slots that are already stopped
        - this directory's entry in the machine-wide index
        """
        self.migrate_legacy()
        if self.sandboxes_dir.exists():
            for path in self.sandboxes_dir.glob("*.json"):
                if self._is_stale_reservation(path):
                    with suppress(FileNotFoundError, OSError):
                        path.unlink()
            # Scratch files from claims and slot writes killed mid-flight.
            for scratch in self.sandboxes_dir.glob(".*.tmp"):
                with suppress(FileNotFoundError, OSError):
                    if time.time() - scratch.stat().st_mtime > _EMPTY_CLAIM_GRACE_SECONDS:
                        scratch.unlink()

        # `current` must name a slot that exists; with none left it goes away
        # entirely, and with slots but no pointer the first one is as good a
        # default as `remove` would have picked.
        names = self.names()
        if self.current() is None:
            if names:
                self.set_current(names[0])
            else:
                with suppress(FileNotFoundError):
                    self.current_file.unlink()
        self.refresh_links()
        self._sweep_ssh_material()

        for name in names:
            data = self.load(name) or {}
            if data.get("stopped_at") and data.get("heartbeat_pid"):
                # Stopped is stopped: no process should still be renewing the
                # lease. Normally `stop` already killed it; this catches slots
                # stopped by a crash or from another machine-wide sweep.
                stop_heartbeat(data["heartbeat_pid"])
                self.update(name, heartbeat_pid=None)

        if self.sandboxes_dir.exists() and any(self.sandboxes_dir.glob("*.json")):
            register_dir(self.working_dir)
        else:
            forget_dir(self.working_dir)

    def _sweep_ssh_material(self) -> None:
        """Delete SSH keys/configs whose slot no longer exists.

        Attribution is deliberately conservative — ``.plato/`` is the user's
        directory too. A config must carry our header; a key must follow the
        ``ssh_key_<slot>_<job>`` naming *and* match no existing slot (including
        reservations, so a start that is mid-provision keeps its key). Pre-slots
        keys (``ssh_key_<job8>``, no second underscore) are left alone.
        """
        if not self.plato_dir.exists():
            return
        slot_names = {p.stem for p in self.sandboxes_dir.glob("*.json")} if self.sandboxes_dir.exists() else set()

        for config in self.plato_dir.glob(f"{SSH_CONFIG_FILE}_*"):
            name = config.name[len(SSH_CONFIG_FILE) + 1 :]
            if name in slot_names:
                continue
            try:
                ours = config.read_text().startswith("# Plato Sandbox SSH Config")
            except OSError:
                continue
            if ours:
                with suppress(FileNotFoundError, OSError):
                    config.unlink()

        for key in self.plato_dir.glob("ssh_key_*"):
            if key.name.endswith(".pub"):
                continue  # removed together with its private half
            rest = key.name[len("ssh_key_") :]
            if "_" not in rest:
                continue
            if any(rest == n or rest.startswith(f"{n}_") for n in slot_names):
                continue
            for candidate in (key, key.with_name(f"{key.name}.pub")):
                with suppress(FileNotFoundError, OSError):
                    candidate.unlink()

    def stop_local(self, name: str, remove: bool = False) -> dict[str, bool]:
        """The local half of every teardown, whatever triggered it.

        Used by ``stop``, ``start --force``, reuse of a finished slot, a start
        that failed after its VM came up, and ``gc`` — one path instead of five
        approximations of it. Kills the slot's heartbeat (best-effort courtesy;
        marking the slot stopped makes it exit on its own within a beat
        anyway), removes the SSH material the slot points at, marks the slot
        stopped (or deletes it), then reconciles so links, leftover files and
        the index all follow.
        """
        result = {"heartbeat_stopped": False, "ssh_removed": False}
        state = self.load(name)
        if state is None:
            # A reservation, or nothing at all: a start that never got to save.
            self.release(name)
            self.reconcile()
            return result

        if state.get("heartbeat_pid"):
            result["heartbeat_stopped"] = stop_heartbeat(state["heartbeat_pid"])
        for rel in (state.get("ssh_key_path"), state.get("ssh_config_path")):
            if not rel:
                continue
            path = Path(rel) if Path(rel).is_absolute() else self.working_dir / rel
            for candidate in (path, Path(f"{path}.pub")):
                with suppress(FileNotFoundError, OSError):
                    candidate.unlink()
                    result["ssh_removed"] = True
        if remove:
            self.remove(name)
        else:
            self.update(name, stopped_at=time.time(), heartbeat_pid=None)
        self.reconcile()
        return result


# =============================================================================
# MACHINE-WIDE DIRECTORY INDEX
# =============================================================================
# ``~/.plato/sandboxes.json`` deliberately stores *nothing about sandboxes
# themselves* — only which working directories have slots. It used to hold a
# copy of every slot's fields, which meant every start/stop/gc had to update
# both places on every path, and any missed path left them disagreeing (a
# stopped sandbox listed as live, a live sibling marked stopped). An index of
# directories cannot go stale in a way that matters: a listed directory with no
# slots is skipped and pruned, and `list --all`/`gc` read the slot files —
# the single source of truth — for everything else.


@contextmanager
def _locked_index() -> Iterator[Path]:
    """Serialize index read-modify-write across concurrent CLI invocations."""
    path = registry_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock_path = path.with_suffix(".lock")
    try:
        import fcntl

        with open(lock_path, "w") as lock:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
            try:
                yield path
            finally:
                fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    except ImportError:  # pragma: no cover - non-POSIX
        yield path


def _read_index() -> list[str]:
    path = registry_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
    except Exception:
        return []
    if isinstance(data, dict) and isinstance(data.get("dirs"), list):
        return [d for d in data["dirs"] if isinstance(d, str)]
    # Pre-index format: a list of per-sandbox entries. Only their working
    # directories carry information the slot files don't already hold.
    entries = data.get("sandboxes") if isinstance(data, dict) else data
    dirs: list[str] = []
    for entry in entries or []:
        if isinstance(entry, dict) and entry.get("working_dir"):
            d = str(entry["working_dir"])
            if d not in dirs:
                dirs.append(d)
    return dirs


def _write_index(dirs: list[str]) -> None:
    path = registry_path()
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"dirs": dirs}, indent=2))
    os.replace(tmp, path)


def registered_dirs() -> list[str]:
    """Every working directory that has (or recently had) sandbox slots."""
    return _read_index()


def register_dir(working_dir: Path | str) -> None:
    resolved = str(Path(working_dir).resolve())
    with _locked_index():
        dirs = _read_index()
        if resolved not in dirs:
            dirs.append(resolved)
            _write_index(dirs)


def forget_dir(working_dir: Path | str) -> None:
    resolved = str(Path(working_dir).resolve())
    with _locked_index():
        dirs = _read_index()
        if resolved in dirs:
            _write_index([d for d in dirs if d != resolved])


# =============================================================================
# HEARTBEAT PROCESSES
# =============================================================================


def heartbeat_alive(pid: int | None) -> bool:
    """True if ``pid`` is a live process we are allowed to signal."""
    if not pid:
        return False
    try:
        os.kill(int(pid), 0)
        return True
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True


def stop_heartbeat(pid: int | None) -> bool:
    """SIGTERM ``pid`` if it is verifiably a heartbeat process.

    Recorded pids go stale — a reboot or a long-stopped slot can leave one
    pointing at a recycled pid — so the process's argv must identify it as a
    heartbeat before it is signalled. Killing nothing is always safe now that
    the heartbeat also exits on its own (its slot file is gone or stopped);
    killing the wrong process never is.

    Returns True when the process is gone or was signalled.
    """
    if pid is None or not heartbeat_alive(pid):
        return True
    if not _argv_is_heartbeat(_process_argv(int(pid))):
        return False
    try:
        os.kill(int(pid), signal.SIGTERM)
        return True
    except ProcessLookupError:
        return True
    except Exception:
        return False


HEARTBEAT_LOG_DIR = Path("/tmp")
#: Embedded in the heartbeat script so its processes can be told apart from
#: anything else whose argv happens to mention a heartbeat log path — these
#: pids get SIGTERMed, and the docs tell people to `tail` those logs.
HEARTBEAT_PROC_MARKER = "plato-sandbox-heartbeat-v1"
_HEARTBEAT_LOG_GLOB = "plato_heartbeat_*.log"
_HEARTBEAT_LOG_RE = re.compile(r"plato_heartbeat_(.+)\.log$")


def _argv_is_heartbeat(argv: str) -> bool:
    """True if ``argv`` is recognizably a sandbox heartbeat process.

    Current scripts embed :data:`HEARTBEAT_PROC_MARKER`. Scripts spawned by
    pre-marker versions of the SDK are still running on people's machines —
    and are exactly the immortal orphans this module exists to end — so they
    must stay killable after an upgrade: they are identified by carrying both
    a heartbeat log path and the stdlib module the script POSTs with. A
    ``tail``/``less``/editor on the log matches the path but never
    ``urllib.request``.
    """
    if HEARTBEAT_PROC_MARKER in argv:
        return True
    return "plato_heartbeat_" in argv and "urllib.request" in argv


def heartbeat_log_path(session_id: str) -> Path:
    """Where a session's heartbeat process writes its log."""
    return HEARTBEAT_LOG_DIR / f"plato_heartbeat_{session_id}.log"


def known_heartbeat_sessions() -> list[str]:
    """Every session that has ever had a heartbeat on this machine.

    Read off the log files rather than any state we keep, so it still finds
    sandboxes whose state file was clobbered before slots existed.
    """
    sessions = []
    for log in sorted(HEARTBEAT_LOG_DIR.glob(_HEARTBEAT_LOG_GLOB)):
        match = _HEARTBEAT_LOG_RE.search(log.name)
        if match:
            sessions.append(match.group(1))
    return sessions


def heartbeats_for_session(session_id: str) -> list[int]:
    """Pids of heartbeat processes for ``session_id``.

    Matched against argv, not against the log file: a heartbeat spawned
    moments ago has not written its log yet, and a teardown racing its own
    start has to find it anyway.

    Matching on the log path alone would also match anything that merely
    *mentions* it — and the docs tell people to ``tail`` that very file when a
    VM dies early. Since these pids get SIGTERMed, a candidate must carry the
    session's log path **and** pass :func:`_argv_is_heartbeat` (the embedded
    marker, or the legacy fingerprint for scripts spawned before the marker
    existed).
    """
    try:
        proc = subprocess.run(
            ["pgrep", "-f", "plato_heartbeat_"],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return []
    log_path = str(heartbeat_log_path(session_id))
    pids = []
    for line in proc.stdout.split():
        try:
            pid = int(line)
        except ValueError:
            continue
        if pid == os.getpid():
            continue
        argv = _process_argv(pid)
        if log_path in argv and _argv_is_heartbeat(argv):
            pids.append(pid)
    return pids


def _process_argv(pid: int) -> str:
    try:
        proc = subprocess.run(["ps", "-p", str(pid), "-o", "args="], capture_output=True, text=True, timeout=15)
    except Exception:
        return ""
    return proc.stdout


def running_heartbeats() -> dict[int, str]:
    """Map pid -> session_id for every heartbeat process on this machine.

    The heartbeat runs as ``python3 -c <script>`` — its session id lives only
    inside the argv text, and that text spans many lines, so this matches each
    known session's log path against the process table with ``pgrep -f`` rather
    than trying to parse multi-line ``ps`` output. This is what finds heartbeats
    orphaned by a clobbered state file, whose pid is in no state or registry.
    """
    found: dict[int, str] = {}
    for session_id in known_heartbeat_sessions():
        for pid in heartbeats_for_session(session_id):
            found[pid] = session_id
    return found
