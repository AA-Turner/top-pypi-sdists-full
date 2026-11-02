from agentic_devtools.adapters.pull_request_details import _deep_merge_state


def test_deep_merge_state_merges_nested_mappings_without_dropping_siblings() -> None:
    base = {"github": {"repo": "o/r", "pull_request_number": 9}}
    override = {"github": {"provider": "github"}}
    assert _deep_merge_state(base, override) == {
        "github": {"repo": "o/r", "pull_request_number": 9, "provider": "github"}
    }


def test_deep_merge_state_overrides_non_mapping_values() -> None:
    base = {"pull_request_id": 1, "repository": "o/r"}
    override = {"pull_request_id": 2}
    assert _deep_merge_state(base, override) == {"pull_request_id": 2, "repository": "o/r"}


def test_deep_merge_state_replaces_when_override_value_is_not_a_mapping() -> None:
    base = {"platform": {"code_hosting": "github"}}
    override = {"platform": "azure_devops"}
    assert _deep_merge_state(base, override) == {"platform": "azure_devops"}


def test_deep_merge_state_does_not_mutate_inputs() -> None:
    base = {"github": {"repo": "o/r"}}
    override = {"github": {"provider": "github"}}
    merged = _deep_merge_state(base, override)
    merged["github"]["repo"] = "changed"
    assert base["github"]["repo"] == "o/r"
