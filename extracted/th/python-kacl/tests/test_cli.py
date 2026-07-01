import json
import os
import shutil

import pytest
from click.testing import CliRunner
from freezegun import freeze_time

from kacl.kacl_cli import cli
from tests.snapshot_directory import snapshot_directory


def test_verify():
    runner = CliRunner()
    result = runner.invoke(cli, ["-f", "tests/data/CHANGELOG.md", "verify"])
    assert result.exit_code == 0
    assert result.output == "Success\n"

    result = runner.invoke(cli, ["-f", "tests/data/CHANGELOG_invalid.md", "verify"])
    assert result.exit_code == 11  # spawns 11 errors


def test_verify_invalid_duplicates():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["-f", "tests/data/CHANGELOG_invalid_duplicates.md", "verify"]
    )
    assert result.exit_code == 2


def test_verify_with_json_output():
    runner = CliRunner()
    result = runner.invoke(
        cli, ["-f", "tests/data/CHANGELOG_invalid.md", "verify", "--json"]
    )
    validation_result = json.loads(result.output)

    assert len(validation_result["errors"]) == 11
    assert validation_result["valid"] is False


def test_current(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(
            cli,
            [
                "-f",
                changelog_file,
                "current",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert result.output == "1.0.0\n"


def test_next(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(
            cli,
            ["-f", changelog_file, "next", "patch"],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert result.output == "1.0.1\n"


@pytest.mark.parametrize(
    "stash_dir",
    [
        (None, True),
        ("stash", True),
        ("stash-no-changes", True),
        ("stash-invalid", False),
    ],
)
@freeze_time("2023-01-01")
def test_release_patch(tmp_path, snapshot, stash_dir):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    if stash_dir[0]:
        stash_dir_local = os.path.join(resources_dir, stash_dir[0])

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        if stash_dir[0]:
            shutil.copytree(
                stash_dir_local, os.path.join(project_root_path, ".kacl_stash")
            )

        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "release",
                "patch",
                "-m",
            ],
            catch_exceptions=False,
        )

        if not stash_dir[1]:
            assert result.exit_code == 1, result.output
        else:
            assert result.exit_code == 0, result.output
            snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_post_bump(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                "CHANGELOG.md",
                "release",
                "post",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_post_manual(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                "CHANGELOG.md",
                "release",
                "2.0.0-hotfix.0",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_post_manual_fail(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                "CHANGELOG.md",
                "release",
                "0.5.0-hotfix.0",
                "-m",
            ],
            catch_exceptions=True,
        )
        assert result.exit_code == 1, result.output


@freeze_time("2023-01-01")
def test_release_version_manual_fail_same_base_after_post(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_post_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                "CHANGELOG.md",
                "release",
                "1.0.0",
                "-m",
            ],
            catch_exceptions=True,
        )
        assert result.exit_code == 1, result.output


@freeze_time("2023-01-01")
def test_release_post_manual_same_base(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                "CHANGELOG.md",
                "release",
                "1.0.0-post.0",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output


@freeze_time("2023-01-01")
def test_release_minor(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "release",
                "minor",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_major(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "release",
                "major",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_major_no_unreleased(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "no-unreleased-config.yml"),
                "-f",
                "CHANGELOG.md",
                "release",
                "major",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_custom(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "release",
                "2.1.1",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_no_change(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_without_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "release",
                "2.1.1",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 1, result.output

        result = runner.invoke(
            cli,
            ["-f", "CHANGELOG.md", "release", "2.1.1", "-m"],
            catch_exceptions=False,
        )
        assert result.exit_code == 1, result.output


@freeze_time("2023-01-01")
def test_add_change_security(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add",
                "Security",
                "Important Security Change",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_add_change_security_stashed(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add",
                "Security",
                "[STASHED] Important Security Change",
                "-m",
                "--stash",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_config(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")

    result = runner.invoke(
        cli,
        [
            "-c",
            os.path.join(resources_dir, "config.yml"),
            "-f",
            "CHANGELOG.md",
            "verify",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code != 0, result.output


@freeze_time("2023-01-01")
def test_squash(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_keepachangelog.com.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "squash",
                "--from-version",
                "0.0.1",
                "--to-version",
                "0.3.0",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_squash_current(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_keepachangelog.com.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "squash",
                "--from-version",
                "0.0.1",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@pytest.mark.skip(reason="No issue tracker openly available, test locally.")
def test_add_comments(tmp_path):
    runner = CliRunner()
    root_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
    )
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_issue_management.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        shutil.copytree(
            os.path.join(root_dir, ".git"), os.path.join(project_root_path, ".git")
        )
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "add-comments",
                "1.0.0",
                "--jira-username",
                os.getenv("JIRA_USERNAME"),
                "--jira-password",
                os.getenv("JIRA_PASSWORD"),
                "--jira-host",
                os.getenv("JIRA_HOST"),
                "--jira-issue-pattern",
                "JIRA-[0-9]+",
                "--jira-issue-pattern",
                "MYJIRA-[0-9]+",
                "--jira-issue-pattern",
                "[A-Z]+-[0-9]+",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output


@freeze_time("2023-01-01")
def test_get_no_link_available(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_missing_link.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                changelog_file,
                "get",
                "2.0.0",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        with open(os.path.join(project_root_path, "output.md"), "w") as file:
            file.write(result.output)
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_get_link_available(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_missing_link.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                changelog_file,
                "get",
                "1.0.0",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        with open(os.path.join(project_root_path, "output.md"), "w") as file:
            file.write(result.output)
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_get_suppress_available_link(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_missing_link.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                changelog_file,
                "get",
                "--no-link",
                "1.0.0",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        with open(os.path.join(project_root_path, "output.md"), "w") as file:
            file.write(result.output)
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_get_suppress_header(tmp_path, snapshot):
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_missing_link.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                changelog_file,
                "get",
                "--no-header",
                "1.0.0",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        with open(os.path.join(project_root_path, "output.md"), "w") as file:
            file.write(result.output)
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_stash_no_pre_existing(tmp_path, snapshot):
    """Test stashing when there is no pre-existing stash file."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "stash",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "Success: Unreleased changes have been moved to" in result.output
        assert "Success: Changelog file CHANGELOG.md has been updated" in result.output

        # Verify stash directory and file were created
        stash_dir = os.path.join(project_root_path, ".kacl_stash")
        assert os.path.exists(stash_dir)
        assert len(os.listdir(stash_dir)) == 1

        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_stash_with_pre_existing(tmp_path, snapshot):
    """Test stashing when there is a pre-existing stash file with changes."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")
    stash_dir_source = os.path.join(resources_dir, "stash")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        # Copy pre-existing stash directory
        shutil.copytree(
            stash_dir_source, os.path.join(project_root_path, ".kacl_stash")
        )

        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "stash",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "Success: Unreleased changes have been moved to" in result.output
        assert "Success: Changelog file CHANGELOG.md has been updated" in result.output

        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_stash_with_link(tmp_path, snapshot):
    """Test stashing when there is a pre-existing stash file with changes."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes_and_link.md")
    stash_dir_source = os.path.join(resources_dir, "stash")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        # Copy pre-existing stash directory
        shutil.copytree(
            stash_dir_source, os.path.join(project_root_path, ".kacl_stash")
        )

        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                "CHANGELOG.md",
                "stash",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "Success: Unreleased changes have been moved to" in result.output
        assert "Success: Changelog file CHANGELOG.md has been updated" in result.output

        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_stash_no_changes(tmp_path, snapshot):
    """Test stashing when there are no unreleased changes."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_without_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "stash",
                "-m",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "Info: No unreleased changes to stash" in result.output

        # Verify no stash directory was created
        stash_dir = os.path.join(project_root_path, ".kacl_stash")
        assert not os.path.exists(stash_dir)


@freeze_time("2023-01-01")
def test_stash_without_modify(tmp_path, snapshot):
    """Test stash command without --modify flag (dry run)."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-f",
                "CHANGELOG.md",
                "stash",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output
        assert "Success: Unreleased changes have been moved to" in result.output
        # Should output the modified changelog content
        assert "## Unreleased" in result.output
        assert "## 1.0.0" in result.output

        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


@freeze_time("2023-01-01")
def test_release_no_unreleased_with_link_generation(tmp_path, snapshot):
    """Test that release with add_unreleased=False and auto-link generates correct links."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        shutil.copyfile(changelog_file, os.path.join(project_root_path, "CHANGELOG.md"))
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "no-unreleased-config.yml"),
                "-f",
                "CHANGELOG.md",
                "release",
                "2.0.0",
                "-m",
                "-g",  # --auto-link
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output

        # Read the updated changelog
        with open(os.path.join(project_root_path, "CHANGELOG.md"), "r") as f:
            content = f.read()

        # Verify no Unreleased section exists
        assert "## Unreleased" not in content or content.index(
            "## 2.0.0"
        ) < content.index("## Unreleased")

        # Verify the new version has a link reference
        assert "[2.0.0]:" in content

        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_get_no_header_with_no_link(tmp_path, snapshot):
    """Test combining --no-header and --no-link flags."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_missing_link.md")

    with runner.isolated_filesystem(temp_dir=tmp_path) as project_root_path:
        result = runner.invoke(
            cli,
            [
                "-c",
                os.path.join(resources_dir, "extension-config.yml"),
                "-f",
                changelog_file,
                "get",
                "--no-header",
                "--no-link",
                "1.0.0",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == 0, result.output

        # Verify no version header
        assert "## 1.0.0" not in result.output
        assert "## [1.0.0]" not in result.output

        # Verify no link reference
        assert "[1.0.0]:" not in result.output

        # Verify sections are present
        assert "### " in result.output

        with open(os.path.join(project_root_path, "output.md"), "w") as file:
            file.write(result.output)
        snapshot_directory(snapshot=snapshot, directory_path=project_root_path)


def test_get_no_header_output_format(tmp_path):
    """Test that --no-header outputs only sections without version header."""
    runner = CliRunner()
    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
    changelog_file = os.path.join(resources_dir, "CHANGELOG_with_changes.md")

    result = runner.invoke(
        cli,
        [
            "-f",
            changelog_file,
            "get",
            "--no-header",
            "1.0.0",
        ],
        catch_exceptions=False,
    )
    assert result.exit_code == 0, result.output

    # Should not contain version header (## 1.0.0 or ## [1.0.0])
    assert "## 1.0.0" not in result.output
    assert "## [1.0.0]" not in result.output

    # Should contain section headers (###)
    assert "###" in result.output

    # Should contain actual content
    assert "New visual identity" in result.output
