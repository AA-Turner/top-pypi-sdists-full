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
