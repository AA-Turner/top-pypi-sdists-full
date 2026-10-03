"""Brand voice kinds — the measured fingerprint of how one person or brand writes.

``voice_fingerprint`` is the stored profile: every field is a number or a set
computed from 5-20 real writing samples by the ``brand_voice_measure`` tool
(aidream ``services/voice_measure``) — never a model's guess and never an
adjective like "warm, professional". It mirrors the ``voice.yaml`` schema of the
voice-extractor skill (Elvis Sun and Carly Martinetti, MIT) field for field, with
a few measured additions named in the field descriptions.

``voice_measure_result`` is ONE union kind across the tool's two actions, the
``topical_map`` precedent: ``extract`` fills ``triage`` / ``fingerprint`` /
``fingerprint_id``; ``check`` fills exactly the skill's check contract
(``verdict``, ``pass_rate``, ``fingerprint``, ``violations``, ``stats``,
``regenerate``). The workflow node ``brand.voice_measure`` returns the same kind,
so a drafting workflow and a chat agent can never disagree about a check.

Raw sample text is never part of any kind here: samples are Sources, referenced
by id and a content hash.

It lives in the package, not in ``aidream/kinds/``, for the same reason as
``fact_check``: the tool result map below may never import aidream.

Publish with::

    uv run python scripts/publish_kind_catalog.py matrx_ai.tools.kinds.voice --apply
"""

from __future__ import annotations

from typing import Literal

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind
from pydantic import Field

Confidence = Literal["insufficient", "low", "medium", "high"]
UsageClass = Literal["never", "rare", "habitual"]


class SentenceLengthStats(KindSubModel):
    mean: float = Field(default=0.0, description="Mean words per sentence.")
    median: float = Field(default=0.0)
    p10: float = Field(default=0.0, description="10th percentile, linear interpolation.")
    p90: float = Field(default=0.0, description="90th percentile, linear interpolation.")
    stdev: float = Field(default=0.0, description="Population standard deviation of sentence length.")
    length_cv: float = Field(default=0.0, description="Burstiness: stdev / mean. AI prose clusters low.")
    one_word_sentence_frequency: float = Field(
        default=0.0, description="Share of sentences of one to three words."
    )
    long_sentence_frequency: float = Field(default=0.0, description="Share of sentences of 35 or more words.")


class ParagraphStats(KindSubModel):
    mean_sentences: float = Field(default=0.0, description="Mean sentences per paragraph (blank-line separated).")
    one_sentence_paragraph_frequency: float = Field(default=0.0)


class Cadence(KindSubModel):
    sentence_length: SentenceLengthStats = Field(default_factory=SentenceLengthStats)
    paragraph_length: ParagraphStats = Field(default_factory=ParagraphStats)
    rhythm_signature: Literal["short-burst", "flowing", "mixed", "listy"] = "mixed"


class CapitalizationQuirks(KindSubModel):
    lowercase_i: bool = False
    sentence_case_headers: bool = False
    all_caps_for_emphasis: Literal["never", "occasional", "habitual"] = "never"


class Mechanics(KindSubModel):
    contractions: Literal["yes", "no", "mixed"] = "mixed"
    contraction_rate: float = Field(default=0.0, description="Contracted / (contracted + expanded) contractible pairs.")
    em_dash_usage: UsageClass = "rare"
    em_dash_per_1k_words: float = 0.0
    oxford_comma: Literal["yes", "no", "inconsistent", "unknown"] = "unknown"
    ellipsis_usage: UsageClass = "never"
    ellipsis_per_1k_words: float = 0.0
    exclamation_rate_per_1k_words: float = 0.0
    question_rate_per_1k_words: float = 0.0
    semicolon_per_1k_words: float = 0.0
    parenthesis_per_1k_words: float = 0.0
    punctuation_classes: dict[str, UsageClass] = Field(
        default_factory=dict,
        description="never | rare | habitual per mark, by fixed cut-offs (< 0.5 per 1k never, < 3 rare).",
    )
    parenthetical_aside_frequency: Literal["low", "medium", "high"] = "low"
    capitalization_quirks: CapitalizationQuirks = Field(default_factory=CapitalizationQuirks)
    smart_quotes: Literal["yes", "no", "mixed"] = "no"


