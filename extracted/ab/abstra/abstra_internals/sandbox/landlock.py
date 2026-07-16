"""Minimal Linux Landlock filesystem sandbox (ABI ≥ 3), via raw syscalls.

Landlock (kernel ≥ 5.13) lets an *unprivileged* process irrevocably drop its
own filesystem access down to an explicit allowlist — no root, no capabilities,
no seccomp. We use it to run console-originated Python snippets read-only over
the whole filesystem (so `abstra.files` / EFS reads still work) while permitting
writes only to scratch dirs. Production EFS mounts — `{projectId}/files`,
`/temp`, `/disabled-stages` — become unwritable structurally, at the kernel.

Why raw ctypes and not a library: zero new native deps, and the surface we need
is exactly three syscalls. Everything here is Linux-only and self-contained.

IRREVOCABILITY: `landlock_restrict_self` cannot be undone for the life of the
process (or reversed in its children — restrictions inherit). Never call this in
a pooled/reused executor; only in a throwaway process that exits after one
snippet. See controllers/execution/sandboxed_snippet.py.

FAIL-CLOSED: if the kernel is too old (ABI < min) or any syscall fails, we raise
rather than silently running unsandboxed. Callers must treat that as "refuse to
run", never as "run anyway".
"""

import ctypes
import os
import platform
from typing import Iterable, List

# Syscall numbers are identical on the arches we deploy (x86_64, aarch64); they
# were added together in the generic range. Guard rather than guess elsewhere.
_SYSCALLS = {
    "x86_64": (444, 445, 446),
    "aarch64": (444, 445, 446),
}

# landlock_create_ruleset(NULL, 0, LANDLOCK_CREATE_RULESET_VERSION) -> ABI version
_LANDLOCK_CREATE_RULESET_VERSION = 1 << 0
_LANDLOCK_RULE_PATH_BENEATH = 1

# prctl(PR_SET_NO_NEW_PRIVS, 1, ...) — required before restrict_self.
_PR_SET_NO_NEW_PRIVS = 38

# O_PATH is Linux-only; name it via getattr so type-checkers on macOS/CI don't
# choke. Value is stable across the arches we run.
_O_PATH = getattr(os, "O_PATH", 0o10000000)

# filesystem access-right bits (handled_access_fs), grouped by the ABI that
# introduced them so we only ask the kernel about bits it knows (unknown bits
# make create_ruleset fail with EINVAL).
_FS_ABI1 = {
    "EXECUTE": 1 << 0,
    "WRITE_FILE": 1 << 1,
    "READ_FILE": 1 << 2,
    "READ_DIR": 1 << 3,
    "REMOVE_DIR": 1 << 4,
    "REMOVE_FILE": 1 << 5,
    "MAKE_CHAR": 1 << 6,
    "MAKE_DIR": 1 << 7,
    "MAKE_REG": 1 << 8,
    "MAKE_SOCK": 1 << 9,
    "MAKE_FIFO": 1 << 10,
    "MAKE_BLOCK": 1 << 11,
    "MAKE_SYM": 1 << 12,
}
_FS_REFER = 1 << 13  # ABI 2
_FS_TRUNCATE = 1 << 14  # ABI 3 — without this, O_TRUNC can still empty an EFS file
_FS_IOCTL_DEV = 1 << 15  # ABI 5

# Read-only view: everything a snippet may do WITHOUT mutating the tree.
_READ_ONLY_BITS = _FS_ABI1["READ_FILE"] | _FS_ABI1["READ_DIR"] | _FS_ABI1["EXECUTE"]


class SandboxError(Exception):
    """A Landlock syscall failed unexpectedly."""


class SandboxUnavailable(SandboxError):
    """Landlock is not usable here (wrong OS, or ABI below the required floor)."""


class _RulesetAttr(ctypes.Structure):
    # Only handled_access_fs. handled_access_net / handled_access_scoped are
    # later-ABI fields we don't use; the kernel zero-fills the rest given our
    # size, which means "don't restrict network/scoping" — intended.
    _fields_ = [("handled_access_fs", ctypes.c_uint64)]


class _PathBeneathAttr(ctypes.Structure):
    # NOTE: packed — the kernel struct is __attribute__((packed)); u64 + s32 = 12
    # bytes, not 16. Getting this wrong silently corrupts parent_fd.
    _pack_ = 1
    _fields_ = [("allowed_access", ctypes.c_uint64), ("parent_fd", ctypes.c_int32)]


def _libc() -> ctypes.CDLL:
    return ctypes.CDLL(None, use_errno=True)


def _syscalls() -> tuple:
    arch = platform.machine()
    nums = _SYSCALLS.get(arch)
    if nums is None:
        raise SandboxUnavailable(f"Landlock syscall numbers unknown for arch {arch!r}")
    return nums


