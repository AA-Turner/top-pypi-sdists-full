from agentic_devtools.cli.setup.copilot_settings import _parse_top_level_members


def test_rejects_non_object():
    try:
        _parse_top_level_members("[]")
    except ValueError as exc:
        assert str(exc) == "settings.json is not a JSON object"
    else:  # pragma: no cover - defensive assertion for the test itself
        raise AssertionError("expected ValueError")


def test_rejects_non_string_key():
    try:
        _parse_top_level_members("{1: 2}")
    except ValueError as exc:
        assert str(exc) == "top-level key is not a string"
    else:  # pragma: no cover - defensive assertion for the test itself
        raise AssertionError("expected ValueError")


def test_rejects_missing_colon():
    try:
        _parse_top_level_members('{"a" 1}')
    except ValueError as exc:
        assert str(exc) == "malformed JSON object entry"
    else:  # pragma: no cover - defensive assertion for the test itself
        raise AssertionError("expected ValueError")


def test_rejects_bad_terminator():
    try:
        _parse_top_level_members('{"a": 1 x')
    except ValueError as exc:
        assert str(exc) == "malformed JSON object terminator"
    else:  # pragma: no cover - defensive assertion for the test itself
        raise AssertionError("expected ValueError")


def test_rejects_unterminated_object():
    try:
        _parse_top_level_members("{")
    except ValueError as exc:
        assert str(exc) == "unterminated JSON object"
    else:  # pragma: no cover - defensive assertion for the test itself
        raise AssertionError("expected ValueError")


def test_rejects_trailing_comma():
    try:
        _parse_top_level_members('{"a": 1,}')
    except ValueError as exc:
        assert str(exc) == "malformed JSON object terminator"
    else:  # pragma: no cover - defensive assertion for the test itself
        raise AssertionError("expected ValueError")


def test_rejects_missing_closing_brace():
    try:
        _parse_top_level_members('{"a": 1')
    except ValueError as exc:
        assert str(exc) == "malformed JSON object terminator"
    else:  # pragma: no cover - defensive assertion for the test itself
        raise AssertionError("expected ValueError")
