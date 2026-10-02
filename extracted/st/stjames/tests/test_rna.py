from pytest import raises

from stjames import NucleotideModification, RNASequence


def test_rna_sequence_defaults() -> None:
    r = RNASequence(sequence="AUCGAUCG")
    assert r.modifications == []


def test_modification_round_trips() -> None:
    r = RNASequence(sequence="AUCGAUCG", modifications=[NucleotideModification(position=2, ccd="PSU")])
    assert r.modifications == [NucleotideModification(position=2, ccd="PSU")]


def test_modification_position_must_be_zero_based() -> None:
    with raises(ValueError):
        NucleotideModification(position=-1, ccd="PSU")


def test_modification_ccd_must_be_nonempty() -> None:
    with raises(ValueError):
        NucleotideModification(position=2, ccd="  ")


def test_modification_position_within_sequence() -> None:
    with raises(ValueError):
        RNASequence(sequence="AUCGAUCG", modifications=[NucleotideModification(position=99, ccd="PSU")])


def test_modification_no_duplicate_positions() -> None:
    with raises(ValueError):
        RNASequence(
            sequence="AUCGAUCG",
            modifications=[NucleotideModification(position=2, ccd="PSU"), NucleotideModification(position=2, ccd="5MC")],
        )
