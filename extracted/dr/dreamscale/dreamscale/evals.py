"""Real-robot evaluation client & blind randomized A/B runner (Continual Learning Loop M6).

Replaces external ``--hud`` grading with native Dreamscale eval sessions:
- ``EvalClient`` talks to ``/v1/evals/...`` and ``/v1/policies/{ref}/scoreboard``.
- ``parse_eval_grade`` parses concise operator input (``y``, ``n``, ``0.0-1.0``, ``d`` discard).
- ``run_blind_eval`` orchestrates a blind randomized A/B (or single-version) station session:
  fetches each blinded trial assignment from the control plane without showing which model runs,
  invokes the trial executor, collects the operator's grade, posts the trial, and reveals the
  statistical summary + winner verdict at the end.
"""

from __future__ import annotations

import math
import urllib.parse
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import httpx

EVAL_GRADE_PROMPT = (
    "Grade trial (y success · n failure · 0–1 partial · d discard [+ optional note]): "
)

_OUTCOME_WORDS: dict[str, tuple[str, float | None]] = {
    "y": ("success", 1.0),
    "yes": ("success", 1.0),
    "s": ("success", 1.0),
    "success": ("success", 1.0),
    "pass": ("success", 1.0),
    "n": ("failure", 0.0),
    "no": ("failure", 0.0),
    "f": ("failure", 0.0),
    "fail": ("failure", 0.0),
    "failure": ("failure", 0.0),
    "d": ("discarded", None),
    "discard": ("discarded", None),
    "skip": ("discarded", None),
}


@dataclass(frozen=True)
class EvalGrade:
    outcome: str
    score: float | None = None
    notes: str = ""


@dataclass(frozen=True)
class TrialExecution:
    takeover_count: int = 0
    autonomous_seconds: float = 0.0
    takeover_seconds: float = 0.0
    cycle_seconds: float | None = None
    episode_id: str | None = None
    usage_session_id: str | None = None


def parse_eval_grade(text: str) -> EvalGrade | None:
    """Parse operator grade input into ``EvalGrade``, or ``None`` if unrecognized."""
    cleaned = text.strip()
    if not cleaned:
        return None
    word, _, note = cleaned.partition(" ")
    match = _OUTCOME_WORDS.get(word.lower())
    if match is not None:
        return EvalGrade(outcome=match[0], score=match[1], notes=note.strip())
    try:
        val = float(word)
    except ValueError:
        return None
    if not math.isfinite(val) or not 0.0 <= val <= 1.0:
        return None
    if val >= 1.0:
        outcome = "success"
    elif val <= 0.0:
        outcome = "failure"
    else:
        outcome = "partial"
    return EvalGrade(outcome=outcome, score=round(val, 4), notes=note.strip())


def prompt_eval_grade(
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
) -> EvalGrade:
    while True:
        raw = input_fn(EVAL_GRADE_PROMPT)
        grade = parse_eval_grade(raw)
        if grade is not None:
            return grade
        print_fn("Enter y (success), n (failure), a score 0–1 (partial), or d (discard).")


