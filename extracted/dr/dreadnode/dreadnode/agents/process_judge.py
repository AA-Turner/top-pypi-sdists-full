"""ProcessJudge — LLM-backed gate over (intent, proposed tool call) pairs.

The primitive layer of the guard policy. ``ProcessJudge`` knows
nothing about ``Trajectory``, ``Hook``, or ``SessionPolicy`` — it takes
pre-shaped inputs (a list of :class:`Message` plus a :class:`ToolCall`)
and returns a :class:`ProcessDecision`. Hook code is responsible for the
trajectory-to-intent transformation.

Composition: reuses the lower-level :func:`dreadnode.scorers.judge.judge`
function so XML response parsing and the regex fallback stay in one
place. The default safety-floor rubric ships at
``dreadnode/policies/rubrics/process/default.yaml`` and is layered with
any user-supplied rubric under a ``## Project-specific scope`` header
unless ``replace_default_rubric=True``.
"""

import typing as t
from dataclasses import dataclass
from pathlib import Path

from dreadnode.generators.generator import GenerateParams, Generator, get_generator

if t.TYPE_CHECKING:
    from dreadnode.agents.tools import ToolCall
    from dreadnode.generators.message import Message


_DEFAULT_RUBRIC_PATH: Path = (
    Path(__file__).parent.parent / "policies" / "rubrics" / "process" / "default.yaml"
)

_USER_RUBRIC_HEADER = "## Project-specific scope"


@dataclass(slots=True)
class ProcessDecision:
    """Outcome of one :class:`ProcessJudge` invocation.

    Two-valued by design — the agent will run an allowed call or won't run
    a denied one. A "warn" mode is deliberately absent; the gating layer
    cannot usefully half-allow a tool call.
    """

    allow: bool
    reason: str


