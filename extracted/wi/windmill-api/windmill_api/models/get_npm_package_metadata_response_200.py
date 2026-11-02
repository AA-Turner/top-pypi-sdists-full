from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_npm_package_metadata_response_200_tags import GetNpmPackageMetadataResponse200Tags


T = TypeVar("T", bound="GetNpmPackageMetadataResponse200")


@_attrs_define
class GetNpmPackageMetadataResponse200:
    """
    Attributes:
        tags (Union[Unset, GetNpmPackageMetadataResponse200Tags]):
        versions (Union[Unset, List[str]]):
    """

    tags: Union[Unset, "GetNpmPackageMetadataResponse200Tags"] = UNSET
    versions: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        versions: Union[Unset, List[str]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = self.versions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tags is not UNSET:
            field_dict["tags"] = tags
        if versions is not UNSET:
            field_dict["versions"] = versions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_npm_package_metadata_response_200_tags import GetNpmPackageMetadataResponse200Tags

        d = src_dict.copy()
        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, GetNpmPackageMetadataResponse200Tags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = GetNpmPackageMetadataResponse200Tags.from_dict(_tags)

        versions = cast(List[str], d.pop("versions", UNSET))

        get_npm_package_metadata_response_200 = cls(
            tags=tags,
            versions=versions,
        )

        get_npm_package_metadata_response_200.additional_properties = d
        return get_npm_package_metadata_response_200

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
