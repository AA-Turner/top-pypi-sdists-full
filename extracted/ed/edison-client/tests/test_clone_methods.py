"""Tests for the admin-only clone methods on RestClient."""

import json
import os
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import httpx
import pytest
import pytest_asyncio

from edison_client.clients.clone_methods import (
    CloneError,
    CloneInvalidRequestError,
    CloneMethods,
    CloneNotFoundError,
    ClonePermissionError,
)
from edison_client.clients.rest_client import ProjectError, RestClient
from edison_client.clients.workspace_methods import WorkspacePermissionError
from edison_client.models.clone import ChatCloneResponse, ProjectCloneResponse
from edison_client.models.rest import ContentLocation, WorldModel


class _StubCloneClient(CloneMethods):
    """Bare CloneMethods with mocked sync/async clients for unit tests."""

    def __init__(self, response: MagicMock) -> None:
        self._sync = MagicMock(spec=httpx.Client)
        self._sync.post.return_value = response
        self._async = MagicMock(spec=httpx.AsyncClient)
        self._async.post = AsyncMock(return_value=response)

    @property
    def client(self) -> httpx.Client:
        return self._sync

    @property
    def async_client(self) -> httpx.AsyncClient:
        return self._async


class TestCloneErrorMapping:
    def test_clone_project_404_maps_to_not_found(self) -> None:
        clone = _StubCloneClient(_stub_response(404))
        with pytest.raises(CloneNotFoundError):
            clone.clone_project(uuid4(), name="vibe-bench")

    def test_clone_project_403_maps_to_permission(self) -> None:
        clone = _StubCloneClient(_stub_response(403))
        with pytest.raises(ClonePermissionError):
            clone.clone_project(uuid4(), name="vibe-bench")

    def test_clone_project_unexpected_status_maps_to_base_error(self) -> None:
        clone = _StubCloneClient(_stub_response(418))
        with pytest.raises(CloneError) as exc_info:
            clone.clone_project(uuid4(), name="vibe-bench")
        assert not isinstance(
            exc_info.value,
            CloneNotFoundError | ClonePermissionError | CloneInvalidRequestError,
        )

    def test_clone_chat_422_maps_to_invalid_request(self) -> None:
        clone = _StubCloneClient(_stub_response(422))
        with pytest.raises(CloneInvalidRequestError):
            clone.clone_chat(uuid4(), uuid4())

    def test_clone_chat_404_maps_to_not_found(self) -> None:
        clone = _StubCloneClient(_stub_response(404))
        with pytest.raises(CloneNotFoundError):
            clone.clone_chat(uuid4(), uuid4())

    @pytest.mark.asyncio
    async def test_aclone_project_404_maps_to_not_found(self) -> None:
        clone = _StubCloneClient(_stub_response(404))
        with pytest.raises(CloneNotFoundError):
            await clone.aclone_project(uuid4(), name="vibe-bench")

    @pytest.mark.asyncio
    async def test_aclone_chat_422_maps_to_invalid_request(self) -> None:
        clone = _StubCloneClient(_stub_response(422))
        with pytest.raises(CloneInvalidRequestError):
            await clone.aclone_chat(uuid4(), uuid4())


class TestCloneRequestShape:
    def test_clone_project_posts_to_admin_route_with_name(self) -> None:
        project_id = uuid4()
        new_project_id = uuid4()
        chat_project_id = uuid4()
        clone = _StubCloneClient(
            _stub_response(
                200,
                {
                    "project_id": str(new_project_id),
                    "chat_project_id": str(chat_project_id),
                    "world_model_id_map": {},
                },
            )
        )

        result = clone.clone_project(project_id, name="vibe-bench")

        assert isinstance(result, ProjectCloneResponse)
        assert result.project_id == new_project_id
        assert result.chat_project_id == chat_project_id, (
            "chat writes go to the cloned persona's child, not its workspace root"
        )
        clone._sync.post.assert_called_once()
        args, kwargs = clone._sync.post.call_args
        assert args[0] == f"/v0.1/admin/projects/{project_id}/clone"
        assert kwargs["json"] == {"name": "vibe-bench"}

    def test_clone_chat_serializes_uuid_keys(self) -> None:
        source_session = uuid4()
        target_project = uuid4()
        old_wm, new_wm = uuid4(), uuid4()
        new_session = uuid4()
        clone = _StubCloneClient(
            _stub_response(200, {"session_id": str(new_session), "message_count": 7})
        )

        result = clone.clone_chat(
            source_session, target_project, limit=5, world_model_id_map={old_wm: new_wm}
        )

        assert isinstance(result, ChatCloneResponse)
        assert result.session_id == new_session
        assert result.message_count == 7
        _, kwargs = clone._sync.post.call_args
        body = kwargs["json"]
        assert body["source_session_id"] == str(source_session)
        assert body["target_project_id"] == str(target_project)
        assert body["limit"] == 5
        assert body["world_model_id_map"] == {str(old_wm): str(new_wm)}


