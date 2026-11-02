"""Tests for model_family."""

from agentic_devtools.cli.azure_devops.review_reviewer_models import model_family


class TestModelFamily:
    """Tests for model_family."""

    def test_none_returns_none(self):
        """None input returns None."""
        assert model_family(None) is None

    def test_empty_string_returns_none(self):
        """Empty string returns None."""
        assert model_family("") is None

    def test_known_claude_family(self):
        """A Claude model resolves to the 'claude' family."""
        assert model_family("Claude Opus 4.6") == "claude"

    def test_known_gpt_family(self):
        """A GPT model resolves to the 'gpt' family."""
        assert model_family("gpt-5.3-codex") == "gpt"

    def test_known_o_series_family(self):
        """An o-series model resolves to the 'o-series' family."""
        assert model_family("o4-mini") == "o-series"

    def test_unknown_model_is_its_own_family(self):
        """An unknown but non-empty model name is its own (lowercased) family."""
        assert model_family("Llama-3") == "llama-3"
