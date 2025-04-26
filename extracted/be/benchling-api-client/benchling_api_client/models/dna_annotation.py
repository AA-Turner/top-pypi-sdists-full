from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.sequence_feature_custom_field import SequenceFeatureCustomField
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaAnnotation")


@attr.s(auto_attribs=True, repr=False)
class DnaAnnotation:
    """  """

    _end: Union[Unset, int] = UNSET
    _start: Union[Unset, int] = UNSET
    _strand: Union[Unset, int] = UNSET
    _type: Union[Unset, str] = UNSET
    _color: Union[Unset, str] = UNSET
    _custom_fields: Union[Unset, List[SequenceFeatureCustomField]] = UNSET
    _name: Union[Unset, str] = UNSET
    _notes: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("end={}".format(repr(self._end)))
        fields.append("start={}".format(repr(self._start)))
        fields.append("strand={}".format(repr(self._strand)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("color={}".format(repr(self._color)))
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("notes={}".format(repr(self._notes)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DnaAnnotation({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        end = self._end
        start = self._start
        strand = self._strand
        type = self._type
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
        if end is not UNSET:
            field_dict["end"] = end
        if start is not UNSET:
            field_dict["start"] = start
        if strand is not UNSET:
            field_dict["strand"] = strand
        if type is not UNSET:
            field_dict["type"] = type
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

        def get_end() -> Union[Unset, int]:
            end = d.pop("end")
            return end

        try:
            end = get_end()
        except KeyError:
            if strict:
                raise
            end = cast(Union[Unset, int], UNSET)

        def get_start() -> Union[Unset, int]:
            start = d.pop("start")
            return start

        try:
            start = get_start()
        except KeyError:
            if strict:
                raise
            start = cast(Union[Unset, int], UNSET)

        def get_strand() -> Union[Unset, int]:
            strand = d.pop("strand")
            return strand

        try:
            strand = get_strand()
        except KeyError:
            if strict:
                raise
            strand = cast(Union[Unset, int], UNSET)

        def get_type() -> Union[Unset, str]:
            type = d.pop("type")
            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, str], UNSET)

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

        dna_annotation = cls(
            end=end,
            start=start,
            strand=strand,
            type=type,
            color=color,
            custom_fields=custom_fields,
            name=name,
            notes=notes,
        )

        dna_annotation.additional_properties = d
        return dna_annotation

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
    def end(self) -> int:
        """ 0-based exclusive end index. The end of the sequence is always represented as 0. """
        if isinstance(self._end, Unset):
            raise NotPresentError(self, "end")
        return self._end

    @end.setter
    def end(self, value: int) -> None:
        self._end = value

    @end.deleter
    def end(self) -> None:
        self._end = UNSET

    @property
    def start(self) -> int:
        """ 0-based inclusive start index. """
        if isinstance(self._start, Unset):
            raise NotPresentError(self, "start")
        return self._start

    @start.setter
    def start(self, value: int) -> None:
        self._start = value

    @start.deleter
    def start(self) -> None:
        self._start = UNSET

    @property
    def strand(self) -> int:
        if isinstance(self._strand, Unset):
            raise NotPresentError(self, "strand")
        return self._strand

    @strand.setter
    def strand(self, value: int) -> None:
        self._strand = value

    @strand.deleter
    def strand(self) -> None:
        self._strand = UNSET

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
