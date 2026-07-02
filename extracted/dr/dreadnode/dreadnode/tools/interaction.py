"""
User interaction tools for agents.

These tools allow agents to ask for clarification, present options,
and get user input during execution.
"""

import asyncio
import typing as t
from contextvars import ContextVar, Token
from uuid import uuid4

from loguru import logger

from dreadnode.agents.tools import Toolset, tool, tool_method
from dreadnode.app.api.models import (
    HumanInputResponse,
    HumanPrompt,
    HumanPromptOption,
    HumanQuestion,
    QuestionAnswer,
)
from dreadnode.core.meta import Config


class UserCancelled(Exception):  # noqa: N818
    """Raised inside ``ask_user`` when the user cancels the prompt.

    The ``@tool`` decorator catches it and surfaces it to the LLM as a
    structured tool error. Distinct from ``CancelledError`` (which
    signals turn-abort and must propagate untouched through the asyncio
    cancellation machinery).
    """


# Context variable for user input callback
# This allows the CLI to inject its input handler
_user_input_callback: ContextVar[t.Callable[[str, list[str] | None], t.Awaitable[str]] | None] = (
    ContextVar("user_input_callback", default=None)
)

HumanPromptHandler = t.Callable[[HumanPrompt], t.Awaitable[HumanInputResponse]]
_human_prompt_handler: ContextVar[HumanPromptHandler | None] = ContextVar(
    "human_prompt_handler",
    default=None,
)


def set_user_input_callback(
    callback: t.Callable[[str, list[str] | None], t.Awaitable[str]],
) -> None:
    """
    Set the callback for getting user input.

    The callback receives:
    - question: The question to ask
    - options: Optional list of choices (None for free-form input)

    Returns the user's response string.
    """
    _user_input_callback.set(callback)


def set_human_prompt_handler(handler: HumanPromptHandler) -> Token[HumanPromptHandler | None]:
    """Set the handler for structured human prompts."""
    return _human_prompt_handler.set(handler)


def reset_human_prompt_handler(token: Token[HumanPromptHandler | None]) -> None:
    """Reset the structured human prompt handler."""
    _human_prompt_handler.reset(token)


def get_user_input_callback() -> t.Callable[[str, list[str] | None], t.Awaitable[str]] | None:
    """Get the current user input callback."""
    return _user_input_callback.get()


def get_human_prompt_handler() -> HumanPromptHandler | None:
    """Get the structured human prompt handler."""
    return _human_prompt_handler.get()


_APPROVE_LABEL = "Allow"
_DENY_LABEL = "Deny"


class RuntimePermissionBridge:
    """Bridges a foreign engine's tool-approval callback into the HITL path.

    Implements the ``PermissionBridge`` protocol (see
    ``dreadnode.agents.engines.base``). A foreign engine (e.g. ``claude-code``)
    calls :meth:`request_tool_approval`; we build a ``HumanPrompt`` and route it
    through the *same* per-turn human-prompt handler ``ask_user`` uses, so the
    existing ``prompt.required`` / ``prompt.respond`` UX is preserved — including
    autonomous-policy auto-deny (the handler resolves ``cancel`` instantly) and
    the eval-worker path (CAP-EGOV-007).
    """

    async def request_tool_approval(self, *, tool_name: str, tool_input: dict[str, t.Any]) -> bool:
        handler = get_human_prompt_handler()
        if handler is None:
            # No HITL context registered (e.g. bare-SDK use outside a turn).
            # Fail open — the engine only attaches this bridge inside a runtime
            # turn, where a handler is always set; autonomous denial is handled
            # by the handler itself returning ``cancel``.
            logger.debug("Tool approval requested for '{}' with no handler; allowing", tool_name)
            return True

        summary = ", ".join(f"{k}={v!r}" for k, v in list(tool_input.items())[:4])
        prompt = HumanPrompt(
            request_id=str(uuid4()),
            questions=[
                HumanQuestion(
                    kind="choice",
                    prompt=f"Allow tool '{tool_name}'? ({summary})"
                    if summary
                    else f"Allow tool '{tool_name}'?",
                    header="Tool approval",
                    options=[
                        HumanPromptOption(label=_APPROVE_LABEL),
                        HumanPromptOption(label=_DENY_LABEL),
                    ],
                    custom=False,
                )
            ],
        )
        response = await handler(prompt)
        if response.action == "cancel" or not response.answers:
            return False
        answer = response.answers[0]
        selected = list(answer.selected_labels)
        if answer.text:
            selected.append(answer.text)
        return any(label.lower() == _APPROVE_LABEL.lower() for label in selected)


