from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsPlanItemRequest")



@_attrs_define
class ManagedAgentsPlanItemRequest:
    """ One step of a plan or to-do list an agent reported while working. Appears on an event's content when the agent's
    harness emits a plan; the service records it without acting on it.

        Example:
            {'content': 'example', 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example'}

        Attributes:
            content (str | Unset): Text of the planned step as the agent wrote it.
            id (str | Unset): Identifier for this plan entry, stable across the turns that update it.
            status (str | Unset): Progress value the agent reported for this step. Passed through as written and not
                interpreted by the service.
     """

    content: str | Unset = UNSET
    id: str | Unset = UNSET
    status: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        content = self.content

        id = self.id

        status = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if content is not UNSET:
            field_dict["content"] = content
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content = d.pop("content", UNSET)

        id = d.pop("id", UNSET)

        status = d.pop("status", UNSET)

        managed_agents_plan_item_request = cls(
            content=content,
            id=id,
            status=status,
        )


        managed_agents_plan_item_request.additional_properties = d
        return managed_agents_plan_item_request

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
