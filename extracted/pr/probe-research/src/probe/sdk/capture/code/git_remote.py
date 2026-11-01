"""find a commit a remote has (pushed base, commit on remote), recording the remote URL without credentials."""

from __future__ import annotations
import re
import subprocess
import tempfile
from functools import lru_cache


# `ls-remote` is the only git call here that touches the network. Left unbounded
# it can block the start of a training run indefinitely -- on an unreachable host,
# or worse, waiting forever on a credential prompt nobody is there to answer.
_LS_REMOTE_TIMEOUT = 10.0
# A verify fetch pulls one commit at depth 1. Bounded for the same reason as
# ls-remote: an audit must not wedge on one unreachable remote.
_VERIFY_TIMEOUT = 20.0


_SHA_RE = re.compile(r"[0-9a-f]{40,64}")
#: A commit `commit_on_remote` may ask a remote for: a full or abbreviated SHA.
_COMMIT_RE = re.compile(r"[0-9a-fA-F]{7,64}")
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

    Both come from a run's recorded metadata, which any writer in the team can
    set: a remote that reads as an option (a leading '-') or a commit that is not
    hex is never asked about, and `--` ends git's options before them.
    """
    if not remote or not commit or remote.startswith("-") or not _COMMIT_RE.fullmatch(commit):
        return False
    with tempfile.TemporaryDirectory(prefix="probe-verify-") as tmp:
        _git(tmp, "init", "-q", ".", check=False, timeout=timeout)
        try:
            proc = subprocess.run(
                ["git", "fetch", "--depth", "1", "--quiet", "--", remote, commit],
                cwd=tmp, capture_output=True, text=True,
                env=_NONINTERACTIVE_ENV(), timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            return False
        return proc.returncode == 0
from probe.sdk.capture.code.git import _NONINTERACTIVE_ENV, _git, _read_only  # noqa: E402 -- pieces need each other; the front door loads this one first