async def _default_input(question: str, options: list[str] | None = None) -> str:
    """Default input handler using stdin (blocking)."""

    if options:
        prompt_lines = [f"  {i}. {opt}" for i, opt in enumerate(options, 1)]
        prompt_lines.append(f"  {len(options) + 1}. Other (free text)")
        prompt_text = f"{question}\n" + "\n".join(prompt_lines) + "\nYour choice (number or text): "

        # Run blocking input in thread
        response = await asyncio.to_thread(input, prompt_text)

        # Parse response
        try:
            idx = int(response.strip()) - 1
            if 0 <= idx < len(options):
                return options[idx]
            if idx == len(options):
                return await asyncio.to_thread(input, "Enter your response: ")
        except ValueError:
            pass

        return response.strip()
    return await asyncio.to_thread(input, f"{question}\n> ")


def _coerce_options(
    options: list[str] | list[HumanPromptOption] | None,
) -> list[HumanPromptOption]:
    if not options:
        return []
    return [
        opt if isinstance(opt, HumanPromptOption) else HumanPromptOption(label=str(opt))
        for opt in options
    ]


def _summarize_answer(question: HumanQuestion, answer: QuestionAnswer) -> str:
    """Render a single answer as an LLM-friendly string."""
    if answer.was_custom and (answer.custom_text or answer.text):
        return (answer.custom_text or answer.text or "").strip()
    if question.kind == "input":
        return (answer.text or "").strip()
    if answer.selected_labels:
        return ", ".join(answer.selected_labels)
    return ""


def _summarize_response(prompt: HumanPrompt, response: HumanInputResponse) -> str:
    """Render a submitted response as the tool's return string."""
    answers = response.answers or []
    if len(prompt.questions) == 1:
        if not answers:
            return ""
        return _summarize_answer(prompt.questions[0], answers[0])
    parts: list[str] = []
    for question, answer in zip(prompt.questions, answers, strict=False):
        header = question.header or question.prompt
        parts.append(f"{header}: {_summarize_answer(question, answer)}")
    return "\n".join(parts)


