import json
import os
import platform
import tarfile
import tempfile
import zipfile
from pathlib import Path
from subprocess import run

import pytest
from connector.compile import BundleDetails, bundle_onprem, collect_package_data_files


def test_compile():
    # First, compile from the SDK and check that behavior
    tmpdirname = tempfile.mkdtemp()
    sdk_cli = "connector"

    compile_command = [
        sdk_cli,
        "compile-on-prem",
        "--app-id",
        "mock_connector",
        "--connector-root-module-dir",
        "projects/connectors/python/mock-connector/mock_connector",
        "--output-directory",
        str(tmpdirname),
    ]
    result = run(
        " ".join(compile_command),
        shell=True,
        capture_output=True,
        cwd=Path(os.path.dirname(__file__)).parent.parent.parent.parent.parent,
    )
    stdout = str(result.stdout, "utf-8")
    stderr = str(result.stderr, "utf-8")
    if result.returncode != 0:
        print("stdout:\n", stdout)
        print("stderr:\n", stderr)
        pytest.fail(f"Exited {result.returncode}: {' '.join(compile_command)}")
    archive = stdout.strip(" \n\t")
    print("archive:", archive)
    assert (
        len(archive) > 0 and len(archive.split(" ")) == 1
    ), f"The output doesn't look like a single file: '{archive}'"
    assert os.path.exists(archive), f"The output isn't a file: '{archive}'"
    with tempfile.TemporaryDirectory() as tempdir:
        if platform.system() == "Windows":
            assert archive.endswith(".zip"), "Archive isn't a zip file"
            with zipfile.ZipFile(archive) as zip:
                zip.extractall(tempdir)
            executable = str(Path(tempdir) / "main.exe")
        else:
            assert archive.endswith(".tar.gz"), "Archive isn't a tar file"
            with tarfile.open(archive) as tar:
                tar.extractall(tempdir)

            executable = str(Path(tempdir) / "main")
            assert os.access(executable, os.X_OK), f"The file isn't executable: '{archive}'"

        # Now, check the compiled connector archive
        info_command = [executable, "info"]
        result = run(
            " ".join(info_command),
            shell=True,
            capture_output=True,
        )
        assert result.returncode == 0, f"Exited {result.returncode}: {' '.join(info_command)}"
        try:
            info_json = json.loads(str(result.stdout, "utf-8"))
        except json.JSONDecodeError:
            pytest.fail("Non JSON emitted from compiled connector")
        assert "response" in info_json, "Unexpected JSON structure from compiled connector"
        assert (
            "version" in info_json["response"]
        ), "Unexpected JSON structure from compiled connector"


def test_compile_collects_package_data():
    """package-data declared in pyproject.toml is bundled automatically, without
    needing an explicit --data-file, at its package-relative destination."""
    tmpdirname = tempfile.mkdtemp()
    sdk_cli = "connector"

    compile_command = [
        sdk_cli,
        "compile-on-prem",
        "--app-id",
        "mock_connector",
        "--connector-root-module-dir",
        "projects/connectors/python/mock-connector/mock_connector",
        "--output-directory",
        str(tmpdirname),
    ]
    result = run(
        " ".join(compile_command),
        shell=True,
        capture_output=True,
        cwd=Path(os.path.dirname(__file__)).parent.parent.parent.parent.parent,
    )
    stdout = str(result.stdout, "utf-8")
    stderr = str(result.stderr, "utf-8")
    if result.returncode != 0:
        print("stdout:\n", stdout)
        print("stderr:\n", stderr)
        pytest.fail(f"Exited {result.returncode}: {' '.join(compile_command)}")
    archive = stdout.strip(" \n\t")
    assert os.path.exists(archive), f"The output isn't a file: '{archive}'"

    with tempfile.TemporaryDirectory() as tempdir:
        if platform.system() == "Windows":
            with zipfile.ZipFile(archive) as zip:
                zip.extractall(tempdir)
        else:
            with tarfile.open(archive) as tar:
                tar.extractall(tempdir)

        # package-data is placed package-relative: _internal/mock_connector/...
        data_file_path = (
            Path(tempdir) / "_internal" / "mock_connector" / "test_data" / "test_data.txt"
        )
        assert (
            data_file_path.exists()
        ), f"Package-data file not found in compiled archive: {data_file_path}"
        assert "test data file" in data_file_path.read_text().lower()


