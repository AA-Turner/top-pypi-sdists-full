import os

from click.testing import CliRunner
from localstack_cli import config
from localstack_cli.pro.core import config as pro_config
from localstack_cli.pro.core.cli.extensions import extensions as extensions_cli


def test_extensions_install_with_IMAGE_NAME_installs_correct_venv_version(tmp_path, monkeypatch):
    volume_dir = tmp_path / "volume"
    monkeypatch.setattr(config, "VOLUME_DIR", str(volume_dir))

    # define an image version with an older Python version
    monkeypatch.setenv("IMAGE_NAME", "localstack/localstack-pro:4.8.1")

    runner = CliRunner()
    runner.invoke(extensions_cli, ["install", "localstack-extension-hello-world"])

    # check that the venv for the extensions was created with Python 3.11
    python_bin = volume_dir / "lib" / "extensions" / "python_venv" / "lib" / "python3.11"
    assert python_bin.exists(), f"Python 3.11 venv not found at {python_bin}"


def test_extensions_list_without_image_name_or_auth_env(tmp_path, monkeypatch):
    # explicitly declare this is the CLI and unset a potential IMAGE_NAME
    monkeypatch.setenv("LOCALSTACK_CLI", "1")
    monkeypatch.setenv("IMAGE_NAME", "")

    # extract the auth token from the test environment
    token = os.environ.get("LOCALSTACK_AUTH_TOKEN")

    # unset all auth token env vars
    monkeypatch.setenv("LOCALSTACK_AUTH_TOKEN", "")
    monkeypatch.setenv("LOCALSTACK_API_KEY", "")

    # create a temporary auth cache file
    tmp_auth_cache_path = tmp_path / "auth.json"
    monkeypatch.setattr(pro_config, "AUTH_CACHE_PATH", str(tmp_auth_cache_path))

    # set the token in the temp auth cache
    from localstack_cli.pro.core.bootstrap.auth import get_auth_cache

    cache = get_auth_cache()
    cache["LOCALSTACK_AUTH_TOKEN"] = token
    cache.save()

    # make sure that the extensions list command works properly by
    # defaulting to the Pro image even though IMAGE_NAME and
    # LOCALSTACK_AUTH_TOKEN are not set
    runner = CliRunner()
    result = runner.invoke(extensions_cli, ["list"])
    assert result.exit_code == 0
