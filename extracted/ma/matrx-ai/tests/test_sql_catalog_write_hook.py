"""sql tool writes to ai.* catalog tables notify the host reload hook."""

from __future__ import annotations

from matrx_ai import _ext
from matrx_ai.tools.implementations import database


def test_catalog_write_calls_hook(monkeypatch):
    seen: list[tuple[str, str, str]] = []
    monkeypatch.setitem(
        _ext._registry, "ai_catalog_write_hook", lambda s, t, v: seen.append((s, t, v))
    )
    database._after_catalog_write("ai", "offering", "update")
    database._after_catalog_write("ai", "model_definition", "insert")
    assert seen == [("ai", "offering", "update"), ("ai", "model_definition", "insert")]


def test_non_catalog_write_does_not_call_hook(monkeypatch):
    seen: list[tuple[str, str, str]] = []
    monkeypatch.setitem(
        _ext._registry, "ai_catalog_write_hook", lambda s, t, v: seen.append((s, t, v))
    )
    database._after_catalog_write("chat", "message", "insert")
    database._after_catalog_write(None, "offering", "insert")
    assert seen == []


def test_hook_exceptions_never_fail_the_write(monkeypatch):
    def _boom(*_a):
        raise RuntimeError("host exploded")

    monkeypatch.setitem(_ext._registry, "ai_catalog_write_hook", _boom)
    database._after_catalog_write("ai", "api", "update")  # must not raise


def test_every_catalog_table_is_covered():
    assert database.AI_CATALOG_TABLES >= {
        "ai.provider",
        "ai.model_definition",
        "ai.endpoint",
        "ai.api",
        "ai.offering",
        "ai.setting",
        "ai.model_alias",
    }


def test_catalog_rule_writer_rejects_processor_scalar_conflict():
    error = database._guard_catalog_rules(
        "ai",
        "offering",
        [
            {
                "id": "bad-offering",
                "override": {
                    "params": {
                        "reasoning_effort": {
                            "processor": "together_reasoning",
                            "value_map": {"high": "high"},
                        }
                    },
                    "constraints": [],
                },
            }
        ],
    )
    assert error is not None
    assert "processor cannot coexist" in error


def test_catalog_rule_writer_allows_processor_owned_rule():
    error = database._guard_catalog_rules(
        "ai",
        "offering",
        [
            {
                "override": {
                    "params": {
                        "reasoning_effort": {
                            "processor": "together_reasoning",
                            "processor_config": {"order": 100},
                        }
                    },
                    "constraints": [],
                }
            }
        ],
    )
    assert error is None
