# -*- coding: utf-8 -*-

from boto_session_manager.manager import BotoSesManager
from boto_session_manager.manager import PATH_DEFAULT_SNAPSHOT

import pytest
import botocore.exceptions
from botocore.stub import Stubber

import os
import json
import shutil
import subprocess
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from boto_session_manager.services import AwsServiceEnum
from boto_session_manager.tests.settings import AWS_REGION
from boto_session_manager.tests.settings import IS_CI
from boto_session_manager.tests.settings import TEST_AWS_PROFILE_ENV_VAR
from boto_session_manager.tests.settings import TEST_IAM_USER_NAME
from boto_session_manager.tests.settings import TEST_IAM_ROLE_NAME
from boto_session_manager.tests.settings import TEST_IAM_ROLE_WITH_EXTERNAL_ID_NAME
from boto_session_manager.tests.settings import TEST_ROLE_EXTERNAL_ID
from boto_session_manager.tests.settings import load_bsm_project

AWS_CLI_ENV_VARS = [
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "AWS_REGION",
    "AWS_PROFILE",
]


def make_offline_bsm(**kwargs) -> BotoSesManager:
    """
    A manager with fake static credentials: creating clients and reading the
    credentials never calls AWS, so these tests run without network.
    """
    return BotoSesManager(
        aws_access_key_id="AKIAFAKE",
        aws_secret_access_key="fake-secret",
        region_name=AWS_REGION,
        **kwargs,
    )


# ------------------------------------------------------------------------------
# Offline: no AWS call
# ------------------------------------------------------------------------------
class TestCache:
    def test_get_client(self):
        bsm = make_offline_bsm()
        s3_client = bsm.get_client(AwsServiceEnum.S3)
        assert bsm.get_client(AwsServiceEnum.S3) is s3_client
        # the typed property shares the cache
        assert bsm.s3_client is s3_client
        # the cache key is the service name only: later kwargs are ignored
        assert bsm.get_client(AwsServiceEnum.S3, region_name="eu-west-1") is s3_client

    def test_get_resource(self):
        bsm = make_offline_bsm()
        s3_resource = bsm.get_resource(AwsServiceEnum.S3)
        assert bsm.get_resource(AwsServiceEnum.S3) is s3_resource

    def test_default_client_kwargs(self):
        endpoint_url = "http://localhost:4566"
        bsm = make_offline_bsm(default_client_kwargs={"endpoint_url": endpoint_url})
        assert bsm.s3_client.meta.endpoint_url == endpoint_url
        s3_resource = bsm.get_resource(AwsServiceEnum.S3)
        assert s3_resource.meta.client.meta.endpoint_url == endpoint_url

    def test_create_boto_ses(self):
        bsm = make_offline_bsm()
        assert bsm.boto_ses is bsm.boto_ses
        assert bsm.create_boto_ses() is not bsm.boto_ses
        assert bsm.aws_region == AWS_REGION

    def test_clear_cache(self):
        bsm = make_offline_bsm()
        boto_ses = bsm.boto_ses
        s3_client = bsm.s3_client
        _ = bsm.get_resource(AwsServiceEnum.S3)
        _ = bsm.aws_region
        bsm.clear_cache()
        assert len(bsm._client_cache) == 0
        assert len(bsm._resource_cache) == 0
        assert bsm.boto_ses is not boto_ses
        assert bsm.s3_client is not s3_client


class TestExpiration:
    def test_default(self):
        bsm = make_offline_bsm()
        assert bsm.is_expired() is False
        # the default expiration time is one year from now
        assert bsm.is_expired(delta=400 * 24 * 3600) is True

    def test_explicit_expiration_time(self):
        now = datetime.now(timezone.utc)
        bsm = make_offline_bsm(expiration_time=now + timedelta(seconds=600))
        assert bsm.is_expired() is False
        assert bsm.is_expired(delta=300) is False
        assert bsm.is_expired(delta=900) is True


