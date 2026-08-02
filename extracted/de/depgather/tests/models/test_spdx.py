from pathlib import Path

import pytest

from depgather.models.spdx import SPDX

THISDIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
	"src",
	[
		"empty.json",
		"spdx.json",
	],
)
def test_model_validate(src: str) -> None:
	SPDX.model_validate_json((THISDIR / "data" / src).read_bytes())
