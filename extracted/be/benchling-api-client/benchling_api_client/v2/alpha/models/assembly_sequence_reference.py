from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_sequence_reference_polymer_type import AssemblySequenceReferencePolymerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblySequenceReference")


@attr.s(auto_attribs=True, repr=False)
class AssemblySequenceReference:
    """  """

    _polymer_type: AssemblySequenceReferencePolymerType
    _sequence_id: str

    def __repr__(self):
        fields = []
        fields.append("polymer_type={}".format(repr(self._polymer_type)))
        fields.append("sequence_id={}".format(repr(self._sequence_id)))
        return "AssemblySequenceReference({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        polymer_type = self._polymer_type.value

        sequence_id = self._sequence_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if polymer_type is not UNSET:
            field_dict["polymerType"] = polymer_type
        if sequence_id is not UNSET:
            field_dict["sequenceId"] = sequence_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_polymer_type() -> AssemblySequenceReferencePolymerType:
            _polymer_type = d.pop("polymerType")
            try:
                polymer_type = AssemblySequenceReferencePolymerType(_polymer_type)
            except ValueError:
                polymer_type = AssemblySequenceReferencePolymerType.of_unknown(_polymer_type)

            return polymer_type

        try:
            polymer_type = get_polymer_type()
        except KeyError:
            if strict:
                raise
            polymer_type = cast(AssemblySequenceReferencePolymerType, UNSET)

        def get_sequence_id() -> str:
            sequence_id = d.pop("sequenceId")
            return sequence_id

        try:
            sequence_id = get_sequence_id()
        except KeyError:
            if strict:
                raise
            sequence_id = cast(str, UNSET)

        assembly_sequence_reference = cls(
            polymer_type=polymer_type,
            sequence_id=sequence_id,
        )

        return assembly_sequence_reference

    @property
    def polymer_type(self) -> AssemblySequenceReferencePolymerType:
        if isinstance(self._polymer_type, Unset):
            raise NotPresentError(self, "polymer_type")
        return self._polymer_type

    @polymer_type.setter
    def polymer_type(self, value: AssemblySequenceReferencePolymerType) -> None:
        self._polymer_type = value

    @property
    def sequence_id(self) -> str:
        """ API identifier for the nucleotide sequence. """
        if isinstance(self._sequence_id, Unset):
            raise NotPresentError(self, "sequence_id")
        return self._sequence_id

    @sequence_id.setter
    def sequence_id(self, value: str) -> None:
        self._sequence_id = value
