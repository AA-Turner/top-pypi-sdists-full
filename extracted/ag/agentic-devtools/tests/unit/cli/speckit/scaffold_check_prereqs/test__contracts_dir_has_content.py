"""Tests for ``_contracts_dir_has_content``."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_check_prereqs import _contracts_dir_has_content


class TestContractsDirHasContent:
    """_contracts_dir_has_content reports whether contracts/ has entries."""

    def test_missing_directory_returns_false(self, tmp_path: Path) -> None:
        assert _contracts_dir_has_content(tmp_path / "contracts") is False

    def test_empty_directory_returns_false(self, tmp_path: Path) -> None:
        contracts_dir = tmp_path / "contracts"
        contracts_dir.mkdir()

        assert _contracts_dir_has_content(contracts_dir) is False

    def test_directory_with_entries_returns_true(self, tmp_path: Path) -> None:
        contracts_dir = tmp_path / "contracts"
        contracts_dir.mkdir()
        (contracts_dir / "api.yaml").write_text("openapi: 3.0.0", encoding="utf-8")

        assert _contracts_dir_has_content(contracts_dir) is True

    def test_path_that_is_a_file_returns_false(self, tmp_path: Path) -> None:
        contracts_path = tmp_path / "contracts"
        contracts_path.write_text("not a directory", encoding="utf-8")

        assert _contracts_dir_has_content(contracts_path) is False

    def test_unreadable_directory_returns_false(self, tmp_path: Path) -> None:
        contracts_dir = tmp_path / "contracts"
        contracts_dir.mkdir()

        with patch.object(type(contracts_dir), "iterdir", side_effect=PermissionError("permission denied")):
            assert _contracts_dir_has_content(contracts_dir) is False

    def test_symlinked_entry_raises_value_error(self, tmp_path: Path) -> None:
        contracts_dir = tmp_path / "contracts"
        contracts_dir.mkdir()
        target = tmp_path / "api.yaml"
        target.write_text("openapi: 3.0.0", encoding="utf-8")
        (contracts_dir / "linked.yaml").symlink_to(target)

        with pytest.raises(ValueError, match="Refusing symlinked contracts/ entry"):
            _contracts_dir_has_content(contracts_dir)
