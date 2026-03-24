import importlib
import json
import os
import pkgutil

import localstack_cli.utils.container_utils.docker_cmd_client
import pytest
import requests
from click.testing import CliRunner
from localstack_cli import config, constants
from localstack_cli.cli.localstack import localstack as cli
from localstack_cli.config import in_docker
from localstack_cli.constants import MODULE_MAIN_PATH
from localstack_cli.utils.bootstrap import in_ci
from localstack_cli.utils.common import poll_condition
from localstack_cli.utils.files import mkdir
from localstack_cli.utils.run import run, to_str


@pytest.fixture
def runner():
    return CliRunner()


def container_exists(client, container_name):
    try:
        container_id = client.get_container_id(container_name)
        return True if container_id else False
    except Exception:
        return False


@pytest.fixture(autouse=True)
def container_client():
    client = localstack_cli.utils.container_utils.docker_cmd_client.CmdDockerClient()

    yield client

    try:
        client.stop_container(config.MAIN_CONTAINER_NAME, timeout=5)
    except Exception:
        pass

    # wait until container has been removed
    assert poll_condition(
        lambda: not container_exists(client, config.MAIN_CONTAINER_NAME), timeout=20
    )


@pytest.mark.skipif(condition=in_docker(), reason="cannot run CLI tests in docker")
class TestCliContainerLifecycle:
    def test_start_wait_stop(self, runner, container_client, monkeypatch, caplog):
        monkeypatch.setenv("DEBUG", "1")
        result = runner.invoke(cli, ["start", "-d"])
        assert result.exit_code == 0
        assert "starting LocalStack" in result.output

        # ensure that all entrypoints could be imported
        assert "error importing entrypoint" not in caplog.text

        result = runner.invoke(cli, ["wait", "-t", "180"])
        assert result.exit_code == 0

        assert container_client.is_container_running(config.MAIN_CONTAINER_NAME), (
            "container name was not running after wait"
        )

        health = requests.get(config.internal_service_url() + "/_localstack/health")
        assert health.ok, f"health request did not return OK: {health.text}"

        result = runner.invoke(cli, ["stop"])
        assert result.exit_code == 0

        with pytest.raises(requests.ConnectionError):
            requests.get(config.internal_service_url() + "/_localstack/health")

    def test_wait_timeout_raises_exception(self, runner, container_client):
        # assume a wait without start fails
        result = runner.invoke(cli, ["wait", "-t", "0.5"])
        assert result.exit_code != 0

    def test_logs(self, runner, container_client):
        result = runner.invoke(cli, ["logs"])
        assert result.exit_code != 0

        runner.invoke(cli, ["start", "-d"])
        runner.invoke(cli, ["wait", "-t", "180"])

        result = runner.invoke(cli, ["logs"])
        assert constants.READY_MARKER_OUTPUT in result.output

    def test_status_services(self, runner):
        result = runner.invoke(cli, ["status", "services"])
        assert result.exit_code != 0
        assert "could not connect to LocalStack health endpoint" in result.output

        runner.invoke(cli, ["start", "-d"])
        runner.invoke(cli, ["wait", "-t", "180"])

        result = runner.invoke(cli, ["status", "services"])

        # just a smoke test
        assert "dynamodb" in result.output
        for line in result.output.splitlines():
            if "dynamodb" in line:
                assert "available" in line

    def test_custom_docker_flags(self, runner, tmp_path, monkeypatch, container_client):
        volume = tmp_path / "volume"
        volume.mkdir()

        monkeypatch.setattr(config, "DOCKER_FLAGS", f"-p 42069 -v {volume}:{volume}")

        runner.invoke(cli, ["start", "-d"])
        runner.invoke(cli, ["wait", "-t", "180"])

        inspect = container_client.inspect_container(config.MAIN_CONTAINER_NAME)
        assert "42069/tcp" in inspect["HostConfig"]["PortBindings"]
        assert f"{volume}:{volume}" in inspect["HostConfig"]["Binds"]

    def test_volume_dir_mounted_correctly(self, runner, tmp_path, monkeypatch, container_client):
        volume_dir = tmp_path / "volume"

        # set different directories and make sure they are mounted correctly
        monkeypatch.setenv("LOCALSTACK_VOLUME_DIR", str(volume_dir))
        monkeypatch.setattr(config, "VOLUME_DIR", str(volume_dir))

        runner.invoke(cli, ["start", "-d"])
        runner.invoke(cli, ["wait", "-t", "60"])

        # check that mounts were created correctly
        inspect = container_client.inspect_container(config.MAIN_CONTAINER_NAME)
        binds = inspect["HostConfig"]["Binds"]
        assert f"{volume_dir}:{constants.DEFAULT_VOLUME_DIR}" in binds

    def test_container_starts_non_root(self, runner, monkeypatch, container_client):
        user = "localstack"
        monkeypatch.setattr(config, "DOCKER_FLAGS", f"--user={user}")

        if in_ci() and os.path.exists("/home/runner"):
            volume_dir = "/home/runner/.cache/localstack/volume/"
            mkdir(volume_dir)
            run(["sudo", "chmod", "-R", "777", volume_dir])

        runner.invoke(cli, ["start", "-d"])
        runner.invoke(cli, ["wait", "-t", "180"])

        cmd = ["awslocal", "stepfunctions", "list-state-machines"]
        output = container_client.exec_in_container(config.MAIN_CONTAINER_NAME, cmd)
        result = json.loads(output[0])
        assert "stateMachines" in result

        output = container_client.exec_in_container(config.MAIN_CONTAINER_NAME, ["ps", "-fu", user])
        assert "localstack-supervisor" in to_str(output[0])

