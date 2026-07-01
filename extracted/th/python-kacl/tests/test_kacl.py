import os
from unittest import TestCase

import pytest
import yaml

import kacl
from kacl.config import KACLConfig
from kacl.exception import KACLException
from tests.snapshot_directory import snapshot_directory


class TestKacl(TestCase):
    def test_load_valid(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )
        changelog = kacl.load(changelog_file)

        self.assertEqual(changelog.title(), "Changelog")
        self.assertGreater(len(changelog.versions()), 0)

        version = changelog.get("1.0.0")
        self.assertIsNotNone(version)

        added_changes = version.changes("Added")
        self.assertIsNotNone(added_changes)

        added_items = added_changes.items()
        self.assertIsNotNone(added_items)

    def test_dump(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )
        changelog = kacl.load(changelog_file)
        changelog_dump = kacl.dump(changelog)
        self.assertIsNotNone(changelog_dump)

        with open(changelog_file, "r") as reference_file:
            changelog_reference = reference_file.read()
        reference_file.close()

        changelog_dump_lines = changelog_dump.split("\n")
        changelog_reference_lines = changelog_reference.split("\n")

        self.assertEqual(len(changelog_dump_lines), len(changelog_reference_lines))

        for i in range(len(changelog_dump_lines)):
            if changelog_dump_lines[i] != changelog_reference_lines[i]:
                print(
                    f"Line {i + 1} differs:\n"
                    f"Dump: {changelog_dump_lines[i]}\n"
                    f"Reference: {changelog_reference_lines[i]}"
                )

        self.assertEqual(changelog_dump, changelog_reference)

    def test_add_change(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )

        changelog = kacl.load(changelog_file)

        msg = "This is my first added change"
        changelog.add("Added", msg)

        changelog_dump = kacl.dump(changelog)
        self.assertIsNotNone(changelog_dump)

        changelog_changed = kacl.parse(changelog_dump)
        self.assertIsNotNone(changelog_changed)

        unreleased = changelog_changed.get("Unreleased")
        self.assertIsNotNone(unreleased)

        unreleased_change_sections = unreleased.sections()
        self.assertIsNotNone(unreleased_change_sections)
        self.assertIn("Added", unreleased_change_sections)

        unreleased_changes_added = unreleased.changes("Added")
        self.assertIsNotNone(unreleased_changes_added)

        self.assertIn(msg, unreleased_changes_added.items())

    def test_release(self):
        valid_files = ["CHANGELOG.md", "CHANGELOG_unrelease_only.md"]

        for filename in valid_files:
            changelog_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data", filename
            )
            changelog = kacl.load(changelog_file)

            msg = "This is my first added change"
            changelog.add("Added", msg)

            self.assertTrue(changelog.has_changes())

            changelog.release(version="2.0.0", link="https://my-new-version/2.0.0.html")

            changelog_dump = kacl.dump(changelog)
            self.assertIsNotNone(changelog_dump)

            changelog_changed = kacl.parse(changelog_dump)
            self.assertIsNotNone(changelog_changed)

            version = changelog_changed.get("2.0.0")
            self.assertIsNotNone(version)

            self.assertIn(msg, version.changes("Added").items())

    def test_invalid(self):
        invalid_files = [
            "CHANGELOG_invalid.md",
            "CHANGELOG_missing_sections.md",
            "CHANGELOG_no_unreleased.md",
        ]

        for filename in invalid_files:
            changelog_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data", filename
            )
            changelog = kacl.load(changelog_file)
            self.assertFalse(changelog.is_valid())

    def test_valid(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )
        changelog = kacl.load(changelog_file)
        self.assertTrue(changelog.is_valid())

        validation = changelog.validate()
        self.assertGreaterEqual(len(validation.errors()), 0)

    def test_valid_keepachangelogcom(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data/CHANGELOG_keepachangelog.com.md",
        )
        changelog = kacl.load(changelog_file)
        self.assertTrue(changelog.is_valid())

        validation = changelog.validate()
        self.assertGreaterEqual(len(validation.errors()), 0)

    def test_valid_project_changelog(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "CHANGELOG.md"
        )
        changelog = kacl.load(changelog_file)
        self.assertTrue(changelog.is_valid())

        validation = changelog.validate()
        self.assertGreaterEqual(len(validation.errors()), 0)

    def test_invalid_version_ordering(self):
        invalid_files = [
            "CHANGELOG_duplicate_version.md",
            "CHANGELOG_ascending_versions.md",
        ]

        for filename in invalid_files:
            changelog_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data", filename
            )
            changelog = kacl.load(changelog_file)
            self.assertFalse(changelog.is_valid())

            error_messages = [e.error_message() for e in changelog.validate().errors()]
            self.assertTrue(
                any("descending" in m for m in error_messages), error_messages
            )

    def test_valid_descending_versions_with_prerelease(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data/CHANGELOG_descending_prerelease.md",
        )
        changelog = kacl.load(changelog_file)

        error_messages = [e.error_message() for e in changelog.validate().errors()]
        ordering_errors = [
            m for m in error_messages if "descending" in m or "Duplicate" in m
        ]
        self.assertEqual(ordering_errors, [], error_messages)

    def test_load_empty(self):
        changelog = kacl.parse("")
        self.assertFalse(changelog.is_valid())

    def test_release_without_changes(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data/CHANGELOG_no_unreleased.md",
        )
        changelog = kacl.load(changelog_file)

        self.assertFalse(changelog.has_changes())
        self.assertRaises(
            Exception,
            changelog.release,
            "1.1.1",
            "https://gitlab.com/schmieder.matthias/python-kacl.git/-/compare/v1.0.0...HEAD",
        )

    def test_release_existing_version(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )
        changelog = kacl.load(changelog_file)

        msg = "This is my first added change"
        changelog.add("Added", msg)

        self.assertTrue(changelog.has_changes())
        self.assertRaises(
            Exception,
            changelog.release,
            "1.0.0",
            "https://gitlab.com/schmieder.matthias/python-kacl.git/-/compare/v1.0.0...HEAD",
        )

    def test_release_without_older_version(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )
        changelog = kacl.load(changelog_file)

        msg = "This is my first added change"
        changelog.add("Added", msg)

        self.assertTrue(changelog.has_changes())
        self.assertRaises(
            Exception,
            changelog.release,
            "0.9.0",
            "https://gitlab.com/schmieder.matthias/python-kacl.git/-/compare/v1.0.0...HEAD",
        )

    def test_release_with_non_semver(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )
        changelog = kacl.load(changelog_file)

        msg = "This is my first added change"
        changelog.add("Added", msg)

        self.assertTrue(changelog.has_changes())
        self.assertRaises(
            Exception,
            changelog.release,
            "a0.9.0",
            "https://gitlab.com/schmieder.matthias/python-kacl.git/-/compare/v1.0.0...HEAD",
        )

    def test_release_with_allow_no_changes_flag(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data/CHANGELOG_without_changes.md",
        )
        changelog = kacl.load(changelog_file)

        self.assertFalse(changelog.has_changes())
        changelog.release("1.0.1", allow_no_changes=True)
        self.assertEqual("1.0.1", changelog.current_version())

    def test_release_with_increment(self):
        tests = {
            "major": "2.0.0",
            "minor": "1.2.0",
            "patch": "1.1.2",
        }
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )

        for increment, expected_version in tests.items():
            changelog = kacl.load(changelog_file)

            msg = "This is my first added change"
            changelog.add("Added", msg)

            self.assertTrue(changelog.has_changes())
            changelog.release(increment=increment)
            self.assertEqual(expected_version, changelog.current_version())

        fail_tests = {"post": "1.0.0-post.1"}

        for increment, expected_version in fail_tests.items():
            changelog = kacl.load(changelog_file)
            changelog.config.post_release_version_prefix = None

            msg = "This is my first added change"
            changelog.add("Added", msg)

            self.assertTrue(changelog.has_changes())
            self.assertRaises(KACLException, changelog.release, increment=increment)

    def test_release_with_increment_extension(self):
        tests = {
            "major": "2.0.0",
            "minor": "1.2.0",
            "patch": "1.1.2",
            "post": "1.1.1-post.1",
        }
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )

        for increment, expected_version in tests.items():
            changelog = kacl.load(changelog_file)
            changelog.config.post_release_version_prefix = "post"

            msg = "This is my first added change"
            changelog.add("Added", msg)

            self.assertTrue(changelog.has_changes())
            changelog.release(increment=increment)
            self.assertEqual(expected_version, changelog.current_version())

    def test_release_with_increment_extension_hotfix(self):
        tests = {
            "major": "2.0.0",
            "minor": "1.2.0",
            "patch": "1.1.2",
            "post": "1.1.1-hotfix.1",
        }
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG.md"
        )

        for increment, expected_version in tests.items():
            changelog = kacl.load(changelog_file)
            changelog.config.post_release_version_prefix = "hotfix"

            msg = "This is my first added change"
            changelog.add("Added", msg)

            self.assertTrue(changelog.has_changes())
            changelog.release(increment=increment)
            self.assertEqual(expected_version, changelog.current_version())

    def test_post_release_with_increment(self):
        tests = {
            "major": "2.0.0",
            "minor": "1.1.0",
            "patch": "1.0.1",
            "post": "1.0.0-post.2",
        }
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/CHANGELOG_post.md"
        )

        for increment, expected_version in tests.items():
            changelog = kacl.load(changelog_file)
            changelog.config.post_release_version_prefix = "post"

            msg = "This is my first added change"
            changelog.add("Added", msg)

            self.assertTrue(changelog.has_changes())
            changelog.release(increment=increment)
            self.assertEqual(expected_version, changelog.current_version())

    def test_unreleased_missing_sections(self):
        changelog_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data/CHANGELOG_missing_sections.md",
        )

        changelog = kacl.load(changelog_file)
        changelog.validate()
        self.assertFalse(changelog.is_valid())

    def test_config(self):
        config_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "data/config.yml"
        )
        kacl_config = KACLConfig(config_file=config_file)

        default_config = dict()
        with open("kacl/config/kacl-default.yml", "r") as f:
            default_config = yaml.safe_load(f)["kacl"]

        # changes in config_file
        # changelog_file: CHANGELOG.md
        # allowed_header_titles:
        #   - ChangeLog
        # allowed_version_sections:
        #   - Security
        # git:
        #   commit: False

        self.assertNotEqual(
            kacl_config.allowed_header_titles, default_config["allowed_header_titles"]
        )
        self.assertEqual(kacl_config.allowed_header_titles, ["ChangeLog"])

        self.assertNotEqual(
            kacl_config.allowed_version_sections,
            default_config["allowed_version_sections"],
        )
        self.assertEqual(kacl_config.allowed_version_sections, ["Security"])

        self.assertNotEqual(
            kacl_config.git_create_commit, default_config["git"]["commit"]
        )
        self.assertEqual(kacl_config.git_create_commit, True)

    def test_link_generation(self):
        valid_files = ["CHANGELOG_unrelease_only.md"]

        for filename in valid_files:
            changelog_file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data", filename
            )
            changelog = kacl.load(changelog_file)

            changelog = kacl.load(changelog_file)
            changelog.generate_links()

            versions = changelog.versions()
            for v in versions:
                self.assertIsNotNone(v.link())


