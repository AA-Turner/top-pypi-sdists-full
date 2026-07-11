# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for the bump_version module."""

from __future__ import annotations

import datetime
import tempfile
from pathlib import Path

import pytest
import semver
import yaml

from airbyte_ops_mcp.airbyte_repo.bump_version import (
    BumpType,
    ChangelogEntry,
    ChangelogParsingError,
    ConnectorNotFoundError,
    InvalidVersionError,
    VersionNotFoundError,
    bump_connector_version,
    calculate_new_version,
    get_connector_path,
    get_current_version,
    parse_changelog,
    strip_prerelease_suffix,
    update_changelog,
    update_metadata_version,
    update_pyproject_version,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "current_version,bump_type,new_version,expected",
    [
        pytest.param("1.0.0", BumpType.PATCH, None, "1.0.1", id="patch_bump"),
        pytest.param("1.0.0", BumpType.MINOR, None, "1.1.0", id="minor_bump"),
        pytest.param("1.0.0", BumpType.MAJOR, None, "2.0.0", id="major_bump"),
        pytest.param("1.2.3", BumpType.PATCH, None, "1.2.4", id="patch_bump_complex"),
        pytest.param(
            "0.1.0", BumpType.MINOR, None, "0.2.0", id="minor_bump_zero_major"
        ),
        pytest.param("1.0.0", None, "2.0.0", "2.0.0", id="explicit_version"),
        pytest.param("1.0.0", None, "1.5.0", "1.5.0", id="explicit_version_minor"),
        # RC bump types on non-RC versions
        pytest.param(
            "1.2.3", BumpType.PATCH_RC, None, "1.2.4-rc.1", id="patch_rc_from_stable"
        ),
        pytest.param(
            "1.2.3", BumpType.MINOR_RC, None, "1.3.0-rc.1", id="minor_rc_from_stable"
        ),
        pytest.param(
            "1.2.3", BumpType.MAJOR_RC, None, "2.0.0-rc.1", id="major_rc_from_stable"
        ),
        pytest.param(
            "0.1.0",
            BumpType.MINOR_RC,
            None,
            "0.2.0-rc.1",
            id="minor_rc_from_zero_major",
        ),
        # Smart 'rc' bump type
        pytest.param(
            "1.2.3",
            BumpType.RC,
            None,
            "1.3.0-rc.1",
            id="rc_from_stable_defaults_to_minor",
        ),
        pytest.param(
            "1.3.0-rc.1", BumpType.RC, None, "1.3.0-rc.2", id="rc_bump_rc_number"
        ),
        pytest.param(
            "1.3.0-rc.5", BumpType.RC, None, "1.3.0-rc.6", id="rc_bump_high_rc_number"
        ),
        # Promote
        pytest.param(
            "1.3.0-rc.2", BumpType.PROMOTE, None, "1.3.0", id="promote_rc_to_stable"
        ),
        pytest.param(
            "2.0.0-rc.1",
            BumpType.PROMOTE,
            None,
            "2.0.0",
            id="promote_major_rc_to_stable",
        ),
    ],
)
def test_calculate_new_version(
    current_version: str,
    bump_type: BumpType | None,
    new_version: str | None,
    expected: str,
):
    """Test version calculation with various bump types and explicit versions."""
    result = calculate_new_version(current_version, bump_type, new_version)
    assert result == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "current_version,new_version,error_type",
    [
        pytest.param(
            "1.0.0", "invalid", InvalidVersionError, id="invalid_explicit_version"
        ),
        pytest.param(
            "invalid", BumpType.PATCH, InvalidVersionError, id="invalid_current_version"
        ),
        # Non-RC bump types on an RC version should fail
        pytest.param(
            "1.3.0-rc.1", BumpType.PATCH, InvalidVersionError, id="patch_on_rc_version"
        ),
        pytest.param(
            "1.3.0-rc.1", BumpType.MINOR, InvalidVersionError, id="minor_on_rc_version"
        ),
        pytest.param(
            "1.3.0-rc.1", BumpType.MAJOR, InvalidVersionError, id="major_on_rc_version"
        ),
        pytest.param(
            "1.3.0-rc.1",
            BumpType.PATCH_RC,
            InvalidVersionError,
            id="patch_rc_on_rc_version",
        ),
        pytest.param(
            "1.3.0-rc.1",
            BumpType.MINOR_RC,
            InvalidVersionError,
            id="minor_rc_on_rc_version",
        ),
        pytest.param(
            "1.3.0-rc.1",
            BumpType.MAJOR_RC,
            InvalidVersionError,
            id="major_rc_on_rc_version",
        ),
        # Promote on non-RC should fail
        pytest.param(
            "1.2.3",
            BumpType.PROMOTE,
            InvalidVersionError,
            id="promote_on_stable_version",
        ),
        # Malformed RC suffixes should fail
        pytest.param(
            "1.3.0-rc.0",
            BumpType.RC,
            InvalidVersionError,
            id="rc_bump_on_rc_zero",
        ),
        pytest.param(
            "1.3.0-rc.0",
            BumpType.PROMOTE,
            InvalidVersionError,
            id="promote_rc_zero",
        ),
    ],
)
def test_calculate_new_version_errors(
    current_version: str,
    new_version: str | BumpType,
    error_type: type,
):
    """Test version calculation error cases."""
    if isinstance(new_version, BumpType):
        with pytest.raises(error_type):
            calculate_new_version(current_version, new_version, None)
    else:
        with pytest.raises(error_type):
            calculate_new_version(current_version, None, new_version)


