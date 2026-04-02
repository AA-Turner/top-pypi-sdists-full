from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExportOfferingDataRequest")


@_attrs_define
class ExportOfferingDataRequest:
    """
    Attributes:
        name (str):
        description (str):
        full_description (str):
        vendor_details (str):
        getting_started (str):
        integration_guide (str):
        type_ (str):
        shared (bool):
        billable (bool):
        state (str):
        category_name (Union[None, str]):
        country (str):
        latitude (Union[None, float]):
        longitude (Union[None, float]):
        access_url (str):
        paused_reason (str):
        attributes (Union[Unset, Any]):
        options (Union[Unset, Any]):
    """

    name: str
    description: str
    full_description: str
    vendor_details: str
    getting_started: str
    integration_guide: str
    type_: str
    shared: bool
    billable: bool
    state: str
    category_name: Union[None, str]
    country: str
    latitude: Union[None, float]
    longitude: Union[None, float]
    access_url: str
    paused_reason: str
    attributes: Union[Unset, Any] = UNSET
    options: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        full_description = self.full_description

        vendor_details = self.vendor_details

        getting_started = self.getting_started

        integration_guide = self.integration_guide

        type_ = self.type_

        shared = self.shared

        billable = self.billable

        state = self.state

        category_name: Union[None, str]
        category_name = self.category_name

        country = self.country

        latitude: Union[None, float]
        latitude = self.latitude

        longitude: Union[None, float]
        longitude = self.longitude

        access_url = self.access_url

        paused_reason = self.paused_reason

        attributes = self.attributes

        options = self.options

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "full_description": full_description,
                "vendor_details": vendor_details,
                "getting_started": getting_started,
                "integration_guide": integration_guide,
                "type": type_,
                "shared": shared,
                "billable": billable,
                "state": state,
                "category_name": category_name,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,
                "access_url": access_url,
                "paused_reason": paused_reason,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if options is not UNSET:
            field_dict["options"] = options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        full_description = d.pop("full_description")

        vendor_details = d.pop("vendor_details")

        getting_started = d.pop("getting_started")

        integration_guide = d.pop("integration_guide")

        type_ = d.pop("type")

        shared = d.pop("shared")

        billable = d.pop("billable")

        state = d.pop("state")

        def _parse_category_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        category_name = _parse_category_name(d.pop("category_name"))

        country = d.pop("country")

        def _parse_latitude(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        latitude = _parse_latitude(d.pop("latitude"))

        def _parse_longitude(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        longitude = _parse_longitude(d.pop("longitude"))

        access_url = d.pop("access_url")

        paused_reason = d.pop("paused_reason")

        attributes = d.pop("attributes", UNSET)

        options = d.pop("options", UNSET)

        export_offering_data_request = cls(
            name=name,
            description=description,
            full_description=full_description,
            vendor_details=vendor_details,
            getting_started=getting_started,
            integration_guide=integration_guide,
            type_=type_,
            shared=shared,
            billable=billable,
            state=state,
            category_name=category_name,
            country=country,
            latitude=latitude,
            longitude=longitude,
            access_url=access_url,
            paused_reason=paused_reason,
            attributes=attributes,
            options=options,
        )

        export_offering_data_request.additional_properties = d
        return export_offering_data_request

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
