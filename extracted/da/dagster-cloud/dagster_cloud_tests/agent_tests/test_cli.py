import json
import os
from unittest import mock

import pytest
import yaml
from dagster_cloud.agent.cli import app
from dagster_cloud.workspace.docker import DockerUserCodeLauncher
from dagster_cloud.workspace.user_code_launcher import ProcessUserCodeLauncher
from typer.testing import CliRunner


@pytest.fixture
def token():
    return "agent:hooli:1b2c814969d746b09d9k4d7e6g065cn4"


@pytest.fixture
def deployment():
    return "staging"


@pytest.fixture
def agent_label():
    return "my-agent"


@pytest.fixture
def dagster_config(token, deployment, agent_label):
    return {
        "instance_class": {
            "module": "dagster_cloud.instance",
            "class": "DagsterCloudAgentInstance",
        },
        "dagster_cloud_api": {
            "agent_token": token,
            "deployment": deployment,
            "agent_label": agent_label,
        },
        "user_code_launcher": {
            "module": "dagster_cloud.workspace.docker",
            "class": "DockerUserCodeLauncher",
        },
    }


@pytest.fixture
def dagster_home(tmpdir, dagster_config):
    dagster_yaml = tmpdir / "dagster.yaml"
    dagster_yaml.write_text(yaml.dump(dagster_config), "utf-8")
    return str(tmpdir)


@pytest.fixture
def instance_spy():
    class Spy:
        def __init__(self):
            self._spy = None

        def set(self, obj):
            self._spy = obj

        def __getattr__(self, name):
            return getattr(self._spy, name)

    return Spy()


@pytest.fixture
def runner(instance_spy, tmpdir, monkeypatch):
    # Isolate tests from our local env
    for env in os.environ.keys():
        if env.startswith("DAGSTER_"):
            monkeypatch.setattr("os.environ", {})

    def mock_run_loop(_agent, *args, **kwargs):
        instance_spy.set(_agent._instance)  # noqa: SLF001

    with mock.patch("dagster_cloud.agent.cli.DagsterCloudAgent.run_loop", mock_run_loop):
        yield CliRunner()


# Happy paths
def test_dagster_home_env(runner, monkeypatch, dagster_home, instance_spy, token, deployment):
    monkeypatch.setenv("DAGSTER_HOME", dagster_home)
    result = runner.invoke(app, [])
    assert not result.exit_code
    assert instance_spy.dagster_cloud_agent_token == token


def test_dagster_home_arg(runner, dagster_home, instance_spy, token, deployment):
    result = runner.invoke(app, [dagster_home])
    assert not result.exit_code
    assert instance_spy.dagster_cloud_agent_token == token
    assert instance_spy.deployment_name == deployment


def test_options(runner, instance_spy, token, deployment):
    result = runner.invoke(app, ["--agent-token", token, "--deployment", deployment])
    assert not result.exit_code
    assert instance_spy.dagster_cloud_agent_token == token
    assert instance_spy.deployment_name == deployment


def test_config(runner, instance_spy, dagster_config, token, deployment):
    result = runner.invoke(app, ["--config", json.dumps(dagster_config)])
    assert not result.exit_code
    assert instance_spy.dagster_cloud_agent_token == token
    assert instance_spy.deployment_name == deployment
    assert isinstance(instance_spy.user_code_launcher, DockerUserCodeLauncher)


# Failures
def test_nothing_configured_fails(runner):
    result = runner.invoke(app, [])
    assert result.exit_code
    assert "No directory provided" in result.output


def test_options_incomplete_fails(runner, token, deployment):
    # No deployment
    result = runner.invoke(app, ["--agent-token", token])
    assert result.exit_code
    assert "both an agent token and a deployment" in result.output

    # No agent token
    result = runner.invoke(app, ["--deployment", deployment])
    assert result.exit_code
    assert "both an agent token and a deployment" in result.output


def test_options_and_dagster_home_arg_fails(runner, dagster_home, token, deployment):
    result = runner.invoke(app, [dagster_home, "--agent-token", token, "--deployment", deployment])
    assert result.exit_code
    assert "Cannot supply both" in result.output


