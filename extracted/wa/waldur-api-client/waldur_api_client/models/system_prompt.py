import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="SystemPrompt")


@_attrs_define
class SystemPrompt:
    """
    Attributes:
        uuid (UUID):
        name (str):
        is_active (bool): Whether this prompt is currently used by the AI Assistant. Only one prompt can be active.
        created (datetime.datetime):
        modified (datetime.datetime):
        description (Union[Unset, str]):
        custom_instructions (Union[Unset, str]): Additional instructions injected into the system prompt. Use this for
            organisation-specific context, terminology, FAQ content, or behavioural guidelines. Supports {assistant_name}
            and {organization} placeholders.
    """

    uuid: UUID
    name: str
    is_active: bool
    created: datetime.datetime
    modified: datetime.datetime
    description: Union[Unset, str] = UNSET
    custom_instructions: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        is_active = self.is_active

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        description = self.description

        custom_instructions = self.custom_instructions

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "is_active": is_active,
                "created": created,
                "modified": modified,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if custom_instructions is not UNSET:
            field_dict["custom_instructions"] = custom_instructions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        is_active = d.pop("is_active")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        description = d.pop("description", UNSET)

        custom_instructions = d.pop("custom_instructions", UNSET)

        system_prompt = cls(
            uuid=uuid,
            name=name,
            is_active=is_active,
            created=created,
            modified=modified,
            description=description,
            custom_instructions=custom_instructions,
        )

        system_prompt.additional_properties = d
        return system_prompt

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
