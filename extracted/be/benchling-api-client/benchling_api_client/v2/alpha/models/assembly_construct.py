from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.assembly_created_primer import AssemblyCreatedPrimer
from ..models.assembly_protein_reference import AssemblyProteinReference
from ..models.assembly_sequence_reference import AssemblySequenceReference
from ..models.assembly_transient_primer import AssemblyTransientPrimer
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyConstruct")


@attr.s(auto_attribs=True, repr=False)
class AssemblyConstruct:
    """  """

    _construct_fragment_ids: Union[Unset, List[str]] = UNSET
    _construct_primers: Union[
        Unset, List[Union[AssemblyCreatedPrimer, AssemblyTransientPrimer, UnknownType]]
    ] = UNSET
    _id: Union[Unset, str] = UNSET
    _output_polymer: Union[Unset, AssemblySequenceReference, AssemblyProteinReference, UnknownType] = UNSET

    def __repr__(self):
        fields = []
        fields.append("construct_fragment_ids={}".format(repr(self._construct_fragment_ids)))
        fields.append("construct_primers={}".format(repr(self._construct_primers)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("output_polymer={}".format(repr(self._output_polymer)))
        return "AssemblyConstruct({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        construct_fragment_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._construct_fragment_ids, Unset):
            construct_fragment_ids = self._construct_fragment_ids

        construct_primers: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._construct_primers, Unset):
            construct_primers = []
            for construct_primers_item_data in self._construct_primers:
                if isinstance(construct_primers_item_data, UnknownType):
                    construct_primers_item = construct_primers_item_data.value
                elif isinstance(construct_primers_item_data, AssemblyCreatedPrimer):
                    construct_primers_item = construct_primers_item_data.to_dict()

                else:
                    construct_primers_item = construct_primers_item_data.to_dict()

                construct_primers.append(construct_primers_item)

        id = self._id
        output_polymer: Union[Unset, Dict[str, Any]]
        if isinstance(self._output_polymer, Unset):
            output_polymer = UNSET
        elif isinstance(self._output_polymer, UnknownType):
            output_polymer = self._output_polymer.value
        elif isinstance(self._output_polymer, AssemblySequenceReference):
            output_polymer = self._output_polymer.to_dict()

        else:
            output_polymer = self._output_polymer.to_dict()

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if construct_fragment_ids is not UNSET:
            field_dict["constructFragmentIds"] = construct_fragment_ids
        if construct_primers is not UNSET:
            field_dict["constructPrimers"] = construct_primers
        if id is not UNSET:
            field_dict["id"] = id
        if output_polymer is not UNSET:
            field_dict["outputPolymer"] = output_polymer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_construct_fragment_ids() -> Union[Unset, List[str]]:
            construct_fragment_ids = cast(List[str], d.pop("constructFragmentIds"))

            return construct_fragment_ids

        try:
            construct_fragment_ids = get_construct_fragment_ids()
        except KeyError:
            if strict:
                raise
            construct_fragment_ids = cast(Union[Unset, List[str]], UNSET)

        def get_construct_primers() -> Union[
            Unset, List[Union[AssemblyCreatedPrimer, AssemblyTransientPrimer, UnknownType]]
        ]:
            construct_primers = []
            _construct_primers = d.pop("constructPrimers")
            for construct_primers_item_data in _construct_primers or []:

                def _parse_construct_primers_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[AssemblyCreatedPrimer, AssemblyTransientPrimer, UnknownType]:
                    construct_primers_item: Union[AssemblyCreatedPrimer, AssemblyTransientPrimer, UnknownType]
                    discriminator_value: str = cast(str, data.get("type"))
                    if discriminator_value is not None:
                        if discriminator_value == "BULK_ASSEMBLY_CREATED_PRIMER":
                            construct_primers_item = AssemblyCreatedPrimer.from_dict(data, strict=False)

                            return construct_primers_item
                        if discriminator_value == "BULK_ASSEMBLY_TRANSIENT_PRIMER":
                            construct_primers_item = AssemblyTransientPrimer.from_dict(data, strict=False)

                            return construct_primers_item

                        return UnknownType(value=data)
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        construct_primers_item = AssemblyCreatedPrimer.from_dict(data, strict=True)

                        return construct_primers_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        construct_primers_item = AssemblyTransientPrimer.from_dict(data, strict=True)

                        return construct_primers_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                construct_primers_item = _parse_construct_primers_item(construct_primers_item_data)

                construct_primers.append(construct_primers_item)

            return construct_primers

        try:
            construct_primers = get_construct_primers()
        except KeyError:
            if strict:
                raise
            construct_primers = cast(
                Union[Unset, List[Union[AssemblyCreatedPrimer, AssemblyTransientPrimer, UnknownType]]], UNSET
            )

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_output_polymer() -> Union[
            Unset, AssemblySequenceReference, AssemblyProteinReference, UnknownType
        ]:
            output_polymer: Union[Unset, AssemblySequenceReference, AssemblyProteinReference, UnknownType]
            _output_polymer = d.pop("outputPolymer")

            if not isinstance(_output_polymer, Unset):
                discriminator = _output_polymer["polymerType"]
                if discriminator == "AA_SEQUENCE":
                    output_polymer = AssemblyProteinReference.from_dict(_output_polymer)
                elif discriminator == "NUCLEOTIDE_SEQUENCE":
                    output_polymer = AssemblySequenceReference.from_dict(_output_polymer)
                else:
                    output_polymer = UnknownType(value=_output_polymer)

            return output_polymer

        try:
            output_polymer = get_output_polymer()
        except KeyError:
            if strict:
                raise
            output_polymer = cast(
                Union[Unset, AssemblySequenceReference, AssemblyProteinReference, UnknownType], UNSET
            )

        assembly_construct = cls(
            construct_fragment_ids=construct_fragment_ids,
            construct_primers=construct_primers,
            id=id,
            output_polymer=output_polymer,
        )

        return assembly_construct

    @property
    def construct_fragment_ids(self) -> List[str]:
        if isinstance(self._construct_fragment_ids, Unset):
            raise NotPresentError(self, "construct_fragment_ids")
        return self._construct_fragment_ids

    @construct_fragment_ids.setter
    def construct_fragment_ids(self, value: List[str]) -> None:
        self._construct_fragment_ids = value

    @construct_fragment_ids.deleter
    def construct_fragment_ids(self) -> None:
        self._construct_fragment_ids = UNSET

    @property
    def construct_primers(self) -> List[Union[AssemblyCreatedPrimer, AssemblyTransientPrimer, UnknownType]]:
        if isinstance(self._construct_primers, Unset):
            raise NotPresentError(self, "construct_primers")
        return self._construct_primers

    @construct_primers.setter
    def construct_primers(
        self, value: List[Union[AssemblyCreatedPrimer, AssemblyTransientPrimer, UnknownType]]
    ) -> None:
        self._construct_primers = value

    @construct_primers.deleter
    def construct_primers(self) -> None:
        self._construct_primers = UNSET

    @property
    def id(self) -> str:
        """ Unique identifier for the construct. """
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def output_polymer(self) -> Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]:
        if isinstance(self._output_polymer, Unset):
            raise NotPresentError(self, "output_polymer")
        return self._output_polymer

    @output_polymer.setter
    def output_polymer(
        self, value: Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]
    ) -> None:
        self._output_polymer = value

    @output_polymer.deleter
    def output_polymer(self) -> None:
        self._output_polymer = UNSET
