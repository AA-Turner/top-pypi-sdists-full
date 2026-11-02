"""Tests for get_model_icon function."""

from agentic_devtools.cli.azure_devops.review_attribution import get_model_icon


class TestGetModelIcon:
    """Tests for get_model_icon."""

    def test_claude_returns_brain_emoji(self):
        """Test that a Claude model name returns the brain emoji."""
        assert get_model_icon("Claude Opus 4.6") == "🧠"

    def test_claude_lowercase_prefix(self):
        """Test Claude prefix matching is case-insensitive."""
        assert get_model_icon("claude-3-opus") == "🧠"

    def test_gpt_returns_crystal_ball_emoji(self):
        """Test that a GPT model name returns the crystal ball emoji."""
        assert get_model_icon("GPT-4o") == "🔮"

    def test_gpt_lowercase(self):
        """Test GPT prefix matching is case-insensitive."""
        assert get_model_icon("gpt-4-turbo") == "🔮"

    def test_gemini_returns_gem_emoji(self):
        """Test that a Gemini model name returns the gem emoji."""
        assert get_model_icon("Gemini Ultra") == "💎"

    def test_gemini_lowercase(self):
        """Test Gemini prefix matching is case-insensitive."""
        assert get_model_icon("gemini-pro") == "💎"

    def test_o_series_returns_cyclone_emoji(self):
        """Test that an o-series model name returns the cyclone emoji."""
        assert get_model_icon("o4-mini") == "🌀"

    def test_deepseek_returns_whale_emoji(self):
        """Test that a DeepSeek model name returns the whale emoji."""
        assert get_model_icon("deepseek-v3") == "🐳"

    def test_glm_returns_blue_diamond_emoji(self):
        """Test that a GLM model name returns the blue diamond emoji."""
        assert get_model_icon("glm-4.6") == "🔷"

    def test_unknown_model_returns_generic_robot(self):
        """Test that an unknown model name returns the generic robot emoji."""
        assert get_model_icon("Llama-3") == "🤖"

    def test_empty_string_returns_generic_robot(self):
        """Test that an empty string returns the generic robot emoji."""
        assert get_model_icon("") == "🤖"

    def test_none_returns_generic_robot(self):
        """Test that None returns the generic robot emoji."""
        assert get_model_icon(None) == "🤖"

    def test_arbitrary_model_returns_generic_robot(self):
        """Test that an arbitrary/unknown model name returns the fallback icon."""
        assert get_model_icon("MistralAI-7B") == "🤖"
