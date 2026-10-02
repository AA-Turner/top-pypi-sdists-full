from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.marketplace_image_dto_docker_tags_detail_item import MarketplaceImageDtoDockerTagsDetailItem





T = TypeVar("T", bound="MarketplaceImageDto")



@_attrs_define
class MarketplaceImageDto:
    """ A Docker image published in the marketplace for reuse across environments.

        Example:
            {'id': 'd1effba4-1efa-47b2-8032-d041e3f0d03c', 'imageRepo': 'us-central1-docker.pkg.dev/example-
                project/marketplace/swe-bench-verified', 'description': 'SWE-bench Verified harness image — runs agentic patch-
                and-test rollouts against 500 human-verified GitHub issues.', 'dockerTags': ['latest', 'v1.2.0', 'v1.1.0'],
                'dockerTagsDetail': [{'tag': 'latest', 'sizeBytes': 5368709120, 'pushedAt': '2026-01-16T14:20:00.000Z'}, {'tag':
                'v1.2.0', 'sizeBytes': 5368709120, 'pushedAt': '2026-01-16T14:20:00.000Z'}], 'imageSizeBytes': 10737418240,
                'lastPushedAt': '2026-01-16T14:20:00.000Z', 'registry': 'us-central1-docker.pkg.dev', 'syncedAt':
                '2026-01-16T15:00:00.000Z', 'createdAt': '2026-01-15T09:30:00.000Z', 'updatedAt': '2026-01-16T15:00:00.000Z'}

        Attributes:
            id (UUID): Stable marketplace-image identifier (UUID).
            image_repo (str): Repository path of the image.
            description (str): Description of the marketplace image.
            docker_tags (list[str]): All tag names available for this image.
            docker_tags_detail (list[MarketplaceImageDtoDockerTagsDetailItem]): Per-tag detail including size and push time.
            image_size_bytes (float): Total cumulative size across all tags of this image in bytes. Example: 5368709120.
            last_pushed_at (None | str): Timestamp when any tag of this image was most recently pushed (ISO-8601, UTC). Null
                if no tags have been pushed.
            registry (str): Container registry host serving the image.
            synced_at (str): Timestamp when this image was last synced from the upstream registry (ISO-8601, UTC).
            created_at (str): Timestamp when the marketplace entry was created (ISO-8601, UTC).
            updated_at (str): Timestamp when the marketplace entry was last updated (ISO-8601, UTC).
     """

    id: UUID
    image_repo: str
    description: str
    docker_tags: list[str]
    docker_tags_detail: list[MarketplaceImageDtoDockerTagsDetailItem]
    image_size_bytes: float
    last_pushed_at: None | str
    registry: str
    synced_at: str
    created_at: str
    updated_at: str





    def to_dict(self) -> dict[str, Any]:
        from ..models.marketplace_image_dto_docker_tags_detail_item import MarketplaceImageDtoDockerTagsDetailItem # noqa: PLC0415
        id = str(self.id)

        image_repo = self.image_repo

        description = self.description

        docker_tags = self.docker_tags



        docker_tags_detail = []
        for docker_tags_detail_item_data in self.docker_tags_detail:
            docker_tags_detail_item = docker_tags_detail_item_data.to_dict()
            docker_tags_detail.append(docker_tags_detail_item)



        image_size_bytes = self.image_size_bytes

        last_pushed_at: None | str
        last_pushed_at = self.last_pushed_at

        registry = self.registry

        synced_at = self.synced_at

        created_at = self.created_at

        updated_at = self.updated_at


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "imageRepo": image_repo,
            "description": description,
            "dockerTags": docker_tags,
            "dockerTagsDetail": docker_tags_detail,
            "imageSizeBytes": image_size_bytes,
            "lastPushedAt": last_pushed_at,
            "registry": registry,
            "syncedAt": synced_at,
            "createdAt": created_at,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.marketplace_image_dto_docker_tags_detail_item import MarketplaceImageDtoDockerTagsDetailItem # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        image_repo = d.pop("imageRepo")

        description = d.pop("description")

        docker_tags = cast(list[str], d.pop("dockerTags"))


        docker_tags_detail = []
        _docker_tags_detail = d.pop("dockerTagsDetail")
        for docker_tags_detail_item_data in (_docker_tags_detail):
            docker_tags_detail_item = MarketplaceImageDtoDockerTagsDetailItem.from_dict(docker_tags_detail_item_data)



            docker_tags_detail.append(docker_tags_detail_item)


        image_size_bytes = d.pop("imageSizeBytes")

        def _parse_last_pushed_at(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_pushed_at = _parse_last_pushed_at(d.pop("lastPushedAt"))


        registry = d.pop("registry")

        synced_at = d.pop("syncedAt")

        created_at = d.pop("createdAt")

        updated_at = d.pop("updatedAt")

        marketplace_image_dto = cls(
            id=id,
            image_repo=image_repo,
            description=description,
            docker_tags=docker_tags,
            docker_tags_detail=docker_tags_detail,
            image_size_bytes=image_size_bytes,
            last_pushed_at=last_pushed_at,
            registry=registry,
            synced_at=synced_at,
            created_at=created_at,
            updated_at=updated_at,
        )

        return marketplace_image_dto

