"""SDK non-disruptive code + environment capture (Execution Record).

``capture_git_snapshot`` READS git provenance (HEAD, branch, dirty) and writes
nothing into the repository. It used to commit the whole working tree, untracked
files included, into a shadow ref ``refs/probe/snapshots/<run_id>``: that needed a
git identity (a bare pod has none, and then nothing at all was captured), grew
one repo's ``.git`` from 20 to 306 MB, and ``git push --mirror`` published the
refs -- an untracked `.env` among them. Nothing ever read the shadow commit: the
captured BYTES are the record (see ``capture_manifest``). Old refs are reported
once and removed only by ``probe snapshot-prune-refs`` (plan 2.6, decision D10).

GPU capture is best-effort ambient context. Dependency capture is STRICT by
default, in both directions that matter: it raises rather than storing an empty
package set, AND rather than storing the WRONG one. The second guard exists
because the first is not enough -- an out-of-process caller (the CLI is a
uv-tool install with its own interpreter) that enumerates itself produces a
full, plausible, entirely wrong dependency list, which is indistinguishable
downstream from a correct capture. See ``capture_env``.
"""

from __future__ import annotations

import fnmatch
import contextlib
import hashlib
import json
import os
import unicodedata
import stat
import platform
import re
import socket
import subprocess
import sys
import tempfile
import time
from collections import Counter
from functools import lru_cache
from typing import Any, Literal

from ..tap_core.secrets import _keyword_windows
from ..tap_core.secrets import scan as _scan
from ..tap_core.secrets import scan_quick as _scan_quick
from . import homedir
from . import ignore as _ignore
from . import owndirs as _owndirs
from . import secret_gate as _secret_gate
from .errors import RosError
from .hashing import local_file_uri


class SnapshotError(RosError):
    """Git plumbing failed or the cwd is not a git repository."""


# `ls-remote` is the only git call here that touches the network. Left unbounded
# it can block the start of a training run indefinitely -- on an unreachable host,
# or worse, waiting forever on a credential prompt nobody is there to answer.
_LS_REMOTE_TIMEOUT = 10.0
# A verify fetch pulls one commit at depth 1. Bounded for the same reason as
# ls-remote: an audit must not wedge on one unreachable remote.
_VERIFY_TIMEOUT = 20.0


def _NONINTERACTIVE_ENV() -> dict:
    """Git env that fails fast instead of prompting for credentials."""
    return {
        **os.environ,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_SSH_COMMAND": os.environ.get(
            "GIT_SSH_COMMAND", "ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new"
        ),
    }


def _read_only(env: dict | None = None) -> dict:
    """Git env for a capture: ``GIT_OPTIONAL_LOCKS=0`` so ``status`` never
    refreshes and rewrites the user's index behind their back. Every git call
    a capture makes goes through here; a capture never writes to ``.git``."""
    return {**(os.environ if env is None else env), "GIT_OPTIONAL_LOCKS": "0"}


def _git(
    cwd: str,
    *args: str,
    env: dict | None = None,
    check: bool = True,
    timeout: float | None = None,
) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=cwd,
            env=_read_only(env),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        if check:
            raise SnapshotError(f"git {' '.join(args)}: timed out after {timeout}s") from None
        return ""
    if check and proc.returncode != 0:
        raise SnapshotError(f"git {' '.join(args)}: {proc.stderr.strip()}")
    return proc.stdout.strip()


def _git_paths(cwd: str, *args: str, check: bool = True) -> list[str]:
    """Run a `-z`-terminated git listing and return its paths, decoded the way the
    filesystem would (`os.fsdecode`, surrogateescape), never line-split.

    Path listings MUST come through here, not through :func:`_git` +
    ``splitlines()``: without ``-z`` git C-quotes anything unusual (a double
    quote, a backslash, a tab, and by default every non-ASCII byte), the quoted
    form fails ``isfile`` and the file silently leaves the manifest; and with
    quoting off, ``str.splitlines()`` treats U+2028 as a line break, so a
    directory named ``x\u2028..`` yields a manifest path ``../...`` that walks
    OUT of the tree (found by review: a cloned repo could capture the sibling
    ``~/.ssh/id_rsa``). NUL is the one byte a path cannot contain.
    """
    proc = subprocess.run(["git", *args], cwd=cwd, env=_read_only(), capture_output=True)
    if check and proc.returncode != 0:
        raise SnapshotError(f"git {' '.join(args)}: {proc.stderr.decode('utf-8', 'replace').strip()}")
    return [os.fsdecode(chunk) for chunk in proc.stdout.split(b"\0") if chunk]


def _utf8_clean(path: str) -> bool:
    try:
        path.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def _printable(path: str) -> str:
    """A surrogate-escaped (non-UTF-8) name rendered with U+FFFD so it can be
    logged and stored in JSON; used only where the name is REPORTED, never
    where it must open the file."""
    return path if _utf8_clean(path) else path.encode("utf-8", "surrogateescape").decode("utf-8", "replace")


def wire_name(path: str) -> str:
    """The name a manifest path travels under to the server: NFC, which the
    server canonicalises to and echoes. The manifest keeps the path as the
    filesystem spelled it (already POSIX, see ``_posix``); restore and
    snapshot-show map back through this same function."""
    return unicodedata.normalize("NFC", path)


def _posix(rel: str) -> str:
    """Manifest paths are POSIX on every box: a Windows walk yields backslashes,
    which the server refuses and a Linux restore would not match. Recorded at
    capture time so the reader never has to know which box captured."""
    return rel.replace(os.sep, "/") if os.sep != "/" else rel


def is_inside_tree(path: str) -> bool:
    """True iff a manifest/archive path is relative and never leaves the tree.
    Git will not track a ``..`` component, so a manifest that carries one was
    not produced by the walk this module does -- treat it as hostile."""
    if not path or os.path.isabs(path) or "\0" in path:
        return False
    # Windows treats a backslash as a separator and `C:` as a drive: a name a
    # POSIX capture stored verbatim must not become `..\..\x` or `C:\x` on a
    # Windows restore. Split on BOTH separators; a plain `back\slash.py` still
    # passes (no dot segments), so real filenames are not lost.
    if path.startswith("\\") or re.match(r"^[A-Za-z]:", path):
        return False
    return all(seg not in ("", ".", "..") for seg in re.split(r"[\\/]", path))


def _repo_check(cwd: str) -> tuple[bool, str | None]:
    """``(inside a work tree, why git could not say)``. The reason is set only
    when git could not answer -- no git executable, or git refusing the repo
    (``detected dubious ownership`` in a container) -- never for a plain
    directory, which is not an error."""
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=cwd,
            env=_read_only(),
            capture_output=True,
            text=True,
        )
    except OSError as exc:  # no git binary (a slim image), or not executable
        return False, f"git is not runnable here ({type(exc).__name__})"
    if proc.returncode == 0 and proc.stdout.strip() == "true":
        return True, None
    stderr = proc.stderr.strip()
    if proc.returncode != 0 and "not a git repository" not in stderr:
        return False, (stderr.splitlines()[0] if stderr else f"git exited {proc.returncode}")
    return False, None


def is_git_repo(cwd: str) -> bool:
    """True inside a git work tree git can read. Any failure to ask -- no git
    executable, a repo git refuses -- is False, and the capture falls back to the
    directory manifest rather than to nothing."""
    return _repo_check(cwd)[0]


def _dot_git_above(cwd: str) -> bool:
    here = os.path.abspath(cwd)
    while True:
        if os.path.exists(os.path.join(here, ".git")):
            return True
        parent = os.path.dirname(here)
        if parent == here:
            return False
        here = parent


def capture_git_snapshot(run_id: str | None = None, cwd: str | None = None) -> dict[str, Any]:
    """Git PROVENANCE for the tree a run starts in: HEAD, branch, dirty.

    READ-ONLY. Three reads under ``GIT_OPTIONAL_LOCKS=0`` (``rev-parse --verify -q
    HEAD``, ``symbolic-ref --short -q HEAD``, ``status --porcelain``), so no object,
    ref or index write happens and none of what used to break capture can: no
    author identity (a bare pod), an unborn HEAD, a read-only ``.git``.

    ``commit`` and ``ref`` are always None: the shadow commit is retired (see the
    module docstring). They stay in the shape because callers read them.
    ``run_id`` is accepted and unused, for the same reason.

    Raises :class:`SnapshotError` if ``cwd`` is not a git repo.
    """
    cwd = cwd or os.getcwd()
    if not is_git_repo(cwd):
        raise SnapshotError(f"{cwd} is not a git repository")
    return _git_state(cwd)[0]


def _git_state(cwd: str) -> tuple[dict[str, Any], str | None]:
    """HEAD, branch and dirty, plus why dirty is unknown (or None).

    ``status`` reads the index and HEAD does not, so a corrupt index fails only
    the dirty check: HEAD and the branch are still recorded, dirty is None
    (unknown, never guessed) and git's reason is returned for ``git_error``.
    """
    head = _git(cwd, "rev-parse", "--verify", "-q", "HEAD", check=False) or None
    # An unborn branch still has a name; a detached HEAD has none (None).
    branch = _git(cwd, "symbolic-ref", "--short", "-q", "HEAD", check=False) or None
    dirty: bool | None
    try:
        dirty, error = bool(_git(cwd, "status", "--porcelain", check=True)), None
    except SnapshotError as exc:
        dirty, error = None, str(exc)
    return {"commit": None, "ref": None, "branch": branch, "head": head, "dirty": dirty}, error


def git_provenance(cwd: str) -> tuple[dict[str, Any] | None, str | None]:
    """``(capture_git_snapshot(...) or None, git_error or None)``, never raising.

    Git is provenance, not the record, so it may never cost the capture: a repo
    git cannot read is captured as a plain directory, and WHY is returned for
    ``meta.git_error``. A plain directory is not an error.
    """
    in_repo, reason = _repo_check(cwd)
    if not in_repo:
        # Only a directory that IS a repo (a `.git` above it) is missing
        # something; a plain folder has no provenance to lose.
        return None, (reason if reason and _dot_git_above(cwd) else None)
    try:
        info, error = _git_state(cwd)
    except (SnapshotError, OSError) as exc:
        return None, str(exc) or type(exc).__name__
    notice_old_snapshot_refs(cwd)
    return info, error


#: Where the retired shadow commits lived. Still READ (to report and prune them).
SNAPSHOT_REFS_PREFIX = "refs/probe/snapshots/"


def old_snapshot_refs(cwd: str) -> list[tuple[str, str]]:
    """Every ``refs/probe/snapshots/*`` ref in this repo as ``(ref, sha)``, loose
    or packed (``for-each-ref`` reads both). A ref name cannot hold a space."""
    out: list[tuple[str, str]] = []
    listing = _git(
        cwd, "for-each-ref", "--format=%(objectname) %(refname)", SNAPSHOT_REFS_PREFIX, check=False
    )
    for line in listing.splitlines():
        sha, _, ref = line.partition(" ")
        if ref.startswith(SNAPSHOT_REFS_PREFIX):
            out.append((ref, sha))
    return out