@pytest.mark.skip(reason="TODO: fix test setup - extensions tests need investigation")
class TestExtensionsCli:
    def test_extensions_install_with_IMAGE_NAME_installs_correct_venv_version(
        self, runner, tmp_path, monkeypatch
    ):
        from localstack_cli.pro.core.cli.extensions import extensions as extensions_cli

        volume_dir = tmp_path / "volume"
        monkeypatch.setattr(config, "VOLUME_DIR", str(volume_dir))

        # define an image version with an older Python version
        monkeypatch.setenv("IMAGE_NAME", "localstack/localstack-pro:4.8.1")

        runner.invoke(extensions_cli, ["install", "localstack-extension-hello-world"])

        # check that the venv for the extensions was created with Python 3.11
        python_bin = volume_dir / "lib" / "extensions" / "python_venv" / "lib" / "python3.11"
        assert python_bin.exists(), f"Python 3.11 venv not found at {python_bin}"

    def test_extensions_list_without_image_name_or_auth_env(self, runner, tmp_path, monkeypatch):
        from localstack_cli.pro.core import config as pro_config
        from localstack_cli.pro.core.bootstrap.auth import get_auth_cache
        from localstack_cli.pro.core.cli.extensions import extensions as extensions_cli

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
        cache = get_auth_cache()
        cache["LOCALSTACK_AUTH_TOKEN"] = token
        cache.save()

        # make sure that the extensions list command works properly by
        # defaulting to the Pro image even though IMAGE_NAME and
        # LOCALSTACK_AUTH_TOKEN are not set
        result = runner.invoke(extensions_cli, ["list"])
        assert result.exit_code == 0


class TestImports:
    def test_cli_imports_from_bootstrap(self):
        """
        Simple test to assert we can import different code paths within the `bootstrap` module with
        different Python versions (covered by CLI tests which are parametrized with different versions).
        """
        from localstack_cli.pro.core import bootstrap

        def import_all_recursively(module):
            module_path = getattr(module, "__path__", None)
            if not module_path:
                return
            for loader, name, is_pkg in pkgutil.walk_packages(module_path):
                sub_module = importlib.import_module(f"{module.__name__}.{name}")
                import_all_recursively(sub_module)

        import_all_recursively(bootstrap)
