from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.chart_note_part_chart import ChartNotePartChart
from ..models.chart_note_part_type import ChartNotePartType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChartNotePart")


@attr.s(auto_attribs=True, repr=False)
class ChartNotePart:
    """  """

    _chart: Union[Unset, ChartNotePartChart] = UNSET
    _type: Union[Unset, ChartNotePartType] = UNSET
    _indentation: Union[Unset, int] = 0
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("chart={}".format(repr(self._chart)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("indentation={}".format(repr(self._indentation)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ChartNotePart({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        chart: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._chart, Unset):
            chart = self._chart.to_dict()

        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        indentation = self._indentation

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if chart is not UNSET:
            field_dict["chart"] = chart
        if type is not UNSET:
            field_dict["type"] = type
        if indentation is not UNSET:
            field_dict["indentation"] = indentation

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_chart() -> Union[Unset, ChartNotePartChart]:
            chart: Union[Unset, Union[Unset, ChartNotePartChart]] = UNSET
            _chart = d.pop("chart")

            if not isinstance(_chart, Unset):
                chart = ChartNotePartChart.from_dict(_chart)

            return chart

        try:
            chart = get_chart()
        except KeyError:
            if strict:
                raise
            chart = cast(Union[Unset, ChartNotePartChart], UNSET)

        def get_type() -> Union[Unset, ChartNotePartType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = ChartNotePartType(_type)
                except ValueError:
                    type = ChartNotePartType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, ChartNotePartType], UNSET)

        def get_indentation() -> Union[Unset, int]:
            indentation = d.pop("indentation")
            return indentation

        try:
            indentation = get_indentation()
        except KeyError:
            if strict:
                raise
            indentation = cast(Union[Unset, int], UNSET)

        chart_note_part = cls(
            chart=chart,
            type=type,
            indentation=indentation,
        )

        chart_note_part.additional_properties = d
        return chart_note_part

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
    def chart(self) -> ChartNotePartChart:
        """ The full configuration for the chart to be displayed in-line in this note part. """
        if isinstance(self._chart, Unset):
            raise NotPresentError(self, "chart")
        return self._chart

    @chart.setter
    def chart(self, value: ChartNotePartChart) -> None:
        self._chart = value

    @chart.deleter
    def chart(self) -> None:
        self._chart = UNSET

    @property
    def type(self) -> ChartNotePartType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: ChartNotePartType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

    @property
    def indentation(self) -> int:
        """All notes have an indentation level - the default is 0 for no indent. For lists, indentation gives notes hierarchy - a bulleted list with children is modeled as one note part with indentation 1 followed by note parts with indentation 2, for example."""
        if isinstance(self._indentation, Unset):
            raise NotPresentError(self, "indentation")
        return self._indentation

    @indentation.setter
    def indentation(self, value: int) -> None:
        self._indentation = value

    @indentation.deleter
    def indentation(self) -> None:
        self._indentation = UNSET
