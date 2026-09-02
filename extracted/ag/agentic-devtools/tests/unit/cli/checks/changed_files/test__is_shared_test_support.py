"""Tests for _is_shared_test_support."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.changed_files import _is_shared_test_support


class TestIsSharedTestSupport:
    """Tests for _is_shared_test_support."""

    @pytest.mark.parametrize(
        "name",
        ["conftest.py", "_contract_scenarios.py", "_helpers.py"],
    )
    def test_support_modules_true(self, name):
        assert _is_shared_test_support(name) is True

    @pytest.mark.parametrize(
        "name",
        ["__init__.py", "test_foo.py", "foo.py", "module.py"],
    )
    def test_non_support_modules_false(self, name):
        assert _is_shared_test_support(name) is False