@pytest.mark.unit
def test_calculate_new_version_missing_args():
    """Test that ValueError is raised when neither bump_type nor new_version is provided."""
    with pytest.raises(
        ValueError, match="Either bump_type or new_version must be provided"
    ):
        calculate_new_version("1.0.0", None, None)


@pytest.mark.unit
@pytest.mark.parametrize(
    "version_string,expected",
    [
        pytest.param("1.2.3", "1.2.3", id="stable_version_unchanged"),
        pytest.param("2.23.16-rc.1", "2.23.16", id="rc_suffix_stripped"),
        pytest.param("1.3.0-rc.5", "1.3.0", id="rc_high_number_stripped"),
        pytest.param("0.1.0-rc.1", "0.1.0", id="rc_zero_major_stripped"),
        pytest.param("1.0.0-preview.abc1234", "1.0.0", id="preview_suffix_stripped"),
        pytest.param("10.20.30", "10.20.30", id="large_version_numbers"),
    ],
)
def test_strip_prerelease_suffix(
    version_string: str,
    expected: str,
):
    """Test stripping pre-release suffixes from version strings."""
    result = strip_prerelease_suffix(version_string)
    assert result == expected


@pytest.mark.unit
def test_strip_prerelease_suffix_invalid_version():
    """Test that InvalidVersionError is raised for invalid version strings."""
    with pytest.raises(InvalidVersionError):
        strip_prerelease_suffix("not-a-version")


@pytest.mark.unit
def test_get_connector_path_not_found():
    """Test that ConnectorNotFoundError is raised for non-existent connector."""
    with tempfile.TemporaryDirectory() as tmpdir, pytest.raises(ConnectorNotFoundError):
        get_connector_path(tmpdir, "source-nonexistent")


@pytest.mark.unit
def test_get_connector_path_exists():
    """Test that get_connector_path returns correct path for existing connector."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = (
            Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        )
        connector_dir.mkdir(parents=True)

        result = get_connector_path(tmpdir, "source-test")
        assert result == connector_dir


@pytest.mark.unit
def test_get_current_version():
    """Test getting current version from metadata.yaml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = (
            Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        )
        connector_dir.mkdir(parents=True)

        metadata_content = """data:
  dockerImageTag: "1.2.3"
  name: source-test
"""
        (connector_dir / "metadata.yaml").write_text(metadata_content)

        version = get_current_version(connector_dir)
        assert version == "1.2.3"


