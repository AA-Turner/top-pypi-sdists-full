from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.cloud_agent_prompt_image import CloudAgentPromptImage


T = TypeVar("T", bound="CreateCloudAgentRunRequest")


@_attrs_define
class CreateCloudAgentRunRequest:
    """
    Attributes:
        prompt (str):
        images (list[CloudAgentPromptImage] | Unset):
        resume_session_id (str | Unset):
        parent_run_id (str | Unset):
    """

    prompt: str
    images: list[CloudAgentPromptImage] | Unset = UNSET
    resume_session_id: str | Unset = UNSET
    parent_run_id: str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        prompt = self.prompt

        images: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.images, Unset):
            images = []
            for images_item_data in self.images:
                images_item = images_item_data.to_dict()
                images.append(images_item)

        resume_session_id = self.resume_session_id

        parent_run_id = self.parent_run_id

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "prompt": prompt,
            }
        )
        if images is not UNSET:
            field_dict["images"] = images
        if resume_session_id is not UNSET:
            field_dict["resume_session_id"] = resume_session_id
        if parent_run_id is not UNSET:
            field_dict["parent_run_id"] = parent_run_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.cloud_agent_prompt_image import CloudAgentPromptImage

        d = dict(src_dict)
        prompt = d.pop("prompt")

        _images = d.pop("images", UNSET)
        images: list[CloudAgentPromptImage] | Unset = UNSET
        if _images is not UNSET:
            images = []
            for images_item_data in _images:
                images_item = CloudAgentPromptImage.from_dict(images_item_data)

                images.append(images_item)

        resume_session_id = d.pop("resume_session_id", UNSET)

        parent_run_id = d.pop("parent_run_id", UNSET)

        create_cloud_agent_run_request = cls(
            prompt=prompt,
            images=images,
            resume_session_id=resume_session_id,
            parent_run_id=parent_run_id,
        )

        return create_cloud_agent_run_request
