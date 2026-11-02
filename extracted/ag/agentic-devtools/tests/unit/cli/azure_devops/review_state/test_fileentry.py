"""Tests for FileEntry dataclass."""

import pytest

from agentic_devtools.cli.azure_devops.review_state import FileEntry, ReviewStatus, SuggestionEntry


def _make_suggestion() -> SuggestionEntry:
    return SuggestionEntry(
        threadId=100,
        commentId=200,
        line=1,
        endLine=5,
        severity="high",
        outOfScope=False,
        linkText="lines 1 - 5",
        content="Missing null check",
    )


class TestFileEntry:
    """Tests for FileEntry dataclass."""

    def test_creation_with_defaults(self):
        """Test creation with minimal required fields and defaults."""
        f = FileEntry(threadId=161048, commentId=1771800050, folder="mgmt-backend", fileName="SomeFile.cs")
        assert f.threadId == 161048
        assert f.commentId == 1771800050
        assert f.folder == "mgmt-backend"
        assert f.fileName == "SomeFile.cs"
        assert f.status == ReviewStatus.UNREVIEWED
        assert f.summary is None
        assert f.changeTrackingId is None
        assert f.suggestions == []
        assert f.previousSuggestions is None
        assert f.suggestionVerificationStatus is None

    def test_creation_with_all_fields(self):
        """Test creation with all fields specified."""
        suggestion = _make_suggestion()
        f = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            status="approved",
            summary="Looks good",
            changeTrackingId=42,
            suggestions=[suggestion],
        )
        assert f.status == "approved"
        assert f.summary == "Looks good"
        assert f.changeTrackingId == 42
        assert len(f.suggestions) == 1

    def test_to_dict(self):
        """Test serialization to dictionary."""
        f = FileEntry(
            threadId=161048,
            commentId=1771800050,
            folder="mgmt-backend",
            fileName="SomeFile.cs",
            status="unreviewed",
            summary=None,
            changeTrackingId=42,
            suggestions=[],
        )
        d = f.to_dict()
        assert d == {
            "threadId": 161048,
            "commentId": 1771800050,
            "folder": "mgmt-backend",
            "fileName": "SomeFile.cs",
            "status": "unreviewed",
            "summary": None,
            "changeTrackingId": 42,
            "suggestions": [],
            "previousSuggestions": None,
            "suggestionVerificationStatus": None,
        }

    def test_to_dict_with_suggestions(self):
        """Test serialization with suggestions."""
        suggestion = _make_suggestion()
        f = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            suggestions=[suggestion],
        )
        d = f.to_dict()
        assert len(d["suggestions"]) == 1
        assert d["suggestions"][0]["threadId"] == 100

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        data = {
            "threadId": 161048,
            "commentId": 1771800050,
            "folder": "mgmt-backend",
            "fileName": "SomeFile.cs",
            "status": "approved",
            "summary": "Reviewed",
            "changeTrackingId": 42,
            "suggestions": [],
        }
        f = FileEntry.from_dict(data)
        assert f.threadId == 161048
        assert f.folder == "mgmt-backend"
        assert f.status == "approved"
        assert f.summary == "Reviewed"
        assert f.changeTrackingId == 42
        assert f.suggestions == []

    def test_from_dict_with_suggestions(self):
        """Test deserialization with embedded suggestions."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "folder": "src",
            "fileName": "app.py",
            "suggestions": [
                {
                    "threadId": 100,
                    "commentId": 200,
                    "line": 1,
                    "endLine": 5,
                    "severity": "high",
                    "outOfScope": False,
                    "linkText": "lines 1 - 5",
                    "content": "Missing null check",
                }
            ],
        }
        f = FileEntry.from_dict(data)
        assert len(f.suggestions) == 1
        assert f.suggestions[0].threadId == 100

    def test_from_dict_defaults(self):
        """Test from_dict with missing optional fields uses defaults."""
        data = {"threadId": 1, "commentId": 2, "folder": "src", "fileName": "app.py"}
        f = FileEntry.from_dict(data)
        assert f.status == ReviewStatus.UNREVIEWED
        assert f.summary is None
        assert f.changeTrackingId is None
        assert f.suggestions == []

    def test_roundtrip(self):
        """Test to_dict/from_dict round-trips correctly."""
        suggestion = _make_suggestion()
        original = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            status="needs-work",
            summary="Has issues",
            changeTrackingId=7,
            suggestions=[suggestion],
        )
        restored = FileEntry.from_dict(original.to_dict())
        assert restored.threadId == 1
        assert restored.status == "needs-work"
        assert restored.summary == "Has issues"
        assert restored.changeTrackingId == 7
        assert len(restored.suggestions) == 1

    def test_suggestions_default_is_independent(self):
        """Test that default suggestions lists are independent per instance."""
        f1 = FileEntry(threadId=1, commentId=1, folder="a", fileName="b.py")
        f2 = FileEntry(threadId=2, commentId=2, folder="a", fileName="c.py")
        f1.suggestions.append(_make_suggestion())
        assert f2.suggestions == []

    def test_previous_suggestions_default_is_none(self):
        """Test that previousSuggestions defaults to None (never rotated)."""
        f = FileEntry(threadId=1, commentId=2, folder="src", fileName="app.py")
        assert f.previousSuggestions is None

    def test_previous_suggestions_none_is_independent(self):
        """Test that setting previousSuggestions on one instance doesn't affect another."""
        f1 = FileEntry(threadId=1, commentId=1, folder="a", fileName="b.py")
        f2 = FileEntry(threadId=2, commentId=2, folder="a", fileName="c.py")
        f1.previousSuggestions = [_make_suggestion()]
        assert f2.previousSuggestions is None

    def test_to_dict_includes_previous_suggestions(self):
        """Test that to_dict serialises previousSuggestions."""
        suggestion = _make_suggestion()
        f = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            previousSuggestions=[suggestion],
        )
        d = f.to_dict()
        assert "previousSuggestions" in d
        assert len(d["previousSuggestions"]) == 1
        assert d["previousSuggestions"][0]["threadId"] == 100

    def test_from_dict_deserialises_previous_suggestions(self):
        """Test that from_dict reads previousSuggestions."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "folder": "src",
            "fileName": "app.py",
            "suggestions": [],
            "previousSuggestions": [
                {
                    "threadId": 50,
                    "commentId": 60,
                    "line": 3,
                    "endLine": 3,
                    "severity": "low",
                    "outOfScope": False,
                    "linkText": "line 3",
                    "content": "Old suggestion",
                }
            ],
        }
        f = FileEntry.from_dict(data)
        assert len(f.previousSuggestions) == 1
        assert f.previousSuggestions[0].threadId == 50

    def test_from_dict_missing_previous_suggestions_defaults_to_none(self):
        """Test that from_dict defaults previousSuggestions to None when key absent (backward compat)."""
        data = {"threadId": 1, "commentId": 2, "folder": "src", "fileName": "app.py"}
        f = FileEntry.from_dict(data)
        assert f.previousSuggestions is None

    @pytest.mark.parametrize(
        ("field", "value"),
        [
            ("modelId", 47),
            ("providerType", 47),
            ("latencyMs", "47"),
            ("finishReason", 47),
            ("tokensUsed", "1234"),
            ("processingPath", 47),
            ("crossIdentity", "true"),
        ],
    )
    def test_from_dict_rejects_invalid_attribution_fields(self, field, value):
        """Test that from_dict rejects attribution values with invalid types."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "folder": "src",
            "fileName": "app.py",
            field: value,
        }

        with pytest.raises(ValueError, match=field):
            FileEntry.from_dict(data)

    def test_roundtrip_with_previous_suggestions(self):
        """Test to_dict/from_dict round-trips previousSuggestions correctly."""
        suggestion = _make_suggestion()
        original = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            status="needs-work",
            suggestions=[],
            previousSuggestions=[suggestion],
        )
        restored = FileEntry.from_dict(original.to_dict())
        assert len(restored.previousSuggestions) == 1
        assert restored.previousSuggestions[0].threadId == 100
        assert restored.suggestions == []

    def test_suggestion_verification_status_default_is_none(self):
        """Test that suggestionVerificationStatus defaults to None."""
        f = FileEntry(threadId=1, commentId=2, folder="src", fileName="app.py")
        assert f.suggestionVerificationStatus is None

    def test_suggestion_verification_status_creation(self):
        """Test creation with explicit suggestionVerificationStatus."""
        f = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            suggestionVerificationStatus="unaddressed",
        )
        assert f.suggestionVerificationStatus == "unaddressed"

    def test_suggestion_verification_status_to_dict(self):
        """Test that to_dict serialises suggestionVerificationStatus."""
        f = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            suggestionVerificationStatus="pending_verification",
        )
        d = f.to_dict()
        assert d["suggestionVerificationStatus"] == "pending_verification"

    def test_suggestion_verification_status_from_dict(self):
        """Test that from_dict reads suggestionVerificationStatus."""
        data = {
            "threadId": 1,
            "commentId": 2,
            "folder": "src",
            "fileName": "app.py",
            "suggestionVerificationStatus": "unaddressed",
        }
        f = FileEntry.from_dict(data)
        assert f.suggestionVerificationStatus == "unaddressed"

    def test_suggestion_verification_status_missing_defaults_to_none(self):
        """Test that missing suggestionVerificationStatus defaults to None."""
        data = {"threadId": 1, "commentId": 2, "folder": "src", "fileName": "app.py"}
        f = FileEntry.from_dict(data)
        assert f.suggestionVerificationStatus is None

    def test_roundtrip_with_suggestion_verification_status(self):
        """Test to_dict/from_dict round-trips suggestionVerificationStatus."""
        original = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            suggestionVerificationStatus="pending_verification",
        )
        restored = FileEntry.from_dict(original.to_dict())
        assert restored.suggestionVerificationStatus == "pending_verification"

    def test_roundtrip_with_runtime_attribution_fields(self):
        """Runtime attribution fields are preserved through to_dict/from_dict."""
        original = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
            modelId="gemini-3.7-flash",
            providerType="copilot",
            latencyMs=47,
            finishReason="stop",
            tokensUsed=1234,
        )
        restored = FileEntry.from_dict(original.to_dict())
        assert restored.modelId == "gemini-3.7-flash"
        assert restored.providerType == "copilot"
        assert restored.latencyMs == 47
        assert restored.finishReason == "stop"
        assert restored.tokensUsed == 1234

    def test_to_dict_includes_processing_path_when_set(self):
        """Test that to_dict serialises processingPath when not None."""
        f = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
        )
        f.processingPath = "inherited"
        d = f.to_dict()
        assert d["processingPath"] == "inherited"

    def test_to_dict_excludes_processing_path_when_none(self):
        """Test that to_dict omits processingPath when None."""
        f = FileEntry(
            threadId=1,
            commentId=2,
            folder="src",
            fileName="app.py",
        )
        assert f.processingPath is None
        d = f.to_dict()
        assert "processingPath" not in d


class TestFileEntryBackwardCompat:
    """Old review-state.json with removed System B fields still loads."""

    def test_from_dict_ignores_legacy_model_verdict_fields(self):
        """Legacy modelVerdicts/consolidationStatus keys are silently ignored."""
        legacy = {
            "threadId": 1,
            "commentId": 2,
            "folder": "src",
            "fileName": "app.py",
            "status": "approved",
            "summary": "ok",
            "modelVerdicts": [{"modelId": "gpt-4o", "status": "approved", "verdictType": "agree"}],
            "consolidationStatus": "complete",
        }
        fe = FileEntry.from_dict(legacy)
        assert fe.threadId == 1
        assert fe.status == "approved"
        assert fe.summary == "ok"
        d = fe.to_dict()
        assert "modelVerdicts" not in d
        assert "consolidationStatus" not in d
