from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAppByVersionResponse200PolicyAllowedS3KeysItem")


@_attrs_define
class GetAppByVersionResponse200PolicyAllowedS3KeysItem:
    """
    Attributes:
        s3_path (Union[Unset, str]):
        resource (Union[Unset, str]):
    """

    s3_path: Union[Unset, str] = UNSET
    resource: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        s3_path = self.s3_path
        resource = self.resource

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if s3_path is not UNSET:
            field_dict["s3_path"] = s3_path
        if resource is not UNSET:
            field_dict["resource"] = resource

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        s3_path = d.pop("s3_path", UNSET)

        resource = d.pop("resource", UNSET)

        get_app_by_version_response_200_policy_allowed_s3_keys_item = cls(
            s3_path=s3_path,
            resource=resource,
        )

        get_app_by_version_response_200_policy_allowed_s3_keys_item.additional_properties = d
        return get_app_by_version_response_200_policy_allowed_s3_keys_item

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
