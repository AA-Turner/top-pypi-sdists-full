# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for release block MCP helpers."""

from unittest.mock import patch

import requests

from airbyte_ops_mcp.mcp import release_block


class _Response:
    def __init__(
        self,
        *,
        status_code: int = 200,
        text: str = "",
        json_data: dict | None = None,
    ) -> None:
        self.status_code = status_code
        self.text = text
        self._json_data = json_data or {}

    def json(self) -> dict:
        return self._json_data

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


def test_check_single_connector_block_uses_explicit_ref() -> None:
    """Single connector checks fetch marker contents from the requested ref."""
    with patch(
        "airbyte_ops_mcp.mcp.release_block.get_file_contents_at_ref",
        return_value="reason: broken\nyanked_version: 1.2.3\n",
    ) as get_file_contents:
        result = release_block._check_single_connector_block(
            "source-faker",
            "token",
            "feature-branch",
        )

        get_file_contents.assert_called_once_with(
            owner="airbytehq",
            repo="airbyte",
            path="airbyte-integrations/connectors/source-faker/block-release.yaml",
            ref="feature-branch",
            token="token",
        )
    assert result == [
        {
            "connector_name": "source-faker",
            "reason": "broken",
            "yanked_version": "1.2.3",
            "blocked_at": None,
            "blocked_by": None,
        }
    ]


def test_search_all_blocked_connectors_can_return_names_only() -> None:
    """Names-only listings avoid fetching every marker file."""
    with patch(
        "airbyte_ops_mcp.mcp.release_block.get_file_contents_at_ref"
    ) as get_file_contents, patch(
        "airbyte_ops_mcp.mcp.release_block.requests.get",
        return_value=_Response(
            json_data={
                "tree": [
                    {
                        "path": "airbyte-integrations/connectors/source-faker/block-release.yaml"
                    },
                    {
                        "path": "airbyte-integrations/connectors/source-faker/metadata.yaml"
                    },
                ]
            }
        ),
    ) as requests_get:
        result = release_block._search_all_blocked_connectors(
            token="token",
            ref="feature/branch",
            include_details=False,
        )

        requests_get.assert_called_once_with(
            "https://api.github.com/repos/airbytehq/airbyte/git/trees/feature%2Fbranch",
            headers={
                "Authorization": "Bearer token",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            params={"recursive": "1"},
            timeout=30,
        )
        get_file_contents.assert_not_called()
    assert result == [{"connector_name": "source-faker"}]


def test_search_all_blocked_connectors_fetches_details_when_requested() -> None:
    """Detailed listings parse marker files found in the Git tree."""
    with patch(
        "airbyte_ops_mcp.mcp.release_block.requests.get",
        return_value=_Response(
            json_data={
                "tree": [
                    {
                        "path": "airbyte-integrations/connectors/source-faker/block-release.yaml"
                    }
                ]
            }
        ),
    ), patch(
        "airbyte_ops_mcp.mcp.release_block.get_file_contents_at_ref",
        return_value="reason: broken\nblocked_by: aj\n",
    ) as get_file_contents:
        result = release_block._search_all_blocked_connectors(
            token="token",
            ref="master",
            include_details=True,
        )

        get_file_contents.assert_called_once_with(
            owner="airbytehq",
            repo="airbyte",
            path="airbyte-integrations/connectors/source-faker/block-release.yaml",
            ref="master",
            token="token",
        )
    assert result == [
        {
            "connector_name": "source-faker",
            "reason": "broken",
            "yanked_version": None,
            "blocked_at": None,
            "blocked_by": "aj",
        }
    ]
