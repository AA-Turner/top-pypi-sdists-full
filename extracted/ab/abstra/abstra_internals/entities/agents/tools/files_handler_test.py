import shutil
import tempfile
from pathlib import Path

import pytest

from abstra_internals.entities.agents.tools.files_handler import (
    FilesListHandler,
    FilesReadHandler,
    FilesWriteHandler,
    _is_glob_allowed,
    _safe_path,
)


class TestSafePath:
    def setup_method(self):
        self.base = Path(tempfile.mkdtemp()).resolve()

    def teardown_method(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_normal_relative_path(self):
        result = _safe_path(self.base, "subdir/file.txt")
        assert str(result).startswith(str(self.base.resolve()))
        assert result == (self.base / "subdir" / "file.txt").resolve()

    def test_path_traversal_raises(self):
        with pytest.raises(ValueError, match="Path traversal not allowed"):
            _safe_path(self.base, "../../etc/passwd")

    def test_dot_path(self):
        result = _safe_path(self.base, ".")
        assert result == self.base.resolve()

    def test_simple_filename(self):
        result = _safe_path(self.base, "readme.txt")
        assert result == (self.base / "readme.txt").resolve()


class TestIsGlobAllowed:
    def test_empty_pattern_allows_all(self):
        assert _is_glob_allowed("anything.txt", "") is True

    def test_matching_pattern(self):
        assert _is_glob_allowed("report.csv", "*.csv") is True

    def test_non_matching_pattern(self):
        assert _is_glob_allowed("report.csv", "*.txt") is False

    def test_wildcard_pattern(self):
        assert _is_glob_allowed("data/file.json", "data/*") is True

    def test_nested_path_with_glob(self):
        # fnmatch's * matches everything including /, so *.py matches a/b/c.py
        assert _is_glob_allowed("a/b/c.py", "*.py") is True
        assert _is_glob_allowed("a/b/c.py", "a/b/*.py") is True
        assert _is_glob_allowed("a/b/c.py", "*.txt") is False


class TestFilesReadHandler:
    def setup_method(self):
        self.base = Path(tempfile.mkdtemp()).resolve()

    def teardown_method(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_read_existing_file(self):
        test_file = self.base / "hello.txt"
        test_file.write_text("Hello, World!", encoding="utf-8")

        handler = FilesReadHandler(base_dir=self.base)
        result = handler.execute({"path": "hello.txt"})
        assert result == "Hello, World!"

    def test_read_missing_file(self):
        handler = FilesReadHandler(base_dir=self.base)
        result = handler.execute({"path": "nonexistent.txt"})
        assert "Error" in result
        assert "not found" in result

    def test_read_empty_path(self):
        handler = FilesReadHandler(base_dir=self.base)
        result = handler.execute({"path": ""})
        assert "Error" in result

    def test_read_path_traversal_returns_error(self):
        handler = FilesReadHandler(base_dir=self.base)
        result = handler.execute({"path": "../../etc/passwd"})
        assert "Error" in result
        assert "traversal" in result.lower()

    def test_read_glob_blocks_disallowed_path(self):
        test_file = self.base / "secret.log"
        test_file.write_text("secret data", encoding="utf-8")

        handler = FilesReadHandler(base_dir=self.base, glob_pattern="*.txt")
        result = handler.execute({"path": "secret.log"})
        assert "Error" in result
        assert "not allowed" in result

    def test_name_and_description(self):
        handler = FilesReadHandler(base_dir=self.base)
        assert handler.name == "files_read"
        assert isinstance(handler.description, str)
        assert len(handler.description) > 0

    def test_input_schema(self):
        handler = FilesReadHandler(base_dir=self.base)
        schema = handler.input_schema
        assert schema["type"] == "object"
        assert "path" in schema["properties"]
        assert "path" in schema["required"]


class TestFilesWriteHandler:
    def setup_method(self):
        self.base = Path(tempfile.mkdtemp()).resolve()

    def teardown_method(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_write_new_file(self):
        handler = FilesWriteHandler(base_dir=self.base)
        result = handler.execute({"path": "output.txt", "content": "test content"})
        assert "File written" in result

        written = (self.base / "output.txt").read_text(encoding="utf-8")
        assert written == "test content"

    def test_write_creates_parent_dirs(self):
        handler = FilesWriteHandler(base_dir=self.base)
        result = handler.execute({"path": "sub/dir/file.txt", "content": "nested"})
        assert "File written" in result
        assert (self.base / "sub" / "dir" / "file.txt").exists()

    def test_write_empty_path_returns_error(self):
        handler = FilesWriteHandler(base_dir=self.base)
        result = handler.execute({"path": "", "content": "x"})
        assert "Error" in result

    def test_write_path_traversal_returns_error(self):
        handler = FilesWriteHandler(base_dir=self.base)
        result = handler.execute({"path": "../../evil.txt", "content": "x"})
        assert "Error" in result

    def test_write_glob_blocks_disallowed_path(self):
        handler = FilesWriteHandler(base_dir=self.base, glob_pattern="*.csv")
        result = handler.execute({"path": "data.json", "content": "{}"})
        assert "Error" in result
        assert "not allowed" in result


class TestFilesListHandler:
    def setup_method(self):
        self.base = Path(tempfile.mkdtemp()).resolve()

    def teardown_method(self):
        shutil.rmtree(self.base, ignore_errors=True)

    def test_list_files_in_directory(self):
        (self.base / "a.txt").write_text("aaa", encoding="utf-8")
        (self.base / "b.txt").write_text("bbb", encoding="utf-8")

        handler = FilesListHandler(base_dir=self.base)
        result = handler.execute({"path": "."})
        assert "a.txt" in result
        assert "b.txt" in result

    def test_list_empty_directory(self):
        handler = FilesListHandler(base_dir=self.base)
        result = handler.execute({"path": "."})
        assert "empty" in result.lower()

    def test_list_nonexistent_directory(self):
        handler = FilesListHandler(base_dir=self.base)
        result = handler.execute({"path": "nope"})
        assert "Error" in result
        assert "not found" in result

    def test_list_shows_dirs_and_files(self):
        subdir = self.base / "subdir"
        subdir.mkdir()
        (self.base / "file.txt").write_text("x", encoding="utf-8")

        handler = FilesListHandler(base_dir=self.base)
        result = handler.execute({"path": "."})
        assert "dir" in result
        assert "file" in result

    def test_list_with_glob_filter(self):
        (self.base / "ok.csv").write_text("data", encoding="utf-8")
        (self.base / "skip.txt").write_text("data", encoding="utf-8")

        handler = FilesListHandler(base_dir=self.base, glob_pattern="*.csv")
        result = handler.execute({"path": "."})
        assert "ok.csv" in result
        assert "skip.txt" not in result
