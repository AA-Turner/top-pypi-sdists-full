from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="CloudAgentArtifact")


@_attrs_define
class CloudAgentArtifact:
    """
    Attributes:
        id (str):
        run_id (str):
        harness_id (str):
        name (str):
        media_type (str):
        size (int):
        created_at (str):
        content_base64 (str | Unset):
    """

    id: str
    run_id: str
    harness_id: str
    name: str
    media_type: str
    size: int
    created_at: str
    content_base64: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        run_id = self.run_id

        harness_id = self.harness_id

        name = self.name

        media_type = self.media_type

        size = self.size

        created_at = self.created_at

        content_base64 = self.content_base64

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "run_id": run_id,
                "harness_id": harness_id,
                "name": name,
                "media_type": media_type,
                "size": size,
                "created_at": created_at,
            }
        )
        if content_base64 is not UNSET:
            field_dict["content_base64"] = content_base64

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        run_id = d.pop("run_id")

        harness_id = d.pop("harness_id")

        name = d.pop("name")

        media_type = d.pop("media_type")

        size = d.pop("size")

        created_at = d.pop("created_at")

        content_base64 = d.pop("content_base64", UNSET)

        cloud_agent_artifact = cls(
            id=id,
            run_id=run_id,
            harness_id=harness_id,
            name=name,
            media_type=media_type,
            size=size,
            created_at=created_at,
            content_base64=content_base64,
        )

        return cloud_agent_artifact
