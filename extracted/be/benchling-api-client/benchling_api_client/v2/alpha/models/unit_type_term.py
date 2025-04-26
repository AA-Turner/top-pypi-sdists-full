from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.unit_type_term_value import UnitTypeTermValue
from ..types import UNSET, Unset

T = TypeVar("T", bound="UnitTypeTerm")


@attr.s(auto_attribs=True, repr=False)
class UnitTypeTerm:
    """  """

    _exponent: Union[Unset, int] = UNSET
    _value: Union[Unset, UnitTypeTermValue] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("exponent={}".format(repr(self._exponent)))
        fields.append("value={}".format(repr(self._value)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "UnitTypeTerm({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        exponent = self._exponent
        value: Union[Unset, int] = UNSET
        if not isinstance(self._value, Unset):
            value = self._value.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if exponent is not UNSET:
            field_dict["exponent"] = exponent
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_exponent() -> Union[Unset, int]:
            exponent = d.pop("exponent")
            return exponent

        try:
            exponent = get_exponent()
        except KeyError:
            if strict:
                raise
            exponent = cast(Union[Unset, int], UNSET)

        def get_value() -> Union[Unset, UnitTypeTermValue]:
            value = UNSET
            _value = d.pop("value")
            if _value is not None and _value is not UNSET:
                try:
                    value = UnitTypeTermValue(_value)
                except ValueError:
                    value = UnitTypeTermValue.of_unknown(_value)

            return value

        try:
            value = get_value()
        except KeyError:
            if strict:
                raise
            value = cast(Union[Unset, UnitTypeTermValue], UNSET)

        unit_type_term = cls(
            exponent=exponent,
            value=value,
        )

        unit_type_term.additional_properties = d
        return unit_type_term

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
    def exponent(self) -> int:
        if isinstance(self._exponent, Unset):
            raise NotPresentError(self, "exponent")
        return self._exponent

    @exponent.setter
    def exponent(self, value: int) -> None:
        self._exponent = value

    @exponent.deleter
    def exponent(self) -> None:
        self._exponent = UNSET

    @property
    def value(self) -> UnitTypeTermValue:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: UnitTypeTermValue) -> None:
        self._value = value

    @value.deleter
    def value(self) -> None:
        self._value = UNSET
