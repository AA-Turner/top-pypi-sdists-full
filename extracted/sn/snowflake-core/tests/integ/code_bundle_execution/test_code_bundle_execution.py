"""Integration tests for the anonymous EXECUTE CODE BUNDLE FROM <stage> REST surface.

The stage-location fixtures (local to this module) stage only the application files on an SSE-encrypted
stage: ``execution_stage_location`` stages the Python ``data/simple_bundle/main.py`` and
``scala_execution_stage_location`` stages the Scala ``data/scala_bundle`` assembly jar. No code_bundle
config file is staged; every test supplies the bundle config inline via ``specification`` (WITH
SPECIFICATION), so the stage only needs to hold the entry-point file (main.py) or the main jar.
"""

from pathlib import Path

import pytest

from snowflake.core.code_bundle_execution import (
    BundleSpec,
    CodeBundleExecutionCollection,
    CodeBundleSpecification,
    ExecuteCodeBundleRequest,
    SuccessAcceptedResponse,
    SuccessResponse,
)
from snowflake.core.exceptions import NotFoundError
from snowflake.core.stage import Stage, StageEncryption
from tests.integ.utils import assert_code_bundle_execution_succeeded, random_string


pytestmark = pytest.mark.min_sf_ver("10.27.100")

# Directories holding the application files to stage (config is supplied inline via ``specification``, so
# no code_bundle.(yml|yaml) is staged). ``simple_bundle`` holds the Python entry point (main.py);
# ``scala_bundle`` holds the assembly jar. Files are staged at the stage root.
_BUNDLE_DIR = Path(__file__).parent / "data" / "simple_bundle"
_SCALA_BUNDLE_DIR = Path(__file__).parent / "data" / "scala_bundle"
_SCALA_BUNDLE_JAR = "scos-cb-scala_2.12-1.0.0-assembly.jar"

# Inline bundle config (WITH SPECIFICATION) for the Python bundle, mirroring what used to be staged as
# code_bundle.yml. Supplying it inline means no config file needs to live on the stage. The request's
# ``specification`` field is now a typed CodeBundleSpecification, but a plain dict of the same shape is
# still accepted (pydantic coerces it), so this dict form doubles as back-compat coverage; the typed
# equivalent is exercised by ``_python_bundle_spec_typed`` / the typed tests below.
_PYTHON_BUNDLE_SPEC = {
    "bundle": {
        "type": "custom",
        "compute_type": "warehouse",
        "language": "python",
        "compute_options": {"runtime_version": "3.11"},
    }
}


def _python_bundle_spec_typed() -> CodeBundleSpecification:
    """Return the typed equivalent of ``_PYTHON_BUNDLE_SPEC`` (a CodeBundleSpecification/BundleSpec)."""
    return CodeBundleSpecification(
        bundle=BundleSpec(
            type="custom",
            compute_type="warehouse",
            language="python",
            compute_options={"runtime_version": "3.11"},
        )
    )


def _iter_bundle_files(bundle_dir: Path):
    """Yield ``(absolute_path, relative_dir)`` for every file under ``bundle_dir``.

    ``relative_dir`` is ``""`` for files at the bundle root, otherwise the POSIX-style subdirectory path
    ending in ``"/"``, so it can be appended directly to the stage location.
    """
    for file_path in bundle_dir.rglob("*"):
        if file_path.is_file():
            relative_dir = file_path.parent.relative_to(bundle_dir).as_posix()
            relative_dir = "" if relative_dir == "." else relative_dir + "/"
            yield file_path, relative_dir


def _stage_bundle(session, stages, bundle_dir: Path):
    """Create an SSE-encrypted stage, PUT every file under ``bundle_dir`` onto it, and return the stage.

    The stage uses ``SNOWFLAKE_SSE`` (server-side) encryption so PUT does not add client-side-encryption
    headers: the anonymous EXECUTE CODE BUNDLE FROM <stage> path reads the config file directly off the
    stage, which a none-mode storage volume rejects if the file carries CSE headers.
    """
    stage_name = random_string(5, "test_cbe_stage_")
    bundle_stage = stages.create(
        Stage(name=stage_name, kind="PERMANENT", encryption=StageEncryption(type="SNOWFLAKE_SSE"))
    )
    for file_path, relative_dir in _iter_bundle_files(bundle_dir):
        session.file.put(str(file_path), f"@{bundle_stage.name}/{relative_dir}", auto_compress=False)
    return bundle_stage


