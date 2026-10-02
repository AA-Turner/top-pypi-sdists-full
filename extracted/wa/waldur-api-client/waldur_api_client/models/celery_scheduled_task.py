from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.celery_task import CeleryTask


T = TypeVar("T", bound="CeleryScheduledTask")


@_attrs_define
class CeleryScheduledTask:
    """
    Attributes:
        eta (str): Estimated time of arrival for the task
        priority (int): Task priority level
        request (CeleryTask):
    """

    eta: str
    priority: int
    request: "CeleryTask"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        eta = self.eta

        priority = self.priority

        request = self.request.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eta": eta,
                "priority": priority,
                "request": request,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.celery_task import CeleryTask

        d = dict(src_dict)
        eta = d.pop("eta")

        priority = d.pop("priority")

        request = CeleryTask.from_dict(d.pop("request"))

        celery_scheduled_task = cls(
            eta=eta,
            priority=priority,
            request=request,
        )

        celery_scheduled_task.additional_properties = d
        return celery_scheduled_task

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
