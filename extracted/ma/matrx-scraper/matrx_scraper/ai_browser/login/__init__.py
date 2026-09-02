"""Agent-directed login — the pure, injectable core (WS-7, D-11/D-12).

A login is a CAPABILITY, not a page interaction. The agent states the whole attempt
in one call (``spec``); the system resolves and types the secret without the agent
seeing it (``executor`` + injected ``SecretResolver``/``WorkerFill``); verification
returns one of four outcomes with a confidence value and the signals that produced it
(``verifier``); state is captured before and after (core, not diagnostics); per-site
recipes turn a fragile guess into a reliable login (``recipe``); every result tells
the agent how to report a leak (``leak_report``); the six-digit code is a follow-up
call, never part of the first (``totp_seam``).

Everything here is pure or protocol-injected, so the whole flow is testable against
synthetic pages and a FakeWorker before any real worker or DB exists. Persistence
(``browser.login_attempt`` / ``browser.login_recipe`` / ``browser.capture``) and the
vault resolution live in the aidream host, which consumes these primitives.
"""

from __future__ import annotations

from .capture import (
    CaptureBranch,
    CaptureContext,
    CaptureFieldSpec,
    CaptureReceipt,
    CredentialCaptureSpec,
    DocumentedRecipeSpec,
    LoginAttemptStore,
    RecipeStore,
    build_proposed_recipe,
    resolve_capture_context,
)
from .executor import (
    FieldUnavailable,
    PageObserver,
    SecretResolver,
    StateCapturer,
    WorkerFill,
    run_login_attempt,
)
from .leak_report import HOW_TO_REPORT, FeedbackBlock, LeakReport, feedback_block
from .recipe import (
    AWS_IAM_CONSOLE_RECIPE,
    SEEDED_RECIPES,
    LoginRecipe,
    RecipeFieldMap,
    SignalDescriptor,
    match_seeded_recipe,
)
from .results import CaptureRef, LoginAttemptResult, RecipeRef
from .spec import (
    AttemptSpec,
    ExpectSpec,
    FieldSpec,
    SpecIncompleteError,
    StepSpec,
    SubmitSpec,
    WaitForSpec,
)
from .totp_seam import ChallengeResponse, TotpCodeInjector
from .verifier import (
    AMBIGUOUS_STRUCTURAL_REASONS,
    AUTH_FLOW_URL_SEGMENTS,
    CHALLENGE_URL_SEGMENTS,
    Outcome,
    PageObservation,
    Verdict,
    VerdictSignal,
    url_segments,
    verify,
)

__all__ = [
    "AWS_IAM_CONSOLE_RECIPE",
    "AttemptSpec",
    "CaptureBranch",
    "CaptureContext",
    "CaptureFieldSpec",
    "CaptureReceipt",
    "CaptureRef",
    "CredentialCaptureSpec",
    "DocumentedRecipeSpec",
    "LoginAttemptStore",
    "RecipeStore",
    "build_proposed_recipe",
    "resolve_capture_context",
    "ChallengeResponse",
    "ExpectSpec",
    "FeedbackBlock",
    "FieldSpec",
    "FieldUnavailable",
    "HOW_TO_REPORT",
    "LeakReport",
    "LoginAttemptResult",
    "LoginRecipe",
    "Outcome",
    "AMBIGUOUS_STRUCTURAL_REASONS",
    "AUTH_FLOW_URL_SEGMENTS",
    "CHALLENGE_URL_SEGMENTS",
    "PageObservation",
    "PageObserver",
    "RecipeFieldMap",
    "RecipeRef",
    "SEEDED_RECIPES",
    "SecretResolver",
    "SignalDescriptor",
    "SpecIncompleteError",
    "StateCapturer",
    "StepSpec",
    "SubmitSpec",
    "TotpCodeInjector",
    "Verdict",
    "VerdictSignal",
    "WaitForSpec",
    "WorkerFill",
    "feedback_block",
    "match_seeded_recipe",
    "run_login_attempt",
    "url_segments",
    "verify",
]
