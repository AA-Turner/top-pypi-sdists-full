from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.payment_type_enum import PaymentTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_profile_attributes_request import PaymentProfileAttributesRequest


T = TypeVar("T", bound="PaymentProfileRequest")


@_attrs_define
class PaymentProfileRequest:
    """
    Attributes:
        name (str):
        organization (str):
        payment_type (PaymentTypeEnum):
        attributes (Union[Unset, PaymentProfileAttributesRequest]):
        is_active (Union[None, Unset, bool]):  Default: True.
    """

    name: str
    organization: str
    payment_type: PaymentTypeEnum
    attributes: Union[Unset, "PaymentProfileAttributesRequest"] = UNSET
    is_active: Union[None, Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        organization = self.organization

        payment_type = self.payment_type.value

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        is_active: Union[None, Unset, bool]
        if isinstance(self.is_active, Unset):
            is_active = UNSET
        else:
            is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "organization": organization,
                "payment_type": payment_type,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_profile_attributes_request import PaymentProfileAttributesRequest

        d = dict(src_dict)
        name = d.pop("name")

        organization = d.pop("organization")

        payment_type = PaymentTypeEnum(d.pop("payment_type"))

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, PaymentProfileAttributesRequest]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = PaymentProfileAttributesRequest.from_dict(_attributes)

        def _parse_is_active(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_active = _parse_is_active(d.pop("is_active", UNSET))

        payment_profile_request = cls(
            name=name,
            organization=organization,
            payment_type=payment_type,
            attributes=attributes,
            is_active=is_active,
        )

        payment_profile_request.additional_properties = d
        return payment_profile_request

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
