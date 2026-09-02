from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetMcpToolsResponse200ItemAnnotations")


@_attrs_define
class GetMcpToolsResponse200ItemAnnotations:
    """
    Attributes:
        title (Union[Unset, str]):
        read_only_hint (Union[Unset, bool]):
        destructive_hint (Union[Unset, bool]):
        idempotent_hint (Union[Unset, bool]):
        open_world_hint (Union[Unset, bool]):
    """

    title: Union[Unset, str] = UNSET
    read_only_hint: Union[Unset, bool] = UNSET
    destructive_hint: Union[Unset, bool] = UNSET
    idempotent_hint: Union[Unset, bool] = UNSET
    open_world_hint: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        read_only_hint = self.read_only_hint
        destructive_hint = self.destructive_hint
        idempotent_hint = self.idempotent_hint
        open_world_hint = self.open_world_hint

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if title is not UNSET:
            field_dict["title"] = title
        if read_only_hint is not UNSET:
            field_dict["readOnlyHint"] = read_only_hint
        if destructive_hint is not UNSET:
            field_dict["destructiveHint"] = destructive_hint
        if idempotent_hint is not UNSET:
            field_dict["idempotentHint"] = idempotent_hint
        if open_world_hint is not UNSET:
            field_dict["openWorldHint"] = open_world_hint

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title", UNSET)

        read_only_hint = d.pop("readOnlyHint", UNSET)

        destructive_hint = d.pop("destructiveHint", UNSET)

        idempotent_hint = d.pop("idempotentHint", UNSET)

        open_world_hint = d.pop("openWorldHint", UNSET)

        get_mcp_tools_response_200_item_annotations = cls(
            title=title,
            read_only_hint=read_only_hint,
            destructive_hint=destructive_hint,
            idempotent_hint=idempotent_hint,
            open_world_hint=open_world_hint,
        )

        get_mcp_tools_response_200_item_annotations.additional_properties = d
        return get_mcp_tools_response_200_item_annotations

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