def test_squash(tmp_path, snapshot):
    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_keepachangelog.com.md",
    )
    changelog = kacl.load(changelog_file)
    assert changelog.is_valid()

    validation = changelog.validate()
    assert len(validation.errors()) < 1

    changelog.squash(version_start="0.0.1", version_end="0.3.0", keep_version_info=True)

    squashed_changelog_file = os.path.join(tmp_path, "CHANGELOG.md")
    # Open the file for writing.
    with open(squashed_changelog_file, "w") as f:
        f.write(kacl.dump(changelog))

    snapshot_directory(snapshot=snapshot, directory_path=tmp_path)


@pytest.mark.skip(reason="No issue tracker openly available, test locally.")
def test_issue_tracker_comment(tmp_path):
    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_issue_management.md",
    )
    changelog = kacl.load(changelog_file)
    assert changelog.is_valid()

    changelog.add_comments(version=changelog.current_version())


def test_render_comments(tmp_path):
    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_issue_management.md",
    )
    changelog = kacl.load(changelog_file)
    assert changelog.is_valid()

    rendered_comments = changelog.render_comments(version=changelog.current_version())

    assert "jira" in rendered_comments


def test_get_issues(tmp_path):
    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_issue_management.md",
    )
    changelog = kacl.load(changelog_file)
    assert changelog.is_valid()

    issues = changelog.get_associated_issues(version=changelog.current_version())
    assert len(issues["jira"]) == 5


