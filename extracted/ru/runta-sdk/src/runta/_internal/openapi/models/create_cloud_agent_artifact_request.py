from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateCloudAgentArtifactRequest")


@_attrs_define
class CreateCloudAgentArtifactRequest:
    """
    Attributes:
        run_id (str):
        name (str):
        content_base64 (str):
        media_type (str | Unset):
    """

    run_id: str
    name: str
    content_base64: str
    media_type: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        run_id = self.run_id

        name = self.name

        content_base64 = self.content_base64

        media_type = self.media_type

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "run_id": run_id,
                "name": name,
                "content_base64": content_base64,
            }
        )
        if media_type is not UNSET:
            field_dict["media_type"] = media_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        run_id = d.pop("run_id")

        name = d.pop("name")

        content_base64 = d.pop("content_base64")

        media_type = d.pop("media_type", UNSET)

        create_cloud_agent_artifact_request = cls(
            run_id=run_id,
            name=name,
            content_base64=content_base64,
            media_type=media_type,
        )

        return create_cloud_agent_artifact_request
