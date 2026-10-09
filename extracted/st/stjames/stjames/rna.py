"""RNA-related data models."""

from typing import Self

from pydantic import model_validator

from .base import Base
from .nucleotide import NucleotideModification


class RNASequence(Base):
    """RNA sequence data.

    Attributes:
        sequence: nucleotide string
        modifications: non-standard nucleotides overriding positions in the sequence
    """

    sequence: str
    modifications: list[NucleotideModification] = []

    @model_validator(mode="after")
    def validate_modifications(self) -> Self:
        """Check RNA modification positions and uniqueness.

        Returns:
            validated sequence

        Raises:
            ValueError: modification is out of range or duplicated
        """
        seen: set[int] = set()
        for mod in self.modifications:
            if mod.position >= len(self.sequence):
                raise ValueError(f"Modification position {mod.position} is outside the sequence of length {len(self.sequence)}")
            if mod.position in seen:
                raise ValueError(f"Multiple modifications specified for position {mod.position}")
            seen.add(mod.position)
        return self
