"""Scene class managing all scenes."""

import logging

from aiopvapi.resources.scene_member import SceneMember
from aiopvapi.helpers.aiorequest import AioRequest
from aiopvapi.helpers.api_base import ApiResource
from aiopvapi.helpers.constants import (
    ATTR_ROOM_ID,
    ATTR_ROOM_IDS,
    ATTR_SCENE,
    ATTR_SCENE_ID,
    ATTR_SHADE_IDS,
)
from aiopvapi.helpers.tools import join_path

_LOGGER = logging.getLogger(__name__)


class Scene(ApiResource):
    """Powerview Scene class."""

    api_endpoint = "scenes"

    def __init__(
        self,
        raw_data: dict,
        request: AioRequest,
        scene_members: dict[SceneMember] | None = None,
    ) -> None:
        """Initialize the scene."""
        if ATTR_SCENE in raw_data:
            raw_data = raw_data.get(ATTR_SCENE)
        super().__init__(request, self.api_endpoint, raw_data)
        # For v2: pre-filter scene members belonging to this scene and
        # store shade ids here since v2 doesn't return shade ids in the scene data
        self._scene_members = scene_members

    @property
    def shade_ids(self) -> list[int]:
        """Return shade ids for the scene."""
        if self.api_version >= 3:
            return self._raw_data.get(ATTR_SHADE_IDS, [])

        # account for creation of object with no scene members data
        # (e.g. when creating a new scene and not passing the object)
        if not self._scene_members:
            return []

        # For v2, need to filter the scene members data to find shade ids for this scene
        return [
            member.shade_id
            for member in self._scene_members.values()
            if member.scene_id == self.id
        ]

    @property
    def room_id(self) -> list[int]:
        """Return the id of room(s) associated with this scene."""
        if self.api_version >= 3:
            return self._raw_data.get(ATTR_ROOM_IDS, [])
        return [self._raw_data.get(ATTR_ROOM_ID)]

    async def activate(self) -> list[int]:
        """Activate this scene."""
        if self.request.api_version >= 3:
            resource_path = join_path(self.base_path, str(self.id), "activate")
            _val = await self.request.put(resource_path)
        else:
            _val = await self.request.get(
                self.base_path, params={ATTR_SCENE_ID: self._id}
            )
            # v2 returns format {'shadeIds': ids} so flattening the list to align v3
            _val = _val.get(ATTR_SHADE_IDS)
        # should return an array of ID's that belong to the scene
        return _val
