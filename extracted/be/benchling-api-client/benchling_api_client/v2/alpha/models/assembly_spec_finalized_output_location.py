from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblySpecFinalizedOutputLocation")


@attr.s(auto_attribs=True, repr=False)
class AssemblySpecFinalizedOutputLocation:
    """  """

    _construct_folder_id: str
    _fragment_folder_id: Union[Unset, str] = UNSET
    _primer_folder_id: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("construct_folder_id={}".format(repr(self._construct_folder_id)))
        fields.append("fragment_folder_id={}".format(repr(self._fragment_folder_id)))
        fields.append("primer_folder_id={}".format(repr(self._primer_folder_id)))
        return "AssemblySpecFinalizedOutputLocation({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        construct_folder_id = self._construct_folder_id
        fragment_folder_id = self._fragment_folder_id
        primer_folder_id = self._primer_folder_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if construct_folder_id is not UNSET:
            field_dict["constructFolderId"] = construct_folder_id
        if fragment_folder_id is not UNSET:
            field_dict["fragmentFolderId"] = fragment_folder_id
        if primer_folder_id is not UNSET:
            field_dict["primerFolderId"] = primer_folder_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_construct_folder_id() -> str:
            construct_folder_id = d.pop("constructFolderId")
            return construct_folder_id

        try:
            construct_folder_id = get_construct_folder_id()
        except KeyError:
            if strict:
                raise
            construct_folder_id = cast(str, UNSET)

        def get_fragment_folder_id() -> Union[Unset, str]:
            fragment_folder_id = d.pop("fragmentFolderId")
            return fragment_folder_id

        try:
            fragment_folder_id = get_fragment_folder_id()
        except KeyError:
            if strict:
                raise
            fragment_folder_id = cast(Union[Unset, str], UNSET)

        def get_primer_folder_id() -> Union[Unset, str]:
            primer_folder_id = d.pop("primerFolderId")
            return primer_folder_id

        try:
            primer_folder_id = get_primer_folder_id()
        except KeyError:
            if strict:
                raise
            primer_folder_id = cast(Union[Unset, str], UNSET)

        assembly_spec_finalized_output_location = cls(
            construct_folder_id=construct_folder_id,
            fragment_folder_id=fragment_folder_id,
            primer_folder_id=primer_folder_id,
        )

        return assembly_spec_finalized_output_location

    @property
    def construct_folder_id(self) -> str:
        """ API identifier of the folder in which to create the constructs """
        if isinstance(self._construct_folder_id, Unset):
            raise NotPresentError(self, "construct_folder_id")
        return self._construct_folder_id

    @construct_folder_id.setter
    def construct_folder_id(self, value: str) -> None:
        self._construct_folder_id = value

    @property
    def fragment_folder_id(self) -> str:
        """ API identifier of the folder in which to create the fragments, if any. If not specified, fragments will not be created. """
        if isinstance(self._fragment_folder_id, Unset):
            raise NotPresentError(self, "fragment_folder_id")
        return self._fragment_folder_id

    @fragment_folder_id.setter
    def fragment_folder_id(self, value: str) -> None:
        self._fragment_folder_id = value

    @fragment_folder_id.deleter
    def fragment_folder_id(self) -> None:
        self._fragment_folder_id = UNSET

    @property
    def primer_folder_id(self) -> str:
        """ API identifier of the folder in which to create the primers, if any. If not specified, primers will not be created as Benchling oligos, but will still be referencable in the context of the assembly, if they were designed. """
        if isinstance(self._primer_folder_id, Unset):
            raise NotPresentError(self, "primer_folder_id")
        return self._primer_folder_id

    @primer_folder_id.setter
    def primer_folder_id(self, value: str) -> None:
        self._primer_folder_id = value

    @primer_folder_id.deleter
    def primer_folder_id(self) -> None:
        self._primer_folder_id = UNSET
