import copy

import pytest

from snowflake.core.code_bundle import (
    CodeBundle,
    CodeBundleCollection,
    ExecuteCodeBundleRequest,
    SuccessAcceptedResponse,
)
from snowflake.core.code_bundle_execution import CodeBundleExecutionCollection
from snowflake.core.exceptions import ConflictError
from tests.integ.utils import assert_code_bundle_execution_succeeded, random_string


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_create_and_fetch_code_bundle(code_bundles: CodeBundleCollection, code_bundle_stage_location):
    new_bundle_def = CodeBundle(
        name=random_string(10, "test_code_bundle_"),
        from_location=code_bundle_stage_location,
        comment="code bundle first",
    )
    bundle = None
    try:
        bundle = code_bundles.create(new_bundle_def)
        created = bundle.fetch()
        assert created.name == new_bundle_def.name.upper()
        assert created.comment == new_bundle_def.comment

        with pytest.raises(ConflictError):
            code_bundles.create(new_bundle_def, mode="error_if_exists")

        new_bundle_def_1 = copy.deepcopy(new_bundle_def)
        new_bundle_def_1.comment = "code bundle second"
        bundle = code_bundles.create(new_bundle_def_1, mode="if_not_exists")
        created = bundle.fetch()
        # if_not_exists does not replace, so the original comment is retained
        assert created.comment == new_bundle_def.comment
    finally:
        if bundle is not None:
            bundle.drop()

    bundle = None
    try:
        bundle = code_bundles.create(new_bundle_def_1, mode="or_replace")
        created = bundle.fetch()
        assert created.comment == new_bundle_def_1.comment
    finally:
        if bundle is not None:
            bundle.drop()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_iter_code_bundle(code_bundles: CodeBundleCollection, code_bundle_stage_location):
    bundle_name = random_string(10, "test_code_bundle_iter_")
    bundle = code_bundles.create(CodeBundle(name=bundle_name, from_location=code_bundle_stage_location))
    try:
        names = [b.name for b in code_bundles.iter(like=f"{bundle_name}%")]
        assert bundle_name.upper() in [n.upper() for n in names]
    finally:
        bundle.drop()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_drop_code_bundle(code_bundles: CodeBundleCollection, code_bundle_stage_location):
    bundle_name = random_string(10, "test_code_bundle_drop_")
    bundle = code_bundles.create(CodeBundle(name=bundle_name, from_location=code_bundle_stage_location))
    bundle.drop()
    # dropping a non-existent bundle with if_exists=True should not raise
    bundle.drop(if_exists=True)


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_add_version_code_bundle(code_bundles: CodeBundleCollection, code_bundle_stage_location):
    from snowflake.core.code_bundle import AddVersionCodeBundleRequest

    bundle_name = random_string(10, "test_code_bundle_add_version_")
    bundle = code_bundles.create(CodeBundle(name=bundle_name, from_location=code_bundle_stage_location))
    try:
        bundle.add_version(AddVersionCodeBundleRequest(from_location=code_bundle_stage_location))
    finally:
        bundle.drop()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_code_bundle(
    code_bundles: CodeBundleCollection,
    code_bundle_execution: CodeBundleExecutionCollection,
    executable_code_bundle_stage_location,
):
    # EXECUTE a named code bundle: POST /.../code-bundles/{name}:execute. async_exec=True → the server
    # accepts the execution and returns a SuccessAcceptedResponse carrying the job id.
    bundle_name = random_string(10, "test_code_bundle_execute_")
    bundle = code_bundles.create(CodeBundle(name=bundle_name, from_location=executable_code_bundle_stage_location))
    try:
        response = bundle.execute(ExecuteCodeBundleRequest(entrypoint="main.py"), async_exec=True)
        assert isinstance(response, SuccessAcceptedResponse)
        # job_id is the query id of the accepted execution (5 hyphen-separated groups).
        assert isinstance(response.job_id, str) and response.job_id.count("-") == 4, response.job_id

        # async_exec only accepts the submission; poll to completion *before* the finally block drops the
        # bundle, otherwise the async job races teardown and fails with "Notebook Project does not exist".
        assert_code_bundle_execution_succeeded(code_bundle_execution, response.job_id)
    finally:
        bundle.drop()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_code_bundle_with_arguments(
    code_bundles: CodeBundleCollection,
    code_bundle_execution: CodeBundleExecutionCollection,
    executable_code_bundle_stage_location,
):
    # Same :execute endpoint, exercising the list-valued ``arguments`` over the wire.
    bundle_name = random_string(10, "test_code_bundle_execute_args_")
    bundle = code_bundles.create(CodeBundle(name=bundle_name, from_location=executable_code_bundle_stage_location))
    try:
        response = bundle.execute(
            ExecuteCodeBundleRequest(entrypoint="main.py", arguments=["--flag", "value"]),
            async_exec=True,
        )
        assert isinstance(response, SuccessAcceptedResponse)
        assert isinstance(response.job_id, str) and response.job_id.count("-") == 4, response.job_id

        assert_code_bundle_execution_succeeded(code_bundle_execution, response.job_id)
    finally:
        bundle.drop()


@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
def test_execute_scala_code_bundle_with_arguments(
    code_bundles: CodeBundleCollection,
    code_bundle_execution: CodeBundleExecutionCollection,
    executable_scala_code_bundle_stage_location,
):
    # Same :execute endpoint as the Python case, but running the Scala/Spark bundle: the entrypoint is the
    # jar's main class rather than a .py file, and ``arguments`` is exercised over the wire.
    bundle_name = random_string(10, "test_scala_code_bundle_execute_args_")
    bundle = code_bundles.create(
        CodeBundle(name=bundle_name, from_location=executable_scala_code_bundle_stage_location)
    )
    # ScosJvmHelloApp uses args[0] as the (required) result table name and echoes the remaining tokens,
    # so the first argument must be a valid identifier; the extra tokens exercise multi-valued arguments.
    result_table = random_string(10, "scos_result_")
    try:
        response = bundle.execute(
            ExecuteCodeBundleRequest(
                entrypoint="com.code_bundle_example.ScosJvmHelloApp",
                arguments=[result_table, "--flag", "value"],
            ),
            async_exec=True,
        )
        assert isinstance(response, SuccessAcceptedResponse)
        assert isinstance(response.job_id, str) and response.job_id.count("-") == 4, response.job_id

        # async_exec only means the submission was accepted; poll the execution to completion *before*
        # the finally block drops the bundle, otherwise the async job races teardown and fails with
        # "Notebook Project '<bundle>' does not exist". Assert the job actually succeeded.
        assert_code_bundle_execution_succeeded(code_bundle_execution, response.job_id)
    finally:
        bundle.drop()
