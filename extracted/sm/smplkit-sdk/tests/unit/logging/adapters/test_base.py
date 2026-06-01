"""Tests for LoggingAdapter ABC and adapters __init__ lazy loading."""

from __future__ import annotations

import pytest

from smplkit.logging.adapters.base import LoggingAdapter


class TestLoggingAdapterABC:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            LoggingAdapter()  # type: ignore[abstract]

    def test_concrete_must_implement_all(self):
        class PartialAdapter(LoggingAdapter):
            @property
            def name(self) -> str:
                return "partial"

            def discover(self):  # type: ignore[override]
                return []

        with pytest.raises(TypeError):
            PartialAdapter()  # type: ignore[abstract]

    def test_concrete_subclass_works(self):
        class FullAdapter(LoggingAdapter):
            @property
            def name(self) -> str:
                return "full"

            def discover(self) -> list[tuple[str, int]]:
                return []

            def apply_level(self, logger_name: str, level: int) -> None:
                pass

            def install_hook(self, on_new_logger):  # type: ignore[override]
                pass

            def uninstall_hook(self) -> None:
                pass

        adapter = FullAdapter()
        assert adapter.name == "full"
        assert adapter.discover() == []


class TestAdaptersInitLazyLoading:
    def test_loguru_adapter_accessible_via_getattr(self):
        import smplkit.logging.adapters as adapters_pkg

        cls = adapters_pkg.LoguruAdapter
        assert cls.__name__ == "LoguruAdapter"

    def test_unknown_attr_raises(self):
        import smplkit.logging.adapters as adapters_pkg

        with pytest.raises(AttributeError, match="no attribute"):
            _ = adapters_pkg.NoSuchAdapter  # type: ignore[attr-defined]
