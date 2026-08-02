from pathlib import Path

import pytest

from depgather.models.pypijson import ProjectResponse

THISDIR = Path(__file__).resolve().parent


@pytest.mark.parametrize(
	"src",
	[
		"empty.json",
		"example.json",
		"example_version.json",
		"invalid_url.json",
		"requests.json",
	],
)
def test_model_validate(src: str) -> None:
	ProjectResponse.model_validate_json((THISDIR / "data" / src).read_bytes())


def test_model_invalid_url() -> None:
	resp = ProjectResponse.model_validate_json((THISDIR / "data/invalid_url.json").read_bytes())
	assert resp.info.bugtrack_url.host == "example.invalid"
	assert resp.info.package_url.host == "example.invalid"
