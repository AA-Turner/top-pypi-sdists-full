from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="RnaSequencePart")


@attr.s(auto_attribs=True, repr=False)
class RnaSequencePart:
    """  """

    _strand: Union[Unset, int] = UNSET
    _end: Union[Unset, int] = UNSET
    _sequence_id: Union[Unset, str] = UNSET
    _start: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("strand={}".format(repr(self._strand)))
        fields.append("end={}".format(repr(self._end)))
        fields.append("sequence_id={}".format(repr(self._sequence_id)))
        fields.append("start={}".format(repr(self._start)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "RnaSequencePart({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        strand = self._strand
        end = self._end
        sequence_id = self._sequence_id
        start = self._start

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if strand is not UNSET:
            field_dict["strand"] = strand
        if end is not UNSET:
            field_dict["end"] = end
        if sequence_id is not UNSET:
            field_dict["sequenceId"] = sequence_id
        if start is not UNSET:
            field_dict["start"] = start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_strand() -> Union[Unset, int]:
            strand = d.pop("strand")
            return strand

        try:
            strand = get_strand()
        except KeyError:
            if strict:
                raise
            strand = cast(Union[Unset, int], UNSET)

        def get_end() -> Union[Unset, int]:
            end = d.pop("end")
            return end

        try:
            end = get_end()
        except KeyError:
            if strict:
                raise
            end = cast(Union[Unset, int], UNSET)

        def get_sequence_id() -> Union[Unset, str]:
            sequence_id = d.pop("sequenceId")
            return sequence_id

        try:
            sequence_id = get_sequence_id()
        except KeyError:
            if strict:
                raise
            sequence_id = cast(Union[Unset, str], UNSET)

        def get_start() -> Union[Unset, int]:
            start = d.pop("start")
            return start

        try:
            start = get_start()
        except KeyError:
            if strict:
                raise
            start = cast(Union[Unset, int], UNSET)

        rna_sequence_part = cls(
            strand=strand,
            end=end,
            sequence_id=sequence_id,
            start=start,
        )

        rna_sequence_part.additional_properties = d
        return rna_sequence_part

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
    def sequence_id(self) -> str:
        if isinstance(self._sequence_id, Unset):
            raise NotPresentError(self, "sequence_id")
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, value: str) -> None:
        self._sequence_id = value

    @sequence_id.deleter
    def sequence_id(self) -> None:
        self._sequence_id = UNSET

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