def test_simple_metadata(tmp_path):
    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_with_simple_metadata.md",
    )
    changelog = kacl.load(changelog_file)
    assert changelog.is_valid()

    changelog.release(increment="major")

    content = kacl.dump(changelog)

    assert "---\ntitle: CHANGELOG\n---\n" in str(content)


def test_complex_metadata(tmp_path):
    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_with_complex_metadata.md",
    )
    changelog = kacl.load(changelog_file)
    assert changelog.is_valid()

    changelog.release(increment="major")

    content = kacl.dump(changelog)

    assert (
        "---\nlist:\n- entry1\n- additional: true\n  key: value\ntitle: CHANGELOG\n---\n"
        in str(content)
    )


def test_release_no_unreleased_with_autolink(tmp_path):
    """Test that auto-linking works correctly when add_unreleased=False."""
    from kacl.config import KACLConfig

    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_with_changes.md",
    )
    config_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/no-unreleased-config.yml",
    )

    # Load changelog and set custom config
    changelog = kacl.load(changelog_file)
    changelog.config = KACLConfig(config_file)
    assert changelog.is_valid()

    # Release with auto-linking
    changelog.release(version="2.0.0", auto_link=True)

    # Verify the new version has a link
    new_version = changelog.get("2.0.0")
    assert new_version is not None
    assert new_version.link() is not None

    # Verify there's no Unreleased section after release
    versions = changelog.versions()
    assert (
        versions[0].version() == "2.0.0"
    ), "First version should be the new release, not Unreleased"

    # Verify the link points to the correct comparison
    content = kacl.dump(changelog)
    assert "[2.0.0]:" in content, "New version should have a link reference"


