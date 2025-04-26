from typing import Union

from ..extensions import UnknownType
from ..models.aa_sequence import AaSequence
from ..models.custom_entity import CustomEntity
from ..models.dna_oligo import DnaOligo
from ..models.dna_sequence import DnaSequence
from ..models.inaccessible_resource import InaccessibleResource
from ..models.mixture import Mixture
from ..models.rna_oligo import RnaOligo

EntityOrInaccessibleResource = Union[
    Union[DnaSequence, AaSequence, Mixture, DnaOligo, RnaOligo, CustomEntity, UnknownType],
    InaccessibleResource,
    UnknownType,
]
