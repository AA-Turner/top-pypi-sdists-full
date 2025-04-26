from typing import Any, cast, Dict, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.assembly_protein_reference_polymer_type import AssemblyProteinReferencePolymerType
from ..types import UNSET, Unset

T = TypeVar("T", bound="AssemblyProteinReference")


@attr.s(auto_attribs=True, repr=False)
class AssemblyProteinReference:
    """  """

    _polymer_type: AssemblyProteinReferencePolymerType
    _protein_id: str

    def __repr__(self):
        fields = []
        fields.append("polymer_type={}".format(repr(self._polymer_type)))
        fields.append("protein_id={}".format(repr(self._protein_id)))
        return "AssemblyProteinReference({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        polymer_type = self._polymer_type.value

        protein_id = self._protein_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if polymer_type is not UNSET:
            field_dict["polymerType"] = polymer_type
        if protein_id is not UNSET:
            field_dict["proteinId"] = protein_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_polymer_type() -> AssemblyProteinReferencePolymerType:
            _polymer_type = d.pop("polymerType")
            try:
                polymer_type = AssemblyProteinReferencePolymerType(_polymer_type)
            except ValueError:
                polymer_type = AssemblyProteinReferencePolymerType.of_unknown(_polymer_type)

            return polymer_type

        try:
            polymer_type = get_polymer_type()
        except KeyError:
            if strict:
                raise
            polymer_type = cast(AssemblyProteinReferencePolymerType, UNSET)

        def get_protein_id() -> str:
            protein_id = d.pop("proteinId")
            return protein_id

        try:
            protein_id = get_protein_id()
        except KeyError:
            if strict:
                raise
            protein_id = cast(str, UNSET)

        assembly_protein_reference = cls(
            polymer_type=polymer_type,
            protein_id=protein_id,
        )

        return assembly_protein_reference

    @property
    def polymer_type(self) -> AssemblyProteinReferencePolymerType:
        if isinstance(self._polymer_type, Unset):
            raise NotPresentError(self, "polymer_type")
        return self._polymer_type

    @polymer_type.setter
    def polymer_type(self, value: AssemblyProteinReferencePolymerType) -> None:
        self._polymer_type = value

    @property
    def protein_id(self) -> str:
        """ API identifier for the amino acid sequence. """
        if isinstance(self._protein_id, Unset):
            raise NotPresentError(self, "protein_id")
        return self._protein_id

    @protein_id.setter
    def protein_id(self, value: str) -> None:
        self._protein_id = value
