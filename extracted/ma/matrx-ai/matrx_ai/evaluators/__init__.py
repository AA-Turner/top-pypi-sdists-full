"""Judges — the platform's evaluation primitive, and its accuracy record.

Start at :class:`JudgeContract` + :class:`Judge` (``judge.py``). A judge is a
first-class specialist with a declared contract and a measured track record
(Engram VISION §3.3); :class:`Selector` is the comparison-only specialization
that picks among speculative branches (§3.6); ``ledger.py`` records every
invocation to ``platform.judge_verdict`` and stamps the agreement bit when
ground truth arrives; ``calibration.py`` turns those rows into Cohen's kappa.

:class:`AIJudge` is the original strict-JSON pass/fail evaluator that the test
tier uses (``packages/matrx-graph/tests/conftest.py``). It stays — it is the
funnel :class:`Judge` is built on — but new evaluation goes through
:class:`Judge`, because AIJudge alone leaves no accuracy record.
"""

from matrx_ai.evaluators.ai_judge import AIJudge, JudgeError, JudgeVerdict
from matrx_ai.evaluators.calibration import (
    Calibration,
    LabeledCase,
    calibrate,
    cohens_kappa,
)
from matrx_ai.evaluators.judge import (
    COMPARATIVE_VERDICTS,
    RUBRIC_VERDICTS,
    EntityRef,
    Judge,
    JudgeAssessment,
    JudgeContract,
    JudgeContractError,
    JudgeInputs,
    JudgeOutcome,
    JudgeSubject,
)
from matrx_ai.evaluators.ledger import record_agreement, record_verdict
from matrx_ai.evaluators.selector import Selection, SelectionComparison, Selector

__all__ = [
    "COMPARATIVE_VERDICTS",
    "RUBRIC_VERDICTS",
    "AIJudge",
    "Calibration",
    "EntityRef",
    "Judge",
    "JudgeAssessment",
    "JudgeContract",
    "JudgeContractError",
    "JudgeError",
    "JudgeInputs",
    "JudgeOutcome",
    "JudgeSubject",
    "JudgeVerdict",
    "LabeledCase",
    "Selection",
    "SelectionComparison",
    "Selector",
    "calibrate",
    "cohens_kappa",
    "record_agreement",
    "record_verdict",
]
