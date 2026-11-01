"""This machine's stable identity, independent of every credential it holds.

A 128-bit random device instance id, minted once and kept across setup, reauth,
credential rotation, logout and upgrade (setting up twice used to create two
"devices" because the server keyed on the authorization UUID).

    ~/.local/state/probe/device.json   (not config.json: dotfiles symlink that and
    would SHARE one id across machines)
    { "device_instance_id": "...", "created_at": ..., "home": "...", "machine": "m1:<hash>" }

Not a credential: no authority, useless without a bearer token. Rule of thumb: a split
(one machine, two rows) costs a retirable row; a merge (two machines, one row) destroys
the evidence, so every choice here prefers splitting. Honours `PROBE_DEVICE_ID_PATH`
(and an isolated `PROBE_CONFIG_PATH`), serializes the first mint with a lock, and
guards a shared `$HOME` with a witness. The witness must not move: it is
`_machine_witness()` (`/etc/machine-id` or macOS hardware UUID), never the hostname,
which a captive WiFi renamed and so forked a laptop's identity.

Full rationale: DESIGN.md in this folder.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import socket
import stat
import sys
import tempfile
import time
from pathlib import Path

from ...foundation.durable import homedir

#: 128 bits: collision-proof, log-readable. Must satisfy the server's
#: `^[A-Za-z0-9_-]{16,128}$` and the same CHECK in both databases.
_ID_BYTES = 16

FILENAME = "device.json"

#: macOS hardware UUID size; a finite lookup bound (`gethostuuid(2)` reads `{0, 0}` as "wait forever").
_UUID_BYTES = 16
_UUID_WAIT_SECONDS = 2

#: Half a sha256 (128 bits): it only answers "same machine?".
_WITNESS_HEX_LEN = 32

#: Read bound for a device file: a shared `$HOME` is writable by others, and the id is
#: 32 chars in tiny JSON, so a huge file is an attack or corruption.
_MAX_DEVICE_FILE_BYTES = 64 * 1024

#: A machine id must look like one: systemd writes `uninitialized` on first boot and
#: `gethostuuid` can return all zeros on some VMs; both are STABLE and SHARED across
#: hosts in that state, a fleet-wide merge disguised as a valid witness.
_MACHINE_ID_RE = re.compile(r"^[0-9a-f]{32}$")
_DEGENERATE_MACHINE_IDS = frozenset({"0" * 32})

#: Cached only when non-empty; see `_machine_id`.
_MACHINE_ID_CACHE = ""


def _valid_id(value: object) -> str | None:
    """`value` if it is an id every layer will accept, else None.

    `device_headers` silently drops a malformed id, but `device_authorize` sends it in a
    request BODY with no such filter, so a bad file would 4xx on LOGIN. Validate once
    here, at adoption, so all four layers agree.
    """
    from probe.foundation.request_identity.request_identity import _DEVICE_INSTANCE_RE

    if not isinstance(value, str) or not _DEVICE_INSTANCE_RE.fullmatch(value):
        return None
    return value


def device_file() -> Path:
    """Where this machine's identity lives.

    `PROBE_DEVICE_ID_PATH` wins outright; else an overridden `PROBE_CONFIG_PATH` pulls
    the device file alongside it, so an isolated test/dev config does not share the real
    machine's identity (the divergence `config_path()` documents).
    """
    override = os.environ.get("PROBE_DEVICE_ID_PATH")
    if override:
        return Path(override)
    config_override = os.environ.get("PROBE_CONFIG_PATH")
    if config_override:
        return Path(config_override).parent / FILENAME
    xdg = os.environ.get("XDG_STATE_HOME")
    base = Path(xdg) if xdg else homedir.home() / ".local" / "state"
    return base / "probe" / FILENAME


def _home_fingerprint() -> str:
    """The LEGACY witness: `<hostname>:<$HOME>`.

    Still the ONLY witness where no stable machine id exists (`_machine_witness`);
    elsewhere kept beside `machine` as a human-readable trace and not compared once
    `machine` exists. The hostname follows the network (a captive WiFi made a Mac
    `visitor-10-59-125-182`), which read as "a different machine" and forked a second
    identity. See `_ours` for adopting files written before the stable witness.
    """
    try:
        host = socket.gethostname().split(".")[0].strip()
    except OSError:
        host = ""
    return f"{host or 'unknown-host'}:{homedir.home()}"


def _darwin_host_uuid() -> str:
    """macOS's hardware UUID via `gethostuuid(2)`, or "" if it cannot be read.

    ctypes, not `ioreg`/`scutil`: this is on every CLI startup and a subprocess costs more.

    THE TIMEOUT IS NOT OPTIONAL: `gethostuuid(2)` treats a `wait` of `{0, 0}` as "wait
    INDEFINITELY", which would hang every CLI invocation; pass a finite bound and take
    the hostname fallback on EWOULDBLOCK.

    `argtypes`/`restype` are declared because ctypes otherwise guesses (a struct-pointer
    call becomes undefined behaviour on a future ABI).
    """
    try:
        import ctypes

        libc = ctypes.CDLL("libc.dylib")

        class _Timespec(ctypes.Structure):
            _fields_ = (("tv_sec", ctypes.c_int64), ("tv_nsec", ctypes.c_long))

        buf_type = ctypes.c_ubyte * _UUID_BYTES
        libc.gethostuuid.argtypes = (buf_type, ctypes.POINTER(_Timespec))
        libc.gethostuuid.restype = ctypes.c_int
        buf = buf_type()
        if libc.gethostuuid(buf, ctypes.byref(_Timespec(_UUID_WAIT_SECONDS, 0))) != 0:
            return ""
        return bytes(buf).hex()
    except (OSError, AttributeError, ValueError, ImportError):
        return ""


def _machine_id() -> str:
    """A per-machine fact that does NOT move when the network renames the host.

    `/etc/machine-id` on Linux, the hardware UUID on macOS: both survive DHCP, WiFi and
    rename changes yet differ between nodes sharing one `$HOME`.

    "" when the platform offers neither (the hostname witness stays in charge, also
    inside a container: see `_in_container`).

    RESIDUAL LIMIT: a golden VM/bare-metal image baking `/etc/machine-id` (a systemd
    footgun; images should ship it empty) hands every clone one value, so clones sharing
    one `$HOME` would merge.
    """
    global _MACHINE_ID_CACHE
    # Cache SUCCESSES ONLY: a cached failure would pin a long-lived process to the hostname fallback.
    if _MACHINE_ID_CACHE:
        return _MACHINE_ID_CACHE
    if not _in_container():
        for candidate in ("/etc/machine-id", "/var/lib/dbus/machine-id"):
            try:
                value = Path(candidate).read_text(encoding="utf-8").strip()
            except (OSError, ValueError):
                continue
            if _usable_machine_id(value):
                _MACHINE_ID_CACHE = value
                return value
    if sys.platform == "darwin":
        found = _darwin_host_uuid()
        _MACHINE_ID_CACHE = found if _usable_machine_id(found) else ""
        return _MACHINE_ID_CACHE
    return ""


def _usable_machine_id(value: str) -> bool:
    """Whether `value` identifies ONE machine, rather than a class of them."""
    return bool(_MACHINE_ID_RE.fullmatch(value)) and value not in _DEGENERATE_MACHINE_IDS


def _in_container() -> bool:
    """Whether this process is running inside a container image.

    `/etc/machine-id` is a FILE IN THE IMAGE: replicas of one image share it, so it names
    an image and replicas sharing a persistent `$HOME` (k8s PVC) would claim one
    identity. Measured on 3 replicas with one home: machine-id yields ONE id, hostname
    correctly three. So in a container the witness is withheld and the hostname governs
    (unique and stable per container). Laptops are untouched.

    Conservative: only real container-runtime signals. A false positive costs a host the
    fix; a false negative changes nothing from before.
    """
    if Path("/.dockerenv").exists():
        return True
    try:
        cgroup = Path("/proc/self/cgroup").read_text(encoding="utf-8")
    except (OSError, ValueError):
        return False
    return any(marker in cgroup for marker in ("docker", "kubepods", "containerd", "lxc"))


def _machine_witness() -> str | None:
    """The stable witness written into `machine`, or None when unavailable.

    Hashed, not raw: a hardware UUID is a durable cross-application fingerprint and this
    file is readable by anything that reads `$HOME`. `$HOME` stays in the hash: the
    guard defends a shared home, so (machine, home) identifies "this machine's state".
    """
    machine = _machine_id()
    if not machine:
        return None
    digest = hashlib.sha256(f"{machine}:{homedir.home()}".encode()).hexdigest()
    return f"m1:{digest[:_WITNESS_HEX_LEN]}"


def _read(path: Path) -> dict:
    """This file as a dict, or `{}` for anything that is not one.

    A shared `$HOME` is untrusted input: a FIFO blocks the open forever and a symlink to
    `/dev/zero` reads until the process dies. So: no symlink following, regular files
    only, bounded read.
    """
    if not hasattr(os, "O_NOFOLLOW") and os.path.islink(path):
        return {}  # Windows: no O_NOFOLLOW, so refuse a link before the open
    try:
        fd = os.open(
            path,
            os.O_RDONLY
            | getattr(os, "O_NONBLOCK", 0)
            | getattr(os, "O_NOFOLLOW", 0)
            | getattr(os, "O_BINARY", 0),
        )
    except OSError:
        return {}
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return {}
        raw = os.read(fd, _MAX_DEVICE_FILE_BYTES)
    except OSError:
        return {}
    finally:
        os.close(fd)
    try:
        data = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError, RecursionError):
        # RecursionError is not a ValueError: deep nesting would silently lose the identity, unlogged.
        return {}
    return data if isinstance(data, dict) else {}


def _write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".device-", suffix=".json")
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    try:
        path.chmod(0o600)
    except OSError:
        pass


def _mint() -> str:
    return secrets.token_hex(_ID_BYTES)


def _namespaced(path: Path, witness: str) -> Path:
    """The per-machine sibling of `path` for a machine that cannot use it."""
    digest = hashlib.sha256(witness.encode()).hexdigest()[:12]
    return path.with_name(f"{path.stem}-{digest}{path.suffix}")


def _stamp(path: Path, witness: str | None) -> None:
    """Record the stable witness on a file adopted through the legacy one.

    Best effort: a read-only `$HOME` keeps resolving by hostname (degraded, not broken).
    The id is never touched; this only adds the fact that makes the NEXT rename a non-event.
    """
    if witness is None:
        return
    payload = _read(path)
    if _valid_id(payload.get("device_instance_id")) is None or payload.get("machine") == witness:
        return
    payload["machine"] = witness
    try:
        _write(path, payload)
    except OSError:
        pass


def device_instance_id() -> str | None:
    """This machine's id, minting one on first use.

    None only when the id cannot be persisted (read-only home, full disk): an unsaved id
    would differ per invocation and mint a device row per command, so callers send
    nothing and the server behaves as for a client without device identity.
    """
    path = device_file()
    fingerprint = _home_fingerprint()
    witness = _machine_witness()

    def _claimed(payload: dict) -> str | None:
        """The id in `payload` when it records OUR stable machine witness: the strongest
        evidence, and the only kind that survives a rename."""
        value = _valid_id(payload.get("device_instance_id"))
        recorded = payload.get("machine")
        if value is None:
            return None
        if witness is None or not isinstance(recorded, str) or not recorded:
            return None
        return value if recorded == witness else None

    def _ours(payload: dict) -> str | None:
        """The id in `payload`, but only if this machine may claim it.

        No `home` means the file predates the witness and IS ours (rejecting it would
        re-mint on upgrade and split every machine). Someone else's home means a
        shared/NFS `$HOME` or baked image: adopting it would merge two machines.

        A file with `machine` is judged on THAT alone (the hostname moves). The legacy
        `home` path stays strict: a hostname-only difference is NOT accepted as a rename,
        since on disk it looks like a second node on a shared `$HOME` and a merge is
        worse than a split.
        """
        value = _valid_id(payload.get("device_instance_id"))
        if value is None:
            return None
        if witness is not None and payload.get("machine"):
            return _claimed(payload)
        if payload.get("home") not in (None, fingerprint):
            return None
        return value

    canonical_path = path
    canonical = _read(path)

    # Strongest evidence first: the stable witness on the canonical file (steady state, one read).
    claimed = _claimed(canonical)
    if claimed is not None:
        return claimed

    # Then this machine's own NAMESPACED file, addressed directly: its name is a pure
    # function of the witness, so a machine on a shared `$HOME` finds its identity in one
    # more read (no directory scan: costly on NFS at every startup, and peers can add names).
    namespaced_path = _namespaced(canonical_path, witness) if witness is not None else None
    if namespaced_path is not None:
        claimed = _claimed(_read(namespaced_path))
        if claimed is not None:
            return claimed

    current = _ours(canonical)
    if current is not None:
        # Proven ours; recording the stable witness stops the next rename forking it.
        _stamp(canonical_path, witness)
        return current

    # SHARED $HOME: give this machine its own file instead of overwriting the other's.
    # Overwriting is a trap: on NFS/container-shared homes each node would rewrite the
    # other's file, minting a fresh id per invocation and hitting the server's per-member
    # device cap. Namespacing keeps the anti-merge guarantee.
    #
    # The WITNESS check (not mere file existence) makes this safe: the read above is a
    # snapshot, so in a race a second process could find the FIRST process's file on this
    # very machine and fork onto a namespaced path. Only a file this machine may not
    # claim is another machine's.
    #
    # A HOSTNAME-KEYED SIBLING IS NEVER ADOPTED: pre-witness forks sit in
    # `_namespaced(path, fingerprint)`, but captive-network names derive from an IP, so two
    # machines on one network share them, and adopting (then stamping) would make the theft
    # permanent. A split costs a retirable row; a merge destroys the evidence.
    if _valid_id(canonical.get("device_instance_id")) and current is None:
        path = namespaced_path or _namespaced(canonical_path, fingerprint)
        current = _ours(_read(path))
        if current is not None:
            _stamp(path, witness)
            return current

    # Serialize the first mint: two concurrent `probe` processes would both mint, leaving two permanent device rows.
    lock = path.with_suffix(".lock")
    holder = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        holder = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        # Someone else is minting: re-read rather than race; a stale lock is broken on the next invocation.
        for _ in range(40):
            time.sleep(0.05)
            again = _ours(_read(path))
            if again is not None:
                return again
        try:
            if time.time() - lock.stat().st_mtime > 30:
                lock.unlink(missing_ok=True)
        except OSError:
            pass
        return None
    except OSError:
        return None

    try:
        # Re-read under the lock (the winner may have finished), through `_ours` NOT raw:
        # a raw read would re-adopt the file the home check just rejected.
        current = _ours(_read(path))
        if current is not None:
            return current
        minted = _mint()
        payload = {
            "device_instance_id": minted,
            "created_at": int(time.time()),
            "home": fingerprint,
        }
        # `home` stays for humans and for a rolled-back client; `machine` is what a rename is judged against.
        if witness is not None:
            payload["machine"] = witness
        _write(path, payload)
        return minted
    except OSError:
        return None
    finally:
        os.close(holder)
        lock.unlink(missing_ok=True)
