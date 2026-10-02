"""Protein-related data models."""

from typing import Self

from pydantic import model_validator

from .base import Base


class ResidueModification(Base):
    """
    A non-standard (modified) residue at a position in a protein sequence.

    The canonical residue at `position` is replaced by the residue named by
    the Chemical Component Dictionary (CCD) code, e.g. `SEP` for phosphoserine.

    :param position: 0-based index of the modified residue in the sequence
    :param ccd: CCD code of the modified residue (e.g. `SEP`)
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


class ProteinSequence(Base):
    """
    Protein sequence data.

    :param sequence: amino-acid sequence string
    :param cyclic: whether this sequence forms a cyclic peptide
    :param modifications: non-standard residues overriding positions in the sequence
    """

    sequence: str
    cyclic: bool = False
    id: str | None = None
    modifications: list[ResidueModification] = []

    @model_validator(mode="after")
    def validate_modifications(self) -> Self:
        seen: set[int] = set()
        for mod in self.modifications:
            if mod.position >= len(self.sequence):
                raise ValueError(f"Modification position {mod.position} is outside the sequence of length {len(self.sequence)}")
            if mod.position in seen:
                raise ValueError(f"Multiple modifications specified for position {mod.position}")
            seen.add(mod.position)
        return self
