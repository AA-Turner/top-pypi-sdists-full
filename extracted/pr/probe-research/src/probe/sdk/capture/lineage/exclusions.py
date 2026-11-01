"""which paths are never a run's input or output: system and tool caches, Probe's own folders, credentials, .probeignore and .probe.config."""

from __future__ import annotations
import functools
import os
import sys
from typing import Any
#: Environment variables naming cache folders: a write under one is a download.
_CACHE_ENVS = (
    "XDG_CACHE_HOME",
    "HF_HOME",
    "HF_HUB_CACHE",
    "HF_DATASETS_CACHE",
    "TRANSFORMERS_CACHE",
    "TORCH_HOME",
)
#: Path fragments under which a write is a cache fill, never an output.
_WRITE_ONLY_PARTS = ("/.cache/",)
#: Longest path sent. The server keys reads on the path, and a btree entry has
#: a hard size limit; one over it would fail the whole batch it rides in.
MAX_PATH_BYTES = 2048
#: Below this, a `.probe.config` `hash` path is sent with its path and size
#: only (F30): no sha256, fingerprint or rows. The server's 64-byte floor
#: (`MIN_MATCH_BYTES`) is a MATCH floor; this one keeps the hash off the wire.
HASH_LEVEL_MIN_BYTES = 64

_CODE_SUFFIXES = (".py", ".pyc", ".pyo", ".pyd", ".so", ".dylib", ".dll", ".pth", ".pyi")
#: Operating-system trees. `/usr` by its system parts only: `/usr/src/app` is
#: the working directory of the official Python images.
_SYSTEM_PREFIXES = (
    "/proc/",
    "/sys/",
    "/dev/",
    "/etc/",
    "/usr/lib/",
    "/usr/lib64/",
    "/usr/libexec/",
    "/usr/share/",
    "/usr/include/",
    "/usr/bin/",
    "/usr/sbin/",
    "/usr/local/lib/",
    "/usr/local/share/",
    "/usr/local/include/",
    "/usr/local/bin/",
    "/lib/",
    "/lib64/",
    "/bin/",
    "/sbin/",
    "/System/",
    "/Library/",
    "/private/etc/",
    "/private/var/db/",
    "/run/",
    "/var/lib/",
)
#: Under a system prefix but where data lives: removable and mounted disks.
_SYSTEM_ALLOWED = ("/run/media/", "/run/mnt/")
#: Path fragments of tool caches. Deliberately NOT all of ~/.cache: model and
#: dataset caches (huggingface, torch hub) hold the inputs lineage is about.
_TOOL_CACHE_PARTS = (
    "/.cache/pip/",
    "/.cache/uv/",
    "/.cache/pypoetry/",
    "/.cache/torch_extensions/",
    "/.cache/pre-commit/",
    "/.cache/matplotlib/",
    "/.cache/fontconfig/",
    "/.triton/",
    "/.nv/",
    "/__pycache__/",
    "/.ipython/",
    "/.jupyter/",
    "/.config/probe/",
    "/.local/state/probe/",
    "/.probe/",
)
#: Where tools keep credentials. A read's path and hash are shown to everyone
#: who can see the run, so a token file must never become one -- including the
#: ones inside a cache that is otherwise a real input (~/.cache/huggingface).
_CREDENTIAL_PARTS = (
    "/.ssh/",
    "/.gnupg/",
    "/.aws/",
    "/.azure/",
    "/.kube/",
    "/.docker/",
    "/.kaggle/",
    "/.config/gh/",
    "/.config/gcloud/",
    "/.config/wandb/",
    "/.cache/huggingface/token",
    "/.cache/huggingface/stored_tokens",
    "/.huggingface/token",
    "/.databrickscfg",
    "/.netrc",
    "/.pgpass",
    "/.git-credentials",
    "/.modal.toml",
)


def _as_prefix(path: Any) -> set[str]:
    """``path`` as the prefixes a hooked path may start with: as given and
    resolved (a symlinked home), each ending in a separator."""
    out: set[str] = set()
    try:
        for p in (os.path.abspath(os.fspath(path)), os.path.realpath(os.fspath(path))):
            out.add(p if p.endswith(os.sep) else p + os.sep)
    except (TypeError, ValueError, OSError):
        pass
    return out


#: Interpreter prefixes that are whole system roots: a Debian/Ubuntu Python (or
#: a venv on one) has `base_prefix = /usr`, and excluding it would drop
#: `/usr/src/app`, the working directory of the official images. Its library
#: folders are excluded by name instead (sysconfig, below).
_ROOT_PREFIXES = ("/", "/usr", "/usr/local")


def _excluded_prefixes() -> tuple[str, ...]:
    prefixes = {
        p for p in (sys.prefix, sys.base_prefix, sys.exec_prefix) if p not in _ROOT_PREFIXES
    }
    try:
        import site
        import sysconfig

        prefixes.update(site.getsitepackages())
        prefixes.add(site.getusersitepackages())
        for name in ("stdlib", "platstdlib", "purelib", "platlib"):
            path = sysconfig.get_paths().get(name)
            if path:
                prefixes.add(path)
    except Exception:  # noqa: BLE001 -- a virtualenv without site helpers
        pass
    out = []
    for p in prefixes:
        if p:
            p = os.path.abspath(p)
            out.append(p if p.endswith(os.sep) else p + os.sep)
    return tuple(sorted(out))


@functools.cache
def _interpreter_prefixes() -> tuple[str, ...]:
    return _excluded_prefixes()


