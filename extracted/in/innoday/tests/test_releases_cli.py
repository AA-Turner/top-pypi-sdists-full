"""
Tests for `innoday releases create`/`update` CLI commands.

Mocks InnoDayAPIClient.get/post/patch directly rather than hitting a real
API -- these tests are about ReleasesCommands' own logic (409-fallback,
version->id resolution for update, body construction), not the router.
"""

import argparse
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.cli.commands.releases import ReleasesCommands


def _args(**overrides):
    defaults = dict(
        version="v1.0.0",
        org_id=None,
        project_id="proj-1",
        name=None,
        status="planned",
        released_at=None,
        notes=None,
        summary=None,
        changelog_json=None,
        if_exists="fail",
        format="table",
    )
    defaults.update(overrides)
    return argparse.Namespace(**defaults)


def _config():
    config = MagicMock()
    config.get_current_organization.return_value = "acme"
    config.get_organization_id.return_value = "org-1"
    config.get_current_project_id.return_value = "proj-1"
    return config


def _response(status_code, json_body=None, text=""):
    resp = MagicMock()
    resp.status_code = status_code
    resp.json.return_value = json_body or {}
    resp.text = text
    return resp


class TestReleasesCreate:
    @pytest.mark.asyncio
    async def test_create_success(self):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.post = AsyncMock(
                return_value=_response(201, {"version": "v1.0.0", "status": "planned"})
            )
            client.close = AsyncMock()

            result = await ReleasesCommands._handle_create(_args(), config)

        assert result == 0
        client.post.assert_called_once()
        endpoint, kwargs = client.post.call_args
        assert "/organizations/org-1/releases" == endpoint[0]
        assert kwargs["json"]["version"] == "v1.0.0"
        assert kwargs["json"]["project_id"] == "proj-1"

    @pytest.mark.asyncio
    async def test_create_success_json_format_prints_structured_output(self, capsys):
        """Programmatic callers (e.g. blastoff shelling out to this CLI) need
        reliable structured output, not rich-formatted text with emoji."""
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.post = AsyncMock(
                return_value=_response(
                    201, {"id": "release-1", "version": "v1.0.0", "status": "planned"}
                )
            )
            client.close = AsyncMock()

            result = await ReleasesCommands._handle_create(_args(format="json"), config)

        assert result == 0
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["id"] == "release-1"
        assert parsed["version"] == "v1.0.0"

    @pytest.mark.asyncio
    async def test_create_conflict_without_if_exists_fails(self):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.post = AsyncMock(return_value=_response(409))
            client.close = AsyncMock()

            result = await ReleasesCommands._handle_create(_args(), config)

        assert result == 1

    @pytest.mark.asyncio
    async def test_create_conflict_with_if_exists_update_patches_instead(self):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.post = AsyncMock(return_value=_response(409))
            client.get = AsyncMock(
                return_value=_response(200, {"id": "release-1", "version": "v1.0.0"})
            )
            client.patch = AsyncMock(
                return_value=_response(200, {"version": "v1.0.0", "status": "planned"})
            )
            client.close = AsyncMock()

            result = await ReleasesCommands._handle_create(
                _args(if_exists="update"), config
            )

        assert result == 0
        client.patch.assert_called_once()
        endpoint = client.patch.call_args[0][0]
        assert endpoint == "/organizations/org-1/releases/release-1"

    @pytest.mark.asyncio
    async def test_create_invalid_changelog_json_fails_before_any_request(self):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.post = AsyncMock()

            result = await ReleasesCommands._handle_create(
                _args(changelog_json="{not valid json"), config
            )

        assert result == 1
        client.post.assert_not_called()


class TestReleasesUpdate:
    @pytest.mark.asyncio
    async def test_update_resolves_version_to_id_then_patches(self):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.get = AsyncMock(
                return_value=_response(200, {"id": "release-1", "version": "v1.0.0"})
            )
            client.patch = AsyncMock(
                return_value=_response(200, {"version": "v1.0.0", "status": "released"})
            )
            client.close = AsyncMock()

            result = await ReleasesCommands._handle_update(
                _args(status="released"), config
            )

        assert result == 0
        client.patch.assert_called_once()
        endpoint, kwargs = client.patch.call_args
        assert endpoint[0] == "/organizations/org-1/releases/release-1"
        assert kwargs["json"]["status"] == "released"

    @pytest.mark.asyncio
    async def test_update_success_json_format_prints_structured_output(self, capsys):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.get = AsyncMock(
                return_value=_response(200, {"id": "release-1", "version": "v1.0.0"})
            )
            client.patch = AsyncMock(
                return_value=_response(
                    200, {"id": "release-1", "version": "v1.0.0", "status": "released"}
                )
            )
            client.close = AsyncMock()

            result = await ReleasesCommands._handle_update(
                _args(status="released", format="json"), config
            )

        assert result == 0
        captured = capsys.readouterr()
        parsed = json.loads(captured.out)
        assert parsed["id"] == "release-1"
        assert parsed["status"] == "released"

    @pytest.mark.asyncio
    async def test_update_no_fields_fails_before_any_request(self):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.get = AsyncMock()

            result = await ReleasesCommands._handle_update(_args(status=None), config)

        assert result == 1
        client.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_unknown_version_returns_error(self):
        config = _config()
        with patch("src.cli.commands.releases.InnoDayAPIClient") as MockClient:
            client = MockClient.return_value
            client.get = AsyncMock(return_value=_response(404))
            client.close = AsyncMock()

            result = await ReleasesCommands._handle_update(
                _args(status="released"), config
            )

        assert result == 1