def bundle_snapshot_refs(cwd: str, refs: list[str], path: str) -> None:
    """Back ``refs`` up, with every object they reach, to a git bundle at
    ``path``, and verify it. Undo a prune with
    ``git fetch <path> 'refs/probe/snapshots/*:refs/probe/snapshots/*'``, even
    after gc has removed the objects from the repo.

    The bundle holds the same bytes the refs do (an untracked ``.env`` among
    them), so it may not land in the working tree: the next code capture would
    upload it, and ``git add .`` would commit it.
    """
    top = _git(cwd, "rev-parse", "--show-toplevel", check=False)
    target = os.path.realpath(path)
    if top:
        top = os.path.realpath(top)
        git_dir = os.path.realpath(os.path.join(top, ".git"))
        inside = target == top or target.startswith(top + os.sep)
        if inside and not target.startswith(git_dir + os.sep):
            raise SnapshotError(
                f"{path} is inside the working tree ({top}); code capture would upload "
                "it. Write the bundle somewhere outside the repository."
            )
    if os.path.exists(target):
        raise SnapshotError(f"{path} already exists; refusing to overwrite it")
    proc = subprocess.run(
        ["git", "bundle", "create", target, "--stdin"],
        cwd=cwd,
        input="".join(f"{ref}\n" for ref in refs),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SnapshotError(f"git bundle create: {proc.stderr.strip()}")
    check = subprocess.run(
        ["git", "bundle", "list-heads", target], cwd=cwd, capture_output=True, text=True
    )
    held = {line.split(" ", 1)[1] for line in check.stdout.splitlines() if " " in line}
    if check.returncode != 0 or not set(refs) <= held:
        raise SnapshotError(f"git bundle {path} does not hold every ref; nothing deleted")


def prune_snapshot_refs(cwd: str, refs: list[tuple[str, str]]) -> None:
    """Delete exactly these ``(ref, sha)`` pairs, in one transaction.

    EXPLICIT ONLY (decision D10): a shadow commit may be the only copy of a dirty
    tree whose upload failed, so nothing deletes these on its own, and the CLI
    decides which are safe. One ``update-ref --stdin`` transaction removes packed
    refs as well as loose ones, and each delete names the sha it expects: a ref
    that moved after it was listed fails the whole transaction rather than
    deleting a commit nobody saw. The objects stay until git's gc removes them.
    """
    if not refs:
        return
    proc = subprocess.run(
        ["git", "update-ref", "--stdin"],
        cwd=cwd,
        input="".join(f"delete {ref} {sha}\n" for ref, sha in refs),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SnapshotError(f"git update-ref: {proc.stderr.strip()}")
    # What the notice counted is gone: the refs still left get one fresh notice.
    forget_snapshot_ref_notice(cwd)


_NOTICED: set[str] = set()


def _notice_marker(common_dir: str) -> str:
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(str(homedir.home()), ".local", "state")
    key = hashlib.sha256(os.path.abspath(common_dir).encode("utf-8", "surrogateescape")).hexdigest()[:16]
    return os.path.join(base, "probe", "notices", f"snapshot-refs-{key}")


def _common_dir(cwd: str) -> str | None:
    common = _git(cwd, "rev-parse", "--git-common-dir", check=False)
    if not common:
        return None
    return os.path.abspath(common if os.path.isabs(common) else os.path.join(cwd, common))


def _shown_count(marker: str) -> int | None:
    """How many refs the last notice counted, or None if it was never shown."""
    try:
        with open(marker, encoding="utf-8") as fh:
            return int(fh.read().strip() or "0")
    except (OSError, ValueError):
        return None


def _write_marker(marker: str, count: int) -> None:
    try:
        os.makedirs(os.path.dirname(marker), exist_ok=True)
        with open(marker, "w", encoding="utf-8") as fh:
            fh.write(f"{count}\n")
    except OSError:
        pass  # once per process instead of once per machine


def forget_snapshot_ref_notice(cwd: str) -> None:
    """Let the notice show again for this repo (after a prune)."""
    try:
        common = _common_dir(cwd)
        if common:
            _NOTICED.discard(common)
            with contextlib.suppress(FileNotFoundError):
                os.remove(_notice_marker(common))
    except Exception:  # noqa: BLE001, S110 -- a notice may never cost the prune
        pass


def notice_old_snapshot_refs(cwd: str) -> bool:
    """Say once per repo per machine that old snapshot refs are still here, and
    again when there are more of them than last time. Never deletes (D10). True
    when the notice was shown.

    Written straight to stderr, not through ``warnings``: training scripts run
    with warnings ignored often enough (``PYTHONWARNINGS=ignore``,
    ``simplefilter("ignore")``) that a once-only warning could be marked shown
    and never seen. The marker is written only after the notice was.
    """
    try:
        common = _common_dir(cwd)
        if not common or common in _NOTICED:
            return False
        _NOTICED.add(common)
        refs = old_snapshot_refs(cwd)
        marker = _notice_marker(common)
        shown = _shown_count(marker)
        if shown is not None and len(refs) <= shown:
            if len(refs) < shown:
                _write_marker(marker, len(refs))  # so that growth from here is seen
            return False
        if not refs:
            return False
        print(
            f"probe: this repo still holds {len(refs)} old code-snapshot ref(s) "
            f"({SNAPSHOT_REFS_PREFIX}*) from earlier Probe versions. Each is a copy of "
            "the working tree at run start, untracked files included, and `git push "
            "--mirror` publishes them. Probe no longer writes them and never deletes "
            "them on its own: review with `probe snapshot-prune-refs --dry-run`, "
            "remove with `probe snapshot-prune-refs`. This notice is shown once "
            "(again only if more appear).",
            file=sys.stderr,
            flush=True,
        )
        _write_marker(marker, len(refs))
        return True
    except Exception:  # noqa: BLE001 -- a notice may never cost the capture
        return False


_SHA_RE = re.compile(r"[0-9a-f]{40,64}")
_CREDENTIAL_URI = re.compile(r"(?P<scheme>[A-Za-z][A-Za-z0-9+.-]*://)[^/@\s]+@")
# ssh scp-syntax: user@host:path -- strip the userinfo, keep host:path.
_SCP_USERINFO = re.compile(r"^[^/@\s]+@(?=[^/\s]+:)")


def _scrub_remote(url: str | None) -> str | None:
    """Drop credentials from a remote URL before it is recorded anywhere.

    Git remotes routinely carry tokens: GitHub Actions' ``persist-credentials``
    writes ``https://x-access-token:<TOKEN>@github.com/...`` and CI clones use
    ``https://oauth2:$TOKEN@...``. This value lands in run metadata and artifact
    meta, which are readable by anyone with access to the run, so an unscrubbed
    URL copies a live credential into durable storage.
    """
    if not url:
        return None
    scrubbed = _CREDENTIAL_URI.sub(r"\g<scheme><redacted>@", url)
    return _SCP_USERINFO.sub("<redacted>@", scrubbed)


def _remote_url(cwd: str, remote: str) -> str | None:
    return _scrub_remote(_git(cwd, "remote", "get-url", remote, check=False) or None)


def pushed_base(cwd: str) -> tuple[str | None, str | None]:
    """A commit that is an ancestor of HEAD *and* present on a remote.

    Returns ``(commit, scrubbed_remote_url)``, or ``(None, None)`` when nothing
    about the local history can be proven to exist anywhere else. HEAD itself is
    preferred; otherwise the NEWEST merge-base across all remote heads is used,
    so an unrelated stale branch cannot drag the base backwards.

    This is the check whose absence made every prior snapshot a dangling
    pointer. ``git remote -v`` printing a URL proves nothing -- commits can be
    local-only forever. Remote refs are read with ``ls-remote`` (authoritative,
    unlike a possibly-stale remote-tracking ref), and a remote head we do not
    have locally is treated as NOT pushed, so the failure mode is "upload the
    bytes", never "assume they are retrievable".

    The network call is bounded and non-interactive: an unreachable or
    credential-prompting remote must not hang the start of a training run.
    """
    remotes = [r for r in _git(cwd, "remote", check=False).splitlines() if r.strip()]
    if not remotes:
        return None, None
    remote = "origin" if "origin" in remotes else remotes[0]

    head = _git(cwd, "rev-parse", "HEAD", check=False)
    if not head:
        return None, None

    listing = _git(
        cwd, "ls-remote", "--heads", remote,
        check=False, timeout=_LS_REMOTE_TIMEOUT, env=_NONINTERACTIVE_ENV(),
    )
    if not listing:
        return None, None

    shas = []
    for line in listing.splitlines():
        sha = line.split("\t", 1)[0].strip()
        # Advertised object ids are hex; anything else (notably a leading '-')
        # would be parsed as a git option rather than a rev.
        if sha and _SHA_RE.fullmatch(sha):
            shas.append(sha)

    if not shas:
        return None, None

    # One `cat-file --batch-check` for every advertised SHA instead of one
    # `cat-file -e` process per branch. A remote head we do not have locally is
    # treated as NOT pushed, same rule as before. (~6000 branches would hit
    # ARG_MAX on the rev-list below; switch to `rev-list --stdin` if that
    # ever becomes real.)
    probe = subprocess.run(
        ["git", "cat-file", "--batch-check"],
        cwd=cwd, input="\n".join(shas) + "\n", env=_read_only(),
        capture_output=True, text=True,
    )
    present = []
    for line in probe.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "commit":
            present.append(parts[0])
    if not present:
        return None, None

    # `--boundary` computes the pushed frontier directly, which is merge-safe;
    # the old max-over-pairwise-merge-bases only approximated it. Boundary
    # lines are emitted newest-first, so the first is the newest pushed
    # ancestor. Empty output means HEAD is reachable from an advertised head.
    out = subprocess.run(
        ["git", "rev-list", "--boundary", "HEAD", "--not", *present],
        cwd=cwd, env=_read_only(), capture_output=True, text=True,
    )
    if out.returncode != 0:
        return None, None
    lines = [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]
    if not lines:
        return head, _remote_url(cwd, remote)
    boundary = [ln[1:] for ln in lines if ln.startswith("-")]
    if not boundary:
        return None, None
    return boundary[0], _remote_url(cwd, remote)


@lru_cache(maxsize=256)
def commit_on_remote(remote: str, commit: str, timeout: float = _VERIFY_TIMEOUT) -> bool:
    """Can this commit actually be fetched from this remote, right now?

    The question a recorded reference is making a claim about, and the one nothing
    asked for 19 runs. `ls-remote` cannot answer it: it lists ref tips, while a
    capture base is usually an ancestor of one. So ask the server for the object
    itself -- a depth-1 fetch of the bare SHA into a throwaway repo, which is
    exactly what a reproduction would do.

    False means "could not prove it", not "definitely gone": an unreachable host,
    a timeout, or a private repo we lack credentials for all land here. That is
    the safe direction -- the alternative is calling a run reproducible on a guess.

    MEMOIZED on (remote, commit), which is what makes a bulk audit affordable.
    Runs from one machine share a base commit, so auditing 200 runs is a handful
    of fetches, not 200. This is never called during a run -- only by an explicit
    `check(verify=True)` -- so it cannot slow training or artifact upload.
    """
    if not remote or not commit:
        return False
    with tempfile.TemporaryDirectory(prefix="probe-verify-") as tmp:
        _git(tmp, "init", "-q", ".", check=False, timeout=timeout)
        try:
            proc = subprocess.run(
                ["git", "fetch", "--depth", "1", "--quiet", remote, commit],
                cwd=tmp, capture_output=True, text=True,
                env=_NONINTERACTIVE_ENV(), timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return False
        return proc.returncode == 0


def _file_sha256(path: str) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


# Refuse rather than silently ship a partial archive. Raise it with
# `--max-upload-mb` when a repo genuinely needs to.
DEFAULT_MAX_UPLOAD_BYTES = 256 * 1024 * 1024

#: The largest file whose bytes a capture will upload: the credential gate's own
#: inspection limit (``secret_gate.ScanPolicy.max_bytes``, which is also the
#: server's upload ceiling). A file above it is not scanned, so its bytes never
#: leave; it is RECORDED instead (a file-path reference: path, host, sha256), the
#: same outcome as a file over ``reference_over_bytes``. Before this, such a file
#: was classified for upload and then refused by the transport or the server.
CONTENT_SCAN_MAX_BYTES = _secret_gate.ScanPolicy().max_bytes
#: Seconds ONE file may spend in the content scan, and seconds ONE snapshot may
#: spend scanning in total. The scanner reads text dense in its keywords at
#: ~4 MB/s -- an LLM training log printing `tokens/s` on every line is exactly
#: that, and 60 MB of it took 16-20 s at `probe.init()`. Capture stays broad (D7,
#: D12: every file up to 64 MiB); the budget is a safety stop, never a size rule.
#: A file whose scan runs past its budget, or a large (> FULL_SCAN_MAX_BYTES)
#: non-source file reached after the snapshot's budget is spent, is WITHHELD
#: with reason ``scan_budget``: recorded, never uploaded unscanned. Small files
#: and source files are always scanned, and the file budget holds for them too:
#: a big file's clock is read between chunks, a small file's between the
#: scanner's hits (``credential_rules``' ``deadline``; one regex pass cannot be
#: interrupted, so a small file can run a little past it). Override with the
#: env vars below; ``0`` removes a budget.
FILE_SCAN_BUDGET_SEC = 3.0
SNAPSHOT_SCAN_BUDGET_SEC = 15.0
FILE_SCAN_BUDGET_ENV = "PROBE_SNAPSHOT_FILE_SCAN_BUDGET_SEC"
SNAPSHOT_SCAN_BUDGET_ENV = "PROBE_SNAPSHOT_SCAN_BUDGET_SEC"
SCAN_BUDGET_REASON = "scan_budget"


def _budget_seconds(env: str, default: float) -> float:
    raw = os.environ.get(env, "").strip()
    try:
        value = float(raw) if raw else default
    except ValueError:
        return default
    if value != value or value < 0:  # NaN or negative: not a budget
        return default
    return float("inf") if value == 0 else value


#: Up to this size a file gets the scanner's full rule set WITH its decoding
#: layer -- base64, ``%xx`` and ``\\uXXXX`` escapes decoded and scanned again --
#: read next to each rule's keywords. Above it, the quick check (no decoding),
#: streamed in bounded chunks. Measured 2026-09-27 on 2,000 files / 35.7 MB of
#: this repo: quick 2.5 s, quick + decoding 4.0 s, un-windowed ``scan()`` 12.7 s,
#: ``secret_gate.inspect_bytes`` 31.7 s. Almost every file a repo holds is well
#: under 2 MiB, so almost every file gets the decoding pass.
FULL_SCAN_MAX_BYTES = 2 * 1024 * 1024

#: Chunks for the streamed quick scan of a big file, and how much of the previous
#: chunk each one re-reads: wider than the longest span a rule can match (a
#: private-key block, ~33K) plus a keyword's lead, so nothing is missed at a seam.
_SCAN_CHUNK = 1 << 20
_SCAN_OVERLAP = 40_000

#: A WITHHELD entry (a file left out for a credential) carries its sha256 only
#: from this size up. Below it the file is short enough that its hash could be
#: brute-forced back to a password offline, and the manifest is readable by the
#: whole team; path, mode and size still identify it.
WITHHELD_HASH_MIN_BYTES = 1024 * 1024

#: Source files, where `name = <expression>` is ordinary code. The scanner's
#: key-name tier (``anchored-secret``) exists for transcripts, where a false
#: positive costs a mangled string; here it costs the whole file. So in these
#: files that ONE rule's hit is dropped when its value is unquoted AND its first
#: word is code (see ``_code_shaped``) -- `token = tokens[0]`, `getpass.getpass()`,
#: `contextvars.Token` -- while `# api_key: a8f5...` in a comment still counts.
#: Notebooks are NOT here: `%env KEY=...` lines and printed outputs are data.
_SOURCE_SUFFIXES = (
    ".py", ".pyi", ".pyx", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx",
    ".go", ".rs", ".java", ".kt", ".scala", ".c", ".h", ".cc", ".cpp", ".cxx", ".hpp",
    ".cu", ".cuh", ".swift", ".rb", ".php", ".lua", ".jl", ".r", ".cs",
)
_KEY_NAME_RULE = "anchored-secret"
#: A field name that marks its value as a credential, matched anywhere in the
#: KEY of a `key = value` / `key: value` pair (camelCase included). The scanner
#: finds the hit; this decides whether the separator in front of it really
#: belongs to such a key, or to another one on the same line (`help=`, `noqa:`).
_ANCHOR_WORD = re.compile(
    r"(?i)secret|passw(?:or)?d|pwd|api[_ \-]?key|access[_ \-]?key|private[_ \-]?key"
    r"|token|credential|bearer|encryption[_ \-]?key|signing[_ \-]?key|(?-i:[A-Z0-9]_KEY)(?![A-Za-z0-9])"
    # The scanner's vendor-owned key names (`azure_openai_key`, `openaiKey`); it
    # has already checked that the name says who issued the key.
    r"|(?-i:[a-z0-9]_key|[A-Za-z0-9]Key)(?![A-Za-z0-9])"
)
#: `key` then `:`/`=` (and an opening quote) at the end of the text before a
#: value. A `<`, `>`, `!` or `=` in front of the `=` makes it a comparison.
_SEPARATOR_TAIL = re.compile(r"(?P<op>[<>!=]?)(?P<sep>[:=])\s*[\"']?\s*$")
_KEY_SPLIT = re.compile(r"[,;(){}\[\]\"'`#?&<>|]")
#: A value that is a template slot, not a value: `{user}` (f-string, JSX),
#: `${VAR}`, `$2::uuid` (SQL bind), `$db_password` (a lower-case variable, in
#: letters and `_` only, like the scanner's `_SLOT`), `%s`, `%(name)s`,
#: `<TOKEN>`, `***`, `...`.
_PLACEHOLDER = re.compile(
    r"\{[^{}]*\}|\$\{[^{}]*\}|\$\d+(?:::\w+)?|\$[A-Z_][A-Z0-9_]*|\$[a-z_][A-Za-z_]*|%s|%\(\w+\)s"
    r"|<[^<>]*>|\*{3,}|\.{3}|:[A-Za-z_]\w*"
)
#: The password part of `scheme://user:PASSWORD@` when it is a slot or a word
#: that names what goes there (`https://user:password@host` in a docstring).
_USERINFO_PLACEHOLDER = re.compile(
    r"(?i)" + _PLACEHOLDER.pattern + r"|pass(?:word)?|passwd|pwd|secret|token|changeme|example|x{3,}"
)
_CREDENTIAL_URI_PASSWORD = re.compile(r"://[^/@\s:]*:(?P<pw>[^/@\s]+)@")
_TYPE_NAMES = frozenset({
    "str", "int", "float", "bool", "bytes", "None", "Any", "Optional", "Union", "Final",
    "ClassVar", "SecretStr", "SecretBytes", "dict", "list", "tuple", "set", "Dict", "List",
    "Tuple", "Set", "Sequence", "Mapping", "object", "type", "Literal",
})
_NAME_ATTR = re.compile(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+(?:\(.*)?")
_CALL_OR_INDEX = re.compile(r"[A-Za-z_][\w.]*[(\[]")
_IDENTIFIER = re.compile(r"[A-Za-z_]\w*")
_HEXISH = re.compile(r"[0-9a-fA-F]{16,}")
#: ` = "literal"` (an assignment, spaced) or `default="literal"` on the rest of
#: a line -- not `==`, and not another keyword argument (`description="..."`).
_DEFAULT_LITERAL = re.compile(r"(?:(?<=\s)=(?!=)|\bdefault\s*=)\s*[rbuRBU]?([\"'])(?P<lit>[^\"'\n]+)\1")
_UTF16_BOMS = (b"\xff\xfe", b"\xfe\xff")
#: Punctuation that ends a value without being part of it (a closing quote or
#: bracket, a sentence's period). Not `=`: that is base64 padding.
_TRAILING = ".,;:)]}\"'`"
#: How far past (``_VERDICT_REACH``) and before (``_VERDICT_LOOKBACK``) one
#: key-name hit `_anchored_verdict` and the re-reads in `_counted_rules` look.
#: The scanner puts a key within 24 characters of its separator and a typed
#: field's literal within ~40 more, so these hold all a verdict reads. Reading
#: the whole line made a one-line file quadratic: a 150 KB minified JSON of
#: `"password": ...` rows took 17 s, a 1 MB line of `azure_openai_key=...`
#: 550 s. A line cut at the reach reads as going on; a key cut at the lookback
#: still ends in its anchor word.
_VERDICT_REACH = 1024
_VERDICT_LOOKBACK = 256
_FIRST_WORD = re.compile(r"\s*(\S*)")
_WORD_RUN = re.compile(r"\w+")


class _ScanOutOfTime(Exception):
    """A file's content scan ran past its time budget (see FILE_SCAN_BUDGET_SEC)."""


def _check_deadline(deadline: float | None) -> None:
    if deadline is not None and time.monotonic() > deadline:
        raise _ScanOutOfTime


def _is_placeholder(first: str) -> bool:
    """A template slot, with or without the punctuation that closes it
    (`{counter}`, `{counter}}`, `$2::uuid"`)."""
    for candidate in (first, first.rstrip(_TRAILING), first.rstrip(_TRAILING) + "}"):
        if _PLACEHOLDER.fullmatch(candidate.strip("\"'`")):
            return True
    return False


def _code_shaped(first: str, text: str, uses: Any = None) -> bool:
    """Whether the first word of an unquoted value is code, not a literal:
    `name.attr`, `name(`, `name[`, a type name, a lone `#` (a comment follows),
    or a plain identifier that is used elsewhere in the same file. Only the
    FIRST word counts -- the rest of the line (`(rotate monthly)`, `. Ask ops`)
    says nothing about the value -- and a trailing `=` is base64 padding.
    ``uses(word)`` counts a word's whole-word uses in ``text`` (`_counted_rules`
    counts every word once instead of searching the file once per hit)."""
    if first == "#":
        return True
    word = first.rstrip(_TRAILING)
    if not word:
        return True
    if word in _TYPE_NAMES or _NAME_ATTR.fullmatch(word) or _CALL_OR_INDEX.match(word):
        return True
    if _IDENTIFIER.fullmatch(word) and not _HEXISH.fullmatch(word):
        if uses is not None:
            return uses(word) >= 2
        return len(re.findall(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text)) >= 2
    return False


def _line_end(text: str, at: int) -> int:
    """The end of ``at``'s line, or ``at + _VERDICT_REACH`` if that comes first."""
    reach = min(len(text), at + _VERDICT_REACH)
    newline = text.find("\n", at, reach)
    return reach if newline < 0 else newline


def _anchored_verdict(text: str, f: Any, source: bool, uses: Any = None) -> tuple[bool, str | None]:
    """``(counts, key)`` for one key-name hit. ``key`` is set when the hit is
    dropped as CODE under a credential key, so the caller can look further along
    the line (a typed field: `password: str = "..."`). Reads `_VERDICT_LOOKBACK`
    before the hit and `_VERDICT_REACH` after it, never the whole line."""
    floor = max(0, f.start - _VERDICT_LOOKBACK)
    newline = text.rfind("\n", floor, f.start)
    line_start = floor if newline < 0 else newline + 1
    line_end = _line_end(text, f.start)
    before = text[line_start:f.start]
    if not before.strip() and (newline >= 0 or floor == 0):
        return False, None  # the value is on the NEXT line (YAML `token:` then a block)
    # The separator and what follows it end `before`: 64 characters hold them
    # (more whitespace than that and the hit counts, below).
    tail = _SEPARATOR_TAIL.search(before, max(0, len(before) - 64))
    if tail is None:
        return True, None  # cannot tell what it belongs to: count it
    if tail.group("op"):
        return False, None  # `<=`, `>=`, `!=`, `==`: a comparison
    key = _KEY_SPLIT.split(before[: tail.start()].rstrip(" \t\"'`]"))[-1].strip()
    if not _ANCHOR_WORD.search(key):
        # A `default=` belongs to whatever the line declares: an option
        # (`add_argument("--api-key", default=...)`), a lookup
        # (`os.getenv("WANDB_API_KEY", default=...)`) or a typed field
        # (`api_key: str = Field(default=...)`).
        if key.lower() != "default" or not _ANCHOR_WORD.search(before[: tail.start()]):
            return False, None  # the separator belongs to another key (`help=`, `noqa:`)
    first = _FIRST_WORD.match(text, f.start, line_end).group(1)
    if _is_placeholder(first):
        return False, None
    if f.start > 0 and text[f.start - 1] in "\"'":
        return True, None  # a quoted literal is never code
    if source and _code_shaped(first, text, uses):
        return False, key
    return True, None


def _vendor_rules(text: str) -> set[str]:
    """Every rule but the key-name one, over ``text`` with the decoding layer."""
    return {
        g.rule for g in _scan(text, _accel=_keyword_windows)
        if g.rule != _KEY_NAME_RULE and not _placeholder_uri(text, g)
    }


def _placeholder_uri(text: str, f: Any) -> bool:
    if f.rule != "credential-uri":
        return False
    m = _CREDENTIAL_URI_PASSWORD.search(text[f.start:f.end])
    return bool(m and _USERINFO_PLACEHOLDER.fullmatch(m.group("pw")))


def _counted_rules(text: str, findings: list, source: bool, deadline: float | None = None) -> set[str]:
    """The rules that keep a file out, after the false-positive rules below.

    - A `scheme://user:PASSWORD@` whose password is a slot (`{password}`,
      `<TOKEN>`, `$PW`) or a placeholder word is a template, not a credential.
    - A key-name hit counts unless: its value starts on the next line; its
      separator is a comparison or belongs to a non-credential key on the same
      line (`add_argument("--token", help=...)`, `# noqa:`); its value is a slot
      (`{counter}`, `$2::uuid`); or, in source files, the value's FIRST word is
      code (see ``_code_shaped``). A quoted literal always counts.
    - A dropped span is scanned again with the full rules and decoding, so a
      vendor token the scanner merged into it (it keeps one name for
      overlapping hits) still counts; and a dropped typed field
      (`password: str = "..."`, `password: str = field(default="...")`) is
      re-read as `key = "<the literal later on the line>"`.

    Each hit's work is bounded (`_VERDICT_REACH`), and past ``deadline`` (a
    `time.monotonic()` value) it raises `_ScanOutOfTime`.
    """
    rules: set[str] = set()
    counted: Counter[str] | None = None
    rescanned: dict[str, set[str]] = {}

    def uses(word: str) -> int:
        nonlocal counted
        if counted is None:
            # `(?<!\w)word(?!\w)` for an identifier `word` is exactly a whole
            # `\w+` run equal to it, so one count serves every hit.
            counted = Counter(_WORD_RUN.findall(text))
        return counted[word]

    for f in findings:
        _check_deadline(deadline)
        if _placeholder_uri(text, f):
            continue
        if f.rule != _KEY_NAME_RULE:
            rules.add(f.rule)
            continue
        counts, key = _anchored_verdict(text, f, source, uses)
        if counts:
            rules.add(f.rule)
            continue
        # The scanner's findings do not overlap, so a vendor token merged into
        # this one lies INSIDE its span: the span is what is read again, once
        # per distinct span (a generated file repeats `token = tokens[0]`).
        span = text[f.start:f.end]
        if span not in rescanned:
            rescanned[span] = _vendor_rules(span)
        rules |= rescanned[span]
        if key:
            # From the VALUE's start: the password rule's span can swallow the
            # `=` (`password: str = "..."` -> `str =`).
            line_end = _line_end(text, f.start)
            quoted = text.find('"', f.start, line_end) >= 0 or text.find("'", f.start, line_end) >= 0
            default = _DEFAULT_LITERAL.search(text, f.start, line_end) if quoted else None
            if default:
                synthetic = f'{key} = "{default.group("lit")}"'
                rules |= {g.rule for g in _scan(synthetic) if not _placeholder_uri(synthetic, g)}
    return rules


def _utf16_codec(raw: bytes | bytearray) -> str | None:
    """``utf-16-le``/``utf-16-be`` when the bytes read as UTF-16 -- a byte-order
    mark, or (no mark, Windows tools often omit it) NUL in most odd or even
    positions of the first 4 KB -- else None."""
    if raw[:2] == b"\xff\xfe":
        return "utf-16-le"
    if raw[:2] == b"\xfe\xff":
        return "utf-16-be"
    head = bytes(raw[:4096])
    if len(head) < 8:
        return None
    even, odd = head[0::2], head[1::2]
    if odd.count(0) >= 0.7 * len(odd) and even.count(0) <= 0.1 * len(even):
        return "utf-16-le"
    if even.count(0) >= 0.7 * len(even) and odd.count(0) <= 0.1 * len(odd):
        return "utf-16-be"
    return None


def _text_views(raw: bytes | bytearray, codec: str | None = None) -> list[tuple[str, bool]]:
    """``[(text, is_text), ...]`` to scan. UTF-8 is read as UTF-8. UTF-16 (a
    byte-order mark, or NUL-interleaved without one) is read as UTF-16, beside
    a latin-1 view in case a binary file only looked like it. Anything else goes
    through the latin-1 view -- one character per byte -- so a plainly written
    token inside a pickle or a stored zip member is still seen."""
    codec = codec or _utf16_codec(raw)
    if codec:
        body = raw[2:] if raw[:2] in _UTF16_BOMS else raw
        return [(bytes(body).decode(codec, "replace"), True), (raw.decode("latin-1"), False)]
    try:
        return [(raw.decode("utf-8"), True)]
    except UnicodeDecodeError:
        return [(raw.decode("latin-1"), False)]


#: Notebooks up to this size are also read as their CODE (`_notebook_rules`).
#: The JSON of an `.ipynb` escapes every `"` inside a cell
#: (`OPENAI_API_KEY = \"...\"`), which hides a quoted literal from every rule
#: that reads quotes. Outputs (plots as base64) are what make a notebook big,
#: and parsing holds a few times the file, so there is a ceiling.
NOTEBOOK_DECODE_MAX_BYTES = 16 * 1024 * 1024


def _notebook_code(raw: bytes | bytearray) -> str | None:
    """The source of a notebook's code cells, JSON-decoded, one cell after
    another; None when ``raw`` is not a notebook with code in it. nbformat 4
    (`cells`, `source`) and 3 (`worksheets`, `input`)."""
    try:
        notebook = json.loads(bytes(raw))
    except (ValueError, RecursionError):  # not JSON (UnicodeDecodeError is a ValueError)
        return None
    if not isinstance(notebook, dict):
        return None
    cells = notebook.get("cells")
    if not isinstance(cells, list):
        sheets = notebook.get("worksheets")
        cells = [
            cell for sheet in sheets if isinstance(sheet, dict) and isinstance(sheet.get("cells"), list)
            for cell in sheet["cells"]
        ] if isinstance(sheets, list) else []
    parts: list[str] = []
    for cell in cells:
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue
        source = cell.get("source", cell.get("input"))
        if isinstance(source, list):
            source = "".join(line for line in source if isinstance(line, str))
        if isinstance(source, str) and source.strip():
            parts.append(source)
    return "\n\n".join(parts) or None


def _notebook_rules(raw: bytes | bytearray, deadline: float | None = None) -> set[str]:
    """Rules found in a notebook's code cells, read as Python source (the
    verdict the same code gets in a `.py` file). The raw JSON is scanned as
    well, by the caller: outputs and `%env` lines are read there."""
    code = _notebook_code(raw)
    if code is None:
        return set()
    findings = _scan(code, _accel=_keyword_windows)
    _check_deadline(deadline)
    return _counted_rules(code, findings, True, deadline)


def credential_rules(
    raw: bytes | bytearray, name: str, *, deadline: float | None = None
) -> tuple[str, ...]:
    """Rule names (never a matched value) of the credentials in ``raw``; empty
    when it looks clean. ``name`` is the file's basename. Past ``deadline`` (a
    `time.monotonic()` value, checked between hits) it raises
    `_ScanOutOfTime`, and the caller withholds the file.

    The scanner is the shared one (``tap_core.secrets``): its full rule set with
    the decoding layer up to FULL_SCAN_MAX_BYTES, the quick check above that,
    then the false-positive rules in ``_counted_rules``. NOT a backstop: the
    server's upload relay inspects every object it stores and records what it
    finds (``artifacts.credential_findings``), but it stores the bytes
    regardless -- so what this check misses IS stored. Known misses: a token
    split across strings or lines; a bare credential with no recognizable shape
    or key name; decoding (base64, escapes) above FULL_SCAN_MAX_BYTES; and the
    scanner residuals listed in agent/TODOS.md (all-letter values under camelCase
    keys, owner-less `*_key` names, URL passwords with `/`). Compressed archives
    are opened separately (``_archive_rules``); a notebook's code cells are read
    again, JSON-decoded, as Python source (``_notebook_rules``).

    A scanner failure is a finding: a file that could not be checked does not
    ship.
    """
    lowered = name.lower()
    code = lowered.endswith(_SOURCE_SUFFIXES)
    rules: set[str] = set()
    try:
        for text, is_text in _text_views(raw):
            if len(raw) <= FULL_SCAN_MAX_BYTES:
                findings = _scan(text, _accel=_keyword_windows)
            else:
                findings = _scan_quick(text)
            _check_deadline(deadline)
            rules |= _counted_rules(text, findings, is_text and code, deadline)
        if lowered.endswith(".ipynb") and len(raw) <= NOTEBOOK_DECODE_MAX_BYTES:
            rules |= _notebook_rules(raw, deadline)
    except _ScanOutOfTime:
        raise
    except Exception:  # noqa: BLE001 -- fail closed: unscanned bytes stay home
        return ("inspection-failed",)
    return tuple(sorted(rules))


def _chunk_rules(chunk: bytes | bytearray, name: str, codec: str | None = None) -> set[str]:
    """One window of a big file: the quick check over a latin-1 view (length-
    preserving, so lowering it is cheap; every rule's shape is ASCII), plus a
    UTF-16 view when the file is UTF-16 (windows stay on even byte offsets)."""
    code = name.lower().endswith(_SOURCE_SUFFIXES)
    views = [(chunk.decode("latin-1"), code)]
    if codec:
        views.insert(0, (bytes(chunk).decode(codec, "replace"), code))
    rules: set[str] = set()
    try:
        for text, source in views:
            rules |= _counted_rules(text, _scan_quick(text), source)
    except Exception:  # noqa: BLE001 -- fail closed
        return {"inspection-failed"}
    return rules


#: Decompressed bytes one archive may yield to the scan; past it the archive is
#: withheld for the scan budget (a small gzip can expand to gigabytes).
ARCHIVE_EXPAND_MAX_BYTES = 256 * 1024 * 1024
_UNREADABLE_ARCHIVE = "unreadable-archive"
_NAME_IN_ARCHIVE = "credential-name-in-archive"


def _compressed_kind(head: bytes) -> str | None:
    """The compression wrapping a file, from its first bytes: its CONTENT is not
    in its raw bytes, so the raw scan cannot see it. A zip is listed here too;
    ``_archive_rules`` only opens its compressed members (a stored member -- a
    torch checkpoint, say -- is already plain in the raw bytes)."""
    if head[:2] == b"\x1f\x8b":
        return "gzip"
    if head[:3] == b"BZh":
        return "bz2"
    if head[:6] == b"\xfd7zXZ\x00":
        return "xz"
    if head[:4] in (b"PK\x03\x04", b"PK\x05\x06"):
        return "zip"
    return None


def _archive_streams(path: str, kind: str):
    """``(member name, readable)`` pairs to scan: the members of a compressed
    tar (their names checked too), the compressed members of a zip, or the one
    decompressed stream of a plain `.gz`/`.bz2`/`.xz`. One level deep."""
    import bz2
    import gzip
    import lzma
    import tarfile
    import zipfile

    if kind == "zip":
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.compress_type == zipfile.ZIP_STORED:
                    continue
                with zf.open(info) as member:
                    yield info.filename, member
        return
    opener = {"gzip": gzip.open, "bz2": bz2.open, "xz": lzma.open}[kind]
    tar_mode = {"gzip": "r|gz", "bz2": "r|bz2", "xz": "r|xz"}[kind]
    try:
        tar = tarfile.open(path, mode=tar_mode)
    except tarfile.ReadError:
        tar = None
    if tar is not None:
        with tar:
            for info in tar:
                if not info.isfile():
                    continue
                member = tar.extractfile(info)
                if member is not None:
                    yield info.name, member
        return
    with opener(path, "rb") as stream:
        yield os.path.basename(path).rsplit(".", 1)[0], stream


def _archive_rules(
    path: str, kind: str, allowed: float, spent: float
) -> tuple[set[str], float, bool]:
    """``(rules, seconds spent in total, out of budget)`` for what a compressed
    archive holds: each member's NAME against the credential-name rules and its
    decompressed bytes through the same chunked scan as a big file, under the
    same time budget. An archive that cannot be opened (corrupt, encrypted) is a
    finding: its bytes are not uploaded unread."""
    rules: set[str] = set()
    expanded = 0
    try:
        for member_name, stream in _archive_streams(path, kind):
            base = member_name.rsplit("/", 1)[-1]
            if _skip_reason(base) == "secret" or _in_secret_dir(member_name):
                rules.add(_NAME_IN_ARCHIVE)
            carry = b""
            codec: str | None = None
            while True:
                chunk = stream.read(_SCAN_CHUNK)
                if not chunk:
                    break
                if not carry:
                    codec = _utf16_codec(chunk)
                expanded += len(chunk)
                if expanded > ARCHIVE_EXPAND_MAX_BYTES:
                    return rules, spent, True
                window = carry + chunk
                started = time.monotonic()
                rules |= _chunk_rules(window, base, codec)
                spent += time.monotonic() - started
                carry = window[-_SCAN_OVERLAP:]
                if spent >= allowed:
                    return rules, spent, True
    except Exception:  # noqa: BLE001 -- corrupt, truncated, encrypted: not readable
        rules.add(_UNREADABLE_ARCHIVE)
    return rules, spent, False


def _read_for_capture(
    path: str,
    name: str,
    *,
    scan: bool,
    limit: int,
    file_budget: float = float("inf"),
    total_left: float = float("inf"),
) -> tuple[str, int, tuple[str, ...], float, bool]:
    """``(sha256, size, credential rules, seconds scanning, budget ran out)`` from
    ONE read, so what is scanned is exactly what was hashed. Nothing past
    ``limit`` is scanned (the file is then too large to upload at all). A file up
    to FULL_SCAN_MAX_BYTES is scanned whole; a bigger one in overlapping chunks,
    so memory stays at a few MB whatever its size (a 60 MB keyword-dense log held
    ~530 MB before), UTF-16 included (the codec is read from the first chunk and
    windows stay on even offsets). The time budgets are checked between chunks:
    past ``file_budget`` seconds on this file -- or, for a non-source file, past
    what is ``total_left`` of the snapshot's budget -- the scan stops, hashing
    goes on, and the caller withholds the file. A whole-scanned file gets
    ``file_budget`` too, as ``credential_rules``' deadline. A compressed archive
    is then opened and its members scanned too (``_archive_rules``), and a
    notebook too big to scan whole has its code cells read up to
    NOTEBOOK_DECODE_MAX_BYTES (``_notebook_rules``)."""
    h = hashlib.sha256()
    rules: set[str] = set()
    n = 0
    spent = 0.0
    out_of_budget = False
    source = name.lower().endswith(_SOURCE_SUFFIXES)
    allowed = file_budget if source else min(file_budget, total_left)
    head = b""
    codec: str | None = None
    with open(path, "rb") as fh:
        size = os.fstat(fh.fileno()).st_size
        whole = scan and size <= FULL_SCAN_MAX_BYTES
        if scan and not whole and allowed <= 0:
            out_of_budget = True  # the snapshot's budget is spent: do not start
        small: bytearray | None = bytearray() if whole else None
        notebook: bytearray | None = (
            bytearray()
            if scan and not whole and size <= NOTEBOOK_DECODE_MAX_BYTES and name.lower().endswith(".ipynb")
            else None
        )
        carry = b""
        for chunk in iter(lambda: fh.read(_SCAN_CHUNK), b""):
            h.update(chunk)
            if n == 0:
                head = chunk[:4096]
                codec = _utf16_codec(head)
            n += len(chunk)
            if not scan or n > limit or out_of_budget:
                small = notebook = None
                continue
            if notebook is not None:
                notebook.extend(chunk)
                if len(notebook) > NOTEBOOK_DECODE_MAX_BYTES:
                    notebook = None  # grew while being read: the raw scan still covers it
            if small is not None:
                small.extend(chunk)
                if len(small) <= FULL_SCAN_MAX_BYTES:
                    continue
                # Grew past the full-scan size while being read: stream the rest.
                window, small = small, None
            else:
                window = carry + chunk
            started = time.monotonic()
            rules |= _chunk_rules(window, name, codec)
            spent += time.monotonic() - started
            carry = bytes(window[-_SCAN_OVERLAP:])
            if spent >= allowed:
                out_of_budget = True
    if small is not None and n <= limit and not out_of_budget:
        started = time.monotonic()
        try:
            rules |= set(credential_rules(small, name, deadline=started + file_budget))
        except _ScanOutOfTime:
            out_of_budget = True
        spent += time.monotonic() - started
    if notebook is not None and n <= limit and not out_of_budget:
        started = time.monotonic()
        try:
            rules |= _notebook_rules(notebook, deadline=started + max(0.0, allowed - spent))
        except _ScanOutOfTime:
            out_of_budget = True
        except Exception:  # noqa: BLE001 -- fail closed, as credential_rules does
            rules.add("inspection-failed")
        spent += time.monotonic() - started
    kind = _compressed_kind(head) if scan and n <= limit and not out_of_budget else None
    if kind is not None:
        archive_rules, spent, out_of_budget = _archive_rules(path, kind, allowed, spent)
        rules |= archive_rules
    return h.hexdigest(), n, tuple(sorted(rules)), spent, out_of_budget and n <= limit


class _ContentGate:
    """What every captured file passes before it can be classified for upload.

    A snapshot stores EXACT bytes (restore verifies each sha256), so unlike
    ``log_artifact`` it cannot redact: a file with a credential is WITHHELD. It
    stays in the manifest as ``source: "withheld"`` with its size and reason (and
    its sha256 only from WITHHELD_HASH_MIN_BYTES up), so the tree's identity does
    not depend on whether a scan ran, and it is REPORTED in ``skipped`` (reason
    ``secret``, ``found_in: content``, the rule names). Live, before this
    existed: an untracked `.env` and a scratch file with a `probe_pat_` token
    were stored byte-identical from a git repo.

    Every upload path re-verifies the recorded sha256 on the descriptor it
    streams and pins it on the PUT, so nothing can change between this check
    and storage.

    ``scan`` switches the check. ``budget`` bounds it: the bytes that could be
    uploaded (``max_upload_bytes``); past it the capture would be refused as too
    large anyway, so it is refused HERE, before paying to scan what cannot ship.
    ``budget=None`` scans without a bound (a capture that will not upload).

    Time is bounded too (FILE_SCAN_BUDGET_SEC for every file,
    SNAPSHOT_SCAN_BUDGET_SEC for large non-source ones): a file the scan could
    not finish in time is withheld with reason ``scan_budget``, because
    unscanned bytes are never uploaded, and the run warns about it.
    """

    def __init__(self, *, scan: bool = True, budget: int | None = None) -> None:
        self.scan = scan
        self.budget = budget
        self.scanned = 0
        self.skipped: list[dict[str, Any]] = []
        self.file_budget = _budget_seconds(FILE_SCAN_BUDGET_ENV, FILE_SCAN_BUDGET_SEC)
        self.total_budget = _budget_seconds(SNAPSHOT_SCAN_BUDGET_ENV, SNAPSHOT_SCAN_BUDGET_SEC)
        self.seconds = 0.0

    def entry(
        self,
        full: str,
        rel: str,
        *,
        reference_over_bytes: int,
        tracked: bool = False,
        **extra: Any,
    ) -> dict[str, Any]:
        """The manifest entry for one regular file: ``blob``, ``reference``, or
        ``withheld`` when its content holds a credential (reason ``secret``) or
        its scan ran out of time (reason ``scan_budget``).

        The size limit does not depend on ``scan``: which files are copied, and so
        the tree's identity, must not change with whether a scan ran."""
        limit = min(reference_over_bytes, CONTENT_SCAN_MAX_BYTES)
        if self.scan and self.budget is not None:
            try:
                expected = os.path.getsize(full)
            except OSError:
                expected = 0
            if expected <= limit:
                self.scanned += expected
                if self.scanned > self.budget:
                    raise SnapshotTooLarge(
                        f"more than {self.budget / 1e6:.0f} MB of files would be uploaded, "
                        "over the cap; raise --max-upload-mb, or lower --reference-over-mb so "
                        "the large files are recorded where they live instead of copied"
                    )
        sha, size, rules, seconds, out_of_time = _read_for_capture(
            full,
            os.path.basename(rel),
            scan=self.scan,
            limit=limit,
            file_budget=self.file_budget,
            total_left=self.total_budget - self.seconds,
        )
        self.seconds += seconds
        mode = "100755" if os.access(full, os.X_OK) else "100644"
        entry: dict[str, Any] = {"path": rel, "mode": mode, "sha256": sha, "size": size, **extra}
        _classify_by_size(entry, full, reference_over_bytes=limit)
        if entry["source"] != "blob" or not (rules or out_of_time):
            return entry
        # A finding decides; a scan cut short by the clock only when none was found.
        if not rules:
            reason = SCAN_BUDGET_REASON
        elif set(rules) <= {"inspection-failed", _UNREADABLE_ARCHIVE}:
            reason = "uninspectable"
        else:
            reason = "secret"
        self.skipped.append(
            {
                "path": rel,
                "reason": reason,
                "found_in": "content" if rules else "scan_time",
                **({"rules": list(rules)} if rules else {"seconds": round(seconds, 2)}),
                **({"tracked": True} if tracked else {}),
            }
        )
        withheld: dict[str, Any] = {
            "path": rel, "mode": mode, "size": size, "source": "withheld", "reason": reason, **extra,
        }
        if size >= WITHHELD_HASH_MIN_BYTES:
            withheld["sha256"] = sha
        return withheld


def _entry_identity(e: dict[str, Any]) -> str:
    """One manifest entry's line in ``tree_sha256``. A withheld entry with no
    sha256 contributes its size instead, so two trees differing only in a
    withheld file of a different size still differ."""
    sha = e.get("sha256")
    if sha is None and e.get("source") == "withheld":
        sha = f"withheld:{e.get('size')}"
    return f"{e['path']}\0{e['mode']}\0{sha}\n"


def tree_digest(entries: list[dict[str, Any]]) -> str:
    """``tree_sha256`` over ``(path, mode, sha256)`` in path order."""
    digest = hashlib.sha256()
    for e in sorted(entries, key=lambda e: e["path"]):
        digest.update(_entry_identity(e).encode())
    return digest.hexdigest()


#: Above this, an included file is RECORDED rather than uploaded. A base
#: checkpoint or a dataset shard is an input whose identity matters and whose
#: bytes are already sitting on a shared volume; copying tens of GB per run to
#: re-store what is already there is not reproducibility, it is duplication.
DEFAULT_REFERENCE_OVER_BYTES = 100 * 1024 * 1024

#: File ceiling for a NON-GIT capture. Git bounds its own walk by what is
#: tracked; a bare directory has nothing to bound it, so the walk is whatever
#: happens to sit under the cwd -- and `probe run start` runs in whatever
#: directory a person's shell is parked in.
#:
#: Measured 2026-08-10 in ~/Documents/GitHub (a directory of ~245 checkouts):
#: 276,507 entries, 54.6s of walking and sha256, every one classified pending
#: upload -- and then a 256MB upload cap to fail against at the END. The run
#: itself was created in well under a second; the whole stall was this.
#:
#: A ceiling, not a truncation: a manifest missing files it never mentions is
#: the thing `skipped` exists to prevent, and half a tree reproduces nothing.
#: Overflow raises SnapshotTooLarge, which the auto-snapshot hook turns into a
#: warning -- capture is never a gate (maintainer decision 2026-08-06), so the
#: run survives uncaptured rather than the command hanging.
#:
#: 20k is well above a real project (this repo is ~1.5k files) and well below
#: a directory that is really somebody's whole workspace.
DEFAULT_MAX_DIRECTORY_ENTRIES = 20_000


def _classify_by_size(
    entry: dict[str, Any], full: str, *, reference_over_bytes: int
) -> dict[str, Any]:
    """Set ``source`` from size alone: copy the bytes, or record where they live.

    ``source="blob"``      small enough to store; uploaded as a capture row (or into
                           the code-bytes archive under PROBE_CODE_STORAGE=archive).
    ``source="reference"`` too large to copy per run; the path, host and sha256
                           are recorded so the file is identified and verifiable,
                           and restore reports where it lives instead of
                           pretending it can rebuild it.

    Size is the ONLY input, deliberately. Whether git could supply a file used to
    be asked first and decided the bytes: a tracked file byte-identical to a
    pushed commit was recorded as a git reference and never uploaded. That
    reference resolves only while the commit does -- reachable from the machine
    doing the rebuild, on a remote that still has it, in a repo that was not
    force-pushed or deleted -- and a dead one is indistinguishable from a live
    one until somebody tries to rebuild. `Client.check_run` had to grow a
    network probe (`unresolvable_code_reference`) purely to tell them apart.

    Code is small and copying it is cheap, so code is copied. What stays a
    reference is what genuinely cannot be: the 40GB checkpoint above the
    threshold, which is a file-path reference (path/host/sha256) and never a git
    one.
    """
    if entry["size"] > reference_over_bytes:
        entry["source"] = "reference"
        entry["uri"] = local_file_uri(os.path.abspath(full))
        entry["host"] = socket.gethostname()
    else:
        entry["source"] = "blob"
    return entry


#: How many ``probeignore`` records one manifest lists (the first, by path);
#: ``n_probeignore`` counts them all. `*.jsonl` over a results tree matched
#: 6,667 files, 450 KB of one artifact row's meta.
PROBEIGNORE_REPORT_LIMIT = 50


class _Ignored:
    """Paths a ``.probeignore`` pattern excluded (plan (n)), reported under
    reason ``probeignore``: an excluded directory once (the top-most one), not
    once per file under it, and at most ``PROBEIGNORE_REPORT_LIMIT`` records,
    with the exact count in ``count``.

    Applied AFTER the safety stops: a credential is reported as one whatever
    the patterns say, and nothing here can re-include a path.
    """

    def __init__(self, rules: _ignore.IgnoreRules | None, cwd: str) -> None:
        self.rules = rules
        self.cwd = cwd
        self.records: dict[str, dict[str, Any]] = {}
        self._dirs: dict[str, bool] = {}
        self.count = 0

    def _dir(self, rel_dir: str) -> bool:
        hit = self._dirs.get(rel_dir)
        if hit is None:
            hit = self._dirs[rel_dir] = bool(
                self.rules
                and self.rules.ignored(rel_dir, base=self.cwd, is_dir=True, capture_root=self.cwd)
            )
        return hit

    def directory(self, rel_dir: str) -> bool:
        """For a walk that prunes: is this directory excluded (recorded if so)?"""
        if self.rules is None or not self._dir(rel_dir):
            return False
        self.records.setdefault(rel_dir, {"path": rel_dir, "reason": _ignore.REASON})
        return True

    def path(self, rel: str) -> bool:
        """Is this file excluded, by itself or by an excluded parent directory?"""
        if self.rules is None:
            return False
        parts = rel.split("/")
        for depth in range(1, len(parts)):
            parent = "/".join(parts[:depth])
            if self._dir(parent):
                self.records.setdefault(parent, {"path": parent, "reason": _ignore.REASON})
                return True
        if self.rules.ignored(rel, base=self.cwd, capture_root=self.cwd):
            self.records.setdefault(rel, {"path": rel, "reason": _ignore.REASON})
            return True
        return False

    def report(self, entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """The first ``PROBEIGNORE_REPORT_LIMIT`` records, minus any file an
        explicit ``include=`` captured anyway; ``count`` is set to all of them."""
        captured = {e["path"] for e in entries}
        records = [r for path, r in sorted(self.records.items()) if path not in captured]
        self.count = len(records)
        return records[:PROBEIGNORE_REPORT_LIMIT]


def _include_entries(
    cwd: str,
    include: list[str],
    already: set[str],
    *,
    reference_over_bytes: int,
    gate: _ContentGate,
    skipped: list[dict[str, Any]],
    own: _owndirs.Within | None = None,
) -> list[dict[str, Any]]:
    """Manifest entries for explicitly named paths git would not offer.

    ``.gitignore`` is right about build output and wrong about a downloaded
    dataset, a base checkpoint, or a config deliberately kept out of the repo.
    Those are INPUTS, and the manifest had no way to name them -- so they were
    recorded nowhere, not even as a hash.

    Two outcomes, decided by size:

    ``source="blob"``      small enough to store; uploaded as a capture row (or into
                           the code-bytes archive under PROBE_CODE_STORAGE=archive).
    ``source="reference"`` too large; the path, host and sha256 are recorded so the
                           file is identified and verifiable, and restore reports
                           where it lives instead of pretending it can rebuild it.

    Deliberately NOT recursive by default: a glob names what it names. Passing a
    directory captures it whole, which is the caller's explicit choice.

    Naming a path does not waive the credential stops: a credential-shaped name
    is skipped and a file whose content holds a credential goes through ``gate``,
    both reported in ``skipped`` -- a directory include sweeps up whatever sits
    in it, and nothing about naming a folder says "upload the key in it". The
    same goes for the SDK's own folders (``own``, `probe.sdk.owndirs`): its
    queue is never the run's code, reported once per folder.
    """
    import glob as _glob

    own_reported = {s["path"] for s in skipped if s.get("reason") == _owndirs.REASON}

    found: list[dict[str, Any]] = []
    seen: set[str] = set()
    root_real = os.path.realpath(cwd)
    for pattern in include:
        matches = _glob.glob(os.path.join(cwd, pattern), recursive=True)
        if not matches:
            raise SnapshotError(f"--include {pattern!r} matched no files under {cwd}")
        for match in sorted(matches):
            targets = [match]
            if os.path.isdir(match):
                targets = sorted(
                    os.path.join(root, name)
                    for root, dirs, files in os.walk(match)
                    for name in files
                    # Credential folders are NOT pruned here: they are reported
                    # file by file below, never dropped in silence.
                    if not any(part in SKIP_GENERATED_DIRS for part in root.split(os.sep))
                )
            for full in targets:
                rel = _posix(os.path.relpath(full, cwd))
                if rel.startswith("..") or os.path.isabs(rel):
                    raise SnapshotError(f"--include {pattern!r} escapes {cwd}: {rel}")
                if rel in already or rel in seen:
                    continue
                top = own.top(rel) if own is not None else None
                if top is not None:
                    if top not in own_reported:
                        own_reported.add(top)
                        skipped.append({"path": top, "reason": _owndirs.REASON})
                    continue
                if os.path.islink(full):
                    # Recorded as the link it is, never read through: `include=
                    # ["key.txt"]` where key.txt points at ~/.wandb must not
                    # upload the key. Restore rebuilds the link from its target.
                    seen.add(rel)
                    target = os.readlink(full)
                    found.append({
                        "path": rel, "mode": "120000",
                        "sha256": hashlib.sha256(target.encode()).hexdigest(),
                        "size": len(target.encode()), "source": "blob",
                        "symlink_target": target, "included": True,
                    })
                    continue
                if not os.path.isfile(full):
                    continue
                seen.add(rel)
                real = os.path.realpath(full)
                if real != root_real and not real.startswith(root_real + os.sep):
                    # Inside by its PATH, outside by where it lives: a folder
                    # symlinked into the project (`ext -> ~/.config`).
                    skipped.append({"path": rel, "reason": "outside_tree"})
                    continue
                reason = "secret" if _in_secret_dir(rel) else _skip_reason(os.path.basename(full))
                if reason is not None:
                    skipped.append({"path": rel, "reason": reason})
                    continue
                found.append(
                    gate.entry(full, rel, reference_over_bytes=reference_over_bytes, included=True)
                )
    return found


#: Root-level dependency descriptors captured as FILES, not just as the
#: enumerated interpreter packages — the lockfile is what a rebuild consumes,
#: and a dirty/gitignored one was previously lost with no record.
LOCKFILE_NAMES = (
    "uv.lock", "poetry.lock", "pyproject.toml", "environment.yml",
    "package-lock.json", "Cargo.lock",
)
DEFAULT_MAX_LOCKFILE_BYTES = 1024 * 1024


def _is_lockfile(name: str) -> bool:
    return name in LOCKFILE_NAMES or fnmatch.fnmatch(name, "requirements*.txt")


# Directories that are rebuilt from a lockfile or a cache, never authored. Left
# in, the first snapshot of an ordinary Python project uploads a few hundred MB
# of `.venv` and calls it the experiment's code.
SKIP_GENERATED_DIRS = frozenset({
    ".git", ".hg", ".svn",
    ".venv", "venv", "env", "virtualenv",
    "node_modules", "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".ipynb_checkpoints", ".tox", ".eggs", "site-packages",
})
#: Credential directories. An agent told to "keep the keys somewhere safe" makes
#: one of these; a snapshot must not then ship it. Applied to EVERY path
#: component, on every path: the git listing, the directory walk and `include=`
#: matches (the git path used to skip them only in the non-git walk, so an
#: untracked `.secrets/wandb` inside a repo went up).
SKIP_SECRET_DIRS = frozenset({".secrets", "secrets", ".aws", ".gnupg", ".ssh", ".docker"})
#: Every directory a walk prunes (`inputs` and `outputs` read this union).
SKIP_DIRS = SKIP_GENERATED_DIRS | SKIP_SECRET_DIRS

# Secret-shaped names. A directory walk with no `.gitignore` to honour would
# otherwise ship credentials off the machine as a side effect of tracking an
# experiment -- the exact hazard the git path avoids for free. Excluded by
# default and REPORTED, so a caller who genuinely needs one knows it is absent.
#
# Matched on the STEM, not by equality. The list used to be exact-match, and it
# read as complete while missing the file that actually leaked: an agent wrote
# `/workspace/<user>/.secrets/aws_credentials` (Anthrogen, 2026-08-30), which
# is not `credentials` and so was not skipped. `foo_credentials`,
# `credentials.bak` and `prod-secrets.json` all had the same hole.
SKIP_SECRETS = (
    ".env", ".env.local", ".envrc", ".netrc", "netrc", "_netrc", ".npmrc", ".pypirc",
    ".pgpass", "pgpass.conf", ".dockercfg", ".git-credentials",
    "credentials", "credentials.json", "secrets.json", "service-account.json",
)
#: Stems that make a filename credential-shaped wherever they appear in it.
SKIP_SECRET_STEMS = ("credentials", "secrets", "secret_key", "id_rsa", "id_ed25519", "id_ecdsa")
SKIP_SECRET_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".keystore", ".jks", ".ovpn", ".env")
SKIP_SECRET_PREFIXES = ("id_rsa", "id_ed25519", "id_ecdsa", ".env.", ".env-")
SKIP_FILE_SUFFIXES = (".pyc", ".pyo", ".so", ".o", ".DS_Store")
#: A committed template of a credential file (`.env.example`) is documentation,
#: not a credential; its CONTENT is still scanned like any file's.
TEMPLATE_SUFFIXES = (".example", ".sample", ".template", ".tmpl", ".dist")


def _secret_name(name: str, *, stems: bool) -> bool:
    lowered = name.lower()
    if lowered.endswith(TEMPLATE_SUFFIXES):
        return False
    if name in SKIP_SECRETS or lowered.startswith(SKIP_SECRET_PREFIXES):
        return True
    if lowered.endswith(SKIP_SECRET_SUFFIXES):
        return True
    return stems and any(stem in lowered for stem in SKIP_SECRET_STEMS)


def _skip_reason(name: str) -> str | None:
    """Why a file NAME keeps an untracked or walked file out of a capture
    (every rule: exact names, prefixes, suffixes, stems, generated), or None.
    Also the rule `inputs` and `outputs` apply."""
    if _secret_name(name, stems=True):
        return "secret"
    if name.lower().endswith(SKIP_FILE_SUFFIXES) or name == ".DS_Store":
        return "generated"
    return None


def _tracked_skip_reason(name: str) -> str | None:
    """The name rule for a file git TRACKS: only the exact names, prefixes and
    suffixes. A committed file is the project's own, and the stem rule would
    drop code (`tap_core/secrets.py`, `sync-secrets.sh`) and the generated rule
    a committed native library -- both break a restore. Its content is scanned
    like any file's, and every tracked skip is announced."""
    return "secret" if _secret_name(name, stems=False) else None


def _in_secret_dir(rel: str) -> bool:
    """Whether any directory component of a manifest path is a credential folder."""
    return any(part in SKIP_SECRET_DIRS for part in rel.split("/")[:-1])


def capture_directory_manifest(
    cwd: str | None = None,
    *,
    include: list[str] | None = None,
    reference_over_bytes: int = DEFAULT_REFERENCE_OVER_BYTES,
    max_entries: int = DEFAULT_MAX_DIRECTORY_ENTRIES,
    scan: bool = True,
    scan_budget_bytes: int | None = DEFAULT_MAX_UPLOAD_BYTES,
    ignore: _ignore.IgnoreRules | None = None,
) -> dict[str, Any]:
    """Manifest for a directory that is NOT a git repository.

    Same shape and the same :func:`_classify_by_size` rule as
    :func:`capture_manifest`; the differences are WHICH files get walked (the
    filtered walk below rather than ``ls-files``) and that ``base_commit`` and
    ``remote`` are None because there is no repo to take them from.

    The walk is size-gated like everything else: a file over
    ``reference_over_bytes`` is recorded as a file-path reference rather than
    swept into the archive, where it would push the whole snapshot past the
    upload ceiling and lose the other files with it.

    The exclusions are the whole design. Git gave the classifier `.gitignore` for
    free; a bare directory has nothing, so the defaults have to be conservative in
    the one direction that matters. ``SKIP_DIRS`` drops what a lockfile rebuilds,
    and ``SKIP_SECRETS`` drops credential-shaped files -- auto-uploading a working
    directory must not be how a `.env` leaves the machine. The SDK's own folders
    (its outbox, its state, its ``$TMPDIR`` stand-ins: `probe.sdk.owndirs`) are
    skipped too, when the tree holds one: a job started in ``$TMPDIR`` used to
    take its own queue files as its code.

    Everything skipped is REPORTED in ``skipped``, because once a filter exists,
    absence from the manifest stops being informative on its own: a reader has to
    be able to tell "not an input" from "excluded by policy".

    ``max_entries`` bounds the walk (see ``DEFAULT_MAX_DIRECTORY_ENTRIES``) and is
    checked DURING it, not after: the cost being bounded is the walk itself, so a
    ceiling enforced on the finished manifest would refuse a tree only after
    paying the minute it took to build it.

    A name is not the only way a credential arrives: a `config.yaml` holding an
    HF token has an innocent name. With ``scan`` (the default) every file that
    could be uploaded is content-scanned (:class:`_ContentGate`, bounded by
    ``scan_budget_bytes``; None = unbounded) and WITHHELD when it holds one: kept
    in ``entries`` as ``source: "withheld"``, never uploaded, and reported.
    """
    cwd = os.path.abspath(cwd or os.getcwd())
    if not os.path.isdir(cwd):
        raise SnapshotError(f"{cwd} is not a directory")

    entries: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    gate = _ContentGate(scan=scan, budget=scan_budget_bytes)

    def _guard() -> None:
        if len(entries) <= max_entries:
            return
        raise SnapshotTooLarge(
            f"{cwd} holds more than {max_entries:,} capturable files and is not a "
            "git repository, so every one of them would be hashed and uploaded. "
            "That is a workspace, not a project: start the run from the project "
            "directory, or pass max_entries= to raise the ceiling deliberately."
        )

    ignored = _Ignored(ignore, cwd)
    # The SDK's own folders (its outbox, its state, its $TMPDIR stand-ins)
    # when this tree holds one: a job started in $TMPDIR swept its own queue.
    own = _owndirs.current().within(os.path.realpath(cwd))
    for root, dirnames, filenames in os.walk(cwd):
        for name in sorted(dirnames):
            if name in SKIP_DIRS:
                skipped.append(
                    {
                        "path": _posix(os.path.relpath(os.path.join(root, name), cwd)),
                        "reason": "secret" if name in SKIP_SECRET_DIRS else "generated",
                    }
                )
        kept = []
        for d in sorted(dirnames):
            if d in SKIP_DIRS:
                continue
            rel_dir = _posix(os.path.relpath(os.path.join(root, d), cwd))
            if own is not None and own.top(rel_dir) is not None:
                skipped.append({"path": rel_dir, "reason": _owndirs.REASON})
                continue
            if not ignored.directory(rel_dir):
                kept.append(d)
        dirnames[:] = kept

        for name in sorted(filenames):
            full = os.path.join(root, name)
            rel = _posix(os.path.relpath(full, cwd))
            if own is not None and own.top(rel) is not None:
                skipped.append({"path": rel, "reason": _owndirs.REASON})
                continue
            reason = _skip_reason(name)
            if reason is not None:
                skipped.append({"path": rel, "reason": reason})
                continue
            if ignored.path(rel):
                continue
            if os.path.islink(full):
                target = os.readlink(full)
                entries.append({
                    "path": rel,
                    "mode": "120000",
                    "sha256": hashlib.sha256(target.encode()).hexdigest(),
                    "size": len(target.encode()),
                    "source": "blob",
                    "symlink_target": target,
                })
                _guard()
                continue
            if not os.path.isfile(full):
                continue
            # Counted BEFORE the hash: reading the file is the cost the ceiling
            # exists to stop paying.
            entries.append({"path": rel})
            _guard()
            entries[-1] = gate.entry(full, rel, reference_over_bytes=reference_over_bytes)

    if include:
        entries.extend(
            _include_entries(
                cwd,
                include,
                # Already decided -- captured, withheld, or skipped and reported --
                # so an include that names one again neither re-adds nor re-reports it.
                # A `.probeignore` exclusion is not in this set: an explicit include wins.
                {e["path"] for e in entries} | {s["path"] for s in skipped},
                reference_over_bytes=reference_over_bytes,
                gate=gate,
                skipped=skipped,
                own=own,
            )
        )
    skipped.extend(ignored.report(entries))
    skipped.extend(gate.skipped)
    # The walk above already includes lockfiles -- they are not in any SKIP
    # filter -- so only the identity tag is new here, matching capture_manifest.
    for e in entries:
        if "/" not in e["path"] and _is_lockfile(e["path"]):
            e["lockfile"] = True
    entries.sort(key=lambda e: e["path"])

    return {
        "entries": entries,
        "tree_sha256": tree_digest(entries),
        "base_commit": None,
        "remote": None,
        "n_git_referenced": 0,
        "n_pending_upload": sum(1 for e in entries if e["source"] == "blob"),
        "n_referenced_offsite": sum(1 for e in entries if e["source"] == "reference"),
        "n_withheld": sum(1 for e in entries if e["source"] == "withheld"),
        "vcs": None,
        "skipped": skipped,
        **({"n_probeignore": ignored.count} if ignored.count else {}),
    }


#: Cap on reported ignored-secret paths. A repo can `.gitignore` an entire
#: directory of certificates; the point is to tell a reader that credential-
#: shaped inputs were excluded, not to enumerate every one.
MAX_REPORTED_IGNORED_SECRETS = 20


def _ignored_secrets(cwd: str) -> list[dict[str, str]]:
    """Gitignored, credential-shaped paths — REPORTED, never captured.

    The non-git walk has always reported these: ``SKIP_SECRETS`` drops a `.env`
    and `skipped` records that it did, so a reader can tell "not an input" from
    "excluded by policy". Inside a repo the same file was excluded even more
    quietly -- `ls-files --exclude-standard` simply never offers it, and only
    lockfiles get a force-add -- so absence carried no information at all. That
    asymmetry is the bug: the git path is the common one, and a run whose
    behaviour depended on a gitignored `.env` looked identically captured to one
    that needed nothing.

    Excluding them stays correct — auto-uploading a working directory must not
    be how a credential leaves the machine. Only the silence changes.

    ``--directory`` collapses an ignored directory to one entry instead of
    walking it, which keeps this bounded on a repo that ignores `.venv` or
    `node_modules`. Directories are then dropped: a collapsed `secrets/` says
    nothing about what is inside, and claiming otherwise would be worse than
    silence.
    """
    listing = _git_paths(
        cwd, "ls-files", "-z", "--others", "--ignored", "--exclude-standard", "--directory",
        check=False,
    )
    found: list[dict[str, str]] = []
    for path in listing:
        path = _printable(path)
        if not path or path.endswith("/"):
            continue
        reason = _skip_reason(os.path.basename(path))
        if reason == "secret":
            found.append({"path": path, "reason": reason})
    found.sort(key=lambda s: s["path"])
    if len(found) > MAX_REPORTED_IGNORED_SECRETS:
        extra = len(found) - MAX_REPORTED_IGNORED_SECRETS
        found = found[:MAX_REPORTED_IGNORED_SECRETS]
        found.append({"path": f"<{extra} more>", "reason": "secret"})
    return found


def capture_manifest(
    cwd: str | None = None,
    *,
    include: list[str] | None = None,
    reference_over_bytes: int = DEFAULT_REFERENCE_OVER_BYTES,
    max_entries: int = DEFAULT_MAX_DIRECTORY_ENTRIES,
    scan: bool = True,
    scan_budget_bytes: int | None = DEFAULT_MAX_UPLOAD_BYTES,
    ignore: _ignore.IgnoreRules | None = None,
) -> dict[str, Any]:
    """Classify each captured file as bytes-to-upload or too-large-to-copy.

    CLASSIFICATION ONLY. Nothing here moves bytes: a ``source="blob"`` entry
    carries ``path``/``mode``/``sha256``/``size`` and says "someone must upload
    this". ``n_pending_upload`` is a work count, not a record of work done.

    **Git referencing is retired.** Every tracked file's bytes are uploaded,
    whether or not a pushed commit holds the same content. What used to happen
    -- byte-identical to a pushed commit means record a blob id and skip the
    upload -- traded a certain, cheap copy for a pointer that resolves only
    while the remote does. The bytes are the record; git is provenance. See
    :func:`_classify_by_size`.

    The single remaining escape is size: over ``reference_over_bytes`` a file
    becomes a FILE-PATH reference (path, host, sha256), never a git one, because
    copying a 40GB checkpoint into every run of a sweep is duplication rather
    than reproducibility.

    ``tree_sha256`` hashes ``(path, mode, sha256)`` and deliberately excludes the
    source, so an identity minted before this change still matches the same tree
    captured after it. Symlinks participate as their target so a retarget is
    visible.

    Outside a git repository this delegates to :func:`capture_directory_manifest`,
    which now differs only in WHICH files it walks (a filtered directory walk
    rather than ``ls-files``) and in having no ``base_commit``/``remote`` to
    record. The classification is identical, which it was not while git
    referencing existed. ``max_entries`` bounds that path only -- inside a repo
    the walk is already bounded by what git tracks.

    **The credential stops are the same on both paths.** ``ls-files`` offers
    every untracked file that is not ignored, and this used to classify all of
    them for upload with no filter at all: live, an untracked `.env` and a
    scratch file holding a `probe_pat_` token were stored byte-identical. Now:

    - an UNTRACKED path passes :func:`_skip_reason` (the directory walk's name
      filter); a TRACKED one only :func:`_tracked_skip_reason` (exact names,
      prefixes, suffixes -- a committed `tap_core/secrets.py` is code);
    - any path under a credential folder (``SKIP_SECRET_DIRS``) is skipped;
    - with ``scan`` (the default) every file that could be uploaded passes
      :class:`_ContentGate` and is WITHHELD when its content holds a credential
      (kept in ``entries`` as ``source: "withheld"``, never uploaded).

    Everything stopped is reported in ``skipped`` (a tracked one marked
    ``tracked: true``), never dropped in silence.
    """
    cwd = cwd or os.getcwd()

    def as_directory() -> dict[str, Any]:
        # Forwarded, not dropped: this used to call through with the cwd alone, so
        # an explicitly `include=`d file was silently absent from the manifest of
        # any non-git tree -- the one place the caller had said out loud that it
        # mattered.
        return capture_directory_manifest(
            cwd,
            include=include,
            reference_over_bytes=reference_over_bytes,
            max_entries=max_entries,
            scan=scan,
            scan_budget_bytes=scan_budget_bytes,
            ignore=ignore,
        )

    if not is_git_repo(cwd):
        return as_directory()
    try:
        tracked = set(_git_paths(cwd, "ls-files", "-z", "--cached"))
        untracked = _git_paths(cwd, "ls-files", "-z", "--others", "--exclude-standard")
    except SnapshotError:
        # A repo git can find but not list (a corrupt index) is captured like one
        # git cannot read at all: as a plain directory. Git is provenance and may
        # never cost the capture (plan 2.6); `git_provenance` records why.
        return as_directory()

    base, remote = pushed_base(cwd)
    listed = sorted(tracked | set(untracked))
    # A name that is not valid UTF-8 (decoded with surrogates) cannot enter the
    # tree digest or the JSON execution record; it is excluded VISIBLY, like a
    # credential-shaped name, never dropped in silence.
    unencodable = [p for p in listed if not _utf8_clean(p)]
    outside = [p for p in listed if _utf8_clean(p) and not is_inside_tree(p)]
    paths = sorted(p for p in listed if is_inside_tree(p) and _utf8_clean(p))

    entries: list[dict[str, Any]] = []
    named: list[dict[str, Any]] = []  # credential folders, credential-shaped or generated names
    gate = _ContentGate(scan=scan, budget=scan_budget_bytes)
    ignored = _Ignored(ignore, cwd)
    # An untracked outbox or state folder in the repo (XDG_STATE_HOME inside
    # it, a dotfiles repo at $HOME): one report per folder, never its files.
    own = _owndirs.current().within(os.path.realpath(cwd))
    own_tops: set[str] = set()
    for path in paths:
        if own is not None:
            top = own.top(path)
            if top is not None:
                own_tops.add(top)
                continue
        full = os.path.join(cwd, path)
        is_tracked = path in tracked
        base_name = os.path.basename(path)
        if _in_secret_dir(path):
            reason: str | None = "secret"
        elif is_tracked:
            reason = _tracked_skip_reason(base_name)
        else:
            reason = _skip_reason(base_name)
        if reason is not None:
            named.append({"path": path, "reason": reason, **({"tracked": True} if is_tracked else {})})
            continue
        if ignored.path(path):
            continue
        if os.path.islink(full):
            target = os.readlink(full)
            entries.append({
                "path": path,
                "mode": "120000",
                "sha256": hashlib.sha256(target.encode()).hexdigest(),
                "size": len(target.encode()),
                "source": "blob",
                "symlink_target": target,
            })
            continue
        # `ls-files --cached` still lists tracked files deleted from the worktree.
        if not os.path.isfile(full):
            continue
        entries.append(
            gate.entry(full, path, reference_over_bytes=reference_over_bytes, tracked=is_tracked)
        )
    named.extend({"path": top, "reason": _owndirs.REASON} for top in sorted(own_tops))

    if include:
        entries.extend(
            _include_entries(
                cwd,
                include,
                # Already decided -- captured, withheld, or skipped and reported --
                # so an include that names one again neither re-adds nor re-reports it.
                # A `.probeignore` exclusion is not in this set: an explicit include wins.
                {e["path"] for e in entries} | {s["path"] for s in named},
                reference_over_bytes=reference_over_bytes,
                gate=gate,
                skipped=named,
                own=own,
            )
        )
        entries.sort(key=lambda e: e["path"])

    # Root-level lockfiles are FORCED into the manifest even when `.gitignore`
    # would otherwise hide them from `ls-files` -- the exact gap that lost a
    # dirty uv.lock with no record at all. Already-tracked/included lockfiles
    # just get the identity tag below; only the gitignored/untracked case needs
    # a new entry, and it is capped so an oversized one is reported, not shipped.
    skipped: list[dict[str, Any]] = _ignored_secrets(cwd)
    reported = {s["path"] for s in skipped}
    # An include can name a gitignored credential `_ignored_secrets` already
    # reported; one path, one report.
    skipped.extend(s for s in named if s["path"] not in reported)
    skipped.extend({"path": _printable(p), "reason": "non_utf8_name"} for p in unencodable)
    skipped.extend({"path": p, "reason": "outside_tree"} for p in outside)
    have = {e["path"] for e in entries} | {s["path"] for s in skipped} | set(ignored.records)
    for name in sorted(os.listdir(cwd)):
        if not _is_lockfile(name):
            continue
        full = os.path.join(cwd, name)
        if not os.path.isfile(full) or os.path.islink(full):
            continue
        if name in have:
            continue  # tracked, included or already reported; tagged below
        if ignored.path(name):
            continue  # forced in only by default, so a `.probeignore` line wins
        if os.path.getsize(full) > DEFAULT_MAX_LOCKFILE_BYTES:
            skipped.append({"path": name, "reason": "lockfile_too_large"})
            continue
        # A lockfile is content like any other: a private index URL with its
        # password in it must not ride along because the file is a lockfile.
        entry = gate.entry(
            full, name, reference_over_bytes=DEFAULT_MAX_LOCKFILE_BYTES, lockfile=True
        )
        entry["mode"] = "100644"
        entries.append(entry)
    skipped.extend(ignored.report(entries))
    skipped.extend(gate.skipped)
    for e in entries:
        if "/" not in e["path"] and _is_lockfile(e["path"]):
            e["lockfile"] = True
    entries.sort(key=lambda e: e["path"])

    return {
        "entries": entries,
        "tree_sha256": tree_digest(entries),
        "base_commit": base,
        # PROVENANCE ONLY, since git referencing was retired: "this tree
        # corresponds to commit X on remote Y", which a human reads and
        # `check_run --verify` may still resolve. No entry's bytes depend on it.
        "remote": remote,
        # Structurally 0 now. Kept in the shape rather than dropped because
        # `restore`, `snapshot-show` and the code-snapshot meta of every run
        # captured before this read the key, and an absent key would read as
        # "unknown" where the truthful answer is "none".
        "n_git_referenced": 0,
        "n_pending_upload": sum(1 for e in entries if e["source"] == "blob"),
        "n_referenced_offsite": sum(1 for e in entries if e["source"] == "reference"),
        "n_withheld": sum(1 for e in entries if e["source"] == "withheld"),
        "skipped": skipped,
        **({"n_probeignore": ignored.count} if ignored.count else {}),
    }



CODE_BYTES_ARTIFACT = "code-bytes"


class SnapshotTooLarge(SnapshotError):
    """The pending bytes exceed the cap. Never truncated to fit."""


class _ChangedUnderStream(SnapshotError):
    """A file's bytes changed between its verification read and the read that
    streamed it into the tar; the wrong member is already written. Carries the
    path so the builder can rebuild once with that file reported as changed."""

    def __init__(self, path: str) -> None:
        super().__init__(
            f"{path!r} changed while it was being archived; the archive is discarded"
        )
        self.path = path


def pending_entries(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """The files git cannot supply -- edited, untracked, unpushed, or no remote.

    These are exactly the files that make a run unreproducible on any other
    machine: the manifest records a sha256 for them, and a sha256 verifies a file
    you already have rather than producing one you do not.

    ``source="reference"`` is deliberately excluded: those are the deliberately
    off-platform ones (a base checkpoint on a shared volume), identified and
    verifiable but not copied.
    """
    return [e for e in (manifest.get("entries") or []) if e.get("source") == "blob"]


def build_pending_archive(
    cwd: str,
    manifest: dict[str, Any],
    dest: str,
    *,
    max_bytes: int = DEFAULT_MAX_UPLOAD_BYTES,
) -> dict[str, Any]:
    """Tar+gzip exactly the pending files into ``dest``. Returns a summary.

    DETERMINISTIC: mtime, uid/gid, owner names and member order are all
    normalised, and gzip's own mtime header is zeroed. Two identical trees
    therefore produce byte-identical archives, which is what lets the upload's
    content-addressed ``have`` check short-circuit -- a 200-run sweep over
    unchanged code uploads once and skips the other 199.

    Modes and symlinks survive: the manifest already distinguishes ``100755``
    from ``100644`` and records ``symlink_target`` for ``120000`` entries, and a
    restored tree that lost the executable bit does not run.

    Raises :class:`SnapshotTooLarge` rather than dropping files to fit.

    A tree that DRIFTED since the manifest was taken (a log the training job is
    still appending to, a results file rewritten, a temp file gone) is not an
    error and not a reason to store nothing: every regular file is hashed as it
    streams into the tar and compared to the manifest's ``sha256``/``size``,
    every symlink's target to ``symlink_target``, and the ones that still match
    are archived. The ones that do not are left out and NAMED -- ``missing`` and
    ``changed`` in the summary, ``n_files`` = what was actually written -- so the
    caller records them as unstored and a reader sees exactly which files this
    run is missing. What used to happen here was the silent version: a missing
    file was skipped and ``n_files`` still claimed it (an archive recorded as
    7,689 files held 316).

    Two things DO raise :class:`SnapshotError`: a manifest entry with no
    ``sha256``/``size`` (a malformed record, never archived unverified) and a
    file that shrank while its bytes were streaming (the tar member is already
    short, so the archive cannot be continued). Both leave nothing on disk.
    """
    pending = pending_entries(manifest)
    total = sum(int(e.get("size") or 0) for e in pending)
    if total > max_bytes:
        raise SnapshotTooLarge(
            f"pending code bytes are {total / 1e6:.1f} MB, over the "
            f"{max_bytes / 1e6:.0f} MB cap; raise --max-upload-mb, or lower "
            "--reference-over-mb so the large files are recorded where they "
            "live instead of copied"
        )


    # gzip mtime=0 AND filename="" so the container header is deterministic too,
    # not just the tar. Without the explicit filename, GzipFile copies the output
    # file's own name into the header -- so writing the same tree to two paths
    # produced two different hashes and the upload's content-addressed dedup
    # never fired. A test pins this.
    # A file whose bytes change between its verification read and the streamed
    # read has already put a wrong member in the tar. A sqlite file or an mmap'd
    # progress array rewritten in place at constant size can do that on every
    # snapshot, so the archive is rebuilt ONCE with that file reported as
    # changed; a second such file in the rebuild is genuinely a tree that will
    # not hold still, and raises.
    exclude: set[str] = set()
    for _attempt in (1, 2):
        try:
            missing, changed, written, written_bytes = _build_archive_once(
                cwd, pending, dest, exclude
            )
            break
        except _ChangedUnderStream as exc:
            if _attempt == 2:
                raise SnapshotError(f"{exc}; re-run the snapshot") from exc
            exclude.add(exc.path)

    sha, size = _file_sha256(dest)
    return {
        "path": dest,
        "sha256": sha,
        "size_bytes": size,
        "n_files": written,
        "uncompressed_bytes": written_bytes,
        "missing": missing,
        "changed": changed,
        "drift_message": (
            _partial_archive_message(missing, changed) if (missing or changed) else None
        ),
    }


_Verdict = Literal["written", "missing", "changed"]


def _build_archive_once(
    cwd: str, pending: list[dict[str, Any]], dest: str, exclude: set[str]
) -> tuple[list[str], list[str], int, int]:
    """One pass over ``pending`` into a fresh ``dest``. Paths in ``exclude`` are
    reported changed without being read. Any exception unlinks ``dest``."""
    import gzip
    import tarfile

    missing: list[str] = []
    changed: list[str] = []
    written = 0
    written_bytes = 0
    try:
        # Level 6, not the default 9: measured on a 7,902-file / 152 MB tree,
        # level 9 was ~60% of this function's wall time (14.1 s vs 5.6 s) for
        # 0.3% smaller output. Any fixed level keeps the archive deterministic.
        with open(dest, "wb") as raw, gzip.GzipFile(
            filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=6
        ) as gz:
            with tarfile.open(fileobj=gz, mode="w") as archive:
                for entry in sorted(pending, key=lambda e: str(e.get("path"))):
                    path = entry.get("path")
                    verdict = "changed" if path in exclude else _archive_entry(archive, cwd, entry)
                    if verdict == "missing":
                        missing.append(path)
                    elif verdict == "changed":
                        changed.append(path)
                    else:
                        written += 1
                        written_bytes += int(entry.get("size") or 0)
    except BaseException:
        # Whatever interrupted the write, never leave a partial archive behind.
        with contextlib.suppress(OSError):
            os.unlink(dest)
        raise
    return missing, changed, written, written_bytes

#: How many drifted paths ride on the artifact meta / return dict. The COUNT is
#: never capped (``pending_upload`` is exact); the list is, because a tree that
#: drifted by thousands of files does not need thousands of names on one row.
DRIFTED_META_LIMIT = 50
_HASH_CHUNK = 1 << 20


def _archive_entry(archive: Any, cwd: str, entry: dict[str, Any]) -> _Verdict:
    """Verify ONE manifest entry against the working tree and stream it into
    ``archive`` if it still matches. Returns ``"written"``, ``"missing"`` or
    ``"changed"``. Raises SnapshotError for a malformed entry, a path that would
    leave the tree, a file that shrank or changed while its bytes were entering
    the tar, or an archive write failure -- every one leaves nothing on disk.

    Source-side surprises are verdicts, never exceptions: the file is opened
    with ``O_NOFOLLOW | O_NONBLOCK`` so a symlink or FIFO swapped in between the
    ``lstat`` and the ``open`` is refused on the descriptor instead of followed
    or blocked on; ``fstat`` re-checks "regular file of the recorded size"; the
    file is hashed BEFORE it is streamed (bounded to the recorded size, so a
    log that grew keeps its recorded prefix and archives as recorded), and
    hashed again as it streams. A mismatch on that second hash means the bytes
    changed inside the window between the two reads and a wrong member is
    already in the tar: that aborts the archive rather than uploading unverified
    bytes under a verified name.
    """
    import tarfile

    path = entry.get("path")
    if not isinstance(path, str) or not is_inside_tree(path):
        raise SnapshotError(f"manifest entry path {path!r} is not a relative path inside the tree")
    full = os.path.join(cwd, path)
    mode = entry.get("mode")

    if mode == "120000":
        recorded = entry.get("symlink_target")
        if not isinstance(recorded, str):
            raise SnapshotError(f"manifest entry {path!r} is a symlink with no recorded target")
        try:
            target = os.readlink(full)
        except FileNotFoundError:
            return "missing"
        except OSError:
            return "changed"  # not a symlink any more, or unreadable
        if target != recorded:
            return "changed"
        info = tarfile.TarInfo(path)
        info.type = tarfile.SYMTYPE
        info.linkname = recorded
        _normalise_member(info)
        _write_member(archive, info, None, path)
        return "written"

    verdict, fh = open_verified_file(cwd, entry)
    if verdict != "ok" or fh is None:
        return verdict  # "missing" | "changed"
    expected_size = int(entry["size"])
    expected_sha = entry["sha256"]
    with fh:
        info = tarfile.TarInfo(path)
        info.size = expected_size
        info.mode = 0o755 if mode == "100755" else 0o644
        _normalise_member(info)
        reader = _HashingReader(fh)
        _write_member(archive, info, reader, path, expected_size)
    if reader.hexdigest() != expected_sha:
        raise _ChangedUnderStream(path)
    return "written"


def open_verified_file(cwd: str, entry: dict[str, Any]) -> tuple[str, Any]:
    """Open ONE manifest entry's regular file only if it still matches its
    record, and hand back the descriptor positioned at byte 0.

    Returns ``("ok", fh)`` -- the caller owns and closes ``fh`` -- or
    ``("missing", None)`` / ``("changed", None)``. The file is opened with
    ``O_NOFOLLOW | O_NONBLOCK`` so a symlink or FIFO swapped in since the
    manifest is refused on the descriptor instead of followed or blocked on;
    ``fstat`` re-checks "regular file of the recorded size"; the bytes are hashed
    (bounded to the recorded size) BEFORE anything reads them again, so a
    consumer that streams the same descriptor sends exactly the bytes that were
    verified. Shared by the archive and the per-file capture paths: whatever
    leaves the machine has been checked against the record the same way.
    Raises SnapshotError for a malformed entry or a path that leaves the tree.
    """
    path = entry.get("path")
    if not isinstance(path, str) or not is_inside_tree(path):
        raise SnapshotError(f"manifest entry path {path!r} is not a relative path inside the tree")
    full = os.path.join(cwd, path)
    expected_sha = entry.get("sha256")
    size = entry.get("size")
    if not isinstance(expected_sha, str) or not expected_sha or isinstance(size, bool):
        raise SnapshotError(f"manifest entry {path!r} has no sha256/size; the record is malformed")
    try:
        expected_size = int(size)
    except (TypeError, ValueError):
        raise SnapshotError(f"manifest entry {path!r} has no sha256/size; the record is malformed") from None
    if expected_size < 0:
        raise SnapshotError(f"manifest entry {path!r} has a negative size; the record is malformed")

    try:
        st = os.lstat(full)
    except FileNotFoundError:
        return "missing", None
    except OSError:
        return "changed", None
    if not stat.S_ISREG(st.st_mode) or st.st_size != expected_size:
        return "changed", None
    # Every flag guarded: Windows has neither O_NONBLOCK nor O_NOFOLLOW, and an
    # AttributeError here would escape the fail-open handler.
    flags = (
        os.O_RDONLY
        | getattr(os, "O_NONBLOCK", 0)
        | getattr(os, "O_NOFOLLOW", 0)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_BINARY", 0)
    )
    try:
        fd = os.open(full, flags)
    except FileNotFoundError:
        return "missing", None
    except OSError:
        return "changed", None  # ELOOP (a symlink now), ENXIO, EACCES, ...
    fh = os.fdopen(fd, "rb")
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size != expected_size:
            fh.close()
            return "changed", None
        _clear_nonblock(fd)
        pre = _HashingReader(fh)
        remaining = expected_size
        while remaining:
            chunk = pre.read(min(_HASH_CHUNK, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
        if pre.bytes_read != expected_size or pre.hexdigest() != expected_sha:
            fh.close()
            return "changed", None
        fh.seek(0)
    except OSError:
        fh.close()
        return "changed", None
    return "ok", fh


def _clear_nonblock(fd: int) -> None:
    """Drop O_NONBLOCK after the descriptor proved to be a regular file (it was
    only there so a swapped-in FIFO could not block the open). No-op where the
    flag or fcntl does not exist (Windows)."""
    nonblock = getattr(os, "O_NONBLOCK", 0)
    if not nonblock:
        return
    try:
        import fcntl
    except ImportError:
        return
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) & ~nonblock)


def _write_member(archive: Any, info: Any, reader: Any, path: str, expected_size: int = 0) -> None:
    """One place for every archive write, so a write-side failure (ENOSPC, EIO,
    a file that shrank under the stream) is ALWAYS an abort with a precise
    message -- never mistaken for source drift and carried on from."""
    try:
        if reader is None:
            archive.addfile(info)
        else:
            archive.addfile(info, reader)
    except OSError as exc:
        if reader is not None and reader.bytes_read < expected_size:
            raise SnapshotError(
                f"{path!r} shrank while it was being archived; the archive is discarded, "
                "re-run the snapshot"
            ) from exc
        raise SnapshotError(f"writing {path!r} to the archive failed: {exc}") from exc


def _normalise_member(info: Any) -> None:  # tarfile.TarInfo; tarfile is imported lazily
    """Zero every field that would make two identical trees hash differently."""
    info.mtime = 0
    info.uid = info.gid = 0
    info.uname = info.gname = ""


class _HashingReader:
    """Hashes exactly the bytes pulled through it and counts them. Used twice per
    file: once to verify the file BEFORE it is streamed (bounded to the recorded
    size), once on the bytes ``tarfile`` actually pulls into the archive."""

    def __init__(self, fh) -> None:
        self._fh = fh
        self._h = hashlib.sha256()
        self.bytes_read = 0

    def read(self, n: int = -1) -> bytes:
        chunk = self._fh.read(n)
        self._h.update(chunk)
        self.bytes_read += len(chunk)
        return chunk

    def hexdigest(self) -> str:
        return self._h.hexdigest()


_PARTIAL_LIST_LIMIT = 5


def _partial_archive_message(missing: list[str], changed: list[str]) -> str:
    def _show(paths: list[str]) -> str:
        head = ", ".join(paths[:_PARTIAL_LIST_LIMIT])
        extra = len(paths) - _PARTIAL_LIST_LIMIT
        return head + (f", +{extra} more" if extra > 0 else "")

    parts = []
    if missing:
        parts.append(f"{len(missing)} missing from the working tree ({_show(missing)})")
    if changed:
        parts.append(f"{len(changed)} changed since the manifest was taken ({_show(changed)})")
    return (
        "left out of the archive because the tree no longer matched its manifest: "
        + "; ".join(parts)
        + ". Re-run the snapshot to capture them."
    )




# THE enumeration -- there is deliberately only one, and it always runs inside
# the TARGET interpreter, even when that is this process.
#
# An in-process variant used to exist alongside this for the SDK path. It was
# deleted rather than kept-and-tested: two implementations of one algorithm
# whose outputs are HASHED into `env_ref` will drift, and the drift surfaces as
# two identical environments comparing unequal -- indistinguishable from a real
# dependency change. Its only unique capability was seeing runtime `sys.path`
# mutations, and those are derivable: the `sys.path.insert` line lives in the
# code the snapshot already captures. The spawn costs ~50ms ONCE per run (a
# snapshot is a launch-time act, not a training-loop one), so there is no hot
# path to protect here -- that constraint belongs to `probe log`.
#
# Written for the oldest interpreter a project venv might hold: `dist.name` is
# 3.10+, `dist.metadata['Name']` is not. First occurrence wins, matching
# `sys.path` shadowing order. No pip required -- `uv venv` installs none.
_ENUMERATE_PROGRAM = r"""
import json, sys
from importlib import metadata

seen = {}
for dist in metadata.distributions():
    try:
        name = dist.metadata["Name"]
    except Exception:
        name = None
    if not name:
        continue
    if name not in seen:
        seen[name] = dist.version or "0"
json.dump(
    {
        "python": ".".join(str(p) for p in sys.version_info[:3]),
        "executable": sys.executable,
        "packages": sorted("%s==%s" % (n, v) for n, v in seen.items()),
    },
    sys.stdout,
)
"""

_ENUMERATE_TIMEOUT = 60.0

# Layout of a venv, POSIX and Windows.
_VENV_BIN = ("bin", "Scripts")
_VENV_PYTHON = ("python", "python3", "python.exe")
# Ordered: a project that has both `.venv` and `venv` almost always maintains
# the first (uv, poetry and pdm all create `.venv`) and keeps the other stale.
_VENV_DIR_NAMES = (".venv", "venv", "env")


def venv_python(venv: str) -> str | None:
    """The interpreter inside ``venv``, or None if it does not look like a venv."""
    for bindir in _VENV_BIN:
        for name in _VENV_PYTHON:
            candidate = os.path.join(venv, bindir, name)
            if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
                return candidate
    return None


def find_venv(cwd: str | None = None) -> tuple[str | None, str | None]:
    """Locate the virtualenv whose packages belong to the code at ``cwd``.

    Returns ``(venv_root, resolved_via)``, or ``(None, None)``.

    Order, strongest tie to the snapshotted code first:

    1. a venv directory inside the project -- ``.venv`` / ``venv`` / ``env``,
       walking ``cwd`` upward and stopping AT the git toplevel. The snapshot is
       of a repository, so the search is bounded by that repository; without the
       bound a project with no venv would silently adopt one from a parent
       directory that has nothing to do with it.
    2. ``VIRTUAL_ENV`` -- an activated env, including the one ``uv run`` exports.
    3. ``CONDA_PREFIX`` -- conda envs live outside the project by design.
    """
    cwd = os.path.abspath(cwd or os.getcwd())

    top = _git(cwd, "rev-parse", "--show-toplevel", check=False)
    ceiling = os.path.abspath(top) if top else cwd

    directory = cwd
    while True:
        for name in _VENV_DIR_NAMES:
            candidate = os.path.join(directory, name)
            if venv_python(candidate):
                return candidate, "project-venv"
        if os.path.normcase(directory) == os.path.normcase(ceiling):
            break
        parent = os.path.dirname(directory)
        if parent == directory:
            break
        directory = parent

    for var in ("VIRTUAL_ENV", "CONDA_PREFIX"):
        value = os.environ.get(var)
        if value and venv_python(value):
            return os.path.abspath(value), var

    return None, None


def _enumerate_foreign(python: str) -> tuple[str, list[str]]:
    """``(python_version, packages)`` as reported BY ``python`` itself.

    ``PYTHONHOME`` is dropped because it repoints an interpreter's stdlib at
    another installation's, which breaks a foreign interpreter outright. The
    rest of the environment is inherited on purpose: ``PYTHONPATH`` and user
    site-packages genuinely contribute modules to the run being recorded, so
    isolating them would record an environment nobody actually uses.
    """
    env = {k: v for k, v in os.environ.items() if k != "PYTHONHOME"}
    try:
        proc = subprocess.run(
            [python, "-c", _ENUMERATE_PROGRAM],
            capture_output=True,
            text=True,
            timeout=_ENUMERATE_TIMEOUT,
            env=env,
        )
    except subprocess.TimeoutExpired:
        raise SnapshotError(
            f"{python} did not report its packages within {_ENUMERATE_TIMEOUT}s"
        ) from None
    except OSError as exc:
        raise SnapshotError(f"could not run {python}: {exc}") from exc
    if proc.returncode != 0:
        raise SnapshotError(
            f"{python} could not enumerate its packages: {proc.stderr.strip()[:400]}"
        )
    try:
        payload = json.loads(proc.stdout)
        return payload["python"], list(payload["packages"])
    except (ValueError, KeyError, TypeError) as exc:
        raise SnapshotError(f"{python} returned an unreadable package list: {exc}") from exc


def _is_inside(path: str, root: str) -> bool:
    try:
        return not os.path.relpath(os.path.realpath(path), os.path.realpath(root)).startswith("..")
    except ValueError:  # different drives on Windows
        return False


#: ``resolved_via`` when no environment could be attributed to the project: no
#: venv was found and the running interpreter is foreign to the tree. A NAMED
#: constant because it is a cross-module contract -- `capture_env` produces it
#: and the CLI branches on it to warn -- and a typo on either side would
#: silently restore the confident-wrong capture this value exists to prevent.
UNRESOLVED_FALLBACK = "unresolved-fallback"


def capture_env(
    cwd: str | None = None,
    *,
    venv: str | None = None,
    detect_venv: bool = False,
    strict: bool = True,
) -> dict[str, Any]:
    """Resolved dependency list for the reproducibility manifest.

    Stores the PACKAGES THEMSELVES, not just a digest of them. An earlier
    implementation kept only ``packages_sha256`` + a count, which can tell you
    that two runs differed and can never tell you what either one used -- the
    same failure shape as recording a commit SHA whose objects are gone.

    WHICH environment gets recorded is the whole problem this signature exists to
    solve. Enumerating the calling process is right for the SDK, whose
    ``run.snapshot()`` runs inside the training venv, and wrong for the CLI,
    which is a uv-tool install with its own interpreter and its own ~40
    packages. Recording those is not a degraded capture; it is a confident,
    plausible, WRONG one, and it is exactly the "different venvs" failure the
    execution record exists to eliminate.

    Resolution order:

    - ``venv`` -- an explicit path always wins.
    - ``detect_venv`` -- resolve the project's venv via :func:`find_venv`. This
      is the out-of-process caller's mode: the CLI is not the thing that runs
      the code, so its own interpreter is evidence of nothing.
    - neither -- the current interpreter, enumerated in-process. The default,
      because an in-process caller IS the environment being recorded.

    A resolved venv is read by running ``importlib.metadata`` under ITS
    interpreter, so the answer comes from the environment itself rather than
    from a guess about its layout, and no ``pip`` is required (``uv venv``
    installs none).

    ``strict`` (the default) covers two distinct failures, both of which used to
    pass silently:

    - the dependency set cannot be resolved, or resolves to nothing;
    - ``detect_venv`` found no project venv and the running interpreter is
      foreign to ``cwd`` -- i.e. we are about to record the wrong environment.

    The returned mapping carries ``venv`` / ``python_executable`` /
    ``resolved_via`` so that a capture which picked the wrong environment is
    visible rather than indistinguishable from a correct one. Those three are
    PROVENANCE, not identity: split them off with
    :func:`split_env_provenance` before the result reaches an execution record.
    """
    resolved_via = "interpreter"
    venv_root: str | None = None

    if venv is not None:
        venv_root, resolved_via = os.path.abspath(venv), "explicit"
        if venv_python(venv_root) is None:
            raise SnapshotError(f"{venv} is not a virtualenv (no bin/python inside)")
    elif detect_venv:
        venv_root, found_via = find_venv(cwd)
        if venv_root is not None:
            resolved_via = found_via or "project-venv"

    python_exe = sys.executable
    if venv_root is not None:
        python_exe = venv_python(venv_root) or sys.executable
    elif detect_venv:
        # No project venv, so the only candidate left is the interpreter running
        # this code -- acceptable only when it lives in the tree being recorded
        # (probe pip-installed into the project's own env). Anything else is the
        # caller's own toolchain, and recording it is the bug, not a fallback.
        root = cwd or os.getcwd()
        top = _git(root, "rev-parse", "--show-toplevel", check=False) or root
        if _is_inside(sys.prefix, top):
            resolved_via = "interpreter"
        elif strict:
            raise SnapshotError(
                f"no virtualenv found for {os.path.abspath(root)}, and the running "
                f"interpreter ({sys.prefix}) is outside it -- refusing to record "
                "this process's own packages as the project's. Pass --venv PATH "
                "(SDK: venv=...), or activate the environment the code runs in."
            )
        else:
            resolved_via = UNRESOLVED_FALLBACK

    info: dict[str, Any] = {
        "python": sys.version.split()[0],
        "python_executable": python_exe,
        "venv": venv_root,
        "resolved_via": resolved_via,
    }

    # The branch above has ALREADY decided this interpreter is foreign to the
    # project ("recording it is the bug, not a fallback"). Enumerating it anyway
    # is what non-strict callers used to do, and it produced a full, plausible,
    # entirely WRONG dependency list -- the CLI's own typer/rich rather than the
    # project's torch/transformers -- which is indistinguishable downstream from
    # a correct capture. Strict raises; non-strict now records the provenance and
    # nothing else, because a known-wrong answer is worse than a missing one.
    #
    # `python` goes too: this interpreter's version is no more the project's than
    # its packages are. What survives is ``resolved_via=UNRESOLVED_FALLBACK``,
    # which says why the environment is absent.
    if resolved_via == UNRESOLVED_FALLBACK:
        info.pop("python", None)
        return info

    # A frozen build (PyInstaller and friends) rewrites sys.executable to the
    # bundled application, which does not understand `-c` -- it would re-run the
    # app. Refuse instead of enumerating whatever that produces.
    if getattr(sys, "frozen", False) and python_exe == sys.executable:
        raise SnapshotError(
            "cannot enumerate packages from a frozen interpreter "
            f"({sys.executable}); pass --venv PATH (SDK: venv=...) naming the "
            "environment whose packages should be recorded"
        )

    try:
        info["python"], packages = _enumerate_foreign(python_exe)
    except SnapshotError:
        raise
    except Exception as exc:  # noqa: BLE001 - surfaced, never swallowed
        if strict:
            raise SnapshotError(f"could not resolve installed distributions: {exc}") from exc
        return info

    if not packages and strict:
        raise SnapshotError(
            f"resolved zero installed distributions from {python_exe}; refusing to "
            "record an empty dependency set as if it were captured"
        )

    info["packages"] = packages
    info["package_count"] = len(packages)
    # NOTE: the digest domain covers sorted `name==version` lines from
    # importlib.metadata, not raw `pip freeze` stdout. Do not compare values
    # across that upgrade boundary.
    info["packages_sha256"] = hashlib.sha256("\n".join(packages).encode()).hexdigest()
    return info


# How the environment was FOUND, as against what the environment IS. Machine
# -specific by nature: the same packages live at /Users/x/p/.venv on a laptop
# and /workspace/p/.venv on a training box.
ENV_PROVENANCE_KEYS = ("venv", "python_executable", "resolved_via")


def split_env_provenance(info: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """Split :func:`capture_env` output into ``(identity, provenance)``.

    The execution record's ``content_hash`` covers the WHOLE ``deps`` section
    (research-os ``app/execution/service.py`` ``canonical_hash``, which
    json-dumps every section sorted). Any machine-specific value inside it makes
    two genuinely identical environments at different paths hash differently --
    and ``env_ref`` equality is precisely what a reader compares to ask "did
    these two runs use the same environment?". Recording the venv path there
    would answer "no" to a "yes", which is the same confidently-wrong shape this
    module exists to eliminate.

    So identity (python + packages) is hashed, and provenance rides on the
    ``code-snapshot`` artifact meta, which ``Client.check_run`` already reads.
    """
    provenance = {k: info[k] for k in ENV_PROVENANCE_KEYS if k in info}
    identity = {k: v for k, v in info.items() if k not in ENV_PROVENANCE_KEYS}
    return identity, provenance


def capture_gpu() -> list[dict[str, Any]]:
    """Best-effort in-container GPU inventory via nvidia-smi (RunPod path)."""
    query = "index,name,memory.total,driver_version"
    try:
        proc = subprocess.run(
            ["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if proc.returncode != 0:
        return []
    gpus: list[dict[str, Any]] = []
    for line in proc.stdout.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) == 4:
            gpus.append(
                {
                    "index": parts[0],
                    "name": parts[1],
                    "memory_total_mib": parts[2],
                    "driver_version": parts[3],
                }
            )
    return gpus


def capture_system() -> dict[str, Any]:
    """Machine-stable identity: OS, CPU/RAM, CUDA stack. Joins the GPU inventory
    under ``execution_records.hardware`` — hashed into env identity, which is
    correct because two runs on identical nodes must still share one record.
    Per-launch facts (hostname, env values) belong in the launch block instead."""
    info: dict[str, Any] = {
        "os": {
            "platform": platform.platform(),
            "machine": platform.machine(),
            "python_implementation": platform.python_implementation(),
        },
        "cpu": {"count": os.cpu_count() or 0},
    }
    try:
        with open("/etc/os-release") as fh:
            for line in fh:
                if line.startswith("PRETTY_NAME="):
                    info["os"]["distro"] = line.split("=", 1)[1].strip().strip('"')
                    break
    except OSError:
        pass
    libc = platform.libc_ver()
    if libc[0]:
        info["os"]["libc"] = f"{libc[0]} {libc[1]}"
    try:
        names = os.sysconf_names
        if "SC_PAGE_SIZE" in names and "SC_PHYS_PAGES" in names:
            info["cpu"]["mem_total_bytes"] = (
                os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
            )
    except (OSError, ValueError, AttributeError):
        pass
    torch = sys.modules.get("torch")
    if torch is not None:
        try:
            runtime = getattr(getattr(torch, "version", None), "cuda", None)
            if runtime:
                cuda: dict[str, Any] = {"runtime": runtime}
                cudnn = torch.backends.cudnn.version()
                if cudnn:
                    cuda["cudnn"] = cudnn
                info["cuda"] = cuda
        except Exception:
            pass
    else:
        try:
            out = subprocess.run(
                ["nvcc", "--version"], capture_output=True, text=True, timeout=5
            )
            m = re.search(r"release ([\d.]+)", out.stdout)
            if m:
                info["cuda"] = {"runtime": m.group(1)}
        except (OSError, subprocess.TimeoutExpired):
            pass
    return info
