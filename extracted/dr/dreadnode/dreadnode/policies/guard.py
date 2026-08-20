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
from dreadnode.policies.scope import Policy, ScopeConfig

if t.TYPE_CHECKING:
    from dreadnode.agents.engines.base import PermissionBridge, PolicyFacet


class GuardSessionPolicy(HeadlessSessionPolicy):
    """Headless mode + LLM-judged tool-call gating.

    The runtime auto-denies ``ask_user()`` (inherited
    ``is_autonomous=True``), enforces a per-turn step budget (inherited
    ``max_steps``), and runs every tool call past a
    :class:`ProcessJudge` for allow/deny.

    Scope can be configured two ways:

    - **Structured scope** via ``scope`` (full :class:`ScopeConfig`) or
      the ``preset`` shortcut (``recon_only``, ``standard_pentest``,
      ``red_team``). The scope model defines capability categories
      (reconnaissance, exploitation, credential access, etc.) and target
      boundaries (networks, domains, services, cloud resources, identities).
      The resolved scope is rendered to a natural-language rubric for the
      judge. Any additional ``rubric`` text is appended after the scope rubric.

    - **Freeform rubric** via ``rubric`` — a plain-text string or YAML path
      layered on top of the safety-floor default.

    The judge sees a slice of the live trajectory selected by
    ``transcript_strategy``. The default ``intent_plus_calls`` shows the
    user task plus the prior tool-call sequence (no responses).

    Transcript strategies:

    - ``rubric_only`` — no transcript, cheapest.
    - ``intent_only`` — system + user-authored messages only.
    - ``intent_plus_calls`` *(default)* — adds tool-call sequence, no results.
    - ``intent_plus_outputs_summary`` — adds LLM-summarized tool results.
    - ``full`` — entire trajectory including assistant prose.

    Example::

        # TUI — preset shortcut:
        # /policy guard judge_model=anthropic/claude-haiku-4-5 preset=standard_pentest

        # TUI — freeform rubric:
        # /policy guard judge_model=anthropic/claude-haiku-4-5 rubric="In-scope: api.example.com"

        # API — full scope config:
        POST /api/sessions/{id}/policy
        {
          "name": "guard",
          "judge_model": "anthropic/claude-haiku-4-5",
          "scope": {
            "preset": "standard_pentest",
            "boundaries": {
              "in_scope": [{"cidr": "10.0.1.0/24", "label": "DMZ"}],
              "out_of_scope": [{"host": "10.0.1.5", "label": "monitoring"}]
            },
            "capabilities": {
              "lateral_movement": {"policy": "deny"},
              "credential_access": {"password_spraying": "allow"}
            }
          }
        }
    """

    name: t.ClassVar[str] = "guard"
    display_label: t.ClassVar[str] = "guard"

    judge_model: str = Field(min_length=1, description="Model identifier for the process judge.")
    rubric: str | Path | None = Field(
        default=None,
        description=(
            "Optional user rubric layered on top of the safety-floor default "
            "(or appended after a scope-rendered rubric when ``scope`` or "
            "``preset`` is also set)."
        ),
    )
    scope: ScopeConfig | None = Field(
        default=None,
        description=(
            "Structured scope configuration with capability categories and "
            "target boundaries. Resolved and rendered to a rubric for the judge. "
            'Use ``preset`` as a shortcut for ``scope={"preset": "..."}``.'
        ),
    )
    preset: str | None = Field(
        default=None,
        description=(
            'Shortcut for ``scope={"preset": "..."}``. Sets a named baseline '
            "scope config (``recon_only``, ``standard_pentest``, ``red_team``). "
            "Ignored when ``scope`` is explicitly provided."
        ),
    )
    replace_default_rubric: bool = False
    cache: bool = Field(
        default=True,
        description=(
            "Prefix-cache the judge prompt. Set false to "
            "drop the cache_control markers; decisions are identical either way."
        ),
    )

    transcript_strategy: TranscriptStrategy = "intent_plus_calls"
    on_deny: OnDeny = "retry"
    on_judge_error: OnJudgeError = "deny"
    always_allow: tuple[str, ...] = ()
    always_deny: tuple[str, ...] = ()
    ask_behavior: t.Literal["prompt", "deny"] = Field(
        default="prompt",
        description=(
            "How judge ASK decisions resolve. ``prompt`` requests attended operator "
            "approval; ``deny`` fails closed without creating a pending prompt for "
            "headless/background/eval sessions."
        ),
    )

    _judge: ProcessJudge = PrivateAttr()
    _judge_hook: Hook = PrivateAttr()
    _effective_scope: ScopeConfig | None = PrivateAttr(default=None)
    _has_ask_capabilities: bool = PrivateAttr(default=False)
    _permission_ref: "t.Callable[[], PermissionBridge | None] | None" = PrivateAttr(default=None)

    @property
    def needs_permission_bridge(self) -> bool:
        """Guard needs the bridge when scope has ASK capabilities."""
        return self._has_ask_capabilities and self.ask_behavior == "prompt"

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

    def _build_effective_rubric(self) -> str | Path | None:
        """Build the effective rubric from scope config and/or freeform rubric.

        Resolution:
        - If ``scope`` is set, resolve and render it to a rubric string.
        - If ``preset`` is set (and ``scope`` is not), create a ScopeConfig from it.
        - If ``rubric`` is also set, append it after the scope rubric.
        - If neither scope nor rubric is set, return None (safety-floor default only).
        """
        scope_config = self.scope
        if scope_config is None and self.preset is not None:
            scope_config = ScopeConfig(preset=self.preset)

        if scope_config is not None:
            self._effective_scope = scope_config
            resolved = scope_config.resolve()
            self._has_ask_capabilities = any(
                Policy.ASK in subs.values() for subs in resolved.categories.values()
            )
            scope_rubric = resolved.render_rubric()

            if self.rubric is not None:
                # Append freeform rubric after scope-rendered rubric
                freeform = self.rubric if isinstance(self.rubric, str) else self.rubric.read_text()
                return f"{scope_rubric}\n\n## Additional Rules\n{freeform}"
            return scope_rubric

        return self.rubric

    def model_post_init(self, _ctx: t.Any) -> None:
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

        effective_rubric = self._build_effective_rubric()

        self._judge = ProcessJudge(
            model=resolved_judge_model,
            rubric=effective_rubric,
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
            permission=lambda: self._permission_ref() if self._permission_ref else None,
        )

    @property
    def hooks(self) -> list[Hook]:
        """Inherited step-budget hooks plus the judge gate."""
        return [*super().hooks, self._judge_hook]


__all__ = ["GuardSessionPolicy"]
