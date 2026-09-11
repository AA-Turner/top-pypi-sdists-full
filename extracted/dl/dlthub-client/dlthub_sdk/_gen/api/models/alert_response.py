from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trigger_type import TriggerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.email_alert_action_response import EmailAlertActionResponse


T = TypeVar("T", bound="AlertResponse")


@_attrs_define
class AlertResponse:
    """
    Attributes:
        display_label (str): Human-readable label for the trigger
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-run-failure')
        workspace_id (UUID): Workspace owning this alert
        actions (list[EmailAlertActionResponse] | Unset): Configured actions
    """

    display_label: str
    trigger: TriggerType
    workspace_id: UUID
    actions: list[EmailAlertActionResponse] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_label = self.display_label

        trigger = self.trigger.value

        workspace_id = str(self.workspace_id)

        actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item = actions_item_data.to_dict()
                actions.append(actions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "display_label": display_label,
                "trigger": trigger,
                "workspace_id": workspace_id,
            }
        )
        if actions is not UNSET:
            field_dict["actions"] = actions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.email_alert_action_response import EmailAlertActionResponse

        d = dict(src_dict)
        display_label = d.pop("display_label")

        trigger = TriggerType(d.pop("trigger"))

        workspace_id = UUID(d.pop("workspace_id"))

        _actions = d.pop("actions", UNSET)
        actions: list[EmailAlertActionResponse] | Unset = UNSET
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:
                actions_item = EmailAlertActionResponse.from_dict(actions_item_data)

                actions.append(actions_item)

        alert_response = cls(
            display_label=display_label,
            trigger=trigger,
            workspace_id=workspace_id,
            actions=actions,
        )

        alert_response.additional_properties = d
        return alert_response

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