@pytest.fixture(scope="module")
def execution_stage_location(session, stages) -> str:
    """Stage only the Python entry point (main.py) and return its stage location.

    No code_bundle.yml is staged: the Python execute tests supply the bundle config inline via
    ``specification``, so the stage only needs to hold the entry-point file.
    """
    bundle_stage = _stage_bundle(session, stages, _BUNDLE_DIR)
    try:
        yield f"@{bundle_stage.database.name}.{bundle_stage.schema.name}.{bundle_stage.name}"
    finally:
        bundle_stage.drop()


@pytest.fixture(scope="module")
def scala_execution_stage_location(session, stages) -> str:
    """Stage only the Scala assembly jar and return its stage location.

    No code_bundle.yaml is staged: the Scala execute test supplies the bundle config inline via
    ``specification``, so the stage only needs to hold the main jar.
    """
    bundle_stage = _stage_bundle(session, stages, _SCALA_BUNDLE_DIR)
    try:
        yield f"@{bundle_stage.database.name}.{bundle_stage.schema.name}.{bundle_stage.name}"
    finally:
        bundle_stage.drop()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_code_bundle(code_bundle_execution: CodeBundleExecutionCollection, execution_stage_location):
    # Execute a code bundle directly from a stage location. async_exec defaults to True, so the server
    # accepts the execution and returns a SuccessAcceptedResponse carrying the job id. The bundle config is
    # supplied inline via ``specification`` (an object), and ``execution_name`` supplies a caller-chosen run
    # name recorded in run history.
    response = code_bundle_execution.execute(
        ExecuteCodeBundleRequest(
            from_location=execution_stage_location,
            entrypoint="main.py",
            specification=_PYTHON_BUNDLE_SPEC,
            execution_name="test_cbe_named_run",
        )
    )
    assert isinstance(response, SuccessAcceptedResponse)
    # job_id is the query id of the accepted execution (5 hyphen-separated groups).
    assert isinstance(response.job_id, str) and response.job_id.count("-") == 4, response.job_id
    assert response.message, "accepted response should carry a status message"

    # Acceptance is not success: poll the async job to completion and assert it actually succeeded.
    assert_code_bundle_execution_succeeded(code_bundle_execution, response.job_id)


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_code_bundle_with_typed_specification(
    code_bundle_execution: CodeBundleExecutionCollection, execution_stage_location
):
    # Same execute path as test_execute_code_bundle, but supplying ``specification`` as a typed
    # CodeBundleSpecification(bundle=BundleSpec(...)) instead of a raw dict. This exercises the typed
    # spec end-to-end; it serializes to the same JSON the dict form produces, so the server sees an
    # identical payload.
    typed_spec = _python_bundle_spec_typed()
    # Sanity-check the typed model serializes to the same wire payload as the dict form.
    assert typed_spec.to_dict() == _PYTHON_BUNDLE_SPEC

    response = code_bundle_execution.execute(
        ExecuteCodeBundleRequest(
            from_location=execution_stage_location,
            entrypoint="main.py",
            specification=typed_spec,
            execution_name="test_cbe_typed_spec_run",
        )
    )
    assert isinstance(response, SuccessAcceptedResponse)
    assert isinstance(response.job_id, str) and response.job_id.count("-") == 4, response.job_id

    assert_code_bundle_execution_succeeded(code_bundle_execution, response.job_id)


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_code_bundle_with_arguments(
    code_bundle_execution: CodeBundleExecutionCollection, execution_stage_location
):
    # ``arguments`` is a list of strings; exercise it over the wire.
    response = code_bundle_execution.execute(
        ExecuteCodeBundleRequest(
            from_location=execution_stage_location,
            entrypoint="main.py",
            arguments=["--flag", "value"],
            specification=_PYTHON_BUNDLE_SPEC,
        )
    )
    assert isinstance(response, SuccessAcceptedResponse)
    assert isinstance(response.job_id, str) and response.job_id.count("-") == 4, response.job_id

    assert_code_bundle_execution_succeeded(code_bundle_execution, response.job_id)


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_scala_code_bundle_with_arguments(
    code_bundle_execution: CodeBundleExecutionCollection, scala_execution_stage_location
):
    # Anonymous EXECUTE CODE BUNDLE for a Scala/Spark bundle: the entrypoint is the jar's main class
    # rather than a .py file, and ``from_location`` is the path to the main JAR after the stage. The bundle
    # config can't be read off the stage in this form, so it is supplied inline via ``specification``
    # (WITH SPECIFICATION), here built as a typed CodeBundleSpecification/BundleSpec exercising the
    # list-valued ``env_vars`` field. The main jar comes from ``from_location``, so it must NOT also be
    # repeated in java_dependencies.jars (that would duplicate it in the IMPORTS clause). ScosJvmHelloApp
    # uses args[0] as the (required) result table name and echoes the rest, so the first argument must be
    # an identifier.
    jar_url = f"{scala_execution_stage_location}/{_SCALA_BUNDLE_JAR}"
    specification = CodeBundleSpecification(
        bundle=BundleSpec(
            type="spark",
            compute_type="warehouse",
            language="scala",
            compute_options={"runtime_version": "1.29", "language_version": "2.12"},
            env_vars=[
                {"SCOS_ENV_A": "named_a"},
                {"SCOS_ENV_B": "named_b"},
                {"SPARK_LOCAL_IP": "127.0.0.1"},
                {"SNOWPARK_SUBMIT_SPARK_APPLICATION_ID": "SSA_TEST_1234"},
            ],
        )
    )
    # The typed spec must serialize to the same wire payload as the equivalent raw dict.
    assert specification.to_dict() == {
        "bundle": {
            "type": "spark",
            "compute_type": "warehouse",
            "language": "scala",
            "compute_options": {"runtime_version": "1.29", "language_version": "2.12"},
            "env_vars": [
                {"SCOS_ENV_A": "named_a"},
                {"SCOS_ENV_B": "named_b"},
                {"SPARK_LOCAL_IP": "127.0.0.1"},
                {"SNOWPARK_SUBMIT_SPARK_APPLICATION_ID": "SSA_TEST_1234"},
            ],
        }
    }
    result_table = random_string(10, "scos_result_")
    response = code_bundle_execution.execute(
        ExecuteCodeBundleRequest(
            from_location=jar_url,
            entrypoint="com.code_bundle_example.ScosJvmHelloApp",
            arguments=[result_table, "--flag", "value"],
            specification=specification,
        )
    )
    assert isinstance(response, SuccessAcceptedResponse)
    assert isinstance(response.job_id, str) and response.job_id.count("-") == 4, response.job_id

    assert_code_bundle_execution_succeeded(code_bundle_execution, response.job_id)


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
@pytest.mark.skip
def test_execute_and_fetch_status(code_bundle_execution: CodeBundleExecutionCollection, execution_stage_location):
    # An async execution returns a SuccessAcceptedResponse carrying the job id; fetch its status.
    response = code_bundle_execution.execute(
        ExecuteCodeBundleRequest(
            from_location=execution_stage_location,
            entrypoint="main.py",
            specification=_PYTHON_BUNDLE_SPEC,
        ),
        async_exec=True,
    )
    assert isinstance(response, SuccessAcceptedResponse)
    execution_id = response.job_id
    assert execution_id and execution_id.count("-") == 4, execution_id

    # Poll to a terminal status and assert the job succeeded (not just that a status was returned).
    status = assert_code_bundle_execution_succeeded(code_bundle_execution, execution_id)
    assert status.execution_id == execution_id
    # The recorded query is the EXECUTE CODE BUNDLE statement we submitted.
    assert status.query_text and "EXECUTE CODE BUNDLE" in status.query_text.upper()
    assert "MAIN.PY" in status.query_text.upper()
    assert status.user, "the submitting user should be populated"
    # database_name / schema_name are the session context the execution ran in (renamed from
    # database / schema in the OpenAPI spec); both should be populated for a code bundle execution.
    assert status.database_name, "database_name should be populated"
    assert status.schema_name, "schema_name should be populated"


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_and_cancel(code_bundle_execution: CodeBundleExecutionCollection, execution_stage_location):
    # An async execution returns a SuccessAcceptedResponse carrying the job id; cancel it.
    response = code_bundle_execution.execute(
        ExecuteCodeBundleRequest(
            from_location=execution_stage_location,
            entrypoint="main.py",
            specification=_PYTHON_BUNDLE_SPEC,
        ),
        async_exec=True,
    )
    assert isinstance(response, SuccessAcceptedResponse)
    execution_id = response.job_id
    assert execution_id and execution_id.count("-") == 4, execution_id

    # Cancelling a running execution returns a status message that echoes the cancelled query id.
    # If the bundle finishes before the cancel reaches the server (common for trivial bundles), the
    # server returns "Identified SQL statement is not currently executing." instead — both outcomes
    # are valid; what matters is that cancel() returns a SuccessResponse without raising.
    cancel_response = code_bundle_execution[execution_id].cancel()
    assert isinstance(cancel_response, SuccessResponse)
    assert cancel_response.status, "cancel response should carry a non-empty status message"
    assert execution_id in cancel_response.status or "not currently executing" in cancel_response.status.lower()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_fetch_status_unknown_execution(code_bundle_execution: CodeBundleExecutionCollection):
    # An unknown execution id yields an empty list from the server, which fetch_status surfaces as NotFoundError.
    execution = code_bundle_execution["00000000-0000-0000-0000-000000000000"]
    with pytest.raises(NotFoundError):
        execution.fetch_status()
