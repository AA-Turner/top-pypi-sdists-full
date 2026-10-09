"""Define multiple sequence alignment workflows."""

from ..base import LowercaseStrEnum
from .workflow import ProteinSequenceWorkflow


class MSAFormat(LowercaseStrEnum):
    """Format of the MSA."""

    COLABFOLD = "colabfold"
    CHAI = "chai"
    BOLTZ = "boltz"


class MSAWorkflow(ProteinSequenceWorkflow):
    """Workflow for generating a MSA from protein sequences.

    Attributes:
        initial_protein_sequences: protein sequences of interest

        output_formats: formats of MSA return files
    """

    output_formats: list[MSAFormat] = [MSAFormat.COLABFOLD]
