"""Tests for ProviderFactory."""

import time
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from agentic_devtools.orchestration.llm.config import load_config
from agentic_devtools.orchestration.llm.errors import AuthenticationError
from agentic_devtools.orchestration.llm.factory import ProviderFactory, get_provider
from agentic_devtools.orchestration.llm.providers.azure_openai import AzureOpenAIProvider
from agentic_devtools.orchestration.llm.providers.copilot import CopilotProvider
from agentic_devtools.orchestration.llm.providers.local_model import LocalModelProvider
from agentic_devtools.orchestration.llm.providers.openai_direct import OpenAIDirectProvider


class TestProviderFactory:
    """Tests for ProviderFactory."""

    def test_get_provider_returns_azure(self, monkeypatch):
        monkeypatch.setenv("AZURE_KEY", "test-key-123")
        config = load_config(
            config_dict={
                "providers": {
                    "azure-main": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "AZURE_KEY",
                    }
                },
                "defaults": {"provider": "azure-main"},
            }
        )
        factory = ProviderFactory(config)
        provider = factory.get_provider("any_node")
        assert isinstance(provider, AzureOpenAIProvider)

    def test_get_provider_returns_copilot_with_injected_transport(self):
        config = load_config(
            config_dict={
                "providers": {"copilot": {"type": "copilot", "model": "gemini-3.7-flash"}},
                "defaults": {"provider": "copilot"},
            }
        )
        transport = object()
        factory = ProviderFactory(config, copilot_transport_factory=lambda _config: transport)

        provider = factory.get_provider("review_files", "pr_review")

        assert isinstance(provider, CopilotProvider)
        assert provider._transport is transport

    def test_copilot_rejects_api_key_configuration(self):
        with pytest.warns(UserWarning, match="api_key_env"):
            config = load_config(
                config_dict={
                    "providers": {
                        "copilot": {
                            "type": "copilot",
                            "model": "gemini-3.7-flash",
                            "api_key_env": "UNUSED",
                        }
                    },
                    "defaults": {"provider": "copilot"},
                }
            )
        factory = ProviderFactory(config)
        with pytest.raises(ValueError, match="api_key_env"):
            factory.get_provider("review_files", "pr_review")

    @pytest.mark.asyncio
    async def test_preflight_runs_provider_preflight(self, monkeypatch):
        config = load_config(config_dict={"providers": {}})
        factory = ProviderFactory(config)
        provider = SimpleNamespace()
        preflight = AsyncMock()
        provider.preflight = preflight
        monkeypatch.setattr(factory, "get_provider", lambda *_args: provider)

        assert await factory.preflight("node", "workflow", models=["model"]) is provider
        preflight.assert_awaited_once_with(["model"])

    @pytest.mark.asyncio
    async def test_preflight_supports_provider_without_preflight(self, monkeypatch):
        factory = ProviderFactory(load_config(config_dict={"providers": {}}))
        provider = SimpleNamespace()
        monkeypatch.setattr(factory, "get_provider", lambda *_args: provider)

        assert await factory.preflight("node") is provider

    def test_get_provider_caches_instances(self, monkeypatch):
        monkeypatch.setenv("AZURE_KEY", "test-key")
        config = load_config(
            config_dict={
                "providers": {
                    "main": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "AZURE_KEY",
                    }
                },
                "defaults": {"provider": "main"},
            }
        )
        factory = ProviderFactory(config)
        p1 = factory.get_provider("node_a")
        p2 = factory.get_provider("node_b")
        assert p1 is p2  # Same provider cached

    def test_get_provider_thread_safe_cache(self, monkeypatch):
        monkeypatch.setenv("AZURE_KEY", "test-key")
        config = load_config(
            config_dict={
                "providers": {
                    "main": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "AZURE_KEY",
                    }
                },
                "defaults": {"provider": "main"},
            }
        )
        factory = ProviderFactory(config)

        created_instances = []

        def _fake_create_provider(_node_config):
            time.sleep(0.01)
            provider = object()
            created_instances.append(provider)
            return provider

        monkeypatch.setattr("agentic_devtools.orchestration.llm.factory._create_provider", _fake_create_provider)

        with ThreadPoolExecutor(max_workers=8) as executor:
            providers = list(executor.map(lambda _: factory.get_provider("node_a"), range(20)))

        assert len(created_instances) == 1
        assert all(provider is providers[0] for provider in providers)

    def test_raises_on_missing_api_key(self, monkeypatch):
        monkeypatch.delenv("MISSING_KEY", raising=False)
        config = load_config(
            config_dict={
                "providers": {
                    "main": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "MISSING_KEY",
                    }
                },
                "defaults": {"provider": "main"},
            }
        )
        factory = ProviderFactory(config)
        with pytest.raises(AuthenticationError):
            factory.get_provider("any_node")

    def test_synthesizes_fallback_on_no_provider_configured(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-123")
        config = load_config(config_dict={"providers": {}})
        factory = ProviderFactory(config)

        with pytest.warns(UserWarning, match="synthesizing fallback OPENAI_DIRECT"):
            provider = factory.get_provider("any_node")

        assert isinstance(provider, OpenAIDirectProvider)
        assert provider._model == "gpt-4o"

    def test_synthesizes_fallback_missing_api_key_raises_auth_error(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        config = load_config(config_dict={"providers": {}})
        factory = ProviderFactory(config)

        with pytest.warns(UserWarning, match="synthesizing fallback OPENAI_DIRECT"):
            with pytest.raises(AuthenticationError, match="OPENAI_API_KEY"):
                factory.get_provider("my_node", "my_workflow")

    def test_different_providers_for_different_nodes(self, monkeypatch):
        monkeypatch.setenv("AZURE_KEY", "ak")
        monkeypatch.setenv("OPENAI_KEY", "ok")
        config = load_config(
            config_dict={
                "providers": {
                    "azure": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "AZURE_KEY",
                    },
                    "openai": {
                        "type": "openai_direct",
                        "model": "gpt-4o-mini",
                        "api_key_env": "OPENAI_KEY",
                    },
                },
                "defaults": {"provider": "azure"},
                "workflows": {
                    "pr_review": {
                        "nodes": {
                            "summary": {"provider": "openai"},
                        },
                    },
                },
            }
        )
        factory = ProviderFactory(config)
        review_provider = factory.get_provider("analysis", "pr_review")
        summary_provider = factory.get_provider("summary", "pr_review")
        assert isinstance(review_provider, AzureOpenAIProvider)
        assert isinstance(summary_provider, OpenAIDirectProvider)

    def test_config_property(self, monkeypatch):
        config = load_config(config_dict={"providers": {}})
        factory = ProviderFactory(config)
        assert factory.config is config

    def test_get_local_model_provider(self, monkeypatch):
        config = load_config(
            config_dict={
                "providers": {
                    "local": {
                        "type": "local_model",
                        "model": "llama3",
                        "endpoint": "http://localhost:11434/v1",
                    }
                },
                "defaults": {"provider": "local"},
            }
        )
        factory = ProviderFactory(config)
        provider = factory.get_provider("any_node")
        assert isinstance(provider, LocalModelProvider)


class TestGetProviderFunction:
    """Tests for get_provider convenience function."""

    def test_returns_provider(self, monkeypatch):
        monkeypatch.setenv("TEST_KEY", "key123")
        config = load_config(
            config_dict={
                "providers": {
                    "main": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "TEST_KEY",
                    }
                },
                "defaults": {"provider": "main"},
            }
        )
        provider = get_provider("node_a", config=config)
        assert isinstance(provider, AzureOpenAIProvider)


