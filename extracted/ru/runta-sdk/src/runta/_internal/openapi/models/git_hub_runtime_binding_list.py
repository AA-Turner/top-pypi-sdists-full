from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.git_hub_runtime_binding import GitHubRuntimeBinding


T = TypeVar("T", bound="GitHubRuntimeBindingList")


@_attrs_define
class GitHubRuntimeBindingList:
    """
    Attributes:
        bindings (list[GitHubRuntimeBinding]):
    """

    bindings: list[GitHubRuntimeBinding]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        bindings = []
        for bindings_item_data in self.bindings:
            bindings_item = bindings_item_data.to_dict()
            bindings.append(bindings_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "bindings": bindings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_runtime_binding import GitHubRuntimeBinding

        d = dict(src_dict)
        bindings = []
        _bindings = d.pop("bindings")
        for bindings_item_data in _bindings:
            bindings_item = GitHubRuntimeBinding.from_dict(bindings_item_data)

            bindings.append(bindings_item)

        git_hub_runtime_binding_list = cls(
            bindings=bindings,
        )

        git_hub_runtime_binding_list.additional_properties = d
        return git_hub_runtime_binding_list

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
