from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.cloud_agent_runtime_reference_type import CloudAgentRuntimeReferenceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="CloudAgentRuntimeReference")


@_attrs_define
class CloudAgentRuntimeReference:
    """
    Attributes:
        type_ (CloudAgentRuntimeReferenceType):
        image_id (str | Unset):
        checkpoint_id (str | Unset):
        id (str | Unset):
    """

    type_: CloudAgentRuntimeReferenceType
    image_id: str | Unset = UNSET
    checkpoint_id: str | Unset = UNSET
    id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        image_id = self.image_id

        checkpoint_id = self.checkpoint_id

        id = self.id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
            }
        )
        if image_id is not UNSET:
            field_dict["image_id"] = image_id
        if checkpoint_id is not UNSET:
            field_dict["checkpoint_id"] = checkpoint_id
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = CloudAgentRuntimeReferenceType(d.pop("type"))

        image_id = d.pop("image_id", UNSET)

        checkpoint_id = d.pop("checkpoint_id", UNSET)

        id = d.pop("id", UNSET)

        cloud_agent_runtime_reference = cls(
            type_=type_,
            image_id=image_id,
            checkpoint_id=checkpoint_id,
            id=id,
        )

        return cloud_agent_runtime_reference