class EvalClient:
    """Thin authenticated client for Dreamscale real-robot evaluation APIs."""

    def __init__(
        self,
        *,
        api_url: str,
        api_key: str,
        http_client: httpx.Client | None = None,
        timeout_s: float = 30.0,
    ) -> None:
        self.api_url = api_url.rstrip("/")
        self.api_key = api_key
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=timeout_s)

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def create_session(
        self,
        *,
        mode: str = "blind_ab",
        policy_ref: str | None = None,
        slot_a_deployment_id: str | None = None,
        slot_a_version: int | None = None,
        slot_b_deployment_id: str | None = None,
        slot_b_version: int | None = None,
        target_trials: int = 20,
        title: str = "",
        task: str = "",
        robot_id: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "mode": mode,
            "policy_ref": policy_ref,
            "slot_a_deployment_id": slot_a_deployment_id,
            "slot_a_version": slot_a_version,
            "slot_b_deployment_id": slot_b_deployment_id,
            "slot_b_version": slot_b_version,
            "target_trials": int(target_trials),
            "title": title,
            "task": task,
            "robot_id": robot_id,
        }
        resp = self._client.post(
            f"{self.api_url}/v1/evals/sessions",
            json={k: v for k, v in body.items() if v is not None},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()["session"]

    def list_sessions(
        self, *, policy_ref: str | None = None, status: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if policy_ref:
            params["policy_ref"] = policy_ref
        if status:
            params["status"] = status
        resp = self._client.get(
            f"{self.api_url}/v1/evals/sessions", params=params, headers=self._headers()
        )
        resp.raise_for_status()
        return resp.json().get("sessions") or []

    def get_session(self, session_id: str) -> dict[str, Any]:
        resp = self._client.get(
            f"{self.api_url}/v1/evals/sessions/{urllib.parse.quote(session_id)}",
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()["session"]

    def next_trial(self, session_id: str) -> dict[str, Any]:
        resp = self._client.get(
            f"{self.api_url}/v1/evals/sessions/{urllib.parse.quote(session_id)}/next",
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()

    def record_trial(
        self,
        session_id: str,
        *,
        trial_index: int,
        outcome: str,
        score: float | None = None,
        takeover_count: int = 0,
        autonomous_seconds: float = 0.0,
        takeover_seconds: float = 0.0,
        cycle_seconds: float | None = None,
        episode_id: str | None = None,
        usage_session_id: str | None = None,
        robot_id: str | None = None,
        task: str | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "trial_index": trial_index,
            "outcome": outcome,
            "score": score,
            "takeover_count": int(takeover_count),
            "autonomous_seconds": float(autonomous_seconds),
            "takeover_seconds": float(takeover_seconds),
            "cycle_seconds": cycle_seconds,
            "episode_id": episode_id,
            "usage_session_id": usage_session_id,
            "robot_id": robot_id,
            "task": task,
            "notes": notes,
        }
        resp = self._client.post(
            f"{self.api_url}/v1/evals/sessions/{urllib.parse.quote(session_id)}/trials",
            json={k: v for k, v in body.items() if v is not None},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()

    def reveal_session(self, session_id: str) -> dict[str, Any]:
        resp = self._client.post(
            f"{self.api_url}/v1/evals/sessions/{urllib.parse.quote(session_id)}/reveal",
            json={},
            headers=self._headers(),
        )
        resp.raise_for_status()
        return resp.json()["session"]

    def policy_scoreboard(self, policy_ref: str) -> dict[str, Any]:
        quoted = urllib.parse.quote(policy_ref, safe="/")
        resp = self._client.get(
            f"{self.api_url}/v1/policies/{quoted}/scoreboard", headers=self._headers()
        )
        resp.raise_for_status()
        return resp.json()


def format_eval_summary(session: dict[str, Any]) -> list[str]:
    """Render a crisp plain-text summary of a revealed eval session."""
    lines = [f"Eval {session['id']} — {session.get('title') or session['mode']}"]
    summary = session.get("summary")
    if not summary:
        lines.append(
            f"  Status: {session['status']} "
            f"({session['completed_trials']}/{session['target_trials']} trials; still blinded)"
        )
        return lines

    def _fmt_slot(label: str, slot: dict[str, Any]) -> str:
        ver = f"v{slot['version']}" if slot.get("version") is not None else slot["deployment_id"]
        sr = (
            f"{slot['success_rate'] * 100:.1f}% ({slot['successes']}/{slot['scored_trials']})"
            if slot.get("success_rate") is not None
            else "n/a"
        )
        tk = (
            f"{slot['mean_takeovers']:.2f}/ep"
            if slot.get("mean_takeovers") is not None
            else "n/a"
        )
        cyc = (
            f"{slot['mean_cycle_seconds']:.1f}s"
            if slot.get("mean_cycle_seconds") is not None
            else "n/a"
        )
        return f"  {label} ({ver}): success {sr} · takeovers {tk} · cycle {cyc}"

    lines.append(_fmt_slot("Slot A", summary["slot_a"]))
    if summary.get("slot_b"):
        lines.append(_fmt_slot("Slot B", summary["slot_b"]))
        p_txt = f" (p={summary['p_value']:.3f})" if summary.get("p_value") is not None else ""
        verdict_map = {
            "slot_b_wins": "Candidate (Slot B) wins",
            "slot_b_leads": "Candidate (Slot B) leads",
            "slot_a_wins": "Baseline (Slot A) wins",
            "slot_a_leads": "Baseline (Slot A) leads",
            "tie": "Tie",
            "inconclusive": "Inconclusive",
        }
        verdict = verdict_map.get(summary.get("verdict") or "", str(summary.get("verdict")))
        lines.append(f"  Verdict: {verdict}{p_txt}")
    return lines


def run_blind_eval(
    client: EvalClient,
    *,
    session_id: str,
    run_trial: Callable[[str, str, int, int], TrialExecution],
    grade_fn: Callable[[], EvalGrade] | None = None,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
    robot_id: str | None = None,
    reveal_on_finish: bool = True,
) -> dict[str, Any]:
    """Execute every remaining blinded trial in ``session_id`` without revealing A vs B."""
    grader = grade_fn or (lambda: prompt_eval_grade(input_fn=input_fn, print_fn=print_fn))
    while True:
        assignment = client.next_trial(session_id)
        if assignment.get("done"):
            break
        trial_idx = int(assignment["trial_index"])
        trial_num = int(assignment.get("trial_number") or (trial_idx + 1))
        total = int(assignment["target_trials"])
        deployment_id = str(assignment["deployment_id"])
        task = str(assignment.get("task") or "")

        # Never print deployment_id or slot while blinded!
        print_fn(f"\nTrial {trial_num}/{total} (blinded) — running policy…")
        execution = run_trial(deployment_id, task, trial_num, total)
        grade = grader()
        client.record_trial(
            session_id,
            trial_index=trial_idx,
            outcome=grade.outcome,
            score=grade.score,
            takeover_count=execution.takeover_count,
            autonomous_seconds=execution.autonomous_seconds,
            takeover_seconds=execution.takeover_seconds,
            cycle_seconds=execution.cycle_seconds,
            episode_id=execution.episode_id,
            usage_session_id=execution.usage_session_id,
            robot_id=robot_id,
            task=task,
            notes=grade.notes,
        )
        print_fn(f"Recorded trial {trial_num}/{total} ({grade.outcome}).")

    if reveal_on_finish:
        revealed = client.reveal_session(session_id)
        for line in format_eval_summary(revealed):
            print_fn(line)
        return revealed
    return client.get_session(session_id)
