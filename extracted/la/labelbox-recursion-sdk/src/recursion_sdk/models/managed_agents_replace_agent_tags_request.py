from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ManagedAgentsReplaceAgentTagsRequest")



@_attrs_define
class ManagedAgentsReplaceAgentTagsRequest:
    """ Request body for atomically replacing an agent's complete mutable tag classification.

        Example:
            {'tag_ids': ['example']}

        Attributes:
            tag_ids (list[str]): Complete replacement set of tag ids, with at most 32 distinct ids. Every id must be a live
                tag in the caller's organization. Duplicates are collapsed before enforcing the limit; [] removes every tag.
     """

    tag_ids: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        tag_ids = self.tag_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "tag_ids": tag_ids,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        tag_ids = cast(list[str], d.pop("tag_ids"))


        managed_agents_replace_agent_tags_request = cls(
            tag_ids=tag_ids,
        )


        managed_agents_replace_agent_tags_request.additional_properties = d
        return managed_agents_replace_agent_tags_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