def test_collect_package_data_files(tmp_path):
    """collect_package_data_files resolves package-data globs to package-relative
    destinations and skips unsupported wildcard keys."""
    package_dir = tmp_path / "my_pkg"
    (package_dir / "WSDL").mkdir(parents=True)
    (package_dir / "instructions").mkdir()
    (package_dir / "service.wsdl").write_text("top-level wsdl")
    (package_dir / "WSDL" / "schema.wsdl").write_text("nested wsdl")
    (package_dir / "instructions" / "auth.md").write_text("# auth")

    (tmp_path / "pyproject.toml").write_text(
        "[tool.setuptools.package-data]\n"
        'my_pkg = ["*.wsdl", "WSDL/*.wsdl", "instructions/*.md"]\n'
        '"*" = ["ignored/*.txt"]\n'
    )

    result = collect_package_data_files(tmp_path)
    dest_by_name = {src.name: dest for src, dest in result}

    assert dest_by_name == {
        "service.wsdl": "my_pkg",
        "schema.wsdl": "my_pkg/WSDL",
        "auth.md": "my_pkg/instructions",
    }
    # Sources are absolute and exist
    for src, _ in result:
        assert src.is_absolute() and src.is_file()


def test_collect_package_data_files_no_pyproject(tmp_path):
    """Returns empty when there is no pyproject.toml or no package-data table."""
    assert collect_package_data_files(tmp_path) == []
    (tmp_path / "pyproject.toml").write_text("[project]\nname = 'x'\n")
    assert collect_package_data_files(tmp_path) == []


@pytest.mark.skipif(
    platform.system() == "Windows",
    reason="chmod/tar permission handling only applies to the non-Windows bundle path",
)
def test_bundle_onprem_sets_permissions_recursively(tmp_path):
    """Every archived member is written with mode 0o770, including nested files and
    files whose names contain spaces.

    Regression test for INTPLAT-2409: the packaging flow must set permissions across
    the whole tree before archiving. tar.add() recurses into directories, so a nested
    file gets written to the archive when its parent directory is added; if it hasn't
    been chmod'd yet it lands in the tarball with its original mode. A file name with a
    space also previously broke the shell-based `chmod` this replaced.
    """
    compiled_root = tmp_path / "dist" / "main"
    nested = compiled_root / "_internal" / "jaraco" / "text"
    nested.mkdir(parents=True)
    (compiled_root / "main").write_text("#!/bin/sh\n")
    (nested / "Lorem ipsum.txt").write_text("lorem")

    # Start from modes other than 0o770 so the assertion is meaningful.
    for path in compiled_root.rglob("*"):
        path.chmod(0o755 if path.is_dir() else 0o644)

    archive = bundle_onprem(
        BundleDetails(
            source_root_directory=tmp_path,
            compiled_root_directory=compiled_root,
            bundle_directory=tmp_path / "bundled",
            version="1.2.3",
            app_id="mock_connector",
        )
    )

    assert archive.exists() and archive.name.endswith(".tar.gz")

    with tarfile.open(archive) as tar:
        members = tar.getmembers()

    names = {m.name for m in members}
    # The file whose name contains a space made it into the archive intact.
    assert "_internal/jaraco/text/Lorem ipsum.txt" in names

    # Every compiled member is 0o770, including those added via directory recursion.
    # metadata.toml is added separately and isn't governed by the chmod pass.
    bad = {
        m.name: oct(m.mode)
        for m in members
        if m.name != "metadata.toml" and (m.mode & 0o777) != 0o770
    }
    assert not bad, f"archive members with unexpected mode: {bad}"
