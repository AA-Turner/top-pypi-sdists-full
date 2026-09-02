from runlayer_cli.main import app
from runlayer_cli.aiwatch import app as aiwatch_app


def test_version_flag(runner):
    """runlayer --version"""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "runlayer version" in result.output


def test_aiwatch_version_flag(runner):
    """aiwatch --version"""
    result = runner.invoke(aiwatch_app, ["--version"])
    assert result.exit_code == 0
    assert "aiwatch version" in result.output


def test_aiwatch_version_short_flag(runner):
    """aiwatch -v"""
    result = runner.invoke(aiwatch_app, ["-v"])
    assert result.exit_code == 0
    assert "aiwatch version" in result.output
