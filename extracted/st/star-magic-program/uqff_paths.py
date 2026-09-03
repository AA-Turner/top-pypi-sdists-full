"""uqff_paths - THE FRONT DOOR's foundation (v0.412.0): one stable API that
locates the Star-Magic corpus on every install layout, so nothing in the
package ever depends on "run it from the repo."

Layouts resolved, in order:
  1. REPO / source checkout: everything sits beside this module.
  2. INSTALLED (venv / system): modules in site-packages, the full repo
     mirror under <prefix>/share/star-magic-program (the wheel carries the
     COMPLETE repository as data-files - Daniel's full-wheel rule).
  3. pip --target FLATTENED: share/star-magic-program under the target root.

Daniel's lock (2026-09-01): the fidelity gate must resolve via this module
and pass from site-packages. data_root() is that resolution; the gate
chdir()s to it at bootstrap, which makes every one of its relative reads
correct on every layout without rewriting a 1.3 MB test file.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_SENTINELS = ("UNIFIED_REGISTRY.csv", "WHITEPAPER_INDEX.md", "uqff_calculator.py")


def _is_root(p: Path) -> bool:
    try:
        return all((p / s).exists() for s in _SENTINELS)
    except OSError:
        return False


def data_root() -> Path:
    """The directory containing the complete corpus (repo or installed mirror)."""
    here = Path(__file__).resolve().parent
    candidates = [
        here,                                             # repo checkout
        here / "share" / "star-magic-program",            # pip --target flatten
        here.parent / "share" / "star-magic-program",     # target/site adjacent
        here.parent.parent / "share" / "star-magic-program",
        here.parent.parent.parent / "share" / "star-magic-program",  # venv: site-packages -> prefix
        Path(sys.prefix) / "share" / "star-magic-program",
        Path(sys.exec_prefix) / "share" / "star-magic-program",
        Path(os.environ.get("STAR_MAGIC_DATA_ROOT", "/nonexistent")),
    ]
    try:
        import site
        for sp in (site.getuserbase(), *site.PREFIXES):
            candidates.append(Path(sp) / "share" / "star-magic-program")
    except Exception:
        pass
    for c in candidates:
        if _is_root(c):
            return c
    raise FileNotFoundError(
        "star-magic corpus not found on this layout; searched: "
        + "; ".join(str(c) for c in candidates)
        + " - set STAR_MAGIC_DATA_ROOT to the directory holding "
        + ", ".join(_SENTINELS))


def resolve(relpath: str) -> Path:
    """Absolute path of any published file, on any layout."""
    return data_root() / relpath


def corpus() -> Path:
    """The whitepapers directory (2,303 files)."""
    return resolve("whitepapers")


def registry() -> Path:
    return resolve("UNIFIED_REGISTRY.csv")


def results_table() -> Path:
    return resolve("UNIFIED_REGISTRY_RESULTS_TABLE.csv")
