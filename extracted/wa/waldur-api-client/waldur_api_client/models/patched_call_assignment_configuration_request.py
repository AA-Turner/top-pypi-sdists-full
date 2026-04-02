from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedCallAssignmentConfigurationRequest")


@_attrs_define
class PatchedCallAssignmentConfigurationRequest:
    """
    Attributes:
        auto_reassign_on_decline (Union[Unset, bool]): Automatically assign next-best reviewer when someone declines. If
            False, manager must manually approve reassignments.
        max_auto_reassign_attempts (Union[Unset, int]): Maximum automatic reassignment attempts before requiring manual
            intervention.
        assignment_expiration_days (Union[Unset, int]): Days until assignment invitation expires if not responded to.
        send_reminder_before_expiry_days (Union[Unset, int]): Days before expiry to send reminder notification.
    """

    auto_reassign_on_decline: Union[Unset, bool] = UNSET
    max_auto_reassign_attempts: Union[Unset, int] = UNSET
    assignment_expiration_days: Union[Unset, int] = UNSET
    send_reminder_before_expiry_days: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_reassign_on_decline = self.auto_reassign_on_decline

        max_auto_reassign_attempts = self.max_auto_reassign_attempts

        assignment_expiration_days = self.assignment_expiration_days

        send_reminder_before_expiry_days = self.send_reminder_before_expiry_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_reassign_on_decline is not UNSET:
            field_dict["auto_reassign_on_decline"] = auto_reassign_on_decline
        if max_auto_reassign_attempts is not UNSET:
            field_dict["max_auto_reassign_attempts"] = max_auto_reassign_attempts
        if assignment_expiration_days is not UNSET:
            field_dict["assignment_expiration_days"] = assignment_expiration_days
        if send_reminder_before_expiry_days is not UNSET:
            field_dict["send_reminder_before_expiry_days"] = send_reminder_before_expiry_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_reassign_on_decline = d.pop("auto_reassign_on_decline", UNSET)

        max_auto_reassign_attempts = d.pop("max_auto_reassign_attempts", UNSET)

        assignment_expiration_days = d.pop("assignment_expiration_days", UNSET)

        send_reminder_before_expiry_days = d.pop("send_reminder_before_expiry_days", UNSET)

        patched_call_assignment_configuration_request = cls(
            auto_reassign_on_decline=auto_reassign_on_decline,
            max_auto_reassign_attempts=max_auto_reassign_attempts,
            assignment_expiration_days=assignment_expiration_days,
            send_reminder_before_expiry_days=send_reminder_before_expiry_days,
        )

        patched_call_assignment_configuration_request.additional_properties = d
        return patched_call_assignment_configuration_request

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
