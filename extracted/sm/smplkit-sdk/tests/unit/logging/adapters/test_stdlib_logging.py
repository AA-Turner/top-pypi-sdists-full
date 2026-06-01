"""Tests for StdlibLoggingAdapter."""

from __future__ import annotations

import logging as stdlib_logging
from unittest.mock import patch

import smplkit._debug as _debug_mod
from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter


class TestDiscover:
    def test_finds_existing_loggers(self):
        test_name = "test.stdlib_adapter.discover_existing_001"
        stdlib_logging.getLogger(test_name)
        adapter = StdlibLoggingAdapter()
        result = adapter.discover()
        names = [n for n, _exp, _eff in result]
        assert test_name in names

    def test_finds_root(self):
        adapter = StdlibLoggingAdapter()
        result = adapter.discover()
        names = [n for n, _exp, _eff in result]
        assert "root" in names

    def test_skips_placeholders(self):
        test_name = "test.stdlib_adapter.placeholder.deep.logger_002"
        stdlib_logging.getLogger(test_name)
        adapter = StdlibLoggingAdapter()
        result = adapter.discover()
        for name, _exp, _eff in result:
            obj = stdlib_logging.root.manager.loggerDict.get(name)
            if obj is not None:
                assert isinstance(obj, stdlib_logging.Logger)

    def test_with_prefix_filter(self):
        test_name = "test.stdlib_adapter.prefix.match_003"
        other_name = "other.stdlib_adapter.prefix.no_match_003"
        stdlib_logging.getLogger(test_name)
        stdlib_logging.getLogger(other_name)
        adapter = StdlibLoggingAdapter(prefix="test.stdlib_adapter.prefix")
        result = adapter.discover()
        names = [n for n, _exp, _eff in result]
        assert test_name in names
        assert other_name not in names
        # root should not be included when prefix is set
        assert "root" not in names

    def test_discover_existing_false(self):
        test_name = "test.stdlib_adapter.no_discover_004"
        stdlib_logging.getLogger(test_name)
        adapter = StdlibLoggingAdapter(discover_existing=False)
        result = adapter.discover()
        assert result == []

    def test_returns_explicit_and_effective_level(self):
        """Logger with explicit level returns it; loggers without one return None."""
        test_name = "test.stdlib_adapter.level_check_005"
        lg = stdlib_logging.getLogger(test_name)
        lg.setLevel(stdlib_logging.ERROR)
        adapter = StdlibLoggingAdapter()
        result = adapter.discover()
        level_map = {n: (exp, eff) for n, exp, eff in result}
        explicit, effective = level_map[test_name]
        assert explicit == stdlib_logging.ERROR
        assert effective == stdlib_logging.ERROR

    def test_inherited_logger_has_null_explicit_level(self):
        """Logger with no explicit level has explicit=None, effective=parent level."""
        parent_name = "test.stdlib_adapter.inherit_parent_005b"
        child_name = "test.stdlib_adapter.inherit_parent_005b.child"
        parent_lg = stdlib_logging.getLogger(parent_name)
        parent_lg.setLevel(stdlib_logging.WARNING)
        child_lg = stdlib_logging.getLogger(child_name)
        child_lg.setLevel(0)  # NOTSET — will inherit from parent

        adapter = StdlibLoggingAdapter()
        result = adapter.discover()
        level_map = {n: (exp, eff) for n, exp, eff in result}
        assert child_name in level_map
        explicit, effective = level_map[child_name]
        assert explicit is None  # not explicitly set
        assert effective == stdlib_logging.WARNING  # inherits parent's level

    def test_root_logger_has_non_null_explicit_level(self):
        """Root logger always has an explicit level."""
        adapter = StdlibLoggingAdapter()
        result = adapter.discover()
        level_map = {n: (exp, eff) for n, exp, eff in result}
        assert "root" in level_map
        explicit, _effective = level_map["root"]
        assert explicit is not None  # root always has explicit level


class TestApplyLevel:
    def test_sets_level_on_logger(self):
        test_name = "test.stdlib_adapter.apply_level_006"
        lg = stdlib_logging.getLogger(test_name)
        lg.setLevel(stdlib_logging.DEBUG)
        adapter = StdlibLoggingAdapter()
        adapter.apply_level(test_name, stdlib_logging.ERROR)
        assert lg.level == stdlib_logging.ERROR


