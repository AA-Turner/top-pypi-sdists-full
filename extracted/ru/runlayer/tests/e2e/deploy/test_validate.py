from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app


def test_validate_valid_yaml(runner, cli_args, api_client, tmp_path, unique_id, cleanup_deployments):
    """runlayer deploy validate --config <path>"""
    deployment = api_client.create_deployment(f"e2e-validate-{unique_id}")
    cleanup_deployments.append(deployment.id)

    yaml_content = (
        f"id: {deployment.id}\n"
        f"name: e2e-validate-{unique_id}\n"
        "runtime: docker\n"
        "image: nginx:latest\n"
        "service:\n"
        "  port: 8080\n"
    )
    config = tmp_path / "runlayer.yaml"
    config.write_text(yaml_content)

    result = runner.invoke(
        app, [*cli_args, "deploy", "validate", "--config", str(config)]
    )
    output = strip_ansi(result.output)
    assert result.exit_code == 0, result.output
    assert "valid" in output.lower()

    api_client.delete_deployment(deployment.id)


def test_validate_invalid_yaml(runner, cli_args, tmp_path):
    """runlayer deploy validate --config <path>"""
    config = tmp_path / "runlayer.yaml"
    config.write_text("not: valid: deployment: yaml\n  broken")

    result = runner.invoke(
        app, [*cli_args, "deploy", "validate", "--config", str(config)]
    )
    assert result.exit_code != 0


def test_validate_missing_file(runner, cli_args, tmp_path):
    """runlayer deploy validate --config <path>"""
    result = runner.invoke(
        app,
        [*cli_args, "deploy", "validate", "--config", str(tmp_path / "nope.yaml")],
    )
    assert result.exit_code != 0
