from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotationCreateUseSharedDelimiter")


@attr.s(auto_attribs=True, repr=False)
class CustomNotationCreateUseSharedDelimiter:
    """ By default the system assumes that all delimiters "belong" to a single token (such as in a notation like "[A][B][C]"). This setting allows specifying a single "shared" delimiter instead, e.g. the commas in "A,B,C". """

    _delimiter: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("delimiter={}".format(repr(self._delimiter)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CustomNotationCreateUseSharedDelimiter({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        delimiter = self._delimiter

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if delimiter is not UNSET:
            field_dict["delimiter"] = delimiter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_delimiter() -> Union[Unset, str]:
            delimiter = d.pop("delimiter")
            return delimiter

        try:
            delimiter = get_delimiter()
        except KeyError:
            if strict:
                raise
            delimiter = cast(Union[Unset, str], UNSET)

        custom_notation_create_use_shared_delimiter = cls(
            delimiter=delimiter,
        )

        custom_notation_create_use_shared_delimiter.additional_properties = d
        return custom_notation_create_use_shared_delimiter

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
    def delimiter(self) -> str:
        if isinstance(self._delimiter, Unset):
            raise NotPresentError(self, "delimiter")
        return self._delimiter

    @delimiter.setter
    def delimiter(self, value: str) -> None:
        self._delimiter = value

    @delimiter.deleter
    def delimiter(self) -> None:
        self._delimiter = UNSET
