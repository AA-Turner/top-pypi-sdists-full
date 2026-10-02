import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="SetEarliestApproveRequest")


@_attrs_define
class SetEarliestApproveRequest:
    """
    Attributes:
        earliest_approve (Union[None, datetime.datetime]):
    """

    earliest_approve: Union[None, datetime.datetime]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        earliest_approve: Union[None, str]
        if isinstance(self.earliest_approve, datetime.datetime):
            earliest_approve = self.earliest_approve.isoformat()
        else:
            earliest_approve = self.earliest_approve

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "earliest_approve": earliest_approve,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_earliest_approve(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                earliest_approve_type_0 = isoparse(data)

                return earliest_approve_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        earliest_approve = _parse_earliest_approve(d.pop("earliest_approve"))

        set_earliest_approve_request = cls(
            earliest_approve=earliest_approve,
        )

        set_earliest_approve_request.additional_properties = d
        return set_earliest_approve_request

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
