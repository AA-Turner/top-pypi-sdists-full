from typing import Union

from ..extensions import UnknownType
from ..models.dna_oligo import DnaOligo
from ..models.rna_oligo import RnaOligo

Oligo = Union[DnaOligo, RnaOligo, UnknownType]
