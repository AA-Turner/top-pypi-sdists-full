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
import hashlib
import os
import unicodedata
import re
import socket
from typing import Any
from probe.foundation.walk_skips import (  # noqa: F401 -- CACHEDIR_* served here as before
    CACHEDIR_SIGNATURE,
    CACHEDIR_TAG,
    GENERATED_DIRS,
    is_tagged_cache_dir,
)
from ...recording_rules import ignore as _ignore
from .. import owndirs as _owndirs
from ...errors import RosError
from ...artifact.hashing import local_file_uri


class SnapshotError(RosError):
    """Git plumbing failed or the cwd is not a git repository."""


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


def _probe_config_excluded(path: str, is_dir: bool) -> bool:
    """Excluded by a researcher's `.probe.config` (paths Probe never records).
    Never reported: not even the name of an excluded path goes into a manifest."""
    from ...recording_rules import recording_rules as _exclusions

    return _exclusions.excluded(path, is_dir=is_dir, hot=True).excluded


def _config_checker():
    """A `.probe.config` checker for one snapshot (`probe_config.Checker`)."""
    from ...recording_rules import recording_rules as _exclusions

    return _exclusions.checker(hot=True)


class _Ignored:
    """Paths a ``.probeignore`` pattern excluded (plan (n)), reported under
    reason ``probeignore``: an excluded directory once (the top-most one), not
    once per file under it, and at most ``PROBEIGNORE_REPORT_LIMIT`` records,
    with the exact count in ``count``.

    Applied AFTER the safety stops: a credential is reported as one whatever
    the patterns say, and nothing here can re-include a path. A path a
    researcher's ``.probe.config`` excludes is dropped BEFORE everything,
    silently (`config_excluded`): no record names it.
    """

    def __init__(self, rules: _ignore.IgnoreRules | None, cwd: str) -> None:
        self.rules = rules
        self.cwd = cwd
        self.records: dict[str, dict[str, Any]] = {}
        self._dirs: dict[str, bool] = {}
        self._config = _config_checker()
        self.count = 0

    def _dir(self, rel_dir: str) -> bool:
        hit = self._dirs.get(rel_dir)
        if hit is None:
            hit = self._dirs[rel_dir] = bool(
                self.rules
                and self.rules.ignored(rel_dir, base=self.cwd, is_dir=True, capture_root=self.cwd)
            )
        return hit

    def _config_dir(self, rel_dir: str) -> bool:
        """For a walk that prunes: is this folder closed (`off`)? A `read` folder
        stays open, for an `@probe on` line inside it; its files are checked."""
        return self._config.closed(os.path.join(self.cwd, rel_dir))

    def config_excluded(self, rel: str) -> bool:
        """Is this file excluded by a `.probe.config` (itself, or a closed folder
        above it)? One `Checker` per snapshot: paths in a row share their folders."""
        return self._config.check(os.path.join(self.cwd, rel), is_dir=False).excluded

    def unnamed(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """`records` minus any whose path a `.probe.config` excludes (as a file
        or a folder): a manifest never names an excluded path, whatever the
        reason it would have been reported for."""
        return [
            r for r in records
            if not isinstance(r.get("path"), str)
            or not self._config.check(os.path.join(self.cwd, r["path"])).excluded
        ]

    def directory(self, rel_dir: str) -> bool:
        """For a walk that prunes: is this directory excluded (recorded if a
        `.probeignore` excluded it)?"""
        if self._config_dir(rel_dir):
            return True
        if self.rules is None or not self._dir(rel_dir):
            return False
        self.records.setdefault(rel_dir, {"path": rel_dir, "reason": _ignore.REASON})
        return True

    def path(self, rel: str) -> bool:
        """Is this file excluded, by itself or by an excluded parent directory?"""
        if self.config_excluded(rel):
            return True
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
    same goes for the SDK's own folders (``own``, `probe.sdk.capture.owndirs`): its
    queue is never the run's code, reported once per folder.
    """
    config = _config_checker()
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
                if config.check(full, is_dir=os.path.isdir(full)).excluded:
                    continue  # a researcher's `.probe.config` beats an explicit include
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


def _is_lockfile(name: str) -> bool:
    return name in LOCKFILE_NAMES or fnmatch.fnmatch(name, "requirements*.txt")


# Directories that are rebuilt from a lockfile or a cache, never authored. Left
# in, the first snapshot of an ordinary Python project uploads a few hundred MB
# of `.venv` and calls it the experiment's code.
SKIP_GENERATED_DIRS = GENERATED_DIRS | {".hg", ".svn", "env", "virtualenv", ".eggs", "site-packages"}
#: Credential directories. An agent told to "keep the keys somewhere safe" makes
#: one of these; a snapshot must not then ship it. Applied to EVERY path
#: component, on every path: the git listing, the directory walk and `include=`
#: matches (the git path used to skip them only in the non-git walk, so an
#: untracked `.secrets/wandb` inside a repo went up).
SKIP_SECRET_DIRS = frozenset({".secrets", "secrets", ".aws", ".gnupg", ".ssh", ".docker"})


class TaggedCaches:
    """The top-most tagged cache folder above a relative path, each folder
    checked once. For listings that name files rather than walk folders (git's
    untracked list), where the walk's prune-on-entry is not available."""

    def __init__(self, root: str) -> None:
        self._root = root
        self._seen: dict[str, bool] = {}

    def top(self, rel: str) -> str | None:
        parts = rel.split("/")[:-1]
        for i in range(1, len(parts) + 1):
            folder = "/".join(parts[:i])
            hit = self._seen.get(folder)
            if hit is None:
                hit = self._seen[folder] = is_tagged_cache_dir(os.path.join(self._root, folder))
            if hit:
                return folder
        return None

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



CODE_BYTES_ARTIFACT = "code-bytes"


class SnapshotTooLarge(SnapshotError):
    """The pending bytes exceed the cap. Never truncated to fit."""
from probe.sdk.capture.code.content_gate import _ContentGate  # noqa: E402 -- pieces need each other; the front door loads this one first
