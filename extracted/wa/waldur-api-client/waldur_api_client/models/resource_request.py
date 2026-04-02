import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceRequest")


@_attrs_define
class ResourceRequest:
    """
    Attributes:
        offering (str):
        name (str):
        plan (Union[Unset, str]):
        slug (Union[Unset, str]): URL-friendly identifier. Only editable by staff users.
        end_date (Union[None, Unset, datetime.date]): The date is inclusive. Once reached, a resource will be scheduled
            for termination.
        downscaled (Union[Unset, bool]):
        paused (Union[Unset, bool]):
    """

    offering: str
    name: str
    plan: Union[Unset, str] = UNSET
    slug: Union[Unset, str] = UNSET
    end_date: Union[None, Unset, datetime.date] = UNSET
    downscaled: Union[Unset, bool] = UNSET
    paused: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering = self.offering

        name = self.name

        plan = self.plan

        slug = self.slug

        end_date: Union[None, Unset, str]
        if isinstance(self.end_date, Unset):
            end_date = UNSET
        elif isinstance(self.end_date, datetime.date):
            end_date = self.end_date.isoformat()
        else:
            end_date = self.end_date

        downscaled = self.downscaled

        paused = self.paused

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering": offering,
                "name": name,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan
        if slug is not UNSET:
            field_dict["slug"] = slug
        if end_date is not UNSET:
            field_dict["end_date"] = end_date
        if downscaled is not UNSET:
            field_dict["downscaled"] = downscaled
        if paused is not UNSET:
            field_dict["paused"] = paused

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        offering = d.pop("offering")

        name = d.pop("name")

        plan = d.pop("plan", UNSET)

        slug = d.pop("slug", UNSET)

        def _parse_end_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                end_date_type_0 = isoparse(data).date()

                return end_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        end_date = _parse_end_date(d.pop("end_date", UNSET))

        downscaled = d.pop("downscaled", UNSET)

        paused = d.pop("paused", UNSET)

        resource_request = cls(
            offering=offering,
            name=name,
            plan=plan,
            slug=slug,
            end_date=end_date,
            downscaled=downscaled,
            paused=paused,
        )

        resource_request.additional_properties = d
        return resource_request

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
