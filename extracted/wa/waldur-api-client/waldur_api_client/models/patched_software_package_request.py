from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedSoftwarePackageRequest")


@_attrs_define
class PatchedSoftwarePackageRequest:
    """
    Attributes:
        catalog (Union[Unset, str]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        homepage (Union[None, Unset, str]):
        categories (Union[Unset, Any]): Package categories (e.g., ['bio', 'hpc', 'build-tools'])
        licenses (Union[Unset, Any]): Software licenses (e.g., ['GPL-3.0', 'MIT'])
        maintainers (Union[Unset, Any]): Package maintainers
        is_extension (Union[Unset, bool]): Whether this package is an extension of another package
    """

    catalog: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    homepage: Union[None, Unset, str] = UNSET
    categories: Union[Unset, Any] = UNSET
    licenses: Union[Unset, Any] = UNSET
    maintainers: Union[Unset, Any] = UNSET
    is_extension: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        catalog = self.catalog

        name = self.name

        description = self.description

        homepage: Union[None, Unset, str]
        if isinstance(self.homepage, Unset):
            homepage = UNSET
        else:
            homepage = self.homepage

        categories = self.categories

        licenses = self.licenses

        maintainers = self.maintainers

        is_extension = self.is_extension

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if catalog is not UNSET:
            field_dict["catalog"] = catalog
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if homepage is not UNSET:
            field_dict["homepage"] = homepage
        if categories is not UNSET:
            field_dict["categories"] = categories
        if licenses is not UNSET:
            field_dict["licenses"] = licenses
        if maintainers is not UNSET:
            field_dict["maintainers"] = maintainers
        if is_extension is not UNSET:
            field_dict["is_extension"] = is_extension

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        catalog = d.pop("catalog", UNSET)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        def _parse_homepage(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        homepage = _parse_homepage(d.pop("homepage", UNSET))

        categories = d.pop("categories", UNSET)

        licenses = d.pop("licenses", UNSET)

        maintainers = d.pop("maintainers", UNSET)

        is_extension = d.pop("is_extension", UNSET)

        patched_software_package_request = cls(
            catalog=catalog,
            name=name,
            description=description,
            homepage=homepage,
            categories=categories,
            licenses=licenses,
            maintainers=maintainers,
            is_extension=is_extension,
        )

        patched_software_package_request.additional_properties = d
        return patched_software_package_request

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
