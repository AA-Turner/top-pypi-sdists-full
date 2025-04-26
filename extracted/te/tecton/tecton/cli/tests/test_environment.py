import os
from dataclasses import dataclass
from typing import List

import pytest

from tecton.cli.environment import EnvironmentDependencies
from tecton.cli.environment import UploadPart
from tecton.cli.environment import _get_pkg_to_version
from tecton.cli.environment import _run_dependency_resolution
from tecton.cli.environment import get_upload_parts
from tecton.cli.environment_utils import is_valid_environment_name
from tecton.cli.upload_utils import DEFAULT_UPLOAD_PART_SIZE_MB


ERROR_INPUT_REQUIREMENTS_TEXT = """
urllib3<1.27
tecton==1.1.0b6
"""

INPUT_REQUIREMENTS_TEXT = """
# THIS IS A MESS
# This is an implicit value, here for clarity
--index-url https://pypi.python.org/simple/

# pypika @ https://s3.us-west-2.amazonaws.com/tecton.ai.public/python/PyPika-0.48.9-py2.py3-none-any.whl
xformers==0.0.28.post1
# tecton[rift-materialization] @ file:///Users/vitaly/dev/tecton/bazel-bin/sdk/pypi/tecton-99.99.99-py3-none-any.whl # hello
tecton-runtime==1.0.0

# pydantic<2
# setuptools<70
urllib3<1.27

# protobuf<=4.25.3 # hi
tecton[rift-materialization]==1.1.0b6
"""

RESOLVED_REQUIREMENTS_TEXT = """
--index-url https://pypi.python.org/simple/
--find-links https://s3.us-west-2.amazonaws.com/tecton.ai.public/python/index.html

deltalake==0.18.2
    # via tecton
    # from https://pypi.python.org/simple/
tecton[rift-materialization] @ file:///Users/vitaly/dev/tecton/bazel-bin/sdk/pypi/tecton-99.99.99-py3-none-any.whl
    # via -r requirements.txt
tecton-runtime==1.0.0
    # via -r requirements.txt
    # from https://pypi.python.org/simple/
"""


SAMPLE_LOCK_JSON = {
    "locked_resolves": [
        {
            "locked_requirements": [
                {
                    "project_name": "attrs",
                    "requires_dists": [
                        "attrs[tests-mypy]; extra == 'tests-no-zope'",
                        "hypothesis; extra == 'tests-no-zope'",
                    ],
                    "version": "23.2.0",
                },
                {"project_name": "boto3", "requires_dists": ["botocore<1.35.0,>=1.34.87"], "version": "1.34.87"},
                {"project_name": "pytest", "requires_dists": [], "version": "8.1.1"},
            ]
        }
    ],
    "requirements": ["attrs==23.2.0", "boto3==1.34.87", "pytest"],
}


@pytest.fixture
def uv_binary_setup(tmp_path):
    import importlib.metadata
    from importlib.util import find_spec

    version = importlib.metadata.version("uv")
    base_dir = os.path.dirname(os.path.dirname(find_spec("uv").origin))
    new_path = os.path.join(base_dir, f"uv-{version}.data/scripts")
    # set this up because `uv` via @pip does not unpack binaries in discoverable location
    if os.path.exists(new_path):
        os.environ["UV_INSTALL_DIR"] = new_path


@pytest.fixture
def input_requirements_file(tmp_path):
    requirements_path = tmp_path / "requirements.txt"
    requirements_path.write_text(INPUT_REQUIREMENTS_TEXT)
    return requirements_path


@pytest.fixture
def error_input_requirements_file(tmp_path):
    requirements_path = tmp_path / "resolved.txt"
    requirements_path.write_text(ERROR_INPUT_REQUIREMENTS_TEXT)
    return requirements_path


@pytest.fixture
def resolved_requirements_file(tmp_path):
    requirements_path = tmp_path / "resolved.txt"
    requirements_path.write_text(RESOLVED_REQUIREMENTS_TEXT)
    return requirements_path


@dataclass
class FileSplit__TestCase:
    name: str
    file_size: int
    expected_parts: List[UploadPart]