class TestUnsupportedProviderType:
    """Tests for unsupported provider type in factory."""

    def test_unsupported_provider_type_raises(self):
        from unittest.mock import MagicMock

        from agentic_devtools.orchestration.llm.factory import _create_provider

        node_config = MagicMock()
        node_config.provider_type = MagicMock()
        node_config.api_key_env = None

        with pytest.raises(ValueError, match="Unsupported provider type"):
            _create_provider(node_config)


class TestProviderCacheKeyIncludesParams:
    """Tests that provider instances with different params are not shared."""

    def test_same_provider_different_temperature_gets_separate_instances(self, monkeypatch):
        """Nodes sharing a provider+model but differing in temperature must get separate instances."""
        monkeypatch.setenv("AZURE_KEY", "test-key-123")
        config = load_config(
            config_dict={
                "providers": {
                    "azure-main": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "AZURE_KEY",
                        "temperature": 0.0,
                    }
                },
                "workflows": {
                    "wf": {
                        "default_provider": "azure-main",
                        "nodes": {
                            "cool": {"provider": "azure-main", "temperature": 0.0},
                            "warm": {"provider": "azure-main", "temperature": 0.9},
                        },
                    }
                },
            }
        )
        factory = ProviderFactory(config)
        cool_provider = factory.get_provider("cool", "wf")
        warm_provider = factory.get_provider("warm", "wf")
        # Different temperatures → must NOT share the same instance
        assert cool_provider is not warm_provider

    def test_same_provider_different_timeout_override_gets_separate_instances(self, monkeypatch):
        """Nodes with different timeout overrides must not share cached provider instances."""
        monkeypatch.setenv("AZURE_KEY", "test-key-123")
        config = load_config(
            config_dict={
                "providers": {
                    "azure-main": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "AZURE_KEY",
                        "timeout_seconds": 30,
                    }
                },
                "workflows": {
                    "wf": {
                        "default_provider": "azure-main",
                        "nodes": {
                            "fast": {"provider": "azure-main", "timeout_seconds": 5},
                            "slow": {"provider": "azure-main", "timeout_seconds": 60},
                        },
                    }
                },
            }
        )
        factory = ProviderFactory(config)
        fast_provider = factory.get_provider("fast", "wf")
        slow_provider = factory.get_provider("slow", "wf")
        assert fast_provider is not slow_provider

    def test_cache_key_no_collision_when_provider_id_contains_colon(self, monkeypatch):
        """Provider IDs or model names containing ':' must not cause cache key collisions.

        A string-join key like "a:b:c" and "a:b:c" built from different component
        combinations (e.g. provider_id="team:azure", model="gpt" vs provider_id="team",
        model="azure:gpt") would collide. A tuple key is unambiguous.
        """
        monkeypatch.setenv("KEY_A", "key-a")
        monkeypatch.setenv("KEY_B", "key-b")
        config = load_config(
            config_dict={
                "providers": {
                    "team:azure": {
                        "type": "azure_openai",
                        "model": "gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "KEY_A",
                    },
                    "team": {
                        "type": "azure_openai",
                        "model": "azure:gpt-4o",
                        "endpoint": "https://test.openai.azure.com",
                        "api_key_env": "KEY_B",
                    },
                },
                "workflows": {
                    "wf": {
                        "nodes": {
                            "node_a": {"provider": "team:azure"},
                            "node_b": {"provider": "team"},
                        }
                    }
                },
            }
        )
        factory = ProviderFactory(config)
        provider_a = factory.get_provider("node_a", "wf")
        provider_b = factory.get_provider("node_b", "wf")
        # Different providers — must not collide to the same cached instance
        assert provider_a is not provider_b


