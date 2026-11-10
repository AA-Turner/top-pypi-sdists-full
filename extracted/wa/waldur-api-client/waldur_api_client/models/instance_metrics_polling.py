import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="InstanceMetricsPolling")


@_attrs_define
class InstanceMetricsPolling:
    """
    Attributes:
        enabled (bool): Whether the instance's provider collects instance metrics.
        interval_minutes (int): Minutes between reads now, the faster ones included.
        offering_interval_minutes (int): Minutes between reads when nobody asked for faster ones.
        faster_until (Union[None, datetime.datetime]):
        last_polled_at (Union[None, datetime.datetime]):
        next_poll_at (Union[None, datetime.datetime]): Empty while the instance is not running.
        can_manage (bool): Whether the user may ask for faster reads or a read now.
        instance_name (Union[None, str]): The instance whose reads cover the resource; for a volume, the one it is
            attached to. Empty for a detached volume.
        instance_resource_uuid (Union[None, UUID]):
    """

    enabled: bool
    interval_minutes: int
    offering_interval_minutes: int
    faster_until: Union[None, datetime.datetime]
    last_polled_at: Union[None, datetime.datetime]
    next_poll_at: Union[None, datetime.datetime]
    can_manage: bool
    instance_name: Union[None, str]
    instance_resource_uuid: Union[None, UUID]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        interval_minutes = self.interval_minutes

        offering_interval_minutes = self.offering_interval_minutes

        faster_until: Union[None, str]
        if isinstance(self.faster_until, datetime.datetime):
            faster_until = self.faster_until.isoformat()
        else:
            faster_until = self.faster_until

        last_polled_at: Union[None, str]
        if isinstance(self.last_polled_at, datetime.datetime):
            last_polled_at = self.last_polled_at.isoformat()
        else:
            last_polled_at = self.last_polled_at

        next_poll_at: Union[None, str]
        if isinstance(self.next_poll_at, datetime.datetime):
            next_poll_at = self.next_poll_at.isoformat()
        else:
            next_poll_at = self.next_poll_at

        can_manage = self.can_manage

        instance_name: Union[None, str]
        instance_name = self.instance_name

        instance_resource_uuid: Union[None, str]
        if isinstance(self.instance_resource_uuid, UUID):
            instance_resource_uuid = str(self.instance_resource_uuid)
        else:
            instance_resource_uuid = self.instance_resource_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "interval_minutes": interval_minutes,
                "offering_interval_minutes": offering_interval_minutes,
                "faster_until": faster_until,
                "last_polled_at": last_polled_at,
                "next_poll_at": next_poll_at,
                "can_manage": can_manage,
                "instance_name": instance_name,
                "instance_resource_uuid": instance_resource_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        enabled = d.pop("enabled")

        interval_minutes = d.pop("interval_minutes")

        offering_interval_minutes = d.pop("offering_interval_minutes")

        def _parse_faster_until(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                faster_until_type_0 = isoparse(data)

                return faster_until_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        faster_until = _parse_faster_until(d.pop("faster_until"))

        def _parse_last_polled_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_polled_at_type_0 = isoparse(data)

                return last_polled_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_polled_at = _parse_last_polled_at(d.pop("last_polled_at"))

        def _parse_next_poll_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_poll_at_type_0 = isoparse(data)

                return next_poll_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        next_poll_at = _parse_next_poll_at(d.pop("next_poll_at"))

        can_manage = d.pop("can_manage")

        def _parse_instance_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        instance_name = _parse_instance_name(d.pop("instance_name"))

        def _parse_instance_resource_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                instance_resource_uuid_type_0 = UUID(data)

                return instance_resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        instance_resource_uuid = _parse_instance_resource_uuid(d.pop("instance_resource_uuid"))

        instance_metrics_polling = cls(
            enabled=enabled,
            interval_minutes=interval_minutes,
            offering_interval_minutes=offering_interval_minutes,
            faster_until=faster_until,
            last_polled_at=last_polled_at,
            next_poll_at=next_poll_at,
            can_manage=can_manage,
            instance_name=instance_name,
            instance_resource_uuid=instance_resource_uuid,
        )

        instance_metrics_polling.additional_properties = d
        return instance_metrics_polling

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
