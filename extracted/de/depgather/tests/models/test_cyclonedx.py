from pathlib import Path

import pytest

from depgather.models.cyclonedx import Bom

THISDIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
	"src",
	[
		"empty.json",
		"cyclonedx.json",
	],
)
def test_model_validate(src: str) -> None:
	Bom.model_validate_json((THISDIR / "data" / src).read_bytes())
