from agentic_devtools.cli.ci import guards as guards_module


def test_normalizes_supported_author_aliases() -> None:
    assert guards_module._comment_author_login({"author": "Dispatch-Bot"}) == "dispatch-bot"
    assert guards_module._comment_author_login({"author": {"login": "Dispatch-Bot"}}) == "dispatch-bot"
    assert guards_module._comment_author_login({"author_login": "Dispatch-Bot"}) == "dispatch-bot"
    assert guards_module._comment_author_login({"user": {"login": "Dispatch-Bot"}}) == "dispatch-bot"


def test_returns_none_when_author_aliases_are_absent() -> None:
    assert guards_module._comment_author_login({"id": 1}) is None


def test_rejects_missing_or_invalid_author_alias_shapes() -> None:
    invalid = guards_module._ALIAS_CONFLICT

    assert guards_module._comment_author_login({"author": {}}) is invalid
    assert guards_module._comment_author_login({"author_login": ""}) is invalid
    assert guards_module._comment_author_login({"user": "dispatch-bot"}) is invalid
    assert guards_module._comment_author_login({"user": {}}) is invalid


def test_rejects_conflicting_author_alias_values() -> None:
    invalid = guards_module._ALIAS_CONFLICT

    assert guards_module._comment_author_login({"author": "dispatch-bot", "author_login": "other-bot"}) is invalid
