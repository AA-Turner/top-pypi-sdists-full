from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_dependents_response_200_item_importer_kind import GetDependentsResponse200ItemImporterKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetDependentsResponse200Item")


@_attrs_define
class GetDependentsResponse200Item:
    """
    Attributes:
        importer_path (str):
        importer_kind (GetDependentsResponse200ItemImporterKind):
        importer_node_ids (Union[Unset, None, List[str]]):
    """

    importer_path: str
    importer_kind: GetDependentsResponse200ItemImporterKind
    importer_node_ids: Union[Unset, None, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        importer_path = self.importer_path
        importer_kind = self.importer_kind.value

        importer_node_ids: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.importer_node_ids, Unset):
            if self.importer_node_ids is None:
                importer_node_ids = None
            else:
                importer_node_ids = self.importer_node_ids

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "importer_path": importer_path,
                "importer_kind": importer_kind,
            }
        )
        if importer_node_ids is not UNSET:
            field_dict["importer_node_ids"] = importer_node_ids

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        importer_path = d.pop("importer_path")

        importer_kind = GetDependentsResponse200ItemImporterKind(d.pop("importer_kind"))

        importer_node_ids = cast(List[str], d.pop("importer_node_ids", UNSET))

        get_dependents_response_200_item = cls(
            importer_path=importer_path,
            importer_kind=importer_kind,
            importer_node_ids=importer_node_ids,
        )

        get_dependents_response_200_item.additional_properties = d
        return get_dependents_response_200_item

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
