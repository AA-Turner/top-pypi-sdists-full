"""Filesystem paths Efterlev uses — vendored catalogs + workspace output dirs.

Two distinct concerns live in this module:

1. **Vendored catalog resolution** (FRMR + NIST 800-53): catalogs ship
   inside the wheel and are resolved at runtime via `vendored_catalogs_dir()`.
   `EXPECTED_HASHES` mirrors the provenance table in `catalogs/README.md`;
   `verify_catalog_hashes` enforces it.

2. **Workspace output directories** (v0.1.160 / #365): the visible-vs-hidden
   split. Customer-facing artifacts (reports, POA&M, OSCAL, submission
   zips) write to `<workspace>/efterlev-out/` so they're discoverable.
   Internal state (cache, store, llm-cache, receipts.log, config.toml,
   redactions, customer-authored manifests) stays under the hidden
   `<workspace>/.efterlev/` directory.

   Use `reports_dir()`, `submissions_dir()`, `poam_dir()`, `oscal_dir()`,
   `internal_root()` everywhere instead of constructing paths inline.
   The legacy read-only helpers (`legacy_reports_dir`,
   `legacy_submissions_dir`) and the iterators (`iter_report_dirs`,
   `iter_submission_dirs`) let readers surface pre-v0.1.160 artifacts
   on upgraded workspaces without forcing a manual `mv`.
"""

from __future__ import annotations

import hashlib
import os
from importlib.resources import files
from pathlib import Path

from efterlev.errors import CatalogLoadError

# Per catalogs/README.md provenance table (2026-04-19). Update here when bumped.
EXPECTED_HASHES: dict[str, str] = {
    "frmr/FRMR.documentation.json": (
        "bbb734e9acb5a7ad48dafd6b2f442178f2b507c78c46b897cc4b1852c746c7c4"
    ),
    "frmr/FRMR.md": ("43aa72808f63d5e49055f47434ee273654cb09fe80b0e5eb02401a02dc9f1e8d"),
    "frmr/FedRAMP.schema.json": (
        "1301497c55c6c188b8ba6c1236dc2d7c73286b55dc2ca5e6013ad38f0ba75f0c"
    ),
    "nist/NIST_SP-800-53_rev5_catalog.json": (
        "1645df6a370dcb931db2e2d5d70c2f77bc89c38499a416c23a70eb2c0e595bcc"
    ),
}

_MARKER = "frmr/FRMR.documentation.json"


def _contains_marker(candidate: Path) -> bool:
    return (candidate / _MARKER).is_file()


def vendored_catalogs_dir() -> Path:
    """Return the directory containing the vendored FRMR + NIST catalogs.

    Raises `CatalogLoadError` if no candidate location contains a recognizable
    FRMR file. Callers should treat this as a configuration / packaging error
    and instruct the user to reinstall or set `EFTERLEV_CATALOGS_DIR`.
    """
    override = os.environ.get("EFTERLEV_CATALOGS_DIR")
    if override:
        path = Path(override).resolve()
        if _contains_marker(path):
            return path
        raise CatalogLoadError(f"EFTERLEV_CATALOGS_DIR={override!r} does not contain {_MARKER}")

    # Dev / editable install: walk up from this module looking for repo-root catalogs/.
    current = Path(__file__).resolve().parent
    for parent in [*current.parents]:
        candidate = parent / "catalogs"
        if _contains_marker(candidate):
            return candidate

    # Wheel install: force-included under the package.
    try:
        packaged = Path(str(files("efterlev") / "catalogs"))
        if _contains_marker(packaged):
            return packaged
    except (ModuleNotFoundError, FileNotFoundError):
        pass

    raise CatalogLoadError(
        "cannot locate vendored catalogs/. Reinstall Efterlev or set "
        "EFTERLEV_CATALOGS_DIR to the directory holding frmr/ and nist/."
    )


def resolve_within_root(candidate: Path, root: Path) -> Path | None:
    """Resolve `candidate` against `root`, rejecting any path that escapes it.

    Used by the Remediation Agent / CLI to safely read `.tf` files referenced
    by `Evidence.source_ref.file`. Evidence could in principle contain a
    traversal payload (`../../../etc/passwd`) — a malicious detector, a
    corrupted store, or a hand-edited blob could smuggle one in. This helper
    joins `candidate` onto `root`, fully resolves symlinks, and verifies the
    result is still under the resolved `root`. Returns the resolved path on
    success, `None` on any attempted escape.

    `candidate` may be absolute or relative. Both are treated the same way:
    resolve against `root`, then check containment. In the post-2026-04-22
    path-hardening pass, detectors and the manifest loader record
    repo-relative paths in `Evidence.source_ref.file` specifically so this
    helper's job is trivial: `root / rel_path`, resolved. Absolute paths are
    still accepted (for back-compat with legacy Evidence records that may
    predate the hardening, and for single-file test callers that pass
    absolute paths) — containment is the real safety check. Absolute paths
    outside `root` (`/etc/passwd`, `../../../secrets`) still fail
    containment and are rejected.
    """
    resolved_root = root.resolve()
    try:
        # When `candidate` is absolute, `resolved_root / candidate` ignores
        # `resolved_root` and yields `candidate`. When it's relative, the
        # two are joined. Both paths then go through `.resolve()` to
        # normalize symlinks and `..` segments before the containment check.
        full = (resolved_root / candidate).resolve()
        # relative_to raises ValueError if `full` isn't under `resolved_root`.
        full.relative_to(resolved_root)
    except (OSError, ValueError):
        return None
    return full


# --- Workspace output directories (v0.1.160 / #365) ----------------------

_OUTPUT_DIR_NAME = "efterlev-out"
_INTERNAL_DIR_NAME = ".efterlev"


def _resolve_profile_subdir(profile: str | None) -> str:
    """Return the profile-scoped output-subdir segment.

    v0.1.166 / #371: when no profile is provided, fall back to the
    `EFTERLEV_PROFILE` env var so callers don't have to thread the
    profile name through every call site. Returns the empty string
    when no profile is active — output paths stay at today's
    backward-compatible default.
    """
    from efterlev.profile import get_active_profile, profile_output_subdir

    effective = profile if profile is not None else get_active_profile()
    return profile_output_subdir(effective)


def output_root(workspace_root: Path, profile: str | None = None) -> Path:
    """Return the customer-facing output root.

    v0.1.160+: `<workspace>/efterlev-out/`.
    v0.1.166+: when a profile is active (explicit `profile=` arg OR
    `EFTERLEV_PROFILE` env var set), output scopes to
    `<workspace>/efterlev-out/profile-<name>/` so prod and staging
    reports don't overwrite each other.
    """
    subdir = _resolve_profile_subdir(profile)
    base = workspace_root / _OUTPUT_DIR_NAME
    return base / subdir if subdir else base


def reports_dir(workspace_root: Path, profile: str | None = None) -> Path:
    """Where Efterlev WRITES report artifacts (HTML + JSON sidecars,
    FRMR attestations, scan output, scan-diff output). Profile-scoped
    when a profile is active (v0.1.166+).
    """
    return output_root(workspace_root, profile) / "reports"


def submissions_dir(workspace_root: Path, profile: str | None = None) -> Path:
    """Where `efterlev submission package` writes the bundled zip.
    Profile-scoped when a profile is active (v0.1.166+).
    """
    return output_root(workspace_root, profile) / "submissions"


def poam_dir(workspace_root: Path, profile: str | None = None) -> Path:
    """Markdown POA&M output directory. Profile-scoped (v0.1.166+)."""
    return reports_dir(workspace_root, profile) / "poam"


def oscal_dir(workspace_root: Path, profile: str | None = None) -> Path:
    """OSCAL POA&M + Component-Definition output directory.
    Profile-scoped (v0.1.166+)."""
    return reports_dir(workspace_root, profile) / "oscal"


