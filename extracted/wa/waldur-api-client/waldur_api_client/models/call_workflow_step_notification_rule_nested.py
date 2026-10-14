from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.recipient_enum import RecipientEnum
from ..models.trigger_enum import TriggerEnum

T = TypeVar("T", bound="CallWorkflowStepNotificationRuleNested")


@_attrs_define
class CallWorkflowStepNotificationRuleNested:
    """
    Attributes:
        uuid (UUID):
        trigger (TriggerEnum):
        recipient (RecipientEnum):
        days_before (Union[None, int]): Only for deadline_approaching: how many days before the step's deadline the
            reminder is sent.
        is_enabled (bool):
        notified_proposal_roles (list[str]):
    """

    uuid: UUID
    trigger: TriggerEnum
    recipient: RecipientEnum
    days_before: Union[None, int]
    is_enabled: bool
    notified_proposal_roles: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        trigger = self.trigger.value

        recipient = self.recipient.value

        days_before: Union[None, int]
        days_before = self.days_before

        is_enabled = self.is_enabled

        notified_proposal_roles = self.notified_proposal_roles

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "trigger": trigger,
                "recipient": recipient,
                "days_before": days_before,
                "is_enabled": is_enabled,
                "notified_proposal_roles": notified_proposal_roles,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        trigger = TriggerEnum(d.pop("trigger"))

        recipient = RecipientEnum(d.pop("recipient"))

        def _parse_days_before(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        days_before = _parse_days_before(d.pop("days_before"))

        is_enabled = d.pop("is_enabled")

        notified_proposal_roles = cast(list[str], d.pop("notified_proposal_roles"))

        call_workflow_step_notification_rule_nested = cls(
            uuid=uuid,
            trigger=trigger,
            recipient=recipient,
            days_before=days_before,
            is_enabled=is_enabled,
            notified_proposal_roles=notified_proposal_roles,
        )

        call_workflow_step_notification_rule_nested.additional_properties = d
        return call_workflow_step_notification_rule_nested

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
