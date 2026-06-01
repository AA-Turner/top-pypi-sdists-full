# Copyright (c) 2023 Airbyte, Inc., all rights reserved.

"""Tests for CheckMigrationGuide in the connector QA checks."""

from unittest.mock import Mock

from airbyte_ops_mcp.connector_qa.checks.documentation.documentation import (
    CheckMigrationGuide,
)
from airbyte_ops_mcp.connector_qa.models import CheckStatus


class TestCheckMigrationGuide:
    def test_passed_when_no_breaking_changes(self):
        connector = Mock(
            technical_name="test-connector", metadata={}, migration_guide_file_path=None
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.PASSED
        assert "No breaking changes found" in result.message

    def test_fail_when_migration_guide_missing(self, tmp_path):
        connector = Mock(
            technical_name="test-connector",
            metadata={"releases": {"breakingChanges": {"1.0.0": "Description"}}},
            migration_guide_file_path=tmp_path / "not_existing.md",
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.FAILED
        assert "Migration guide file is missing" in result.message

    def test_fail_when_missing_breaking_change_heading(self, tmp_path):
        connector = Mock(
            name_from_metadata="Test Connector",
            technical_name="test-connector",
            metadata={
                "releases": {
                    "breakingChanges": {"1.0.0": "Description", "2.0.0": "Description"}
                }
            },
            migration_guide_file_path=tmp_path / "migration_guide.md",
        )
        connector.migration_guide_file_path.write_text(
            "# Test Connector Migration Guide\n## Upgrading to 1.0.0\n"
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.FAILED
        assert "is missing headings for breaking changes" in result.message

    def test_fail_when_breaking_headings_in_ascending_order(self, tmp_path):
        connector = Mock(
            name_from_metadata="Test Connector",
            technical_name="test-connector",
            metadata={
                "releases": {
                    "breakingChanges": {"1.0.0": "Description", "2.0.0": "Description"}
                }
            },
            migration_guide_file_path=tmp_path / "migration_guide.md",
        )
        connector.migration_guide_file_path.write_text(
            "# Test Connector Migration Guide\n## Upgrading to 1.0.0\n## Upgrading to 2.0.0\n"
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.FAILED
        assert "has version headings out of descending order" in result.message

    def test_pass_when_correct_breaking_change_headings(self, tmp_path):
        connector = Mock(
            name_from_metadata="Test Connector",
            technical_name="test-connector",
            metadata={
                "releases": {
                    "breakingChanges": {"1.0.0": "Description", "2.0.0": "Description"}
                }
            },
            migration_guide_file_path=tmp_path / "migration_guide.md",
        )
        connector.migration_guide_file_path.write_text(
            "# Test Connector Migration Guide\n## Upgrading to 2.0.0\n## Upgrading to 1.0.0\n"
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.PASSED
        assert "The migration guide is correctly templated" in result.message

    def test_pass_when_extra_non_breaking_headings_present(self, tmp_path):
        """Extra headings for non-breaking versions should be allowed.

        The migration guide may document non-breaking changes (e.g. informational
        migration notes). These extra headings should not cause the check to fail
        as long as all breaking change headings are present in the correct order.
        """
        connector = Mock(
            name_from_metadata="Test Connector",
            technical_name="test-connector",
            metadata={
                "releases": {
                    "breakingChanges": {"1.0.0": "Description", "2.0.0": "Description"}
                }
            },
            migration_guide_file_path=tmp_path / "migration_guide.md",
        )
        connector.migration_guide_file_path.write_text(
            "# Test Connector Migration Guide\n"
            "## Upgrading to 2.1.0\n"
            "Non-breaking informational note.\n"
            "## Upgrading to 2.0.0\n"
            "Breaking change details.\n"
            "## Upgrading to 1.0.0\n"
            "Breaking change details.\n"
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.PASSED
        assert "The migration guide is correctly templated" in result.message

    def test_fail_when_extra_headings_but_missing_breaking(self, tmp_path):
        """Extra non-breaking headings should not compensate for missing breaking change headings."""
        connector = Mock(
            name_from_metadata="Test Connector",
            technical_name="test-connector",
            metadata={
                "releases": {
                    "breakingChanges": {"1.0.0": "Description", "2.0.0": "Description"}
                }
            },
            migration_guide_file_path=tmp_path / "migration_guide.md",
        )
        connector.migration_guide_file_path.write_text(
            "# Test Connector Migration Guide\n"
            "## Upgrading to 2.1.0\n"
            "Non-breaking informational note.\n"
            "## Upgrading to 1.0.0\n"
            "Breaking change details.\n"
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.FAILED
        assert "is missing headings for breaking changes" in result.message

    def test_fail_when_all_headings_out_of_order_with_extra(self, tmp_path):
        """All version headings must be in descending order, including non-breaking ones."""
        connector = Mock(
            name_from_metadata="Test Connector",
            technical_name="test-connector",
            metadata={
                "releases": {
                    "breakingChanges": {"1.0.0": "Description", "2.0.0": "Description"}
                }
            },
            migration_guide_file_path=tmp_path / "migration_guide.md",
        )
        connector.migration_guide_file_path.write_text(
            "# Test Connector Migration Guide\n"
            "## Upgrading to 2.1.0\n"
            "Non-breaking informational note.\n"
            "## Upgrading to 1.0.0\n"
            "Breaking change details.\n"
            "## Upgrading to 2.0.0\n"
            "Breaking change details.\n"
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.FAILED
        assert "has version headings out of descending order" in result.message

    def test_pass_with_multiple_extra_headings_interspersed(self, tmp_path):
        """Multiple extra non-breaking headings interspersed with breaking ones should pass."""
        connector = Mock(
            name_from_metadata="Test Connector",
            technical_name="test-connector",
            metadata={
                "releases": {
                    "breakingChanges": {
                        "1.0.0": "Description",
                        "2.0.0": "Description",
                        "3.0.0": "Description",
                    }
                }
            },
            migration_guide_file_path=tmp_path / "migration_guide.md",
        )
        connector.migration_guide_file_path.write_text(
            "# Test Connector Migration Guide\n"
            "## Upgrading to 3.1.0\n"
            "Non-breaking note.\n"
            "## Upgrading to 3.0.0\n"
            "Breaking change.\n"
            "## Upgrading to 2.5.0\n"
            "Non-breaking note.\n"
            "## Upgrading to 2.0.0\n"
            "Breaking change.\n"
            "## Upgrading to 1.5.0\n"
            "Non-breaking note.\n"
            "## Upgrading to 1.0.0\n"
            "Breaking change.\n"
        )

        result = CheckMigrationGuide()._run(connector)

        assert result.status == CheckStatus.PASSED
        assert "The migration guide is correctly templated" in result.message
