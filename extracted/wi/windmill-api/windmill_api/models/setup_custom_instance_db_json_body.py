from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.setup_custom_instance_db_json_body_tag import SetupCustomInstanceDbJsonBodyTag
from ..types import UNSET, Unset

T = TypeVar("T", bound="SetupCustomInstanceDbJsonBody")


@_attrs_define
class SetupCustomInstanceDbJsonBody:
    """
    Attributes:
        tag (Union[Unset, SetupCustomInstanceDbJsonBodyTag]):
    """

    tag: Union[Unset, SetupCustomInstanceDbJsonBodyTag] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        tag: Union[Unset, str] = UNSET
        if not isinstance(self.tag, Unset):
            tag = self.tag.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if tag is not UNSET:
            field_dict["tag"] = tag

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _tag = d.pop("tag", UNSET)
        tag: Union[Unset, SetupCustomInstanceDbJsonBodyTag]
        if isinstance(_tag, Unset):
            tag = UNSET
        else:
            tag = SetupCustomInstanceDbJsonBodyTag(_tag)

        setup_custom_instance_db_json_body = cls(
            tag=tag,
        )

        setup_custom_instance_db_json_body.additional_properties = d
        return setup_custom_instance_db_json_body

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
