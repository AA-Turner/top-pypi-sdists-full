import json
import re
from functools import partial
from pathlib import Path
from unittest.mock import patch
from uuid import UUID, uuid4

import icechunk
import pytest
import yaml

from . import has_typer

from arraylake import config
from arraylake.token import Auth0UrlCode, AuthProviderConfig, TokenHandler
from arraylake.types import UserInfo


@pytest.fixture(scope="session")
def invoke():
    if not has_typer:
        pytest.skip("requires typer")

    from typer.testing import CliRunner

    from arraylake.cli.main import app

    runner = CliRunner()
    i = partial(runner.invoke, app)
    return i


def test_cli_version(invoke) -> None:
    result = invoke(["--version"])
    assert result.exit_code == 0
    assert "arraylake, version " in result.output


def test_cli_diagnostics(invoke) -> None:
    result = invoke(["--diagnostics"])
    assert result.exit_code == 0
    assert "python" in result.output
    assert "arraylake" in result.output


def test_help(invoke) -> None:
    result = invoke(["--help"])
    assert result.exit_code == 0
    assert all([cmd in result.output for cmd in ("auth", "config", "repo", "compute", "--version", "--config", "--help")]), result.output


def test_repo(invoke, helpers, sync_isolated_org_with_bucket) -> None:
    org_name, bucket_id = sync_isolated_org_with_bucket()
    _o_origin_name = helpers.random_repo_id()
    repo_name = f"{org_name}/{_o_origin_name}"

    result = invoke(["repo", "list", org_name])
    assert result.exit_code == 0
    assert "No results" in result.stdout
    assert "──────────────" not in result.stdout

    result = invoke(["repo", "--help"])
    assert result.exit_code == 0
    assert all([cmd in result.output for cmd in ("create", "delete", "list", "--help")]), result.output

    result = invoke(["repo", "create", repo_name, "--bucket-config-nickname", "bad-bucket"])
    assert result.exit_code > 0
    assert f"bucket bad-bucket does not exist" in result.output

    # without a bucket nickname (uses default bucket)
    result = invoke(["repo", "create", repo_name])
    assert result.exit_code == 0, result.output

    # We need to skip over console control characters to match strings
    assert re.search(f"Creating repo.+{repo_name}.+succeeded", result.output)

    # Server returns the existing repo idempotently, but icechunk fails because
    # the storage prefix already has data. The client's error handler deletes the
    # metastore entry as cleanup. In practice this only happens on HTTP retries
    # where the first request actually succeeded.
    result = invoke(["repo", "create", repo_name])
    assert result.exit_code != 0
    assert "clean prefixes" in result.output

    # Re-create since the failed duplicate cleaned up the metastore entry
    result = invoke(["repo", "create", repo_name])
    assert result.exit_code == 0

    # TODO: test this on a populated repo
    result = invoke(["repo", "tree", repo_name])
    assert result.exit_code == 0
    assert "Repo is empty" in result.stdout

    result = invoke(["repo", "list", org_name])
    assert result.exit_code == 0
    # We need to skip over console control characters to match strings
    assert re.search(f"Listing repos for.+{org_name}.+succeeded", result.stdout)
    assert all([cmd in result.stdout for cmd in (org_name, _o_origin_name, "Created")])
    # check table is expected width
    for line in result.stdout.split("\n")[2:-1]:
        assert len(line) >= 80, line

    result = invoke(["repo", "list", "--output", "json", org_name])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert len(data) == 1
    assert all([key in data[0] for key in ("org", "name", "created", "description")])
    assert data[0]["org"] == org_name
    assert data[0]["name"] == _o_origin_name

    result = invoke(["repo", "get-status", repo_name])
    assert result.exit_code == 0
    data = result.stdout
    assert data.startswith("online")

    result = invoke(["repo", "get-status", repo_name, "--output", "json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["mode"] == "online"

    # set-status sets the mode via PUT (succeeds) then calls get_repo_object to
    # display the result.  For HMAC repos, get_repo_object is now blocked when
    # the repo is not online (409), so the CLI command exits with an error even
    # though the mode was successfully changed.
    result = invoke(["repo", "set-status", repo_name, "offline"])
    assert result.exit_code != 0

    result = invoke(["repo", "set-status", repo_name, "maintenance", "--output", "json"])
    assert result.exit_code != 0

    # Restore to online before deleting
    result = invoke(["repo", "set-status", repo_name, "online"])
    assert result.exit_code == 0

    result = invoke(["repo", "delete", repo_name, "--confirm"])
    assert result.exit_code == 0
    # We need to skip over console control characters to match strings
    assert re.search(f"Deleting repo.+{repo_name}.+succeeded", result.stdout)

    result = invoke(["repo", "create", repo_name])
    assert result.exit_code == 0

    result = invoke(["repo", "delete", repo_name], input="y\n")
    assert result.exit_code == 0
    assert re.search(f"Deleting repo.+{repo_name}.+succeeded", result.stdout)

    # deleting again should be idempotent (server returns 204)
    result = invoke(["repo", "delete", repo_name], input="y\n")
    assert result.exit_code == 0

    # list empty org
    result = invoke(["repo", "list", "--output", "json", org_name])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data == []


def test_repo_import(invoke, sync_isolated_org_with_bucket) -> None:
    org_name, _ = sync_isolated_org_with_bucket()
    repo_name = f"{org_name}/imported-repo"
    bucket_nickname = "test_bucket"  # default nickname from default_bucket fixture

    # Create icechunk repo directly outside of arraylake
    repo_prefix = str(uuid4())[:8]
    ic_storage = icechunk.s3_storage(
        bucket="testbucket",
        prefix=repo_prefix,
        region="us-east-1",
        endpoint_url="http://localhost:9000",
        allow_http=True,
        access_key_id="minio123",
        secret_access_key="minio123",
        force_path_style=True,
    )
    icechunk.Repository.create(storage=ic_storage)

    # Test the CLI import command
    result = invoke(["repo", "import", repo_name, bucket_nickname, repo_prefix])
    assert result.exit_code == 0, result.output
    assert re.search(f"Importing repo.+{repo_name}.+succeeded", result.output)

    # Verify repo exists
    result = invoke(["repo", "list", org_name, "--output", "json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert any(r["name"] == "imported-repo" for r in data)


def test_list_repo_bad_org(invoke):
    result = invoke(["repo", "list", "foo123"])
    assert result.exit_code >= 1
    assert "foo123 not found" in result.output


def test_list_repos_empty_org(invoke, org_name):
    result = invoke(["repo", "list", org_name, "--output", "json"])
    assert result.exit_code == 0
    assert json.loads(result.stdout) == []

    result = invoke(["repo", "list", org_name])
    assert result.exit_code == 0
    assert "No results" in result.stdout
    assert "──────────────" not in result.stdout


def test_create_modify_repo_metadata(invoke, sync_isolated_org_with_bucket) -> None:
    org_name, _ = sync_isolated_org_with_bucket()

    # Create a repo with metadata and description
    repo_name_1 = f"{org_name}/foo"
    description = "This is a test repo"
    metadata = {"foo": "bar", "baz": 123}
    result = invoke(["repo", "create", repo_name_1, "--description", description, "--metadata", json.dumps(metadata)])
    assert result.exit_code == 0

    # Create a repo with no metadata
    repo_name_2 = f"{org_name}/bar"
    result = invoke(["repo", "create", repo_name_2])
    assert result.exit_code == 0

    # List repos and filter on metadata
    result = invoke(["repo", "list", org_name, "--output", "json"])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 2

    result = invoke(["repo", "list", org_name, "--output", "json", "--filter-metadata", '{"foo": "bar"}'])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 1

    # Check that we can list with a table output
    result = invoke(["repo", "list", org_name])
    assert result.exit_code == 0

    # Modify metadata and description
    new_description = "This is an updated test repo"
    update_metadata = {"foo": "baz"}
    add_metadata = {"qux": 456}
    result = invoke(
        [
            "repo",
            "modify",
            repo_name_1,
            "--description",
            new_description,
            "--update-metadata",
            json.dumps(update_metadata),
            "--remove-metadata",
            "baz",
            "--add-metadata",
            json.dumps(add_metadata),
        ]
    )
    assert result.exit_code == 0

    # Verify the metadata was updated
    result = invoke(["repo", "list", org_name, "--output", "json", "--filter-metadata", '{"foo": "baz", "qux": 456}'])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert len(data) == 1


def test_config(invoke, temp_config_file) -> None:
    result = invoke(["config", "--help"])
    assert result.exit_code == 0
    assert all([cmd in result.output for cmd in ("init", "get", "set", "unset", "list", "--help")]), result.output

    result = invoke(["config", "list", "--output", "json", "--path", str(temp_config_file)])
    assert result.exit_code == 0
    orig_config = json.loads(result.stdout)

    result = invoke(["config", "set", "foo", "bar", "--path", str(temp_config_file)])
    assert result.exit_code == 0
    with temp_config_file.open() as f:
        data = yaml.safe_load(f)
    assert data["foo"] == "bar"

    result = invoke(["config", "unset", "foo", "--path", str(temp_config_file)])
    assert result.exit_code == 0
    with temp_config_file.open() as f:
        data = yaml.safe_load(f)
    assert "foo" not in data
    assert orig_config == data

    result = invoke(["config", "list"])
    assert result.exit_code == 0

    result = invoke(["config", "list", "--path", str(temp_config_file)])
    assert result.exit_code == 0

    result = invoke(["--config", "foo=bar", "config", "list"])
    assert result.exit_code == 0
    assert "foo" in result.output

    result = invoke(["config", "get", "service.uri", "--path", str(temp_config_file)])
    assert result.exit_code == 0
    assert "http" in result.output


def test_config_init(invoke, tmpdir):
    temp_file = tmpdir / "config.yaml"
    c = config.collect(paths=[temp_file])

    result = invoke(["config", "init", "--help"])

    result = invoke(
        ["config", "init", "--path", str(temp_file)],
        input="\n".join(["s3://foobar"]),
    )
    assert result.exit_code == 0
    assert "Config file updated" in result.output


def test_config_set_empty_file(invoke, tmpdir):
    fname = Path(tmpdir) / "config.yaml"
    fname.touch()

    result = invoke(["config", "set", "foo", "bar", "--path", str(fname)])
    assert result.exit_code == 0


def test_auth(invoke, test_token_file, helpers) -> None:
    result = invoke(["auth", "--help"])
    assert result.exit_code == 0
    for cmd in ["login", "logout", "refresh", "status", "token"]:
        assert cmd in result.stdout

    test_tokens = helpers.oauth_tokens_from_file(test_token_file)
    test_token_file.unlink()
    refreshed_tokens = test_tokens.model_copy(update={"id_token": "123456789abcdefg"})

    class MockTokenHandler(TokenHandler):
        async def get_authorize_info(self) -> Auth0UrlCode:
            return Auth0UrlCode(url="https://foo.auth0.com", user_code="sample-code", device_code="12345", interval=1, expires_in=100)

        async def get_token(self, device_code: str, interval: int, expires_in: int):
            self.update(test_tokens)

        async def refresh_token(self):
            self.update(refreshed_tokens)

        async def _logout(self):
            pass  # skip calling out to auth0

        async def _get_user(self) -> UserInfo:
            return UserInfo(
                id=UUID("aeeb8bfa-e8f4-4724-9427-c3d5af661900"),
                email="spam@foo.com",
                first_name="TestFirst",
                family_name="TestFamily",
            )

        async def _update_user_profile(self) -> UserInfo:
            return UserInfo(
                id=UUID("aeeb8bfa-e8f4-4724-9427-c3d5af661900"),
                email="spam@foo.com",
                first_name="TestFirst",
                family_name="TestFamily",
            )

    def get_auth_handler(api_endpoint: str):
        return MockTokenHandler(api_endpoint=api_endpoint)

    with patch("arraylake.cli.auth.get_auth_handler", get_auth_handler), patch("arraylake.token.open_new") as mock_open_new:
        result = invoke(["auth", "login"], input="sample-code-12345")
        assert mock_open_new.call_count == 1  # check that browser was opened
        assert result.exit_code == 0
        assert test_tokens == helpers.oauth_tokens_from_file(test_token_file)
        assert "spam@foo.com" in result.stdout

        result = invoke(["auth", "logout"])
        assert result.exit_code == 0
        assert not test_token_file.is_file()
        assert mock_open_new.call_count == 1  # check that browser was not opened

        result = invoke(["auth", "login", "--no-browser"], input="sample-code-12345")
        assert result.exit_code == 0
        assert test_tokens == helpers.oauth_tokens_from_file(test_token_file)
        assert "spam@foo.com" in result.stdout

        result = invoke(["auth", "logout"])
        assert result.exit_code == 0
        assert not test_token_file.is_file()

        result = invoke(["auth", "login", "--nobrowser"], input="sample-code-12345")
        assert result.exit_code == 0
        assert test_tokens == helpers.oauth_tokens_from_file(test_token_file)
        assert "spam@foo.com" in result.stdout

        result = invoke(["auth", "refresh"])
        assert result.exit_code == 0
        assert refreshed_tokens.model_dump() == helpers.oauth_tokens_from_file(test_token_file).model_dump()

        result = invoke(["auth", "status"])
        assert result.exit_code == 0
        assert "spam@foo.com" in result.stdout

        result = invoke(["auth", "token"])
        assert result.exit_code == 0
        assert refreshed_tokens.id_token in result.output

        result = invoke(["auth", "logout"])
        assert result.exit_code == 0
        assert not test_token_file.is_file()


def test_auth_login_with_failed_refresh(invoke, test_token_file, helpers) -> None:
    test_tokens = helpers.oauth_tokens_from_file(test_token_file)

    user_code = "sample-code-12345"
    device_code = "12345"

    class MockTokenHandler(TokenHandler):
        refresh_count = 0  # keep track of how many times refresh_token was called

        @property
        def auth_provider_config(self) -> AuthProviderConfig:
            return AuthProviderConfig(domain="foo.auth0.com", client_id="bar")

        async def get_authorize_info(self) -> Auth0UrlCode:
            return Auth0UrlCode(url="https://foo.auth0.com", user_code=user_code, device_code=device_code, interval=1, expires_in=100)

        async def get_token(self, device_code: str, interval: int, expires_in: int):
            assert device_code == device_code
            self.update(test_tokens)

        async def refresh_token(self):
            MockTokenHandler.refresh_count += 1
            raise ValueError("Failed to refresh token")

        async def _get_user(self) -> UserInfo:
            return UserInfo(
                id=UUID("aeeb8bfa-e8f4-4724-9427-c3d5af661900"),
                email="spam@foo.com",
                first_name="TestFirst",
                family_name="TestFamily",
            )

        async def _update_user_profile(self) -> UserInfo:
            return UserInfo(
                id=UUID("aeeb8bfa-e8f4-4724-9427-c3d5af661900"),
                email="spam@foo.com",
                first_name="TestFirst",
                family_name="TestFamily",
            )

    def get_auth_handler(api_endpoint: str):
        return MockTokenHandler(api_endpoint=api_endpoint)

    with patch("arraylake.cli.auth.get_auth_handler", get_auth_handler), patch("arraylake.token.open_new") as mock_open_new:
        result = invoke(["auth", "login"], input="sample-code-12345")
        assert result.exit_code == 0
        assert test_tokens == helpers.oauth_tokens_from_file(test_token_file)
        assert "spam@foo.com" in result.stdout
        assert MockTokenHandler.refresh_count == 1  # check that we called refresh
        assert mock_open_new.call_count == 1  # check that browser was opened


@pytest.mark.parametrize("cmd", ["refresh", "token", "status"])
def test_auth_commands_that_require_login(invoke, cmd, test_token_file) -> None:
    test_token_file.unlink()
    # all of these commands should raise an error if not logged in
    result = invoke(["auth", cmd])
    assert result.exit_code != 0
    assert "Not logged in" in result.stdout