FILE_SPLIT_TEST_CASES = [
    FileSplit__TestCase(
        name="single_file",
        file_size=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024 - 1,
        expected_parts=[UploadPart(part_number=1, offset=0, part_size=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024 - 1)],
    ),
    FileSplit__TestCase(
        name="exact_multiple_parts",
        file_size=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024 * 5,
        expected_parts=[
            UploadPart(
                part_number=i,
                offset=(i - 1) * DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024,
                part_size=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024,
            )
            for i in range(1, 6)
        ],
    ),
    FileSplit__TestCase(
        name="multiple_parts_with_last_part_smaller",
        file_size=(DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024 * 2) + (DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024 // 2),
        expected_parts=[
            UploadPart(part_number=1, offset=0, part_size=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024),
            UploadPart(
                part_number=2,
                offset=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024,
                part_size=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024,
            ),
            UploadPart(
                part_number=3,
                offset=2 * DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024,
                part_size=DEFAULT_UPLOAD_PART_SIZE_MB * 1024 * 1024 // 2,
            ),
        ],
    ),
    FileSplit__TestCase(
        name="zero_size_file",
        file_size=0,
        expected_parts=[],
    ),
]


@pytest.mark.parametrize("test_case", FILE_SPLIT_TEST_CASES, ids=[tc.name for tc in FILE_SPLIT_TEST_CASES])
def test_get_upload_parts(test_case):
    parts = get_upload_parts(test_case.file_size)
    assert len(parts) == len(test_case.expected_parts)
    for part, expected_part in zip(parts, test_case.expected_parts):
        assert part.part_size == expected_part.part_size
        assert part.part_number == expected_part.part_number
        assert part.offset == expected_part.offset


@pytest.mark.parametrize(
    "name, expected",
    [
        ("env123", True),
        ("env_123", True),
        ("ENV-123", True),
        ("env*123", False),
        ("env?123", False),
        ("env!123", False),
        ("", False),
        ("env 123", False),
        ("env_01234567890123456789001234567890012345678900123456789001234567890", False),
    ],
)
def test_environments(name, expected):
    assert is_valid_environment_name(name) == expected


@pytest.mark.skip("Test requires internet access.")
def test_requirements_resolution_uv(input_requirements_file, tmp_path, uv_binary_setup):
    # tests python dependency resolution (using `uv`)
    resolved_requirements_path, tecton_runtime_version, tecton_rift_version = _run_dependency_resolution(
        input_requirements_file, tmp_path, python_version="3.9", tool="uv"
    )

    assert tecton_runtime_version == "1.0.0"
    assert tecton_rift_version == "1.1.0b6"


@pytest.mark.skip("Test requires internet access. Pex cannot resolve `xformers` because of manylinux compatibility")
def test_requirements_resolution_pex(input_requirements_file, tmp_path):
    # tests python dependency resolution (using `pex`)
    resolved_requirements_path, tecton_runtime_version, tecton_rift_version = _run_dependency_resolution(
        input_requirements_file, tmp_path, python_version="3.9", tool="pex"
    )

    assert tecton_runtime_version == "1.0.0"
    assert tecton_rift_version == "1.1.0b6"


def test_error_requirements_resolution(error_input_requirements_file, tmp_path):
    # exists because requirements does not have any supporting tecton libraries
    with pytest.raises(SystemExit) as e:
        _run_dependency_resolution(error_input_requirements_file, tmp_path, python_version="3.9", tool="uv")
    assert e.type == SystemExit
    assert e.value.code == 1


def test_get_tecton_versions_from_resolved(resolved_requirements_file):
    tecton_pkg_to_version = _get_pkg_to_version(
        resolved_requirements_file, packages=["tecton[rift-materialization]", "tecton-runtime", "deltalake"]
    )
    tecton_runtime_version = tecton_pkg_to_version.get("tecton-runtime")
    tecton_rift_version = tecton_pkg_to_version.get("tecton[rift-materialization]")
    deltalake_version = tecton_pkg_to_version.get("deltalake")

    assert tecton_runtime_version == "1.0.0"
    assert tecton_rift_version == "99.99.99"
    assert deltalake_version == "0.18.2"


@pytest.fixture
def environment_dependencies():
    return EnvironmentDependencies(SAMPLE_LOCK_JSON)


@pytest.mark.parametrize(
    "package_name, expected_version",
    [("attrs", "23.2.0"), ("boto3", "1.34.87"), ("pytest", "8.1.1"), ("nonexistent", None)],
)
def test_get_version(environment_dependencies, package_name, expected_version):
    assert environment_dependencies.get_version(package_name) == expected_version


@pytest.mark.parametrize(
    "package_name, expected_presence", [("attrs", True), ("boto3", True), ("pytest", True), ("nonexistent", False)]
)
def test_is_dependency_present(environment_dependencies, package_name, expected_presence):
    assert environment_dependencies.is_dependency_present(package_name) == expected_presence


@pytest.mark.parametrize(
    "package_name, expected_extras", [("attrs", ["tests-no-zope"]), ("boto3", []), ("pytest", []), ("nonexistent", [])]
)
def test_get_dependency_extras(environment_dependencies, package_name, expected_extras):
    extras = environment_dependencies.get_dependency_extras(package_name)
    assert extras == expected_extras