@pytest.mark.unit
def test_get_current_version_not_found():
    """Test that VersionNotFoundError is raised when metadata.yaml doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = Path(tmpdir) / "source-test"
        connector_dir.mkdir(parents=True)

        with pytest.raises(VersionNotFoundError):
            get_current_version(connector_dir)


@pytest.mark.unit
def test_get_current_version_missing_tag():
    """Test that VersionNotFoundError is raised when dockerImageTag is missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = Path(tmpdir) / "source-test"
        connector_dir.mkdir(parents=True)

        metadata_content = """data:
  name: source-test
"""
        (connector_dir / "metadata.yaml").write_text(metadata_content)

        with pytest.raises(VersionNotFoundError):
            get_current_version(connector_dir)


@pytest.mark.unit
def test_update_metadata_version():
    """Test updating version in metadata.yaml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = Path(tmpdir)

        metadata_content = """data:
  dockerImageTag: 1.0.0
  name: source-test
"""
        (connector_dir / "metadata.yaml").write_text(metadata_content)

        result = update_metadata_version(connector_dir, "1.1.0")
        assert result is True

        updated_content = (connector_dir / "metadata.yaml").read_text()
        assert "dockerImageTag: 1.1.0" in updated_content
        assert "dockerImageTag: 1.0.0" not in updated_content


@pytest.mark.unit
def test_update_metadata_version_dry_run():
    """Test that dry_run doesn't modify the file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = Path(tmpdir)

        metadata_content = """data:
  dockerImageTag: 1.0.0
  name: source-test
"""
        (connector_dir / "metadata.yaml").write_text(metadata_content)

        result = update_metadata_version(connector_dir, "1.1.0", dry_run=True)
        assert result is True

        # File should not be modified
        content = (connector_dir / "metadata.yaml").read_text()
        assert "dockerImageTag: 1.0.0" in content


@pytest.mark.unit
def test_update_pyproject_version():
    """Test updating version in pyproject.toml."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = Path(tmpdir)

        pyproject_content = """[tool.poetry]
name = "source-test"
version = "1.0.0"
"""
        (connector_dir / "pyproject.toml").write_text(pyproject_content)

        result = update_pyproject_version(connector_dir, "1.1.0")
        assert result is True

        updated_content = (connector_dir / "pyproject.toml").read_text()
        assert 'version = "1.1.0"' in updated_content


@pytest.mark.unit
def test_update_pyproject_version_no_file():
    """Test that update_pyproject_version returns False when file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = Path(tmpdir)

        result = update_pyproject_version(connector_dir, "1.1.0")
        assert result is False


@pytest.mark.unit
def test_parse_changelog_valid():
    """Test parsing a valid changelog table."""
    markdown_lines = [
        "# Changelog",
        "",
        "| Version | Date | Pull Request | Subject |",
        "|---------|------|--------------|---------|",
        "| 1.0.0 | 2025-01-01 | [123](https://github.com/airbytehq/airbyte/pull/123) | Initial release |",
    ]

    start_index, entries = parse_changelog(markdown_lines)
    assert start_index == 4
    assert len(entries) == 1

    entry = next(iter(entries))
    assert str(entry.version) == "1.0.0"
    assert entry.pr_number == 123
    assert entry.comment == "Initial release"


@pytest.mark.unit
def test_parse_changelog_with_rc_version():
    """Test parsing a changelog table that contains RC version entries."""
    markdown_lines = [
        "# Changelog",
        "",
        "| Version | Date | Pull Request | Subject |",
        "|---------|------|--------------|---------|",
        "| 1.3.0-rc.2 | 2025-02-01 | [456](https://github.com/airbytehq/airbyte/pull/456) | RC bump |",
        "| 1.2.3 | 2025-01-01 | [123](https://github.com/airbytehq/airbyte/pull/123) | Initial release |",
    ]

    start_index, entries = parse_changelog(markdown_lines)
    assert start_index == 4
    assert len(entries) == 2

    versions = {str(e.version) for e in entries}
    assert "1.3.0-rc.2" in versions
    assert "1.2.3" in versions


