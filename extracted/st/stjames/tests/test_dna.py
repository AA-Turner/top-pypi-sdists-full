"""Test dna behavior and validation."""

from pytest import raises

from stjames import DNASequence, NucleotideModification


def test_dna_sequence_defaults() -> None:
    """Initialize DNA sequences without residue modifications."""
    d = DNASequence(sequence="ATCGATCG")
    assert d.modifications == []


def test_modification_round_trips() -> None:
    """Preserve modified residue positions and CCD identifiers."""
    d = DNASequence(sequence="ATCGATCG", modifications=[NucleotideModification(position=2, ccd="5MC")])
    assert d.modifications == [NucleotideModification(position=2, ccd="5MC")]


def test_modification_position_must_be_zero_based() -> None:
    """Reject negative residue modification indices."""
    with raises(ValueError):
        NucleotideModification(position=-1, ccd="5MC")


def test_modification_ccd_must_be_nonempty() -> None:
    """Reject empty CCD identifiers for modified residues."""
    with raises(ValueError):
        NucleotideModification(position=2, ccd="  ")


def test_modification_position_within_sequence() -> None:
    """Reject residue modifications beyond the sequence length."""
    with raises(ValueError):
        DNASequence(sequence="ATCGATCG", modifications=[NucleotideModification(position=99, ccd="5MC")])


def test_modification_no_duplicate_positions() -> None:
    """Reject multiple modifications at the same sequence position."""
    with raises(ValueError):
        DNASequence(
            sequence="ATCGATCG",
            modifications=[NucleotideModification(position=2, ccd="5MC"), NucleotideModification(position=2, ccd="DHU")],
        )
