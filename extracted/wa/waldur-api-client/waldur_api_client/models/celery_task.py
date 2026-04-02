from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.celery_task_delivery_info import CeleryTaskDeliveryInfo
    from ..models.celery_task_kwargs import CeleryTaskKwargs


T = TypeVar("T", bound="CeleryTask")


@_attrs_define
class CeleryTask:
    """
    Attributes:
        id (str): Unique task identifier
        name (str): Name of the task
        args (list[Any]): Positional arguments passed to the task
        kwargs (CeleryTaskKwargs): Keyword arguments passed to the task
        type_ (str): Task type
        hostname (str): Worker hostname executing the task
        time_start (float): Unix timestamp when task started
        acknowledged (bool): Whether task has been acknowledged
        delivery_info (CeleryTaskDeliveryInfo): Message delivery information
        worker_pid (int): Worker process ID
    """

    id: str
    name: str
    args: list[Any]
    kwargs: "CeleryTaskKwargs"
    type_: str
    hostname: str
    time_start: float
    acknowledged: bool
    delivery_info: "CeleryTaskDeliveryInfo"
    worker_pid: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        args = self.args

        kwargs = self.kwargs.to_dict()

        type_ = self.type_

        hostname = self.hostname

        time_start = self.time_start

        acknowledged = self.acknowledged

        delivery_info = self.delivery_info.to_dict()

        worker_pid = self.worker_pid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "args": args,
                "kwargs": kwargs,
                "type": type_,
                "hostname": hostname,
                "time_start": time_start,
                "acknowledged": acknowledged,
                "delivery_info": delivery_info,
                "worker_pid": worker_pid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.celery_task_delivery_info import CeleryTaskDeliveryInfo
        from ..models.celery_task_kwargs import CeleryTaskKwargs

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        args = cast(list[Any], d.pop("args"))

        kwargs = CeleryTaskKwargs.from_dict(d.pop("kwargs"))

        type_ = d.pop("type")

        hostname = d.pop("hostname")

        time_start = d.pop("time_start")

        acknowledged = d.pop("acknowledged")

        delivery_info = CeleryTaskDeliveryInfo.from_dict(d.pop("delivery_info"))

        worker_pid = d.pop("worker_pid")

        celery_task = cls(
            id=id,
            name=name,
            args=args,
            kwargs=kwargs,
            type_=type_,
            hostname=hostname,
            time_start=time_start,
            acknowledged=acknowledged,
            delivery_info=delivery_info,
            worker_pid=worker_pid,
        )

        celery_task.additional_properties = d
        return celery_task

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
