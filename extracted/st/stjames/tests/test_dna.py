from pytest import raises

from stjames import DNASequence, NucleotideModification


def test_dna_sequence_defaults() -> None:
    d = DNASequence(sequence="ATCGATCG")
    assert d.modifications == []


def test_modification_round_trips() -> None:
    d = DNASequence(sequence="ATCGATCG", modifications=[NucleotideModification(position=2, ccd="5MC")])
    assert d.modifications == [NucleotideModification(position=2, ccd="5MC")]


def test_modification_position_must_be_zero_based() -> None:
    with raises(ValueError):
        NucleotideModification(position=-1, ccd="5MC")


def test_modification_ccd_must_be_nonempty() -> None:
    with raises(ValueError):
        NucleotideModification(position=2, ccd="  ")


def test_modification_position_within_sequence() -> None:
    with raises(ValueError):
        DNASequence(sequence="ATCGATCG", modifications=[NucleotideModification(position=99, ccd="5MC")])


def test_modification_no_duplicate_positions() -> None:
    with raises(ValueError):
        DNASequence(
            sequence="ATCGATCG",
            modifications=[NucleotideModification(position=2, ccd="5MC"), NucleotideModification(position=2, ccd="DHU")],
        )
