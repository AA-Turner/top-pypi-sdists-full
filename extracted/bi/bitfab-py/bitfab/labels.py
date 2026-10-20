"""Deprecated module. Import the ``Verdict*`` names and ``VerdictsClient`` from ``bitfab.verdicts`` instead."""

from bitfab.traces import AssertionLabelEvidence
from bitfab.verdicts import (
    HUMAN_VERDICTS_PATH,
    VERDICTS_PATH,
    AssertionVerdict,
    HumanLabelUpdate,
    HumanVerdictOutcome,
    LabelStatus,
    LabelUpdate,
    TraceVerdicts,
    Verdict,
    VerdictAction,
    VerdictConfidence,
    VerdictOutcome,
    VerdictsClient,
    VerdictSource,
)

LABELS_PATH = VERDICTS_PATH
HUMAN_LABELS_PATH = HUMAN_VERDICTS_PATH
LabelConfidence = VerdictConfidence
LabelAction = VerdictAction
LabelSource = VerdictSource
LabelOutcome = VerdictOutcome
HumanLabelOutcome = HumanVerdictOutcome
TraceLabels = TraceVerdicts
LabelsClient = VerdictsClient

__all__ = [
    "HUMAN_LABELS_PATH",
    "LABELS_PATH",
    "AssertionLabelEvidence",
    "AssertionVerdict",
    "HumanLabelOutcome",
    "HumanLabelUpdate",
    "LabelAction",
    "LabelConfidence",
    "LabelOutcome",
    "LabelSource",
    "LabelStatus",
    "LabelUpdate",
    "LabelsClient",
    "TraceLabels",
    "Verdict",
]
