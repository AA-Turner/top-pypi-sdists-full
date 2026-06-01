"""Tests for the level resolution algorithm."""

from unittest.mock import patch

import smplkit._debug as _debug_mod
from smplkit.logging._resolution import _find_resolution_source, resolve_level


class TestResolveLevelBasic:
    def test_logger_env_level_wins(self):
        loggers = {
            "com.example.sql": {
                "level": "DEBUG",
                "group": None,
                "managed": True,
                "environments": {"production": {"level": "ERROR"}},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, {}) == "ERROR"

    def test_logger_base_level_when_no_env(self):
        loggers = {
            "com.example.sql": {
                "level": "DEBUG",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, {}) == "DEBUG"

    def test_logger_base_level_when_different_env(self):
        loggers = {
            "com.example.sql": {
                "level": "DEBUG",
                "group": None,
                "managed": True,
                "environments": {"staging": {"level": "TRACE"}},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, {}) == "DEBUG"

    def test_fallback_to_info(self):
        assert resolve_level("unknown.logger", "production", {}, {}) == "INFO"


class TestResolveLevelGroupChain:
    def test_group_env_level(self):
        loggers = {
            "com.example.sql": {
                "level": None,
                "group": "group-1",
                "managed": True,
                "environments": {},
            }
        }
        groups = {
            "group-1": {
                "level": "WARN",
                "group": None,
                "environments": {"production": {"level": "ERROR"}},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, groups) == "ERROR"

    def test_group_base_level(self):
        loggers = {
            "com.example.sql": {
                "level": None,
                "group": "group-1",
                "managed": True,
                "environments": {},
            }
        }
        groups = {
            "group-1": {
                "level": "WARN",
                "group": None,
                "environments": {},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, groups) == "WARN"

    def test_nested_group_chain(self):
        loggers = {
            "com.example.sql": {
                "level": None,
                "group": "group-child",
                "managed": True,
                "environments": {},
            }
        }
        groups = {
            "group-child": {
                "level": None,
                "group": "group-parent",
                "environments": {},
            },
            "group-parent": {
                "level": "FATAL",
                "group": None,
                "environments": {},
            },
        }
        assert resolve_level("com.example.sql", "production", loggers, groups) == "FATAL"

    def test_group_cycle_does_not_infinite_loop(self):
        loggers = {
            "com.example.sql": {
                "level": None,
                "group": "group-a",
                "managed": True,
                "environments": {},
            }
        }
        groups = {
            "group-a": {
                "level": None,
                "group": "group-b",
                "environments": {},
            },
            "group-b": {
                "level": None,
                "group": "group-a",
                "environments": {},
            },
        }
        # Should fall through to INFO without looping
        assert resolve_level("com.example.sql", "production", loggers, groups) == "INFO"


class TestResolveLevelDotAncestry:
    def test_parent_logger_level(self):
        loggers = {
            "com.example": {
                "level": "WARN",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, {}) == "WARN"

    def test_grandparent_logger_level(self):
        loggers = {
            "com": {
                "level": "ERROR",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, {}) == "ERROR"

    def test_closest_ancestor_wins(self):
        loggers = {
            "com": {
                "level": "ERROR",
                "group": None,
                "managed": True,
                "environments": {},
            },
            "com.example": {
                "level": "DEBUG",
                "group": None,
                "managed": True,
                "environments": {},
            },
        }
        assert resolve_level("com.example.sql", "production", loggers, {}) == "DEBUG"

    def test_group_takes_precedence_over_dot_ancestor(self):
        loggers = {
            "com.example.sql": {
                "level": None,
                "group": "group-1",
                "managed": True,
                "environments": {},
            },
            "com.example": {
                "level": "DEBUG",
                "group": None,
                "managed": True,
                "environments": {},
            },
        }
        groups = {
            "group-1": {
                "level": "ERROR",
                "group": None,
                "environments": {},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, groups) == "ERROR"

    def test_ancestor_env_level(self):
        loggers = {
            "com.example": {
                "level": "DEBUG",
                "group": None,
                "managed": True,
                "environments": {"production": {"level": "FATAL"}},
            }
        }
        assert resolve_level("com.example.sql", "production", loggers, {}) == "FATAL"


class TestResolveLevelEdgeCases:
    def test_logger_not_in_loggers_dict(self):
        assert resolve_level("nonexistent", "prod", {}, {}) == "INFO"

    def test_group_id_not_in_groups_dict(self):
        loggers = {
            "com.example": {
                "level": None,
                "group": "missing-group-id",
                "managed": True,
                "environments": {},
            }
        }
        # Falls through group chain (missing), then no dot ancestry, fallback
        assert resolve_level("com.example", "prod", loggers, {}) == "INFO"

    def test_empty_environments_dict(self):
        loggers = {
            "test": {
                "level": "WARN",
                "group": None,
                "managed": True,
                "environments": None,
            }
        }
        assert resolve_level("test", "prod", loggers, {}) == "WARN"


class TestFindResolutionSource:
    """Coverage for _find_resolution_source — the debug-only source detector."""

    _LOGGERS = {
        "with.env": {
            "level": "DEBUG",
            "group": None,
            "environments": {"production": {"level": "ERROR"}},
        },
        "with.base": {
            "level": "WARN",
            "group": None,
            "environments": {},
        },
        "with.group": {
            "level": None,
            "group": "g1",
            "environments": {},
        },
        "no.resolution": {
            "level": None,
            "group": None,
            "environments": {},
        },
    }
    _GROUPS = {
        "g1": {"level": "DEBUG", "group": None, "environments": {}},
    }

    def test_env_override_source(self):
        source = _find_resolution_source("with.env", "production", self._LOGGERS, self._GROUPS)
        assert source == 'env override "production"'

    def test_base_level_source(self):
        source = _find_resolution_source("with.base", "production", self._LOGGERS, self._GROUPS)
        assert source == "base level"

    def test_group_source(self):
        source = _find_resolution_source("with.group", "production", self._LOGGERS, self._GROUPS)
        assert source == 'group "g1"'

    def test_unknown_source_when_no_resolution(self):
        source = _find_resolution_source("no.resolution", "production", self._LOGGERS, self._GROUPS)
        assert source == "unknown"

    def test_not_found_when_logger_missing(self):
        source = _find_resolution_source("missing", "production", {}, {})
        assert source == "not found"


class TestResolveLevelDebugOutput:
    """Verify resolve_level emits debug output when enabled."""

    def test_debug_output_for_direct_resolution(self, capsys):
        loggers = {
            "sql": {
                "level": "DEBUG",
                "group": None,
                "environments": {"prod": {"level": "ERROR"}},
            }
        }
        with patch.object(_debug_mod, "_DEBUG_ENABLED", True):
            result = resolve_level("sql", "prod", loggers, {})

        assert result == "ERROR"
        captured = capsys.readouterr()
        assert "[smplkit:resolution]" in captured.err
        assert "sql" in captured.err
        assert "ERROR" in captured.err
