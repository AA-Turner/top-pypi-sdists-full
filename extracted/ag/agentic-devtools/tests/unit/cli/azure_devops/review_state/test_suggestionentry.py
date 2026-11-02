"""Tests for SuggestionEntry dataclass."""

from agentic_devtools.cli.azure_devops.review_state import SuggestionEntry


def _make_suggestion(**kwargs) -> SuggestionEntry:
    defaults = {
        "threadId": 100,
        "commentId": 200,
        "line": 10,
        "endLine": 20,
        "severity": "high",
        "outOfScope": False,
        "linkText": "lines 10 - 20",
        "content": "Missing null check",
    }
    defaults.update(kwargs)
    return SuggestionEntry(**defaults)  # type: ignore[arg-type]


class TestSuggestionEntry:
    """Tests for SuggestionEntry dataclass."""

    def test_creation(self):
        """Test basic creation of a SuggestionEntry."""
        s = _make_suggestion()
        assert s.threadId == 100
        assert s.commentId == 200
        assert s.line == 10
        assert s.endLine == 20
        assert s.severity == "high"
        assert s.outOfScope is False
        assert s.linkText == "lines 10 - 20"
        assert s.content == "Missing null check"
        assert s.replacement_code is None

    def test_creation_with_replacement_code(self):
        """Test creation with an optional replacement_code field."""
        s = _make_suggestion(replacement_code="x = 1\n")
        assert s.replacement_code == "x = 1\n"

    def test_to_dict(self):
        """Test serialization to dictionary without replacement_code."""
        s = _make_suggestion()
        d = s.to_dict()
        assert d == {
            "threadId": 100,
            "commentId": 200,
            "line": 10,
            "endLine": 20,
            "severity": "high",
            "outOfScope": False,
            "linkText": "lines 10 - 20",
            "content": "Missing null check",
        }
        assert "replacementCode" not in d

    def test_to_dict_with_replacement_code(self):
        """Test serialization includes replacement_code when set."""
        s = _make_suggestion(replacement_code="return None")
        d = s.to_dict()
        assert d["replacementCode"] == "return None"

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "threadId": 100,
            "commentId": 200,
            "line": 10,
            "endLine": 20,
            "severity": "high",
            "outOfScope": False,
            "linkText": "lines 10 - 20",
            "content": "Missing null check",
        }
        s = SuggestionEntry.from_dict(data)
        assert s.threadId == 100
        assert s.commentId == 200
        assert s.line == 10
        assert s.endLine == 20
        assert s.severity == "high"
        assert s.outOfScope is False
        assert s.linkText == "lines 10 - 20"
        assert s.content == "Missing null check"
        assert s.replacement_code is None

    def test_from_dict_with_replacement_code(self):
        """Test deserialization reads replacement_code when present."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "line": 5,
            "endLine": 5,
            "severity": "medium",
            "outOfScope": False,
            "linkText": "line 5",
            "content": "Use const",
            "replacementCode": "const x = 1;",
        }
        s = SuggestionEntry.from_dict(data)
        assert s.replacement_code == "const x = 1;"

    def test_from_dict_with_legacy_replacement_code_key(self):
        """Legacy snake_case replacement_code key remains supported."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "line": 5,
            "endLine": 5,
            "severity": "medium",
            "outOfScope": False,
            "linkText": "line 5",
            "content": "Use const",
            "replacement_code": "const x = 2;",
        }
        s = SuggestionEntry.from_dict(data)
        assert s.replacement_code == "const x = 2;"

    def test_roundtrip(self):
        """Test that to_dict/from_dict round-trips correctly."""
        original = _make_suggestion(outOfScope=True, severity="low")
        restored = SuggestionEntry.from_dict(original.to_dict())
        assert restored.threadId == original.threadId
        assert restored.outOfScope is True
        assert restored.severity == "low"
        assert restored.replacement_code is None

    def test_roundtrip_with_replacement_code(self):
        """Test that replacement_code survives a to_dict/from_dict round-trip."""
        original = _make_suggestion(replacement_code="x = 42")
        restored = SuggestionEntry.from_dict(original.to_dict())
        assert restored.replacement_code == "x = 42"

    def test_out_of_scope_true(self):
        """Test out_of_scope=True serializes correctly."""
        s = _make_suggestion(outOfScope=True)
        assert s.to_dict()["outOfScope"] is True

    def test_from_dict_non_string_replacement_code_treated_as_none(self):
        """Non-string replacement_code values from persisted JSON are coerced to None."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "line": 5,
            "endLine": 5,
            "severity": "medium",
            "outOfScope": False,
            "linkText": "line 5",
            "content": "Use const",
            "replacementCode": ["line 1", "line 2"],
        }
        s = SuggestionEntry.from_dict(data)
        assert s.replacement_code is None

    def test_from_dict_dict_replacement_code_treated_as_none(self):
        """A dict-valued replacement_code from persisted JSON is coerced to None."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "line": 5,
            "endLine": 5,
            "severity": "medium",
            "outOfScope": False,
            "linkText": "line 5",
            "content": "Use const",
            "replacementCode": {"code": "x = 1"},
        }
        s = SuggestionEntry.from_dict(data)
        assert s.replacement_code is None
