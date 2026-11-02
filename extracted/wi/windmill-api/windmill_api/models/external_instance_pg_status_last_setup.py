import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.external_instance_pg_status_last_setup_steps_item import ExternalInstancePgStatusLastSetupStepsItem


T = TypeVar("T", bound="ExternalInstancePgStatusLastSetup")


@_attrs_define
class ExternalInstancePgStatusLastSetup:
    """
    Attributes:
        success (bool): no step failed; warnings leave it true
        finished_at (datetime.datetime):
        steps (List['ExternalInstancePgStatusLastSetupStepsItem']):
    """

    success: bool
    finished_at: datetime.datetime
    steps: List["ExternalInstancePgStatusLastSetupStepsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        success = self.success
        finished_at = self.finished_at.isoformat()

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()

            steps.append(steps_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "success": success,
                "finished_at": finished_at,
                "steps": steps,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.external_instance_pg_status_last_setup_steps_item import (
            ExternalInstancePgStatusLastSetupStepsItem,
        )

        d = src_dict.copy()
        success = d.pop("success")

        finished_at = isoparse(d.pop("finished_at"))

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = ExternalInstancePgStatusLastSetupStepsItem.from_dict(steps_item_data)

            steps.append(steps_item)

        external_instance_pg_status_last_setup = cls(
            success=success,
            finished_at=finished_at,
            steps=steps,
        )

        external_instance_pg_status_last_setup.additional_properties = d
        return external_instance_pg_status_last_setup

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