@tool
async def ask_user(
    question: t.Annotated[
        str | None,
        "The question to ask the user (single-question shorthand).",
    ] = None,
    options: t.Annotated[
        list[str] | list[HumanPromptOption] | None,
        "Optional list of choices for the single-question shorthand.",
    ] = None,
    *,
    questions: t.Annotated[
        list[HumanQuestion] | None,
        "Bundle of questions. Mutually exclusive with the ``question`` shorthand.",
    ] = None,
    request_id: t.Annotated[str | None, "Optional request id override."] = None,
) -> str:
    """
    Ask the user one or more questions and wait for their response.

    Use this tool when you need:
    - Clarification on ambiguous requirements
    - User preference between options
    - Confirmation before destructive actions
    - Additional information to proceed

    ## Best Practices
    - Ask specific, clear questions
    - Provide options when choices are limited
    - Don't ask unnecessary questions (use your judgment first)
    - Explain why you're asking if it's not obvious

    ## Examples

    Free-form question:
    ```
    ask_user("What authentication method should I use?")
    ```

    Multiple choice:
    ```
    ask_user(
        "Which database should I configure?",
        options=["PostgreSQL", "MySQL", "SQLite"],
    )
    ```

    Multi-question bundle:
    ```
    ask_user(questions=[
        HumanQuestion(kind="choice", prompt="Framework?",
                      options=[HumanPromptOption(label="React"),
                               HumanPromptOption(label="Vue")]),
        HumanQuestion(kind="input", prompt="App name?"),
    ])
    ```

    Returns:
        Selected label / typed text for a single question, or a
        newline-joined ``Header: answer`` block for bundles.

    Raises:
        UserCancelled: when the user cancels the prompt or runs in
            headless mode (where no human is available).
    """
    if questions is not None and (question is not None or options is not None):
        raise ValueError(
            "ask_user: pass either ``question``/``options`` or ``questions``, not both"
        )

    if questions is not None:
        bundle = list(questions)
    elif question is not None:
        opts = _coerce_options(options)
        kind: t.Literal["choice", "input"] = "choice" if opts else "input"
        bundle = [HumanQuestion(kind=kind, prompt=question, options=opts)]
    else:
        raise ValueError("ask_user: must provide either ``question`` or ``questions``")

    prompt = HumanPrompt(
        request_id=request_id or f"req-{uuid4().hex}",
        questions=bundle,
    )

    prompt_handler = get_human_prompt_handler()
    if prompt_handler is not None:
        first_prompt = bundle[0].prompt
        logger.info("Asking user (structured): {}", first_prompt)
        response = await prompt_handler(prompt)
        if response.action == "cancel":
            raise UserCancelled("user cancelled prompt")
        return _summarize_response(prompt, response)

    # Stdin fallback — single-question only.
    if len(bundle) > 1:
        raise RuntimeError(
            "ask_user bundles require a structured prompt handler; "
            "the stdin fallback only supports single-question prompts",
        )

    callback = get_user_input_callback()
    if callback is None:
        logger.warning("No user input callback set, using default stdin handler")
        callback = _default_input

    legacy_question = bundle[0]
    legacy_options = [opt.label for opt in legacy_question.options] or None
    logger.info("Asking user: {}", legacy_question.prompt)
    response_text = await callback(legacy_question.prompt, legacy_options)
    logger.info("User responded: {}", response_text)
    return response_text


@tool
async def confirm(
    action: t.Annotated[str, "Description of the action to confirm"],
    *,
    default_yes: t.Annotated[bool, "Whether to default to yes if the answer is unclear"] = False,
) -> bool:
    """
    Ask user to confirm an action.

    Returns True if confirmed, False if rejected. Cancel (Esc, or
    headless auto-cancel) is treated as the safe default and returns
    ``default_yes``.

    Args:
        action: What you're asking to confirm.
        default_yes: Value returned when the user cancels or gives an
            ambiguous response.

    Returns:
        True if user confirms, False otherwise.
    """
    try:
        response = await ask_user(f"Confirm: {action}", options=["Yes", "No"])
    except UserCancelled:
        return default_yes
    response_lower = response.lower().strip()
    if response_lower in ("yes", "y", "1", "confirm", "ok", "sure"):
        return True
    if response_lower in ("no", "n", "2", "cancel", "abort"):
        return False
    return default_yes


class InteractionToolset(Toolset):
    """
    Toolset for user interaction with configurable callback.

    Use this when you need to inject a custom input handler.
    """

    input_callback: t.Callable[[str, list[str] | None], t.Awaitable[str]] | None = Config(
        default=None
    )
    """Custom callback for getting user input."""

    async def _get_input(self, question: str, options: list[str] | None = None) -> str:
        """Get input using configured callback or default."""
        if self.input_callback:
            return await self.input_callback(question, options)

        if get_human_prompt_handler() is not None:
            return await ask_user(question, options=options)

        callback = get_user_input_callback()
        if callback:
            return await callback(question, options)

        return await _default_input(question, options)

    @tool_method
    async def ask(
        self,
        question: t.Annotated[str, "Question to ask"],
        options: t.Annotated[list[str] | None, "Optional choices"] = None,
    ) -> str:
        """Ask user a question."""
        logger.info(f"Asking: {question}")
        response = await self._get_input(question, options)
        logger.info(f"Response: {response}")
        return response

    @tool_method
    async def confirm_action(
        self,
        action: t.Annotated[str, "Action to confirm"],
    ) -> bool:
        """Ask user to confirm an action."""
        response = await self._get_input(f"Confirm: {action}", options=["Yes", "No"])
        return response.lower().strip() in ("yes", "y", "1")
