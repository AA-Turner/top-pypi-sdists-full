from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="NameTemplatePart")


@attr.s(auto_attribs=True, repr=False)
class NameTemplatePart:
    """  """

    _datetime_format: Union[Unset, None, str] = UNSET
    _field_id: Union[Unset, None, str] = UNSET
    _text: Union[Unset, None, str] = UNSET
    _type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("datetime_format={}".format(repr(self._datetime_format)))
        fields.append("field_id={}".format(repr(self._field_id)))
        fields.append("text={}".format(repr(self._text)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "NameTemplatePart({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        datetime_format = self._datetime_format
        field_id = self._field_id
        text = self._text
        type = self._type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if datetime_format is not UNSET:
            field_dict["datetimeFormat"] = datetime_format
        if field_id is not UNSET:
            field_dict["fieldId"] = field_id
        if text is not UNSET:
            field_dict["text"] = text
        if type is not UNSET:
            field_dict["type"] = type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_datetime_format() -> Union[Unset, None, str]:
            datetime_format = d.pop("datetimeFormat")
            return datetime_format

        try:
            datetime_format = get_datetime_format()
        except KeyError:
            if strict:
                raise
            datetime_format = cast(Union[Unset, None, str], UNSET)

        def get_field_id() -> Union[Unset, None, str]:
            field_id = d.pop("fieldId")
            return field_id

        try:
            field_id = get_field_id()
        except KeyError:
            if strict:
                raise
            field_id = cast(Union[Unset, None, str], UNSET)

        def get_text() -> Union[Unset, None, str]:
            text = d.pop("text")
            return text

        try:
            text = get_text()
        except KeyError:
            if strict:
                raise
            text = cast(Union[Unset, None, str], UNSET)

        def get_type() -> Union[Unset, str]:
            type = d.pop("type")
            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, str], UNSET)

        name_template_part = cls(
            datetime_format=datetime_format,
            field_id=field_id,
            text=text,
            type=type,
        )

        name_template_part.additional_properties = d
        return name_template_part

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
    def datetime_format(self) -> Optional[str]:
        if isinstance(self._datetime_format, Unset):
            raise NotPresentError(self, "datetime_format")
        return self._datetime_format

    @datetime_format.setter
    def datetime_format(self, value: Optional[str]) -> None:
        self._datetime_format = value

    @datetime_format.deleter
    def datetime_format(self) -> None:
        self._datetime_format = UNSET

    @property
    def field_id(self) -> Optional[str]:
        if isinstance(self._field_id, Unset):
            raise NotPresentError(self, "field_id")
        return self._field_id

    @field_id.setter
    def field_id(self, value: Optional[str]) -> None:
        self._field_id = value

    @field_id.deleter
    def field_id(self) -> None:
        self._field_id = UNSET

    @property
    def text(self) -> Optional[str]:
        if isinstance(self._text, Unset):
            raise NotPresentError(self, "text")
        return self._text

    @text.setter
    def text(self, value: Optional[str]) -> None:
        self._text = value

    @text.deleter
    def text(self) -> None:
        self._text = UNSET

    @property
    def type(self) -> str:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: str) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET
