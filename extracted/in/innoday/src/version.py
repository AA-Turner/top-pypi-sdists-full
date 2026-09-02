"""
Version information for InnoDay platform.

MAJOR/MINOR below are edited by hand -- bump MINOR for a real feature
milestone, MAJOR for a breaking change; both are otherwise frozen. Every
merge to main is treated as a patch release: PATCH is never hardcoded
here. It's computed by counting existing `v{MAJOR}.{MINOR}.*` git tags, so
CI never needs to commit this file back to main (which is what broke once
branch protection started requiring PRs -- see
.github/workflows/version-bump.yml).

Reset history: the old scheme bumped MINOR on every merge and had reached
0.110.0-beta. Switched to computed-PATCH starting at 0.111.0-beta --
MINOR bumped to 111 specifically so this sorts ABOVE every prior release
under real PEP 440 ordering. A first attempt reset to 0.0.* instead (with
a _PATCH_BASELINE offset to preserve the release count) shipped two real
releases (0.0.111b0, 0.0.112b0) before this was caught: 0.0.112b0 sorts
BELOW 0.110.0b0, since 0 < 110 in the minor slot -- confirmed via
`pip index versions`, which kept reporting 0.110.0b0 as latest even with
0.0.112b0 present in the index.

Second reset: the project owner deleted the old 0.2.0-beta through
0.111.10-beta GitHub Releases/tags. The PyPI releases themselves
(0.100.0b0 through 0.111.10b0) were NOT yanked at first, though. Reset to
0.1.0-beta assuming they had been yanked; this was wrong.
`scripts/verify_pypi_latest.py` (added in #290) caught it for real on the
very first release under this reset (0.1.3-beta, 2026-07-11): PyPI kept
resolving "latest" as 0.111.10b0, not the just-published release, since
0.111.10b0 numerically outranks anything in the 0.1.x line under real PEP
440 ordering.

A stopgap MINOR bump to 112 briefly landed (#293) to outrank the un-yanked
releases without touching PyPI. The project owner then yanked the actual
offending releases (0.100.0b0 through 0.112.0b0) on pypi.org directly --
the fix verify_pypi_latest.py's own failure message names as preferred --
so MINOR reverts back to 1 here (#doc-revert-293). Yanked releases are
excluded from PyPI's "latest" resolution, so 0.1.x now sorts correctly as
the newest version with no MINOR inflation needed.

When running from an installed distribution (no .git directory -- the
normal case for anyone who `pip install`s or `uvx`s this package),
PATCH/__version__ instead come from the version setuptools baked into the
wheel at build time (importlib.metadata), which was itself computed the
same way, at build time, when the builder's checkout still had .git.
"""

import os
import subprocess
from functools import lru_cache
from pathlib import Path

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_SUFFIX = "-beta"

_REPO_ROOT = Path(__file__).resolve().parent.parent

# Where the container build persists the computed version (see Dockerfile), and
# an env var that overrides it. These are the ONLY version sources that survive
# into a deployed container: the image ships neither .git (so _computed_patch()
# sees zero tags -> 0.1.0b0) nor installed distribution metadata (uv sync
# installs from source in the image, not a pre-built wheel with a baked
# version). The Dockerfile computes the real version from the build-context
# checkout's git tags at build time and writes it to _BAKED_VERSION_FILE, so
# get_version() has an authoritative value with no runtime dependency on .git or
# Railway's clone depth. INNODAY_VERSION lets a caller/CI override at runtime.
_VERSION_ENV_VAR = "INNODAY_VERSION"
_BAKED_VERSION_FILE = _REPO_ROOT / ".innoday_version"


def _baked_version() -> str:
    """Version written into the image at build time, if present (see Dockerfile)."""
    try:
        return _BAKED_VERSION_FILE.read_text().strip()
    except OSError:
        return ""


@lru_cache(maxsize=1)
def _computed_patch() -> int:
    """Count existing v{MAJOR}.{MINOR}.* tags to derive this release's patch.

    Returns 0 when no v{MAJOR}.{MINOR}.* tags exist yet -- the first
    release after a manual MAJOR/MINOR bump starts fresh, matching how the
    old auto-bump always reset PATCH to 0 on a MINOR change.
    """
    if not (_REPO_ROOT / ".git").exists():
        return 0
    prefix = f"v{VERSION_MAJOR}.{VERSION_MINOR}."
    try:
        result = subprocess.run(
            ["git", "tag", "--list", f"{prefix}*"],
            cwd=_REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5,
        )
        tags = [t for t in result.stdout.splitlines() if t.strip()]
        return len(tags)
    except (subprocess.SubprocessError, OSError):
        return 0


def _installed_version() -> str:
    """Version setuptools baked into the wheel at build time, if installed."""
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("innoday")
    except PackageNotFoundError:
        return ""


def compute_version_from_tags() -> str:
    """Compute the version live from git tags, ignoring any installed
    distribution metadata.

    This is the authoritative source at release time -- version-bump.yml
    uses this (not get_version()) to decide what to tag/build/publish,
    since the workflow's own checkout always has .git and the live tag
    count IS the thing being decided, not something to read back from a
    stale editable install. Also always uses VERSION_SUFFIX's exact
    "-beta" spelling, never PEP 440's normalized "b0" -- so every tag this
    repo creates stays in one consistent format for _computed_patch's
    prefix matching to keep working correctly release after release.
    """
    return f"{VERSION_MAJOR}.{VERSION_MINOR}.{_computed_patch()}{VERSION_SUFFIX}"


def get_version() -> str:
    """Get the full version string.

    Resolution order, highest priority first:

    1. The INNODAY_VERSION env var -- a runtime override (e.g. CI or an operator
       pinning a value explicitly).
    2. The .innoday_version file baked into the image at build time by the
       Dockerfile from the build-context checkout's git tags. This is the source
       that makes a deployed container report correctly: inside the image there
       is no .git and no installed distribution metadata, so the two fallbacks
       below both resolve to the 0.1.0b0 first-release stub there.
    3. The version baked into an installed distribution's metadata (the correct
       source of truth for anything installed via pip/uvx).
    4. Computed live from git tags -- for a dev checkout with none of the above
       (e.g. `uv run` against a fresh clone).

    Not used by version-bump.yml itself -- see compute_version_from_tags().
    """
    override = os.environ.get(_VERSION_ENV_VAR, "").strip()
    if override:
        return override
    baked = _baked_version()
    if baked:
        return baked
    installed = _installed_version()
    if installed:
        return installed
    return compute_version_from_tags()


__version__ = "0.1.337-beta"  # frozen for this CI build only, never committed


def get_display_version() -> str:
    """Get a user-friendly version string for display."""
    return f"v{get_version()}"


def get_version_info() -> dict:
    """Get detailed version information."""
    full = get_version()
    parts = full.split("-", 1)
    numeric = parts[0]
    suffix = parts[1] if len(parts) > 1 else None
    major, minor, patch = (int(p) for p in numeric.split("."))
    return {
        "major": major,
        "minor": minor,
        "patch": patch,
        "suffix": suffix,
        "full": full,
        "display": get_display_version(),
    }
