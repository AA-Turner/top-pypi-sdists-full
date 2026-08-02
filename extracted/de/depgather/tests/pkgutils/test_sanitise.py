from pathlib import Path

import pytest

from depgather.utils import sanitize


def test_sanitize_valid(tmp_path: Path) -> None:
	f = tmp_path / "reqs.txt"
	f.write_text("requests>=2.0")

	sanitize(
		requirementsPath=f,
		skipDependencies=["requests"],
		groups=["dev"],
		extras=["cli"],
		base_index_url="https://pypi.org",
	)


@pytest.mark.parametrize(
	"suffix",
	[".exe", ".bin", ".md", ".yaml"],
)
def test_sanitize_invalid_suffix(tmp_path: Path, suffix: str) -> None:
	f = tmp_path / f"reqs{suffix}"
	f.write_text("requests")

	with pytest.raises(RuntimeError, match="unsupported requirements file type"):
		sanitize(f)


@pytest.mark.parametrize(
	"bad_value",
	["bad name", "bad$name", "bad;name", "--evil"],
)
def test_sanitize_invalid_name(tmp_path: Path, bad_value: str) -> None:
	f = tmp_path / "reqs.txt"
	f.write_text("requests")

	with pytest.raises(RuntimeError, match="invalid name"):
		sanitize(
			f,
			skipDependencies=[bad_value],
		)


@pytest.mark.parametrize(
	"bad_value",
	[None, 123, 1.5, object()],
)
def test_sanitize_non_string(tmp_path: Path, bad_value: str) -> None:
	f = tmp_path / "reqs.txt"
	f.write_text("requests")

	with pytest.raises(RuntimeError, match="expected str"):
		sanitize(
			f,
			groups=[bad_value],
		)


@pytest.mark.parametrize(
	"url",
	[
		"ftp://pypi.org",
		"not-a-url",
		"https://",
	],
)
def test_sanitize_invalid_index_url(tmp_path: Path, url: str) -> None:
	f = tmp_path / "reqs.txt"
	f.write_text("requests")

	with pytest.raises(RuntimeError, match="invalid|HTTP"):
		sanitize(f, base_index_url=url)
