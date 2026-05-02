from click.testing import CliRunner
from spred.main import cli

def test_cli_runs():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
