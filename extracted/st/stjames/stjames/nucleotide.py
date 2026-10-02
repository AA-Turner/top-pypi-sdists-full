"""Nucleotide modification data models shared by DNA and RNA."""

from typing import Self

from pydantic import model_validator

from .base import Base


class NucleotideModification(Base):
    """
    A non-standard (modified) nucleotide at a position in a nucleic acid sequence.

    The canonical nucleotide at `position` is replaced by the residue named by
    the Chemical Component Dictionary (CCD) code, e.g. `5MC` for 5-methylcytosine.

    :param position: 0-based index of the modified nucleotide in the sequence
    :param ccd: CCD code of the modified nucleotide (e.g. `5MC`)
    """

    position: int
    ccd: str

    @model_validator(mode="after")
    def validate_modification(self) -> Self:
        if self.position < 0:
            raise ValueError(f"Modification position must be 0-based (>= 0), got {self.position}")
        if not self.ccd.strip():
            raise ValueError("Modification ccd must be a non-empty CCD code")
        return self
