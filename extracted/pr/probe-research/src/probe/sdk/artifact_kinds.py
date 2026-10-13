"""The artifact kind vocabulary, client copy: mirrors ``app/core/artifact_kinds.py``.

`artifacts.kind` holds one of ten values. Five a person or agent chooses --
`checkpoint`, `dataset`, `evaluation`, `code`, `other` -- and five Probe writes
itself (`code_snapshot`, `code_bytes`, `inputs_decision`, `harbor_trial`,
`harbor_capture_manifest`). Any other word is stored as `other` with the word
kept in `meta.kind_label`; a known alias (`benchmark`, `model`, `script`, ...) is
stored as its kind with the word kept the same way; `file` and empty are
`other`, unlabelled.

THE SERVER NORMALIZES, NOT THIS MODULE. The database trigger rewrites every
write, so the client sends whatever word it was given and never has to fold it
first. This copy is for what the client SAYS and for the readers that key on a
kind: `probe artifact add` reporting where a word was filed, and the code-kind
rule that refuses a pointer to code.

Dependency-free (``probe._compat`` only, for Python 3.10's StrEnum) so the SDK,
the CLI and a test can all import it. The server's `kind_filter_sql` is not
copied: it builds SQL. `tests/unit/test_artifact_kinds.py` (server side) pins
this copy's values and aliases to the server's, so change both or neither.
"""

from __future__ import annotations

from probe._compat import StrEnum


class ArtifactKind(StrEnum):
    """The ten values `artifacts.kind` may hold (0336 CHECK)."""

    CHECKPOINT = "checkpoint"
    DATASET = "dataset"
    EVALUATION = "evaluation"
    CODE = "code"
    OTHER = "other"
    CODE_SNAPSHOT = "code_snapshot"
    CODE_BYTES = "code_bytes"
    INPUTS_DECISION = "inputs_decision"
    HARBOR_TRIAL = "harbor_trial"
    HARBOR_CAPTURE_MANIFEST = "harbor_capture_manifest"


#: The kinds a person or agent picks; `--kind` offers these and only these.
USER_ARTIFACT_KINDS: tuple[ArtifactKind, ...] = (
    ArtifactKind.CHECKPOINT,
    ArtifactKind.DATASET,
    ArtifactKind.EVALUATION,
    ArtifactKind.CODE,
    ArtifactKind.OTHER,
)

#: Written by Probe's own clients (code capture, the inputs record, the Harbor
#: connector). Allowed values, never refused.
SYSTEM_ARTIFACT_KINDS: tuple[ArtifactKind, ...] = (
    ArtifactKind.CODE_SNAPSHOT,
    ArtifactKind.CODE_BYTES,
    ArtifactKind.INPUTS_DECISION,
    ArtifactKind.HARBOR_TRIAL,
    ArtifactKind.HARBOR_CAPTURE_MANIFEST,
)

#: What a row gets when the caller names no kind.
DEFAULT_ARTIFACT_KIND = ArtifactKind.OTHER

#: Where the word a caller sent is kept when it is not the stored kind.
KIND_LABEL_KEY = "kind_label"

#: A kept word is cut to this many characters: a label, not a document.
KIND_LABEL_MAX_CHARS = 64

#: Words that mean "nobody said": stored as `other` with NO label, so a label
#: always means a person or agent chose a word.
UNLABELLED_WORDS: frozenset[str] = frozenset({"", "file"})

#: Spellings stored as a listed kind, keyed after `_lookup_key` (lowercase,
#: `-` and spaces read as `_`). The server's table, word for word.
ARTIFACT_KIND_ALIASES: dict[str, ArtifactKind] = {
    **dict.fromkeys(
        ("checkpoint_reference", "checkpoint_manifest", "model", "weights", "ckpt"),
        ArtifactKind.CHECKPOINT,
    ),
    **dict.fromkeys(("data", "dataset_manifest", "dataset_reference"), ArtifactKind.DATASET),
    **dict.fromkeys(
        (
            "result",
            "results",
            "result_reference",
            "evaluation_result",
            "evaluation_results",
            "evaluation_output",
            "evaluation_summary",
            "evaluation_validation",
            "evaluation_reference",
            "benchmark",
            "validation",
            "validation_output",
            "metrics",
            "metrics_export",
            "test_report",
            "samples",
            "predictions",
            "generations",
        ),
        ArtifactKind.EVALUATION,
    ),
    **dict.fromkeys(("script", "source", "test", "code_bundle"), ArtifactKind.CODE),
    "input_decision": ArtifactKind.INPUTS_DECISION,
}


def _lookup_key(word: str) -> str:
    return word.strip().lower().replace("-", "_").replace(" ", "_")


def normalize_artifact_kind(word: str | None) -> tuple[ArtifactKind, str | None]:
    """The stored kind for `word` and the label kept beside it (None for none).

    A listed value (in any case or with `-` for `_`) is itself, unlabelled; an
    alias is its kind, labelled with the word; `file`, empty and None are
    `other`, unlabelled; anything else is `other`, labelled.
    """
    spoken = (word or "").strip().lower()
    key = _lookup_key(spoken)
    if key in ArtifactKind.__members__.values():
        return ArtifactKind(key), None
    if key in UNLABELLED_WORDS:
        return ArtifactKind.OTHER, None
    label = spoken[:KIND_LABEL_MAX_CHARS]
    return ARTIFACT_KIND_ALIASES.get(key, ArtifactKind.OTHER), label


def stored_kind_values(kind: ArtifactKind) -> list[str]:
    """Every raw `artifacts.kind` value a filter for `kind` must match while old
    rows are still being rewritten: the kind and each alias of it (and, for
    `other`, the unlabelled words). After the backfill only the first exists."""
    values = [kind.value, *(alias for alias, target in ARTIFACT_KIND_ALIASES.items() if target is kind)]
    if kind is ArtifactKind.OTHER:
        values.extend(sorted(UNLABELLED_WORDS - {""}))
    return values
