"""Tests for load_config function."""

import builtins

import pytest

from agentic_devtools.orchestration.llm import config as config_module
from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot, load_config
from agentic_devtools.orchestration.llm.types import ProviderType


class TestLoadConfig:
    """Tests for load_config."""

    def test_load_from_dict(self):
        config_dict = {
            "providers": {
                "azure-main": {
                    "type": "azure_openai",
                    "model": "gpt-4o",
                    "endpoint": "https://my.openai.azure.com",
                    "api_key_env": "AZURE_KEY",
                }
            },
            "defaults": {"provider": "azure-main"},
        }
        snapshot = load_config(config_dict=config_dict)
        assert isinstance(snapshot, LLMConfigSnapshot)
        assert "azure-main" in snapshot.providers
        assert snapshot.providers["azure-main"].provider_type == ProviderType.AZURE_OPENAI
        assert snapshot.providers["azure-main"].model == "gpt-4o"

    def test_load_empty_config(self):
        snapshot = load_config(config_dict={})
        assert snapshot.providers == {}
        assert snapshot.workflows == {}

    def test_missing_file_returns_empty(self, tmp_path):
        snapshot = load_config(config_path=tmp_path / "nonexistent.yml")
        assert snapshot.providers == {}

    def test_load_from_yaml_file(self, tmp_path):
        config_file = tmp_path / "config.yml"
        config_file.write_text(
            """
providers:
  openai-direct:
    type: openai_direct
    model: gpt-4o-mini
    api_key_env: OPENAI_API_KEY
defaults:
  provider: openai-direct
"""
        )
        snapshot = load_config(config_path=config_file)
        assert "openai-direct" in snapshot.providers
        assert snapshot.providers["openai-direct"].model == "gpt-4o-mini"

    def test_load_from_yaml_file_uses_utf8_encoding(self, tmp_path, monkeypatch):
        config_file = tmp_path / "config.yml"
        config_file.write_text(
            """
providers:
  openai-direct:
    type: openai_direct
    model: gpt-4o-mini
    api_key_env: OPENAI_API_KEY
""",
            encoding="utf-8",
        )
        encodings: list[str | None] = []

        def recording_open(*args, **kwargs):
            encodings.append(kwargs.get("encoding"))
            return builtins.open(*args, **kwargs)

        monkeypatch.setattr(config_module, "open", recording_open, raising=False)

        snapshot = load_config(config_path=config_file)

        assert "openai-direct" in snapshot.providers
        assert encodings == ["utf-8"]

    def test_duplicate_node_mapping_raises(self):
        """load_config propagates duplicate node mapping validation errors."""
        from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError

        class DuplicateItemsDict(dict):
            """Dict subclass that yields duplicate items."""

            def items(self):
                yield "analysis", {"provider": "p1"}
                yield "analysis", {"provider": "p2"}

        config_dict = {
            "providers": {
                "p1": {"type": "azure_openai", "model": "gpt-4o"},
                "p2": {"type": "openai_direct", "model": "gpt-4o-mini"},
            },
            "workflows": {
                "pr_review": {
                    "nodes": DuplicateItemsDict(),
                }
            },
        }

        with pytest.raises(DuplicateNodeMappingError):
            load_config(config_dict=config_dict)

    def test_config_snapshot_is_frozen(self):
        snapshot = load_config(config_dict={"providers": {}})
        with pytest.raises(AttributeError):
            snapshot.providers = {}  # type: ignore[misc]

    def test_config_snapshot_nested_mappings_are_immutable(self):
        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
                "workflows": {"pr_review": {"nodes": {"analysis": {"provider": "main"}}}},
            }
        )
        with pytest.raises(TypeError):
            snapshot.providers["other"] = snapshot.providers["main"]  # type: ignore[index]
        with pytest.raises(TypeError):
            snapshot.workflows["pr_review"]["nodes"]["analysis"]["provider"] = "other"  # type: ignore[index]

    def test_validation_warnings_emitted(self):
        """Config with missing required fields triggers warnings."""
        config_dict = {
            "providers": {
                "bad": {"model": "gpt-4o"},  # missing 'type'
            }
        }
        with pytest.warns(UserWarning, match="LLM config validation"):
            load_config(config_dict=config_dict)

    def test_non_dict_provider_skipped(self):
        """Non-dict provider entries are skipped with a validation warning."""
        config_dict = {
            "providers": {
                "not-a-dict": "invalid",
                "good": {"type": "azure_openai", "model": "gpt-4o", "endpoint": "https://x.com"},
            }
        }
        with pytest.warns(UserWarning):
            snapshot = load_config(config_dict=config_dict)
        assert "not-a-dict" not in snapshot.providers
        assert "good" in snapshot.providers

    def test_invalid_provider_type_skipped(self):
        """Provider with invalid type value is skipped."""
        config_dict = {
            "providers": {
                "bad-type": {"type": "invalid_provider", "model": "gpt-4o"},
            }
        }
        with pytest.warns(UserWarning):
            snapshot = load_config(config_dict=config_dict)
        assert "bad-type" not in snapshot.providers

    def test_non_mapping_root_is_safely_ignored(self):
        """Non-dict root config should degrade to empty sections."""
        with pytest.warns(UserWarning):
            snapshot = load_config(config_dict="not-a-dict")  # type: ignore[arg-type]
        assert snapshot.providers == {}
        assert snapshot.workflows == {}
        assert snapshot.defaults == {}

    def test_non_mapping_sections_are_safely_ignored(self):
        """Non-dict providers/workflows/defaults sections should be treated as empty."""
        with pytest.warns(UserWarning):
            snapshot = load_config(
                config_dict={
                    "providers": ["invalid"],
                    "workflows": "invalid",
                    "defaults": ["invalid"],
                }
            )
        assert snapshot.providers == {}
        assert snapshot.workflows == {}
        assert snapshot.defaults == {}

    def test_provider_with_empty_model_is_skipped(self):
        """Provider with empty or missing model string is silently skipped."""
        config_dict = {
            "providers": {
                "no-model": {"type": "azure_openai"},
                "empty-model": {"type": "azure_openai", "model": ""},
                "good": {"type": "azure_openai", "model": "gpt-4o", "endpoint": "https://x.com"},
            }
        }
        with pytest.warns(UserWarning):
            snapshot = load_config(config_dict=config_dict)
        assert "no-model" not in snapshot.providers
        assert "empty-model" not in snapshot.providers
        assert "good" in snapshot.providers

    def test_provider_with_whitespace_only_model_is_skipped(self):
        """Provider with whitespace-only model string is skipped (not just empty-string)."""
        config_dict = {
            "providers": {
                "whitespace-model": {"type": "azure_openai", "model": "   "},
                "good": {"type": "azure_openai", "model": "gpt-4o", "endpoint": "https://x.com"},
            }
        }
        with pytest.warns(UserWarning):
            snapshot = load_config(config_dict=config_dict)
        assert "whitespace-model" not in snapshot.providers
        assert "good" in snapshot.providers

    def test_provider_with_non_string_model_is_skipped(self):
        """Provider with a non-string model value (e.g. null or integer) is skipped."""
        config_dict = {
            "providers": {
                "null-model": {"type": "azure_openai", "model": None},
                "int-model": {"type": "azure_openai", "model": 42},
                "good": {"type": "azure_openai", "model": "gpt-4o", "endpoint": "https://x.com"},
            }
        }
        with pytest.warns(UserWarning):
            snapshot = load_config(config_dict=config_dict)
        assert "null-model" not in snapshot.providers
        assert "int-model" not in snapshot.providers
        assert "good" in snapshot.providers

    def test_provider_model_is_stripped(self):
        """Leading/trailing whitespace around a valid model name is stripped."""
        config_dict = {
            "providers": {
                "padded": {"type": "azure_openai", "model": "  gpt-4o  ", "endpoint": "https://x.com"},
            }
        }
        snapshot = load_config(config_dict=config_dict)
        assert "padded" in snapshot.providers
        assert snapshot.providers["padded"].model == "gpt-4o"

    def test_string_max_tokens_is_coerced_to_int(self):
        """max_tokens as a quoted string should be coerced to int with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": "4096"},
            }
        }
        import pytest

        with pytest.warns(UserWarning, match="max_tokens"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens == 4096

    def test_string_temperature_is_coerced_to_float(self):
        """temperature as a quoted string should be coerced to float with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "temperature": "0.7"},
            }
        }
        import pytest

        with pytest.warns(UserWarning, match="temperature"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].temperature == pytest.approx(0.7)

    def test_string_timeout_seconds_is_coerced_to_int(self):
        """timeout_seconds as a quoted string should be coerced to int with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "timeout_seconds": "60"},
            }
        }
        import pytest

        with pytest.warns(UserWarning, match="timeout_seconds"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].timeout_seconds == 60

    def test_non_numeric_max_tokens_string_is_ignored(self):
        """Non-parseable max_tokens string should be ignored with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": "large"},
            }
        }
        import pytest

        with pytest.warns(UserWarning, match="max_tokens"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens is None

    def test_float_max_tokens_with_no_fractional_part_is_coerced_to_int(self):
        """max_tokens=4096.0 (whole-number float) should be coerced to int 4096."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": 4096.0},
            }
        }
        snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens == 4096
        assert isinstance(snapshot.providers["p"].max_tokens, int)

    def test_int_temperature_is_promoted_to_float(self):
        """temperature=1 (integer) should be silently promoted to float 1.0."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "temperature": 1},
            }
        }
        snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].temperature == 1.0
        assert isinstance(snapshot.providers["p"].temperature, float)

    def test_bool_max_tokens_is_ignored_with_warning(self):
        """Boolean max_tokens should be rejected (not coerced to int)."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": True},
            }
        }
        with pytest.warns(UserWarning, match="max_tokens"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens is None

    def test_bool_temperature_is_ignored_with_warning(self):
        """Boolean temperature should be rejected (not coerced to float)."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "temperature": False},
            }
        }
        with pytest.warns(UserWarning, match="temperature"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].temperature is None

    def test_negative_temperature_is_ignored_with_warning(self):
        """Negative temperature should be rejected with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "temperature": -0.1},
            }
        }
        with pytest.warns(UserWarning, match="temperature"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].temperature is None

    def test_temperature_above_two_is_ignored_with_warning(self):
        """temperature > 2 should be rejected with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "temperature": 2.1},
            }
        }
        with pytest.warns(UserWarning, match="temperature"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].temperature is None

    def test_out_of_range_string_temperature_is_ignored_with_warning(self):
        """Out-of-range temperature provided as string should be rejected with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "temperature": "2.5"},
            }
        }
        with pytest.warns(UserWarning, match="temperature"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].temperature is None

    def test_unexpected_type_max_tokens_is_ignored_with_warning(self):
        """max_tokens with an unexpected type (e.g. list) should be ignored with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": [4096]},
            }
        }
        import pytest

        with pytest.warns(UserWarning, match="max_tokens"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens is None

    def test_unexpected_type_temperature_is_ignored_with_warning(self):
        """temperature with an unexpected type (e.g. list) should be ignored with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "temperature": [0.7]},
            }
        }
        import pytest

        with pytest.warns(UserWarning, match="temperature"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].temperature is None

    def test_negative_int_max_tokens_is_ignored_with_warning(self):
        """Negative integer max_tokens should be rejected with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": -1},
            }
        }
        with pytest.warns(UserWarning, match="max_tokens"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens is None

    def test_negative_float_max_tokens_is_ignored_with_warning(self):
        """Negative whole-number float max_tokens should be rejected with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": -128.0},
            }
        }
        with pytest.warns(UserWarning, match="max_tokens"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens is None

    def test_negative_string_max_tokens_is_ignored_with_warning(self):
        """Negative max_tokens expressed as a quoted string should be rejected with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": "-512"},
            }
        }
        with pytest.warns(UserWarning, match="max_tokens"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].max_tokens is None

    def test_negative_int_timeout_seconds_is_ignored_with_warning(self):
        """Negative integer timeout_seconds should be rejected with a warning."""
        config_dict = {
            "providers": {
                "p": {"type": "azure_openai", "model": "gpt-4o", "timeout_seconds": -30},
            }
        }
        with pytest.warns(UserWarning, match="timeout_seconds"):
            snapshot = load_config(config_dict=config_dict)
        assert snapshot.providers["p"].timeout_seconds is None

    def test_integer_provider_key_is_skipped_with_warning(self):
        """Provider with a non-string key (e.g. unquoted YAML integer) should be skipped."""
        # In YAML, an unquoted integer key is parsed as int by yaml.safe_load.
        # We simulate that here by passing the dict directly.
        config_dict = {
            "providers": {
                42: {"type": "azure_openai", "model": "gpt-4o"},
                "good": {"type": "azure_openai", "model": "gpt-4o"},
            }
        }
        with pytest.warns(UserWarning, match="not a string"):
            snapshot = load_config(config_dict=config_dict)
        assert 42 not in snapshot.providers
        assert "good" in snapshot.providers

    def test_float_provider_key_is_skipped_with_warning(self):
        """Provider with a float key (e.g. unquoted YAML float) should be skipped."""
        config_dict = {
            "providers": {
                1.5: {"type": "azure_openai", "model": "gpt-4o"},
                "good": {"type": "openai_direct", "model": "gpt-4o-mini", "api_key_env": "KEY"},
            }
        }
        with pytest.warns(UserWarning, match="not a string"):
            snapshot = load_config(config_dict=config_dict)
        assert 1.5 not in snapshot.providers
        assert "good" in snapshot.providers

    def test_empty_string_provider_key_is_skipped_with_warning(self):
        """Provider with an empty-string key should be skipped with a warning."""
        config_dict = {
            "providers": {
                "": {"type": "azure_openai", "model": "gpt-4o"},
                "good": {"type": "azure_openai", "model": "gpt-4o"},
            }
        }
        with pytest.warns(UserWarning, match="empty or whitespace-only"):
            snapshot = load_config(config_dict=config_dict)
        assert "" not in snapshot.providers
        assert "good" in snapshot.providers

    def test_whitespace_only_provider_key_is_skipped_with_warning(self):
        """Provider with a whitespace-only key should be skipped and stripped to empty."""
        config_dict = {
            "providers": {
                "   ": {"type": "azure_openai", "model": "gpt-4o"},
                "good": {"type": "azure_openai", "model": "gpt-4o"},
            }
        }
        with pytest.warns(UserWarning, match="empty or whitespace-only"):
            snapshot = load_config(config_dict=config_dict)
        assert "   " not in snapshot.providers
        assert "" not in snapshot.providers  # stripped form also not present
        assert "good" in snapshot.providers

    def test_padded_provider_key_is_stored_under_stripped_name(self):
        """A provider key with leading/trailing whitespace is stored under its stripped form."""
        config_dict = {
            "providers": {
                "  my-provider  ": {"type": "azure_openai", "model": "gpt-4o"},
            }
        }
        snapshot = load_config(config_dict=config_dict)
        # Original padded key must not appear; only the stripped name is stored
        assert "  my-provider  " not in snapshot.providers
        assert "my-provider" in snapshot.providers
