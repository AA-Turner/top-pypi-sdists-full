from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.string_select_form_field_form_factor import StringSelectFormFieldFormFactor
from ..models.string_select_form_field_option import StringSelectFormFieldOption
from ..models.string_select_form_field_type import StringSelectFormFieldType
from ..types import UNSET, Unset

T = TypeVar("T", bound="StringSelectFormField")


@attr.s(auto_attribs=True, repr=False)
class StringSelectFormField:
    """  """

    _form_factor: Union[Unset, StringSelectFormFieldFormFactor] = UNSET
    _max_selections: Union[Unset, int] = UNSET
    _options: Union[Unset, List[StringSelectFormFieldOption]] = UNSET
    _type: Union[Unset, StringSelectFormFieldType] = UNSET
    _description: Union[Unset, str] = UNSET
    _is_required: Union[Unset, bool] = UNSET
    _key: Union[Unset, str] = UNSET
    _label: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("form_factor={}".format(repr(self._form_factor)))
        fields.append("max_selections={}".format(repr(self._max_selections)))
        fields.append("options={}".format(repr(self._options)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("is_required={}".format(repr(self._is_required)))
        fields.append("key={}".format(repr(self._key)))
        fields.append("label={}".format(repr(self._label)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "StringSelectFormField({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        form_factor: Union[Unset, int] = UNSET
        if not isinstance(self._form_factor, Unset):
            form_factor = self._form_factor.value

        max_selections = self._max_selections
        options: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._options, Unset):
            options = []
            for options_item_data in self._options:
                options_item = options_item_data.to_dict()

                options.append(options_item)

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
        if form_factor is not UNSET:
            field_dict["formFactor"] = form_factor
        if max_selections is not UNSET:
            field_dict["maxSelections"] = max_selections
        if options is not UNSET:
            field_dict["options"] = options
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

        def get_form_factor() -> Union[Unset, StringSelectFormFieldFormFactor]:
            form_factor = UNSET
            _form_factor = d.pop("formFactor")
            if _form_factor is not None and _form_factor is not UNSET:
                try:
                    form_factor = StringSelectFormFieldFormFactor(_form_factor)
                except ValueError:
                    form_factor = StringSelectFormFieldFormFactor.of_unknown(_form_factor)

            return form_factor

        try:
            form_factor = get_form_factor()
        except KeyError:
            if strict:
                raise
            form_factor = cast(Union[Unset, StringSelectFormFieldFormFactor], UNSET)

        def get_max_selections() -> Union[Unset, int]:
            max_selections = d.pop("maxSelections")
            return max_selections

        try:
            max_selections = get_max_selections()
        except KeyError:
            if strict:
                raise
            max_selections = cast(Union[Unset, int], UNSET)

        def get_options() -> Union[Unset, List[StringSelectFormFieldOption]]:
            options = []
            _options = d.pop("options")
            for options_item_data in _options or []:
                options_item = StringSelectFormFieldOption.from_dict(options_item_data, strict=False)

                options.append(options_item)

            return options

        try:
            options = get_options()
        except KeyError:
            if strict:
                raise
            options = cast(Union[Unset, List[StringSelectFormFieldOption]], UNSET)

        def get_type() -> Union[Unset, StringSelectFormFieldType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = StringSelectFormFieldType(_type)
                except ValueError:
                    type = StringSelectFormFieldType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, StringSelectFormFieldType], UNSET)

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

        string_select_form_field = cls(
            form_factor=form_factor,
            max_selections=max_selections,
            options=options,
            type=type,
            description=description,
            is_required=is_required,
            key=key,
            label=label,
        )

        string_select_form_field.additional_properties = d
        return string_select_form_field

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
    def form_factor(self) -> StringSelectFormFieldFormFactor:
        if isinstance(self._form_factor, Unset):
            raise NotPresentError(self, "form_factor")
        return self._form_factor

    @form_factor.setter
    def form_factor(self, value: StringSelectFormFieldFormFactor) -> None:
        self._form_factor = value

    @form_factor.deleter
    def form_factor(self) -> None:
        self._form_factor = UNSET

    @property
    def max_selections(self) -> int:
        if isinstance(self._max_selections, Unset):
            raise NotPresentError(self, "max_selections")
        return self._max_selections

    @max_selections.setter
    def max_selections(self, value: int) -> None:
        self._max_selections = value

    @max_selections.deleter
    def max_selections(self) -> None:
        self._max_selections = UNSET

    @property
    def options(self) -> List[StringSelectFormFieldOption]:
        if isinstance(self._options, Unset):
            raise NotPresentError(self, "options")
        return self._options

    @options.setter
    def options(self, value: List[StringSelectFormFieldOption]) -> None:
        self._options = value

    @options.deleter
    def options(self) -> None:
        self._options = UNSET

    @property
    def type(self) -> StringSelectFormFieldType:
        """The type of this form field. Type declares how this field behaves and dictates the additional properties passed along with the required properties like label and key"""
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: StringSelectFormFieldType) -> None:
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
