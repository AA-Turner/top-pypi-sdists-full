from pathlib import Path

import pytest

from depgather.pip_cli import PipResolver
from tests.utils import assert_eq_packages, assert_not_in_packages

THISDIR = Path(__file__).resolve().parent


def test_file_not_exists() -> None:
	requirementsPath: Path = THISDIR / "file_does_not_exist.toml"
	with pytest.raises(RuntimeError):
		PipResolver.gather(
			requirementsPath=requirementsPath,
		)


def test_requirements() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements.txt"
	skipDependencies: set[str] = {"TOSKIP"}

	# note: This error originates from a subprocess, and is likely not a problem with pip.
	# ERROR: Failed to build 'pandas' when getting requirements to build wheel
	with pytest.raises(RuntimeError, match="error: subprocess-exited-with-error"):
		PipResolver.gather(
			skipDependencies=skipDependencies,
			extras=set(),
			groups=set(),
			requirementsPath=requirementsPath,
		)


def test_requirements_with_hashes() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements_hash.txt"
	skipDependencies = {"TOSKIP"}

	deps = PipResolver.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)
	assert_eq_packages(deps, {"PACKAGING"})
	assert_not_in_packages(deps, "TOSKIP")


def test_issue_84() -> None:
	requirementsPath = THISDIR / "data/issue/lc_84.txt"

	deps = PipResolver.gather(
		skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
	)

	assert_eq_packages(
		deps,
		{
			"amqp",
			"billiard",
			"celery",
			"click",
			"click-didyoumean",
			"click-plugins",
			"click-repl",
			"kombu",
			"prompt-toolkit",
			"pytz",
			"tzdata",
			"vine",
			"wcwidth",
			# "packaging", # not present locally
		},
	)
