from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.draft_item_ref_kind import DraftItemRefKind

T = TypeVar("T", bound="DraftItemRef")


@_attrs_define
class DraftItemRef:
    """
    Attributes:
        kind (DraftItemRefKind): Closed set of item kinds a user can autosave as a draft. Mirrors the
            Postgres `DRAFT_KIND` enum and the backend `UserDraftItemKind`.
        path (str):
    """

    kind: DraftItemRefKind
    path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        kind = DraftItemRefKind(d.pop("kind"))

        path = d.pop("path")

        draft_item_ref = cls(
            kind=kind,
            path=path,
        )

        draft_item_ref.additional_properties = d
        return draft_item_ref

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
