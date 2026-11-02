from agentic_devtools.adapters.pull_request_details import _github_change_type


def test_github_change_type_maps_known_statuses() -> None:
    assert _github_change_type("added") == "add"
    assert _github_change_type("copied") == "add"
    assert _github_change_type("removed") == "delete"
    assert _github_change_type("renamed") == "rename"


def test_github_change_type_defaults_to_edit() -> None:
    assert _github_change_type("modified") == "edit"
    assert _github_change_type("") == "edit"
