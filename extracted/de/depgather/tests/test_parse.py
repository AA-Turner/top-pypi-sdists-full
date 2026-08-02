from pathlib import Path
from unittest.mock import MagicMock

import pytest

from depgather.native import NativeInfer
from depgather.parse import ResolverName, gather
from depgather.utils import enable_verbose
from tests.utils import assert_eq_packages

THISDIR = Path(__file__).resolve().parent
enable_verbose()


def test_file_not_exists() -> None:
	requirementsPath: Path = THISDIR / "file_does_not_exist.toml"
	with pytest.raises(RuntimeError):
		gather(
			requirementsPath=requirementsPath,
		)


@pytest.mark.parametrize(
	("resolvername"),
	[
		(ResolverName.NATIVE),
		(ResolverName.UV),
		(ResolverName.PIP),
	],
)
def test_lockfiles(resolvername: ResolverName) -> None:
	requirementsPath: Path = THISDIR / "data/example1" / "pylock.toml"
	skipDependencies: set[str] = {"TOSKIP"}

	gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
		preferred_resolver=resolvername,
	)


@pytest.mark.parametrize(
	("lockfile", "extradelta"),
	[
		("poetry.lock", {"pip", "uv", "pygments"}),
		("uv_.lock", {"pip", "uv", "depgather"}),
		("pylock.toml", {"depgather"}),
	],
)
def test_lockfiles_fav_uv(
	monkeypatch: pytest.MonkeyPatch, lockfile: str, extradelta: set[str]
) -> None:
	"""This takes the minimal lockfiles from the following commands as applied to this library

	The commands to generate these files are as follows:
	uvx poetry lock
	uv export --format pylock.toml > pylock
	uv sync
	"""

	mock = MagicMock(wraps=NativeInfer.gather)

	monkeypatch.setattr(
		NativeInfer,
		"gather",
		mock,
	)

	requirementsPath: Path = THISDIR / "data/example1" / lockfile
	skipDependencies: set[str] = {"TOSKIP"}

	deps = gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
		preferred_resolver=ResolverName.UV,
	)

	mock.assert_called_once()

	expected = {
		"basedpyright",
		"colorama",
		"coverage",
		"iniconfig",
		"nodejs-wheel-binaries",
		"packaging",
		"pluggy",
		"pytest",
		"requirements-parser",
		"ruff",
		"tomli",
	}

	assert len(deps) == len(expected) + len(extradelta)

	# assert depgather.native.NativeInfer.gather( called

	assert_eq_packages(deps, expected | extradelta)


@pytest.mark.parametrize(
	("sbom"),
	[
		("cyclonedx.json"),
		("spdx.json"),
	],
)
def test_sbom_fav_uv(monkeypatch: pytest.MonkeyPatch, sbom: str) -> None:
	"""This takes the minimal sbom from as applied to depgather (with the dev group,
	no extras)
	"""

	mock = MagicMock(wraps=NativeInfer.gather)

	monkeypatch.setattr(
		NativeInfer,
		"gather",
		mock,
	)
	sbomPath: Path = THISDIR / "data" / sbom

	deps = gather(
		requirementsPath=sbomPath,
		skipDependencies=set(),
		extras=set(),
		groups={"dev"},
		preferred_resolver=ResolverName.UV,
	)

	mock.assert_called_once()

	expected = {
		"basedpyright",
		"colorama",  # windows only requirement
		"coverage",
		"iniconfig",
		"nodejs-wheel-binaries",
		"packaging",
		"pluggy",
		"pytest",
		"requirements-parser",
		"ruff",
		"tomli",
		"loguru",
		"win32-setctime",
	}

	assert_eq_packages(deps, expected)
