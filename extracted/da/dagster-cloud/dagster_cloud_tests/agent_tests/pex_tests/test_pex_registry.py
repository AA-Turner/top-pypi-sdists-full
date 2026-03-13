import os
import subprocess
import tempfile
import threading
from pathlib import Path
from unittest import mock

import boto3
import moto
import pytest
from dagster_cloud.pex.grpc.server.registry import PexInstallationError, PexS3Registry
from dagster_cloud_cli.core.workspace import PexMetadata

BUCKET = "pex-registry-test-bucket"
PREFIX = "org-storage/test"


def file_content(filepath) -> str:
    with open(filepath, encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="module")
def s3_test_bucket():
    with moto.mock_aws():
        with mock.patch.dict(
            os.environ,
            {
                "DAGSTER_CLOUD_SERVERLESS_STORAGE_S3_BUCKET": BUCKET,
                "DAGSTER_CLOUD_SERVERLESS_STORAGE_S3_PREFIX": PREFIX,
            },
        ):
            s3 = boto3.resource("s3", region_name="us-east-1")
            s3.create_bucket(Bucket=BUCKET)
            yield s3.Bucket(BUCKET)


def test_pex_registry_with_bad_pex_files(s3_test_bucket):
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = PexS3Registry(tmpdir)

        with pytest.raises(ValueError, match="prefix"):
            registry.get_pex_executable(PexMetadata(pex_tag="invalid-tag"))

        # add some fake pex files
        for name in ["source-hash1.pex", "deps-hash2.pex", "deps-hash3.pex"]:
            s3_test_bucket.put_object(Key=f"{PREFIX}/pex/{name}", Body=name + "-content")

        with pytest.raises(PexInstallationError):
            registry.get_pex_executable(PexMetadata(pex_tag="files=source-hash1.pex"))

        # no source pex
        with pytest.raises(ValueError, match="no source"):
            registry.get_pex_executable(PexMetadata(pex_tag="files=deps-hash2.pex:deps-hash3.pex"))

        # missing file
        with pytest.raises(Exception, match="404"):
            registry.get_pex_executable(
                PexMetadata(pex_tag="files=deps-nosuchhash.pex:source-hash1.pex")
            )


def test_pex_registry_with_good_pex_files(
    sample_repos_pex_files, s3_test_bucket, venvs_root, monkeypatch
):
    with tempfile.TemporaryDirectory() as tmpdir:
        pex_root = os.path.join(tmpdir, ".pex")
        monkeypatch.setenv("PEX_ROOT", pex_root)
        registry = PexS3Registry(tmpdir)

        # add real pex files
        files = sample_repos_pex_files["repo-1"]
        for filepath in files["all"]:
            s3_test_bucket.put_object(
                Key=f"{PREFIX}/pex/{filepath.name}", Body=filepath.read_bytes()
            )

        pex_executable = registry.get_pex_executable(PexMetadata(pex_tag=files["pex_tag"]))

        # ensure it got unpacked under the venv directory
        assert pex_executable.venv_dirs
        for venv_dir in pex_executable.venv_dirs:
            assert Path(venv_dir).parent == venvs_root
        assert venvs_root in Path(pex_executable.source_path).parents

        # ensure PEX_ROOT cache got cleaned up
        assert not os.path.exists(pex_root) or not os.listdir(pex_root)

        # try to run the pex_executable
        env = {**os.environ, **pex_executable.environ}
        output = subprocess.check_output(
            [pex_executable.source_path, "-m", "dagster", "--version"],
            env=env,
            encoding="utf-8",
        )
        assert "version" in output

        output = subprocess.check_output(
            [pex_executable.source_path, "-c", "import repo_1; print(repo_1.defs);"],
            env={**os.environ, **pex_executable.environ},
            encoding="utf-8",
        )
        assert "Definitions" in output


def test_pex_registry_cleanup_files(sample_repos_pex_files, s3_test_bucket, venvs_root):
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = PexS3Registry(tmpdir)

        # pick two arbitrary repos
        repo_1_files = sample_repos_pex_files["repo-1"]
        repo_2_files = sample_repos_pex_files["repo-with-console-script"]

        # upload all pex files to mock s3
        for filepath in repo_1_files["all"] + repo_2_files["all"]:
            s3_test_bucket.put_object(
                Key=f"{PREFIX}/pex/{filepath.name}", Body=filepath.read_bytes()
            )

        pex_tag1 = repo_1_files["pex_tag"]
        # create a pex tag that re-uses the deps.pex with a new source.pex
        files2 = [filepath.name for filepath in repo_1_files["deps"] + [repo_2_files["source"]]]
        pex_tag2 = "files=" + ":".join(sorted(files2))

        # install both pex executables, should result in 3 venvs (deps venv will be shared)
        pex_executable1 = registry.get_pex_executable(PexMetadata(pex_tag=pex_tag1))
        registry.get_pex_executable(PexMetadata(pex_tag=pex_tag2))
        assert len(os.listdir(venvs_root)) == 3

        # preserve 1 executable, should preserve 2 in-use venvs
        registry.cleanup_unused_files(in_use_pex_metadatas=[PexMetadata(pex_tag=pex_tag1)])
        assert len(os.listdir(venvs_root)) == 2

        # should match the preserved executable
        assert set(os.listdir(venvs_root)) == {
            Path(path).name for path in pex_executable1.venv_dirs
        }

        # re-running cleanup should not add/remove any files
        registry.cleanup_unused_files(in_use_pex_metadatas=[PexMetadata(pex_tag=pex_tag1)])
        assert set(os.listdir(venvs_root)) == {
            Path(path).name for path in pex_executable1.venv_dirs
        }

        # reinstall a previously deleted executable (pex_tag2)
        registry.get_pex_executable(PexMetadata(pex_tag=pex_tag2))
        assert len(os.listdir(venvs_root)) == 3
        # cleanup should not delete the re-added venv
        registry.cleanup_unused_files(
            in_use_pex_metadatas=[PexMetadata(pex_tag=pex_tag1), PexMetadata(pex_tag=pex_tag2)]
        )
        assert len(os.listdir(venvs_root)) == 3

        # cleanup everything
        registry.cleanup_unused_files(in_use_pex_metadatas=[])
        assert len(os.listdir(venvs_root)) == 0

        # test concurrent cleanup and installation
        def install_loop():
            for i in range(5):
                assert registry.get_pex_executable(PexMetadata(pex_tag=pex_tag1))
                assert registry.get_pex_executable(PexMetadata(pex_tag=pex_tag2))

        def cleanup_loop():
            for i in range(1000):
                registry.cleanup_unused_files(in_use_pex_metadatas=[])

        threading.Thread(target=cleanup_loop).start()
        install_loop()


def test_pex_console_scripts(sample_repos_pex_files, s3_test_bucket, venvs_root):
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = PexS3Registry(tmpdir)
        files = sample_repos_pex_files["repo-with-console-script"]
        for filepath in files["all"]:
            s3_test_bucket.put_object(
                Key=f"{PREFIX}/pex/{filepath.name}", Body=filepath.read_bytes()
            )

        pex_executable = registry.get_pex_executable(PexMetadata(pex_tag=files["pex_tag"]))
        assert pex_executable.venv_dirs, "pex did not get unpacked into venvs"
        assert str(venvs_root) in pex_executable.environ["PATH"]

        # try to run the console script from within the pex executable context
        proc = subprocess.run(
            [
                pex_executable.source_path,
                "-c",
                "import subprocess; subprocess.run(['flask', '--version']);",
            ],
            env={**os.environ, **pex_executable.environ},
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr + proc.stdout
        assert "Flask" in proc.stdout


def test_pex_quickstart_etl(sample_repos_pex_files, s3_test_bucket, venvs_root):
    # this test runs "dagster job list" to ensure the dependencies of quickstart, such as
    # wordcloud, are available
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = PexS3Registry(tmpdir)
        files = sample_repos_pex_files["repo-quickstart-etl"]
        for filepath in files["all"]:
            s3_test_bucket.put_object(
                Key=f"{PREFIX}/pex/{filepath.name}", Body=filepath.read_bytes()
            )

        pex_executable = registry.get_pex_executable(PexMetadata(pex_tag=files["pex_tag"]))
        assert pex_executable.venv_dirs, "pex did not get unpacked into a venv"
        assert str(venvs_root) in pex_executable.environ["PATH"]

        # try to run the console script from within the pex executable context
        proc = subprocess.run(
            [
                "dagster",
                "job",
                "list",
                "--package-name",
                "quickstart_etl",
            ],
            env={**os.environ, **pex_executable.environ},
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr + proc.stdout

        ### Typical output ###
        # Job: all_assets_job
        # Ops: (Execution Order)
        #     hackernews_topstory_ids
        #     hackernews_topstories
        #     hackernews_topstories_word_cloud
        assert "Job: all_assets_job" in proc.stdout
        assert "hackernews_topstories" in [line.strip() for line in proc.stdout.splitlines()]


def test_pex_requirements_txt(sample_repos_pex_files, s3_test_bucket, venvs_root):
    # test various features of requirements.txt such as local packages and comments
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = PexS3Registry(tmpdir)
        files = sample_repos_pex_files["repo-with-requirements-txt"]
        for filepath in files["all"]:
            s3_test_bucket.put_object(
                Key=f"{PREFIX}/pex/{filepath.name}", Body=filepath.read_bytes()
            )

        pex_executable = registry.get_pex_executable(PexMetadata(pex_tag=files["pex_tag"]))
        assert pex_executable.venv_dirs, "pex did not get unpacked into a venv"
        assert str(venvs_root) in pex_executable.environ["PATH"]

        # try to import the local packages and their dependencies from within the pex executable
        proc = subprocess.run(
            [
                pex_executable.source_path,
                "-c",
                (
                    "import local_package_a, local_package_b, click,"
                    " bottle;print(local_package_a.local_package_a_msg,"
                    " local_package_b.local_package_b_msg);"
                ),
            ],
            env={**os.environ, **pex_executable.environ},
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr + proc.stdout
        assert "local_package_a" in proc.stdout
        assert "local_package_b" in proc.stdout

        # try to import a dep added using a git+https url
        proc = subprocess.run(
            [
                pex_executable.source_path,
                "-c",
                "import flask;print(flask.__version__);",
            ],
            env={**os.environ, **pex_executable.environ},
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr + proc.stdout
        assert "2.2.2" in proc.stdout


def test_pex_requirements_txt_hashes(sample_repos_pex_files, s3_test_bucket, venvs_root):
    # test various features of requirements.txt such as local packages and comments
    with tempfile.TemporaryDirectory() as tmpdir:
        registry = PexS3Registry(tmpdir)
        files = sample_repos_pex_files["repo-with-requirements-txt-hashes"]
        for filepath in files["all"]:
            s3_test_bucket.put_object(
                Key=f"{PREFIX}/pex/{filepath.name}", Body=filepath.read_bytes()
            )

        pex_executable = registry.get_pex_executable(PexMetadata(pex_tag=files["pex_tag"]))
        assert pex_executable.venv_dirs, "pex did not get unpacked into a venv"
        assert str(venvs_root) in pex_executable.environ["PATH"]

        # try to import the local packages and their dependencies from within the pex executable
        proc = subprocess.run(
            [pex_executable.source_path, "-c", "import click;"],
            env={**os.environ, **pex_executable.environ},
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr + proc.stdout
