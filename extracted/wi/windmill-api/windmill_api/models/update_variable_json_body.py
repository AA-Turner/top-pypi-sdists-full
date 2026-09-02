from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateVariableJsonBody")


@_attrs_define
class UpdateVariableJsonBody:
    """
    Attributes:
        path (Union[Unset, str]): The path to the variable
        value (Union[Unset, str]): The new value of the variable
        is_secret (Union[Unset, bool]): Whether the variable is a secret
        description (Union[Unset, str]): The new description of the variable
        labels (Union[Unset, List[str]]):
        ws_specific (Union[Unset, bool]):
    """

    path: Union[Unset, str] = UNSET
    value: Union[Unset, str] = UNSET
    is_secret: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    ws_specific: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value
        is_secret = self.is_secret
        description = self.description
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        ws_specific = self.ws_specific

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if path is not UNSET:
            field_dict["path"] = path
        if value is not UNSET:
            field_dict["value"] = value
        if is_secret is not UNSET:
            field_dict["is_secret"] = is_secret
        if description is not UNSET:
            field_dict["description"] = description
        if labels is not UNSET:
            field_dict["labels"] = labels
        if ws_specific is not UNSET:
            field_dict["ws_specific"] = ws_specific

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path", UNSET)

        value = d.pop("value", UNSET)

        is_secret = d.pop("is_secret", UNSET)

        description = d.pop("description", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        ws_specific = d.pop("ws_specific", UNSET)

        update_variable_json_body = cls(
            path=path,
            value=value,
            is_secret=is_secret,
            description=description,
            labels=labels,
            ws_specific=ws_specific,
        )

        update_variable_json_body.additional_properties = d
        return update_variable_json_body

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
