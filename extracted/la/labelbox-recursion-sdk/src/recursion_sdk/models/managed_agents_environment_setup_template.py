from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupTemplate")



@_attrs_define
class ManagedAgentsEnvironmentSetupTemplate:
    """ A starting-point setup script. The same list feeds the console and the API so humans and agents model the same
    idiom.

        Example:
            {'accelerator': True, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'script': 'example', 'summary': 'example',
                'title': 'example'}

        Attributes:
            id (str): Stable identifier of the template.
            script (str): The setup script. Edit it; it is a starting point, not a preset.
            summary (str): What the template sets up and when to choose it.
            title (str): Short name shown in a picker.
            accelerator (bool | Unset): True when the template assumes a GPU environment.
     """

    id: str
    script: str
    summary: str
    title: str
    accelerator: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        script = self.script

        summary = self.summary

        title = self.title

        accelerator = self.accelerator


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "script": script,
            "summary": summary,
            "title": title,
        })
        if accelerator is not UNSET:
            field_dict["accelerator"] = accelerator

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        script = d.pop("script")

        summary = d.pop("summary")

        title = d.pop("title")

        accelerator = d.pop("accelerator", UNSET)

        managed_agents_environment_setup_template = cls(
            id=id,
            script=script,
            summary=summary,
            title=title,
            accelerator=accelerator,
        )


        managed_agents_environment_setup_template.additional_properties = d
        return managed_agents_environment_setup_template

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
