"""GitTreeSource: a repo's tracked and untracked files through git ls-files, and its gitignored credential-shaped paths (reported, never captured)."""

from __future__ import annotations
import hashlib
import os
import subprocess
from typing import Any
from ....recording_rules import ignore as _ignore
from ... import owndirs as _owndirs
from probe.sdk.capture.code.sources.directory import (
    DEFAULT_MAX_DIRECTORY_ENTRIES,
    DEFAULT_MAX_UPLOAD_BYTES,
    DEFAULT_REFERENCE_OVER_BYTES,
    capture_directory_manifest,
)


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
DEFAULT_MAX_LOCKFILE_BYTES = 1024 * 1024


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
    # A build folder `.gitignore` does not cover (a cargo `target/` under a repo
    # with no `/target` line): one report per folder, never its files. Tracked
    # or not -- the folder declares itself a cache, and the server's sweep of
    # what older SDKs sent cannot tell tracked from untracked either. Only an
    # explicit `include=` brings one in.
    caches = TaggedCaches(cwd)
    cache_tops: set[str] = set()
    for path in paths:
        if own is not None:
            top = own.top(path)
            if top is not None:
                own_tops.add(top)
                continue
        full = os.path.join(cwd, path)
        if ignored.config_excluded(path):
            continue  # a researcher's `.probe.config`: not even its name is recorded
        cache_top = caches.top(path)
        if cache_top is not None:
            cache_tops.add(cache_top)
            continue
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
    named.extend({"path": top, "reason": "generated"} for top in sorted(cache_tops))

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
        "skipped": ignored.unnamed(skipped),
        **({"n_probeignore": ignored.count} if ignored.count else {}),
    }
from probe.sdk.capture.code.code import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    SnapshotError,
    TaggedCaches,
    _Ignored,
    _in_secret_dir,
    _include_entries,
    _is_lockfile,
    _printable,
    _skip_reason,
    _tracked_skip_reason,
    _utf8_clean,
    is_inside_tree,
    tree_digest,
)
from probe.sdk.capture.code.content_gate import _ContentGate  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.code.git import _read_only, is_git_repo  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.code.git_remote import pushed_base  # noqa: E402 -- pieces need each other; the front door loads this one first
