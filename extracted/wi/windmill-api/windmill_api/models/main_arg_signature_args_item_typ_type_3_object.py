from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.main_arg_signature_args_item_typ_type_3_object_props_item import (
        MainArgSignatureArgsItemTypType3ObjectPropsItem,
    )


T = TypeVar("T", bound="MainArgSignatureArgsItemTypType3Object")


@_attrs_define
class MainArgSignatureArgsItemTypType3Object:
    """
    Attributes:
        name (Union[Unset, str]):
        props (Union[Unset, List['MainArgSignatureArgsItemTypType3ObjectPropsItem']]):
    """

    name: Union[Unset, str] = UNSET
    props: Union[Unset, List["MainArgSignatureArgsItemTypType3ObjectPropsItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        props: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.props, Unset):
            props = []
            for props_item_data in self.props:
                props_item = props_item_data.to_dict()

                props.append(props_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if props is not UNSET:
            field_dict["props"] = props

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.main_arg_signature_args_item_typ_type_3_object_props_item import (
            MainArgSignatureArgsItemTypType3ObjectPropsItem,
        )

        d = src_dict.copy()
        name = d.pop("name", UNSET)

        props = []
        _props = d.pop("props", UNSET)
        for props_item_data in _props or []:
            props_item = MainArgSignatureArgsItemTypType3ObjectPropsItem.from_dict(props_item_data)

            props.append(props_item)

        main_arg_signature_args_item_typ_type_3_object = cls(
            name=name,
            props=props,
        )

        main_arg_signature_args_item_typ_type_3_object.additional_properties = d
        return main_arg_signature_args_item_typ_type_3_object

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