class ProcessJudge:
    """LLM-backed gate over (intent, proposed tool call) pairs.

    Example::

        from dreadnode.agents.process_judge import ProcessJudge

        judge = ProcessJudge(
            model="anthropic/claude-haiku-4-5",
            rubric="In-scope domains: api.example.com",
        )
        decision = await judge.evaluate(
            intent=session_messages,
            proposed_call=tool_call,
        )
        if not decision.allow:
            print("denied:", decision.reason)
    """

    def __init__(
        self,
        *,
        model: str | Generator,
        rubric: str | Path | None = None,
        replace_default_rubric: bool = False,
        model_params: dict[str, t.Any] | None = None,
        system_prompt: str | None = None,
        cache: bool = False,
    ) -> None:
        """
        Args:
            cache: Attach ``cache_control`` breakpoints to the judge prompt so
                repeated judgements over one growing session bill the stable
                head (instructions + rubric) and append-only transcript prefix
                at the cache-read rate. The prompt layout is the same either way
                — the rubric always lives in the system message (see
                :meth:`_build_messages`); this flag only toggles the markers, so
                enabling it never changes a decision. Only pays off when calls
                run in order within the cache TTL and the intent clears the
                model's minimum cacheable prefix; markers are harmless on
                providers that ignore them.
        """
        if rubric is None and replace_default_rubric:
            raise ValueError("replace_default_rubric=True requires a user-supplied rubric")

        from dreadnode.scorers.judge import _load_rubric_from_yaml

        default_text, default_system_prompt, _ = _load_rubric_from_yaml(
            _DEFAULT_RUBRIC_PATH, system_prompt=None, name="process_default"
        )

        if rubric is None:
            final_rubric = default_text
        else:
            user_text = self._resolve_user_rubric(rubric)
            final_rubric = (
                user_text
                if replace_default_rubric
                else f"{default_text}\n\n{_USER_RUBRIC_HEADER}\n{user_text}"
            )

        self._model = model
        self._rubric = final_rubric
        self._system_prompt = system_prompt or default_system_prompt
        self._model_params = model_params
        self._cache = cache

    @property
    def model(self) -> str | Generator:
        return self._model

    @property
    def rubric(self) -> str:
        return self._rubric

    @property
    def system_prompt(self) -> str | None:
        return self._system_prompt

    @property
    def cache(self) -> bool:
        return self._cache

    async def evaluate(
        self,
        *,
        intent: "list[Message]",
        proposed_call: "ToolCall",
        context: dict[str, t.Any] | None = None,
    ) -> ProcessDecision:
        """Evaluate a proposed tool call against the rubric.

        Args:
            intent: Trajectory-stripped messages representing the user's
                intent (typically system + user-authored, optionally tool
                outputs depending on the hook's strategy).
            proposed_call: The tool call about to execute. Wire name and
                arguments are passed verbatim — argument redaction is a
                separate concern.
            context: Optional per-call context (task instruction, scope
                metadata) merged into the rendered intent.

        Returns:
            A :class:`ProcessDecision` with ``allow`` and a short reason.
        """
        from dreadnode.scorers.judge import parse_judgement

        proposed_call_text = self._render_proposed_call(proposed_call)
        generator = self._resolve_generator()

        messages = self._build_messages(intent, proposed_call_text, context=context)
        results = await generator.generate_messages([messages], [generator.params])
        result = results[0]
        if isinstance(result, BaseException):
            raise result

        judgement = parse_judgement(result.message.content or "")
        return ProcessDecision(allow=judgement.passing, reason=judgement.reason)

    def _build_messages(
        self,
        intent: "list[Message]",
        proposed_call_text: str,
        context: dict[str, t.Any] | None = None,
    ) -> "list[Message]":
        r"""Build the judge prompt: rubric in the system message, transcript and
        proposed call in the user role.

        The rubric is operator policy, so it lives in the high-authority system
        channel — above the (potentially attacker-influenced) transcript, not
        interleaved with it. This layout is used whether or not caching is
        enabled; ``cache`` only controls whether ``cache_control`` breakpoints
        are attached, so the two paths emit byte-identical prompts and decide
        identically.

        Layout (breakpoints attached only when ``self._cache``)::

            system  (breakpoint): {instructions}\n\n<rubric>…</rubric>  ← stable
            user    (uncached):   "<input>\n# Intent transcript"         ← stable opener
            user    (uncached):   {str(intent[0])}
            …
            user    (breakpoint): {str(intent[-1])}                      ← rolling frontier
            user    (uncached):   "\n</input>\n<output>{call}</output>"  ← tiny, volatile

        The transcript is split into one block per intent message because
        Anthropic cache reads are block-aligned. If the whole transcript lives
        in one growing block, every call writes a new block and never reads the
        previous one. With append-only per-message blocks, earlier messages stay
        byte-identical across calls and the rolling breakpoint moves to the new
        last transcript message. The closing ``</input>`` tag is deliberately
        pushed into the uncached suffix so the last cached transcript block ends
        on raw message content and can be reused by the next call.

        Each block is a separate single-part message so the prefix bytes are
        exactly the block text — no inter-part newline rewriting (which only
        fires between text parts *within* one message) and no ``content_as_str``
        collapse of a cache-marked block (that only triggers on a part with no
        ``cache_control``).
        """
        from dreadnode.generators.message import Message

        marker: t.Literal["ephemeral"] | None = "ephemeral" if self._cache else None
        system_text = f"{self._system_prompt}\n\n<rubric>\n{self._rubric}\n</rubric>"

        header_lines = ["<input>"]
        if context:
            header_lines.append("# Task context")
            for key, value in context.items():
                header_lines.append(f"- {key}: {value}")
            header_lines.append("")
        header_lines.append("# Intent transcript")

        messages = [
            Message(role="system", content=system_text, cache_control=marker),
            Message(role="user", content="\n".join(header_lines)),
        ]
        for i, msg in enumerate(intent):
            messages.append(
                Message(
                    role="user",
                    content=str(msg),
                    cache_control=marker if i == len(intent) - 1 else None,
                )
            )
        messages.append(
            Message(role="user", content=f"\n</input>\n<output>{proposed_call_text}</output>")
        )
        return messages

    def _resolve_generator(self) -> Generator:
        if isinstance(self._model, Generator):
            return self._model
        if not isinstance(self._model, str):
            raise TypeError("model must be a string identifier or a Generator instance.")
        params: GenerateParams | None
        if self._model_params is None:
            params = None
        elif isinstance(self._model_params, GenerateParams):
            params = self._model_params
        else:
            params = GenerateParams.model_validate(self._model_params)
        return get_generator(self._model, params=params)

    @staticmethod
    def _resolve_user_rubric(rubric: str | Path) -> str:
        """Resolve a user rubric to its body text.

        Path or YAML-shaped string → load the YAML and read its ``rubric``
        field. Anything else → treat as a plain string and return as-is.
        """
        from dreadnode.scorers.judge import _is_yaml_rubric, _load_rubric_from_yaml

        if isinstance(rubric, Path) or _is_yaml_rubric(rubric):
            text, _, _ = _load_rubric_from_yaml(rubric, system_prompt=None, name="user")
            return text
        return rubric

    @staticmethod
    def _render_intent(
        intent: "list[Message]",
        *,
        context: dict[str, t.Any] | None = None,
    ) -> str:
        """Render intent messages as a transcript the judge can consume.

        Delegates per-message formatting to ``Message.__str__`` so assistant
        ``tool_calls`` and tool-result ``tool_call_id`` headers actually
        appear in the rendered output — without this, ``intent_plus_calls``
        and ``full`` would silently drop the tool-call sequence the judge
        is supposed to be reasoning about.
        """
        lines: list[str] = []
        if context:
            lines.append("# Task context")
            for key, value in context.items():
                lines.append(f"- {key}: {value}")
            lines.append("")
        if intent:
            lines.append("# Intent transcript")
            for msg in intent:
                lines.append(str(msg))
        return "\n".join(lines)

    @staticmethod
    def _render_proposed_call(proposed_call: "ToolCall") -> str:
        """Render the proposed tool call in a structured XML block."""
        return (
            f"<tool>{proposed_call.name}</tool>\n"
            f"<arguments>{proposed_call.function.arguments}</arguments>"
        )


__all__ = ["ProcessDecision", "ProcessJudge"]
