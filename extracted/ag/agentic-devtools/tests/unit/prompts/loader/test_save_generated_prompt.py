"""
Tests for prompt template loader.
"""

from unittest.mock import patch

import pytest

from agentic_devtools.prompts import loader


class TestSaveGeneratedPrompt:
    """Tests for save_generated_prompt function."""

    def test_save_generated_prompt(self, temp_output_dir):
        """Test saving a generated prompt."""
        prompt_content = "# Generated Prompt\n\nThis is content."
        filepath = loader.save_generated_prompt("test", "initiate", prompt_content)

        assert filepath.exists()
        assert filepath.read_text(encoding="utf-8") == prompt_content
        assert filepath.name == "temp-test-initiate-prompt.md"

    def test_save_creates_directory(self, tmp_path):
        """Test that save creates output directory if needed."""
        output_dir = tmp_path / "new_dir" / "nested"
        with patch.object(loader, "get_temp_output_dir", return_value=output_dir):
            filepath = loader.save_generated_prompt("test", "step", "content")
            assert filepath.parent.exists()

    def test_refuses_symlink_output_path(self, tmp_path):
        """Test save rejects a symlink output path instead of writing through it."""
        output_dir = tmp_path / "state"
        output_dir.mkdir()
        output_path = output_dir / "temp-test-initiate-prompt.md"
        target_file = tmp_path / "sensitive.md"
        target_file.write_text("do-not-overwrite", encoding="utf-8")
        output_path.symlink_to(target_file)

        with patch.object(loader, "get_temp_output_dir", return_value=output_dir):
            with patch("agentic_devtools.prompts.loader.NamedTemporaryFile") as mock_tmp:
                with pytest.raises(OSError, match="symlink"):
                    loader.save_generated_prompt("test", "initiate", "new-content")

        assert target_file.read_text(encoding="utf-8") == "do-not-overwrite"
        mock_tmp.assert_not_called()

    def test_refuses_non_file_output_path(self, tmp_path):
        """Test save rejects an existing output path that is not a regular file."""
        output_dir = tmp_path / "state"
        output_dir.mkdir()
        (output_dir / "temp-test-initiate-prompt.md").mkdir()

        with patch.object(loader, "get_temp_output_dir", return_value=output_dir):
            with patch("agentic_devtools.prompts.loader.NamedTemporaryFile") as mock_tmp:
                with pytest.raises(OSError, match="non-file"):
                    loader.save_generated_prompt("test", "initiate", "new-content")

        mock_tmp.assert_not_called()

    def test_save_cleans_up_when_temp_file_creation_fails(self, tmp_path):
        """Test temp-file creation failure raises and leaves no temp-path cleanup attempt."""
        output_dir = tmp_path / "state"
        output_dir.mkdir()

        with patch.object(loader, "get_temp_output_dir", return_value=output_dir):
            with patch("agentic_devtools.prompts.loader.NamedTemporaryFile", side_effect=OSError("disk full")):
                with pytest.raises(OSError, match="disk full"):
                    loader.save_generated_prompt("test", "initiate", "new-content")

    def test_save_cleans_up_temp_file_when_write_fails(self, tmp_path):
        """Test write failure removes the created temporary file."""
        output_dir = tmp_path / "state"
        output_dir.mkdir()

        class _FailingTempFile:
            def __init__(self, directory):
                self.name = str(directory / ".temp-test-initiate-prompt.md.write-fail.tmp")
                self._file = open(self.name, "w", encoding="utf-8")

            def write(self, _content):
                raise OSError("write failed")

            def __enter__(self):
                return self

            def __exit__(self, _exc_type, _exc, _tb):
                self._file.close()
                return False

        def _named_temp_file(**_kwargs):
            return _FailingTempFile(output_dir)

        with patch.object(loader, "get_temp_output_dir", return_value=output_dir):
            with patch("agentic_devtools.prompts.loader.NamedTemporaryFile", side_effect=_named_temp_file):
                with pytest.raises(OSError, match="write failed"):
                    loader.save_generated_prompt("test", "initiate", "new-content")

        assert not any(output_dir.glob("*.tmp"))
