from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.trigger_type import TriggerType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.alert_filters import AlertFilters
    from ..models.email_alert_action_response import EmailAlertActionResponse
    from ..models.slack_alert_action_response import SlackAlertActionResponse


T = TypeVar("T", bound="AlertResponse")


@_attrs_define
class AlertResponse:
    """
    Attributes:
        display_label (str): Human-readable label for the trigger
        trigger (TriggerType): Machine-readable trigger identifier, lower-kebab-case (e.g. 'job-run-failure')
        workspace_id (UUID): Workspace owning this alert
        actions (list[EmailAlertActionResponse | SlackAlertActionResponse] | Unset): Configured actions
        filters (AlertFilters | Unset): Filters applied to this alert
    """

    display_label: str
    trigger: TriggerType
    workspace_id: UUID
    actions: list[EmailAlertActionResponse | SlackAlertActionResponse] | Unset = UNSET
    filters: AlertFilters | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.email_alert_action_response import EmailAlertActionResponse

        display_label = self.display_label

        trigger = self.trigger.value

        workspace_id = str(self.workspace_id)

        actions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.actions, Unset):
            actions = []
            for actions_item_data in self.actions:
                actions_item: dict[str, Any]
                if isinstance(actions_item_data, EmailAlertActionResponse):
                    actions_item = actions_item_data.to_dict()
                else:
                    actions_item = actions_item_data.to_dict()

                actions.append(actions_item)

        filters: dict[str, Any] | Unset = UNSET
        if not isinstance(self.filters, Unset):
            filters = self.filters.to_dict()

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
        if filters is not UNSET:
            field_dict["filters"] = filters

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.alert_filters import AlertFilters
        from ..models.email_alert_action_response import EmailAlertActionResponse
        from ..models.slack_alert_action_response import SlackAlertActionResponse

        d = dict(src_dict)
        display_label = d.pop("display_label")

        trigger = TriggerType(d.pop("trigger"))

        workspace_id = UUID(d.pop("workspace_id"))

        _actions = d.pop("actions", UNSET)
        actions: list[EmailAlertActionResponse | SlackAlertActionResponse] | Unset = (
            UNSET
        )
        if _actions is not UNSET:
            actions = []
            for actions_item_data in _actions:

                def _parse_actions_item(
                    data: object,
                ) -> EmailAlertActionResponse | SlackAlertActionResponse:
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        actions_item_type_0 = EmailAlertActionResponse.from_dict(data)

                        return actions_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    if not isinstance(data, dict):
                        raise TypeError()
                    actions_item_type_1 = SlackAlertActionResponse.from_dict(data)

                    return actions_item_type_1

                actions_item = _parse_actions_item(actions_item_data)

                actions.append(actions_item)

        _filters = d.pop("filters", UNSET)
        filters: AlertFilters | Unset
        if isinstance(_filters, Unset):
            filters = UNSET
        else:
            filters = AlertFilters.from_dict(_filters)

        alert_response = cls(
            display_label=display_label,
            trigger=trigger,
            workspace_id=workspace_id,
            actions=actions,
            filters=filters,
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
