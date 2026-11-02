from agentic_devtools.cli.pull_request_details import _state_value


def test_state_value_skips_missing_nested_values() -> None:
    assert _state_value({"github": None, "repository": "o/r"}, "github.repo", "repository") == "o/r"
