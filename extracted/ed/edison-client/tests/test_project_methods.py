import json
from collections.abc import Generator
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, PropertyMock, patch
from uuid import uuid4

import httpx
import pytest

from edison_client.clients.rest_client import ProjectError, RestClient

_Harness = tuple[RestClient, MagicMock]


def _stub_response(status_code: int, payload: dict | None = None) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.text = json.dumps(payload or {})
    response.json.return_value = payload or {}
    if status_code >= 400:
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            f"{status_code}", request=MagicMock(), response=response
        )
    else:
        response.raise_for_status.return_value = None
    return response


@contextmanager
def _make_client(response: MagicMock) -> Generator[_Harness, None, None]:
    async_client = MagicMock(spec=httpx.AsyncClient)
    async_client.get = AsyncMock(return_value=response)
    async_client.patch = AsyncMock(return_value=response)
    async_client.post = AsyncMock(return_value=response)

    with (
        patch(
            "edison_client.clients.rest_client.RestClient._fetch_my_orgs",
            return_value=["FutureHouse"],
        ),
        patch(
            "edison_client.clients.rest_client.RestClient.async_client",
            new_callable=PropertyMock,
        ) as async_prop,
    ):
        async_prop.return_value = async_client
        client = RestClient(api_key="test-key", cleanup_on_exit=False)
        yield client, async_client


class TestAgetProject:
    @pytest.mark.asyncio
    async def test_returns_row(self):
        project_id = uuid4()
        payload = {"id": str(project_id), "name": "demo", "metadata": None}
        with _make_client(_stub_response(200, payload)) as (client, async_client):
            assert await client.aget_project(project_id) == payload
            async_client.get.assert_awaited_once_with(f"/v0.1/projects/{project_id}")

    @pytest.mark.asyncio
    async def test_404_maps_to_not_found(self):
        with (
            _make_client(_stub_response(404)) as (client, _),
            pytest.raises(ProjectError, match="not found"),
        ):
            await client.aget_project(uuid4())

    @pytest.mark.asyncio
    async def test_403_maps_to_permission(self):
        with (
            _make_client(_stub_response(403)) as (client, _),
            pytest.raises(ProjectError, match="Permission denied"),
        ):
            await client.aget_project(uuid4())


class TestAupdateProject:
    @pytest.mark.asyncio
    async def test_name_only_rename_omits_metadata(self):
        project_id = uuid4()
        with _make_client(_stub_response(202)) as (client, async_client):
            await client.aupdate_project(project_id, name="renamed")
            async_client.patch.assert_awaited_once_with(
                f"/v0.1/projects/{project_id}", json={"name": "renamed"}
            )

    @pytest.mark.asyncio
    async def test_sends_metadata_when_given(self):
        project_id = uuid4()
        metadata = {"agent": "kosmos", "description": "new"}
        with _make_client(_stub_response(202)) as (client, async_client):
            await client.aupdate_project(project_id, name="renamed", metadata=metadata)
            async_client.patch.assert_awaited_once_with(
                f"/v0.1/projects/{project_id}",
                json={"name": "renamed", "metadata": metadata},
            )

    @pytest.mark.asyncio
    async def test_404_maps_to_not_found(self):
        with (
            _make_client(_stub_response(404)) as (client, _),
            pytest.raises(ProjectError, match="not found"),
        ):
            await client.aupdate_project(uuid4(), name="x")

    @pytest.mark.asyncio
    async def test_403_maps_to_permission(self):
        with (
            _make_client(_stub_response(403)) as (client, _),
            pytest.raises(ProjectError, match="Permission denied"),
        ):
            await client.aupdate_project(uuid4(), name="x")


class TestAcreateProjectHandoff:
    @pytest.mark.asyncio
    async def test_handoff_message_sent_in_body(self):
        persona_id = uuid4()
        project_id = uuid4()
        with _make_client(_stub_response(201, {"id": str(project_id)})) as (
            client,
            async_client,
        ):
            result = await client.acreate_project(
                name="spinoff",
                persona_id=persona_id,
                handoff_message="context to carry over",
            )
            assert result == project_id
            args, kwargs = async_client.post.await_args
            assert args[0] == f"/v0.1/personas/{persona_id}/projects"
            assert kwargs["json"]["handoff_message"] == "context to carry over"

    @pytest.mark.asyncio
    async def test_handoff_message_requires_persona_id(self):
        with (
            _make_client(_stub_response(201, {})) as (client, _),
            pytest.raises(ValueError, match="persona_id"),
        ):
            await client.acreate_project(name="spinoff", handoff_message="context")

    @pytest.mark.asyncio
    async def test_no_handoff_message_omits_field(self):
        persona_id = uuid4()
        project_id = uuid4()
        with _make_client(_stub_response(201, {"id": str(project_id)})) as (
            client,
            async_client,
        ):
            await client.acreate_project(name="spinoff", persona_id=persona_id)
            _, kwargs = async_client.post.await_args
            assert "handoff_message" not in kwargs["json"]
            assert "job_name" not in kwargs["json"]


class TestAcreateProjectJobName:
    @pytest.mark.asyncio
    async def test_job_name_sent_in_body(self):
        persona_id = uuid4()
        project_id = uuid4()
        with _make_client(_stub_response(201, {"id": str(project_id)})) as (
            client,
            async_client,
        ):
            result = await client.acreate_project(
                name="spinoff",
                persona_id=persona_id,
                job_name="job-futurehouse-data-analysis-chat",
            )
            assert result == project_id
            args, kwargs = async_client.post.await_args
            assert args[0] == f"/v0.1/personas/{persona_id}/projects"
            assert kwargs["json"]["job_name"] == "job-futurehouse-data-analysis-chat"

    @pytest.mark.asyncio
    async def test_job_name_requires_persona_id(self):
        with (
            _make_client(_stub_response(201, {})) as (client, _),
            pytest.raises(ValueError, match="persona_id"),
        ):
            await client.acreate_project(
                name="spinoff",
                job_name="job-futurehouse-data-analysis-chat",
            )
