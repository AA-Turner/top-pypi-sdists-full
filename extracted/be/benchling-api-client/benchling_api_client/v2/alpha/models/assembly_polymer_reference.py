from typing import Union

from ..extensions import UnknownType
from ..models.assembly_protein_reference import AssemblyProteinReference
from ..models.assembly_sequence_reference import AssemblySequenceReference

AssemblyPolymerReference = Union[AssemblySequenceReference, AssemblyProteinReference, UnknownType]
