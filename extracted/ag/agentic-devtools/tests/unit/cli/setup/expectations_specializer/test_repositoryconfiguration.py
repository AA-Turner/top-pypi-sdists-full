"""Tests for the ``RepositoryConfiguration`` dataclass."""

from __future__ import annotations

import dataclasses
from types import MappingProxyType

import pytest

from agentic_devtools.cli.setup.expectations_specializer import RepositoryConfiguration


def _make() -> RepositoryConfiguration:
    return RepositoryConfiguration(
        repo="owner/repo",
        issue_adapter="github",
        has_npm=True,
        ssl_hosts=("a.internal",),
        system_only=False,
        version_pin="1.2.3",
        effective_flags=MappingProxyType({"system-only": False}),
    )


class TestRepositoryConfiguration:
    """Construction, field, and frozenness contract."""

    def test_construction_exposes_all_fields(self) -> None:
        """All declared fields are readable on the instance."""
        config = _make()
        assert config.repo == "owner/repo"
        assert config.issue_adapter == "github"
        assert config.has_npm is True
        assert config.ssl_hosts == ("a.internal",)
        assert config.system_only is False
        assert config.version_pin == "1.2.3"
        assert config.effective_flags["system-only"] is False

    def test_is_frozen(self) -> None:
        """The dataclass is frozen — attribute assignment raises."""
        config = _make()
        with pytest.raises(dataclasses.FrozenInstanceError):
            config.repo = "other/repo"  # type: ignore[misc]

    def test_all_fields_required(self) -> None:
        """Constructing without arguments raises ``TypeError``."""
        with pytest.raises(TypeError):
            RepositoryConfiguration()  # type: ignore[call-arg]

    def test_version_pin_accepts_none(self) -> None:
        """``version_pin`` accepts ``None`` for the unpinned case."""
        config = RepositoryConfiguration(
            repo="owner/repo",
            issue_adapter="github",
            has_npm=False,
            ssl_hosts=(),
            system_only=True,
            version_pin=None,
            effective_flags=MappingProxyType({}),
        )
        assert config.version_pin is None
