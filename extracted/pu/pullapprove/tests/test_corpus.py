"""Golden-master test over real production configs.

Each directory under ``corpus/`` is one repo's current CODEREVIEW config set,
exported verbatim from production (see ``corpus/README.md``). For every repo we
record what the current code does — a clean compile, or the exact error a user
would see — and snapshot it. A change that alters the outcome for any real
config shows up as a snapshot diff, so we can't silently break existing users.

Regenerate snapshots after an intended behavior change:

    cd pullapprove && uv run pytest tests/test_corpus.py --insta update
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pullapprove.config import CONFIG_FILENAME_PREFIX, ConfigModel, ConfigModels
from pydantic import ValidationError
from pytest_insta import SnapshotFixture

CORPUS_DIR = Path(__file__).parent / "corpus"


def _repo_dirs() -> list[Path]:
    if not CORPUS_DIR.exists():
        return []
    return sorted(p for p in CORPUS_DIR.iterdir() if p.is_dir())


def _compile_repo(repo_dir: Path) -> dict[str, Any]:
    """Load and compile a repo's config set, never raising.

    Returns the same structured outcome whether the configs are valid or not,
    so the snapshot captures real current behavior either way.
    """
    try:
        configs = ConfigModels(root={})
        for config_path in sorted(repo_dir.rglob(f"{CONFIG_FILENAME_PREFIX}*")):
            if not config_path.is_file():
                continue
            rel = config_path.relative_to(repo_dir)
            configs.add_config(
                ConfigModel.from_content(config_path.read_text(), rel), rel
            )
        compiled = configs.compiled()
    except (ValidationError, ValueError) as e:
        return {"ok": False, "error": f"{type(e).__name__}: {e}"}

    return {
        "ok": True,
        "compiled": {
            path: model.model_dump(mode="json")
            for path, model in compiled.get_config_models().items()
        },
    }


@pytest.mark.parametrize("repo_dir", _repo_dirs(), ids=lambda p: p.name)
def test_corpus_config_compiles(repo_dir: Path, snapshot: SnapshotFixture) -> None:
    # The repo name is already in the parametrized snapshot path, so pass only
    # the format here to avoid duplicating it in the filename.
    assert snapshot(".json") == _compile_repo(repo_dir)
