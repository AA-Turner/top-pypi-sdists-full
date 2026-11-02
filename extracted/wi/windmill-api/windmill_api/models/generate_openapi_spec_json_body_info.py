from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.generate_openapi_spec_json_body_info_contact import GenerateOpenapiSpecJsonBodyInfoContact
    from ..models.generate_openapi_spec_json_body_info_license import GenerateOpenapiSpecJsonBodyInfoLicense


T = TypeVar("T", bound="GenerateOpenapiSpecJsonBodyInfo")


@_attrs_define
class GenerateOpenapiSpecJsonBodyInfo:
    """
    Attributes:
        title (str):
        version (str):
        description (Union[Unset, str]):
        terms_of_service (Union[Unset, str]):
        contact (Union[Unset, GenerateOpenapiSpecJsonBodyInfoContact]):
        license_ (Union[Unset, GenerateOpenapiSpecJsonBodyInfoLicense]):
    """

    title: str
    version: str
    description: Union[Unset, str] = UNSET
    terms_of_service: Union[Unset, str] = UNSET
    contact: Union[Unset, "GenerateOpenapiSpecJsonBodyInfoContact"] = UNSET
    license_: Union[Unset, "GenerateOpenapiSpecJsonBodyInfoLicense"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        version = self.version
        description = self.description
        terms_of_service = self.terms_of_service
        contact: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contact, Unset):
            contact = self.contact.to_dict()

        license_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.license_, Unset):
            license_ = self.license_.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "version": version,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if terms_of_service is not UNSET:
            field_dict["terms_of_service"] = terms_of_service
        if contact is not UNSET:
            field_dict["contact"] = contact
        if license_ is not UNSET:
            field_dict["license"] = license_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.generate_openapi_spec_json_body_info_contact import GenerateOpenapiSpecJsonBodyInfoContact
        from ..models.generate_openapi_spec_json_body_info_license import GenerateOpenapiSpecJsonBodyInfoLicense

        d = src_dict.copy()
        title = d.pop("title")

        version = d.pop("version")

        description = d.pop("description", UNSET)

        terms_of_service = d.pop("terms_of_service", UNSET)

        _contact = d.pop("contact", UNSET)
        contact: Union[Unset, GenerateOpenapiSpecJsonBodyInfoContact]
        if isinstance(_contact, Unset):
            contact = UNSET
        else:
            contact = GenerateOpenapiSpecJsonBodyInfoContact.from_dict(_contact)

        _license_ = d.pop("license", UNSET)
        license_: Union[Unset, GenerateOpenapiSpecJsonBodyInfoLicense]
        if isinstance(_license_, Unset):
            license_ = UNSET
        else:
            license_ = GenerateOpenapiSpecJsonBodyInfoLicense.from_dict(_license_)

        generate_openapi_spec_json_body_info = cls(
            title=title,
            version=version,
            description=description,
            terms_of_service=terms_of_service,
            contact=contact,
            license_=license_,
        )

        generate_openapi_spec_json_body_info.additional_properties = d
        return generate_openapi_spec_json_body_info

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
