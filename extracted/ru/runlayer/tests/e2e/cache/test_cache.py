from runlayer_cli.main import app


def test_cache_clear_no_cache(runner, runlayer_home):
    """runlayer cache clear"""
    result = runner.invoke(app, ["cache", "clear"])
    assert result.exit_code == 0
    assert "does not exist" in result.output


def test_cache_clear_with_cache(runner, runlayer_home):
    """runlayer cache clear"""
    cache_dir = runlayer_home / "oauth-mcp-client-cache"
    cache_dir.mkdir()
    (cache_dir / "token.json").write_text("{}")

    result = runner.invoke(app, ["cache", "clear"])
    assert result.exit_code == 0
    assert "Removed" in result.output
    assert not cache_dir.exists()
