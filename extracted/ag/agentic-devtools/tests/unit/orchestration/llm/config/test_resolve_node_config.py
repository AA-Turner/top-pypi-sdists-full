"""Tests for resolve_node_config function."""

import warnings

import pytest

from agentic_devtools.orchestration.llm.config import load_config, resolve_node_config
from agentic_devtools.orchestration.llm.errors import ProviderNotConfiguredError
from agentic_devtools.orchestration.llm.types import ProviderType


class TestResolveNodeConfig:
    """Tests for resolve_node_config."""

    def test_resolves_from_global_default(self):
        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o", "temperature": 0.7}},
                "defaults": {"provider": "main"},
            }
        )
        config = resolve_node_config(snapshot, "any_workflow", "any_node")
        assert config is not None
        assert config.model == "gpt-4o"
        assert config.provider_type == ProviderType.AZURE_OPENAI

    def test_workflow_level_override(self):
        snapshot = load_config(
            config_dict={
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o"},
                    "fast": {"type": "openai_direct", "model": "gpt-4o-mini"},
                },
                "defaults": {"provider": "main"},
                "workflows": {
                    "pr_review": {"default_provider": "fast"},
                },
            }
        )
        config = resolve_node_config(snapshot, "pr_review", "analysis")
        assert config is not None
        assert config.provider_id == "fast"

    def test_node_level_override(self):
        snapshot = load_config(
            config_dict={
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o"},
                    "fast": {"type": "openai_direct", "model": "gpt-4o-mini"},
                },
                "defaults": {"provider": "main"},
                "workflows": {
                    "pr_review": {
                        "default_provider": "main",
                        "nodes": {
                            "summary": {"provider": "fast", "temperature": 0.2, "max_tokens": 500},
                        },
                    },
                },
            }
        )
        config = resolve_node_config(snapshot, "pr_review", "summary")
        assert config is not None
        assert config.provider_id == "fast"
        assert config.params_override["temperature"] == 0.2
        assert config.params_override["max_tokens"] == 500

    def test_node_model_override(self):
        snapshot = load_config(
            config_dict={
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "defaults": {"provider": "main"},
                "workflows": {
                    "work_on_issue": {
                        "nodes": {
                            "planning": {"model": "gpt-4o-mini"},
                        },
                    },
                },
            }
        )
        config = resolve_node_config(snapshot, "work_on_issue", "planning")
        assert config is not None
        assert config.model_override == "gpt-4o-mini"
        assert config.effective_model == "gpt-4o-mini"

    def test_returns_synthesized_provider_when_no_providers(self):
        snapshot = load_config(config_dict={"providers": {}})
        with pytest.warns(
            UserWarning, match="LLM config: no providers configured; synthesizing fallback OPENAI_DIRECT"
        ):
            config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.provider_type == ProviderType.OPENAI_DIRECT

    def test_pr_review_without_provider_does_not_synthesize_openai(self):
        snapshot = load_config(config_dict={"providers": {}})

        with pytest.raises(ProviderNotConfiguredError):
            resolve_node_config(snapshot, "pr_review", "review_files")

    def test_pr_review_missing_explicit_provider_does_not_fallback(self):
        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {"pr_review": {"default_provider": "missing"}},
            }
        )

        with pytest.raises(ProviderNotConfiguredError):
            resolve_node_config(snapshot, "pr_review", "review_files")

    def test_effective_temperature_from_override(self):
        snapshot = load_config(
            config_dict={
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o", "temperature": 0.7},
                },
                "defaults": {"provider": "main"},
                "workflows": {
                    "w": {"nodes": {"n": {"temperature": 0.1}}},
                },
            }
        )
        config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.effective_temperature == 0.1

    def test_fallback_to_first_provider_when_id_not_found(self):
        snapshot = load_config(
            config_dict={
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "defaults": {"provider": "nonexistent"},
            }
        )
        with pytest.warns(UserWarning, match="not found"):
            config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.provider_id == "main"

    def test_timeout_seconds_in_node_config(self):
        snapshot = load_config(
            config_dict={
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "defaults": {"provider": "main"},
                "workflows": {
                    "w": {"nodes": {"n": {"timeout_seconds": 120}}},
                },
            }
        )
        config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.params_override["timeout_seconds"] == 120

    def test_copilot_ignores_effective_temperature_and_max_tokens(self):
        with pytest.warns(UserWarning):
            snapshot = load_config(
                config_dict={
                    "providers": {
                        "copilot": {
                            "type": "copilot",
                            "model": "gemini-3.7-flash",
                            "temperature": 0.1,
                            "max_tokens": 4096,
                        }
                    },
                    "defaults": {
                        "provider": "copilot",
                        "temperature": 0.2,
                        "max_tokens": 2048,
                    },
                    "workflows": {
                        "pr_review": {
                            "nodes": {
                                "review_files": {
                                    "temperature": 0.3,
                                    "max_tokens": 1024,
                                    "timeout_seconds": 30,
                                }
                            }
                        }
                    },
                }
            )
            config = resolve_node_config(snapshot, "pr_review", "review_files")

        assert config.temperature is None
        assert config.max_tokens is None
        assert "temperature" not in config.params_override
        assert "max_tokens" not in config.params_override
        assert config.params_override["timeout_seconds"] == 30

    def test_copilot_without_unsupported_options_emits_no_warning(self):
        snapshot = load_config(
            config_dict={
                "providers": {
                    "copilot": {
                        "type": "copilot",
                        "model": "gemini-3.7-flash",
                    }
                },
                "defaults": {"provider": "copilot"},
            }
        )

        with warnings.catch_warnings(record=True) as record:
            warnings.simplefilter("always")
            config = resolve_node_config(snapshot, "pr_review", "review_files")

        assert not record
        assert config.temperature is None
        assert config.max_tokens is None

    def test_copilot_warns_when_only_temperature_is_set(self):
        with pytest.warns(UserWarning):
            snapshot = load_config(
                config_dict={
                    "providers": {
                        "copilot": {
                            "type": "copilot",
                            "model": "gemini-3.7-flash",
                            "temperature": 0.1,
                        }
                    },
                    "defaults": {"provider": "copilot"},
                }
            )
            config = resolve_node_config(snapshot, "pr_review", "review_files")

        assert config.temperature is None
        assert config.max_tokens is None

    def test_copilot_warns_when_only_max_tokens_is_set(self):
        with pytest.warns(UserWarning):
            snapshot = load_config(
                config_dict={
                    "providers": {
                        "copilot": {
                            "type": "copilot",
                            "model": "gemini-3.7-flash",
                            "max_tokens": 4096,
                        }
                    },
                    "defaults": {"provider": "copilot"},
                }
            )
            config = resolve_node_config(snapshot, "pr_review", "review_files")

        assert config.temperature is None
        assert config.max_tokens is None

    def test_non_dict_workflow_entry_falls_back_to_defaults(self):
        """Non-dict workflow entries in the snapshot are treated as absent."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot
        from agentic_devtools.orchestration.llm.types import ProviderType

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        # Manually patch workflows with a non-dict entry to bypass load_config filtering
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": "not-a-dict"},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "my_wf", "any_node")
        assert config is not None
        assert config.provider_type == ProviderType.AZURE_OPENAI

    def test_non_dict_nodes_entry_falls_back_to_workflow_default(self):
        """Non-dict nodes value is treated as absent; workflow default provider is used."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot
        from agentic_devtools.orchestration.llm.types import ProviderType

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": "main", "nodes": "not-a-dict"}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "my_wf", "any_node")
        assert config is not None
        assert config.provider_type == ProviderType.AZURE_OPENAI

    def test_non_dict_node_cfg_falls_back_to_workflow_provider(self):
        """Non-dict node config is treated as absent; workflow default provider is used."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot
        from agentic_devtools.orchestration.llm.types import ProviderType

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": "main", "nodes": {"analysis": "not-a-dict"}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "my_wf", "analysis")
        assert config is not None
        assert config.provider_type == ProviderType.AZURE_OPENAI

    def test_zero_max_tokens_not_overridden_by_default(self):
        """Provider max_tokens=0 must not fall back to the global default."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main", "max_tokens": 4096},
            }
        )
        # Manually inject a ProviderConfig with max_tokens=0
        from agentic_devtools.orchestration.llm.types import ProviderConfig, ProviderType

        provider_zero = ProviderConfig(
            provider_id="main",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            max_tokens=0,
        )
        patched = LLMConfigSnapshot(
            providers={"main": provider_zero},
            workflows=snapshot.workflows,
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "any", "any")
        assert config is not None
        assert config.max_tokens == 0

    def test_zero_timeout_seconds_not_overridden_by_default(self):
        """Provider timeout_seconds=0 must not fall back to the global default."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot
        from agentic_devtools.orchestration.llm.types import ProviderConfig, ProviderType

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main", "timeout_seconds": 60},
            }
        )
        provider_zero = ProviderConfig(
            provider_id="main",
            provider_type=ProviderType.AZURE_OPENAI,
            model="gpt-4o",
            timeout_seconds=0,
        )
        patched = LLMConfigSnapshot(
            providers={"main": provider_zero},
            workflows=snapshot.workflows,
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "any", "any")
        assert config is not None
        assert config.timeout_seconds == 0

    def test_null_workflow_default_provider_falls_back_to_global(self):
        """null default_provider in workflow cfg should not override the global default."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {
                    "global-p": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "defaults": {"provider": "global-p"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": None}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "my_wf", "some_node")
        assert config is not None
        assert config.provider_id == "global-p"

    def test_null_node_provider_falls_back_to_workflow_default(self):
        """null provider in node cfg should not override the workflow default."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {
                    "wf-p": {"type": "openai_direct", "model": "gpt-4o-mini"},
                },
                "defaults": {"provider": "wf-p"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": "wf-p", "nodes": {"n": {"provider": None}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "my_wf", "n")
        assert config is not None
        assert config.provider_id == "wf-p"

    def test_null_temperature_override_does_not_shadow_provider_value(self):
        """temperature: null in node cfg must not override the provider's temperature."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o", "temperature": 0.7}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"temperature": None}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert "temperature" not in config.params_override

    def test_null_max_tokens_override_does_not_shadow_provider_value(self):
        """max_tokens: null in node cfg must not override the provider's max_tokens."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o", "max_tokens": 2048}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"max_tokens": None}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert "max_tokens" not in config.params_override

    def test_null_timeout_override_does_not_shadow_provider_value(self):
        """timeout_seconds: null in node cfg must not override the provider's timeout."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o", "timeout_seconds": 30}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"timeout_seconds": None}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert "timeout_seconds" not in config.params_override

    def test_whitespace_only_node_provider_falls_back_to_workflow_default(self):
        """Blank/whitespace-only provider string in node cfg is treated as absent."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"wf-p": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "wf-p"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"default_provider": "wf-p", "nodes": {"n": {"provider": "   "}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert config.provider_id == "wf-p"

    def test_whitespace_only_model_override_is_treated_as_no_override(self):
        """Whitespace-only model in node cfg is normalised to None (no override)."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"model": "   "}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert config.model_override is None

    def test_non_string_model_override_is_ignored_with_warning(self):
        """Non-string model value (e.g. an unquoted integer from YAML) is warned and ignored."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"model": 123}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="non-string"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert config.model_override is None
        # Provider's own model is still used
        assert config.effective_model == "gpt-4o"

    def test_dict_model_override_is_ignored_with_warning(self):
        """A dict value for model is warned about and ignored (no crash)."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"model": {"name": "gpt-4o"}}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="non-string"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert config.model_override is None

    def test_string_temperature_override_is_coerced(self):
        """String temperature value in node cfg should be coerced to float with a warning."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"temperature": "0.3"}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="temperature"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert config.params_override["temperature"] == pytest.approx(0.3)

    def test_string_max_tokens_override_is_coerced(self):
        """String max_tokens value in node cfg should be coerced to int with a warning."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"max_tokens": "2048"}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="max_tokens"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert config.params_override["max_tokens"] == 2048

    def test_string_timeout_override_is_coerced(self):
        """String timeout_seconds value in node cfg should be coerced to int with a warning."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"timeout_seconds": "90"}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="timeout_seconds"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert config.params_override["timeout_seconds"] == 90

    def test_non_numeric_max_tokens_override_is_ignored(self):
        """Non-numeric max_tokens string in node cfg should be ignored with a warning."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"max_tokens": "many"}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="max_tokens"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert "max_tokens" not in config.params_override

    def test_non_numeric_timeout_override_is_ignored(self):
        """Non-numeric timeout_seconds string in node cfg should be ignored with a warning."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"timeout_seconds": "forever"}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="timeout_seconds"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert "timeout_seconds" not in config.params_override

    def test_non_numeric_temperature_override_is_ignored(self):
        """Non-numeric temperature string in node cfg should be ignored with a warning."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"temperature": "hot"}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="temperature"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert "temperature" not in config.params_override

    def test_out_of_range_temperature_override_is_ignored(self):
        """Out-of-range temperature override should be ignored with a warning."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o", "temperature": 0.7},
                },
                "defaults": {"provider": "main"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"w": {"nodes": {"n": {"temperature": 2.5}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="temperature"):
            config = resolve_node_config(patched, "w", "n")
        assert config is not None
        assert "temperature" not in config.params_override
        assert config.effective_temperature == pytest.approx(0.7)

    def test_global_default_provider_is_stripped(self):
        """Whitespace in defaults.provider should be stripped before provider lookup."""
        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": "  main  "},
            }
        )
        config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.provider_id == "main"

    def test_non_string_global_default_provider_warns_on_fallback(self):
        """Non-string defaults.provider should warn when fallback provider is used."""
        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {"provider": 123},
            }
        )
        with pytest.warns(UserWarning, match="falling back to first configured provider"):
            config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.provider_id == "main"

    def test_providers_only_config_warns_on_fallback(self):
        """A providers-only config with no defaults should warn on fallback."""
        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
            }
        )
        with pytest.warns(UserWarning, match="falling back to first configured provider"):
            config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.provider_id == "main"

    def test_string_default_numeric_values_are_coerced(self):
        """String numeric defaults should be coerced when building the resolved node config."""
        snapshot = load_config(
            config_dict={
                "providers": {"main": {"type": "azure_openai", "model": "gpt-4o"}},
                "defaults": {
                    "provider": "main",
                    "max_tokens": "4096",
                    "temperature": "0.25",
                    "timeout_seconds": "90",
                },
            }
        )
        with pytest.warns(UserWarning, match="defaults"):
            config = resolve_node_config(snapshot, "w", "n")
        assert config is not None
        assert config.max_tokens == 4096
        assert config.temperature == pytest.approx(0.25)
        assert config.timeout_seconds == 90

    def test_non_string_workflow_default_provider_warns_and_falls_back(self):
        """Non-string workflow default_provider warns and falls back to global default."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {
                    "global-p": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "defaults": {"provider": "global-p"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": ["list", "value"]}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="non-string"):
            config = resolve_node_config(patched, "my_wf", "some_node")
        assert config is not None
        assert config.provider_id == "global-p"

    def test_non_string_workflow_default_provider_dict_warns_and_falls_back(self):
        """Dict-typed workflow default_provider warns and falls back to global default."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {
                    "global-p": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "defaults": {"provider": "global-p"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": {"nested": "dict"}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="non-string"):
            config = resolve_node_config(patched, "my_wf", "n")
        assert config is not None
        assert config.provider_id == "global-p"

    def test_non_string_node_provider_warns_and_falls_back_to_workflow_default(self):
        """Non-string node provider warns and falls back to workflow default provider."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {
                    "wf-p": {"type": "openai_direct", "model": "gpt-4o-mini"},
                },
                "defaults": {"provider": "wf-p"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": "wf-p", "nodes": {"n": {"provider": ["bad"]}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="non-string"):
            config = resolve_node_config(patched, "my_wf", "n")
        assert config is not None
        assert config.provider_id == "wf-p"

    def test_non_string_node_provider_dict_warns_and_falls_back(self):
        """Dict-typed node provider warns and falls back to workflow default provider."""
        from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot

        snapshot = load_config(
            config_dict={
                "providers": {
                    "wf-p": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "defaults": {"provider": "wf-p"},
            }
        )
        patched = LLMConfigSnapshot(
            providers=snapshot.providers,
            workflows={"my_wf": {"default_provider": "wf-p", "nodes": {"n": {"provider": {"k": "v"}}}}},
            defaults=snapshot.defaults,
            raw=snapshot.raw,
        )
        with pytest.warns(UserWarning, match="non-string"):
            config = resolve_node_config(patched, "my_wf", "n")
        assert config is not None
        assert config.provider_id == "wf-p"