class Lexical(KindSubModel):
    mattr: float = Field(default=0.0, description="Moving-average type-token ratio over a 100-token window.")
    mattr_by_window: dict[str, float] = Field(
        default_factory=dict,
        description="MATTR at windows 25, 50 and 100, so a short draft is compared on a window it can fill.",
    )
    function_word_zvector: dict[str, float] = Field(
        default_factory=dict, description="Burrows's Delta z-scores of the baseline function words."
    )
    delta_band: float = Field(default=1.0, description="Delta distance above which a draft has drifted.")
    baseline_version: str = "english_baseline_v1"


class OpenerSet(KindSubModel):
    observed: list[str] = Field(default_factory=list)
    banned_from_use: list[str] = Field(default_factory=list)
    pos_distribution: dict[str, float] = Field(
        default_factory=dict, description="Share of sentences by the part of speech of their first token (spaCy)."
    )


class CloserSet(KindSubModel):
    observed: list[str] = Field(default_factory=list)
    banned_from_use: list[str] = Field(default_factory=list)


class SentenceInitial(KindSubModel):
    conjunction_starts_allowed: bool = False
    conjunction_start_rate: float = 0.0
    participial_start_rate: float = 0.0
    transitions_used: list[str] = Field(
        default_factory=list,
        description="Which of however / furthermore / moreover / additionally the samples really open with.",
    )
    uses_however_furthermore_moreover: bool = False
    uses_in_conclusion_in_summary: bool = False
    uses_imagine_if: bool = False


class Idioms(KindSubModel):
    signature_phrases: list[str] = Field(default_factory=list, description="Candidates for the person to confirm.")
    signature_words: list[str] = Field(default_factory=list, description="Candidates for the person to confirm.")
    hedges_you_actually_use: list[str] = Field(default_factory=list)
    hedges_you_never_use: list[str] = Field(default_factory=list)


class SampleInvolved(KindSubModel):
    source_id: str
    involved_score: float


class RegisterAxis(KindSubModel):
    involved_score: float = Field(
        default=0.0,
        description="(contraction + first_person + private_verb) - (noun_ratio + nominalization), all as shares.",
    )
    involved_band: float = Field(default=0.25, description="One band on the involved axis.")
    per_sample: list[SampleInvolved] = Field(default_factory=list)


class PerspectiveAnchors(KindSubModel):
    first_person_singular_rate: float = Field(default=0.0, description="Per 1,000 words.")
    first_person_plural_rate: float = 0.0
    second_person_rate: float = 0.0
    third_person_rate: float = 0.0


class TopicSignatures(KindSubModel):
    recurring_themes: list[str] = Field(default_factory=list)
    perspective_anchors: PerspectiveAnchors = Field(default_factory=PerspectiveAnchors)


class BannedStructure(KindSubModel):
    id: str
    pattern: str
    why: str = ""
    severity: Literal["block", "warn"] = "block"
    threshold: str | None = None


class SampleIndexEntry(KindSubModel):
    id: str = Field(description="The Source (processed document) id the text was read from.")
    source: str = "other"
    date: str | None = None
    audience: str | None = None
    word_count: int = 0
    hash: str = Field(default="", description="sha256 of the sample text; the text itself is never stored.")


class CorpusTriage(KindSubModel):
    sample_count: int = 0
    total_words: int = 0
    ai_tell_share: float = Field(default=0.0, description="Share of samples showing two or more named AI tells.")
    ai_tell_samples: list[str] = Field(default_factory=list, description="Source ids of the samples flagged.")
    register_split: bool = Field(default=False, description="True when the samples split into two registers.")
    per_sample_involved: list[SampleInvolved] = Field(default_factory=list)
    confidence: Confidence = "insufficient"
    warnings: list[str] = Field(default_factory=list)


class Extraction(KindSubModel):
    extractor_version: str = "brand.voice_measure/1.0.0"
    baseline_version: str = "english_baseline_v1"
    rules_version: str = "voice-extractor@092d882+matrx.1"
    warnings: list[str] = Field(default_factory=list)
    confidence: Confidence = "medium"
    triage: CorpusTriage | None = None


