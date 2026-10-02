from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsSlackChannel")



@_attrs_define
class ManagedAgentsSlackChannel:
    """ One channel the Slack connection's bot is a member of: the id a binding stores, the name the workspace shows, and
    whether it is private or shared with another organization.

        Example:
            {'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'isExtShared': True, 'isPrivate': True, 'name': 'example-name'}

        Attributes:
            id (str): Slack channel id, the value a trigger binding stores as channel_id.
            is_ext_shared (bool): Whether the channel is shared with another organization (Slack Connect). A proactive
                binding here lets external members start investigations.
            is_private (bool): Whether the channel is private in the connected workspace.
            name (str): Channel name as the connected workspace sees it, without the leading #. Slack Connect channels can
                carry a different name in the other workspace.
     """

    id: str
    is_ext_shared: bool
    is_private: bool
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        is_ext_shared = self.is_ext_shared

        is_private = self.is_private

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "isExtShared": is_ext_shared,
            "isPrivate": is_private,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        is_ext_shared = d.pop("isExtShared")

        is_private = d.pop("isPrivate")

        name = d.pop("name")

        managed_agents_slack_channel = cls(
            id=id,
            is_ext_shared=is_ext_shared,
            is_private=is_private,
            name=name,
        )


        managed_agents_slack_channel.additional_properties = d
        return managed_agents_slack_channel

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
