from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.sequence_feature_custom_field import SequenceFeatureCustomField
from ..types import UNSET, Unset

T = TypeVar("T", bound="SequenceFeatureBase")


@attr.s(auto_attribs=True, repr=False)
class SequenceFeatureBase:
    """  """

    _color: Union[Unset, str] = UNSET
    _custom_fields: Union[Unset, List[SequenceFeatureCustomField]] = UNSET
    _name: Union[Unset, str] = UNSET
    _notes: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("color={}".format(repr(self._color)))
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("notes={}".format(repr(self._notes)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "SequenceFeatureBase({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        color = self._color
        custom_fields: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._custom_fields, Unset):
            custom_fields = []
            for custom_fields_item_data in self._custom_fields:
                custom_fields_item = custom_fields_item_data.to_dict()

                custom_fields.append(custom_fields_item)

        name = self._name
        notes = self._notes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if color is not UNSET:
            field_dict["color"] = color
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if name is not UNSET:
            field_dict["name"] = name
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_color() -> Union[Unset, str]:
            color = d.pop("color")
            return color

        try:
            color = get_color()
        except KeyError:
            if strict:
                raise
            color = cast(Union[Unset, str], UNSET)

        def get_custom_fields() -> Union[Unset, List[SequenceFeatureCustomField]]:
            custom_fields = []
            _custom_fields = d.pop("customFields")
            for custom_fields_item_data in _custom_fields or []:
                custom_fields_item = SequenceFeatureCustomField.from_dict(
                    custom_fields_item_data, strict=False
                )

                custom_fields.append(custom_fields_item)

            return custom_fields

        try:
            custom_fields = get_custom_fields()
        except KeyError:
            if strict:
                raise
            custom_fields = cast(Union[Unset, List[SequenceFeatureCustomField]], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_notes() -> Union[Unset, str]:
            notes = d.pop("notes")
            return notes

        try:
            notes = get_notes()
        except KeyError:
            if strict:
                raise
            notes = cast(Union[Unset, str], UNSET)

        sequence_feature_base = cls(
            color=color,
            custom_fields=custom_fields,
            name=name,
            notes=notes,
        )

        sequence_feature_base.additional_properties = d
        return sequence_feature_base

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
    def color(self) -> str:
        """ Hex color code used when displaying this feature in the UI. """
        if isinstance(self._color, Unset):
            raise NotPresentError(self, "color")
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value

    @color.deleter
    def color(self) -> None:
        self._color = UNSET

    @property
    def custom_fields(self) -> List[SequenceFeatureCustomField]:
        if isinstance(self._custom_fields, Unset):
            raise NotPresentError(self, "custom_fields")
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, value: List[SequenceFeatureCustomField]) -> None:
        self._custom_fields = value

    @custom_fields.deleter
    def custom_fields(self) -> None:
        self._custom_fields = UNSET

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
    def notes(self) -> str:
        if isinstance(self._notes, Unset):
            raise NotPresentError(self, "notes")
        return self._notes

    @notes.setter
    def notes(self, value: str) -> None:
        self._notes = value

    @notes.deleter
    def notes(self) -> None:
        self._notes = UNSET
