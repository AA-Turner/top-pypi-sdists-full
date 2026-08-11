from io import BytesIO
from pathlib import Path

import pytest

from snowflake.core.stage import Stage
from tests.integ.utils import random_string


code_bundle_file = "main.py"

# Directory holding an executable code bundle (code_bundle.yml + main.py). code_bundle.yml must be present
# on the stage at CREATE time so the created bundle version captures the config the :execute endpoint needs.
_EXECUTABLE_BUNDLE_DIR = Path(__file__).parent / "data" / "simple_bundle"

# Directory holding an executable Scala/Spark code bundle (code_bundle.yaml + assembly jar). Like the
# Python bundle above, code_bundle.yaml must be staged at CREATE time so the bundle version captures the
# Scala config the :execute endpoint needs.
_EXECUTABLE_SCALA_BUNDLE_DIR = Path(__file__).parent / "data" / "scala_bundle"


def _stage_bundle_dir(session, stages, bundle_dir: Path) -> str:
    """Create a temporary stage, PUT every file under ``bundle_dir`` onto it, and return its location."""
    stage_name = random_string(5, "test_code_bundle_exec_stage_")
    bundle_stage = stages.create(Stage(name=stage_name, kind="TEMPORARY"))
    for file_path in bundle_dir.rglob("*"):
        if file_path.is_file():
            relative_dir = file_path.parent.relative_to(bundle_dir).as_posix()
            relative_dir = "" if relative_dir == "." else relative_dir + "/"
            session.file.put(str(file_path), f"@{bundle_stage.name}/{relative_dir}", auto_compress=False)
    return bundle_stage


@pytest.fixture(scope="module")
def code_bundle_stage_with_file(session, stages) -> Stage:
    """Create a temporary stage that holds a simple code bundle source file."""
    stage_name = random_string(5, "test_code_bundle_stage_")
    stage = Stage(name=stage_name, kind="TEMPORARY")

    bundle_stage = stages.create(stage)

    try:
        file_path = f"@{bundle_stage.name}/{code_bundle_file}"
        session.file.put_stream(
            BytesIO(b"def main():\n    print('hello from code bundle')\n"),
            file_path,
            auto_compress=False,
        )
        yield bundle_stage
    finally:
        bundle_stage.drop()


@pytest.fixture(scope="module")
def code_bundle_stage_location(code_bundle_stage_with_file) -> str:
    """Return the fully-qualified stage location that a code bundle can be created from."""
    return (
        f"@{code_bundle_stage_with_file.database.name}"
        f".{code_bundle_stage_with_file.schema.name}"
        f".{code_bundle_stage_with_file.name}"
    )


@pytest.fixture(scope="module")
def executable_code_bundle_stage_location(session, stages) -> str:
    """Stage an executable code bundle (code_bundle.yml + main.py) and return its stage location.

    Used by the :execute test: a named bundle created FROM this stage captures code_bundle.yml, which the
    execute endpoint needs. No SSE is required here (unlike anonymous execute-from-stage) because the
    config is read from the captured bundle version, not directly off the stage.
    """
    bundle_stage = _stage_bundle_dir(session, stages, _EXECUTABLE_BUNDLE_DIR)
    try:
        yield f"@{bundle_stage.database.name}.{bundle_stage.schema.name}.{bundle_stage.name}"
    finally:
        bundle_stage.drop()


@pytest.fixture(scope="module")
def executable_scala_code_bundle_stage_location(session, stages) -> str:
    """Stage an executable Scala/Spark code bundle (code_bundle.yaml + assembly jar) and return its location.

    Mirrors ``executable_code_bundle_stage_location`` but for the Scala bundle: a named bundle created FROM
    this stage captures code_bundle.yaml, which the execute endpoint needs to run the jar's main class.
    """
    bundle_stage = _stage_bundle_dir(session, stages, _EXECUTABLE_SCALA_BUNDLE_DIR)
    try:
        yield f"@{bundle_stage.database.name}.{bundle_stage.schema.name}.{bundle_stage.name}"
    finally:
        bundle_stage.drop()
