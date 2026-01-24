from typing import Union

from ..extensions import UnknownType
from ..models.aa_sequence_with_entity_type import AaSequenceWithEntityType
from ..models.custom_entity_with_entity_type import CustomEntityWithEntityType
from ..models.dna_oligo_with_entity_type import DnaOligoWithEntityType
from ..models.dna_sequence_with_entity_type import DnaSequenceWithEntityType
from ..models.mixture_with_entity_type import MixtureWithEntityType
from ..models.molecule_with_entity_type import MoleculeWithEntityType
from ..models.rna_oligo_with_entity_type import RnaOligoWithEntityType
from ..models.rna_sequence_with_entity_type import RnaSequenceWithEntityType

Entity = Union[
    DnaSequenceWithEntityType,
    RnaSequenceWithEntityType,
    AaSequenceWithEntityType,
    MixtureWithEntityType,
    DnaOligoWithEntityType,
    RnaOligoWithEntityType,
    MoleculeWithEntityType,
    CustomEntityWithEntityType,
    UnknownType,
]
