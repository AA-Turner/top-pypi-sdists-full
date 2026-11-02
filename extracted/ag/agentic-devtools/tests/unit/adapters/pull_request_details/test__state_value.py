from agentic_devtools.adapters.pull_request_details import _state_value


def test_state_value_returns_first_present_key() -> None:
    assert _state_value({"github": {"repo": "o/r"}}, "github.repo", "repository") == "o/r"


def test_state_value_skips_non_mapping_intermediate_values() -> None:
    assert _state_value({"github": None, "repository": "o/r"}, "github.repo", "repository") == "o/r"