@pytest.mark.unit
def test_parse_changelog_no_table():
    """Test that ChangelogParsingError is raised when no changelog table exists."""
    markdown_lines = [
        "# Changelog",
        "",
        "No table here",
    ]

    with pytest.raises(ChangelogParsingError):
        parse_changelog(markdown_lines)


@pytest.mark.unit
def test_changelog_entry_to_markdown():
    """Test ChangelogEntry.to_markdown() output."""
    entry = ChangelogEntry(
        date=datetime.date(2025, 1, 15),
        version=semver.Version.parse("1.2.3"),
        pr_number=456,
        comment="Fix bug",
    )

    markdown = entry.to_markdown()
    assert "1.2.3" in markdown
    assert "2025-01-15" in markdown
    assert "456" in markdown
    assert "Fix bug" in markdown


@pytest.mark.unit
def test_bump_connector_version_full():
    """Test full bump_connector_version workflow."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create connector directory structure
        connector_dir = (
            Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        )
        connector_dir.mkdir(parents=True)

        # Create metadata.yaml
        metadata_content = """data:
  dockerImageTag: 1.0.0
  name: source-test
"""
        (connector_dir / "metadata.yaml").write_text(metadata_content)

        # Create pyproject.toml
        pyproject_content = """[tool.poetry]
name = "source-test"
version = "1.0.0"
"""
        (connector_dir / "pyproject.toml").write_text(pyproject_content)

        # Run bump
        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="patch",
        )

        assert result.connector == "source-test"
        assert result.previous_version == "1.0.0"
        assert result.new_version == "1.0.1"
        assert len(result.files_modified) == 2
        assert result.dry_run is False

        # Verify files were updated
        metadata = (connector_dir / "metadata.yaml").read_text()
        assert "dockerImageTag: 1.0.1" in metadata

        pyproject = (connector_dir / "pyproject.toml").read_text()
        assert 'version = "1.0.1"' in pyproject


@pytest.mark.unit
def test_bump_connector_version_dry_run():
    """Test bump_connector_version with dry_run=True."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create connector directory structure
        connector_dir = (
            Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        )
        connector_dir.mkdir(parents=True)

        # Create metadata.yaml
        metadata_content = """data:
  dockerImageTag: 1.0.0
  name: source-test
"""
        (connector_dir / "metadata.yaml").write_text(metadata_content)

        # Run bump with dry_run
        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="minor",
            dry_run=True,
        )

        assert result.connector == "source-test"
        assert result.previous_version == "1.0.0"
        assert result.new_version == "1.1.0"
        assert result.dry_run is True

        # Verify file was NOT updated
        metadata = (connector_dir / "metadata.yaml").read_text()
        assert "dockerImageTag: 1.0.0" in metadata


@pytest.mark.unit
def test_bump_connector_version_connector_not_found():
    """Test bump_connector_version with non-existent connector."""
    with tempfile.TemporaryDirectory() as tmpdir, pytest.raises(ConnectorNotFoundError):
        bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-nonexistent",
            bump_type="patch",
        )


@pytest.mark.unit
def test_update_changelog_adds_entry():
    """Test update_changelog writes a new entry with the given version and PR number."""
    with tempfile.TemporaryDirectory() as tmpdir:
        doc_path = Path(tmpdir) / "test.md"
        doc_path.write_text(
            "# Source Test\n"
            "\n"
            "## Changelog\n"
            "\n"
            "| Version | Date | Pull Request | Subject |\n"
            "|:--------|:-----|:-------------|:--------|\n"
            "| 0.9.0 | 2024-01-01 | [100](https://github.com/airbytehq/airbyte/pull/100) | Initial release |\n"
        )

        modified = update_changelog(
            doc_path=doc_path,
            new_version="1.0.0",
            changelog_message="Promoted release candidate to GA",
            pr_number=12345,
        )

        assert modified is True
        content = doc_path.read_text()
        assert "1.0.0" in content
        assert "12345" in content
        assert "Promoted release candidate to GA" in content
        # Original entry still present
        assert "0.9.0" in content


