from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="UnitSummary")


@attr.s(auto_attribs=True, repr=False)
class UnitSummary:
    """  """

    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _symbol: Union[Unset, str] = UNSET
    _unit_type_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("symbol={}".format(repr(self._symbol)))
        fields.append("unit_type_id={}".format(repr(self._unit_type_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "UnitSummary({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        name = self._name
        symbol = self._symbol
        unit_type_id = self._unit_type_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if symbol is not UNSET:
            field_dict["symbol"] = symbol
        if unit_type_id is not UNSET:
            field_dict["unitTypeId"] = unit_type_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_symbol() -> Union[Unset, str]:
            symbol = d.pop("symbol")
            return symbol

        try:
            symbol = get_symbol()
        except KeyError:
            if strict:
                raise
            symbol = cast(Union[Unset, str], UNSET)

        def get_unit_type_id() -> Union[Unset, str]:
            unit_type_id = d.pop("unitTypeId")
            return unit_type_id

        try:
            unit_type_id = get_unit_type_id()
        except KeyError:
            if strict:
                raise
            unit_type_id = cast(Union[Unset, str], UNSET)

        unit_summary = cls(
            id=id,
            name=name,
            symbol=symbol,
            unit_type_id=unit_type_id,
        )

        unit_summary.additional_properties = d
        return unit_summary

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

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def symbol(self) -> str:
        if isinstance(self._symbol, Unset):
            raise NotPresentError(self, "symbol")
        return self._symbol

    @symbol.setter
    def symbol(self, value: str) -> None:
        self._symbol = value

    @symbol.deleter
    def symbol(self) -> None:
        self._symbol = UNSET

    @property
    def unit_type_id(self) -> str:
        if isinstance(self._unit_type_id, Unset):
            raise NotPresentError(self, "unit_type_id")
        return self._unit_type_id

    @unit_type_id.setter
    def unit_type_id(self, value: str) -> None:
        self._unit_type_id = value

    @unit_type_id.deleter
    def unit_type_id(self) -> None:
        self._unit_type_id = UNSET
