from pathlib import Path

import pytest

from depgather.native import NativeInfer
from depgather.utils import enable_verbose
from tests.utils import assert_eq_packages, assert_in_packages, assert_not_in_packages

THISDIR = Path(__file__).resolve().parent
enable_verbose()


def test_file_not_exists() -> None:
	requirementsPath: Path = THISDIR / "file_does_not_exist.toml"
	with pytest.raises(RuntimeError):
		NativeInfer.gather(
			requirementsPath=requirementsPath,
		)


@pytest.mark.parametrize(
	("lockfile", "extradelta"),
	[
		("poetry.lock", {"pip", "uv", "pygments"}),
		("uv_.lock", {"pip", "uv", "depgather"}),
		("pylock.toml", {"depgather"}),
	],
)
def test_lockfiles(lockfile: str, extradelta: set[str]) -> None:
	"""This takes the minimal lockfiles from the following commands as applied to this library

	The commands to generate these files are as follows:
	uvx poetry lock
	uv export --format pylock.toml > pylock
	uv sync
	"""

	requirementsPath: Path = THISDIR / "data/example1" / lockfile
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)

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

	assert_eq_packages(deps, expected | extradelta)


@pytest.mark.parametrize(
	("sbom"),
	[
		("cyclonedx.json"),
		("spdx.json"),
	],
)
def test_sbom(sbom: str) -> None:
	"""This takes the minimal sbom from as applied to depgather (with the dev group,
	no extras)
	"""

	sbomPath: Path = THISDIR / "data" / sbom

	deps = NativeInfer.gather(
		requirementsPath=sbomPath,
		skipDependencies=set(),
		extras=set(),
		groups={"dev"},
	)

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


@pytest.mark.parametrize(
	("requirements"),
	[
		("requirements.in"),
		("requirements.txt"),
		("pyproject.toml"),
		("poetryv1.toml"),
		# ("setup.py"),
		("setup.cfg"),
	],
)
def test_example1(requirements: str) -> None:
	"""This takes the minimal requirements from as applied to depgather (with the dev group,
	no extras)
	"""

	requirementsPath: Path = THISDIR / "data/example1" / requirements
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
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
		"pygments",  # pygments>=2.7.2; extra == "dev" local; pygments>=2.7.2 in ci/cd
	}

	assert_eq_packages(deps, expected)


@pytest.mark.skip("broken :(")
def test_PEP631() -> None:
	extras: set[str] = {"socks"}
	requirementsPath: Path = THISDIR / "data/pep631_socks.toml"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies=skipDependencies,
		extras=extras,
		groups=set(),
		requirementsPath=requirementsPath,
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


