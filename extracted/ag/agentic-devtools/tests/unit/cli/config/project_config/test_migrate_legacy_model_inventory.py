"""Tests for ``migrate_legacy_model_inventory``."""

import json
from datetime import UTC, datetime, timedelta

import pytest

import agentic_devtools.cli.config.project_config as project_config
from agentic_devtools.cli.config.project_config import DEFAULT_MODEL_ALLOWLIST, migrate_legacy_model_inventory


class TestMigrateLegacyModelInventory:
    """Tests for legacy model inventory migration."""

    def test_non_dict_config_raises(self):
        with pytest.raises(ValueError, match="config must be a dict"):
            migrate_legacy_model_inventory("bad")

    def test_empty_models_dict_is_removed(self):
        assert "models" not in migrate_legacy_model_inventory({"models": {}})

    def test_flat_inventory_normalizes_to_structured_tree(self):
        config = {
            "availableModels": ["claude-opus-4.8", "claude-opus-4.8", "gemini-3.5-flash"],
            "models": {"gemini-3.5-flash": {"modelId": "gemini-3.5-flash"}},
        }
        migrated = migrate_legacy_model_inventory(config)
        assert migrated["availableModels"] == ["claude-opus-4.8", "gemini-3.5-flash"]
        assert "claude-opus-4.8" in migrated["models"]
        assert "surfaces" in migrated["models"]["claude-opus-4.8"]

    def test_unknown_legacy_model_gets_unavailable_metadata_without_warning(self, capsys):
        """Migration keeps unavailable legacy rows quiet so repeated reads stay idempotent."""
        config = {"availableModels": ["unknown-model"]}
        migrated = migrate_legacy_model_inventory(config)
        assert migrated["availableModels"] == ["unknown-model"]
        assert migrated["models"]["unknown-model"]["pricingStatus"] == "unavailable"
        assert capsys.readouterr().err == ""

    def test_known_non_priceable_legacy_model_is_normalized(self, capsys):
        """Known routing pseudo-models stay available without a cost warning."""
        migrated = migrate_legacy_model_inventory({"availableModels": ["auto"]})
        assert migrated["availableModels"] == ["auto"]
        assert migrated["models"]["auto"]["pricingStatus"] == "non_priceable"
        assert capsys.readouterr().err == ""

    def test_non_string_legacy_entries_are_skipped(self):
        config = {"availableModels": [None, "", 7, "claude-opus-4.8"]}
        migrated = migrate_legacy_model_inventory(config)
        assert migrated["availableModels"] == ["claude-opus-4.8"]

    def test_models_tree_entry_without_valid_dict_is_skipped(self):
        """Non-dict models tree entries are excluded from the normalized output."""
        config = {
            "availableModels": ["claude-opus-4.8"],
            "models": {
                "claude-opus-4.8": {"modelId": "claude-opus-4.8"},
                "bad-entry": "not-a-dict",
            },
        }
        migrated = migrate_legacy_model_inventory(config)
        assert "claude-opus-4.8" in migrated["models"]
        assert "bad-entry" not in migrated["models"]

    def test_models_tree_non_string_key_is_skipped(self):
        """Models tree entries with non-string keys are excluded from the normalized output."""
        config = {
            "availableModels": ["claude-opus-4.8"],
            "models": {
                "claude-opus-4.8": {"modelId": "claude-opus-4.8"},
                7: {"modelId": "bad"},
            },
        }
        migrated = migrate_legacy_model_inventory(config)
        assert "claude-opus-4.8" in migrated["models"]
        assert 7 not in migrated["models"]

    def test_models_tree_blank_key_is_skipped(self):
        """Models tree entries with blank string keys are excluded from the normalized output."""
        config = {
            "availableModels": ["claude-opus-4.8"],
            "models": {
                "claude-opus-4.8": {"modelId": "claude-opus-4.8"},
                "  ": {"modelId": "blank"},
            },
        }
        migrated = migrate_legacy_model_inventory(config)
        assert "claude-opus-4.8" in migrated["models"]
        assert "  " not in migrated["models"]

    def test_invalid_models_tree_entry_warns_and_persists_unavailable_marker(self, capsys):
        """Models tree entries that fail validation are persisted as unavailable markers."""
        config = {
            "availableModels": ["claude-opus-4.8"],
            "models": {
                "claude-opus-4.8": {"modelId": "claude-opus-4.8"},
                "invalid": {"surfaces": {"copilot": "bad"}},
            },
        }
        migrated = migrate_legacy_model_inventory(config)
        assert "claude-opus-4.8" in migrated["models"]
        assert migrated["models"]["invalid"]["pricingStatus"] == "unavailable"
        assert migrated["models"]["invalid"].get("unavailableReason") == "invalid"
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_build_failure_in_legacy_list_preserves_available_models(self, monkeypatch, capsys):
        """When _build_model_metadata_entry raises for a legacy list model, it still
        stays in availableModels (probe result preserved) but has no normalized metadata,
        and a WARN_COST_DATA_INVALID warning is emitted."""

        def boom(model_id, *, existing_entry=None, warn_pricing_unavailable=True, emit_warnings=True):
            raise ValueError("boom")

        monkeypatch.setattr(project_config, "_build_model_metadata_entry", boom)
        migrated = migrate_legacy_model_inventory({"models": {}, "availableModels": ["claude-opus-4.8"]})
        assert migrated["availableModels"] == ["claude-opus-4.8"]
        assert "models" not in migrated
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_legacy_build_failure_with_tagged_warning_is_preserved(self, monkeypatch, capsys):
        """Tagged missing/invalid warning messages are emitted without reclassification."""

        def boom(model_id, *, existing_entry=None, warn_pricing_unavailable=True, emit_warnings=True):
            raise ValueError("WARN_COST_DATA_MISSING: synthetic missing data")

        monkeypatch.setattr(project_config, "_build_model_metadata_entry", boom)
        migrated = migrate_legacy_model_inventory({"models": {}, "availableModels": ["claude-opus-4.8"]})
        assert migrated["availableModels"] == ["claude-opus-4.8"]
        assert "models" not in migrated
        stderr = capsys.readouterr().err
        assert "WARN_COST_DATA_MISSING: synthetic missing data" in stderr
        assert "could not build normalized entry" not in stderr

    def test_valid_models_tree_only_is_preserved(self):
        migrated = migrate_legacy_model_inventory({"models": {"gpt-5-mini": {"modelId": "gpt-5-mini"}}})
        assert migrated["models"]["gpt-5-mini"]["modelId"] == "gpt-5-mini"

    def test_existing_priced_row_with_mismatched_key_persists_unavailable_marker(self, capsys):
        config = {
            "models": {
                "model-a": {
                    "modelId": "model-b",
                    "pricingStatus": "priceable",
                    "surfaces": {
                        "copilot": {"modelId": "model-b"},
                        "vscode": {"displayName": "Model B"},
                        "docs": {"displayName": "Model B"},
                    },
                }
            }
        }
        migrated = migrate_legacy_model_inventory(config)
        assert migrated["models"]["model-a"]["pricingStatus"] == "unavailable"
        assert migrated["models"]["model-a"].get("unavailableReason") == "invalid"
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_catalog_only_model_not_promoted_to_available_models(self):
        """Models in the catalog (models tree) that were not probe-discovered must not
        appear in availableModels."""
        config = {
            "availableModels": ["claude-opus-4.8"],
            "models": {"gpt-5-mini": {"modelId": "gpt-5-mini"}},
        }
        migrated = migrate_legacy_model_inventory(config)
        assert migrated["availableModels"] == ["claude-opus-4.8"]
        assert "gpt-5-mini" not in migrated["availableModels"]
        assert "gpt-5-mini" in migrated["models"]

    def test_idempotent_migration_produces_byte_stable_output(self):
        config = {"availableModels": ["claude-opus-4.8"]}
        once = migrate_legacy_model_inventory(config)
        twice = migrate_legacy_model_inventory(once)
        assert json.dumps(once, sort_keys=True) == json.dumps(twice, sort_keys=True)

    def test_invalid_existing_record_persists_unavailable_marker_during_migration(self):
        """Existing models tree entries that fail validate_model_metadata are persisted as unavailable."""
        fresh_timestamp = (datetime.now(UTC) - timedelta(days=1)).replace(microsecond=0).isoformat()
        migrated = migrate_legacy_model_inventory(
            {
                "models": {
                    "claude-opus-4.8": {
                        "modelId": "claude-opus-4.8",
                        "surfaces": {
                            "copilot": {"modelId": "claude-opus-4.8"},
                            "vscode": {"displayName": "claude-opus-4.8"},
                            "docs": {"displayName": "claude-opus-4.8"},
                        },
                        "inputRatePerM": 3,
                        "outputRatePerM": 15,
                        "currency": "USD",
                        "rateUnit": "USD per 1M tokens",
                        "assumedInputTokens": 100_000,
                        "assumedOutputTokens": 10_000,
                        "modelledSessionCost": "0.46",
                        "priceCategory": "standard",
                        "provenance": "curated",
                        "costDataAsOf": fresh_timestamp,
                    }
                }
            }
        )
        assert migrated["models"]["claude-opus-4.8"]["pricingStatus"] == "unavailable"
        assert migrated["models"]["claude-opus-4.8"].get("unavailableReason") == "invalid"

    def test_invalid_existing_model_blocks_catalog_rebuild(self, capsys):
        """Invalid existing rows block catalog fallback rebuild from availableModels."""
        fresh_timestamp = (datetime.now(UTC) - timedelta(days=1)).replace(microsecond=0).isoformat()
        migrated = migrate_legacy_model_inventory(
            {
                "availableModels": ["claude-opus-4.8"],
                "models": {
                    "claude-opus-4.8": {
                        "modelId": "gpt-5-mini",
                        "surfaces": {
                            "copilot": {"modelId": "gpt-5-mini"},
                            "vscode": {"displayName": "gpt-5-mini"},
                            "docs": {"displayName": "gpt-5-mini"},
                        },
                        "inputRatePerM": 3,
                        "outputRatePerM": 15,
                        "currency": "USD",
                        "rateUnit": "USD per 1M tokens",
                        "assumedInputTokens": 100_000,
                        "assumedOutputTokens": 10_000,
                        "modelledSessionCost": "0.45",
                        "priceCategory": "standard",
                        "provenance": "curated",
                        "costDataAsOf": fresh_timestamp,
                    }
                },
            }
        )
        assert migrated["models"]["claude-opus-4.8"]["pricingStatus"] == "unavailable"
        assert migrated["models"]["claude-opus-4.8"].get("unavailableReason") == "invalid"
        assert migrated["availableModels"] == ["claude-opus-4.8"]
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_invalid_existing_acp_row_round_trips_as_fail_closed_marker(self, capsys):
        """ACP-invalid rows persist a valid marker that stays unavailable after re-migration."""
        once = migrate_legacy_model_inventory(
            {
                "availableModels": ["claude-opus-4.8"],
                "models": {
                    "claude-opus-4.8": {
                        "modelId": "claude-opus-4.8",
                        "pricingStatus": "priceable",
                        "sourceMetadata": {"source": "acp-cache"},
                    }
                },
            }
        )

        warning_text = capsys.readouterr().err
        assert "WARN_COST_DATA_INVALID" in warning_text
        assert "source=acp-cache" in warning_text
        assert once["models"]["claude-opus-4.8"]["pricingStatus"] == "unavailable"
        assert once["models"]["claude-opus-4.8"]["unavailableReason"] == "invalid"
        assert once["models"]["claude-opus-4.8"]["provenance"] == "acp-cache"
        assert once["models"]["claude-opus-4.8"]["surfaces"]["copilot"]["modelId"] == "claude-opus-4.8"

        twice = migrate_legacy_model_inventory(once)

        assert twice["models"]["claude-opus-4.8"]["pricingStatus"] == "unavailable"
        assert twice["models"]["claude-opus-4.8"]["unavailableReason"] == "invalid"
        assert twice["models"]["claude-opus-4.8"]["provenance"] == "acp-cache"

    def test_missing_curated_fields_migrate_to_unavailable_without_warning(self, capsys):
        """Migration omits repeated unavailable warnings for incomplete legacy rows."""
        migrated = migrate_legacy_model_inventory(
            {
                "models": {
                    "unknown-model": {
                        "modelId": "unknown-model",
                        "surfaces": {
                            "copilot": {"modelId": "unknown-model"},
                            "vscode": {"displayName": "unknown-model"},
                            "docs": {"displayName": "unknown-model"},
                        },
                    }
                }
            }
        )
        assert migrated["models"]["unknown-model"]["pricingStatus"] == "unavailable"
        assert capsys.readouterr().err == ""

    def test_complete_supplied_inventory_is_retained_with_statuses(self, capsys):
        """Every supplied ACP ID receives a priceable, unavailable, or explicit non-priceable status."""
        migrated = migrate_legacy_model_inventory({"availableModels": list(DEFAULT_MODEL_ALLOWLIST)})
        assert migrated["availableModels"] == list(DEFAULT_MODEL_ALLOWLIST)
        assert set(migrated["models"]) == set(DEFAULT_MODEL_ALLOWLIST)
        assert migrated["models"]["auto"]["pricingStatus"] == "non_priceable"
        assert all(
            entry["pricingStatus"] in {"priceable", "unavailable", "non_priceable"}
            for entry in migrated["models"].values()
        )
        assert "ignoring unknown legacy model" not in capsys.readouterr().err

    def test_canonical_priceable_missing_data_persists_unavailable_marker(self, capsys):
        migrated = migrate_legacy_model_inventory(
            {
                "models": {
                    "model-a": {
                        "modelId": "model-a",
                        "pricingStatus": "priceable",
                        "surfaces": {
                            "copilot": {"modelId": "model-a"},
                            "vscode": {"displayName": "Model A"},
                            "docs": {"displayName": "Model A"},
                        },
                    }
                }
            }
        )
        assert migrated["models"]["model-a"]["pricingStatus"] == "unavailable"
        assert migrated["models"]["model-a"].get("unavailableReason") == "invalid"
        assert "WARN_COST_DATA_MISSING" in capsys.readouterr().err

    def test_explicit_invalid_pricing_status_persists_unavailable_marker(self, capsys):
        migrated = migrate_legacy_model_inventory(
            {
                "models": {
                    "claude-opus-4.8": {
                        "modelId": "claude-opus-4.8",
                        "pricingStatus": "unknown",
                        "currency": "USD",
                        "rateUnit": "USD per 1M tokens",
                        "inputRatePerM": "3",
                        "outputRatePerM": "15",
                        "assumedInputTokens": 1000,
                        "assumedOutputTokens": 1000,
                        "modelledSessionCost": "0.018",
                        "priceCategory": "standard",
                        "provenance": "curated-catalog",
                        "costDataAsOf": "2026-08-01T00:00:00+00:00",
                        "surfaces": {
                            "copilot": {"modelId": "claude-opus-4.8"},
                            "vscode": {"displayName": "Claude Opus 4.8"},
                            "docs": {"displayName": "Claude Opus 4.8"},
                        },
                    }
                }
            }
        )
        assert migrated["models"]["claude-opus-4.8"]["pricingStatus"] == "unavailable"
        assert migrated["models"]["claude-opus-4.8"].get("unavailableReason") == "invalid"
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_canonical_acp_unavailable_row_remains_unavailable_during_migration(self):
        """A persisted ACP unavailable row for a catalog model stays fail-closed."""
        config = {
            "models": {
                "claude-opus-4.8": {
                    "modelId": "claude-opus-4.8",
                    "pricingStatus": "unavailable",
                    "priceCategory": None,
                    "unavailableReason": "invalid",
                    "provenance": "acp-live",
                    "surfaces": {
                        "copilot": {"modelId": "claude-opus-4.8"},
                        "vscode": {"displayName": "Claude Opus 4.8"},
                        "docs": {"displayName": "Claude Opus 4.8"},
                    },
                }
            }
        }
        migrated = migrate_legacy_model_inventory(config)
        entry = migrated["models"]["claude-opus-4.8"]
        assert entry["pricingStatus"] == "unavailable"
        assert entry.get("inputRatePerM") is None
        assert entry["unavailableReason"] == "invalid"
        assert entry["provenance"] == "acp-live"

    def test_canonical_acp_unavailable_row_without_invalid_reason_upgrades_via_catalog_fallback(self):
        """A persisted ACP unavailable row without invalid-pricing reason can be catalog-upgraded."""
        config = {
            "models": {
                "claude-opus-4.8": {
                    "modelId": "claude-opus-4.8",
                    "pricingStatus": "unavailable",
                    "priceCategory": None,
                    "provenance": "acp-live",
                    "surfaces": {
                        "copilot": {"modelId": "claude-opus-4.8"},
                        "vscode": {"displayName": "Claude Opus 4.8"},
                        "docs": {"displayName": "Claude Opus 4.8"},
                    },
                }
            }
        }
        migrated = migrate_legacy_model_inventory(config)
        entry = migrated["models"]["claude-opus-4.8"]
        assert entry["pricingStatus"] == "priceable"
        assert entry.get("inputRatePerM") is not None
        assert entry.get("unavailableReason") is None
        assert entry["provenance"] == "curated-catalog"

    def test_canonical_project_unavailable_row_is_upgraded_to_priceable_via_catalog_fallback(self):
        """A non-ACP unavailable row for a catalog model can be repaired from catalog rates."""
        config = {
            "models": {
                "claude-opus-4.8": {
                    "modelId": "claude-opus-4.8",
                    "pricingStatus": "unavailable",
                    "priceCategory": None,
                    "provenance": "project-config",
                    "surfaces": {
                        "copilot": {"modelId": "claude-opus-4.8"},
                        "vscode": {"displayName": "Claude Opus 4.8"},
                        "docs": {"displayName": "Claude Opus 4.8"},
                    },
                }
            }
        }
        migrated = migrate_legacy_model_inventory(config)
        entry = migrated["models"]["claude-opus-4.8"]
        assert entry["pricingStatus"] == "priceable"
        assert entry.get("inputRatePerM") is not None
        assert entry["provenance"] == "curated-catalog"

    def test_emit_warnings_false_suppresses_invalid_legacy_candidate_warning(self, capsys, monkeypatch):
        """Silent read-time migration drops invalid legacy candidates without re-warning."""

        def fail_build(*_args, **_kwargs):
            raise ValueError("boom")

        monkeypatch.setattr(project_config, "_build_model_metadata_entry", fail_build)

        migrated = migrate_legacy_model_inventory({"availableModels": ["model-a"]}, emit_warnings=False)

        assert migrated["availableModels"] == ["model-a"]
        assert "models" not in migrated
        assert capsys.readouterr().err == ""

    def test_emit_warnings_false_silences_invalid_observed_at_on_unavailable_row(self, capsys):
        """An unavailable canonical row with a malformed observedAt emits no warning on load.

        Repeated reads (emit_warnings=False) must stay completely silent so that every
        ``agdt-*`` command invocation does not re-emit the same WARN_COST_DATA_INVALID
        for a stale persisted row that was already warned about during discovery.
        """
        config = {
            "models": {
                "unknown-model-x": {
                    "modelId": "unknown-model-x",
                    "pricingStatus": "unavailable",
                    "priceCategory": "low",
                    "provenance": "acp-live",
                    "observedAt": "not-a-timestamp",
                    "surfaces": {
                        "copilot": {"modelId": "unknown-model-x"},
                        "vscode": {"displayName": "Unknown Model X"},
                        "docs": {"displayName": "Unknown Model X"},
                    },
                }
            }
        }
        migrate_legacy_model_inventory(config, emit_warnings=False)
        assert capsys.readouterr().err == ""

    def test_emit_warnings_true_surfaces_invalid_observed_at_on_unavailable_row(self, capsys):
        """The same malformed observedAt row DOES warn when emit_warnings=True (default)."""
        config = {
            "models": {
                "unknown-model-x": {
                    "modelId": "unknown-model-x",
                    "pricingStatus": "unavailable",
                    "priceCategory": "low",
                    "provenance": "acp-live",
                    "observedAt": "not-a-timestamp",
                    "surfaces": {
                        "copilot": {"modelId": "unknown-model-x"},
                        "vscode": {"displayName": "Unknown Model X"},
                        "docs": {"displayName": "Unknown Model X"},
                    },
                }
            }
        }
        migrate_legacy_model_inventory(config)
        assert "WARN_COST_DATA_INVALID" in capsys.readouterr().err

    def test_emit_warnings_false_silences_stale_priceable_row_during_load(self, capsys):
        """A priceable canonical row with stale costDataAsOf emits no WARN_COST_DATA_STALE on load.

        Repeated reads must not re-emit staleness warnings for pricing data that was
        already warned about when the config was last saved.
        """
        stale_date = (datetime.now(UTC) - timedelta(days=100)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        config = {
            "models": {
                "claude-opus-4.8": {
                    "modelId": "claude-opus-4.8",
                    "pricingStatus": "priceable",
                    "currency": "USD",
                    "rateUnit": "USD per 1M tokens",
                    "inputRatePerM": "3",
                    "outputRatePerM": "15",
                    "assumedInputTokens": 1000,
                    "assumedOutputTokens": 1000,
                    "modelledSessionCost": "0.018",
                    "priceCategory": "medium",
                    "provenance": "curated-catalog",
                    "costDataAsOf": stale_date,
                    "surfaces": {
                        "copilot": {"modelId": "claude-opus-4.8"},
                        "vscode": {"displayName": "Claude Opus 4.8"},
                        "docs": {"displayName": "Claude Opus 4.8"},
                    },
                }
            }
        }
        migrate_legacy_model_inventory(config, emit_warnings=False)
        assert capsys.readouterr().err == ""

    def test_stale_priceable_row_emits_staleness_warning_only_once(self, capsys):
        """A stale canonical priceable row emits exactly one WARN_COST_DATA_STALE warning."""
        stale_date = (datetime.now(UTC) - timedelta(days=100)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        config = {
            "models": {
                "claude-opus-4.8": {
                    "modelId": "claude-opus-4.8",
                    "pricingStatus": "priceable",
                    "currency": "USD",
                    "rateUnit": "USD per 1M tokens",
                    "inputRatePerM": "3",
                    "outputRatePerM": "15",
                    "assumedInputTokens": 1000,
                    "assumedOutputTokens": 1000,
                    "modelledSessionCost": "0.018",
                    "priceCategory": "medium",
                    "provenance": "curated-catalog",
                    "costDataAsOf": stale_date,
                    "surfaces": {
                        "copilot": {"modelId": "claude-opus-4.8"},
                        "vscode": {"displayName": "Claude Opus 4.8"},
                        "docs": {"displayName": "Claude Opus 4.8"},
                    },
                }
            }
        }
        migrate_legacy_model_inventory(config)
        warning_text = capsys.readouterr().err
        assert warning_text.count("WARN_COST_DATA_STALE") == 1
        assert "model 'claude-opus-4.8'" in warning_text
        assert "source=curated-catalog" in warning_text