class TestProviderValidationAndTimeoutOverrides:
    """Tests for provider creation validation and timeout override wiring."""

    def test_missing_api_key_env_for_openai_direct_raises(self):
        config = load_config(
            config_dict={
                "providers": {"openai": {"type": "openai_direct", "model": "gpt-4o-mini"}},
                "defaults": {"provider": "openai"},
            }
        )
        factory = ProviderFactory(config)
        with pytest.raises(AuthenticationError, match="api_key_env"):
            factory.get_provider("any_node")

    def test_missing_azure_endpoint_raises(self, monkeypatch):
        monkeypatch.setenv("AZURE_KEY", "test-key-123")
        config = load_config(
            config_dict={
                "providers": {"azure": {"type": "azure_openai", "model": "gpt-4o", "api_key_env": "AZURE_KEY"}},
                "defaults": {"provider": "azure"},
            }
        )
        factory = ProviderFactory(config)
        with pytest.raises(ValueError, match="endpoint"):
            factory.get_provider("any_node")

    @pytest.mark.parametrize(
        ("provider_cfg", "env_key", "node_type"),
        [
            (
                {
                    "type": "azure_openai",
                    "model": "gpt-4o",
                    "endpoint": "https://test.openai.azure.com",
                    "api_key_env": "AZURE_KEY",
                    "timeout_seconds": 30,
                },
                ("AZURE_KEY", "k"),
                "azure_node",
            ),
            (
                {
                    "type": "openai_direct",
                    "model": "gpt-4o-mini",
                    "api_key_env": "OPENAI_KEY",
                    "timeout_seconds": 30,
                },
                ("OPENAI_KEY", "k"),
                "openai_node",
            ),
            (
                {"type": "local_model", "model": "llama3", "timeout_seconds": 30},
                None,
                "local_node",
            ),
        ],
    )
    def test_node_timeout_override_is_applied_to_provider_instance(
        self,
        monkeypatch,
        provider_cfg,
        env_key,
        node_type,
    ):
        if env_key is not None:
            monkeypatch.setenv(env_key[0], env_key[1])

        config = load_config(
            config_dict={
                "providers": {"main": provider_cfg},
                "workflows": {"wf": {"default_provider": "main", "nodes": {node_type: {"timeout_seconds": 9}}}},
            }
        )
        factory = ProviderFactory(config)
        provider = factory.get_provider(node_type, "wf")
        assert provider._timeout_seconds == 9