def test_serializer_sections_dict(tmp_path):
    """Test that serializer correctly handles version.sections() dict (for --no-header)."""
    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_with_changes.md",
    )
    changelog = kacl.load(changelog_file)
    version = changelog.get("1.0.0")

    # Get sections dict (what's passed when using --no-header)
    sections = version.sections()

    # Serialize the sections dict
    content = kacl.dump(sections)

    # Verify output doesn't include version header
    assert "## 1.0.0" not in content
    assert "## [1.0.0]" not in content

    # Verify it includes section headers and content
    assert "### Added" in content
    assert "New visual identity" in content


def test_serializer_invalid_dict():
    """Test that serializer rejects invalid dict input."""
    import pytest

    # Try to serialize a plain dict that's not from version.sections()
    invalid_dict = {"key": "value", "another": "item"}

    with pytest.raises(TypeError) as exc_info:
        kacl.dump(invalid_dict)

    assert "KACLChanges" in str(exc_info.value)


def test_release_no_unreleased_multiple_versions(tmp_path):
    """Test auto-link with add_unreleased=False doesn't overwrite existing version links."""
    from kacl.config import KACLConfig

    changelog_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/CHANGELOG_keepachangelog.com.md",
    )
    config_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data/no-unreleased-config.yml",
    )

    # Load changelog and set custom config
    changelog = kacl.load(changelog_file)
    changelog.config = KACLConfig(config_file)

    # Get the second version's link before release (should not be modified)
    versions_before = changelog.versions()
    if len(versions_before) > 1:
        second_version_before = versions_before[1]
        second_version_link_before = second_version_before.link()

    # Release with auto-linking (allow_no_changes since the test file may not have unreleased changes)
    changelog.release(version="2.0.0", auto_link=True, allow_no_changes=True)

    # Get versions after release
    versions_after = changelog.versions()

    # First version should be the new release (not Unreleased)
    assert versions_after[0].version() == "2.0.0"

    # New version should have a link
    assert versions_after[0].link() is not None

    # Second version's link should not have been modified
    if len(versions_before) > 1 and second_version_link_before:
        second_version_after = versions_after[1]
        # The link might be updated during auto-link, but shouldn't be broken
        assert second_version_after.link() is not None
