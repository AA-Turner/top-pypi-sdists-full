from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkspaceOffboardPreviewPreviewTokensItem")


@_attrs_define
class WorkspaceOffboardPreviewPreviewTokensItem:
    """
    Attributes:
        label (str):
        scopes (List[str]):
        expiration (Union[Unset, str]):
    """

    label: str
    scopes: List[str]
    expiration: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        label = self.label
        scopes = self.scopes

        expiration = self.expiration

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "scopes": scopes,
            }
        )
        if expiration is not UNSET:
            field_dict["expiration"] = expiration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label")

        scopes = cast(List[str], d.pop("scopes"))

        expiration = d.pop("expiration", UNSET)

        workspace_offboard_preview_preview_tokens_item = cls(
            label=label,
            scopes=scopes,
            expiration=expiration,
        )

        workspace_offboard_preview_preview_tokens_item.additional_properties = d
        return workspace_offboard_preview_preview_tokens_item

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
