"""This machine's stable identity, independent of every credential it holds.

WHAT THIS FIXES. Setting up used to give the server a fresh authorization, and
the server used that authorization's UUID as the machine's identity. So setting
up twice on one laptop produced two "devices", and Settings filled with rows that
were all the same computer. The device instance id is the missing fact: 128
random bits, generated once, kept across setup, reauthorization, credential
rotation, logout and upgrade.

    ~/.local/state/probe/device.json        <- here, not config.json
    { "device_instance_id": "...", "created_at": ..., "home": "...",
      "machine": "m1:<hash>" }

WHY NOT config.json. That file is routinely symlinked into a dotfiles repo --
`config.save_file` resolves symlinks precisely because people do this -- and a
device id living inside it would be SHARED between every machine that checks the
dotfiles out. Two real laptops reporting as one row is strictly worse than one
laptop reporting as two: a lost identity costs a duplicate row someone can
retire, while a shared identity silently merges two people's machines and there
is no evidence left to separate them.

THE ID IS NOT A CREDENTIAL. It carries no authority, authorizes nothing, and is
useless without a bearer token. The server only ever matches it inside the
already-authenticated user and team.

THREE FAILURE MODES THIS FILE HANDLES, each because the repo already learned it:

  no override   `sdk/config.py::config_path` documents `PROBE_CONFIG_PATH` having
                been honoured by four readers and not the writer, so the setting
                "worked in the field and silently vanished under any test or dev
                environment". `PROBE_DEVICE_ID_PATH` is honoured here, and an
                isolated `PROBE_CONFIG_PATH` implies an isolated device file.
  no lock       `sdk/config.py::_config_lock` exists because two processes can
                read, both decide, and the second write wins -- reachable from a
                CI matrix or two worktree sessions. Two processes both minting a
                first id is the same race, and it produces two permanent device
                rows for one machine.
  shared $HOME  an NFS or container-shared home shares `~/.local/state` exactly
                as thoroughly as dotfiles share `config.json`. The file records
                the machine it was minted on; a mismatch mints a new id rather
                than adopting another machine's. The witness is a tripwire
                against merging -- never identity, which is the one direction it
                is safe in.

THE WITNESS MUST NOT MOVE, which is a fourth thing this file learned the hard
way. It used to be `<hostname>:<$HOME>`, and a hostname is not a property of the
machine -- it is a property of the network the machine is currently on. Joining
a captive WiFi renamed a MacBook to `visitor-10-59-125-182`, its own file
stopped matching, and it forked a second identity and a second Settings row: the
duplicate-rows bug, produced by the guard against it. The witness is now
`_machine_witness()` -- `/etc/machine-id` on Linux, the hardware UUID on macOS --
and `home` is kept alongside it as the human-readable trace only. A file written
before the witness existed is still adopted on the old comparison and stamped
with the new one as it goes, so no machine splits on upgrade.
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

from . import homedir

#: 128 bits. Long enough that collision is not a thing anyone needs to reason
#: about, short enough to read in a log line. Must satisfy the server's
#: `^[A-Za-z0-9_-]{16,128}$` and the same CHECK in both databases.
_ID_BYTES = 16

FILENAME = "device.json"

#: 16 bytes of macOS hardware UUID, and a finite bound on the kernel lookup --
#: `gethostuuid(2)` reads `{0, 0}` as "wait forever".
_UUID_BYTES = 16
_UUID_WAIT_SECONDS = 2

#: Half a sha256, 128 bits: this only ever answers "same machine?", so it needs
#: collision resistance and nothing else. Named for the same reason `_ID_BYTES`
#: is -- a bare `[:32]` in the middle of a digest reads as arbitrary.
_WITNESS_HEX_LEN = 32

#: How much of a device file a resolution will read. A shared `$HOME` is a
#: directory OTHER people can write to, so the read is bounded: the id is 32
#: characters inside a tiny JSON object, and a multi-gigabyte file named like
#: one is an attack or a corruption, never a device.
_MAX_DEVICE_FILE_BYTES = 64 * 1024

#: A machine id must look like one before it is trusted to identify a machine.
#: systemd writes the literal `uninitialized` during first-boot and factory-reset
#: states, and `gethostuuid` can succeed with an all-zero buffer on some VMs --
#: both are STABLE and SHARED across every host in that state, which is a
#: fleet-wide merge wearing the costume of a valid witness.
_MACHINE_ID_RE = re.compile(r"^[0-9a-f]{32}$")
_DEGENERATE_MACHINE_IDS = frozenset({"0" * 32})

#: Cached only when non-empty; see `_machine_id`.
_MACHINE_ID_CACHE = ""


def _valid_id(value: object) -> str | None:
    """`value` if it is an id every layer will accept, else None.

    An id only ever reached the wire through `device_headers`, which drops a
    malformed one silently -- so a hand-edited or truncated file degraded to
    "no device header" and nothing worse. `device_authorize` then began sending
    the same value in a request BODY, where no such filter sits, and a bad file
    turns into a 4xx on LOGIN. Validate once here, at adoption, so a value this
    module hands out is one all four layers agree on.
    """
    from probe.client_headers import _DEVICE_INSTANCE_RE

    if not isinstance(value, str) or not _DEVICE_INSTANCE_RE.fullmatch(value):
        return None
    return value


def device_file() -> Path:
    """Where this machine's identity lives.

    `PROBE_DEVICE_ID_PATH` wins outright. Failing that, an explicitly overridden
    `PROBE_CONFIG_PATH` pulls the device file alongside it, so a test or a dev
    environment that isolates its config does not quietly go on sharing the real
    machine's identity -- the precise divergence `config_path()` documents.
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

    Still read, and still the ONLY witness on a platform that offers no stable
    machine id -- see `_machine_witness`. Everywhere else it is written beside
    `machine` as the human-readable trace and never compared again once that
    field exists. `socket.gethostname()` is
    whatever the current network last called this machine -- on macOS the
    transient name follows the DHCP lease, so a laptop that joins a captive
    network becomes `visitor-10-59-125-182` and stops matching its own file.
    Because the witness GATES adoption, that read as "a different machine" and
    forked a second identity: the very "one laptop, two rows" bug this module
    exists to prevent, re-entered through the guard against it. See
    `_machine_witness` for the stable replacement, and `_ours` for how a file
    written before it is still adopted.
    """
    try:
        host = socket.gethostname().split(".")[0].strip()
    except OSError:
        host = ""
    return f"{host or 'unknown-host'}:{homedir.home()}"


def _darwin_host_uuid() -> str:
    """macOS's hardware UUID via `gethostuuid(2)`, or "" if it cannot be read.

    ctypes rather than `ioreg`/`scutil`: this runs on the startup path of every
    CLI invocation, and a subprocess there costs more than the whole lookup.

    THE TIMEOUT IS NOT OPTIONAL. `gethostuuid(2)` documents that a `wait` of
    `{0, 0}` means "wait INDEFINITELY until it completes" -- the opposite of the
    "don't block" reading the zero value invites. A kernel lookup that stalls
    would hang every CLI invocation before it printed anything, so pass a finite
    bound and take the hostname fallback on EWOULDBLOCK.

    `argtypes`/`restype` are declared because ctypes otherwise guesses: it
    assumes a C `int` return (right here by luck) and converts arguments by
    value, which is how a struct-pointer call quietly becomes undefined
    behaviour on a future ABI.
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

    `/etc/machine-id` on Linux, the hardware UUID on macOS. Both survive a DHCP
    lease, a WiFi change and a rename, and both still differ between two nodes
    sharing one `$HOME` -- which is the only property the witness needs.

    Returns "" when the platform offers neither, and the legacy hostname witness
    stays in charge -- including inside a container, where the file names the
    IMAGE rather than the machine (see `_in_container`).

    RESIDUAL LIMIT: a bare-metal or VM golden image that bakes `/etc/machine-id`
    and is not detected as a container hands every clone the same value, so
    clones sharing one `$HOME` would merge rather than split. That is the
    documented systemd footgun -- an image is meant to ship the file empty --
    and it needs a shared `$HOME` on top to bite.
    """
    global _MACHINE_ID_CACHE
    # SUCCESSES ONLY. Caching a failure would pin a long-lived process to the
    # hostname fallback for its whole life over one transient unreadable file --
    # re-enabling rename-driven splitting in exactly the process most likely to
    # outlive a network change.
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

    `/etc/machine-id` is a FILE IN THE IMAGE. Every replica started from one
    image reads the same value, so it names an image, not a machine -- and a
    fleet of replicas sharing a persistent `$HOME` (a k8s PVC, a mounted home
    volume) would all claim one identity. Measured on three replicas of one
    image with one shared home: the machine-id witness yields ONE id where the
    hostname witness correctly yields three. That is the merge this module
    calls strictly worse than a split, so inside a container the witness is
    withheld and the legacy hostname comparison governs -- which is the RIGHT
    answer there, because a container's hostname is unique to it and stable for
    its whole life. A laptop, which is what the stable witness exists for, is
    untouched by this.

    Deliberately conservative: only signals a container runtime actually
    creates. A false positive costs a host the fix; a false negative costs
    nothing that was not already true before this function existed.
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

    Hashed, not raw: a hardware UUID is a durable cross-application device
    fingerprint, and this file is readable by anything that can read `$HOME`. A
    hash answers the only question asked of it -- "is this the same machine?" --
    while being useless to anyone correlating devices across products.

    `$HOME` stays in the witness. The guard defends a home directory shared
    between machines, so the pair (machine, home) is what identifies "this
    machine's state", exactly as the legacy witness intended.
    """
    machine = _machine_id()
    if not machine:
        return None
    digest = hashlib.sha256(f"{machine}:{homedir.home()}".encode()).hexdigest()
    return f"m1:{digest[:_WITNESS_HEX_LEN]}"