class TestSnapshot:
    def test_to_and_from_snapshot(self):
        bsm = make_offline_bsm()
        snapshot = bsm.to_snapshot()
        assert snapshot == {
            "region_name": AWS_REGION,
            "aws_access_key_id": "AKIAFAKE",
            "aws_secret_access_key": "fake-secret",
        }
        bsm_restored = BotoSesManager.from_snapshot(snapshot)
        assert bsm_restored.to_snapshot() == snapshot

    def test_to_snapshot_with_session_token(self):
        bsm = make_offline_bsm(aws_session_token="fake-token")
        assert bsm.to_snapshot()["aws_session_token"] == "fake-token"

    def test_temp_snapshot(self, tmp_path):
        path = tmp_path / "snapshot.json"
        bsm = make_offline_bsm()
        with bsm.temp_snapshot(path=path) as bsm_yielded:
            assert bsm_yielded is bsm
            assert json.loads(path.read_text()) == bsm.to_snapshot()
            bsm_restored = BotoSesManager.from_snapshot_file(path)
            assert bsm_restored.to_snapshot() == bsm.to_snapshot()
        assert path.exists() is False

    def test_from_snapshot_file_missing(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            BotoSesManager.from_snapshot_file(tmp_path / "missing.json")

    def test_default_snapshot_path(self):
        assert PATH_DEFAULT_SNAPSHOT.name == ".bsm-snapshot.json"


CALLER_IDENTITY = {
    "UserId": "AIDAFAKEUSERID123456",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/fake-user",
}


class TestAccountAlias:
    """
    The IAM answers are stubbed: a real account cannot show all three cases.
    """

    def make_stubbed_bsm(self) -> tuple[BotoSesManager, Stubber]:
        bsm = make_offline_bsm()
        sts_stubber = Stubber(bsm.sts_client)
        sts_stubber.add_response("get_caller_identity", CALLER_IDENTITY)
        sts_stubber.activate()
        iam_stubber = Stubber(bsm.iam_client)
        iam_stubber.activate()
        return bsm, iam_stubber

    def test_alias_set(self, capsys):
        bsm, iam_stubber = self.make_stubbed_bsm()
        iam_stubber.add_response(
            "list_account_aliases",
            {"AccountAliases": ["my-alias"], "IsTruncated": False},
        )
        bsm.print_who_am_i()
        assert "AWS Account Alias = my-alias" in capsys.readouterr().out
        assert bsm.aws_account_alias == "my-alias"  # cached, no second call

    def test_alias_not_set(self, capsys):
        bsm, iam_stubber = self.make_stubbed_bsm()
        iam_stubber.add_response(
            "list_account_aliases",
            {"AccountAliases": [], "IsTruncated": False},
        )
        assert bsm.aws_account_alias is None
        bsm.print_who_am_i(masked=False)
        out = capsys.readouterr().out
        assert "AWS Account Alias = <not set>" in out
        assert f"AWS Account Id = {CALLER_IDENTITY['Account']}" in out

    def test_alias_access_denied(self, capsys):
        bsm, iam_stubber = self.make_stubbed_bsm()
        iam_stubber.add_client_error(
            "list_account_aliases", service_error_code="AccessDenied"
        )
        bsm.print_who_am_i()
        out = capsys.readouterr().out
        assert "AWS Account Alias = <unavailable: AccessDenied>" in out
        assert f"AWS Region = {AWS_REGION}" in out

        # the property itself raises, and the failure is not cached
        iam_stubber.add_client_error(
            "list_account_aliases", service_error_code="AccessDenied"
        )
        with pytest.raises(botocore.exceptions.ClientError):
            _ = bsm.aws_account_alias


class TestAwsCliEnvVar:
    def test_static_credentials(self, monkeypatch):
        """
        Inside the block: the key pair and region, no token, no profile.
        After the block: every variable is back to its value before the block.
        """
        bsm = make_offline_bsm()
        # boto3 reads AWS_PROFILE when it creates the session: create it first
        _ = bsm.boto_ses
        monkeypatch.setenv("AWS_PROFILE", "before")
        monkeypatch.setenv("AWS_SESSION_TOKEN", "before")
        monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
        monkeypatch.delenv("AWS_REGION", raising=False)
        with bsm.awscli() as bsm_yielded:
            assert bsm_yielded is bsm
            assert os.environ["AWS_ACCESS_KEY_ID"] == "AKIAFAKE"
            assert os.environ["AWS_SECRET_ACCESS_KEY"] == "fake-secret"
            assert os.environ["AWS_REGION"] == AWS_REGION
            assert "AWS_SESSION_TOKEN" not in os.environ
            assert "AWS_PROFILE" not in os.environ
        assert os.environ["AWS_PROFILE"] == "before"
        assert os.environ["AWS_SESSION_TOKEN"] == "before"
        assert "AWS_ACCESS_KEY_ID" not in os.environ
        assert "AWS_REGION" not in os.environ

    def test_temporary_credentials(self, monkeypatch):
        for name in AWS_CLI_ENV_VARS:
            monkeypatch.delenv(name, raising=False)
        bsm = make_offline_bsm(aws_session_token="fake-token")
        with bsm.awscli():
            assert os.environ["AWS_SESSION_TOKEN"] == "fake-token"
            assert os.environ["AWS_ACCESS_KEY_ID"] == "AKIAFAKE"
        for name in AWS_CLI_ENV_VARS:
            assert name not in os.environ

    def test_restored_on_error(self, monkeypatch):
        monkeypatch.delenv("AWS_ACCESS_KEY_ID", raising=False)
        bsm = make_offline_bsm()
        with pytest.raises(ZeroDivisionError):
            with bsm.awscli():
                _ = 1 / 0
        assert "AWS_ACCESS_KEY_ID" not in os.environ

    @pytest.mark.skipif(IS_CI, reason="CI has no ~/.aws profile")
    def test_profile(self, monkeypatch):
        """
        A manager built from a profile passes the profile, not the keys.
        """
        for name in AWS_CLI_ENV_VARS:
            monkeypatch.delenv(name, raising=False)
        profile = os.environ[TEST_AWS_PROFILE_ENV_VAR]
        bsm = BotoSesManager(profile_name=profile, region_name=AWS_REGION)
        with bsm.awscli():
            assert os.environ["AWS_PROFILE"] == profile
            assert "AWS_ACCESS_KEY_ID" not in os.environ
        assert "AWS_PROFILE" not in os.environ


# ------------------------------------------------------------------------------
# Real AWS: the test IAM user and roles of ``mise run setup-aws-ci``
# ------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def bsm_project() -> BotoSesManager:
    return load_bsm_project()


def get_role_arn(bsm: BotoSesManager, role_name: str) -> str:
    return f"arn:aws:iam::{bsm.aws_account_id}:role/{role_name}"


def get_caller_arn_via_aws_cli() -> str:
    """
    Run ``aws sts get-caller-identity`` in a subprocess, which only sees the
    credentials through the environment variables.
    """
    aws = shutil.which("aws")
    if aws is None:  # pragma: no cover
        raise EnvironmentError("the aws CLI is not on PATH; run 'mise install'")
    res = subprocess.run(
        [aws, "sts", "get-caller-identity", "--output", "json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(res.stdout)["Arn"]


class TestIdentity:
    def test_iam_user(self, bsm_project):
        sts_res = bsm_project.sts_client.get_caller_identity()
        assert bsm_project.aws_account_id == sts_res["Account"]
        assert bsm_project.aws_account_user_id == sts_res["UserId"]
        assert bsm_project.principal_arn == sts_res["Arn"]
        assert bsm_project.principal_arn.endswith(f":user/{TEST_IAM_USER_NAME}")
        assert bsm_project.aws_region == AWS_REGION

        assert bsm_project.masked_aws_account_id != bsm_project.aws_account_id
        assert "*" in bsm_project.masked_aws_account_user_id
        assert bsm_project.aws_account_id not in bsm_project.masked_principal_arn

        alias = bsm_project.aws_account_alias
        assert alias is None or isinstance(alias, str)
        aliases = bsm_project.iam_client.list_account_aliases()["AccountAliases"]
        assert alias == (aliases[0] if aliases else None)

    def test_print_who_am_i(self, bsm_project, capsys):
        bsm_project.print_who_am_i()
        out = capsys.readouterr().out
        assert bsm_project.masked_principal_arn in out
        assert "AWS Account Alias = " in out


class TestAssumeRole:
    def test_assume_role(self, bsm_project):
        bsm_role = bsm_project.assume_role(
            role_arn=get_role_arn(bsm_project, TEST_IAM_ROLE_NAME),
            duration_seconds=900,
        )
        assert bsm_role is not bsm_project
        assert bsm_role.aws_account_id == bsm_project.aws_account_id
        assert f":assumed-role/{TEST_IAM_ROLE_NAME}/" in bsm_role.principal_arn
        assert bsm_role.aws_region == bsm_project.aws_region
        assert bsm_role.is_expired() is False
        # 900 seconds: expired with a 20 minute safety margin
        assert bsm_role.is_expired(delta=1200) is True
        _ = bsm_role.aws_account_alias

    def test_assume_role_with_all_options(self, bsm_project):
        bsm_role = bsm_project.assume_role(
            role_arn=get_role_arn(bsm_project, TEST_IAM_ROLE_NAME),
            role_session_name="bsm-unit-test",
            duration_seconds=900,
            tags=[{"Key": "Project", "Value": "boto_session_manager"}],
            transitive_tag_keys=["Project"],
            source_identity="bsm-unit-test",
            region_name="us-west-2",
        )
        assert bsm_role.principal_arn.endswith(
            f":assumed-role/{TEST_IAM_ROLE_NAME}/bsm-unit-test"
        )
        assert bsm_role.aws_region == "us-west-2"

    def test_assume_role_with_external_id(self, bsm_project):
        bsm_role = bsm_project.assume_role(
            role_arn=get_role_arn(bsm_project, TEST_IAM_ROLE_WITH_EXTERNAL_ID_NAME),
            duration_seconds=900,
            external_id=TEST_ROLE_EXTERNAL_ID,
        )
        assert (
            f":assumed-role/{TEST_IAM_ROLE_WITH_EXTERNAL_ID_NAME}/"
            in bsm_role.principal_arn
        )

    def test_assume_role_without_external_id_is_denied(self, bsm_project):
        sts_client = bsm_project.sts_client
        with pytest.raises(sts_client.exceptions.ClientError) as e:
            bsm_project.assume_role(
                role_arn=get_role_arn(bsm_project, TEST_IAM_ROLE_WITH_EXTERNAL_ID_NAME),
                duration_seconds=900,
            )
        assert e.value.response["Error"]["Code"] == "AccessDenied"

    def test_assume_role_auto_refresh(self, bsm_project):
        bsm_role = bsm_project.assume_role(
            role_arn=get_role_arn(bsm_project, TEST_IAM_ROLE_NAME),
            duration_seconds=900,
            auto_refresh=True,
        )
        assert f":assumed-role/{TEST_IAM_ROLE_NAME}/" in bsm_role.principal_arn
        # refreshable credentials never expire on the manager side
        assert bsm_role.is_expired(delta=365 * 24 * 3600) is False
        assert bsm_role.default_client_kwargs == bsm_project.default_client_kwargs


class TestAwsCli:
    def test_aws_cli_sees_the_session(self, bsm_project, monkeypatch):
        """
        A subprocess running the AWS CLI acts as the IAM user, then as the
        assumed role, then as neither once the blocks end.
        """
        for name in AWS_CLI_ENV_VARS:
            monkeypatch.delenv(name, raising=False)

        with bsm_project.awscli():
            assert get_caller_arn_via_aws_cli() == bsm_project.principal_arn

        bsm_role = bsm_project.assume_role(
            role_arn=get_role_arn(bsm_project, TEST_IAM_ROLE_NAME),
            duration_seconds=900,
        )
        with bsm_role.awscli():
            assert "AWS_SESSION_TOKEN" in os.environ
            assert get_caller_arn_via_aws_cli() == bsm_role.principal_arn

        for name in AWS_CLI_ENV_VARS:
            assert name not in os.environ

    def test_temp_snapshot_across_processes(self, bsm_project, monkeypatch, tmp_path):
        """
        Inside another session's awscli() block, the default session is that
        session, but the snapshot still gives back the original one.
        """
        for name in AWS_CLI_ENV_VARS:
            monkeypatch.delenv(name, raising=False)
        path = tmp_path / "snapshot.json"

        bsm_role = bsm_project.assume_role(
            role_arn=get_role_arn(bsm_project, TEST_IAM_ROLE_NAME),
            duration_seconds=900,
        )
        with bsm_role.temp_snapshot(path=path):
            with bsm_project.awscli():
                assert BotoSesManager().principal_arn == bsm_project.principal_arn
                bsm_origin = BotoSesManager.from_snapshot_file(path)
                assert bsm_origin.principal_arn == bsm_role.principal_arn
        assert path.exists() is False


if __name__ == "__main__":
    from boto_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "boto_session_manager.manager",
        preview=False,
    )
