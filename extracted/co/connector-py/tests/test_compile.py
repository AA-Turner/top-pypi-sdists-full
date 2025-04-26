import json
import os
import platform
import tarfile
import tempfile
import zipfile
from pathlib import Path
from subprocess import run

import pytest


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