@pytest.mark.skip("broken :(")
def test_requirements() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements.txt"
	skipDependencies: set[str] = {"TOSKIP"}

	deps = NativeInfer.gather(
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
	assert_in_packages(deps, "OPENPYXL")
	assert_not_in_packages(deps, "XARRAY")
	# xarray is an optional dependency of pandas associated with 'computation' key that is not
	# tracked in test_requirements.txt


def test_requirements_with_hashes() -> None:
	requirementsPath: Path = THISDIR / "data/test_requirements_hash.txt"
	skipDependencies = {"TOSKIP"}

	deps = NativeInfer.gather(
		skipDependencies=skipDependencies,
		extras=set(),
		groups=set(),
		requirementsPath=requirementsPath,
	)
	assert_eq_packages(deps, {"PACKAGING"})
	assert_not_in_packages(deps, "TOSKIP")


@pytest.mark.skip("broken :(")
def test_issue_62() -> None:
	requirementsPath = THISDIR / "data/issue/lc_62.toml"

	deps = NativeInfer.gather(
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


@pytest.mark.skip("broken :(")
def test_issue_81() -> None:
	requirementsPath = THISDIR / "data/issue/lc_81.txt"
	deps = NativeInfer.gather(
		skipDependencies=set(), extras=set(), groups=set(), requirementsPath=requirementsPath
	)
	assert_eq_packages(
		deps,
		{
			"aiohttp",
			"aiosignal",
			"annotated-types",
			"anyio",
			"atlassian-python-api",
			"attrs",
			"backoff",
			"beautifulsoup4",
			"bleach",
			"blis",
			"catalogue",
			"certifi",
			"cffi",
			"chardet",
			"charset-normalizer",
			"chevron",
			"click",
			"cloudpathlib",
			"cloudpickle",
			"coloredlogs",
			"confection",
			"cryptography",
			"cupy-cuda12x",
			"cymem",
			"dataclasses-json",
			"dataclasses-json-speakeasy",
			"datasets",
			"defusedxml",
			"deprecated",
			"dill",
			"diskcache",
			"distro",
			"elastic-transport",
			"elasticsearch",
			"emoji",
			"executing",
			"faiss-cpu",
			"fastapi",
			"fastembed",
			"fastjsonschema",
			"fastrlock",
			"filelock",
			"filetype",
			"flashrank",
			"flatbuffers",
			"frozenlist",
			"fsspec",
			"greenlet",
			"grpcio",
			"grpcio-tools",
			"h11",
			"h2",
			"hpack",
			"httpcore",
			"httptools",
			"httpx",
			"huggingface-hub",
			"humanfriendly",
			"hyperframe",
			"idna",
			"iniconfig",
			"interegular",
			"jinja2",
			"jmespath",
			"joblib",
			"jsonpatch",
			"jsonpath-python",
			"jsonpointer",
			"jsonschema",
			"jsonschema-specifications",
			"jupyterlab_pygments",
			"jupyter_client",
			"jupyter_core",
			"langchain",
			"langchain-community",
			"langchain-core",
			"langchain-elasticsearch",
			"langchain-openai",
			"langchain-text-splitters",
			"langcodes",
			"langdetect",
			"langfuse",
			"langsmith",
			"lark",
			"llvmlite",
			"loguru",
			"lxml",
			"markdown",
			"markdownify",
			"markupsafe",
			"marshmallow",
			"mistune",
			"mpmath",
			"msgpack",
			"multidict",
			"multiprocess",
			"murmurhash",
			"mypy-extensions",
			"natsort",
			"nbclient",
			"nbconvert",
			"nbformat",
			"nest-asyncio",
			"networkx",
			"ninja",
			"nltk",
			"numba",
			"numpy",
			"nvidia-cublas-cu12",
			"nvidia-cuda-cupti-cu12",
			"nvidia-cuda-nvrtc-cu12",
			"nvidia-cuda-runtime-cu12",
			"nvidia-cudnn-cu12",
			"nvidia-cufft-cu12",
			"nvidia-curand-cu12",
			"nvidia-cusolver-cu12",
			"nvidia-cusparse-cu12",
			"nvidia-nccl-cu12",
			"nvidia-nvjitlink-cu12",
			"nvidia-nvtx-cu12",
			"oauthlib",
			"onnx",
			"onnxruntime",
			"openai",
			"orjson",
			"outlines",
			"packaging",
			"pandas",
			"pandocfilters",
			"pillow",
			"platformdirs",
			"pluggy",
			"portalocker",
			"preshed",
			"prometheus_client",
			"protobuf",
			"psutil",
			"pyarrow",
			"pyarrow-hotfix",
			"pycparser",
			"pydantic",
			"pydantic_core",
			"pygments",
			"pynvml",
			"pypdf",
			"pytest",
			"python-dateutil",
			"python-dotenv",
			"python-iso639",
			"python-magic",
			"python-multipart",
			"pytz",
			"pyyaml",
			"pyzmq",
			"qdrant-client",
			"rank-bm25",
			"rapidfuzz",
			"ray",
			"referencing",
			"regex",
			"requests",
			"requests-oauthlib",
			"rpds-py",
			"safetensors",
			"scikit-learn",
			"scipy",
			"sentence-transformers",
			"sentencepiece",
			"six",
			"slack-log-handler",
			"smart-open",
			"sniffio",
			"soupsieve",
			"spacy",
			"spacy-legacy",
			"spacy-loggers",
			"sqlalchemy",
			"srsly",
			"starlette",
			"sympy",
			"tabulate",
			"tenacity",
			"thinc",
			"threadpoolctl",
			"tiktoken",
			"tinycss2",
			"tokenizers",
			"torch",
			"tornado",
			"tqdm",
			"traitlets",
			"transformers",
			"triton",
			"typer",
			"typing-inspect",
			"typing_extensions",
			"tzdata",
			"unstructured",
			"unstructured-client",
			"urllib3",
			"uvicorn",
			"uvloop",
			"wasabi",
			"watchfiles",
			"weasel",
			"webencodings",
			"websockets",
			"wrapt",
			"xformers",
			"xxhash",
			"yarl",
		},
	)

	#     RuntimeError:    No solution found when resolving dependencies:
	#        Because nvidia-cudnn-cu12==8.9.2.26 has no wheels with a matching
	#           platform tag and you require nvidia-cudnn-cu12==8.9.2.26, we can
	#           conclude that your requirements are unsatisfiable.


@pytest.mark.skip("broken :(")
def test_issue_84() -> None:
	requirementsPath = THISDIR / "data/issue/lc_84.txt"

	deps = NativeInfer.gather(
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
