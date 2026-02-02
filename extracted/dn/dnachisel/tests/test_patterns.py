import pytest
from pathlib import Path

from dnachisel import SequencePattern, MotifPssmPattern


@pytest.fixture
def test_single_motif_filepath():
    return str(Path(__file__).parent / "data" / "single_motif.meme.txt")


@pytest.fixture
def test_multiple_motif_filepath():
    return str(Path(__file__).parent / "data" / "multiple_motifs.meme.txt")


def test_patterns_from_string():
    pattern = SequencePattern.from_string("6xT")
    assert pattern.expression == "TTTTTT"
    pattern = SequencePattern.from_string("BsmBI_site")
    assert pattern.expression == "CGTCTC"
    pattern = SequencePattern.from_string("5x2mer")
    assert pattern.expression == "([ATGC]{2})\\1{4}"


def test_pssm_pattern_from_file(
    test_single_motif_filepath, test_multiple_motif_filepath
):
    single_pattern = MotifPssmPattern.list_from_file(
        test_single_motif_filepath, "minimal", relative_threshold=0.9
    )
    assert len(single_pattern) == 1
    assert all([isinstance(p, MotifPssmPattern) for p in single_pattern])

    multiple_patterns = MotifPssmPattern.list_from_file(
        test_multiple_motif_filepath, "minimal", relative_threshold=0.9
    )
    assert len(multiple_patterns) == 2
    assert all([isinstance(p, MotifPssmPattern) for p in multiple_patterns])


def test_pssm_from_sequences():
    seqs = ["ACGT", "ACCT", "AAGT"]
    motif_name = "test motif"
    pat = MotifPssmPattern.from_sequences(seqs, name=motif_name, relative_threshold=0.9)
    assert isinstance(pat, MotifPssmPattern)
    assert len(pat.find_matches_in_string("ACATACGTACAC")) == 1
    assert len(pat.find_matches_in_string("ACATAATTACAC")) == 0
