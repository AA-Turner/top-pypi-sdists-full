import pytest

from localstack_cli.cli.exceptions import CLIError
from localstack_cli.pro.core.cli.replicator import (
    ProfileLoadError,
    get_config_from_profile,
    get_source_config,
    get_awscli_config,
)
from localstack_cli.utils.strings import short_uid


@pytest.fixture
def profile_name():
    return f"profile-{short_uid()}"


@pytest.fixture
def access_key_id():
    return f"access-key-{short_uid()}"


@pytest.fixture
def secret_key():
    return f"secret-key-{short_uid()}"


@pytest.fixture
def profile_region():
    return "us-east-7"


@pytest.fixture
def profile_dir(tmpdir, access_key_id, secret_key, profile_name, profile_region):
    config_path = tmpdir / "config"
    credentials_path = tmpdir / "credentials"

    config = f"""[profile {profile_name}]
region = {profile_region}
"""

    credentials = f"""[{profile_name}]
aws_access_key_id = {access_key_id}
aws_secret_access_key = {secret_key}
"""

    with config_path.open("w") as outfile:
        outfile.write(config)

    with credentials_path.open("w") as outfile:
        outfile.write(credentials)

    return tmpdir


def test_load_profile_from_config_file(
    profile_name, profile_dir, profile_region, access_key_id, secret_key
):
    config = get_config_from_profile(profile_name, profile_dir)

    assert config["aws_access_key_id"] == access_key_id
    assert config["aws_secret_access_key"] == secret_key
    assert config.get("aws_session_token") is None
    assert config["region_name"] == profile_region
    assert config["profile_name"] == profile_name


def test_load_missing_profile(tmpdir, profile_dir):
    invalid_profile_name = f"profile-{short_uid()}"
    with pytest.raises(ProfileLoadError) as exc_info:
        get_config_from_profile(invalid_profile_name, profile_dir)

    assert str(exc_info.value) == f"Could not find profile '{invalid_profile_name}'"


def test_envars_override_profile(profile_dir, profile_name, monkeypatch):
    monkeypatch.setenv("AWS_PROFILE", profile_name)

    test_access_key = short_uid()
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", test_access_key)
    test_secret_key = short_uid()
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", test_secret_key)
    test_region = short_uid()
    monkeypatch.setenv("AWS_DEFAULT_REGION", test_region)

    env = get_source_config(profile_dir=profile_dir)

    assert env.get("aws_access_key_id") == test_access_key
    assert env.get("aws_secret_access_key") == test_secret_key
    assert env.get("region_name") == test_region


def test_envars_partial_override_profile(
    access_key_id, profile_dir, profile_name, profile_region, monkeypatch
):
    monkeypatch.setenv("AWS_PROFILE", profile_name)

    test_access_key = short_uid()
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", test_access_key)
    test_secret_key = short_uid()
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", test_secret_key)

    env = get_source_config(profile_dir=profile_dir)

    assert env.get("aws_access_key_id") == test_access_key
    assert env.get("aws_secret_access_key") == test_secret_key
    assert env.get("region_name") == profile_region


def test_envars_partial_override_profile_error(
    access_key_id, profile_dir, profile_name, profile_region, monkeypatch
):
    monkeypatch.setenv("AWS_PROFILE", profile_name)

    test_access_key = short_uid()
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", test_access_key)

    with pytest.raises(CLIError) as e:
        get_source_config(profile_dir=profile_dir)

    assert "Partial credentials found in env" in e.value.message


def test_loading_from_aws_cli(
    profile_name, profile_dir, profile_region, access_key_id, secret_key, monkeypatch
):
    monkeypatch.setenv("AWS_CONFIG_FILE", str(profile_dir / "config"))
    monkeypatch.setenv("AWS_SHARED_CREDENTIALS_FILE", str(profile_dir / "credentials"))
    monkeypatch.setenv("AWS_PROFILE", profile_name)

    config = get_awscli_config()

    assert config["aws_access_key_id"] == access_key_id
    assert config["aws_secret_access_key"] == secret_key
    assert config.get("aws_session_token") is None
    assert config["region_name"] == profile_region