def test_config_and_dagster_home_arg_fails(runner, dagster_home, dagster_config):
    result = runner.invoke(app, [dagster_home, "--config", dagster_config])
    assert result.exit_code
    assert "Cannot supply both" in result.output


def test_dagster_cloud_api_config_invalid(runner):
    result = runner.invoke(app, [dagster_home, "--config", json.dumps({"foo": "bar"})])
    assert result.exit_code


# Order of precedence
def test_prefer_options_over_dagster_home_env(
    runner, monkeypatch, instance_spy, dagster_config, dagster_home, token, deployment
):
    monkeypatch.setenv("DAGSTER_HOME", dagster_home)

    overload_deployment = "overload"
    assert overload_deployment != deployment

    result = runner.invoke(app, ["--agent-token", token, "--deployment", overload_deployment])
    assert not result.exit_code
    assert instance_spy.dagster_cloud_agent_token == token
    assert instance_spy.deployment_name == overload_deployment

    # Other config set in dagster.yaml are ignored
    assert dagster_config["dagster_cloud_api"]["agent_label"]
    assert not instance_spy.dagster_cloud_api_agent_label


def test_prefer_dagster_home_arg_over_env(
    runner, monkeypatch, instance_spy, dagster_home, token, deployment
):
    monkeypatch.setenv("DAGSTER_HOME", "/fake/directory")
    result = runner.invoke(app, [dagster_home])
    assert not result.exit_code
    assert instance_spy.dagster_cloud_agent_token == token
    assert instance_spy.deployment_name == deployment


def test_prefer_config_over_dagster_home_env(runner, monkeypatch, instance_spy, dagster_config):
    monkeypatch.setenv("DAGSTER_HOME", "/fake/directory")
    result = runner.invoke(app, ["--config", json.dumps(dagster_config)])
    assert not result.exit_code
    assert (
        instance_spy.dagster_cloud_agent_token == dagster_config["dagster_cloud_api"]["agent_token"]
    )
    assert instance_spy.deployment_name == dagster_config["dagster_cloud_api"]["deployment"]


def test_merge_options_into_config(runner, monkeypatch, instance_spy, dagster_config):
    overload_deployment = "overload"
    assert overload_deployment != dagster_config["dagster_cloud_api"]["deployment"]

    result = runner.invoke(
        app,
        [
            "--config",
            json.dumps(dagster_config),
            "--deployment",
            overload_deployment,
            "--user-code-launcher",
            "dagster_cloud.workspace.user_code_launcher.ProcessUserCodeLauncher",
        ],
        catch_exceptions=False,
    )
    assert not result.exit_code
    assert (
        instance_spy.dagster_cloud_agent_token == dagster_config["dagster_cloud_api"]["agent_token"]
    )
    assert instance_spy.deployment_name == overload_deployment
    assert isinstance(instance_spy.user_code_launcher, ProcessUserCodeLauncher)


# Other options
def test_agent_label(runner, instance_spy, token, deployment):
    label = "test"
    result = runner.invoke(
        app, ["--agent-token", token, "--deployment", deployment, "--agent-label", label]
    )
    assert not result.exit_code
    assert instance_spy.dagster_cloud_api_agent_label == label


def test_launcher_config(runner, instance_spy, token, deployment):
    env_vars = ["FOO", "BAR"]
    config = json.dumps({"env_vars": env_vars})
    result = runner.invoke(
        app,
        [
            "--agent-token",
            token,
            "--deployment",
            deployment,
            "--user-code-launcher",
            "dagster_cloud.workspace.docker.DockerUserCodeLauncher",
            "--user-code-launcher-config",
            config,
        ],
    )
    assert not result.exit_code
    assert isinstance(instance_spy.user_code_launcher, DockerUserCodeLauncher)
    assert instance_spy.user_code_launcher.env_vars == env_vars


@pytest.mark.skip(reason="TODO")
def test_logging_config(runner):
    pass
