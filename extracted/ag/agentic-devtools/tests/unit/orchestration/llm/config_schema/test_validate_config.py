"""Tests for validate_config function."""

import pytest

from agentic_devtools.orchestration.llm.config_schema import validate_config


class TestValidateConfig:
    """Tests for validate_config."""

    def test_valid_minimal_config(self):
        errors = validate_config(
            {
                "providers": {
                    "main": {"type": "azure_openai", "model": "gpt-4o"},
                }
            }
        )
        assert errors == []

    def test_valid_copilot_config(self):
        errors = validate_config(
            {
                "providers": {
                    "copilot": {
                        "type": "copilot",
                        "model": "gemini-3.7-flash",
                        "timeout_seconds": 120,
                    }
                },
                "workflows": {
                    "pr_review": {
                        "default_provider": "copilot",
                        "model": "gemini-3.7-flash",
                        "nodes": {"review_files": {"provider": "copilot"}},
                    }
                },
            }
        )

        assert errors == []

    def test_copilot_rejects_temperature(self):
        errors = validate_config(
            {
                "providers": {
                    "copilot": {
                        "type": "copilot",
                        "model": "gemini-3.7-flash",
                        "temperature": 0.1,
                    }
                }
            }
        )

        assert any("temperature" in error for error in errors)

    def test_copilot_rejects_max_tokens(self):
        errors = validate_config(
            {
                "providers": {
                    "copilot": {
                        "type": "copilot",
                        "model": "gemini-3.7-flash",
                        "max_tokens": 4096,
                    }
                }
            }
        )

        assert any("max_tokens" in error for error in errors)

    def test_copilot_rejects_api_key_env(self):
        errors = validate_config(
            {
                "providers": {
                    "copilot": {
                        "type": "copilot",
                        "model": "gemini-3.7-flash",
                        "api_key_env": "DO_NOT_READ",
                    }
                }
            }
        )

        assert any("api_key_env" in error for error in errors)

    def test_missing_type_field(self):
        errors = validate_config(
            {
                "providers": {
                    "main": {"model": "gpt-4o"},
                }
            }
        )
        assert any("'type'" in e for e in errors)

    def test_missing_model_field(self):
        errors = validate_config(
            {
                "providers": {
                    "main": {"type": "azure_openai"},
                }
            }
        )
        assert any("'model'" in e for e in errors)

    def test_empty_string_model_field(self):
        """Empty string model value must be flagged as an error."""
        errors = validate_config(
            {
                "providers": {
                    "main": {"type": "azure_openai", "model": ""},
                }
            }
        )
        assert any("'model'" in e for e in errors)

    def test_whitespace_only_model_field(self):
        """Whitespace-only model value must be flagged as an error."""
        errors = validate_config(
            {
                "providers": {
                    "main": {"type": "azure_openai", "model": "   "},
                }
            }
        )
        assert any("'model'" in e for e in errors)

    def test_non_string_model_field(self):
        """Non-string model value must be flagged as an error."""
        errors = validate_config(
            {
                "providers": {
                    "main": {"type": "azure_openai", "model": 42},
                }
            }
        )
        assert any("'model'" in e for e in errors)
        errors = validate_config(
            {
                "providers": {
                    "main": {"type": "anthropic", "model": "claude"},
                }
            }
        )
        assert any("invalid type" in e for e in errors)

    def test_non_dict_config_returns_error(self):
        errors = validate_config("not a dict")  # type: ignore[arg-type]
        assert len(errors) > 0

    def test_single_node_mapping_no_error(self):
        """A node with explicit provider doesn't conflict with default."""
        errors = validate_config(
            {
                "providers": {
                    "p1": {"type": "azure_openai", "model": "gpt-4o"},
                    "p2": {"type": "openai_direct", "model": "gpt-4o-mini"},
                },
                "workflows": {
                    "pr_review": {
                        "default_provider": "p1",
                        "nodes": {
                            "analysis": {"provider": "p2"},
                        },
                    },
                },
            }
        )
        assert errors == []

    def test_same_provider_no_duplicate_error(self):
        """Same provider for a node doesn't raise."""
        errors = validate_config(
            {
                "providers": {
                    "p1": {"type": "azure_openai", "model": "gpt-4o"},
                },
                "workflows": {
                    "pr_review": {
                        "default_provider": "p1",
                        "nodes": {
                            "analysis": {"provider": "p1"},
                        },
                    },
                },
            }
        )
        assert errors == []

    def test_non_dict_providers_field(self):
        """Non-dict 'providers' field returns error."""
        errors = validate_config({"providers": "not a dict"})
        assert any("'providers' must be a dictionary" in e for e in errors)

    def test_non_dict_provider_entry(self):
        """Non-dict provider entry returns error."""
        errors = validate_config({"providers": {"bad": "not-a-dict"}})
        assert any("must be a dictionary" in e for e in errors)

    def test_non_dict_workflow_entry_skipped(self):
        """Non-dict workflow entries are skipped gracefully."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {"bad_workflow": "not a dict"},
            }
        )
        assert errors == []

    def test_non_dict_nodes_entry_skipped(self):
        """Non-dict nodes entries are skipped gracefully."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {"wf": {"nodes": "not a dict"}},
            }
        )
        assert errors == []

    def test_non_dict_node_entry_skipped(self):
        """Non-dict node entries are skipped gracefully."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {"wf": {"nodes": {"analysis": "not a dict"}}},
            }
        )
        assert errors == []

    def test_non_dict_workflows_field_skipped(self):
        """Non-dict 'workflows' field is skipped gracefully."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": "not a dict",
            }
        )
        assert errors == []

    def test_duplicate_node_mapping_raises(self):
        """Duplicate (workflow, node_type) with different providers raises."""
        from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError

        # To trigger this code path, we need the same (workflow_name, node_type) key
        # to appear twice with different providers during iteration. Since Python dicts
        # can't have duplicate keys, we patch the inner nodes dict to yield duplicates.

        class DuplicateItemsDict(dict):
            """Dict subclass that yields duplicate items."""

            def items(self):
                yield "analysis", {"provider": "p1"}
                yield "analysis", {"provider": "p2"}

        config = {
            "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
            "workflows": {
                "wf": {
                    "default_provider": "p1",
                    "nodes": DuplicateItemsDict(),
                }
            },
        }
        with pytest.raises(DuplicateNodeMappingError):
            validate_config(config)

    def test_non_string_node_provider_flagged_and_skipped(self):
        """Non-string node 'provider' value is flagged as error and not mapped."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {
                    "wf": {
                        "nodes": {
                            "analysis": {"provider": {"nested": "dict"}},
                        },
                    },
                },
            }
        )
        assert any("non-string" in e for e in errors)

    @pytest.mark.parametrize("provider_value", [0, False])
    def test_falsy_non_string_node_provider_is_flagged(self, provider_value):
        """Explicit falsy non-string node providers must not fall back silently."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {
                    "wf": {
                        "default_provider": "p1",
                        "nodes": {
                            "analysis": {"provider": provider_value},
                        },
                    },
                },
            }
        )
        assert any("non-string" in e for e in errors)

    def test_non_string_default_provider_flagged_and_skipped(self):
        """Non-string workflow 'default_provider' is flagged as error and not mapped."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {
                    "wf": {
                        "default_provider": ["list", "value"],
                        "nodes": {
                            "analysis": {},
                        },
                    },
                },
            }
        )
        assert any("non-string" in e for e in errors)

    def test_non_string_default_provider_no_nodes_is_flagged(self):
        """Non-string workflow 'default_provider' is caught even when the workflow has no nodes."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {
                    "wf": {
                        "default_provider": {"nested": "dict"},
                    },
                },
            }
        )
        assert any("non-string" in e for e in errors)

    def test_null_node_provider_falls_back_to_default_provider(self):
        """Explicit null 'provider' falls back to default_provider if that is a string."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {
                    "wf": {
                        "default_provider": "p1",
                        "nodes": {
                            "analysis": {"provider": None},
                        },
                    },
                },
            }
        )
        assert errors == []

    def test_empty_string_node_provider_falls_back_to_default_provider(self):
        """Explicit empty string 'provider' falls back to default_provider."""
        errors = validate_config(
            {
                "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
                "workflows": {
                    "wf": {
                        "default_provider": "p1",
                        "nodes": {
                            "analysis": {"provider": ""},
                        },
                    },
                },
            }
        )
        assert errors == []

    def test_empty_string_node_provider_maps_like_default_provider(self):
        """Empty-string provider must behave like the workflow default provider."""
        from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError

        class DuplicateItemsDict(dict):
            """Dict subclass that yields duplicate items."""

            def items(self):
                yield "analysis", {"provider": ""}
                yield "analysis", {"provider": "p1"}

        config = {
            "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
            "workflows": {
                "wf": {
                    "default_provider": "p1",
                    "nodes": DuplicateItemsDict(),
                }
            },
        }
        try:
            validate_config(config)
        except DuplicateNodeMappingError:
            pytest.fail("DuplicateNodeMappingError raised for empty-string provider fallback")

    def test_non_string_provider_does_not_cause_spurious_duplicate_error(self):
        """Non-string provider is flagged and skipped, not treated as a valid mapping."""
        from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError

        class DuplicateItemsDict(dict):
            """Dict subclass that yields duplicate items with non-string provider."""

            def items(self):
                yield "analysis", {"provider": {"nested": "dict"}}
                yield "analysis", {"provider": {"nested": "dict"}}

        config = {
            "providers": {"p1": {"type": "azure_openai", "model": "gpt-4o"}},
            "workflows": {"wf": {"nodes": DuplicateItemsDict()}},
        }
        # Must not raise DuplicateNodeMappingError — invalid values are flagged, not mapped
        try:
            validate_config(config)
        except DuplicateNodeMappingError:
            pytest.fail("DuplicateNodeMappingError raised for non-string provider values")
