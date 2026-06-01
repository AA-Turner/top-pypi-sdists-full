# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
from airbyte_ops_mcp.connector_qa.checks.documentation.documentation import (
    CheckChangelogEntry,
    CheckChangelogSectionContent,
    CheckDocumentationExists,
    CheckDocumentationHeadersOrder,
    CheckDocumentationLinks,
    CheckForAirbyteCloudSectionContent,
    CheckForAirbyteOpenSectionContent,
    CheckIpAllowListSectionContent,
    CheckMigrationGuide,
    CheckPrerequisitesSectionDescribesRequiredFieldsFromSpec,
    CheckSourceSectionContent,
    CheckSupportedSyncModesSectionContent,
    CheckTutorialsSectionContent,
)

ENABLED_CHECKS = [
    CheckMigrationGuide(),
    CheckDocumentationExists(),
    CheckDocumentationLinks(),
    CheckDocumentationHeadersOrder(),
    CheckPrerequisitesSectionDescribesRequiredFieldsFromSpec(),
    CheckSourceSectionContent(),
    CheckForAirbyteCloudSectionContent(),
    CheckForAirbyteOpenSectionContent(),
    CheckSupportedSyncModesSectionContent(),
    CheckTutorialsSectionContent(),
    CheckIpAllowListSectionContent(),
    CheckChangelogSectionContent(),
    CheckChangelogEntry(),
]
