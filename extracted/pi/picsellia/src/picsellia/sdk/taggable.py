import logging
from abc import ABC, abstractmethod
from uuid import UUID

import orjson
from beartype import beartype
from deprecation import deprecated

from picsellia.decorators import exception_handler
from picsellia.sdk.connection import Connection
from picsellia.sdk.tag import Tag, TagTarget

logger = logging.getLogger("picsellia")


class Taggable(ABC):
    def __init__(self, target_type: TagTarget) -> None:
        self._target_type = target_type

    @property
    def target_type(self) -> TagTarget:
        return self._target_type

    @property
    @abstractmethod
    def ids(self) -> list[UUID]:
        pass

    @property
    @deprecated(
        deprecated_in="6.29.0",
        details="You should use connection property instead of this one.",
    )
    def connexion(self) -> Connection:
        """deprecated"""
        return self.connection

    @property
    @abstractmethod
    def connection(self) -> Connection:
        pass

    @exception_handler
    @beartype
    def add_tags(self, tags: Tag | list[Tag]) -> None:
        """Add some tags to an object.
        It can be used on Data/MultiData/Asset/MultiAsset/DatasetVersion/Dataset/Model/ModelVersion.

        You can give a Tag or a list of (Tag).

        Examples:
            ```python
            tag_bicycle = client.create_tag("bicycle", Target.DATA)
            tag_car = client.create_tag("car", Target.DATA)
            tag_truck = client.create_tag("truck", Target.DATA)

            data.add_tags(tag_bicycle)
            data.add_tags([tag_car, tag_truck])
            ```
        """
        if isinstance(tags, Tag):
            tags = [tags]

        assert tags != [], "Given tags are empty. They can't be empty"

        for tag in tags:
            assert tag.target_type == self.target_type, (
                f"Given tag ({tag.name}) is targeted on {tag.target_type}. It can't be added because on a {self.target_type} "
            )

        for tag in tags:
            payload = self.ids
            self.connection.post(
                f"/api/tag/{tag.id}/attach",
                data=orjson.dumps(payload),
            )
        logger.info(f"{len(tags)} tags added to {self}).")

    @exception_handler
    @beartype
    def remove_tags(self, tags: Tag | list[Tag]) -> None:
        """Remove some tags from an object (can be used on Data/Asset/DatasetVersion/Dataset/Model/ModelVersion)

        You can give a (Tag) or a list of (Tag).

        Examples:
            ```python
            data.remove_tags(tag_bicycle)
            data.remove_tags([tag_car, tag_truck])
            ```
        """
        if isinstance(tags, Tag):
            tags = [tags]

        assert tags != [], "Given tags are empty. They can't be empty"

        for tag in tags:
            assert tag.target_type == self._target_type, (
                f"Given tag ({tag.name}) can't be removed because it is not targeted on data"
            )

        for tag in tags:
            payload = self.ids
            self.connection.post(
                f"/api/tag/{tag.id}/detach",
                data=orjson.dumps(payload),
            )
        logger.info(f"{len(tags)} tags removed from {self}.")
