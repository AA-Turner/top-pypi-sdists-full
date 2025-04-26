from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.button_ui_block_type import ButtonUiBlockType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ButtonUiBlockUpdate")


@attr.s(auto_attribs=True, repr=False)
class ButtonUiBlockUpdate:
    """  """

    _id: str
    _text: Union[Unset, str] = UNSET
    _type: Union[Unset, ButtonUiBlockType] = UNSET
    _enabled: Union[Unset, None, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("text={}".format(repr(self._text)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("enabled={}".format(repr(self._enabled)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ButtonUiBlockUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        text = self._text
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        enabled = self._enabled

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if text is not UNSET:
            field_dict["text"] = text
        if type is not UNSET:
            field_dict["type"] = type
        if enabled is not UNSET:
            field_dict["enabled"] = enabled

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_text() -> Union[Unset, str]:
            text = d.pop("text")
            return text

        try:
            text = get_text()
        except KeyError:
            if strict:
                raise
            text = cast(Union[Unset, str], UNSET)

        def get_type() -> Union[Unset, ButtonUiBlockType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = ButtonUiBlockType(_type)
                except ValueError:
                    type = ButtonUiBlockType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, ButtonUiBlockType], UNSET)

        def get_enabled() -> Union[Unset, None, bool]:
            enabled = d.pop("enabled")
            return enabled

        try:
            enabled = get_enabled()
        except KeyError:
            if strict:
                raise
            enabled = cast(Union[Unset, None, bool], UNSET)

        button_ui_block_update = cls(
            id=id,
            text=text,
            type=type,
            enabled=enabled,
        )

        button_ui_block_update.additional_properties = d
        return button_ui_block_update

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

    @property
    def text(self) -> str:
        if isinstance(self._text, Unset):
            raise NotPresentError(self, "text")
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        self._text = value

    @text.deleter
    def text(self) -> None:
        self._text = UNSET

    @property
    def type(self) -> ButtonUiBlockType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: ButtonUiBlockType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def enabled(self) -> Optional[bool]:
        if isinstance(self._enabled, Unset):
            raise NotPresentError(self, "enabled")
        return self._enabled

    @enabled.setter
    def enabled(self, value: Optional[bool]) -> None:
        self._enabled = value

    @enabled.deleter
    def enabled(self) -> None:
        self._enabled = UNSET