def vdr_dir(workspace_root: Path, profile: str | None = None) -> Path:
    """Vulnerability Detection & Response report output directory
    (v0.1.162 / #367; RFC-0012-shaped). Profile-scoped (v0.1.166+).
    """
    return reports_dir(workspace_root, profile) / "vdr"


def inventory_dir(workspace_root: Path, profile: str | None = None) -> Path:
    """Consolidated resource inventory output directory (v0.1.164 /
    #369; RFC-0017 artifact). Profile-scoped (v0.1.166+).
    """
    return reports_dir(workspace_root, profile) / "inventory"


def internal_root(workspace_root: Path) -> Path:
    """Hidden internal-state root (`<workspace>/.efterlev/`).

    Cache, content-addressed store, LLM cache, receipts log, config.toml,
    redactions, and customer-authored manifests live here. Customers
    don't normally browse this directory.
    """
    return workspace_root / _INTERNAL_DIR_NAME


def legacy_reports_dir(workspace_root: Path) -> Path:
    """Pre-v0.1.160 reports location (`<workspace>/.efterlev/reports/`).

    Read-only on v0.1.160+. New writes always land in `reports_dir`.
    Customers with pre-v0.1.160 history on disk can still find their
    old reports here, and `iter_report_dirs` surfaces them when
    callers want a unified "latest of all known artifacts" view.
    """
    return internal_root(workspace_root) / "reports"


def legacy_submissions_dir(workspace_root: Path) -> Path:
    """Pre-v0.1.160 submission location. Read-only on v0.1.160+."""
    return internal_root(workspace_root) / "submissions"


def iter_report_dirs(workspace_root: Path) -> list[Path]:
    """Return all directories that may hold report artifacts, in NEW-first
    then LEGACY order, profile-aware (v0.1.166+).

    When a profile is active, the profile-scoped directory is FIRST
    (where new writes land), then the top-level reports dir as a
    backstop (for artifacts from before the profile was active), then
    the legacy pre-v0.1.160 location. Callers globbing by mtime
    naturally land on the newest match across all three.
    """
    # The active-profile-aware reports dir comes first; new writes land there.
    dirs: list[Path] = [reports_dir(workspace_root)]
    # When a profile is active, also include the un-profiled default
    # location so artifacts written BEFORE the profile was active still
    # surface in readers. Then the pre-v0.1.160 legacy hidden dir.
    from efterlev.profile import get_active_profile

    if get_active_profile() is not None:
        unprofiled = workspace_root / _OUTPUT_DIR_NAME / "reports"
        if unprofiled not in dirs:
            dirs.append(unprofiled)
    dirs.append(legacy_reports_dir(workspace_root))
    return dirs


def iter_submission_dirs(workspace_root: Path) -> list[Path]:
    """Counterpart to `iter_report_dirs` for submission packages.
    Profile-aware (v0.1.166+).
    """
    dirs: list[Path] = [submissions_dir(workspace_root)]
    from efterlev.profile import get_active_profile

    if get_active_profile() is not None:
        unprofiled = workspace_root / _OUTPUT_DIR_NAME / "submissions"
        if unprofiled not in dirs:
            dirs.append(unprofiled)
    dirs.append(legacy_submissions_dir(workspace_root))
    return dirs


def verify_catalog_hashes(catalogs_dir: Path) -> None:
    """Hash every file named in EXPECTED_HASHES under `catalogs_dir`.

    Raises `CatalogLoadError` on the first mismatch or missing file. On
    success, returns None — callers interpret that as "every vendored file is
    exactly the bytes we pinned."
    """
    for rel, expected in EXPECTED_HASHES.items():
        path = catalogs_dir / rel
        if not path.is_file():
            raise CatalogLoadError(f"vendored catalog file missing: {path}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise CatalogLoadError(
                f"SHA-256 mismatch for {rel}: expected {expected}, got {actual}. "
                "Either the vendored file was tampered with, or the expected "
                "hash in src/efterlev/paths.py is out of date (check against "
                "catalogs/README.md)."
            )
