"""Tests for _max_open_deferrals in the defer_suppressed module."""

from __future__ import annotations

import os
from unittest.mock import patch

from agentic_devtools.cli.ci.pipeline.actions.defer_suppressed import (
    DEFAULT_MAX_OPEN_DEFERRALS,
    MAX_OPEN_DEFERRALS_ENV,
    _max_open_deferrals,
)


class TestMaxOpenDeferrals:
    """Tests for the open-deferral ceiling resolution."""

    @patch.dict(os.environ, {}, clear=True)
    def test_defaults_when_unset(self) -> None:
        assert _max_open_deferrals() == DEFAULT_MAX_OPEN_DEFERRALS

    @patch.dict(os.environ, {MAX_OPEN_DEFERRALS_ENV: "  "}, clear=True)
    def test_defaults_when_blank(self) -> None:
        assert _max_open_deferrals() == DEFAULT_MAX_OPEN_DEFERRALS

    @patch.dict(os.environ, {MAX_OPEN_DEFERRALS_ENV: "9"}, clear=True)
    def test_reads_override(self) -> None:
        assert _max_open_deferrals() == 9

    @patch.dict(os.environ, {MAX_OPEN_DEFERRALS_ENV: "many"}, clear=True)
    def test_defaults_when_not_an_integer(self) -> None:
        assert _max_open_deferrals() == DEFAULT_MAX_OPEN_DEFERRALS
