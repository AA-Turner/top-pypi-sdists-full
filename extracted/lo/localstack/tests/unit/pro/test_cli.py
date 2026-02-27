import click
import pytest
from click.testing import CliRunner
from localstack_cli.cli.localstack import create_with_plugins
from localstack_cli.utils import bootstrap

cli: click.Group


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def set_auth_token_configured(monkeypatch):
    monkeypatch.setattr(bootstrap, "is_auth_token_configured", lambda: True)
    from localstack_cli.pro.core.bootstrap.licensingv2 import LicensedLocalstackEnvironment

    monkeypatch.setattr(LicensedLocalstackEnvironment, "activate_license", lambda x: None)


@pytest.fixture
def state_pod_no_op(monkeypatch):
    def _no_op(_sef, *args, **kwargs):
        return True

    def _reachable():
        return

    from localstack_cli.pro.core.bootstrap.pods_client import CloudPodsClient, StateService
    from localstack_cli.pro.core.cli import cli

    monkeypatch.setattr(cli, "_assert_host_reachable", _reachable)
    monkeypatch.setattr(CloudPodsClient, "load", _no_op)
    monkeypatch.setattr(StateService, "export_pod", _no_op)
    monkeypatch.setattr(StateService, "import_pod", _no_op)


@pytest.mark.skip(reason="Test not working in standalone CLI")
def test_load_from_platform_no_login_with_key(runner, state_pod_no_op, set_auth_token_configured):
    """
    Test that it is possible to use Pro cloud pods commands without being logged in, but with configured API key.
    """
    localstack_cli = create_with_plugins()
    result = runner.invoke(localstack_cli.group, ["pod", "load", "my-pod"])
    assert "successfully" in result.output
    assert result.exit_code == 0


@pytest.mark.skip(reason="Test not working in standalone CLI")
def test_export_state(runner, state_pod_no_op, set_auth_token_configured, tmp_path):
    p = tmp_path / "pod.txt"
    p.write_text("test")
    localstack_cli = create_with_plugins()
    result = runner.invoke(localstack_cli.group, ["state", "export", f"{p}"])
    assert "successfully" in result.output
    assert result.exit_code == 0


@pytest.mark.skip(reason="Test not working in standalone CLI")
def test_import_state(runner, state_pod_no_op, tmp_path, set_auth_token_configured):
    p = tmp_path / "pod.txt"
    p.write_text("test")
    localstack_cli = create_with_plugins()
    result = runner.invoke(localstack_cli.group, ["state", "import", f"{p}"])
    assert "successfully" in result.output
    assert result.exit_code == 0
