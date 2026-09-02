"""Shared loader and fixtures for rederive_deferral_variants tests."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_module():
    """Load scripts/rederive_deferral_variants.py as a module."""
    repo_root = Path(__file__).resolve().parents[3]
    script_path = repo_root / "scripts" / "rederive_deferral_variants.py"
    spec = importlib.util.spec_from_file_location("rederive_deferral_variants", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load rederive_deferral_variants.py from {script_path!s}")
    module = importlib.util.module_from_spec(spec)
    # sys.modules registration is required so that @dataclass can resolve
    # forward references via sys.modules.get(cls.__module__).__dict__.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


rederive = _load_module()


def suppressed_body(*paths: str, declared: int | None = None, posted: int | None = None) -> str:
    """Build a CCR review body declaring and rendering suppressed entries.

    Args:
        paths: One suppressed entry per path.
        declared: Override the declared count so the body under- or
            over-declares relative to what the parser extracts (drives G2).
        posted: When set, the body also self-reports this many posted comments.

    Returns:
        A review body the working-tree parser recognises.
    """
    count = len(paths) if declared is None else declared
    entries = "\n\n".join(f"**`{path}`**\n\n* Something may be wrong here." for path in paths)
    preamble = "" if posted is None else f"Copilot reviewed the changes and generated {posted} comments.\n\n"
    return f"{preamble}### Comments suppressed due to low confidence ({count})\n\n{entries}\n"


def posted_body(count: int) -> str:
    """Build a CCR review body reporting *count* posted comments and no suppressions."""
    return f"Copilot reviewed the changes and generated {count} comments.\n"


def round_(
    *,
    review_id: int = 1,
    body: str = "",
    posted_paths: tuple[str, ...] = (),
    submitted_at: str = "2026-08-01T00:00:00Z",
):
    """Build a Round."""
    return rederive.Round(
        review_id=review_id,
        submitted_at=submitted_at,
        body=body,
        posted_paths=posted_paths,
    )


def record(*rounds, number: int = 1, changed_files: tuple[str, ...] = ("specs/1/spec.md",)):
    """Build a PullRequestRecord from *rounds*."""
    return rederive.PullRequestRecord(number=number, changed_files=changed_files, rounds=tuple(rounds))


def measured(*records):
    """Parse *records* into the (record, metrics) pairs the aggregators consume."""
    return rederive.measure_corpus(records)
