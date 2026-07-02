"""Guard session policy — headless mode plus LLM-judged tool gating.

Subclasses :class:`HeadlessSessionPolicy` so the inherited
``is_autonomous=True``, ``max_steps`` budget, and per-turn step counter
all carry over via MRO. Adds a ``ToolStart`` gate backed by a
:class:`ProcessJudge` that consults an LLM before each tool call.

Composition: holds the judge in a private attribute, builds the
gating hook via :func:`process_judge_hook`, and merges it with the
parent's hooks in the :meth:`hooks` property override. The hook
closure captures messages from ``GenerationStart`` and gates on
``ToolStart``; the policy itself stays declarative.
"""

import typing as t
from pathlib import Path

from pydantic import Field, PrivateAttr, model_validator

from dreadnode.agents.hooks import (
    OnDeny,
    OnJudgeError,
    TranscriptStrategy,
    process_judge_hook,
)
from dreadnode.agents.process_judge import ProcessJudge
from dreadnode.core.hook import Hook
from dreadnode.policies import HeadlessSessionPolicy

if t.TYPE_CHECKING:
    from dreadnode.agents.engines.base import PolicyFacet


class GuardSessionPolicy(HeadlessSessionPolicy):
    """Headless mode + LLM-judged tool-call gating.

    The runtime auto-denies ``ask_user()`` (inherited
    ``is_autonomous=True``), enforces a per-turn step budget (inherited
    ``max_steps``), and runs every tool call past a
    :class:`ProcessJudge` for allow/deny.

    The judge sees a slice of the live trajectory selected by
    ``transcript_strategy``. The default ``intent_plus_calls`` shows the
    user task plus the prior tool-call sequence (no responses) — the same
    cut Anthropic's auto-mode uses for its own per-call gating. The other
    options trade prompt size and injection surface against how much
    context the judge has to reason with:

    - ``rubric_only`` — no transcript. Judge sees only the proposed call
      against the rubric. Cheapest, lowest signal.
    - ``intent_only`` — system + user-authored messages. The original
      smallest cut, useful when the rubric encodes everything you care
      about and you don't want intermediate state to drift the judge.
    - ``intent_plus_calls`` *(default)* — adds the assistant tool-call
      sequence with any prose stripped from each call (no tool result
      content, no model justification text). The judge sees what the
      agent has been calling, not the words it used to justify those
      calls.
    - ``intent_plus_outputs_summary`` — ``intent_plus_calls`` plus tool
      results whose content has been replaced with a short LLM summary
      produced by the judge model. Assistant prose is stripped the same
      way; the judge sees calls + summarized results, no model-authored
      narrative. Caches per-``tool_call_id`` so each result is summarized
      at most once per session. Costs an extra summary call per unique
      tool result, billed via the judge model.
    - ``full`` — the entire trajectory, including assistant prose. The
      only strategy that surfaces the model's justification text to the
      judge. Maximum context, maximum surface.

    The captured intent is also trimmed to fit the judge model's context
    window: the system message and the original user task always survive,
    older tool-call/result messages drop first when the rendered transcript
    would exceed the budget. The trim emits a ``process_judge.intent_trimmed``
    metric with ``dropped_messages`` and ``strategy`` attributes.

    The judge prompt is prefix-cached by default (``cache=true``). The rubric
    and instructions sit in the system message, and the transcript is emitted as
    append-only per-message blocks with a rolling breakpoint on the latest
    transcript block. Each judgement within a session can read the prior call's
    transcript prefix at the cache-read rate (~0.1x) instead of full price. The
    prompt layout is identical with caching off — ``cache`` only toggles the
    ``cache_control`` markers, so decisions never change. Set ``cache=false`` to
    disable it (e.g. on a judge model or provider without prompt caching).

    Example::

        # Mid-session swap from the TUI:
        # /policy guard judge_model=anthropic/claude-haiku-4-5
        # /policy guard judge_model=anthropic/claude-haiku-4-5 transcript_strategy=full

        # Or from the API:
        POST /api/sessions/{id}/policy
        {
          "name": "guard",
          "judge_model": "anthropic/claude-haiku-4-5",
          "rubric": "In-scope: api.example.com only",
          "transcript_strategy": "intent_plus_calls",
          "cache": true,
          "max_steps": 20
        }
    """

    name: t.ClassVar[str] = "guard"
    display_label: t.ClassVar[str] = "guard"

    judge_model: str = Field(min_length=1, description="Model identifier for the process judge.")
    rubric: str | Path | None = Field(
        default=None,
        description=(
            "Optional user rubric layered on top of the safety-floor default "
            "unless ``replace_default_rubric`` is true."
        ),
    )
    replace_default_rubric: bool = False
    cache: bool = Field(
        default=True,
        description=(
            "Prefix-cache the judge prompt. The guard judges one call at a time, "
            "in order, within a live session, so each judgement can read the "
            "prior call's transcript prefix at the cache-read rate. Set false to "
            "drop the cache_control markers; decisions are identical either way."
        ),
    )

    transcript_strategy: TranscriptStrategy = "intent_plus_calls"
    on_deny: OnDeny = "retry"
    on_judge_error: OnJudgeError = "deny"
    always_allow: tuple[str, ...] = ()
    always_deny: tuple[str, ...] = ()

    _judge: ProcessJudge = PrivateAttr()
    _judge_hook: Hook = PrivateAttr()

    def required_facets(self) -> "set[PolicyFacet]":
        # The guard judge gates/steers every tool call mid-loop (GUARD_STEERING)
        # and can deny tools (TOOL_APPROVAL) even though the session is autonomous.
        from dreadnode.agents.engines.base import PolicyFacet

        return super().required_facets() | {
            PolicyFacet.GUARD_STEERING,
            PolicyFacet.TOOL_APPROVAL,
        }

    @model_validator(mode="after")
    def _check_short_circuit_lists(self) -> "GuardSessionPolicy":
        overlap = set(self.always_allow) & set(self.always_deny)
        if overlap:
            raise ValueError(f"always_allow and always_deny share entries: {sorted(overlap)}")
        return self

    def model_post_init(self, _ctx: t.Any) -> None:
        # Route the judge through the same model-resolution layer the agent
        # uses for its turn generator. ``dn/<provider>/<name>`` resolves to
        # the platform's LiteLLM proxy (DREADNODE_LLM_BASE / DREADNODE_LLM_API_KEY
        # or local LITELLM_PUBLIC_URL / LITELLM_MASTER_KEY fallbacks). Direct
        # provider strings pass through as-is so the user's own provider
        # API key is honored. The intent: judge billing semantics match the
        # agent's — pay-via-platform if you picked a dn/ model, pay your
        # provider directly if you picked an explicit one.
        from dreadnode.app.server.model_resolution import (
            build_turn_generator,
            resolve_turn_model_config,
        )

        judge_model_config = resolve_turn_model_config(
            requested_model=self.judge_model,
            remembered_model=None,
            agent_def=None,
        )
        resolved_judge_model = build_turn_generator(judge_model_config)

        self._judge = ProcessJudge(
            model=resolved_judge_model,
            rubric=self.rubric,
            replace_default_rubric=self.replace_default_rubric,
            cache=self.cache,
        )
        self._judge_hook = process_judge_hook(
            self._judge,
            transcript_strategy=self.transcript_strategy,
            on_deny=self.on_deny,
            on_judge_error=self.on_judge_error,
            always_allow=self.always_allow,
            always_deny=self.always_deny,
        )

    @property
    def hooks(self) -> list[Hook]:
        """Inherited step-budget hooks plus the judge gate."""
        return [*super().hooks, self._judge_hook]


__all__ = ["GuardSessionPolicy"]
