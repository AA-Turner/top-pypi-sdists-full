"""
decide: one `/v1/decide` call, as a one-shot request.

In one sentence:
`decide()` sends a state plus typed questions and returns calibrated probabilities, building the
exact wire body the gateway's `extra="forbid"` schema accepts and resolving the model against the
shared catalogue.

Upstream trigger  - a caller, once per request
Downstream effect - POST /v1/decide, or a local InvalidRequest naming the mismatch

Answered by a hosted model service, so like chat there is no cold-start wait. A
refused call is not billed: InvalidRequest (400) for criteria that do not fit their question type,
or a request the provider rejected (its own words in the message); Unavailable for a provider that
returned an error (502, retry once then report) or is rate limited or unreachable (503).

"""

from __future__ import annotations

from typing import Any

from .._core.catalogue import _envelope, _resolve
from .._core.transport import Transport
from ..errors import InvalidRequest
from .types import DecideResult


def decide(
    model: Any,
    state: Any,
    questions: dict[str, dict[str, Any]],
    *,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_s: float | None = None,
) -> DecideResult:
    """
    One `/v1/decide` call: a state and typed questions in, calibrated probabilities out.

    `questions` is keyed by your own names; each is
    `{"type": "noul"|"choice"|"score", "instructions": "...", "criteria": ...}`, and the type
    decides what `criteria` must be and what comes back in `answers[name]`:

    noul — a yes/no question; the answer is the probability of yes.
        criteria: optional; when given, {"true": what yes means, "false": what no means}
        {"held": {"type": "noul", "instructions": "Is the cup in the gripper?",
                  "criteria": {"true": "the cup is held", "false": "the cup is not held"}}}
        -> {"type": "noul", "noul": 0.97}

    choice — pick one of several options; the answer is a distribution over them.
        criteria: {option: description}, at least one option
        {"colour": {"type": "choice", "instructions": "What colour is the cup?",
                    "criteria": {"red": "a red cup", "blue": "a blue cup"}}}
        -> {"type": "choice", "choice": "red", "probabilities": {"red": 1, "blue": 0},
            "confidence": 1}

    score — a position on an ordered rubric; the answer is a distribution over its labels.
        criteria: [label, ...] from lowest to highest, at least one
        {"grip": {"type": "score", "instructions": "How firm is the grasp?",
                  "criteria": ["loose", "ok", "firm"]}}
        -> {"type": "score", "score": 1.23, "legend": {"0": "loose", "1": "ok", "2": "firm"},
            "probabilities": {"0": 0.02, "1": 0.73, "2": 0.25}, "confidence": 0.6}

    The model scores rather than generates, so there is no max_tokens or temperature — read
    each answer's `["type"]` and branch on it.

    Errors (a refused call is not billed):
    - InvalidRequest (400): criteria that do not fit the question's type — the message names the
      field, e.g. `questions.grip.criteria: a "score" question needs a list of rubric labels, in
      order, got an object` — or a request the provider rejected, with its own words.
    - Unavailable: the provider returned an error (502 — retry once, then report), or it is rate
      limited or unreachable (503 — `retry_after_s` says how long to wait when it is known).
    Answered by a hosted model service, so there is no cold-start wait.
    """
    m = _resolve(model, api_key, base_url, "decide")
    if m.endpoint != "decide":
        raise InvalidRequest(
            f"{m.short_id} is a {m.endpoint!r} model; decide() needs a decision model. "
            f"See models(endpoint='decide')."
        )
    if not questions:
        raise InvalidRequest("decide() needs at least one question")


    body: dict[str, Any] = {"model": m.id, "state": state, "questions": questions}
    t = Transport(api_key=api_key, base_url=base_url, timeout_s=timeout_s)
    try:
        r = t.post("/v1/decide", body, timeout_s=timeout_s)
    finally:
        t.close()
    env = _envelope(r, m.id)
    return DecideResult(
        id=env["id"], model=env["model"], answers=r.get("answers") or {},
        usage=env["usage"], perf=env["perf"], warnings=env["warnings"],
        cost_usd=float(r.get("cost_usd") or 0.0),
    )
