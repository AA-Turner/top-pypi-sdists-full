import json
from collections.abc import Generator

import pytest
from _pytest.capture import CaptureFixture
from click.testing import CliRunner, Result
from localstack_cli.pro.core.cli.replicator import replicator
from localstack_cli.testing.config import SECONDARY_TEST_AWS_ACCOUNT_ID
from localstack_cli.utils.strings import short_uid
from localstack_cli.utils.sync import retry


@pytest.fixture
def runner(capsys: CaptureFixture[str]) -> Generator[CliRunner]:
    """
    Convenience fixture to return a click.CliRunner for cli testing
    This allows us to keep running the replicator test with  log_cli enabled
    to receive the logs from localstack.
    """

    class NoCapsysCliRunner(CliRunner):
        """Override CliRunner to disable capsys"""

        def __init__(self, **kwargs):
            # Don't combine stdout and stderr into the same output stream
            # The CLI logs to stderr and the output on stdout should be JSON formatted
            # so that it can be parsed by external tools.
            # If we cross the streams then we can no longer parse the output in tests
            # as JSON
            kwargs.pop("mix_stderr", None)
            super().__init__(**kwargs)

        def invoke(self, *args, **kwargs) -> Result:
            # Way to fix https://github.com/pallets/click/issues/824
            with capsys.disabled():
                result = super().invoke(*args, **kwargs)
            return result

    yield NoCapsysCliRunner()


def test_start_mock_replication_job(runner, monkeypatch):
    # ensure AWS_PROFILE is not set in the environment
    monkeypatch.delenv("AWS_PROFILE", raising=False)

    result = runner.invoke(
        replicator,
        ["start", "--replication-type", "MOCK"],
        env={
            "AWS_ACCESS_KEY_ID": "test",
            "AWS_SECRET_ACCESS_KEY": "test",
            "AWS_DEFAULT_REGION": "us-east-1",
        },
    )
    assert result.exit_code == 0, result.output

    response = json.loads(result.stdout)
    job_id = response["job_id"]
    assert response["state"] == "SUBMITTED"
    assert response["error_message"] is None
    assert response["type"] == "MOCK"
    assert response["replication_config"] == {"delay": 1}

    def _assert_status():
        status_result = runner.invoke(replicator, ["status", job_id])
        assert status_result.exit_code == 0, status_result.output

        job_status = json.loads(status_result.stdout)
        assert job_status["state"] == "SUCCEEDED"

    retry(_assert_status, retries=5, sleep=1)


def test_list_resources(runner, monkeypatch):
    result = runner.invoke(replicator, ["resources"])
    assert result.exit_code == 0, result.output

    resources: list[dict] = json.loads(result.stdout)

    supported_resource_types = [resource["resource_type"] for resource in resources]
    assert "AWS::SSM::Parameter" in supported_resource_types

    for resource in resources:
        assert len(resource["policy_statements"]) > 0


@pytest.mark.skip("using runtime client")
@pytest.mark.parametrize("method", ["ARN", "CFN"])
def test_start_single_replication_job(
    method,
    runner,
    monkeypatch,
    aws_client,
    create_parameter,
    source_credentials,
    wait_for_job_state,
    target_aws_client,
    region_name,
    source_aws_endpoint,
):
    parameter_name = f"mock-{short_uid()}"
    create_parameter(
        Name=parameter_name,
        Type="String",
        Value="test",
    )

    args = [
        "start",
        "--replication-type",
        "SINGLE_RESOURCE",
        "--target-account-id",
        SECONDARY_TEST_AWS_ACCOUNT_ID,
    ]

    if method == "ARN":
        parameter_arn = aws_client.ssm.get_parameter(Name=parameter_name)["Parameter"]["ARN"]
        args.extend(["--resource-arn", parameter_arn])
    else:
        args.extend(
            ["--resource-type", "AWS::SSM::Parameter", "--resource-identifier", parameter_name]
        )

    result = runner.invoke(
        replicator,
        args=args,
        env={
            "AWS_ACCESS_KEY_ID": source_credentials.access_key,
            "AWS_SECRET_ACCESS_KEY": source_credentials.secret_key,
            "AWS_SESSION_TOKEN": source_credentials.token,
            "AWS_DEFAULT_REGION": region_name,
            "AWS_ENDPOINT_URL": source_aws_endpoint,
        },
    )

    job_id = json.loads(result.stdout)["job_id"]

    def _assert_status():
        status_result = runner.invoke(replicator, ["status", job_id])
        job_status = json.loads(status_result.stdout)
        assert job_status["state"] == "SUCCEEDED"

    retry(_assert_status, retries=5, sleep=1)

    parameter_found = target_aws_client.ssm.get_parameter(Name=parameter_name)["Parameter"]
    assert parameter_found["Value"] == "test"