def _ignored(rules: Any, path: str) -> bool:
    """Whether a ``.probeignore`` pattern excludes ``path`` (plan (n)). Checked
    after :func:`excluded`, so it only ever removes. A path outside the rules'
    root is matched by the unanchored patterns only, and a read is matched as
    opened AND as resolved, since ``open()`` follows symlinks (see
    :mod:`probe.sdk.recording_rules.ignore`)."""
    return rules is not None and rules.ignored(path, follow=True)


def _config_verdict(path: str, *, resolve: bool = True) -> Any:
    """A researcher's `.probe.config` verdict on ``path`` (`probe_config.Verdict`)."""
    from ...recording_rules import recording_rules as _exclusions

    return _exclusions.excluded(path, is_dir=False, hot=True, resolve=resolve)


def _not_recorded(verdict: Any) -> bool:
    """`read` and `off` record nothing; `hash` records the identity (C9)."""
    return bool(verdict.excluded) and not verdict.identity_only


def _config_excluded(path: str, *, resolve: bool = True) -> bool:
    """Excluded by a researcher's `.probe.config` (paths Probe never records:
    `read` and `off`; a `hash` path IS recorded, identity only). Judged once
    per path where a read or write is recorded (the recorder's own stat
    happened; this adds only `lstat`s of `.probe.config` files, cached per
    folder for a second), and again where reads are hashed and sent (a `probe
    exec` child's spool is collected by its launcher). Never noted, counted or
    hashed."""
    return _not_recorded(_config_verdict(path, resolve=resolve))


def _hash_level(path: str) -> bool:
    """Is ``path`` at `.probe.config` `hash`: recorded by identity only, and
    below `HASH_LEVEL_MIN_BYTES` with no hash at all (F30)?"""
    return bool(_config_verdict(path).identity_only)


def _below_floor(path: str, size: Any) -> bool:
    """A `hash`-level file too small to send a hash of (F30): its path and size
    go, never its sha256, fingerprint or rows. A hash of a tiny file names its
    content to anyone who can guess it."""
    return isinstance(size, int) and size < HASH_LEVEL_MIN_BYTES and _hash_level(path)


def _sendable(path: str) -> bool:
    """A path the server can store: UTF-8 (a filename of arbitrary bytes decodes
    to lone surrogates) and short enough to key on."""
    try:
        return len(path.encode("utf-8")) <= MAX_PATH_BYTES
    except UnicodeEncodeError:
        return False


#: folder -> (its ``os.path.realpath``, the folder's identity then), per
#: process. Resolving a whole path costs one lstat per component, and the
#: write hook resolves every new path it notes: with the folder cached it
#: costs two lstats (the folder, and whether the file itself is a link).
#: Cleared when full.
_real_dirs: dict[str, tuple[str, tuple]] = {}
_REAL_DIRS_MAX = 4096


def _dir_key(st: os.stat_result) -> tuple:
    """What a cached resolution of a folder is valid for: the entry the path
    reaches (``lstat``: through every link on the way, not the last). A link
    retargeted on the way reaches another folder (another inode); the folder
    itself a link, retargeted, is a new link -- and a new ctime, since an
    inode number can be reused at once."""
    import stat as _stat

    link = _stat.S_ISLNK(st.st_mode)
    return (st.st_dev, st.st_ino, link, st.st_ctime_ns if link else 0)


def _resolved(path: str) -> str:
    """``os.path.realpath(path)`` for an absolute path, from the cached
    resolution of its folder -- valid while the folder is the same entry
    (`_dir_key`) -- and one lstat of the file itself."""
    head, tail = os.path.split(path)
    try:
        key = _dir_key(os.lstat(head))
    except OSError:
        return os.path.realpath(path)
    cached = _real_dirs.get(head)
    if cached is not None and cached[1] == key:
        real = cached[0]
    else:
        real = os.path.realpath(head)
        if len(_real_dirs) >= _REAL_DIRS_MAX:
            _real_dirs.clear()
        _real_dirs[head] = (real, key)
    candidate = os.path.join(real, tail) if tail else real
    return os.path.realpath(candidate) if os.path.islink(candidate) else candidate


def _write_config_excluded(path: str, real: str) -> bool:
    """`.probe.config` on a write, as opened AND as resolved: the stricter of
    the two decides (a `hash` link to a `read` file is `off`)."""
    verdict = _config_verdict(path, resolve=False)
    if real != path and not verdict.hidden:
        from ... import probe_config as _pc

        verdict = _pc.stricter(verdict, _config_verdict(real, resolve=False))
    return _not_recorded(verdict)


def _write_skip(target: "_RunReads", path: str) -> bool:
    """Whether a write-open of ``path`` is never noted: :func:`excluded`, the
    run's ``.probeignore``, a cache -- as opened AND as resolved, so a link
    into ``~/.cache/huggingface`` is a download too. Judged once per path per
    process (``write_skipped``), since the rules do not change."""
    if path in target.write_skipped:
        return True
    real = _resolved(path)
    if (
        excluded(path)
        or write_excluded(path)
        or _ignored(target.ignore, path)
        or (real != path and (excluded(real) or write_excluded(real)))
        or _write_config_excluded(path, real)
    ):
        if len(target.write_skipped) < MAX_PATHS:
            target.write_skipped.add(path)
        return True
    return False
from probe.sdk.capture.lineage.lineage import _RunReads, excluded, write_excluded  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.spool.spool import MAX_PATHS  # noqa: E402 -- pieces need each other; the front door loads this one first