class TestInstallHook:
    def setup_method(self):
        self.adapter = StdlibLoggingAdapter()

    def teardown_method(self):
        self.adapter.uninstall_hook()

    def test_detects_new_loggers(self):
        discovered = []

        def on_new(name, explicit, effective):
            discovered.append((name, explicit, effective))

        self.adapter.install_hook(on_new)
        test_name = "test.stdlib_adapter.hook.new_007"
        stdlib_logging.getLogger(test_name)
        assert any(name == test_name for name, _exp, _eff in discovered)

    def test_hook_passes_explicit_and_effective(self):
        """Hook receives explicit_level (None when NOTSET) and effective_level."""
        parent_name = "test.stdlib_adapter.hook.levels_007b"
        parent_lg = stdlib_logging.getLogger(parent_name)
        parent_lg.setLevel(stdlib_logging.INFO)

        calls = []
        self.adapter.install_hook(lambda n, exp, eff: calls.append((n, exp, eff)))
        child_name = "test.stdlib_adapter.hook.levels_007b.child"
        stdlib_logging.getLogger(child_name)
        match = next((c for c in calls if c[0] == child_name), None)
        assert match is not None
        _name, explicit, effective = match
        assert explicit is None  # child has no explicit level
        assert effective == stdlib_logging.INFO  # inherits parent's INFO

    def test_does_not_fire_for_existing(self):
        test_name = "test.stdlib_adapter.hook.existing_008"
        stdlib_logging.getLogger(test_name)

        discovered = []
        self.adapter.install_hook(lambda n, _exp, _eff: discovered.append(n))
        stdlib_logging.getLogger(test_name)
        assert test_name not in discovered

    def test_idempotent_install(self):
        calls_1 = []
        calls_2 = []

        self.adapter.install_hook(lambda n, _exp, _eff: calls_1.append(n))
        self.adapter.install_hook(lambda n, _exp, _eff: calls_2.append(n))

        test_name = "test.stdlib_adapter.hook.idempotent_009"
        stdlib_logging.getLogger(test_name)
        assert test_name in calls_1
        assert test_name not in calls_2

    def test_prefix_filter_in_hook(self):
        adapter = StdlibLoggingAdapter(prefix="test.stdlib_adapter.hook.prefix")
        discovered = []
        adapter.install_hook(lambda n, _exp, _eff: discovered.append(n))

        match_name = "test.stdlib_adapter.hook.prefix.match_010"
        no_match = "other.no_match_010"
        stdlib_logging.getLogger(match_name)
        stdlib_logging.getLogger(no_match)

        assert match_name in discovered
        assert no_match not in discovered
        adapter.uninstall_hook()


class TestUninstallHook:
    def test_restores_original(self):
        adapter = StdlibLoggingAdapter()
        discovered = []
        adapter.install_hook(lambda n, _exp, _eff: discovered.append(n))
        adapter.uninstall_hook()

        test_name = "test.stdlib_adapter.uninstall_011"
        stdlib_logging.getLogger(test_name)
        assert test_name not in discovered

    def test_uninstall_without_install_is_noop(self):
        adapter = StdlibLoggingAdapter()
        adapter.uninstall_hook()  # Should not raise


class TestApplyLevelGuard:
    """Verify the applying guard suppresses re-reporting during apply_level."""

    def setup_method(self):
        self.adapter = StdlibLoggingAdapter()

    def teardown_method(self):
        self.adapter.uninstall_hook()

    def test_guard_suppresses_callback_during_apply(self):
        """When apply_level calls getLogger internally, the hook callback must not fire."""
        discovered = []
        self.adapter.install_hook(lambda n, exp, eff: discovered.append(n))

        # Use a logger name that does NOT yet exist so getLogger creates it during apply_level
        guard_test_name = "test.stdlib_adapter.guard.apply_level_new_012"
        # Pre-emptively make sure it doesn't exist in loggerDict
        stdlib_logging.root.manager.loggerDict.pop(guard_test_name, None)

        # The adapter tracks that we're "applying" this logger via the guard set
        self.adapter._applying_level.add(guard_test_name)
        try:
            # Simulate what apply_level does: call getLogger which triggers the patch
            stdlib_logging.getLogger(guard_test_name)
            # Guard is active — callback must NOT have fired
            assert guard_test_name not in discovered
        finally:
            self.adapter._applying_level.discard(guard_test_name)

    def test_guard_allows_callback_when_not_applying(self):
        """Without the guard, a new logger triggers the callback normally."""
        discovered = []
        self.adapter.install_hook(lambda n, exp, eff: discovered.append(n))

        normal_new = "test.stdlib_adapter.guard.normal_new_013"
        stdlib_logging.root.manager.loggerDict.pop(normal_new, None)
        stdlib_logging.getLogger(normal_new)
        assert normal_new in discovered

    def test_guard_debug_output_when_enabled(self, capsys):
        """When debug is enabled, the suppressed path emits a debug line."""
        discovered = []
        self.adapter.install_hook(lambda n, exp, eff: discovered.append(n))

        guard_name = "test.stdlib_adapter.guard.debug_014"
        stdlib_logging.root.manager.loggerDict.pop(guard_name, None)
        self.adapter._applying_level.add(guard_name)
        try:
            with patch.object(_debug_mod, "_DEBUG_ENABLED", True):
                stdlib_logging.getLogger(guard_name)
        finally:
            self.adapter._applying_level.discard(guard_name)

        captured = capsys.readouterr()
        assert "suppressed" in captured.err
        assert guard_name not in discovered