# ---------------------------------------------------------------------------
# Live e2e tests against the dev backend.
# ---------------------------------------------------------------------------


class CloneTestResources:
    """Track API teardown and journal the IDs needed for filesystem cleanup."""

    def __init__(self, client: RestClient, stack: AsyncExitStack, path: Path) -> None:
        self.client = client
        self.stack = stack
        self.path = path
        self.seed_project_id = UUID(os.environ["EDISON_CLONE_SEED_PROJECT_ID"])
        self.persona_ids: list[UUID] = []
        self.workspace_ids: list[UUID] = []
        self.world_model_ids: list[UUID] = []
        self.save()

    def save(self) -> None:
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(
                {
                    "seed_project_id": str(self.seed_project_id),
                    "persona_ids": [str(id_) for id_ in self.persona_ids],
                    "workspace_ids": [str(id_) for id_ in self.workspace_ids],
                    "world_model_ids": [str(id_) for id_ in self.world_model_ids],
                },
                indent=2,
            )
            + "\n"
        )

        temporary.replace(self.path)

    def track_world_model(self, world_model_id: UUID) -> UUID:
        self.world_model_ids.append(world_model_id)
        self.stack.push_async_callback(self.client.delete_world_model, world_model_id)
        self.save()
        return world_model_id

    def track_clone(
        self, result: ProjectCloneResponse, *, name: str
    ) -> ProjectCloneResponse:
        self.persona_ids.append(result.project_id)
        self.save()
        project = self.client.get_project(result.project_id)
        if project["name"] != name or result.project_id == self.seed_project_id:
            raise ValueError("Refusing to clean up a clone with unexpected ownership")
        self.stack.push_async_callback(self.delete_clone, result)
        for world_model_id in result.world_model_id_map.values():
            self.track_world_model(world_model_id)
        # Resolve the workspace while the project still exists: deleting the
        # project clears the DSS association without deleting the workspace.
        response = self.client.client.get(
            f"/v0.1/data-storage/workspaces/by-project/{result.project_id}"
        )
        response.raise_for_status()
        workspace_id = UUID(response.json()["data_storage"]["id"])
        self.workspace_ids.append(workspace_id)
        self.stack.push_async_callback(self.client.adelete_workspace, workspace_id)
        self.save()
        # The clone route does not copy metadata to the child, so a second
        # clone cannot inherit the seed's marker. Tag each verified private root.
        self.client.update_project(
            result.project_id, metadata={"test_fixture": "edison-client-clone-tests-v1"}
        )
        return result

    async def delete_clone(self, result: ProjectCloneResponse) -> None:
        await self.client.adelete_project(result.project_id)
        # The persona FK cascades to children; assert the public API agrees.
        response = await self.client.async_client.get(
            f"/v0.1/projects/{result.chat_project_id}"
        )
        assert response.status_code == httpx.codes.NOT_FOUND, (
            f"Clone child {result.chat_project_id} survived persona deletion"
        )


@pytest.mark.parametrize("failure_stage", ["workspace_cleanup", "tagging"])
async def test_clone_teardown_cleans_recorded_resources_after_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, failure_stage: str
) -> None:
    seed_id, persona_id, chat_id, workspace_id, world_model_id = (
        uuid4() for _ in range(5)
    )
    monkeypatch.setenv("EDISON_CLONE_SEED_PROJECT_ID", str(seed_id))
    deleted = []

    def handle(request: httpx.Request) -> httpx.Response:
        if request.method == "GET":
            if request.url.path == f"/v0.1/projects/{chat_id}":
                return httpx.Response(404)
            if request.url.path == f"/v0.1/projects/{persona_id}":
                return httpx.Response(200, json={"name": "owned-clone"})
            return httpx.Response(200, json={"data_storage": {"id": str(workspace_id)}})
        if request.method == "PATCH":
            return httpx.Response(403 if failure_stage == "tagging" else 202)
        deleted.append(request.url.path)
        status = (
            403
            if failure_stage == "workspace_cleanup" and "workspaces" in request.url.path
            else 204
        )
        return httpx.Response(status)

    transport = httpx.MockTransport(handle)
    with httpx.Client(base_url="https://example.com", transport=transport) as sync:
        async with httpx.AsyncClient(
            base_url="https://example.com", transport=transport
        ) as async_client:
            monkeypatch.setattr(RestClient, "client", property(lambda _: sync))
            monkeypatch.setattr(
                RestClient, "async_client", property(lambda _: async_client)
            )
            client = RestClient(api_key="test-only-not-a-secret", cleanup_on_exit=False)
            manifest = tmp_path / "clone-resources.json"
            stack = AsyncExitStack()
            resources = CloneTestResources(client, stack, manifest)
            result = ProjectCloneResponse(
                project_id=persona_id,
                chat_project_id=chat_id,
                world_model_id_map={uuid4(): world_model_id},
            )
            if failure_stage == "tagging":
                with pytest.raises(ProjectError):
                    resources.track_clone(result, name="owned-clone")
                await stack.aclose()
            else:
                resources.track_clone(result, name="owned-clone")
                with pytest.raises(WorkspacePermissionError):
                    await stack.aclose()

    assert f"/v0.1/projects/{persona_id}" in deleted
    assert f"/v0.1/world-models/{world_model_id}" in deleted
    assert f"/v0.1/data-storage/workspaces/{workspace_id}" in deleted
    recorded = json.loads(manifest.read_text())
    assert recorded["workspace_ids"] == [str(workspace_id)]
    assert recorded["world_model_ids"] == [str(world_model_id)]


