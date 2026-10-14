"""The packaged fixture people: minted, clearly fake people a clone seeds and a story may name."""

from __future__ import annotations

from pathlib import Path

from plato.personas.models import FixturePool

POOL_PATH = Path(__file__).parent / "fixture_people.json"


def load_pool(path: str | Path | None = None) -> FixturePool:
    """The fixture pool at ``path``, or the packaged one."""
    return FixturePool.model_validate_json(Path(path or POOL_PATH).read_text())
