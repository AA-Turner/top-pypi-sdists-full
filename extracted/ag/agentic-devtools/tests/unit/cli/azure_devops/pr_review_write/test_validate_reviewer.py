"""Tests for validate_reviewer."""

from agentic_devtools.cli.azure_devops.pr_review_write import validate_reviewer


class TestValidateReviewer:
    def test_valid_with_ducks(self):
        reviewer = {
            "model": "claude-opus-4.6",
            "rubberDucks": [
                {"model": "gpt-5.3-codex", "verdict": "reject", "notes": "false positive"},
                {"model": "gemini-3.1-pro-preview", "verdict": "partial"},
            ],
        }
        assert validate_reviewer(reviewer) == []

    def test_valid_without_ducks(self):
        assert validate_reviewer({"model": "claude-opus-4.6"}) == []

    def test_non_dict(self):
        assert validate_reviewer("nope") == ["reviewer: must be an object"]

    def test_missing_model(self):
        errors = validate_reviewer({"model": "  "})
        assert any("reviewer.model" in e for e in errors)

    def test_ducks_not_list(self):
        errors = validate_reviewer({"model": "m", "rubberDucks": "nope"})
        assert any("rubberDucks: must be a list" in e for e in errors)

    def test_duck_non_dict(self):
        errors = validate_reviewer({"model": "m", "rubberDucks": ["nope"]})
        assert any("rubberDucks[0]: must be an object" in e for e in errors)

    def test_duck_missing_model(self):
        errors = validate_reviewer({"model": "m", "rubberDucks": [{"verdict": "accept"}]})
        assert any("rubberDucks[0].model" in e for e in errors)

    def test_duck_invalid_verdict(self):
        errors = validate_reviewer({"model": "m", "rubberDucks": [{"model": "d", "verdict": "maybe"}]})
        assert any("verdict" in e for e in errors)

    def test_duck_notes_non_str(self):
        errors = validate_reviewer({"model": "m", "rubberDucks": [{"model": "d", "verdict": "accept", "notes": 5}]})
        assert any("notes" in e for e in errors)
