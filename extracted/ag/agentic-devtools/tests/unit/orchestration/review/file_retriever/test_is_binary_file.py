"""Tests for is_binary_file function."""

from __future__ import annotations

from agentic_devtools.orchestration.review.file_retriever import is_binary_file


class TestIsBinaryFile:
    """Tests for binary file detection."""

    def test_is_binary_field_true(self) -> None:
        """Explicit isBinary=True is detected as binary."""
        assert is_binary_file({"path": "/src/app.py", "isBinary": True}) is True

    def test_is_binary_field_false_with_text_ext(self) -> None:
        """Explicit isBinary=False is not binary (override of extension check)."""
        assert is_binary_file({"path": "/src/app.py", "isBinary": False}) is False

    def test_is_binary_false_overrides_binary_extension(self) -> None:
        """Explicit isBinary=False takes precedence; extension heuristic is skipped."""
        # .png would normally be detected as binary by extension.
        assert is_binary_file({"isBinary": False, "path": "/assets/logo.png"}) is False

    def test_binary_extension(self) -> None:
        """File with binary extension is detected as binary."""
        assert is_binary_file({"path": "/assets/logo.png"}) is True

    def test_text_extension(self) -> None:
        """File with text extension is not binary."""
        assert is_binary_file({"path": "/src/main.ts"}) is False

    def test_no_extension_not_binary(self) -> None:
        """File with no extension is not binary."""
        assert is_binary_file({"path": "/src/Makefile"}) is False

    def test_python_file_not_binary(self) -> None:
        """Python file is not binary."""
        assert is_binary_file({"path": "/src/app.py"}) is False

    def test_lock_file_not_binary(self) -> None:
        """Lock files are treated as text unless explicitly marked binary."""
        assert is_binary_file({"path": "/poetry.lock"}) is False
