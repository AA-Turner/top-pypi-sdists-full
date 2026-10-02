import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.round_status import RoundStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CallRound")


@_attrs_define
class CallRound:
    """
    Attributes:
        url (str):
        uuid (UUID):
        start_time (datetime.datetime):
        cutoff_time (datetime.datetime):
        call_uuid (UUID):
        call_name (str):
        status (RoundStatus):
        slug (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    start_time: datetime.datetime
    cutoff_time: datetime.datetime
    call_uuid: UUID
    call_name: str
    status: RoundStatus
    slug: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        start_time = self.start_time.isoformat()

        cutoff_time = self.cutoff_time.isoformat()

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        status = self.status.value

        slug = self.slug

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "start_time": start_time,
                "cutoff_time": cutoff_time,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "status": status,
            }
        )
        if slug is not UNSET:
            field_dict["slug"] = slug

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        start_time = isoparse(d.pop("start_time"))

        cutoff_time = isoparse(d.pop("cutoff_time"))

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        status = RoundStatus(d.pop("status"))

        slug = d.pop("slug", UNSET)

        call_round = cls(
            url=url,
            uuid=uuid,
            start_time=start_time,
            cutoff_time=cutoff_time,
            call_uuid=call_uuid,
            call_name=call_name,
            status=status,
            slug=slug,
        )

        call_round.additional_properties = d
        return call_round

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
