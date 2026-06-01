from runlayer_cli.main import app


def test_scan_dry_run(runner, cli_args):
    """runlayer scan --dry-run --no-projects"""
    result = runner.invoke(app, [*cli_args, "scan", "--dry-run", "--no-projects"])
    assert result.exit_code == 0
