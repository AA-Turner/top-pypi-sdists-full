"""Tests for the admin-only clone methods on RestClient."""

from collections.abc import Generator
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import httpx
import pytest

from edison_client.clients.clone_methods import (
    CloneError,
    CloneInvalidRequestError,
    CloneMethods,
    CloneNotFoundError,
    ClonePermissionError,
)
from edison_client.clients.rest_client import RestClient
from edison_client.models.clone import (
    ChatCloneResponse,
    ProjectCloneResponse,
)
from edison_client.models.rest import ContentLocation, WorldModel


class _StubCloneClient(CloneMethods):
    """Bare CloneMethods with mocked sync/async clients for unit tests."""

    def __init__(self, response: MagicMock):
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
    def test_clone_project_404_maps_to_not_found(self):
        clone = _StubCloneClient(_stub_response(404))
        with pytest.raises(CloneNotFoundError):
            clone.clone_project(uuid4(), name="vibe-bench")

    def test_clone_project_403_maps_to_permission(self):
        clone = _StubCloneClient(_stub_response(403))
        with pytest.raises(ClonePermissionError):
            clone.clone_project(uuid4(), name="vibe-bench")

    def test_clone_project_unexpected_status_maps_to_base_error(self):
        clone = _StubCloneClient(_stub_response(418))
        with pytest.raises(CloneError) as exc_info:
            clone.clone_project(uuid4(), name="vibe-bench")
        assert not isinstance(
            exc_info.value,
            CloneNotFoundError | ClonePermissionError | CloneInvalidRequestError,
        )

    def test_clone_chat_422_maps_to_invalid_request(self):
        clone = _StubCloneClient(_stub_response(422))
        with pytest.raises(CloneInvalidRequestError):
            clone.clone_chat(uuid4(), uuid4())

    def test_clone_chat_404_maps_to_not_found(self):
        clone = _StubCloneClient(_stub_response(404))
        with pytest.raises(CloneNotFoundError):
            clone.clone_chat(uuid4(), uuid4())

    @pytest.mark.asyncio
    async def test_aclone_project_404_maps_to_not_found(self):
        clone = _StubCloneClient(_stub_response(404))
        with pytest.raises(CloneNotFoundError):
            await clone.aclone_project(uuid4(), name="vibe-bench")

    @pytest.mark.asyncio
    async def test_aclone_chat_422_maps_to_invalid_request(self):
        clone = _StubCloneClient(_stub_response(422))
        with pytest.raises(CloneInvalidRequestError):
            await clone.aclone_chat(uuid4(), uuid4())


class TestCloneRequestShape:
    def test_clone_project_posts_to_admin_route_with_name(self):
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

    def test_clone_chat_serializes_uuid_keys(self):
        source_session = uuid4()
        target_project = uuid4()
        old_wm, new_wm = uuid4(), uuid4()
        new_session = uuid4()
        clone = _StubCloneClient(
            _stub_response(
                200,
                {"session_id": str(new_session), "message_count": 7},
            )
        )

        result = clone.clone_chat(
            source_session,
            target_project,
            limit=5,
            world_model_id_map={old_wm: new_wm},
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


@pytest.fixture(name="source_project")
def fixture_source_project(
    admin_client: RestClient,
) -> Generator[UUID, None, None]:
    """Create a source project we can clone, plus a workspace it requires."""
    project_id = admin_client.create_project(f"clone-src-{uuid4()}")
    admin_client.create_workspace(name=f"ws-{uuid4()}", project_id=project_id)
    yield project_id
    admin_client.delete_project(project_id)


class TestProjectCloneLive:
    """Round-trip a project clone against the dev backend and re-fetch it."""

    @pytest.mark.live
    @pytest.mark.timeout(120)
    def test_clone_project_round_trip(
        self, admin_client: RestClient, source_project: UUID
    ):
        source_wm_id = admin_client.create_world_model(
            WorldModel(
                content="seed content for clone test",
                content_location=ContentLocation.INLINE,
                name=f"clone-src-wm-{uuid4()}",
                description="source wm for clone test",
                project_id=source_project,
            )
        )

        cloned: UUID | None = None
        try:
            result = admin_client.clone_project(source_project, name="cloned for test")
            cloned = result.project_id

            assert result.project_id != source_project
            assert source_wm_id in result.world_model_id_map
            new_wm_id = result.world_model_id_map[source_wm_id]
            assert new_wm_id != source_wm_id

            # The cloned world_model must report the new project_id.
            cloned_wm = admin_client.get_world_model(world_model_id=new_wm_id)
            assert cloned_wm.id == new_wm_id
            assert UUID(str(cloned_wm.project_id)) == result.project_id

            # And the source world_model is untouched.
            source_wm = admin_client.get_world_model(world_model_id=source_wm_id)
            assert UUID(str(source_wm.project_id)) == source_project
        finally:
            if cloned is not None:
                admin_client.delete_project(cloned)

    @pytest.mark.live
    @pytest.mark.timeout(120)
    @pytest.mark.asyncio
    async def test_aclone_project_round_trip(
        self, admin_client: RestClient, source_project: UUID
    ):
        result = await admin_client.aclone_project(
            source_project, name=f"clone-{uuid4()}"
        )
        try:
            assert result.project_id != source_project
        finally:
            await admin_client.adelete_project(result.project_id)


class TestChatCloneLive:
    @pytest.mark.live
    @pytest.mark.timeout(60)
    def test_clone_chat_missing_source_session_returns_404(
        self, admin_client: RestClient, source_project: UUID
    ):
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
