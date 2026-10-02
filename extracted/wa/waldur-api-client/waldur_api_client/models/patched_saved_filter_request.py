from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.patched_saved_filter_request_filter_params import PatchedSavedFilterRequestFilterParams


T = TypeVar("T", bound="PatchedSavedFilterRequest")


@_attrs_define
class PatchedSavedFilterRequest:
    """
    Attributes:
        name (Union[Unset, str]):
        filter_params (Union[Unset, PatchedSavedFilterRequestFilterParams]): Saved filter parameters as JSON.
        is_shared (Union[Unset, bool]): If True, visible to all staff/support users.
    """

    name: Union[Unset, str] = UNSET
    filter_params: Union[Unset, "PatchedSavedFilterRequestFilterParams"] = UNSET
    is_shared: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        is_shared = self.is_shared

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.patched_saved_filter_request_filter_params import PatchedSavedFilterRequestFilterParams

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        _filter_params = d.pop("filter_params", UNSET)
        filter_params: Union[Unset, PatchedSavedFilterRequestFilterParams]
        if isinstance(_filter_params, Unset):
            filter_params = UNSET
        else:
            filter_params = PatchedSavedFilterRequestFilterParams.from_dict(_filter_params)

        is_shared = d.pop("is_shared", UNSET)

        patched_saved_filter_request = cls(
            name=name,
            filter_params=filter_params,
            is_shared=is_shared,
        )

        patched_saved_filter_request.additional_properties = d
        return patched_saved_filter_request

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
