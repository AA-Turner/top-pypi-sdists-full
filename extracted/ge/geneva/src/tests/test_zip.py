# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# tests for the zip packager

import logging
import os
import re
import site
import subprocess
import sys
import uuid
import zipfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from lance.file import LanceFileSession

import geneva
from geneva.packager.autodetect import package_local_env_into_zips, upload_local_env
from geneva.packager.zip import WorkspaceUnzipper, WorkspaceZipper

_MODULE_TEMPLATE = "print({})"

_LOG = logging.getLogger(__name__)


def _write_and_register_module(path: Path, content: str) -> None:
    with (path / "_geneva_zip_test.py").open("w") as f:
        f.write(content)
    site.addsitedir(path.as_posix())


def test_subprocess_can_not_import_without_zip_packaging(tmp_path: Path) -> None:
    uid = uuid.uuid4().hex
    _write_and_register_module(tmp_path, _MODULE_TEMPLATE.format(f'"{uid}"'))
    p = subprocess.Popen(
        "python -c 'import _geneva_zip_test'",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p.wait()
    stderr = p.stderr.read().decode()
    stdout = p.stdout.read().decode()
    assert p.returncode != 0

    assert stdout == ""
    assert any(
        re.compile(r"ModuleNotFoundError").match(line) for line in stderr.splitlines()
    )


def test_subprocess_can_import_with_zip_packaging(tmp_path: Path) -> None:
    uid = uuid.uuid4().hex
    _write_and_register_module(tmp_path, _MODULE_TEMPLATE.format(f'"{uid}"'))
    zipper = WorkspaceZipper(tmp_path, tmp_path)
    zip_path, _ = zipper.zip()

    content = f"""
from geneva.packager.zip import WorkspaceUnzipper
from pathlib import Path

unzipper = WorkspaceUnzipper()

unzipper.unzip(Path("{zip_path[0]}"))

import _geneva_zip_test
    """.strip()

    p = subprocess.Popen(
        f"python -c '{content}'",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    p.wait()
    stderr = p.stderr.read().decode()
    stdout = p.stdout.read().decode()
    assert p.returncode == 0, f"stdout: {stdout}, stderr: {stderr}"

    assert stderr == ""
    assert stdout == f"{uid}\n"


def test_can_import_and_create_unzipper() -> None:
    WorkspaceUnzipper()


def test_download_and_extract_uses_lance_file_session_without_namespace(
    tmp_path: Path,
) -> None:
    table_base = tmp_path / "manifest_table"
    table_base.mkdir()
    local_zip = tmp_path / "payload.zip"
    with zipfile.ZipFile(local_zip, "w") as zf:
        zf.writestr("pkg/mod.py", "VALUE = 1\n")

    LanceFileSession(str(table_base)).upload_file(
        str(local_zip),
        "_geneva_uploads/payload.zip",
    )

    output_dir = tmp_path / "out"
    output_dir.mkdir()
    geneva._download_and_extract(
        {
            "src_path": f"{table_base}/_geneva_uploads/payload.zip",
            "download_path": tmp_path / "download.zip",
            "output_dir": output_dir,
        }
    )

    assert (output_dir / "pkg" / "mod.py").read_text() == "VALUE = 1\n"


@pytest.mark.slow
def test_package_local_env_into_zips(tmp_path: Path) -> None:
    # two calls to package_local_env_into_zips.
    # both should get a full list, despite excludes.
    paths = package_local_env_into_zips(tmp_path, create_zips=False)

    _LOG.info("Paths detected: %s", paths)
    assert len(paths) > 0, "No paths were detected to package"
    assert all(isinstance(p, list) for p in paths), (
        "All paths should be lists of zip files"
    )

    flatten = [i for sublist in paths for i in sublist]
    assert all(isinstance(p, Path) for p in flatten), (
        "All paths should be lists of Path objects"
    )

    # though we exclude, we should get the list back
    no_paths = package_local_env_into_zips(
        tmp_path, create_zips=False, exclude_files=flatten
    )
    _LOG.info("Paths detected: %s", paths)
    flatten2 = [i for sublist in no_paths for i in sublist]
    assert len(paths) > 0, "No paths were detected to package"
    assert all(isinstance(p, Path) for p in flatten2), (
        "All paths should be lists of Path objects"
    )


@pytest.mark.slow
def test_upload_local_env(tmp_path: Path) -> None:
    mock_uploader = MagicMock()
    mock_uploader.upload_dir = "/mock/upload/dir"
    # _file_exists returns False so files are always "uploaded"
    mock_uploader._file_exists.return_value = False
    # upload returns a predictable URI
    mock_uploader.upload.side_effect = lambda path: f"mock://{path.name}"

    with upload_local_env(zip_output_dir=tmp_path, uploader=mock_uploader) as result:
        # Flatten the result (list of lists)
        flat_result = [item for sublist in result for item in sublist]
        # All returned URIs should be from our mock
        for uri in flat_result:
            assert isinstance(uri, str)
            assert uri.startswith("mock://")
        # Ensure upload was called at least once
        assert mock_uploader.upload.called


# this is unix specific
def test_zipper_non_files(tmp_path: Path) -> None:
    # add tmp tmp_path to sys.path so WorkspaceZipper can validate it
    uid = uuid.uuid4().hex
    _write_and_register_module(tmp_path, _MODULE_TEMPLATE.format(f'"{uid}"'))

    # Test that the zipper skips non-file entries
    (tmp_path / "test_dir").mkdir()
    (tmp_path / "test_dir" / "file.txt").write_text("This is a test file.")
    (tmp_path / "test_dir" / "link").symlink_to("file.txt")
    (tmp_path / "test_dir" / "link-bad").symlink_to("file-fake.txt")  # bad symlink
    os.mkfifo(tmp_path / "test_dir" / "pipe")
    (tmp_path / "empty_dir").mkdir()

    zipper = WorkspaceZipper(tmp_path, tmp_path)
    zip_path, _ = zipper.zip()

    assert len(zip_path) > 0, "No zip files were created"
    assert all(p.is_file() for p in zip_path), "All paths should be files"

    # should be single file, verify that it only has the expected files
    with zip_path[0].open("rb") as f:
        content = f.read()
        assert b"empty_dir" not in content, "empty_dir should not be in the zip"
        assert b"file.txt" in content, "file.txt should be in the zip"
        assert b"link" in content, "good symlink should be in the zip"
        assert b"link-bad" not in content, "bad symlink should not be in the zip"
        assert b"pipe" not in content, "pipe should not be in the zip"


def test_zipper_default_output_dir_excluded_from_rescan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # zips produced in the default .geneva output dir must not feed back
    # into the next scan's checksum/content
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "module.py").write_text("VALUE = 1\n")
    monkeypatch.chdir(workspace)

    zipper = WorkspaceZipper(workspace)
    checksum_before, _, files_before = zipper.checksum()

    zip_paths, zip_checksum = zipper.zip()
    assert zip_paths[0].parent == workspace / ".geneva"
    assert zip_checksum == checksum_before

    checksum_after, _, files_after = zipper.checksum()
    assert checksum_after == checksum_before
    assert files_after == files_before


def test_zipper_output_dir_same_as_path_excluded_from_rescan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # when output_dir is the workspace itself, the produced zips must
    # still be excluded from the next scan
    (tmp_path / "module.py").write_text("VALUE = 1\n")
    monkeypatch.chdir(tmp_path)

    zipper = WorkspaceZipper(tmp_path, tmp_path)
    checksum_before, _, _ = zipper.checksum()

    zip_paths, _ = zipper.zip()
    assert zip_paths[0].parent == tmp_path

    checksum_after, _, files_after = zipper.checksum()
    assert checksum_after == checksum_before
    assert all(not name.endswith(".zip") for name, _ in files_after)


def test_allows_dir_under_parent_of_zip_on_syspath(tmp_path, monkeypatch) -> None:
    # Layout:
    #   tmp_path/
    #     app_code.zip         <-- on sys.path
    #     src/                 <-- we want to zip this
    app_root = tmp_path
    src_dir = app_root / "src"
    src_dir.mkdir()
    (src_dir / "__init__.py").write_text("# test file\n")

    zip_path = app_root / "app_code.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("pkg/__init__.py", "# inside zip\n")

    # Make CWD different from src_dir so the 'value == cwd' fast-path doesn't trigger
    workdir = app_root / "work"
    workdir.mkdir()
    monkeypatch.chdir(workdir)

    # Put the archive on sys.path as many deployments do
    monkeypatch.setattr(sys, "path", [str(zip_path)] + sys.path)

    # accept directories under the parent of a zip on sys.path.  Must NOT raise
    WorkspaceZipper(path=src_dir, output_dir=tmp_path / "output")
