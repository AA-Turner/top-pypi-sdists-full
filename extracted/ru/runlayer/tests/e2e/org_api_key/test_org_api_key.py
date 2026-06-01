from tests.e2e.conftest import strip_ansi

from runlayer_cli.main import app


def test_add_list_remove_lifecycle(runner, runlayer_home):
    """runlayer org-api-key add → list → remove → list"""
    host = "http://localhost:9999"

    result = runner.invoke(
        app,
        ["--host", host, "org-api-key", "add", "mykey", "--secret", "rl_org_test123"],
    )
    assert result.exit_code == 0
    assert "saved" in strip_ansi(result.output)

    result = runner.invoke(app, ["--host", host, "org-api-key", "list"])
    assert result.exit_code == 0
    assert "mykey" in result.output

    result = runner.invoke(app, ["--host", host, "org-api-key", "remove", "mykey"])
    assert result.exit_code == 0
    assert "removed" in strip_ansi(result.output)

    result = runner.invoke(app, ["--host", host, "org-api-key", "list"])
    assert result.exit_code == 0
    assert "No org API keys" in result.output


def test_remove_nonexistent(runner, runlayer_home):
    """runlayer org-api-key remove <name>"""
    host = "http://localhost:9999"
    result = runner.invoke(
        app, ["--host", host, "org-api-key", "remove", "nonexistent"]
    )
    assert result.exit_code == 0
    assert "No org API key" in strip_ansi(result.output)


def test_list_empty(runner, runlayer_home):
    """runlayer org-api-key list"""
    host = "http://localhost:9999"
    result = runner.invoke(app, ["--host", host, "org-api-key", "list"])
    assert result.exit_code == 0
    assert "No org API keys" in result.output
