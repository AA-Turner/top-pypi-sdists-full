import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="DashboardReviewDeadline")


@_attrs_define
class DashboardReviewDeadline:
    """
    Attributes:
        uuid (UUID):
        proposal_uuid (UUID):
        proposal_name (str):
        call_uuid (UUID):
        call_name (str):
        due_date (Union[None, datetime.datetime]):
    """

    uuid: UUID
    proposal_uuid: UUID
    proposal_name: str
    call_uuid: UUID
    call_name: str
    due_date: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        proposal_uuid = str(self.proposal_uuid)

        proposal_name = self.proposal_name

        call_uuid = str(self.call_uuid)

        call_name = self.call_name

        due_date: Union[None, str]
        if isinstance(self.due_date, datetime.datetime):
            due_date = self.due_date.isoformat()
        else:
            due_date = self.due_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "proposal_uuid": proposal_uuid,
                "proposal_name": proposal_name,
                "call_uuid": call_uuid,
                "call_name": call_name,
                "due_date": due_date,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_name = d.pop("proposal_name")

        call_uuid = UUID(d.pop("call_uuid"))

        call_name = d.pop("call_name")

        def _parse_due_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                due_date_type_0 = isoparse(data)

                return due_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        due_date = _parse_due_date(d.pop("due_date"))

        dashboard_review_deadline = cls(
            uuid=uuid,
            proposal_uuid=proposal_uuid,
            proposal_name=proposal_name,
            call_uuid=call_uuid,
            call_name=call_name,
            due_date=due_date,
        )

        dashboard_review_deadline.additional_properties = d
        return dashboard_review_deadline

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
