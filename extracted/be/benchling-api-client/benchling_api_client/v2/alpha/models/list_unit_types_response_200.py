from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.unit_type import UnitType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListUnitTypesResponse_200")


@attr.s(auto_attribs=True, repr=False)
class ListUnitTypesResponse_200:
    """  """

    _next_token: Union[Unset, str] = UNSET
    _unit_types: Union[Unset, List[UnitType]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("unit_types={}".format(repr(self._unit_types)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ListUnitTypesResponse_200({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token
        unit_types: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._unit_types, Unset):
            unit_types = []
            for unit_types_item_data in self._unit_types:
                unit_types_item = unit_types_item_data.to_dict()

                unit_types.append(unit_types_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token
        if unit_types is not UNSET:
            field_dict["unitTypes"] = unit_types

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        def get_unit_types() -> Union[Unset, List[UnitType]]:
            unit_types = []
            _unit_types = d.pop("unitTypes")
            for unit_types_item_data in _unit_types or []:
                unit_types_item = UnitType.from_dict(unit_types_item_data, strict=False)

                unit_types.append(unit_types_item)

            return unit_types

        try:
            unit_types = get_unit_types()
        except KeyError:
            if strict:
                raise
            unit_types = cast(Union[Unset, List[UnitType]], UNSET)

        list_unit_types_response_200 = cls(
            next_token=next_token,
            unit_types=unit_types,
        )

        list_unit_types_response_200.additional_properties = d
        return list_unit_types_response_200

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
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET

    @property
    def unit_types(self) -> List[UnitType]:
        if isinstance(self._unit_types, Unset):
            raise NotPresentError(self, "unit_types")
        return self._unit_types

    @unit_types.setter
    def unit_types(self, value: List[UnitType]) -> None:
        self._unit_types = value

    @unit_types.deleter
    def unit_types(self) -> None:
        self._unit_types = UNSET
