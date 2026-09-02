"""Tests for _prompt_copilot_model."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.setup.commands import _prompt_copilot_model


class TestPromptCopilotModel:
    """Tests for _prompt_copilot_model."""

    def test_saves_selected_model_to_project_config(self, capsys):
        """Should save the selected model to project config."""
        models = ["gpt-5.3-codex", "gpt-4o"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch(
                    "agentic_devtools.cli.config.project_config.save_project_config",
                    return_value=MagicMock(),
                ) as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model()

        mock_save.assert_called_once()
        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "gpt-5.3-codex"

    def test_uses_first_model_as_default_when_no_existing_config(self, capsys):
        """Uses first model as default when no model is configured."""
        models = ["gpt-5.3-codex", "gpt-4o"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    # Enter selects default
                    with patch("agentic_devtools.cli.setup.commands.input", return_value=""):
                        _prompt_copilot_model()

        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "gpt-5.3-codex"

    def test_uses_existing_configured_model_as_default(self, capsys):
        """Uses already-configured model as default when it's in the list."""
        models = ["gpt-5.3-codex", "gpt-4o", "claude-opus-4.6"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch(
                "agentic_devtools.cli.config.project_config.load_project_config",
                return_value={"default_copilot_model": "claude-opus-4.6"},
            ):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    # Enter selects default (should be claude-opus-4.6)
                    with patch("agentic_devtools.cli.setup.commands.input", return_value=""):
                        _prompt_copilot_model(force_prompt=True)

        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "claude-opus-4.6"

    def test_accepts_free_form_model_name(self, capsys):
        """Accepts a free-form model name typed directly."""
        models = ["gpt-5.3-codex", "gpt-4o"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="my-custom-model"):
                        _prompt_copilot_model()

        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "my-custom-model"

    def test_handles_eof_error_gracefully(self, capsys):
        """Handles EOFError (non-interactive) without crashing."""
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=["gpt-4o"]):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.setup.commands.input", side_effect=EOFError):
                    # Should not raise
                    _prompt_copilot_model()

    def test_handles_keyboard_interrupt_gracefully(self, capsys):
        """Handles KeyboardInterrupt without crashing."""
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=["gpt-4o"]):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.setup.commands.input", side_effect=KeyboardInterrupt):
                    # Should not raise
                    _prompt_copilot_model()

    def test_prints_confirmation_message(self, capsys):
        """Prints a confirmation message with the selected model."""
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=["gpt-5.3-codex"]):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config"):
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model()

        out = capsys.readouterr().out
        assert "gpt-5.3-codex" in out
        assert "✓" in out

    def test_invalid_numeric_selection_uses_default(self, capsys):
        """Out-of-range numeric selection keeps the default."""
        models = ["gpt-5.3-codex", "gpt-4o"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="99"):
                        _prompt_copilot_model()

        saved = mock_save.call_args[0][0]
        # Out of range — should fall back to default (first model)
        assert saved["default_copilot_model"] == "gpt-5.3-codex"

    def test_allows_a_free_form_name_when_no_inventory_is_available(self, capsys):
        """An empty inventory still lets the user type a model name."""
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=[]):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="gpt-5-mini"):
                        _prompt_copilot_model()

        assert mock_save.call_args[0][0]["default_copilot_model"] == "gpt-5-mini"
        assert "No Copilot model inventory available" in capsys.readouterr().out

    def test_leaves_the_default_unset_when_nothing_is_selected(self, capsys):
        """No inventory and no answer leaves default_copilot_model unset."""
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=[]):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value=""):
                        _prompt_copilot_model()

        mock_save.assert_not_called()
        assert "No model selected" in capsys.readouterr().out

    def test_internal_fallback_never_uses_stale_or_live_query(self, capsys):
        """The internal fallback never triggers a live ACP handshake or a stale cache read."""
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=["gpt-4o"]) as mock_query:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config"):
                    with patch("agentic_devtools.cli.setup.commands.input", return_value=""):
                        _prompt_copilot_model(refresh_models=True)

        mock_query.assert_called_once_with(refresh=False, allow_stale=False)

    def test_strips_whitespace_from_existing_configured_model(self, capsys):
        """Strips leading/trailing whitespace from existing config before matching."""
        models = ["gpt-5.3-codex", "gpt-4o", "claude-opus-4.6"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch(
                "agentic_devtools.cli.config.project_config.load_project_config",
                return_value={"default_copilot_model": "  claude-opus-4.6  "},
            ):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    # Enter selects default (should match claude-opus-4.6 after strip)
                    with patch("agentic_devtools.cli.setup.commands.input", return_value=""):
                        _prompt_copilot_model(force_prompt=True)

        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "claude-opus-4.6"

    def test_skips_prompt_when_model_already_set(self, capsys):
        """Should skip prompt when default_copilot_model key exists in config."""
        existing = {"default_copilot_model": "gpt-5.3-codex"}
        mock_input = patch("agentic_devtools.cli.setup.commands.input")
        with mock_input as m_input:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                _prompt_copilot_model()

        m_input.assert_not_called()
        out = capsys.readouterr().out
        assert "Default Copilot model already set: gpt-5.3-codex" in out

    def test_skips_prompt_when_model_is_empty_string(self, capsys):
        """Should skip prompt even when default_copilot_model is empty string."""
        existing = {"default_copilot_model": ""}
        mock_input = patch("agentic_devtools.cli.setup.commands.input")
        with mock_input as m_input:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                _prompt_copilot_model()

        m_input.assert_not_called()
        out = capsys.readouterr().out
        assert "Default Copilot model already set:" in out

    def test_force_prompt_re_prompts_when_model_set(self, capsys):
        """Should re-prompt when force_prompt=True even if model exists."""
        existing = {"default_copilot_model": "gpt-4o"}
        models = ["gpt-5.3-codex", "gpt-4o"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model(force_prompt=True)

        mock_save.assert_called_once()
        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "gpt-5.3-codex"

    def test_skips_prompt_when_model_is_none(self, capsys):
        """Should skip prompt when default_copilot_model is None (key present)."""
        existing = {"default_copilot_model": None}
        mock_input = patch("agentic_devtools.cli.setup.commands.input")
        with mock_input as m_input:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                _prompt_copilot_model()

        m_input.assert_not_called()
        out = capsys.readouterr().out
        assert "Default Copilot model already set:" in out

    def test_force_prompt_handles_none_model_gracefully(self, capsys):
        """Should handle None model value gracefully when force_prompt=True."""
        existing = {"default_copilot_model": None}
        models = ["gpt-5.3-codex", "gpt-4o"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model(force_prompt=True)

        mock_save.assert_called_once()
        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "gpt-5.3-codex"

    def test_force_prompt_handles_non_string_model_gracefully(self, capsys):
        """Should handle non-string model value gracefully when force_prompt=True."""
        existing = {"default_copilot_model": 42}
        models = ["gpt-5.3-codex", "gpt-4o"]
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=models):
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model(force_prompt=True)

        mock_save.assert_called_once()
        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "gpt-5.3-codex"

    def test_uses_project_inventory_when_available_models_is_present(self, capsys):
        """Uses availableModels from project config, skipping _query_copilot_models."""
        existing = {"availableModels": ["gpt-5-mini", "claude-opus-4.6"]}
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models") as mock_query:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model()

        mock_query.assert_not_called()
        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "gpt-5-mini"

    def test_filters_invalid_project_inventory_entries_without_requerying(self, capsys):
        """Uses normalized cached models when availableModels contains mixed entries."""
        existing = {"availableModels": ["  gpt-5-mini  ", 42, "   ", "claude-opus-4.6"]}
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models") as mock_query:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                with patch(
                    "agentic_devtools.cli.config.project_config.get_available_models",
                    return_value=["gpt-5-mini", "claude-opus-4.6"],
                ):
                    with patch("agentic_devtools.cli.config.project_config.save_project_config") as mock_save:
                        with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                            _prompt_copilot_model()

        mock_query.assert_not_called()
        saved = mock_save.call_args[0][0]
        assert saved["default_copilot_model"] == "gpt-5-mini"

    def test_falls_back_to_query_when_available_models_is_absent(self, capsys):
        """Falls back to _query_copilot_models when availableModels is not in config."""
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=["gpt-4o"]) as mock_query:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value={}):
                with patch("agentic_devtools.cli.config.project_config.save_project_config"):
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model()

        mock_query.assert_called_once()

    def test_falls_back_to_query_when_available_models_is_not_a_list(self, capsys):
        """Falls back to _query_copilot_models when availableModels has invalid type."""
        existing = {"availableModels": "not-a-list"}
        with patch("agentic_devtools.cli.setup.commands._query_copilot_models", return_value=["gpt-4o"]) as mock_query:
            with patch("agentic_devtools.cli.config.project_config.load_project_config", return_value=existing):
                with patch("agentic_devtools.cli.config.project_config.save_project_config"):
                    with patch("agentic_devtools.cli.setup.commands.input", return_value="1"):
                        _prompt_copilot_model()

        mock_query.assert_called_once()
