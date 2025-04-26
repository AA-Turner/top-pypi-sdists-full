from typing import Any, cast, Dict, List, Optional, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.app_config_item_integer_update_type import AppConfigItemIntegerUpdateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppConfigItemIntegerUpdate")


@attr.s(auto_attribs=True, repr=False)
class AppConfigItemIntegerUpdate:
    """  """

    _type: AppConfigItemIntegerUpdateType
    _value: Optional[int]
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("value={}".format(repr(self._value)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AppConfigItemIntegerUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        value = self._value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> AppConfigItemIntegerUpdateType:
            _type = d.pop("type")
            try:
                type = AppConfigItemIntegerUpdateType(_type)
            except ValueError:
                type = AppConfigItemIntegerUpdateType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(AppConfigItemIntegerUpdateType, UNSET)

        def get_value() -> Optional[int]:
            value = d.pop("value")
            return value

        try:
            value = get_value()
        except KeyError:
            if strict:
                raise
            value = cast(Optional[int], UNSET)

        app_config_item_integer_update = cls(
            type=type,
            value=value,
        )

        app_config_item_integer_update.additional_properties = d
        return app_config_item_integer_update

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
    def type(self) -> AppConfigItemIntegerUpdateType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: AppConfigItemIntegerUpdateType) -> None:
        self._type = value

    @property
    def value(self) -> Optional[int]:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: Optional[int]) -> None:
        self._value = value
