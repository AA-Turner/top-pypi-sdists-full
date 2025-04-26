from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.chip_ui_block_type import ChipUiBlockType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChipUiBlock")


@attr.s(auto_attribs=True, repr=False)
class ChipUiBlock:
    """  """

    _type: ChipUiBlockType
    _value: str
    _id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("type={}".format(repr(self._type)))
        fields.append("value={}".format(repr(self._value)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ChipUiBlock({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        type = self._type.value

        value = self._value
        id = self._id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_type() -> ChipUiBlockType:
            _type = d.pop("type")
            try:
                type = ChipUiBlockType(_type)
            except ValueError:
                type = ChipUiBlockType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(ChipUiBlockType, UNSET)

        def get_value() -> str:
            value = d.pop("value")
            return value

        try:
            value = get_value()
        except KeyError:
            if strict:
                raise
            value = cast(str, UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        chip_ui_block = cls(
            type=type,
            value=value,
            id=id,
        )

        chip_ui_block.additional_properties = d
        return chip_ui_block

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
    def type(self) -> ChipUiBlockType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: ChipUiBlockType) -> None:
        self._type = value

    @property
    def value(self) -> str:
        if isinstance(self._value, Unset):
            raise NotPresentError(self, "value")
        return self._value

    @value.setter
    def value(self, value: str) -> None:
        self._value = value

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
