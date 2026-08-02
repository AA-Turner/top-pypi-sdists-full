import contextlib
from pathlib import Path

import pytest

from depgather.uv_cli import UvCli
from tests.utils import assert_eq_packages, assert_in_packages, assert_not_in_packages

THISDIR = Path(__file__).resolve().parent


def test_file_not_exists() -> None:
	requirementsPath: Path = THISDIR / "file_does_not_exist.toml"
	with pytest.raises(RuntimeError):
		UvCli.gather(
			requirementsPath=requirementsPath,
		)


@pytest.mark.parametrize(
	("lockfile"),
	[
		("poetry.lock"),
		("uv_.lock"),
		("pylock.toml"),
	],
)
def test_lockfiles(lockfile: str) -> None:
	"""This takes the minimal lockfiles from the following commands as applied to this library.

	The commands to generate these files are as follows:
	uvx poetry lock
	uv export --format pylock.toml > pylock
	uv sync
	"""

	requirementsPath: Path = THISDIR / "data/example1" / lockfile
	skipDependencies: set[str] = {"TOSKIP"}

	with pytest.raises(RuntimeError, match="lock files, and sboms are not supported"):
		UvCli.gather(
			skipDependencies=skipDependencies,
			extras=set(),
			groups=set(),
			requirementsPath=requirementsPath,
		)


@pytest.mark.parametrize(
	("requirements"),
	[
		("requirements.in"),
		("requirements.txt"),
		("pyproject.toml"),
		("poetryv1.toml"),
		("setup.py"),
		("setup.cfg"),
	],
)
def test_example1(requirements: str) -> None:
	"""This takes the minumal requirements from as applied to depgather (with the dev group,
	no extras)
	"""

	requirementsPath: Path = THISDIR / "data/example1" / requirements
	skipDependencies: set[str] = {"TOSKIP"}

	deps = UvCli.gather(
		requirementsPath=requirementsPath,
		skipDependencies=skipDependencies,
		extras=set(),
		groups={"dev"},
	)

	expected = {
		"basedpyright",
		# "colorama", # windows only requirement
		"coverage",
		"iniconfig",
		"nodejs-wheel-binaries",
		"packaging",
		"pluggy",
		"pytest",
		"requirements-parser",
		"ruff",
		"tomli",
		"pygments",  # seems inconsistent with my own uv.lock ?
	}

	assert len(deps) == len(expected)
	assert_eq_packages(deps, expected)


def test_PEP631() -> None:
	extras: set[str] = {"socks"}
	requirementsPath: Path = THISDIR / "data/pep631_socks.toml"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = UvCli.gather(
		requirementsPath=requirementsPath,
		skipDependencies=skipDependencies,
		extras=extras,
		groups=set(),
	)

	assert_eq_packages(
		deps,
		{
			"dockerpty",
			"attrs",
			"jsonschema",
			"pyyaml",
			"pysocks",
			"certifi",
			"docker",
			"texttable",
			"docopt",
			"paramiko",
			"idna",
			"cached-property",
			"distro",
			"charset-normalizer",
			"urllib3",
			"websocket-client",
			"requests",
			"python-dotenv",
			"cffi",
			"pynacl",
			"bcrypt",
			"six",
			"pycparser",
			"cryptography",
			"pyrsistent",
			"setuptools",
			"invoke",
		},
	)


def test_requirements() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements.txt"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = UvCli.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)

	assert_eq_packages(
		deps,
		{
			"numpy",
			"odfpy",
			"openpyxl",
			"pandas",
			"six",
			"defusedxml",
			"et-xmlfile",
			"python-dateutil",
			"pytz",
			"pyxlsb",
			"tzdata",
			"xlrd",
			"xlsxwriter",
		},
	)
	assert_in_packages(deps, "openpyxl")
	assert_not_in_packages(deps, "xarray")
	# xarray is an optional dependency of pandas associated with 'computation' key that is not
	# tracked in test_requirements.txt


def test_requirements_with_hashes() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements_hash.txt"
	skipDependencies = {"TOSKIP"}

	deps = UvCli.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)
	assert_eq_packages(deps, {"packaging"})
	assert_not_in_packages(deps, "toskip")


def test_issue_62() -> None:
	requirementsPath = THISDIR / "data/issue/lc_62.toml"

	deps = UvCli.gather(
		skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
	)

	assert_not_in_packages(deps, "PYQT5")

	assert_eq_packages(
		deps,
		{
			"certifi",
			"charset-normalizer",
			"deprecated",
			"earthengine-api",
			"google-api-core",
			"google-api-python-client",
			"google-auth",
			"google-auth-httplib2",
			"google-cloud-core",
			"google-cloud-storage",
			"google-crc32c",
			"google-resumable-media",
			"googleapis-common-protos",
			"httplib2",
			"idna",
			"numpy",
			"pandas",
			"proto-plus",
			"protobuf",
			"pyarrow",
			"pyasn1",
			"pyasn1-modules",
			"pyparsing",
			"python-dateutil",
			"pytz",
			"requests",
			"six",
			"uritemplate",
			"urllib3",
			"wrapt",
			"cffi",
			"cryptography",
			"pycparser",
		},
	)


def test_issue_81() -> None:
	requirementsPath = THISDIR / "data/issue/lc_81.txt"
	with contextlib.suppress(Exception):
		_deps = UvCli.gather(
			skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
		)

	#     RuntimeError:    No solution found when resolving dependencies:
	#        Because nvidia-cudnn-cu12==8.9.2.26 has no wheels with a matching
	#           platform tag and you require nvidia-cudnn-cu12==8.9.2.26, we can
	#           conclude that your requirements are unsatisfiable.


def test_issue_84() -> None:
	requirementsPath = THISDIR / "data/issue/lc_84.txt"

	deps = UvCli.gather(
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
			"packaging",
		},
	)
