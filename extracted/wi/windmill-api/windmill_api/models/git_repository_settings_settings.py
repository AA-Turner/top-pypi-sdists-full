from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.git_repository_settings_settings_include_type_item import GitRepositorySettingsSettingsIncludeTypeItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="GitRepositorySettingsSettings")


@_attrs_define
class GitRepositorySettingsSettings:
    """
    Attributes:
        include_path (Union[Unset, List[str]]):
        include_type (Union[Unset, List[GitRepositorySettingsSettingsIncludeTypeItem]]):
        exclude_path (Union[Unset, List[str]]):
        extra_include_path (Union[Unset, List[str]]):
    """

    include_path: Union[Unset, List[str]] = UNSET
    include_type: Union[Unset, List[GitRepositorySettingsSettingsIncludeTypeItem]] = UNSET
    exclude_path: Union[Unset, List[str]] = UNSET
    extra_include_path: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        include_path: Union[Unset, List[str]] = UNSET
        if not isinstance(self.include_path, Unset):
            include_path = self.include_path

        include_type: Union[Unset, List[str]] = UNSET
        if not isinstance(self.include_type, Unset):
            include_type = []
            for include_type_item_data in self.include_type:
                include_type_item = include_type_item_data.value

                include_type.append(include_type_item)

        exclude_path: Union[Unset, List[str]] = UNSET
        if not isinstance(self.exclude_path, Unset):
            exclude_path = self.exclude_path

        extra_include_path: Union[Unset, List[str]] = UNSET
        if not isinstance(self.extra_include_path, Unset):
            extra_include_path = self.extra_include_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if include_path is not UNSET:
            field_dict["include_path"] = include_path
        if include_type is not UNSET:
            field_dict["include_type"] = include_type
        if exclude_path is not UNSET:
            field_dict["exclude_path"] = exclude_path
        if extra_include_path is not UNSET:
            field_dict["extra_include_path"] = extra_include_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        include_path = cast(List[str], d.pop("include_path", UNSET))

        include_type = []
        _include_type = d.pop("include_type", UNSET)
        for include_type_item_data in _include_type or []:
            include_type_item = GitRepositorySettingsSettingsIncludeTypeItem(include_type_item_data)

            include_type.append(include_type_item)

        exclude_path = cast(List[str], d.pop("exclude_path", UNSET))

        extra_include_path = cast(List[str], d.pop("extra_include_path", UNSET))

        git_repository_settings_settings = cls(
            include_path=include_path,
            include_type=include_type,
            exclude_path=exclude_path,
            extra_include_path=extra_include_path,
        )

        git_repository_settings_settings.additional_properties = d
        return git_repository_settings_settings

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
