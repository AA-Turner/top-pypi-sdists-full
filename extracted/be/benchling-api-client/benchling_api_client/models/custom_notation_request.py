from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotationRequest")


@attr.s(auto_attribs=True, repr=False)
class CustomNotationRequest:
    """  """

    _custom_notation: Union[Unset, str] = UNSET
    _custom_notation_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("custom_notation={}".format(repr(self._custom_notation)))
        fields.append("custom_notation_id={}".format(repr(self._custom_notation_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CustomNotationRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        custom_notation = self._custom_notation
        custom_notation_id = self._custom_notation_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if custom_notation is not UNSET:
            field_dict["customNotation"] = custom_notation
        if custom_notation_id is not UNSET:
            field_dict["customNotationId"] = custom_notation_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_custom_notation() -> Union[Unset, str]:
            custom_notation = d.pop("customNotation")
            return custom_notation

        try:
            custom_notation = get_custom_notation()
        except KeyError:
            if strict:
                raise
            custom_notation = cast(Union[Unset, str], UNSET)

        def get_custom_notation_id() -> Union[Unset, str]:
            custom_notation_id = d.pop("customNotationId")
            return custom_notation_id

        try:
            custom_notation_id = get_custom_notation_id()
        except KeyError:
            if strict:
                raise
            custom_notation_id = cast(Union[Unset, str], UNSET)

        custom_notation_request = cls(
            custom_notation=custom_notation,
            custom_notation_id=custom_notation_id,
        )

        custom_notation_request.additional_properties = d
        return custom_notation_request

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
    def custom_notation(self) -> str:
        """ Representation of the sequence or oligo in the custom notation specified by customNotationId """
        if isinstance(self._custom_notation, Unset):
            raise NotPresentError(self, "custom_notation")
        return self._custom_notation

    @custom_notation.setter
    def custom_notation(self, value: str) -> None:
        self._custom_notation = value

    @custom_notation.deleter
    def custom_notation(self) -> None:
        self._custom_notation = UNSET

    @property
    def custom_notation_id(self) -> str:
        """ ID of the notation used to interpret the string provided in the customNotation field """
        if isinstance(self._custom_notation_id, Unset):
            raise NotPresentError(self, "custom_notation_id")
        return self._custom_notation_id

    @custom_notation_id.setter
    def custom_notation_id(self, value: str) -> None:
        self._custom_notation_id = value

    @custom_notation_id.deleter
    def custom_notation_id(self) -> None:
        self._custom_notation_id = UNSET
