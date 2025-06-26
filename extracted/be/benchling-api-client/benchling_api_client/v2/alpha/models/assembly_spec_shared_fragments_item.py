from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assembly_fragment_shared_orientation import AssemblyFragmentSharedOrientation
from ..models.assembly_protein_reference import AssemblyProteinReference
from ..models.assembly_sequence_reference import AssemblySequenceReference
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblySpecSharedFragmentsItem")


@attr.s(auto_attribs=True, repr=False)
class AssemblySpecSharedFragmentsItem:
    """  """

    _bin_id: str
    _end: float
    _id: str
    _orientation: AssemblyFragmentSharedOrientation
    _polymer: Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]
    _start: float
    _preferred_primer3_id: Union[Unset, str] = UNSET
    _preferred_primer5_id: Union[Unset, str] = UNSET
    _restriction_enzyme3_id: Union[Unset, str] = UNSET
    _restriction_enzyme5_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("bin_id={}".format(repr(self._bin_id)))
        fields.append("end={}".format(repr(self._end)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("orientation={}".format(repr(self._orientation)))
        fields.append("polymer={}".format(repr(self._polymer)))
        fields.append("start={}".format(repr(self._start)))
        fields.append("preferred_primer3_id={}".format(repr(self._preferred_primer3_id)))
        fields.append("preferred_primer5_id={}".format(repr(self._preferred_primer5_id)))
        fields.append("restriction_enzyme3_id={}".format(repr(self._restriction_enzyme3_id)))
        fields.append("restriction_enzyme5_id={}".format(repr(self._restriction_enzyme5_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "AssemblySpecSharedFragmentsItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        bin_id = self._bin_id
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
        preferred_primer3_id = self._preferred_primer3_id
        preferred_primer5_id = self._preferred_primer5_id
        restriction_enzyme3_id = self._restriction_enzyme3_id
        restriction_enzyme5_id = self._restriction_enzyme5_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if bin_id is not UNSET:
            field_dict["binId"] = bin_id
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
        if preferred_primer3_id is not UNSET:
            field_dict["preferredPrimer3Id"] = preferred_primer3_id
        if preferred_primer5_id is not UNSET:
            field_dict["preferredPrimer5Id"] = preferred_primer5_id
        if restriction_enzyme3_id is not UNSET:
            field_dict["restrictionEnzyme3Id"] = restriction_enzyme3_id
        if restriction_enzyme5_id is not UNSET:
            field_dict["restrictionEnzyme5Id"] = restriction_enzyme5_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_bin_id() -> str:
            bin_id = d.pop("binId")
            return bin_id

        try:
            bin_id = get_bin_id()
        except KeyError:
            if strict:
                raise
            bin_id = cast(str, UNSET)

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

        def get_preferred_primer3_id() -> Union[Unset, str]:
            preferred_primer3_id = d.pop("preferredPrimer3Id")
            return preferred_primer3_id

        try:
            preferred_primer3_id = get_preferred_primer3_id()
        except KeyError:
            if strict:
                raise
            preferred_primer3_id = cast(Union[Unset, str], UNSET)

        def get_preferred_primer5_id() -> Union[Unset, str]:
            preferred_primer5_id = d.pop("preferredPrimer5Id")
            return preferred_primer5_id

        try:
            preferred_primer5_id = get_preferred_primer5_id()
        except KeyError:
            if strict:
                raise
            preferred_primer5_id = cast(Union[Unset, str], UNSET)

        def get_restriction_enzyme3_id() -> Union[Unset, str]:
            restriction_enzyme3_id = d.pop("restrictionEnzyme3Id")
            return restriction_enzyme3_id

        try:
            restriction_enzyme3_id = get_restriction_enzyme3_id()
        except KeyError:
            if strict:
                raise
            restriction_enzyme3_id = cast(Union[Unset, str], UNSET)

        def get_restriction_enzyme5_id() -> Union[Unset, str]:
            restriction_enzyme5_id = d.pop("restrictionEnzyme5Id")
            return restriction_enzyme5_id

        try:
            restriction_enzyme5_id = get_restriction_enzyme5_id()
        except KeyError:
            if strict:
                raise
            restriction_enzyme5_id = cast(Union[Unset, str], UNSET)

        assembly_spec_shared_fragments_item = cls(
            bin_id=bin_id,
            end=end,
            id=id,
            orientation=orientation,
            polymer=polymer,
            start=start,
            preferred_primer3_id=preferred_primer3_id,
            preferred_primer5_id=preferred_primer5_id,
            restriction_enzyme3_id=restriction_enzyme3_id,
            restriction_enzyme5_id=restriction_enzyme5_id,
        )

        assembly_spec_shared_fragments_item.additional_properties = d
        return assembly_spec_shared_fragments_item

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
    def bin_id(self) -> str:
        """ ID of the fragment's bin """
        if isinstance(self._bin_id, Unset):
            raise NotPresentError(self, "bin_id")
        return self._bin_id

    @bin_id.setter
    def bin_id(self, value: str) -> None:
        self._bin_id = value

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

    @property
    def preferred_primer3_id(self) -> str:
        """ API identifier of a Benchling oligo to be used as a primer at the 3' end of the fragment. """
        if isinstance(self._preferred_primer3_id, Unset):
            raise NotPresentError(self, "preferred_primer3_id")
        return self._preferred_primer3_id

    @preferred_primer3_id.setter
    def preferred_primer3_id(self, value: str) -> None:
        self._preferred_primer3_id = value

    @preferred_primer3_id.deleter
    def preferred_primer3_id(self) -> None:
        self._preferred_primer3_id = UNSET

    @property
    def preferred_primer5_id(self) -> str:
        """ API identifier of a Benchling oligo to be used as a primer at the 5' end of the fragment. """
        if isinstance(self._preferred_primer5_id, Unset):
            raise NotPresentError(self, "preferred_primer5_id")
        return self._preferred_primer5_id

    @preferred_primer5_id.setter
    def preferred_primer5_id(self, value: str) -> None:
        self._preferred_primer5_id = value

    @preferred_primer5_id.deleter
    def preferred_primer5_id(self) -> None:
        self._preferred_primer5_id = UNSET

    @property
    def restriction_enzyme3_id(self) -> str:
        """ ID of enzyme used to digest fragment at 3' end """
        if isinstance(self._restriction_enzyme3_id, Unset):
            raise NotPresentError(self, "restriction_enzyme3_id")
        return self._restriction_enzyme3_id

    @restriction_enzyme3_id.setter
    def restriction_enzyme3_id(self, value: str) -> None:
        self._restriction_enzyme3_id = value

    @restriction_enzyme3_id.deleter
    def restriction_enzyme3_id(self) -> None:
        self._restriction_enzyme3_id = UNSET

    @property
    def restriction_enzyme5_id(self) -> str:
        """ ID of enzyme used to digest fragment at 5' end """
        if isinstance(self._restriction_enzyme5_id, Unset):
            raise NotPresentError(self, "restriction_enzyme5_id")
        return self._restriction_enzyme5_id

    @restriction_enzyme5_id.setter
    def restriction_enzyme5_id(self, value: str) -> None:
        self._restriction_enzyme5_id = value

    @restriction_enzyme5_id.deleter
    def restriction_enzyme5_id(self) -> None:
        self._restriction_enzyme5_id = UNSET