def get_abi_version() -> int:
    """Return the kernel's Landlock ABI version, or 0 if Landlock is absent."""
    if platform.system() != "Linux":
        return 0
    try:
        create_nr, _, _ = _syscalls()
    except SandboxUnavailable:
        return 0
    libc = _libc()
    ctypes.set_errno(0)
    abi = libc.syscall(
        create_nr,
        None,
        ctypes.c_size_t(0),
        ctypes.c_uint32(_LANDLOCK_CREATE_RULESET_VERSION),
    )
    return abi if abi > 0 else 0


def _handled_mask(abi: int) -> int:
    mask = 0
    for bit in _FS_ABI1.values():
        mask |= bit
    if abi >= 2:
        mask |= _FS_REFER
    if abi >= 3:
        mask |= _FS_TRUNCATE
    if abi >= 5:
        mask |= _FS_IOCTL_DEV
    return mask


def restrict_filesystem(
    read_roots: Iterable[str],
    write_roots: Iterable[str],
    *,
    min_abi: int = 3,
) -> None:
    """Irreversibly restrict THIS process to: read `read_roots`, write `write_roots`.

    `read_roots` get read+list+execute; `write_roots` get the full handled set
    (create/write/remove/truncate/...). Access to a path is the union of every
    matching rule, so a write root beneath a read root is writable.

    min_abi defaults to 3 so TRUNCATE is always enforceable — an ABI-2 kernel
    would let a snippet `open(path, "w")` an existing EFS file and empty it.

    Raises SandboxUnavailable (too old / not Linux) or SandboxError (syscall
    failure). On success there is no return path to un-restrict.
    """
    if platform.system() != "Linux":
        raise SandboxUnavailable("Landlock is Linux-only")

    abi = get_abi_version()
    if abi < min_abi:
        raise SandboxUnavailable(
            f"Landlock ABI {abi} < required {min_abi} (TRUNCATE unavailable)"
        )

    create_nr, add_rule_nr, restrict_nr = _syscalls()
    libc = _libc()
    handled = _handled_mask(abi)
    write_mask = handled  # writable dirs may do anything we handle
    read_mask = _READ_ONLY_BITS & handled

    # 1) no_new_privs — mandatory precondition for restrict_self.
    if libc.prctl(_PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0:
        raise SandboxError(
            f"prctl(PR_SET_NO_NEW_PRIVS) failed: {os.strerror(ctypes.get_errno())}"
        )

    # 2) create the ruleset over the access rights we intend to govern.
    attr = _RulesetAttr(handled_access_fs=handled)
    ctypes.set_errno(0)
    ruleset_fd = libc.syscall(
        create_nr,
        ctypes.byref(attr),
        ctypes.c_size_t(ctypes.sizeof(attr)),
        ctypes.c_uint32(0),
    )
    if ruleset_fd < 0:
        raise SandboxError(
            f"landlock_create_ruleset failed: {os.strerror(ctypes.get_errno())}"
        )

    opened: List[int] = []
    try:
        # 3) one PATH_BENEATH rule per existing root.
        def _add(path: str, allowed: int) -> None:
            if not os.path.exists(path):
                return  # skip missing optional roots rather than fail the whole sandbox
            # O_PATH: a handle for naming only (no read perm needed); CLOEXEC so
            # it can't leak into anything the snippet might exec.
            fd = os.open(path, _O_PATH | os.O_CLOEXEC)
            opened.append(fd)
            rule = _PathBeneathAttr(allowed_access=allowed, parent_fd=fd)
            ctypes.set_errno(0)
            rc = libc.syscall(
                add_rule_nr,
                ruleset_fd,
                _LANDLOCK_RULE_PATH_BENEATH,
                ctypes.byref(rule),
                ctypes.c_uint32(0),
            )
            if rc != 0:
                raise SandboxError(
                    f"landlock_add_rule({path}) failed: {os.strerror(ctypes.get_errno())}"
                )

        for path in read_roots:
            _add(path, read_mask)
        for path in write_roots:
            _add(path, write_mask)

        # 4) enforce. Irreversible from here.
        ctypes.set_errno(0)
        if libc.syscall(restrict_nr, ruleset_fd, ctypes.c_uint32(0)) != 0:
            raise SandboxError(
                f"landlock_restrict_self failed: {os.strerror(ctypes.get_errno())}"
            )
    finally:
        for fd in opened:
            os.close(fd)
        os.close(ruleset_fd)


if __name__ == "__main__":
    # Smoke test: read-only everywhere, write only /tmp. Run on a Landlock host.
    import sys
    import tempfile

    print(f"Landlock ABI: {get_abi_version()}  kernel: {platform.release()}")
    scratch = tempfile.mkdtemp(prefix="landlock-smoke-")
    restrict_filesystem(read_roots=["/"], write_roots=["/tmp", scratch])

    with open(os.path.join(scratch, "allowed.txt"), "w", encoding="utf-8") as ok:
        ok.write("scratch write allowed")
    print("write to scratch: OK")

    with open("/etc/hostname", encoding="utf-8") as f:
        f.read()
    print("read /etc/hostname: OK")

    try:
        open("/etc/abstra-should-fail", "w", encoding="utf-8")
        print("FAIL: wrote outside allowlist")
        sys.exit(1)
    except PermissionError:
        print("write to /etc: correctly DENIED")
