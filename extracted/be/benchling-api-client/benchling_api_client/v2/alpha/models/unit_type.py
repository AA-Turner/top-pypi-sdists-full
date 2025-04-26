from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.unit import Unit
from ..models.unit_type_term import UnitTypeTerm
from ..types import UNSET, Unset

T = TypeVar("T", bound="UnitType")


@attr.s(auto_attribs=True, repr=False)
class UnitType:
    """  """

    _base_unit: Union[Unset, Unit] = UNSET
    _id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _terms: Union[Unset, List[UnitTypeTerm]] = UNSET
    _units: Union[Unset, List[Unit]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("base_unit={}".format(repr(self._base_unit)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("terms={}".format(repr(self._terms)))
        fields.append("units={}".format(repr(self._units)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "UnitType({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        base_unit: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._base_unit, Unset):
            base_unit = self._base_unit.to_dict()

        id = self._id
        name = self._name
        terms: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._terms, Unset):
            terms = []
            for terms_item_data in self._terms:
                terms_item = terms_item_data.to_dict()

                terms.append(terms_item)

        units: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._units, Unset):
            units = []
            for units_item_data in self._units:
                units_item = units_item_data.to_dict()

                units.append(units_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if base_unit is not UNSET:
            field_dict["baseUnit"] = base_unit
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if terms is not UNSET:
            field_dict["terms"] = terms
        if units is not UNSET:
            field_dict["units"] = units

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_base_unit() -> Union[Unset, Unit]:
            base_unit: Union[Unset, Union[Unset, Unit]] = UNSET
            _base_unit = d.pop("baseUnit")

            if not isinstance(_base_unit, Unset):
                base_unit = Unit.from_dict(_base_unit)

            return base_unit

        try:
            base_unit = get_base_unit()
        except KeyError:
            if strict:
                raise
            base_unit = cast(Union[Unset, Unit], UNSET)

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

        def get_terms() -> Union[Unset, List[UnitTypeTerm]]:
            terms = []
            _terms = d.pop("terms")
            for terms_item_data in _terms or []:
                terms_item = UnitTypeTerm.from_dict(terms_item_data, strict=False)

                terms.append(terms_item)

            return terms

        try:
            terms = get_terms()
        except KeyError:
            if strict:
                raise
            terms = cast(Union[Unset, List[UnitTypeTerm]], UNSET)

        def get_units() -> Union[Unset, List[Unit]]:
            units = []
            _units = d.pop("units")
            for units_item_data in _units or []:
                units_item = Unit.from_dict(units_item_data, strict=False)

                units.append(units_item)

            return units

        try:
            units = get_units()
        except KeyError:
            if strict:
                raise
            units = cast(Union[Unset, List[Unit]], UNSET)

        unit_type = cls(
            base_unit=base_unit,
            id=id,
            name=name,
            terms=terms,
            units=units,
        )

        unit_type.additional_properties = d
        return unit_type

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
    def base_unit(self) -> Unit:
        if isinstance(self._base_unit, Unset):
            raise NotPresentError(self, "base_unit")
        return self._base_unit

    @base_unit.setter
    def base_unit(self, value: Unit) -> None:
        self._base_unit = value

    @base_unit.deleter
    def base_unit(self) -> None:
        self._base_unit = UNSET

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
    def terms(self) -> List[UnitTypeTerm]:
        if isinstance(self._terms, Unset):
            raise NotPresentError(self, "terms")
        return self._terms

    @terms.setter
    def terms(self, value: List[UnitTypeTerm]) -> None:
        self._terms = value

    @terms.deleter
    def terms(self) -> None:
        self._terms = UNSET

    @property
    def units(self) -> List[Unit]:
        if isinstance(self._units, Unset):
            raise NotPresentError(self, "units")
        return self._units

    @units.setter
    def units(self, value: List[Unit]) -> None:
        self._units = value

    @units.deleter
    def units(self) -> None:
        self._units = UNSET