def _make_connector(
    tmpdir: str, version: str = "1.0.0", extra_metadata: str = ""
) -> Path:
    """Helper to create a minimal connector directory for testing."""
    connector_dir = Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
    connector_dir.mkdir(parents=True)
    metadata_content = (
        f"data:\n  dockerImageTag: {version}\n  name: source-test\n{extra_metadata}"
    )
    (connector_dir / "metadata.yaml").write_text(metadata_content)
    return connector_dir


@pytest.mark.unit
def test_rc_bump_does_not_create_registry_overrides():
    """RC bump should not add registry override pins."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = _make_connector(tmpdir, version="2.3.0")

        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="minor_rc",
        )

        assert result.new_version == "2.4.0-rc.1"

        metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text())
        data = metadata["data"]

        # Progressive rollout flag should be set
        assert (
            data["releases"]["rolloutConfiguration"]["enableProgressiveRollout"] is True
        )

        assert "registryOverrides" not in data


@pytest.mark.unit
def test_rc_bump_does_not_clobber_existing_overrides():
    """RC bump should preserve pre-existing registry override values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        extra = (
            "  registryOverrides:\n"
            "    cloud:\n"
            "      dockerImageTag: 1.5.0\n"
            "    oss:\n"
            "      dockerImageTag: 1.5.0\n"
        )
        connector_dir = _make_connector(tmpdir, version="2.3.0", extra_metadata=extra)

        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="minor_rc",
        )

        assert result.new_version == "2.4.0-rc.1"

        metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text())
        data = metadata["data"]

        assert data["registryOverrides"]["cloud"]["dockerImageTag"] == "1.5.0"
        assert data["registryOverrides"]["oss"]["dockerImageTag"] == "1.5.0"


@pytest.mark.unit
def test_promote_preserves_registry_overrides():
    """Promote (RC → GA) should preserve registry overrides."""
    with tempfile.TemporaryDirectory() as tmpdir:
        extra = (
            "  releases:\n"
            "    rolloutConfiguration:\n"
            "      enableProgressiveRollout: true\n"
            "  registryOverrides:\n"
            "    cloud:\n"
            "      dockerImageTag: 2.3.0\n"
            "    oss:\n"
            "      dockerImageTag: 2.3.0\n"
        )
        connector_dir = _make_connector(
            tmpdir, version="2.4.0-rc.1", extra_metadata=extra
        )

        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="promote",
        )

        assert result.new_version == "2.4.0"

        metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text())
        data = metadata["data"]

        # Progressive rollout flag should be cleared
        assert (
            data["releases"]["rolloutConfiguration"]["enableProgressiveRollout"]
            is False
        )

        assert data["registryOverrides"]["cloud"]["dockerImageTag"] == "2.3.0"
        assert data["registryOverrides"]["oss"]["dockerImageTag"] == "2.3.0"


