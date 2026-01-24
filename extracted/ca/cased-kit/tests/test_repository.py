"""Tests for Repository class GitHub token environment variable pickup."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from kit.repository import Repository


class TestRepositoryGitHubTokenPickup:
    """Test Repository class automatic GitHub token pickup from environment."""

    @patch.dict(os.environ, {"KIT_GITHUB_TOKEN": "test_kit_token", "GITHUB_TOKEN": "test_github_token"})
    def test_repository_picks_up_kit_github_token(self):
        """Test that Repository picks up KIT_GITHUB_TOKEN when no token provided."""
        with patch.object(Repository, "_clone_github_repo") as mock_clone:
            mock_clone.return_value = Path("/tmp/test")
            
            repo = Repository("https://github.com/test/repo")
            
            # Should have called _clone_github_repo with KIT_GITHUB_TOKEN
            mock_clone.assert_called_once_with(
                "https://github.com/test/repo", 
                "test_kit_token",  # KIT_GITHUB_TOKEN should be used
                None, 
                None
            )

    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_github_token"}, clear=True)
    def test_repository_picks_up_github_token_fallback(self):
        """Test that Repository falls back to GITHUB_TOKEN when KIT_GITHUB_TOKEN not set."""
        with patch.object(Repository, "_clone_github_repo") as mock_clone:
            mock_clone.return_value = Path("/tmp/test")
            
            repo = Repository("https://github.com/test/repo")
            
            # Should have called _clone_github_repo with GITHUB_TOKEN
            mock_clone.assert_called_once_with(
                "https://github.com/test/repo", 
                "test_github_token",  # GITHUB_TOKEN should be used as fallback
                None, 
                None
            )

    @patch.dict(os.environ, {}, clear=True)
    def test_repository_no_token_when_env_empty(self):
        """Test that Repository passes None when no environment tokens are set."""
        with patch.object(Repository, "_clone_github_repo") as mock_clone:
            mock_clone.return_value = Path("/tmp/test")
            
            repo = Repository("https://github.com/test/repo")
            
            # Should have called _clone_github_repo with None
            mock_clone.assert_called_once_with(
                "https://github.com/test/repo", 
                None,  # No token should be passed
                None, 
                None
            )

    @patch.dict(os.environ, {"KIT_GITHUB_TOKEN": "env_token"})
    def test_repository_explicit_token_overrides_env(self):
        """Test that explicitly provided token overrides environment variables."""
        with patch.object(Repository, "_clone_github_repo") as mock_clone:
            mock_clone.return_value = Path("/tmp/test")
            
            repo = Repository("https://github.com/test/repo", github_token="explicit_token")
            
            # Should have called _clone_github_repo with explicit token
            mock_clone.assert_called_once_with(
                "https://github.com/test/repo", 
                "explicit_token",  # Explicit token should override environment
                None, 
                None
            )

    def test_repository_local_path_ignores_token(self):
        """Test that local paths don't use GitHub tokens."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch.dict(os.environ, {"KIT_GITHUB_TOKEN": "test_token"}):
                # Local paths should work fine even with tokens in env
                repo = Repository(tmpdir)
                assert str(repo.local_path) == str(Path(tmpdir).absolute())

    @patch.dict(os.environ, {"KIT_GITHUB_TOKEN": "test_token"})
    def test_repository_with_ref_passes_token(self):
        """Test that Repository passes environment token even when ref is specified."""
        with patch.object(Repository, "_clone_github_repo") as mock_clone:
            mock_clone.return_value = Path("/tmp/test")
            
            repo = Repository("https://github.com/test/repo", ref="main")
            
            # Should have called _clone_github_repo with environment token and ref
            mock_clone.assert_called_once_with(
                "https://github.com/test/repo", 
                "test_token",  # Environment token should be used
                None, 
                "main"
            )


