"""File handler tests."""

import pytest
from bacore.interactors.file_handler import delete_files, get_files_in_dir

pytestmark = pytest.mark.interactors


def test_delete_files(fixt_dir_with_files):
    deleted_files_response = delete_files(path=fixt_dir_with_files, older_than_days=0, recursive=True)
    deleted_files = [file.name for file in deleted_files_response.deleted_files]
    assert deleted_files == [
        "pyproject.toml",
        "readme.md",
        "python_src_file.py",
        "__init__.py",
    ]


def test_get_files_in_dir(fixt_dir_with_files):
    """Get files in directory."""
    files = get_files_in_dir(directory=fixt_dir_with_files, recursive=True)
    file_names = [file.name for file in files]
    assert file_names == [
        "pyproject.toml",
        "readme.md",
        "python_src_file.py",
        "__init__.py",
    ]