@pytest.mark.unit
def test_promote_keeps_progressive_rollout_for_autopilot():
    """Promote leaves `enableProgressiveRollout: true` when mode is autopilot.

    Autopilot connectors treat progressive rollout as their standing default, so
    promoting an RC to GA must not clear the flag.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        extra = (
            "  releases:\n"
            "    rolloutConfiguration:\n"
            "      enableProgressiveRollout: true\n"
            "      defaultRolloutMode: autopilot\n"
        )
        connector_dir = _make_connector(
            tmpdir, version="2.4.0-rc.1", extra_metadata=extra
        )

        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="promote",
        )

        assert result.new_version == "2.4.0"

        metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text())
        rollout = metadata["data"]["releases"]["rolloutConfiguration"]

        # Flag stays on; mode is untouched.
        assert rollout["enableProgressiveRollout"] is True
        assert rollout["defaultRolloutMode"] == "autopilot"


@pytest.mark.unit
def test_promote_ga_progressive_rollout_fails():
    """Promote is only defined for release candidates."""
    with tempfile.TemporaryDirectory() as tmpdir:
        extra = (
            "  releases:\n"
            "    rolloutConfiguration:\n"
            "      enableProgressiveRollout: true\n"
        )
        _make_connector(tmpdir, version="2.4.0", extra_metadata=extra)

        with pytest.raises(InvalidVersionError, match="not a release candidate"):
            bump_connector_version(
                repo_path=tmpdir,
                connector_name="source-test",
                bump_type="promote",
            )


@pytest.mark.unit
def test_rc_bump_preserves_metadata_formatting():
    """RC bump should only change relevant fields, not reformat the entire file.

    This is a regression test for the PyYAML `yaml.dump()` issue where
    round-tripping through `safe_load` / `dump` would change quote styles,
    indentation, and string flow styles.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = (
            Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        )
        connector_dir.mkdir(parents=True)

        # Realistic metadata with mixed quote styles, 4-space list indentation,
        # and multi-line strings — the exact patterns PyYAML would mangle.
        original_content = (
            "data:\n"
            '  dockerImageTag: "2.3.0"\n'
            "  name: source-test\n"
            "  connectorType: source\n"
            "  releases:\n"
            "    breakingChanges:\n"
            "      4.0.0:\n"
            '        message: "ID and products.year fields have new types."\n'
            '        upgradeDeadline: "2023-07-19"\n'
            '        deadlineAction: "disable"\n'
        )
        (connector_dir / "metadata.yaml").write_text(original_content)

        bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="minor_rc",
        )

        result_content = (connector_dir / "metadata.yaml").read_text()

        # The version line should be updated
        assert "2.4.0-rc.1" in result_content

        # Quote styles from the original must be preserved (not single-quoted)
        assert '"2023-07-19"' in result_content
        assert '"disable"' in result_content
        assert '"ID and products.year fields have new types."' in result_content

        # New fields should be added without reformatting existing content
        assert "enableProgressiveRollout: true" in result_content


