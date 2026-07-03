import importlib.metadata as m

from typer.testing import CliRunner

from pymupdf4llm_mcp.cli import app


def test_cli_version_flag_outputs_package_version():
    runner = CliRunner()
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == m.version("pymupdf4llm-mcp")
