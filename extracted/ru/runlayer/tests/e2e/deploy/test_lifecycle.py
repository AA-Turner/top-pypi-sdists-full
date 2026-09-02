import yaml

from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app


def test_deploy_lifecycle(runner, cli_args, api_client, tmp_path, unique_id, cleanup_deployments):
    """runlayer deploy init → pull → destroy"""
    config_path = str(tmp_path / "runlayer.yaml")
    name = f"e2e-{unique_id}"

    result = runner.invoke(
        app,
        [*cli_args, "deploy", "init", "--config", config_path],
        input=f"{name}\n",
    )
    assert result.exit_code == 0, f"init failed: {result.output}"
    assert "Created" in strip_ansi(result.output)

    with open(config_path) as f:
        config = yaml.safe_load(f)
    deployment_id = config.get("id")
    assert deployment_id, f"No id field in created yaml: {config}"

    cleanup_deployments.append(deployment_id)

    pull_path = str(tmp_path / "pulled.yaml")
    result = runner.invoke(
        app,
        [
            *cli_args,
            "deploy",
            "pull",
            "--config",
            pull_path,
            "--deployment-id",
            deployment_id,
        ],
    )
    assert result.exit_code == 0, f"pull failed: {result.output}"

    with open(pull_path) as f:
        pulled = yaml.safe_load(f)
    assert pulled is not None

    deployment = api_client.get_deployment(deployment_id)
    assert deployment.name == name

    result = runner.invoke(
        app,
        [
            *cli_args,
            "deploy",
            "destroy",
            "--deployment-id",
            deployment_id,
        ],
        input="y\n",
    )
    assert result.exit_code == 0, f"destroy failed: {result.output}"
