from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.free_form_text_form_field_canned_responses import FreeFormTextFormFieldCannedResponses
from ..models.free_form_text_form_field_default_keyboard import FreeFormTextFormFieldDefaultKeyboard
from ..models.free_form_text_form_field_type import FreeFormTextFormFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="FreeFormTextFormField")


@attr.s(auto_attribs=True, repr=False)
class FreeFormTextFormField:
    """  """

    _canned_responses: Union[Unset, FreeFormTextFormFieldCannedResponses] = UNSET
    _default_keyboard: Union[Unset, FreeFormTextFormFieldDefaultKeyboard] = UNSET
    _number_of_lines: Union[Unset, float] = UNSET
    _type: Union[Unset, FreeFormTextFormFieldType] = UNSET
    _description: Union[Unset, str] = UNSET
    _is_required: Union[Unset, bool] = UNSET
    _key: Union[Unset, str] = UNSET
    _label: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("canned_responses={}".format(repr(self._canned_responses)))
        fields.append("default_keyboard={}".format(repr(self._default_keyboard)))
        fields.append("number_of_lines={}".format(repr(self._number_of_lines)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("key={}".format(repr(self._key)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "FreeFormTextFormField({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        canned_responses: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._canned_responses, Unset):
            canned_responses = self._canned_responses.to_dict()

        default_keyboard: Union[Unset, int] = UNSET
        if not isinstance(self._default_keyboard, Unset):
            default_keyboard = self._default_keyboard.value

        number_of_lines = self._number_of_lines
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        description = self._description
        is_required = self._is_required
        key = self._key
        label = self._label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if canned_responses is not UNSET:
            field_dict["cannedResponses"] = canned_responses
        if default_keyboard is not UNSET:
            field_dict["defaultKeyboard"] = default_keyboard
        if number_of_lines is not UNSET:
            field_dict["numberOfLines"] = number_of_lines
        if type is not UNSET:
            field_dict["type"] = type
        if description is not UNSET:
            field_dict["description"] = description
        if is_required is not UNSET:
            field_dict["isRequired"] = is_required
        if key is not UNSET:
            field_dict["key"] = key
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_canned_responses() -> Union[Unset, FreeFormTextFormFieldCannedResponses]:
            canned_responses: Union[Unset, Union[Unset, FreeFormTextFormFieldCannedResponses]] = UNSET
            _canned_responses = d.pop("cannedResponses")

            if not isinstance(_canned_responses, Unset):
                canned_responses = FreeFormTextFormFieldCannedResponses.from_dict(_canned_responses)

            return canned_responses

        try:
            canned_responses = get_canned_responses()
        except KeyError:
            if strict:
                raise
            canned_responses = cast(Union[Unset, FreeFormTextFormFieldCannedResponses], UNSET)

        def get_default_keyboard() -> Union[Unset, FreeFormTextFormFieldDefaultKeyboard]:
            default_keyboard = UNSET
            _default_keyboard = d.pop("defaultKeyboard")
            if _default_keyboard is not None and _default_keyboard is not UNSET:
                try:
                    default_keyboard = FreeFormTextFormFieldDefaultKeyboard(_default_keyboard)
                except ValueError:
                    default_keyboard = FreeFormTextFormFieldDefaultKeyboard.of_unknown(_default_keyboard)

            return default_keyboard

        try:
            default_keyboard = get_default_keyboard()
        except KeyError:
            if strict:
                raise
            default_keyboard = cast(Union[Unset, FreeFormTextFormFieldDefaultKeyboard], UNSET)

        def get_number_of_lines() -> Union[Unset, float]:
            number_of_lines = d.pop("numberOfLines")
            return number_of_lines

        try:
            number_of_lines = get_number_of_lines()
        except KeyError:
            if strict:
                raise
            number_of_lines = cast(Union[Unset, float], UNSET)

        def get_type() -> Union[Unset, FreeFormTextFormFieldType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = FreeFormTextFormFieldType(_type)
                except ValueError:
                    type = FreeFormTextFormFieldType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, FreeFormTextFormFieldType], UNSET)

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, str], UNSET)

        def get_is_required() -> Union[Unset, bool]:
            is_required = d.pop("isRequired")
            return is_required

        try:
            is_required = get_is_required()
        except KeyError:
            if strict:
                raise
            is_required = cast(Union[Unset, bool], UNSET)

        def get_key() -> Union[Unset, str]:
            key = d.pop("key")
            return key

        try:
            key = get_key()
        except KeyError:
            if strict:
                raise
            key = cast(Union[Unset, str], UNSET)

        def get_label() -> Union[Unset, str]:
            label = d.pop("label")
            return label

        try:
            label = get_label()
        except KeyError:
            if strict:
                raise
            label = cast(Union[Unset, str], UNSET)

        free_form_text_form_field = cls(
            canned_responses=canned_responses,
            default_keyboard=default_keyboard,
            number_of_lines=number_of_lines,
            type=type,
            description=description,
            is_required=is_required,
            key=key,
            label=label,
        )

        free_form_text_form_field.additional_properties = d
        return free_form_text_form_field

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
    def canned_responses(self) -> FreeFormTextFormFieldCannedResponses:
        if isinstance(self._canned_responses, Unset):
            raise NotPresentError(self, "canned_responses")
        return self._canned_responses

    @canned_responses.setter
    def canned_responses(self, value: FreeFormTextFormFieldCannedResponses) -> None:
        self._canned_responses = value

    @canned_responses.deleter
    def canned_responses(self) -> None:
        self._canned_responses = UNSET

    @property
    def default_keyboard(self) -> FreeFormTextFormFieldDefaultKeyboard:
        if isinstance(self._default_keyboard, Unset):
            raise NotPresentError(self, "default_keyboard")
        return self._default_keyboard

    @default_keyboard.setter
    def default_keyboard(self, value: FreeFormTextFormFieldDefaultKeyboard) -> None:
        self._default_keyboard = value

    @default_keyboard.deleter
    def default_keyboard(self) -> None:
        self._default_keyboard = UNSET

    @property
    def number_of_lines(self) -> float:
        if isinstance(self._number_of_lines, Unset):
            raise NotPresentError(self, "number_of_lines")
        return self._number_of_lines

    @number_of_lines.setter
    def number_of_lines(self, value: float) -> None:
        self._number_of_lines = value

    @number_of_lines.deleter
    def number_of_lines(self) -> None:
        self._number_of_lines = UNSET

    @property
    def type(self) -> FreeFormTextFormFieldType:
        """The type of this form field. Type declares how this field behaves and dictates the additional properties passed along with the required properties like label and key"""
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: FreeFormTextFormFieldType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def description(self) -> str:
        """ Description of the purpose of this field """
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def is_required(self) -> bool:
        """ Whether this field is required to be filled out in order to be a valid submission """
        if isinstance(self._is_required, Unset):
            raise NotPresentError(self, "is_required")
        return self._is_required

    @is_required.setter
    def is_required(self, value: bool) -> None:
        self._is_required = value

    @is_required.deleter
    def is_required(self) -> None:
        self._is_required = UNSET

    @property
    def key(self) -> str:
        """ Reference key of this form field. Used to fix identity of fields beyond the label """
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
    def label(self) -> str:
        """ End user facing name of this form field. What you see when you fill out the form each time """
        if isinstance(self._label, Unset):
            raise NotPresentError(self, "label")
        return self._label

    @label.setter
    def label(self, value: str) -> None:
        self._label = value

    @label.deleter
    def label(self) -> None:
        self._label = UNSET
