import os
import shutil

from click.testing import CliRunner
from freezegun import freeze_time

from kacl.kacl_cli import cli
from tests.snapshot_directory import snapshot_directory


@freeze_time("2023-01-01")
def test_integration_workflow(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))

        # 1. add new changes to changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add",
                "-m",
                "Changed",
                "A default change without stash",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output

        # 2. Check if change is in changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "get",
                "Unreleased",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "A default change without stash" in result.output

        # 3. add new changes to changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add",
                "-m",
                "--stash",
                "Changed",
                "A STASHED change",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output

        # asser that A STASHED change is not in CHANGELOG.md
        with open(os.path.join(project_root_path, "CHANGELOG.md"), "r") as f:
            changelog_content = f.read()
            assert "A STASHED change" not in changelog_content

        # 4. Check if change is in changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "get",
                "Unreleased",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "A STASHED change" in result.output

    assert result.exit_code == 0, result.output
    snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_integration_workflow_config(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")
    config = os.path.join(resources_dir, "stash-config.yml")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        shutil.copyfile(config, os.path.join(project_root_path, ".kacl.yml"))

        # 1. add new changes to changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add",
                "-m",
                "Changed",
                "A default change without stash",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output

        # 2. Check if change is in changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "get",
                "Unreleased",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "A default change without stash" in result.output

        # 3. add new changes to changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add",
                "-m",
                "--stash",
                "Changed",
                "A STASHED change",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output

        # asser that A STASHED change is not in CHANGELOG.md
        with open(os.path.join(project_root_path, "CHANGELOG.md"), "r") as f:
            changelog_content = f.read()
            assert "A STASHED change" not in changelog_content

        # 3. add new changes to changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add",
                "-m",
                "Changed",
                "Another STASHED change",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output

        # asser that A STASHED change is not in CHANGELOG.md
        with open(os.path.join(project_root_path, "CHANGELOG.md"), "r") as f:
            changelog_content = f.read()
            assert "A STASHED change" not in changelog_content

        # 4. Check if change is in changelog
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "get",
                "Unreleased",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "A STASHED change" in result.output

    assert result.exit_code == 0, result.output
    snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_release_with_nested_stash_directory(tmp_path):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")
    config = os.path.join(resources_dir, "stash-config.yml")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))

        # stash file for a branch like "refactor/foo" written by older versions
        result = runner.invoke(
            cli,
            [
                "-c",
                config,
                "-f",
                "CHANGELOG.md",
                "add",
                "--stash",
                "-m",
                "Changed",
                "x",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        stash_dir = os.path.join(project_root_path, ".kacl_stash")
        flat = os.path.join(stash_dir, os.listdir(stash_dir)[0])
        nested_dir = os.path.join(stash_dir, "refactor")
        os.makedirs(nested_dir)
        shutil.move(flat, os.path.join(nested_dir, "foo.md"))

        result = runner.invoke(
            cli,
            ["-c", config, "-f", "CHANGELOG.md", "release", "99.0.0", "-m"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert os.listdir(stash_dir) == []


def test_non_version_link_reference_survives_release(tmp_path):
    runner = CliRunner()
    changelog = (
        "# Changelog\n\n"
        "All notable changes to this project will be documented in this file.\n\n"
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), "
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
        "## [Unreleased]\n\n"
        "### Changed\n\n"
        "- a big change ([!1234])\n\n"
        "[Unreleased]: https://gitlab.com/my/repo/-/compare/v0.9.0...HEAD\n"
        "[!1234]: https://gitlab.com/my/repo/-/merge_requests/1234\n"
    )
    with runner.isolated_filesystem(temp_dir=tmp_path):
        with open("CHANGELOG.md", "w") as f:
            f.write(changelog)
        result = runner.invoke(
            cli,
            ["-f", "CHANGELOG.md", "release", "1.0.0", "-m", "--no-commit"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        with open("CHANGELOG.md") as f:
            content = f.read()
        assert "[!1234]: https://gitlab.com/my/repo/-/merge_requests/1234" in content
