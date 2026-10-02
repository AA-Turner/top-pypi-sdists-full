from pytest import raises

from stjames import ProteinSequence, ResidueModification


def test_protein_sequence_defaults() -> None:
    p = ProteinSequence(sequence="PRSKSDARTRLV")
    assert p.cyclic is False
    assert p.modifications == []


def test_modification_round_trips() -> None:
    p = ProteinSequence(sequence="PRSKSDARTRLV", modifications=[ResidueModification(position=5, ccd="SEP")])
    assert p.modifications == [ResidueModification(position=5, ccd="SEP")]


def test_modification_position_must_be_zero_based() -> None:
    with raises(ValueError):
        ResidueModification(position=-1, ccd="SEP")


def test_modification_ccd_must_be_nonempty() -> None:
    with raises(ValueError):
        ResidueModification(position=5, ccd="  ")


def test_modification_position_within_sequence() -> None:
    with raises(ValueError):
        ProteinSequence(sequence="PRSKSDARTRLV", modifications=[ResidueModification(position=99, ccd="SEP")])


def test_modification_no_duplicate_positions() -> None:
    with raises(ValueError):
        ProteinSequence(
            sequence="PRSKSDARTRLV",
            modifications=[ResidueModification(position=5, ccd="SEP"), ResidueModification(position=5, ccd="TPO")],
        )
