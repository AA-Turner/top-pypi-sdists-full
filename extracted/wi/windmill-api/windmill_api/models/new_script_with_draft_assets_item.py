from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.new_script_with_draft_assets_item_access_type import NewScriptWithDraftAssetsItemAccessType
from ..models.new_script_with_draft_assets_item_alt_access_type import NewScriptWithDraftAssetsItemAltAccessType
from ..models.new_script_with_draft_assets_item_kind import NewScriptWithDraftAssetsItemKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="NewScriptWithDraftAssetsItem")


@_attrs_define
class NewScriptWithDraftAssetsItem:
    """
    Attributes:
        path (str):
        kind (NewScriptWithDraftAssetsItemKind):
        access_type (Union[Unset, NewScriptWithDraftAssetsItemAccessType]):
        alt_access_type (Union[Unset, NewScriptWithDraftAssetsItemAltAccessType]):
    """

    path: str
    kind: NewScriptWithDraftAssetsItemKind
    access_type: Union[Unset, NewScriptWithDraftAssetsItemAccessType] = UNSET
    alt_access_type: Union[Unset, NewScriptWithDraftAssetsItemAltAccessType] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        kind = self.kind.value

        access_type: Union[Unset, str] = UNSET
        if not isinstance(self.access_type, Unset):
            access_type = self.access_type.value

        alt_access_type: Union[Unset, str] = UNSET
        if not isinstance(self.alt_access_type, Unset):
            alt_access_type = self.alt_access_type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "kind": kind,
            }
        )
        if access_type is not UNSET:
            field_dict["access_type"] = access_type
        if alt_access_type is not UNSET:
            field_dict["alt_access_type"] = alt_access_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        kind = NewScriptWithDraftAssetsItemKind(d.pop("kind"))

        _access_type = d.pop("access_type", UNSET)
        access_type: Union[Unset, NewScriptWithDraftAssetsItemAccessType]
        if isinstance(_access_type, Unset):
            access_type = UNSET
        else:
            access_type = NewScriptWithDraftAssetsItemAccessType(_access_type)

        _alt_access_type = d.pop("alt_access_type", UNSET)
        alt_access_type: Union[Unset, NewScriptWithDraftAssetsItemAltAccessType]
        if isinstance(_alt_access_type, Unset):
            alt_access_type = UNSET
        else:
            alt_access_type = NewScriptWithDraftAssetsItemAltAccessType(_alt_access_type)

        new_script_with_draft_assets_item = cls(
            path=path,
            kind=kind,
            access_type=access_type,
            alt_access_type=alt_access_type,
        )

        new_script_with_draft_assets_item.additional_properties = d
        return new_script_with_draft_assets_item

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