class TestRepositoryMultiFileContent:
    """Test Repository class multi-file get_file_content functionality."""

    def test_get_single_file_content(self):
        """Test single file content retrieval (existing behavior)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / "test.py"
            test_content = "def hello():\n    print('world')\n"
            test_file.write_text(test_content)
            
            repo = Repository(tmpdir)
            
            # Single file should return string
            result = repo.get_file_content("test.py")
            assert isinstance(result, str)
            assert result == test_content

    def test_get_multiple_file_contents(self):
        """Test multiple file content retrieval (new behavior)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = Path(tmpdir) / "file1.py"
            file2 = Path(tmpdir) / "file2.py" 
            file3 = Path(tmpdir) / "file3.js"
            
            content1 = "# File 1 content\nprint('hello')\n"
            content2 = "# File 2 content\nprint('world')\n"
            content3 = "// File 3 content\nconsole.log('test');\n"
            
            file1.write_text(content1)
            file2.write_text(content2)
            file3.write_text(content3)
            
            repo = Repository(tmpdir)
            
            # Multiple files should return dict
            result = repo.get_file_content(["file1.py", "file2.py", "file3.js"])
            assert isinstance(result, dict)
            assert len(result) == 3
            assert result["file1.py"] == content1
            assert result["file2.py"] == content2
            assert result["file3.js"] == content3

    def test_get_empty_file_list(self):
        """Test getting content for empty file list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Repository(tmpdir)
            
            # Empty list should return empty dict
            result = repo.get_file_content([])
            assert isinstance(result, dict)
            assert len(result) == 0

    def test_get_single_file_not_found(self):
        """Test error handling for single missing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Repository(tmpdir)
            
            with pytest.raises(FileNotFoundError) as exc_info:
                repo.get_file_content("nonexistent.py")
            assert "File not found in repository: nonexistent.py" in str(exc_info.value)

    def test_get_multiple_files_some_missing(self):
        """Test error handling when some files in list are missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create only one of the requested files
            existing_file = Path(tmpdir) / "exists.py"
            existing_file.write_text("print('exists')")
            
            repo = Repository(tmpdir)
            
            with pytest.raises(IOError) as exc_info:
                repo.get_file_content(["exists.py", "missing1.py", "missing2.py"])
            
            error_msg = str(exc_info.value)
            assert "Files not found: missing1.py, missing2.py" in error_msg

    def test_get_multiple_files_all_missing(self):
        """Test error handling when all files are missing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Repository(tmpdir)
            
            with pytest.raises(IOError) as exc_info:
                repo.get_file_content(["missing1.py", "missing2.py"])
            
            error_msg = str(exc_info.value)
            assert "Files not found: missing1.py, missing2.py" in error_msg

    def test_get_single_file_read_error(self):
        """Test error handling for single file read errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Repository(tmpdir)
            
            # Mock file read error
            with patch.object(repo, "_get_single_file_content") as mock_read:
                mock_read.side_effect = IOError("Permission denied")
                
                with pytest.raises(IOError) as exc_info:
                    repo.get_file_content("test.py")
                assert "Permission denied" in str(exc_info.value)

    def test_get_multiple_files_mixed_errors(self):
        """Test error handling with mix of missing files and read errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create one existing file
            existing_file = Path(tmpdir) / "exists.py"
            existing_file.write_text("print('exists')")
            
            repo = Repository(tmpdir)
            
            # Mock read error for existing file
            original_method = repo._get_single_file_content
            def mock_read_single(file_path):
                if file_path == "exists.py":
                    raise IOError("Read error for exists.py")
                return original_method(file_path)
            
            with patch.object(repo, "_get_single_file_content", side_effect=mock_read_single):
                with pytest.raises(IOError) as exc_info:
                    repo.get_file_content(["exists.py", "missing.py"])
                
                error_msg = str(exc_info.value)
                assert "Files not found: missing.py" in error_msg
                assert "Read errors: exists.py" in error_msg

    def test_get_nested_file_paths(self):
        """Test getting content for files in subdirectories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested directory structure
            subdir = Path(tmpdir) / "src" / "utils"
            subdir.mkdir(parents=True)
            
            file1 = Path(tmpdir) / "main.py"
            file2 = subdir / "helper.py"
            
            content1 = "# Main file\nprint('main')"
            content2 = "# Helper file\nprint('helper')"
            
            file1.write_text(content1)
            file2.write_text(content2)
            
            repo = Repository(tmpdir)
            
            # Test both single and multiple file access with nested paths
            single_result = repo.get_file_content("src/utils/helper.py")
            assert single_result == content2
            
            multi_result = repo.get_file_content(["main.py", "src/utils/helper.py"])
            assert isinstance(multi_result, dict)
            assert multi_result["main.py"] == content1
            assert multi_result["src/utils/helper.py"] == content2

    def test_type_detection_behavior(self):
        """Test that the method correctly detects input type and returns appropriate output type."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = Path(tmpdir) / "test1.py"
            file1.write_text("content1")
            
            repo = Repository(tmpdir)
            
            # String input should return string
            str_result = repo.get_file_content("test1.py")
            assert isinstance(str_result, str)
            
            # List input should return dict  
            list_result = repo.get_file_content(["test1.py"])
            assert isinstance(list_result, dict)
            assert "test1.py" in list_result

    def test_large_file_list_performance(self):
        """Test that multiple file reading works efficiently with larger file lists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple test files
            num_files = 10
            file_paths = []
            expected_contents = {}
            
            for i in range(num_files):
                file_path = f"file_{i}.py"
                full_path = Path(tmpdir) / file_path
                content = f"# File {i} content\nprint('file {i}')\n"
                full_path.write_text(content)
                file_paths.append(file_path)
                expected_contents[file_path] = content
            
            repo = Repository(tmpdir)
            
            # Get all files at once
            result = repo.get_file_content(file_paths)
            
            assert isinstance(result, dict)
            assert len(result) == num_files
            assert result == expected_contents 