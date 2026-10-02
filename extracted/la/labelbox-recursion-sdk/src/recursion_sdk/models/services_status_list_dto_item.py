from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.services_status_list_dto_item_status import ServicesStatusListDtoItemStatus
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.services_status_list_dto_item_details import ServicesStatusListDtoItemDetails





T = TypeVar("T", bound="ServicesStatusListDtoItem")



@_attrs_define
class ServicesStatusListDtoItem:
    """ 
        Attributes:
            details (ServicesStatusListDtoItemDetails): Provider-specific status payload (HTTP code, latency, error message,
                etc.).
            key (str): Stable identifier for the service used as a dictionary key in admin UIs.
            last_checked (datetime.datetime | None): ISO timestamp of the most recent health probe, or null if the service
                has never been checked.
            name (str): Human-readable service name.
            source (str): Origin of the status reading (e.g. an internal probe or a third-party service.)
            status (ServicesStatusListDtoItemStatus): Operational state: operational, degraded, down, or unknown.
     """

    details: ServicesStatusListDtoItemDetails
    key: str
    last_checked: datetime.datetime | None
    name: str
    source: str
    status: ServicesStatusListDtoItemStatus





    def to_dict(self) -> dict[str, Any]:
        from ..models.services_status_list_dto_item_details import ServicesStatusListDtoItemDetails # noqa: PLC0415
        details = self.details.to_dict()

        key = self.key

        last_checked: None | str
        if isinstance(self.last_checked, datetime.datetime):
            last_checked = self.last_checked.isoformat()
        else:
            last_checked = self.last_checked

        name = self.name

        source = self.source

        status = self.status.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "details": details,
            "key": key,
            "last_checked": last_checked,
            "name": name,
            "source": source,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.services_status_list_dto_item_details import ServicesStatusListDtoItemDetails # noqa: PLC0415
        d = dict(src_dict)
        details = ServicesStatusListDtoItemDetails.from_dict(d.pop("details"))




        key = d.pop("key")

        def _parse_last_checked(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_checked_type_0 = datetime.datetime.fromisoformat(data)



                return last_checked_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        last_checked = _parse_last_checked(d.pop("last_checked"))


        name = d.pop("name")

        source = d.pop("source")

        status = ServicesStatusListDtoItemStatus(d.pop("status"))




        services_status_list_dto_item = cls(
            details=details,
            key=key,
            last_checked=last_checked,
            name=name,
            source=source,
            status=status,
        )

        return services_status_list_dto_item

