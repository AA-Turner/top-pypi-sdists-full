import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="PendingRecord")


@_attrs_define
class PendingRecord:
    """
    Attributes:
        uuid (UUID):
        resource_uuid (UUID):
        resource_name (str):
        license_reference (str):
        billing_period (datetime.date):
        consumed_sell (str):
        last_sync_at (Union[None, datetime.datetime]):
    """

    uuid: UUID
    resource_uuid: UUID
    resource_name: str
    license_reference: str
    billing_period: datetime.date
    consumed_sell: str
    last_sync_at: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        license_reference = self.license_reference

        billing_period = self.billing_period.isoformat()

        consumed_sell = self.consumed_sell

        last_sync_at: Union[None, str]
        if isinstance(self.last_sync_at, datetime.datetime):
            last_sync_at = self.last_sync_at.isoformat()
        else:
            last_sync_at = self.last_sync_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "license_reference": license_reference,
                "billing_period": billing_period,
                "consumed_sell": consumed_sell,
                "last_sync_at": last_sync_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        license_reference = d.pop("license_reference")

        billing_period = isoparse(d.pop("billing_period")).date()

        consumed_sell = d.pop("consumed_sell")

        def _parse_last_sync_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_sync_at_type_0 = isoparse(data)

                return last_sync_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_sync_at = _parse_last_sync_at(d.pop("last_sync_at"))

        pending_record = cls(
            uuid=uuid,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            license_reference=license_reference,
            billing_period=billing_period,
            consumed_sell=consumed_sell,
            last_sync_at=last_sync_at,
        )

        pending_record.additional_properties = d
        return pending_record

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