def _read(path: Path) -> dict:
    """This file as a dict, or `{}` for anything that is not one.

    A shared `$HOME` is by definition a directory someone else can write to, so
    what is at `path` is untrusted input, not merely possibly-corrupt: a FIFO
    blocks the open forever and a symlink to `/dev/zero` reads until the process
    dies. Both hang or kill the CLI before it prints anything. Open without
    following a symlink, insist on a regular file, and stop reading at a bound
    no legitimate device file comes close to.
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
        # RecursionError is neither: a deeply nested payload escapes a plain
        # ValueError handler, and both callers turn that into a silent, total
        # loss of device identity with no log to say why.
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

    Best effort on purpose. A read-only `$HOME` means the machine keeps
    resolving by hostname, which is exactly what it did before this function
    existed -- degraded, not broken. The id itself is never touched: this only
    ever adds the fact that makes the NEXT rename a non-event.
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

    Returns None only when the id cannot be persisted at all -- a read-only home,
    a full disk. An id that is not on disk is worse than none: it would differ on
    every invocation and mint a new device row per command, which is the original
    bug amplified. Callers send nothing in that case and the server behaves
    exactly as it does for a client that predates device identity.
    """
    path = device_file()
    fingerprint = _home_fingerprint()
    witness = _machine_witness()

    def _claimed(payload: dict) -> str | None:
        """The id in `payload` when it records OUR stable machine witness.

        The strongest evidence available, and the only one that survives a
        rename: two files can disagree about what this machine is called and
        still agree about which machine it is.
        """
        value = _valid_id(payload.get("device_instance_id"))
        recorded = payload.get("machine")
        if value is None:
            return None
        if witness is None or not isinstance(recorded, str) or not recorded:
            return None
        return value if recorded == witness else None

    def _ours(payload: dict) -> str | None:
        """The id in `payload`, but only if this machine may claim it.

        A file carrying no `home` predates the witness and IS ours -- treating a
        missing witness as a mismatch would re-mint on upgrade and split every
        existing machine in two, which is the bug this guard exists to prevent.
        A file carrying someone else's home is a shared/NFS `$HOME` or a
        container image baked with another machine's state, and adopting it
        would merge two real machines into one row.

        A file that records a `machine` is judged on THAT alone: it was written
        by a client that knew the stable witness, so a hostname comparison can
        only ever second-guess it -- wrongly, since the hostname is the value
        that moves. The legacy `home` path below is for files written before the
        witness existed, and it stays exactly as strict as it always was: a
        hostname-only difference is NOT accepted as a rename here, because from
        disk alone it is indistinguishable from a second node on a shared
        `$HOME`, and merging two machines is the failure this module treats as
        strictly worse than splitting one.
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

    # STRONGEST EVIDENCE FIRST: the stable witness on the canonical file. This
    # is the steady state for every machine that owns it, and it answers with a
    # single read.
    claimed = _claimed(canonical)
    if claimed is not None:
        return claimed

    # THEN THIS MACHINE'S OWN NAMESPACED FILE, addressed DIRECTLY rather than
    # searched for. The name is a pure function of the witness, so a machine
    # that lives on a shared `$HOME` -- where the canonical file belongs to a
    # neighbour and never will be ours -- finds its identity in one more read,
    # from any network, forever.
    #
    # An earlier draft scanned the whole directory for any file bearing our
    # witness. It was doing this job the expensive way (a readdir on the startup
    # path of every invocation, on an NFS mount, over a set of filenames any
    # peer can add to) and it existed only to find a file this line addresses
    # outright.
    namespaced_path = _namespaced(canonical_path, witness) if witness is not None else None
    if namespaced_path is not None:
        claimed = _claimed(_read(namespaced_path))
        if claimed is not None:
            return claimed

    current = _ours(canonical)
    if current is not None:
        # Adoption already proved this file is ours; recording the stable
        # witness is what stops the next rename from forking it.
        _stamp(canonical_path, witness)
        return current

    # SHARED $HOME: give this machine its own file rather than overwriting the
    # other machine's. Overwriting looked like the obvious guard and is a trap --
    # on an NFS or container-shared home each node would reject the other's file
    # and rewrite it, so every invocation on every node mints a fresh id, which
    # is the "new device row per command" failure this module exists to prevent
    # and walks straight into the server's per-member device cap.
    #
    # Namespacing keeps the anti-merge guarantee (no machine ever adopts
    # another's id) while letting each one settle on a stable file of its own.
    #
    # THE WITNESS CHECK IS WHAT MAKES THIS SAFE, and testing merely that the
    # file EXISTS is not the same thing: the read above is a snapshot, so in a
    # race a second process can find the file written by the FIRST one on this
    # very machine and fork itself onto a namespaced path -- two ids for one
    # laptop, which is the failure the lock below exists to prevent,
    # reintroduced above it. Only a file this machine may not claim is another
    # machine's.
    #
    # A HOSTNAME-KEYED SIBLING IS NEVER ADOPTED HERE, and that is the whole
    # reason this branch is short. A machine that forked before the witness
    # existed does have an id sitting in `_namespaced(path, fingerprint)`, and
    # reclaiming it would spare it a duplicate row -- but the DHCP names that
    # caused the fork are derived from an IP, so two machines on one captive
    # network are handed the same one. Adopting on that evidence lets a second
    # machine take a first machine's id, and stamping it would make the theft
    # permanent. This module's stated order of preference settles it: splitting
    # one machine into two rows costs a row somebody can retire, merging two
    # machines into one destroys the evidence that they were ever separate.
    if _valid_id(canonical.get("device_instance_id")) and current is None:
        path = namespaced_path or _namespaced(canonical_path, fingerprint)
        current = _ours(_read(path))
        if current is not None:
            _stamp(path, witness)
            return current

    # Serialize the first-run mint. Without it two concurrent `probe` processes
    # both find nothing, both mint, and one machine ends up with two permanent
    # device rows -- from ordinary concurrency, not from losing the file.
    lock = path.with_suffix(".lock")
    holder = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        holder = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        # Someone else is minting. Give them a moment and re-read rather than
        # racing them; a stale lock is broken below on the next invocation.
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
        # Re-read under the lock: the winner may have finished between our first
        # read and acquiring it. Through `_ours`, NOT raw -- reading the id
        # directly here would re-adopt the very file the home check just
        # rejected, and the mismatch guard would silently do nothing.
        current = _ours(_read(path))
        if current is not None:
            return current
        minted = _mint()
        payload = {
            "device_instance_id": minted,
            "created_at": int(time.time()),
            "home": fingerprint,
        }
        # `home` stays for the human reading this file and for a client rolled
        # back to a version that only understands it; `machine` is what the
        # next rename is judged against.
        if witness is not None:
            payload["machine"] = witness
        _write(path, payload)
        return minted
    except OSError:
        return None
    finally:
        os.close(holder)
        lock.unlink(missing_ok=True)
