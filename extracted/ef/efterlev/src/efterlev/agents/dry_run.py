"""Dry-run session machinery for `efterlev agent {gap, document, remediate} --dry-run`.

When a CLI agent command is invoked with `--dry-run`, the CLI enters a
`DryRunSession` context. Inside that context:

  * `Agent._invoke_llm` checks `active_dry_run_session.get()` and, if set,
    captures the assembled API request envelope into the session and
    returns a structurally-valid stub `output_model` instance instead of
    calling the LLM. The agent's main loop continues to the next
    iteration (next KSI for the documentation agent, etc.) capturing the
    next prompt, until the agent's `run()` returns normally.
  * `ProvenanceStore.write_record` checks the same context var and
    returns a stub `ProvenanceRecord` without touching the SQLite store,
    the blob disk store, or `receipts.log`. Dry-run runs leave zero
    side effects on the workspace's `.efterlev/` directory.

After `agent.run()` returns, the CLI serializes the session's full
`prompts` list as a JSON array of literal Anthropic API request envelopes
(augmented with `_efterlev` metadata: per-prompt iteration index, label,
token estimate, dollar cost estimate). One file or stdout, one JSON
document, every prompt the agent would have sent.

See DECISIONS 2026-05-06 "Tier 1 #2b design: --dry-run / --dump-prompt
on agent commands" for the rationale and alternatives considered.
"""

from __future__ import annotations

from contextlib import AbstractContextManager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any

from efterlev.llm.pricing import estimate_cost_usd
from efterlev.llm.pricing import lookup as lookup_pricing


@dataclass
class CapturedPrompt:
    """One LLM call that would have been made, captured before the network round-trip.

    The first three fields (`model`, `system`, `messages`, `max_tokens`)
    form a literal Anthropic API request envelope — copy this out of the
    JSON dump and pass it to `anthropic.messages.create(**dumped)` to
    reproduce the exact call. The `efterlev_metadata` dict is appended
    under the `_efterlev` key in the serialized JSON; clearly namespaced,
    easy for a downstream API-client to ignore.
    """

    model: str
    system: str
    messages: list[dict[str, Any]]
    max_tokens: int
    label: str  # e.g. "gap_agent.classify_all_ksis", "documentation_agent.KSI-CNA-DFP"
    iteration: int  # 1-indexed; first prompt of the run is iteration=1

    def to_json_envelope(self) -> dict[str, Any]:
        """Return the literal Anthropic API request shape + an `_efterlev` metadata
        sub-object holding our per-prompt extras (iteration, label, token + cost
        estimates)."""
        # Token estimate: local 4-chars-per-token approximation. Coarse but
        # honest; the `_efterlev.token_estimate_method` field flags the
        # precision so an auditor knows what they're looking at. A
        # vendored Anthropic tokenizer is the v0.2 follow-up if a real
        # user complains the estimate is off by >20%.
        input_chars = len(self.system) + sum(len(str(m.get("content", ""))) for m in self.messages)
        token_estimate = max(1, input_chars // 4)
        # Cost-side estimate: input tokens + max-output tokens (worst case).
        # Real runs almost always undershoot max_tokens on output, so this
        # is an upper bound on the per-prompt cost.
        cost_est = estimate_cost_usd(self.model, token_estimate, self.max_tokens)
        cost_field: float | None = round(cost_est, 4) if cost_est is not None else None
        priced = lookup_pricing(self.model)
        cost_method = "anthropic-published as_of " + (priced.as_of if priced else "n/a")
        return {
            "model": self.model,
            "system": self.system,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "_efterlev": {
                "iteration": self.iteration,
                "label": self.label,
                "token_estimate": token_estimate,
                "token_estimate_method": "approximate (4 chars/token)",
                "cost_estimate_usd": cost_field,
                "cost_estimate_method": cost_method,
            },
        }


@dataclass
class DryRunSession:
    """Per-CLI-invocation collector for dry-run prompts + a flag for `write_record`.

    Created by the CLI when `--dry-run` is passed; installed as the
    active context-var for the duration of `agent.run()`. Every captured
    prompt appends to `prompts`; the CLI serializes after `run()` returns.
    """

    prompts: list[CapturedPrompt] = field(default_factory=list)

    def capture(
        self,
        *,
        model: str,
        system: str,
        messages: list[dict[str, Any]],
        max_tokens: int,
        label: str,
    ) -> None:
        """Append one captured prompt to the session. Iteration is the
        1-indexed position in the captured list."""
        self.prompts.append(
            CapturedPrompt(
                model=model,
                system=system,
                messages=messages,
                max_tokens=max_tokens,
                label=label,
                iteration=len(self.prompts) + 1,
            )
        )

    def to_json_array(self) -> list[dict[str, Any]]:
        """Serialize all captured prompts to a list of envelope dicts."""
        return [p.to_json_envelope() for p in self.prompts]

    @property
    def total_token_estimate(self) -> int:
        """Sum of per-prompt token estimates across the session."""
        total = 0
        for p in self.prompts:
            input_chars = len(p.system) + sum(len(str(m.get("content", ""))) for m in p.messages)
            total += max(1, input_chars // 4)
        return total

    @property
    def total_cost_estimate_usd(self) -> float:
        """Sum of per-prompt cost estimates across the session. 0.0 when
        no model in the session is registered in the pricing table."""
        total = 0.0
        for p in self.prompts:
            input_chars = len(p.system) + sum(len(str(m.get("content", ""))) for m in p.messages)
            tokens = max(1, input_chars // 4)
            cost = estimate_cost_usd(p.model, tokens, p.max_tokens)
            if cost is not None:
                total += cost
        return total


# Context var the CLI sets to enter dry-run mode. None when not active.
# Agent._invoke_llm and ProvenanceStore.write_record both check this.
active_dry_run_session: ContextVar[DryRunSession | None] = ContextVar(
    "active_dry_run_session", default=None
)


def get_active_dry_run_session() -> DryRunSession | None:
    """Return the active session if any, else None. Used by callers
    that need to short-circuit (Agent._invoke_llm, ProvenanceStore.write_record)."""
    return active_dry_run_session.get()


class active_dry_run(AbstractContextManager[DryRunSession]):  # noqa: N801 -- snake_case context manager, matches active_store / active_redaction_ledger naming convention
    """Context manager that installs `session` as the active dry-run sink.

    Mirrors the `active_store` / `active_redaction_ledger` pattern from
    elsewhere in the codebase: enter to set the context var, exit to
    restore. Used by the CLI's agent commands when `--dry-run` /
    `--dump-prompt` is passed.
    """

    def __init__(self, session: DryRunSession) -> None:
        self._session = session
        self._token: object | None = None

    def __enter__(self) -> DryRunSession:
        self._token = active_dry_run_session.set(self._session)
        return self._session

    def __exit__(self, *exc_info: object) -> None:
        if self._token is not None:
            active_dry_run_session.reset(self._token)  # type: ignore[arg-type]
            self._token = None
