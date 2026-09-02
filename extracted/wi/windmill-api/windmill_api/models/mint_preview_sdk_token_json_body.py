from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MintPreviewSdkTokenJsonBody")


@_attrs_define
class MintPreviewSdkTokenJsonBody:
    """
    Attributes:
        path (str): App being edited; may not be deployed yet.
        scopes (List[str]): Scopes from the policy being edited. Capped by the curated allowlist and by the caller's own
            scopes, and minted as the caller, so it grants nothing they could not mint themselves.
    """

    path: str
    scopes: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        scopes = self.scopes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "scopes": scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        scopes = cast(List[str], d.pop("scopes"))

        mint_preview_sdk_token_json_body = cls(
            path=path,
            scopes=scopes,
        )

        mint_preview_sdk_token_json_body.additional_properties = d
        return mint_preview_sdk_token_json_body

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
