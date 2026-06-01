import pytest

from mistralai.workflows.core.sandbox import (
    _BASE_PASSTHROUGH_MODULES,
    _EXCLUDED_PREFIXES,
    _discover_workflow_modules,
)


class TestDiscoverWorkflowModules:
    @pytest.fixture(scope="class")
    def discovered(self) -> tuple[str, ...]:
        return _discover_workflow_modules()

    def test_returns_tuple_of_strings(self, discovered: tuple[str, ...]) -> None:
        assert isinstance(discovered, tuple)
        assert all(isinstance(m, str) for m in discovered)

    def test_includes_base_passthrough_modules(self, discovered: tuple[str, ...]) -> None:
        for mod in _BASE_PASSTHROUGH_MODULES:
            assert mod in discovered

    def test_includes_core_workflow_modules(self, discovered: tuple[str, ...]) -> None:
        assert any(m.startswith("mistralai.workflows.core.") for m in discovered)

    @pytest.mark.parametrize("excluded", _EXCLUDED_PREFIXES)
    def test_excludes_prefix(self, discovered: tuple[str, ...], excluded: str) -> None:
        matching = [m for m in discovered if m == excluded or m.startswith(excluded + ".")]
        assert matching == [], f"Excluded prefix {excluded!r} found in: {matching}"

    def test_no_examples_anywhere(self, discovered: tuple[str, ...]) -> None:
        examples = [m for m in discovered if ".examples" in m]
        assert examples == [], f"Example modules leaked into passthrough: {examples}"
