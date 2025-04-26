from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.dropdown_multi_value_ui_block_type import DropdownMultiValueUiBlockType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DropdownMultiValueUiBlockUpdate")


@attr.s(auto_attribs=True, repr=False)
class DropdownMultiValueUiBlockUpdate:
    """  """

    _id: str
    _type: Union[Unset, DropdownMultiValueUiBlockType] = UNSET
    _dropdown_id: Union[Unset, str] = UNSET
    _label: Union[Unset, None, str] = UNSET
    _value: Union[Unset, None, List[str]] = UNSET
    _enabled: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("dropdown_id={}".format(repr(self._dropdown_id)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("value={}".format(repr(self._value)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DropdownMultiValueUiBlockUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        dropdown_id = self._dropdown_id
        label = self._label
        value: Union[Unset, None, List[Any]] = UNSET
        if not isinstance(self._value, Unset):
            if self._value is None:
                value = None
            else:
                value = self._value

        enabled = self._enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if type is not UNSET:
            field_dict["type"] = type
        if dropdown_id is not UNSET:
            field_dict["dropdownId"] = dropdown_id
        if label is not UNSET:
            field_dict["label"] = label
        if value is not UNSET:
            field_dict["value"] = value
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_type() -> Union[Unset, DropdownMultiValueUiBlockType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = DropdownMultiValueUiBlockType(_type)
                except ValueError:
                    type = DropdownMultiValueUiBlockType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, DropdownMultiValueUiBlockType], UNSET)

        def get_dropdown_id() -> Union[Unset, str]:
            dropdown_id = d.pop("dropdownId")
            return dropdown_id

        try:
            dropdown_id = get_dropdown_id()
        except KeyError:
            if strict:
                raise
            dropdown_id = cast(Union[Unset, str], UNSET)

        def get_label() -> Union[Unset, None, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, None, str], UNSET)

        def get_value() -> Union[Unset, None, List[str]]:
            value = cast(List[str], d.pop("value"))

            return value

        try:
            value = get_value()
        except KeyError:
            if strict:
                raise
            value = cast(Union[Unset, None, List[str]], UNSET)

        def get_enabled() -> Union[Unset, None, bool]:
            enabled = d.pop("enabled")
            return enabled

        try:
            enabled = get_enabled()
        except KeyError:
            if strict:
                raise
            enabled = cast(Union[Unset, None, bool], UNSET)

        dropdown_multi_value_ui_block_update = cls(
            id=id,
            type=type,
            dropdown_id=dropdown_id,
            label=label,
            value=value,
            enabled=enabled,
        )

        dropdown_multi_value_ui_block_update.additional_properties = d
        return dropdown_multi_value_ui_block_update

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def type(self) -> DropdownMultiValueUiBlockType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: DropdownMultiValueUiBlockType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def dropdown_id(self) -> str:
        if isinstance(self._dropdown_id, Unset):
            raise NotPresentError(self, "dropdown_id")
        return self._dropdown_id

    @dropdown_id.setter
    def dropdown_id(self, value: str) -> None:
        self._dropdown_id = value

    @dropdown_id.deleter
    def dropdown_id(self) -> None:
        self._dropdown_id = UNSET

    @property
    def label(self) -> Optional[str]:
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: Optional[str]) -> None:
        self._label = value

    @label.deleter
    def label(self) -> None:
        self._label = UNSET

    @property
    def value(self) -> Optional[List[str]]:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: Optional[List[str]]) -> None:
        self._value = value

    @value.deleter
    def value(self) -> None:
        self._value = UNSET

    @property
    def enabled(self) -> Optional[bool]:
        if isinstance(self._enabled, Unset):
            raise NotPresentError(self, "enabled")
        return self._enabled

    @enabled.setter
    def enabled(self, value: Optional[bool]) -> None:
        self._enabled = value

    @enabled.deleter
    def enabled(self) -> None:
        self._enabled = UNSET
