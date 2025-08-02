from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.main_arg_signature_args_item_typ_type_3_object import MainArgSignatureArgsItemTypType3Object


T = TypeVar("T", bound="MainArgSignatureArgsItemTypType3")


@_attrs_define
class MainArgSignatureArgsItemTypType3:
    """
    Attributes:
        object_ (MainArgSignatureArgsItemTypType3Object):
    """

    object_: "MainArgSignatureArgsItemTypType3Object"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        object_ = self.object_.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "object": object_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.main_arg_signature_args_item_typ_type_3_object import MainArgSignatureArgsItemTypType3Object

        d = src_dict.copy()
        object_ = MainArgSignatureArgsItemTypType3Object.from_dict(d.pop("object"))

        main_arg_signature_args_item_typ_type_3 = cls(
            object_=object_,
        )

        main_arg_signature_args_item_typ_type_3.additional_properties = d
        return main_arg_signature_args_item_typ_type_3

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
