from agentic_devtools.ai_providers.copilot_discovery import _default_warn


def test_prints_the_warning_to_stderr(capsys) -> None:
    _default_warn("discovery failed")

    captured = capsys.readouterr()
    assert "discovery failed" in captured.err
    assert captured.out == ""
