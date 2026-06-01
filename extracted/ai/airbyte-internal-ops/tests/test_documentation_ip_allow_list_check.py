from unittest.mock import Mock

import pytest

from airbyte_ops_mcp.connector_ops.utils import ConnectorLanguage
from airbyte_ops_mcp.connector_qa.checks.documentation.documentation import (
    CheckDocumentationHeadersOrder,
    CheckIpAllowListSectionContent,
)
from airbyte_ops_mcp.connector_qa.models import CheckStatus


def _connector(documentation, tmp_path, connector_type="source"):
    documentation_file_path = tmp_path / "example.md"
    documentation_file_path.write_text(documentation)
    connector = Mock()
    connector.ab_internal_sl = 300
    connector.cloud_usage = None
    connector.connector_type = connector_type
    connector.documentation_file_path = documentation_file_path
    connector.is_released = False
    connector.language = ConnectorLanguage.PYTHON
    connector.metadata = {"name": "Example"}
    connector.name_from_metadata = "Example"
    connector.support_level = None
    return connector


@pytest.mark.parametrize(
    "documentation,expected_status,expected_message",
    [
        pytest.param(
            """# Example

## Prerequisites

## Setup guide

## Set up Example

## IP allow list

If you use Airbyte Cloud and your organization restricts access to specific IPs, add the [Airbyte Cloud IP addresses](https://docs.airbyte.com/platform/operating-airbyte/ip-allowlist) to your allow list.

## Changelog

<details>
  <summary>Expand to review</summary>
</details>
""",
            CheckStatus.PASSED,
            "Documentation guidelines are followed",
            id="required_section_present",
        ),
        pytest.param(
            """# Example

## Prerequisites

## Setup guide

## Set up Example

## Changelog

<details>
  <summary>Expand to review</summary>
</details>
""",
            CheckStatus.FAILED,
            "Documentation does not have IP allow list section",
            id="required_section_missing",
        ),
    ],
)
def test_ip_allow_list_section_content(
    tmp_path, documentation, expected_status, expected_message
):
    connector = _connector(documentation, tmp_path)

    result = CheckIpAllowListSectionContent().run(connector)

    assert result.status == expected_status
    assert expected_message in result.message


def test_ip_allow_list_section_content_skips_destinations(tmp_path):
    connector = _connector(
        """# Example

## Changelog

<details>
  <summary>Expand to review</summary>
</details>
""",
        tmp_path,
        connector_type="destination",
    )

    result = CheckIpAllowListSectionContent().run(connector)

    assert result.status == CheckStatus.SKIPPED
    assert "Check does not apply to destination connectors" in result.message


def test_ip_allow_list_header_is_required_before_changelog(tmp_path):
    connector = _connector(
        """# Example

## Prerequisites

## Setup guide

## Set up Example

## Supported sync modes

## Supported Streams

## Changelog

<details>
  <summary>Expand to review</summary>
</details>
""",
        tmp_path,
    )

    errors = CheckDocumentationHeadersOrder().check_headers(connector)

    assert any("IP allow list" in error for error in errors)
