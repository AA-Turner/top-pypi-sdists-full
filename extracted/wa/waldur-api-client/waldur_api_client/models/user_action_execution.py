import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserActionExecution")


@_attrs_define
class UserActionExecution:
    """
    Attributes:
        id (int):
        corrective_action_label (str):
        executed_at (datetime.datetime):
        success (Union[Unset, bool]):
        error_message (Union[Unset, str]):
        execution_metadata (Union[Unset, str]):
    """

    id: int
    corrective_action_label: str
    executed_at: datetime.datetime
    success: Union[Unset, bool] = UNSET
    error_message: Union[Unset, str] = UNSET
    execution_metadata: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        corrective_action_label = self.corrective_action_label

        executed_at = self.executed_at.isoformat()

        success = self.success

        error_message = self.error_message

        execution_metadata = self.execution_metadata

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "corrective_action_label": corrective_action_label,
                "executed_at": executed_at,
            }
        )
        if success is not UNSET:
            field_dict["success"] = success
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if execution_metadata is not UNSET:
            field_dict["execution_metadata"] = execution_metadata

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        corrective_action_label = d.pop("corrective_action_label")

        executed_at = isoparse(d.pop("executed_at"))

        success = d.pop("success", UNSET)

        error_message = d.pop("error_message", UNSET)

        execution_metadata = d.pop("execution_metadata", UNSET)

        user_action_execution = cls(
            id=id,
            corrective_action_label=corrective_action_label,
            executed_at=executed_at,
            success=success,
            error_message=error_message,
            execution_metadata=execution_metadata,
        )

        user_action_execution.additional_properties = d
        return user_action_execution

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
