from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.cloud_agent_prompt_image_mime_type import CloudAgentPromptImageMimeType
from ..models.cloud_agent_prompt_image_type import CloudAgentPromptImageType

T = TypeVar("T", bound="CloudAgentPromptImage")


@_attrs_define
class CloudAgentPromptImage:
    """
    Attributes:
        type_ (CloudAgentPromptImageType):
        data (str):
        mime_type (CloudAgentPromptImageMimeType):
    """

    type_: CloudAgentPromptImageType
    data: str
    mime_type: CloudAgentPromptImageMimeType

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        data = self.data

        mime_type = self.mime_type.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "type": type_,
                "data": data,
                "mime_type": mime_type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = CloudAgentPromptImageType(d.pop("type"))

        data = d.pop("data")

        mime_type = CloudAgentPromptImageMimeType(d.pop("mime_type"))

        cloud_agent_prompt_image = cls(
            type_=type_,
            data=data,
            mime_type=mime_type,
        )

        return cloud_agent_prompt_image