@kind(
    "voice_fingerprint",
    disposition="record",
    label="Voice Fingerprint",
    family="brand",
    example={
        "__kind": "voice_fingerprint",
        "profile_id": "jane-doe-personal",
        "profile_scope": "person",
        "register_label": "casual-professional",
        "sample_count": 8,
        "sample_word_count": 1240,
        "cadence": {"sentence_length": {"mean": 11.2, "p90": 24, "length_cv": 0.7}},
        "mechanics": {"em_dash_usage": "never", "contraction_rate": 0.82},
        "extraction": {"confidence": "medium"},
    },
    maturity="distilled",
)
class VoiceFingerprint(KindModel):
    """A measured writing voice: cadence, mechanics, lexicon, openers, register, idioms."""

    schema_version: int = 1
    profile_id: str = Field(description="Human-readable profile handle.")
    profile_scope: Literal["person", "brand"] = "person"
    created_at: str | None = None
    last_extracted_at: str | None = None
    refresh_due_at: str | None = Field(default=None, description="last_extracted_at + 90 days.")
    sample_count: int = 0
    sample_word_count: int = 0
    sample_age_p50_days: float | None = None
    sample_age_oldest_days: int | None = None
    intent: list[str] = Field(default_factory=list)
    register_label: Literal["formal", "professional", "casual-professional", "casual", "irreverent"] = Field(
        default="professional",
        description="voice.yaml's `register` (renamed: `register` shadows a pydantic model attribute).",
    )
    cadence: Cadence = Field(default_factory=Cadence)
    mechanics: Mechanics = Field(default_factory=Mechanics)
    lexical: Lexical = Field(default_factory=Lexical)
    openers: OpenerSet = Field(default_factory=OpenerSet)
    closers: CloserSet = Field(default_factory=CloserSet)
    sentence_initial: SentenceInitial = Field(default_factory=SentenceInitial)
    idioms: Idioms = Field(default_factory=Idioms)
    register_axis: RegisterAxis = Field(default_factory=RegisterAxis)
    banned_words_user_specific: list[str] = Field(default_factory=list)
    banned_words_global: list[str] = Field(default_factory=list)
    banned_words_global_allowed: list[str] = Field(
        default_factory=list,
        description="Globally banned words the person confirmed as genuinely theirs; the check lets them through.",
    )
    global_words_in_samples: list[str] = Field(
        default_factory=list, description="Globally banned words found in the real samples, flagged for review."
    )
    banned_structures: list[BannedStructure] = Field(default_factory=list)
    topic_signatures: TopicSignatures = Field(default_factory=TopicSignatures)
    samples_index: list[SampleIndexEntry] = Field(default_factory=list)
    extraction: Extraction = Field(default_factory=Extraction)


class VoiceViolation(KindSubModel):
    rule_id: str
    match: str = Field(description="The exact matched text (empty for whole-draft statistics).")
    span: list[int] = Field(description="[start, end] character offsets into the draft.")
    severity: Literal["block", "warn", "info"]
    fix_hint: str


class VoiceCheckStats(KindSubModel):
    draft_mean: float
    fingerprint_mean: float
    drift_score: float = Field(description="0 = on the fingerprint, 1 = fully off it (mean of capped drifts).")


@kind(
    "voice_measure_result",
    disposition="record",
    label="Voice Measurement",
    family="brand",
    example={
        "__kind": "voice_measure_result",
        "action": "check",
        "verdict": "fail",
        "pass_rate": 0.2,
        "fingerprint": "jane-doe-personal@2026-05-18",
        "violations": [
            {
                "rule_id": "banned-word-global",
                "match": "leverages",
                "span": [128, 137],
                "severity": "block",
                "fix_hint": "Use a plain verb such as 'uses', or rewrite the sentence.",
            }
        ],
        "stats": {"draft_mean": 10.2, "fingerprint_mean": 11.2, "drift_score": 0.31},
        "regenerate": True,
    },
    maturity="distilled",
)
class VoiceMeasureResult(KindModel):
    """One result of ``brand_voice_measure``: an extraction or a draft check."""

    action: Literal["extract", "check"]
    # ── check ──
    verdict: Literal["pass", "fail"] | None = None
    pass_rate: float | None = Field(default=None, description="Share of the draft's sentences with no violation.")
    fingerprint: str | None = Field(default=None, description="profile_id@YYYY-MM-DD of the fingerprint used.")
    violations: list[VoiceViolation] | None = None
    stats: VoiceCheckStats | None = None
    regenerate: bool | None = Field(default=None, description="True when any block violation means redraft.")
    # ── extract ──
    triage: CorpusTriage | None = None
    fingerprint_id: str | None = Field(default=None, description="The saved voice_fingerprint row id.")
    profile: VoiceFingerprint | None = Field(default=None, description="The extracted fingerprint.")
    summary: str | None = Field(default=None, description="Plain-English summary for the confirm step.")


VOICE_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "brand_voice_measure": VoiceMeasureResult,
}

__all__ = [
    "CorpusTriage",
    "VOICE_TOOL_RESULT_KINDS",
    "VoiceCheckStats",
    "VoiceFingerprint",
    "VoiceMeasureResult",
    "VoiceViolation",
]
