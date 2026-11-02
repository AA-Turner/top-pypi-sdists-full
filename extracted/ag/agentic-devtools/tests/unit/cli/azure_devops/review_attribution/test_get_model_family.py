"""Tests for get_model_family function."""

from agentic_devtools.cli.azure_devops.review_attribution import get_model_family


class TestGetModelFamily:
    """Tests for get_model_family."""

    def test_claude_returns_claude(self):
        """A Claude model name returns the 'claude' family."""
        assert get_model_family("Claude Opus 4.6") == "claude"

    def test_gpt_returns_gpt(self):
        """A GPT model name returns the 'gpt' family."""
        assert get_model_family("gpt-5.3-codex") == "gpt"

    def test_gemini_returns_gemini(self):
        """A Gemini model name returns the 'gemini' family."""
        assert get_model_family("gemini-3.1-pro-preview") == "gemini"

    def test_o_series_returns_o_series(self):
        """An o-series model name returns the 'o-series' family."""
        assert get_model_family("o4-mini") == "o-series"

    def test_deepseek_returns_deepseek(self):
        """A DeepSeek model name returns the 'deepseek' family."""
        assert get_model_family("deepseek-v3") == "deepseek"

    def test_glm_returns_glm(self):
        """A GLM model name returns the 'glm' family."""
        assert get_model_family("glm-4.6") == "glm"

    def test_case_insensitive(self):
        """Family matching is case-insensitive."""
        assert get_model_family("DEEPSEEK-CODER") == "deepseek"

    def test_unknown_returns_none(self):
        """An unknown model name returns None."""
        assert get_model_family("Llama-3") is None

    def test_empty_string_returns_none(self):
        """An empty string returns None."""
        assert get_model_family("") is None

    def test_none_returns_none(self):
        """None returns None."""
        assert get_model_family(None) is None