@pytest.mark.unit
def test_promote_preserves_metadata_formatting():
    """Promote should only change relevant fields, not reformat the entire file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        connector_dir = (
            Path(tmpdir) / "airbyte-integrations" / "connectors" / "source-test"
        )
        connector_dir.mkdir(parents=True)

        original_content = (
            "data:\n"
            '  dockerImageTag: "2.4.0-rc.1"\n'
            "  name: source-test\n"
            "  releases:\n"
            "    rolloutConfiguration:\n"
            "      enableProgressiveRollout: true\n"
            "    breakingChanges:\n"
            "      4.0.0:\n"
            '        message: "ID and products.year fields have new types."\n'
            '        upgradeDeadline: "2023-07-19"\n'
            "  registryOverrides:\n"
            "    cloud:\n"
            "      dockerImageTag: 2.3.0\n"
            "    oss:\n"
            "      dockerImageTag: 2.3.0\n"
        )
        (connector_dir / "metadata.yaml").write_text(original_content)

        bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="promote",
        )

        result_content = (connector_dir / "metadata.yaml").read_text()

        # Version should be promoted
        assert "2.4.0" in result_content
        assert "rc" not in result_content.split("dockerImageTag")[1].split("\n")[0]

        # Quote styles must be preserved
        assert '"2023-07-19"' in result_content
        assert '"ID and products.year fields have new types."' in result_content

        # Progressive rollout should be disabled
        assert "enableProgressiveRollout: false" in result_content


@pytest.mark.unit
def test_progressive_rollout_enabled_false_disables_flag():
    """Passing `progressive_rollout_enabled=False` should set the flag to false."""
    with tempfile.TemporaryDirectory() as tmpdir:
        extra = (
            "  releases:\n"
            "    rolloutConfiguration:\n"
            "      enableProgressiveRollout: true\n"
        )
        connector_dir = _make_connector(tmpdir, version="2.3.0", extra_metadata=extra)

        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            new_version="2.3.0-preview.abc1234",
            no_changelog=True,
            progressive_rollout_enabled=False,
        )

        assert result.new_version == "2.3.0-preview.abc1234"

        metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text())
        data = metadata["data"]

        # Flag should be set to false
        assert (
            data["releases"]["rolloutConfiguration"]["enableProgressiveRollout"]
            is False
        )


@pytest.mark.unit
def test_progressive_rollout_enabled_false_noop_when_already_false():
    """When the flag is already false, passing `progressive_rollout_enabled=False` is a no-op."""
    with tempfile.TemporaryDirectory() as tmpdir:
        extra = (
            "  releases:\n"
            "    rolloutConfiguration:\n"
            "      enableProgressiveRollout: false\n"
        )
        _make_connector(tmpdir, version="2.3.0", extra_metadata=extra)

        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            new_version="2.3.0-preview.abc1234",
            no_changelog=True,
            progressive_rollout_enabled=False,
        )

        # metadata.yaml should only be listed once (for the version bump),
        # not a second time for the rollout flag since it was already false.
        metadata_entries = [
            f for f in result.files_modified if f.endswith("metadata.yaml")
        ]
        assert len(metadata_entries) == 1


@pytest.mark.unit
def test_progressive_rollout_enabled_false_does_not_touch_overrides():
    """Explicit `progressive_rollout_enabled=False` should NOT remove registry overrides."""
    with tempfile.TemporaryDirectory() as tmpdir:
        extra = (
            "  releases:\n"
            "    rolloutConfiguration:\n"
            "      enableProgressiveRollout: true\n"
            "  registryOverrides:\n"
            "    cloud:\n"
            "      dockerImageTag: 2.2.0\n"
            "    oss:\n"
            "      dockerImageTag: 2.2.0\n"
        )
        connector_dir = _make_connector(tmpdir, version="2.3.0", extra_metadata=extra)

        bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            new_version="2.3.0-preview.abc1234",
            no_changelog=True,
            progressive_rollout_enabled=False,
        )

        metadata = yaml.safe_load((connector_dir / "metadata.yaml").read_text())
        data = metadata["data"]

        # Flag should be false
        assert (
            data["releases"]["rolloutConfiguration"]["enableProgressiveRollout"]
            is False
        )

        # Registry overrides should be PRESERVED (not removed)
        assert data["registryOverrides"]["cloud"]["dockerImageTag"] == "2.2.0"
        assert data["registryOverrides"]["oss"]["dockerImageTag"] == "2.2.0"


@pytest.mark.unit
def test_progressive_rollout_enabled_overrides_automatic_rc_behaviour():
    """Explicit `progressive_rollout_enabled=False` should override the flag but not preclude auto setup."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _make_connector(tmpdir, version="2.3.0")

        result = bump_connector_version(
            repo_path=tmpdir,
            connector_name="source-test",
            bump_type="minor_rc",
            progressive_rollout_enabled=False,
        )

        assert result.new_version == "2.4.0-rc.1"

        metadata = yaml.safe_load(
            (
                Path(tmpdir)
                / "airbyte-integrations"
                / "connectors"
                / "source-test"
                / "metadata.yaml"
            ).read_text()
        )
        data = metadata["data"]

        # Explicit False should win over the automatic RC behaviour
        assert (
            data["releases"]["rolloutConfiguration"]["enableProgressiveRollout"]
            is False
        )
        assert "registryOverrides" not in data
