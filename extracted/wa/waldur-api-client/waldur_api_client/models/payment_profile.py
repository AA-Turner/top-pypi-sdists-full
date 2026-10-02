from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.payment_type_enum import PaymentTypeEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.payment_profile_attributes import PaymentProfileAttributes


T = TypeVar("T", bound="PaymentProfile")


@_attrs_define
class PaymentProfile:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        url (Union[Unset, str]):
        name (Union[Unset, str]):
        organization_uuid (Union[Unset, UUID]):
        organization (Union[Unset, str]):
        attributes (Union[Unset, PaymentProfileAttributes]):
        payment_type (Union[Unset, PaymentTypeEnum]):
        payment_type_display (Union[Unset, str]):
        is_active (Union[None, Unset, bool]):  Default: True.
    """

    uuid: Union[Unset, UUID] = UNSET
    url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    organization_uuid: Union[Unset, UUID] = UNSET
    organization: Union[Unset, str] = UNSET
    attributes: Union[Unset, "PaymentProfileAttributes"] = UNSET
    payment_type: Union[Unset, PaymentTypeEnum] = UNSET
    payment_type_display: Union[Unset, str] = UNSET
    is_active: Union[None, Unset, bool] = True
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        url = self.url

        name = self.name

        organization_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.organization_uuid, Unset):
            organization_uuid = str(self.organization_uuid)

        organization = self.organization

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        payment_type: Union[Unset, str] = UNSET
        if not isinstance(self.payment_type, Unset):
            payment_type = self.payment_type.value

        payment_type_display = self.payment_type_display

        is_active: Union[None, Unset, bool]
        if isinstance(self.is_active, Unset):
            is_active = UNSET
        else:
            is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name
        if organization_uuid is not UNSET:
            field_dict["organization_uuid"] = organization_uuid
        if organization is not UNSET:
            field_dict["organization"] = organization
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if payment_type is not UNSET:
            field_dict["payment_type"] = payment_type
        if payment_type_display is not UNSET:
            field_dict["payment_type_display"] = payment_type_display
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.payment_profile_attributes import PaymentProfileAttributes

        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        _organization_uuid = d.pop("organization_uuid", UNSET)
        organization_uuid: Union[Unset, UUID]
        if isinstance(_organization_uuid, Unset):
            organization_uuid = UNSET
        else:
            organization_uuid = UUID(_organization_uuid)

        organization = d.pop("organization", UNSET)

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, PaymentProfileAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = PaymentProfileAttributes.from_dict(_attributes)

        _payment_type = d.pop("payment_type", UNSET)
        payment_type: Union[Unset, PaymentTypeEnum]
        if isinstance(_payment_type, Unset):
            payment_type = UNSET
        else:
            payment_type = PaymentTypeEnum(_payment_type)

        payment_type_display = d.pop("payment_type_display", UNSET)

        def _parse_is_active(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        is_active = _parse_is_active(d.pop("is_active", UNSET))

        payment_profile = cls(
            uuid=uuid,
            url=url,
            name=name,
            organization_uuid=organization_uuid,
            organization=organization,
            attributes=attributes,
            payment_type=payment_type,
            payment_type_display=payment_type_display,
            is_active=is_active,
        )

        payment_profile.additional_properties = d
        return payment_profile

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
