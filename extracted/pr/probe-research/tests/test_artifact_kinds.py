"""The client's copy of the artifact kind vocabulary (`probe.sdk.artifact_kinds`)
and the client code that reads a kind through it.

The server normalizes every write (migration 0336's trigger), so nothing here
decides what is STORED; these pin what the client SAYS about a word (`probe
artifact add`'s "filed as" line), which words count as code (a code artifact is
stored, never pointed at), and which kind travels as "no kind" on an upload.
The server's `tests/unit/test_artifact_kinds.py` pins this copy to
`app/core/artifact_kinds.py`.
"""

from __future__ import annotations

import importlib

import pytest

from probe.sdk.artifact_kinds import (
    ARTIFACT_KIND_ALIASES,
    DEFAULT_ARTIFACT_KIND,
    KIND_LABEL_MAX_CHARS,
    SYSTEM_ARTIFACT_KINDS,
    UNLABELLED_WORDS,
    USER_ARTIFACT_KINDS,
    ArtifactKind,
    normalize_artifact_kind,
    stored_kind_values,
)
from probe.sdk.filetype import kind_to_send

K = ArtifactKind


@pytest.mark.parametrize(
    ("word", "kind", "label"),
    [
        # A listed value is itself, unlabelled, in any case or separator.
        ("checkpoint", K.CHECKPOINT, None),
        ("dataset", K.DATASET, None),
        ("evaluation", K.EVALUATION, None),
        ("code", K.CODE, None),
        ("other", K.OTHER, None),
        ("code_snapshot", K.CODE_SNAPSHOT, None),
        ("harbor_capture_manifest", K.HARBOR_CAPTURE_MANIFEST, None),
        ("Checkpoint", K.CHECKPOINT, None),
        ("  DATASET ", K.DATASET, None),
        ("code-snapshot", K.CODE_SNAPSHOT, None),
        ("Code-Bytes", K.CODE_BYTES, None),
        ("inputs decision", K.INPUTS_DECISION, None),
        # An alias is its kind, labelled with the word as spoken (lowercased).
        ("benchmark", K.EVALUATION, "benchmark"),
        ("Benchmark", K.EVALUATION, "benchmark"),
        ("model", K.CHECKPOINT, "model"),
        ("data", K.DATASET, "data"),
        ("script", K.CODE, "script"),
        ("test", K.CODE, "test"),
        ("code-bundle", K.CODE, "code-bundle"),
        ("input_decision", K.INPUTS_DECISION, "input_decision"),
        # "Nobody said": other, NO label.
        ("file", K.OTHER, None),
        ("FILE", K.OTHER, None),
        ("", K.OTHER, None),
        ("   ", K.OTHER, None),
        (None, K.OTHER, None),
        # Anything else: other, labelled.
        ("plot", K.OTHER, "plot"),
        ("Report", K.OTHER, "report"),
        ("note", K.OTHER, "note"),
    ],
)
def test_normalize(word, kind, label):
    assert normalize_artifact_kind(word) == (kind, label)


def test_a_long_word_is_kept_cut_to_the_label_limit():
    kind, label = normalize_artifact_kind("  " + "A" * 100 + "  ")
    assert kind is K.OTHER
    assert label == "a" * KIND_LABEL_MAX_CHARS and KIND_LABEL_MAX_CHARS == 64
    # At the limit exactly, the word is kept whole.
    assert normalize_artifact_kind("x" * 64) == (K.OTHER, "x" * 64)


def test_the_two_sets_split_the_ten_values():
    assert len(ArtifactKind) == 10
    assert set(USER_ARTIFACT_KINDS) | set(SYSTEM_ARTIFACT_KINDS) == set(ArtifactKind)
    assert not set(USER_ARTIFACT_KINDS) & set(SYSTEM_ARTIFACT_KINDS)
    assert DEFAULT_ARTIFACT_KIND is K.OTHER and DEFAULT_ARTIFACT_KIND in USER_ARTIFACT_KINDS
    assert [k.value for k in USER_ARTIFACT_KINDS] == ["checkpoint", "dataset", "evaluation", "code", "other"]


def test_no_alias_shadows_a_value_or_an_unlabelled_word():
    """An alias equal to a listed value (or to `file`) would never be read:
    `normalize_artifact_kind` answers those first."""
    values = {k.value for k in ArtifactKind}
    for alias, target in ARTIFACT_KIND_ALIASES.items():
        assert alias not in values and alias not in UNLABELLED_WORDS, alias
        assert alias == alias.lower() and "-" not in alias and " " not in alias, alias
        assert target in ArtifactKind


def test_stored_kind_values():
    assert stored_kind_values(K.CODE) == ["code", "script", "source", "test", "code_bundle"]
    assert stored_kind_values(K.OTHER) == ["other", "file"]
    assert stored_kind_values(K.HARBOR_TRIAL) == ["harbor_trial"]


def test_the_module_is_values_only():
    """`kind_filter_sql` builds SQL and stays on the server."""
    from probe.sdk import artifact_kinds

    assert not hasattr(artifact_kinds, "kind_filter_sql")


# -- what an upload sends ---------------------------------------------------------


@pytest.mark.parametrize(
    ("kind", "sent"),
    [
        (None, None),
        ("other", None),
        ("Other", None),
        ("file", None),
        ("", None),
        ("checkpoint", "checkpoint"),
        ("evaluation", "evaluation"),
        # A word the server labels travels as typed: the label is the word.
        ("report", "report"),
        ("benchmark", "benchmark"),
        ("Code-Snapshot", "Code-Snapshot"),
    ],
)
def test_the_default_kind_travels_as_no_kind(kind, sent):
    assert kind_to_send(kind) == sent


# -- the code-kind rule (`probe artifact add`) --------------------------------------


def _is_code_kind():
    return importlib.import_module("probe.cli.main")._is_code_kind


@pytest.mark.parametrize(
    "word",
    [
        "code", "Code", " code ", "script", "source", "test", "code_bundle", "code-bundle",
        "code_snapshot", "code-snapshot", " Code-Snapshot ", "code_bytes", "code-bytes",
    ],
)
def test_every_word_filed_as_code_is_a_code_kind(word):
    assert _is_code_kind()(word) is True


@pytest.mark.parametrize(
    "word", [None, "", "file", "other", "checkpoint", "evaluation", "notebook", "codes", "report"]
)
def test_other_words_are_not_code_kinds(word):
    assert _is_code_kind()(word) is False
