"""Tests for load_review_model_config()."""

from agentic_devtools.config import load_review_model_config


class TestLoadReviewModelConfig:
    """Tests for loading review model routing configuration."""

    def test_returns_empty_dict_when_no_config(self, tmp_path) -> None:
        """Returns empty dict when no agdt-config.json exists."""
        result = load_review_model_config(str(tmp_path))
        assert result == {}

    def test_returns_empty_dict_when_no_review_section(self, tmp_path) -> None:
        """Returns empty dict when config has no review section."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"other": "stuff"}')

        result = load_review_model_config(str(tmp_path))
        assert result == {}

    def test_returns_empty_dict_when_no_model_routing_key(self, tmp_path) -> None:
        """Returns empty dict when review section has none of the routing keys."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"review": {"focus-areas-file": "test.md"}}')

        result = load_review_model_config(str(tmp_path))
        assert result == {}

    def test_returns_model_routing_dict(self, tmp_path) -> None:
        """Returns the model-routing dict when configured with hyphen key."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"model-routing": {"default-model": "gpt-4o", "rules": []}}}'
        )

        result = load_review_model_config(str(tmp_path))
        assert result == {"default-model": "gpt-4o", "rules": []}

    def test_returns_model_routing_via_models_alias(self, tmp_path) -> None:
        """Returns the routing dict when configured via the 'models' alias."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"models": {"default-model": "claude-opus-4.5", "rules": []}}}'
        )

        result = load_review_model_config(str(tmp_path))
        assert result == {"default-model": "claude-opus-4.5", "rules": []}

    def test_returns_model_routing_via_underscore_alias(self, tmp_path) -> None:
        """Returns the routing dict when configured via the 'model_routing' alias."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"model_routing": {"default-model": "gpt-4o-mini", "rules": []}}}'
        )

        result = load_review_model_config(str(tmp_path))
        assert result == {"default-model": "gpt-4o-mini", "rules": []}

    def test_hyphen_key_takes_precedence_over_models_alias(self, tmp_path) -> None:
        """model-routing key takes precedence over models alias when both are present."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"model-routing": {"default-model": "gpt-4o"}, "models": {"default-model": "fallback"}}}'
        )

        result = load_review_model_config(str(tmp_path))
        assert result == {"default-model": "gpt-4o"}

    def test_empty_hyphen_key_takes_precedence_and_returns_empty(self, tmp_path) -> None:
        """Empty model-routing dict wins over models alias (key-presence beats falsiness)."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"model-routing": {}, "models": {"default-model": "fallback"}}}'
        )

        result = load_review_model_config(str(tmp_path))
        assert result == {}

    def test_empty_models_alias_takes_precedence_over_underscore_alias(self, tmp_path) -> None:
        """Empty models dict wins over model_routing alias (key-presence beats falsiness)."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"models": {}, "model_routing": {"default-model": "fallback"}}}'
        )

        result = load_review_model_config(str(tmp_path))
        assert result == {}

    def test_models_alias_takes_precedence_over_underscore_alias(self, tmp_path) -> None:
        """models alias takes precedence over model_routing alias when both present."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text(
            '{"review": {"models": {"default-model": "gpt-4o"}, "model_routing": {"default-model": "fallback"}}}'
        )

        result = load_review_model_config(str(tmp_path))
        assert result == {"default-model": "gpt-4o"}

    def test_returns_empty_when_model_routing_not_dict(self, tmp_path) -> None:
        """Returns empty dict when model-routing is not a dict."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"review": {"model-routing": "invalid"}}')

        result = load_review_model_config(str(tmp_path))
        assert result == {}

    def test_returns_empty_when_review_not_dict(self, tmp_path) -> None:
        """Returns empty dict when review section is not a dict."""
        config_dir = tmp_path / ".github"
        config_dir.mkdir()
        (config_dir / "agdt-config.json").write_text('{"review": "invalid"}')

        result = load_review_model_config(str(tmp_path))
        assert result == {}
