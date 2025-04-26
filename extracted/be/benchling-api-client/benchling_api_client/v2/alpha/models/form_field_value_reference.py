from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.form_field_value_reference_type import FormFieldValueReferenceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FormFieldValueReference")


@attr.s(auto_attribs=True, repr=False)
class FormFieldValueReference:
    """  """

    _key: Union[Unset, str] = UNSET
    _type: Union[Unset, FormFieldValueReferenceType] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("key={}".format(repr(self._key)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FormFieldValueReference({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        key = self._key
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if key is not UNSET:
            field_dict["key"] = key
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_key() -> Union[Unset, str]:
            key = d.pop("key")
            return key

        try:
            key = get_key()
        except KeyError:
            if strict:
                raise
            key = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, FormFieldValueReferenceType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = FormFieldValueReferenceType(_type)
                except ValueError:
                    type = FormFieldValueReferenceType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, FormFieldValueReferenceType], UNSET)

        form_field_value_reference = cls(
            key=key,
            type=type,
        )

        form_field_value_reference.additional_properties = d
        return form_field_value_reference

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
    def key(self) -> str:
        if isinstance(self._key, Unset):
            raise NotPresentError(self, "key")
        return self._key

    @key.setter
    def key(self, value: str) -> None:
        self._key = value

    @key.deleter
    def key(self) -> None:
        self._key = UNSET

    @property
    def type(self) -> FormFieldValueReferenceType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: FormFieldValueReferenceType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
