"""Test Scene capabilities."""

from unittest.mock import AsyncMock, Mock

from aiopvapi.helpers.aiorequest import AioRequest, PvApiResponseStatusError
from aiopvapi.resources.scene import Scene
import pytest

import base64

from .common import FAKE_BASE_URL, SCENE_RAW_DATA_V1_V2, SCENE_RAW_DATA_V3, scenes_json


def decode_name(value: str) -> str:
    """Decode base64 encoded name."""
    return base64.b64decode(value).decode("utf-8")


@pytest.fixture
def make_request():
    """Return a factory that builds a mock AioRequest for a given API version."""

    def _make_request(api_version: int) -> Mock:
        request = Mock(spec=AioRequest)
        request.hub_ip = FAKE_BASE_URL
        request.api_version = api_version
        request.api_path = "home" if api_version >= 3 else "api"
        return request

    return _make_request


@pytest.fixture
def make_scene(make_request):
    """Return a factory that builds a Scene for a given API version."""

    def _make_scene(api_version: int, raw_data: dict | None = None) -> Scene:
        if raw_data is None:
            raw_data = SCENE_RAW_DATA_V3 if api_version >= 3 else SCENE_RAW_DATA_V1_V2

        return Scene(raw_data, make_request(api_version))

    return _make_scene


@pytest.fixture
def make_scenes(make_scene):
    """Return a factory that builds all Scene objects for a given API version."""

    def _make_scenes(api_version: int) -> list[Scene]:
        data = scenes_json(api_version)

        if api_version >= 3:
            raw_scenes = data
        else:
            raw_scenes = data["sceneData"]

        return [make_scene(api_version, raw_scene) for raw_scene in raw_scenes]

    return _make_scenes


@pytest.mark.parametrize("api_version", [1, 2, 3])
def test_scene_count(api_version: int, make_scenes) -> None:
    """Test that expected number of scenes are returned for each API version."""
    scenes = make_scenes(api_version)

    assert len(scenes) == 18


@pytest.mark.parametrize("api_version", [1, 2, 3])
def test_scene_exists(api_version: int, make_scenes) -> None:
    """Test that specific scenes exist across API versions."""
    scenes = make_scenes(api_version)

    names = [scene.name for scene in scenes]
    assert "Open Study" in names


@pytest.mark.parametrize("api_version", [1, 2, 3])
def test_name_property(api_version: int, make_scenes) -> None:
    """Test that all scene names are correctly resolved."""
    scenes = make_scenes(api_version)

    for scene in scenes:
        raw = scene.raw_data

        if api_version >= 3:
            expected = raw["ptName"]
        else:
            expected = decode_name(raw["name"])

        assert scene.name == expected


@pytest.mark.parametrize("api_version", [1, 2, 3])
def test_room_id_property(api_version: int, make_scenes) -> None:
    """Test that scene room_id property returns correct value."""
    scenes = make_scenes(api_version)

    room_ids = [room_id for scene in scenes for room_id in scene.room_id]

    if api_version >= 3:
        expected = 298
    else:
        expected = 24002

    assert expected in room_ids


@pytest.mark.parametrize("api_version", [1, 2, 3])
def test_full_path(api_version: int, make_scene) -> None:
    """Test that scene base_path is correctly constructed."""
    scene = make_scene(api_version)

    assert scene.base_path == f"http://{FAKE_BASE_URL}/{scene.request.api_path}/scenes"


@pytest.mark.parametrize("api_version", [1, 2, 3])
def test_return_empty(api_version: int, make_scene) -> None:
    """Test that scene returns empty shade_ids."""
    scene = make_scene(api_version)

    assert scene.shade_ids == []


@pytest.mark.parametrize("api_version", [3])
def test_return_shade_ids(api_version: int, make_scene) -> None:
    """Test that API v3 scene returns shade_ids from raw data."""
    raw_data = {**SCENE_RAW_DATA_V3, "shadeIds": [1, 2, 3]}
    scene = make_scene(api_version, raw_data=raw_data)

    assert scene.shade_ids == [1, 2, 3]


@pytest.mark.asyncio
@pytest.mark.parametrize("api_version", [1, 2, 3])
async def test_activate_200(api_version: int, make_scene) -> None:
    """Test successful scene activation for supported API versions."""
    scene = make_scene(api_version)

    if api_version >= 3:
        scene.request.put = AsyncMock(return_value=[10])
    else:
        scene.request.get = AsyncMock(return_value={"shadeIds": [10]})

    resp = await scene.activate()

    assert resp[0] == 10


@pytest.mark.asyncio
@pytest.mark.parametrize("api_version", [1, 2, 3])
async def test_activate_404(api_version: int, make_scene) -> None:
    """Test scene activation failure raises PvApiResponseStatusError."""
    scene = make_scene(api_version)

    error = PvApiResponseStatusError("404 Not Found")

    if api_version == 3:
        scene.request.put = Mock(side_effect=error)
    else:
        scene.request.get = Mock(side_effect=error)

    with pytest.raises(PvApiResponseStatusError):
        await scene.activate()
