from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assembly_fragment_shared_orientation import AssemblyFragmentSharedOrientation
from ..models.assembly_protein_reference import AssemblyProteinReference
from ..models.assembly_sequence_reference import AssemblySequenceReference
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyFragmentShared")


@attr.s(auto_attribs=True, repr=False)
class AssemblyFragmentShared:
    """  """

    _end: float
    _id: str
    _orientation: AssemblyFragmentSharedOrientation
    _polymer: Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]
    _start: float

    def __repr__(self):
        fields = []
        fields.append("end={}".format(repr(self._end)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("orientation={}".format(repr(self._orientation)))
        fields.append("polymer={}".format(repr(self._polymer)))
        fields.append("start={}".format(repr(self._start)))
        return "AssemblyFragmentShared({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        end = self._end
        id = self._id
        orientation = self._orientation.value

        if isinstance(self._polymer, UnknownType):
            polymer = self._polymer.value
        elif isinstance(self._polymer, AssemblySequenceReference):
            polymer = self._polymer.to_dict()

        else:
            polymer = self._polymer.to_dict()

        start = self._start

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if end is not UNSET:
            field_dict["end"] = end
        if id is not UNSET:
            field_dict["id"] = id
        if orientation is not UNSET:
            field_dict["orientation"] = orientation
        if polymer is not UNSET:
            field_dict["polymer"] = polymer
        if start is not UNSET:
            field_dict["start"] = start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_end() -> float:
            end = d.pop("end")
            return end

        try:
            end = get_end()
        except KeyError:
            if strict:
                raise
            end = cast(float, UNSET)

        def get_id() -> str:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(str, UNSET)

        def get_orientation() -> AssemblyFragmentSharedOrientation:
            _orientation = d.pop("orientation")
            try:
                orientation = AssemblyFragmentSharedOrientation(_orientation)
            except ValueError:
                orientation = AssemblyFragmentSharedOrientation.of_unknown(_orientation)

            return orientation

        try:
            orientation = get_orientation()
        except KeyError:
            if strict:
                raise
            orientation = cast(AssemblyFragmentSharedOrientation, UNSET)

        def get_polymer() -> Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]:
            polymer: Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]
            _polymer = d.pop("polymer")

            if True:
                discriminator = _polymer["polymerType"]
                if discriminator == "AA_SEQUENCE":
                    polymer = AssemblyProteinReference.from_dict(_polymer)
                elif discriminator == "NUCLEOTIDE_SEQUENCE":
                    polymer = AssemblySequenceReference.from_dict(_polymer)
                else:
                    polymer = UnknownType(value=_polymer)

            return polymer

        try:
            polymer = get_polymer()
        except KeyError:
            if strict:
                raise
            polymer = cast(Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType], UNSET)

        def get_start() -> float:
            start = d.pop("start")
            return start

        try:
            start = get_start()
        except KeyError:
            if strict:
                raise
            start = cast(float, UNSET)

        assembly_fragment_shared = cls(
            end=end,
            id=id,
            orientation=orientation,
            polymer=polymer,
            start=start,
        )

        return assembly_fragment_shared

    @property
    def end(self) -> float:
        """ End position of the fragment in the provided input. """
        if isinstance(self._end, Unset):
            raise NotPresentError(self, "end")
        return self._end

    @end.setter
    def end(self, value: float) -> None:
        self._end = value

    @property
    def id(self) -> str:
        """ Unique identifier for the fragment. """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @property
    def orientation(self) -> AssemblyFragmentSharedOrientation:
        if isinstance(self._orientation, Unset):
            raise NotPresentError(self, "orientation")
        return self._orientation

    @orientation.setter
    def orientation(self, value: AssemblyFragmentSharedOrientation) -> None:
        self._orientation = value

    @property
    def polymer(self) -> Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]:
        if isinstance(self._polymer, Unset):
            raise NotPresentError(self, "polymer")
        return self._polymer

    @polymer.setter
    def polymer(self, value: Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]) -> None:
        self._polymer = value

    @property
    def start(self) -> float:
        """ Start position of the fragment in the provided input. """
        if isinstance(self._start, Unset):
            raise NotPresentError(self, "start")
        return self._start

    @start.setter
    def start(self, value: float) -> None:
        self._start = value