async def test_clone_tracker_refuses_to_delete_an_unowned_project(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    seed_id = uuid4()
    monkeypatch.setenv("EDISON_CLONE_SEED_PROJECT_ID", str(seed_id))
    requests = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request.method)
        return httpx.Response(200, json={"name": "shared-seed"})

    with httpx.Client(
        base_url="https://example.com", transport=httpx.MockTransport(handle)
    ) as sync:
        monkeypatch.setattr(RestClient, "client", property(lambda _: sync))
        client = RestClient(api_key="test-only-not-a-secret", cleanup_on_exit=False)
        async with AsyncExitStack() as stack:
            resources = CloneTestResources(
                client, stack, tmp_path / "clone-resources.json"
            )
            result = ProjectCloneResponse(project_id=uuid4(), chat_project_id=uuid4())
            with pytest.raises(ValueError, match="unexpected ownership"):
                resources.track_clone(result, name="my-private-clone")
    assert requests == ["GET"]


# The async test's aiohttp transport belongs to its function loop; teardown
# must use that same loop before pytest closes it.
@pytest_asyncio.fixture(name="clone_resources", loop_scope="function")
async def fixture_clone_resources(
    admin_client: RestClient, tmp_path: Path
) -> AsyncIterator[CloneTestResources]:
    async with AsyncExitStack() as stack:
        yield CloneTestResources(admin_client, stack, tmp_path / "clone-resources.json")


@pytest.fixture(name="source_project")
def fixture_source_project(clone_resources: CloneTestResources) -> UUID:
    """Copy an initialized seed; each test mutates only its own source."""
    name = f"sdk-clone-source-{uuid4()}"
    source = clone_resources.track_clone(
        clone_resources.client.clone_project(
            clone_resources.seed_project_id, name=name
        ),
        name=name,
    )
    return source.chat_project_id


class TestProjectCloneLive:
    """Round-trip a project clone against the dev backend and re-fetch it."""

    @pytest.mark.live
    @pytest.mark.timeout(120)
    def test_clone_project_round_trip(
        self,
        admin_client: RestClient,
        source_project: UUID,
        clone_resources: CloneTestResources,
    ) -> None:
        source_wm_id = clone_resources.track_world_model(
            admin_client.create_world_model(
                WorldModel(
                    content="seed content for clone test",
                    content_location=ContentLocation.INLINE,
                    name=f"clone-src-wm-{uuid4()}",
                    description="source wm for clone test",
                    project_id=source_project,
                )
            )
        )

        name = f"sdk-clone-target-{uuid4()}"
        result = clone_resources.track_clone(
            admin_client.clone_project(source_project, name=name), name=name
        )

        assert result.project_id != source_project
        assert source_wm_id in result.world_model_id_map
        new_wm_id = result.world_model_id_map[source_wm_id]
        assert new_wm_id != source_wm_id

        # The cloned world_model must report the new project_id.
        cloned_wm = admin_client.get_world_model(world_model_id=new_wm_id)
        assert UUID(str(cloned_wm.id)) == new_wm_id
        assert UUID(str(cloned_wm.project_id)) == result.project_id

        # And the source world_model is untouched.
        source_wm = admin_client.get_world_model(world_model_id=source_wm_id)
        assert UUID(str(source_wm.project_id)) == source_project

    @pytest.mark.live
    @pytest.mark.timeout(120)
    @pytest.mark.asyncio
    async def test_aclone_project_round_trip(
        self,
        admin_client: RestClient,
        source_project: UUID,
        clone_resources: CloneTestResources,
    ) -> None:
        name = f"sdk-clone-target-{uuid4()}"
        result = clone_resources.track_clone(
            await admin_client.aclone_project(source_project, name=name), name=name
        )
        assert result.project_id != source_project


class TestChatCloneLive:
    @pytest.mark.live
    @pytest.mark.timeout(60)
    def test_clone_chat_missing_source_session_returns_404(
        self, admin_client: RestClient, source_project: UUID
    ) -> None:
        with pytest.raises(CloneNotFoundError):
            admin_client.clone_chat(uuid4(), source_project)


def _stub_response(status_code: int, json_body: dict | None = None) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.text = "" if json_body is None else str(json_body)
    response.json.return_value = json_body
    if 200 <= status_code < 300:
        response.raise_for_status.return_value = None
    else:
        request = httpx.Request("POST", "https://example/test")
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "boom",
            request=request,
            response=httpx.Response(status_code, request=request),
        )
    return response
