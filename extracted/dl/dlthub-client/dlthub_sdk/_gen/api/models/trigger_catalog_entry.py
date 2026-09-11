from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.action_type import ActionType
from ..models.trigger_type import TriggerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="TriggerCatalogEntry")


@_attrs_define
class TriggerCatalogEntry:
    """
    Attributes:
        description (str): Description of the event that causes this trigger to fire
        display_label (str): Human-readable trigger name
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-run-failure')
        supported_actions (list[ActionType] | Unset): Actions supported by this trigger (e.g. [ActionType.EMAIL_SEND])
    """

    description: str
    display_label: str
    trigger: TriggerType
    supported_actions: list[ActionType] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        description = self.description

        display_label = self.display_label

        trigger = self.trigger.value

        supported_actions: list[str] | Unset = UNSET
        if not isinstance(self.supported_actions, Unset):
            supported_actions = []
            for supported_actions_item_data in self.supported_actions:
                supported_actions_item = supported_actions_item_data.value
                supported_actions.append(supported_actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "description": description,
                "display_label": display_label,
                "trigger": trigger,
            }
        )
        if supported_actions is not UNSET:
            field_dict["supported_actions"] = supported_actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        description = d.pop("description")

        display_label = d.pop("display_label")

        trigger = TriggerType(d.pop("trigger"))

        _supported_actions = d.pop("supported_actions", UNSET)
        supported_actions: list[ActionType] | Unset = UNSET
        if _supported_actions is not UNSET:
            supported_actions = []
            for supported_actions_item_data in _supported_actions:
                supported_actions_item = ActionType(supported_actions_item_data)

                supported_actions.append(supported_actions_item)

        trigger_catalog_entry = cls(
            description=description,
            display_label=display_label,
            trigger=trigger,
            supported_actions=supported_actions,
        )

        trigger_catalog_entry.additional_properties = d
        return trigger_catalog_entry

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
