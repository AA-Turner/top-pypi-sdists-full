import enum

import click
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, ToolOutput
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    SystemPromptPart,
    TextPart,
    ToolReturnPart,
    UserPromptPart,
)

from tinybird.tb.modules.agent.utils import TinybirdAgentContext
from tinybird.tb.modules.feedback_manager import FeedbackManager

SYSTEM_PROMPT = """
Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions.
This summary should be thorough in capturing technical details, code patterns, and architectural decisions that would be essential for continuing development work without losing context.

Before providing your final summary, wrap your analysis in <analysis> tags to organize your thoughts and ensure you've covered all necessary points. In your analysis process:

1. Chronologically analyze each message and section of the conversation. For each section thoroughly identify:
   - The user's explicit requests and intents
   - Your approach to addressing the user's requests
   - Key decisions, technical concepts and code patterns
   - Specific details like file names, full code snippets, function signatures, file edits, etc
2. Double-check for technical accuracy and completeness, addressing each required element thoroughly.

Your summary should include the following sections:

1. Primary Request and Intent: Capture all of the user's explicit requests and intents in detail
2. Key Technical Concepts: List all important technical concepts, technologies, and frameworks discussed.
3. Files and Code Sections: Enumerate specific files and code sections examined, modified, or created. Pay special attention to the most recent messages and include full code snippets where applicable and include a summary of why this file read or edit is important.
4. Problem Solving: Document problems solved and any ongoing troubleshooting efforts.
5. Pending Tasks: Outline any pending tasks that you have explicitly been asked to work on.
6. Current Work: Describe in detail precisely what was being worked on immediately before this summary request, paying special attention to the most recent messages from both user and assistant. Include file names and code snippets where applicable.
7. Optional Next Step: List the next step that you will take that is related to the most recent work you were doing. IMPORTANT: ensure that this step is DIRECTLY in line with the user's explicit requests, and the task you were working on immediately before this summary request. If your last task was concluded, then only list next steps if they are explicitly in line with the users request. Do not start on tangential requests without confirming with the user first.
8. If there is a next step, include direct quotes from the most recent conversation showing exactly what task you were working on and where you left off. This should be verbatim to ensure there's no drift in task interpretation.

Here's an example of how your output should be structured:

<example>
<condense>
<analysis>
[Your thought process, ensuring all points are covered thoroughly and accurately]
</analysis>

<context>
1. Primary Request and Intent:
   [Detailed description]

2. Key Technical Concepts:
   - [Concept 1]
   - [Concept 2]
   - [...]

3. Files and Code Sections:
   - [File Name 1]
      - [Summary of why this file is important]
      - [Summary of the changes made to this file, if any]
      - [Important Code Snippet]
   - [File Name 2]
      - [Important Code Snippet]
   - [...]

4. Problem Solving:
   [Description of solved problems and ongoing troubleshooting]

5. Pending Tasks:
   - [Task 1]
   - [Task 2]
   - [...]

6. Current Work:
   [Precise description of current work]

7. Next Step:
   [Next st

</context>
</condense>
</example>

Please provide your summary based on the conversation so far, following this structure and ensuring precision and thoroughness in your response.
"""


class CondenseResult(BaseModel):
    analysis: str = Field(
        ...,
        description="""A summary of the conversation so far, capturing technical details, code patterns, and architectural decisions.""",
    )
    context: str = Field(
        ...,
        description="""The context to continue the conversation with. If applicable based on the current task, this should include:

1. Primary Request and Intent: Capture all of the user's explicit requests and intents in detail
2. Key Technical Concepts: List all important technical concepts, technologies, and frameworks discussed.
3. Files and Code Sections: Enumerate specific files and code sections examined, modified, or created. Pay special attention to the most recent messages and include full code snippets where applicable and include a summary of why this file read or edit is important.
4. Problem Solving: Document problems solved and any ongoing troubleshooting efforts.
5. Pending Tasks: Outline any pending tasks that you have explicitly been asked to work on.
6. Current Work: Describe in detail precisely what was being worked on immediately before this summary request, paying special attention to the most recent messages from both user and assistant. Include file names and code snippets where applicable.
7. Optional Next Step: List the next step that you will take that is related to the most recent work you were doing. IMPORTANT: ensure that this step is DIRECTLY in line with the user's explicit requests, and the task you were working on immediately before this summary request. If your last task was concluded, then only list next steps if they are explicitly in line with the users request. Do not start on tangential requests without confirming with the user first.
8. If there is a next step, include direct quotes from the most recent conversation showing exactly what task you were working on and where you left off. This should be verbatim to ensure there's no drift in task interpretation.
""",
    )


summarize_agent = Agent(
    instructions=SYSTEM_PROMPT,
    output_type=ToolOutput(
        type_=CondenseResult,
        name="condense",
        description="""
Your task is to create a detailed summary of the conversation so far, paying close attention to the user's explicit requests and your previous actions. This summary should be thorough in capturing technical details, code patterns, and architectural decisions that would be essential for continuing with the conversation and supporting any continuing tasks.
The user will be presented with a preview of your generated summary and can choose to use it to compact their context window or keep chatting in the current conversation.
Users may refer to this tool as 'smol' or 'compact' as well. You should consider these to be equivalent to 'condense' when used in a similar context.
""",
        max_retries=5,
    ),
    retries=3,
)


@summarize_agent.tool
def dummy_tool(ctx: RunContext[None]) -> str:
    return "ok"


def get_current_token_consumption(message_history: list[ModelMessage]) -> int:
    current_token_comsumption = 0
    for msg in reversed(message_history):
        if isinstance(msg, ModelResponse) and msg.usage.total_tokens:
            current_token_comsumption = msg.usage.total_tokens
            break
    return current_token_comsumption


MODEL_CONTEXT_WINDOW = 200_000
COMPACT_THRESHOLD = 0.8
MODEL_MAX_TOKENS = 8_000


def need_compact(message_history: list[ModelMessage]) -> bool:
    current_token_comsumption = get_current_token_consumption(message_history) or 0
    token_threshold = COMPACT_THRESHOLD * MODEL_CONTEXT_WINDOW
    will_overflow = current_token_comsumption + MODEL_MAX_TOKENS >= MODEL_CONTEXT_WINDOW
    return (current_token_comsumption and current_token_comsumption >= token_threshold) or will_overflow


def compact_messages(
    ctx: RunContext[TinybirdAgentContext],
    messages: list[ModelMessage],
) -> list[ModelMessage]:
    if not ctx.usage:
        return messages

    if not need_compact(messages):
        return messages

    original_system_prompts = extract_system_prompts(messages)
    history_messages, keep_messages = split_history(messages)

    if len(history_messages) <= 2:
        history_messages, keep_messages = split_history(messages, CompactStrategy.none)
        if len(history_messages) <= 2:
            history_messages, keep_messages = split_history(messages, CompactStrategy.in_conversation)

    if not history_messages:
        return messages

    ctx.deps.thinking_animation.stop()
    click.echo(FeedbackManager.highlight(message="» Compacting messages before continuing..."))
    result = summarize_agent.run_sync(
        "The user has accepted the condensed conversation summary you generated. Use `condense` to generate a summary and context of the conversation so far. "
        "This summary covers important details of the historical conversation with the user which has been truncated. "
        "It's crucial that you respond by ONLY asking the user what you should work on next. "
        "You should NOT take any initiative or make any assumptions about continuing with work. "
        "Keep this response CONCISE and wrap your analysis in <analysis> and <context> tags to organize your thoughts and ensure you've covered all necessary points. ",
        message_history=fix_system_prompt(history_messages, SYSTEM_PROMPT),
        model=ctx.model,
    )
    summary_prompt = f"""Condensed conversation summary(not in the history):
<condense>
<analysis>
{result.output.analysis}
</analysis>

<context>
{result.output.context}
</context>
</condense>
"""
    click.echo(FeedbackManager.info(message="✓ Compacted messages"))
    ctx.deps.thinking_animation.start()
    return [
        ModelRequest(
            parts=[
                *[SystemPromptPart(content=p) for p in original_system_prompts],
                UserPromptPart(content="Please summary the conversation"),
            ]
        ),
        ModelResponse(
            parts=[TextPart(content=summary_prompt)],
        ),
        *keep_messages,
    ]


def fix_system_prompt(message_history: list[ModelMessage], system_prompt: str) -> list[ModelMessage]:
    if not message_history:
        return message_history

    message_history_without_system: list[ModelMessage] = []
    for msg in message_history:
        # Filter out system prompts
        if not isinstance(msg, ModelRequest):
            message_history_without_system.append(msg)
            continue
        message_history_without_system.append(
            ModelRequest(
                parts=[part for part in msg.parts if not isinstance(part, SystemPromptPart)],
                instructions=msg.instructions,
            )
        )
    if message_history_without_system and isinstance(message_history_without_system[0], ModelRequest):
        # inject system prompt
        message_history_without_system[0].parts.insert(0, SystemPromptPart(content=system_prompt))

    return message_history_without_system


def extract_system_prompts(message_history: list[ModelMessage]) -> list[str]:
    system_prompts = []
    for msg in message_history:
        if isinstance(msg, ModelRequest) and isinstance(msg.parts[0], SystemPromptPart):
            system_prompts.append(msg.parts[0].content)
    return system_prompts


class CompactStrategy(str, enum.Enum):
    in_conversation = "in_conversation"
    """Compact all message, including this round conversation"""

    none = "none"
    """Compact all previous messages"""

    last_two = "last_two"
    """Keeping the last two previous messages"""


def _split_history(
    message_history: list[ModelMessage],
    n: int,
) -> tuple[list[ModelMessage], list[ModelMessage]]:
    """
    Returns a tuple of (history, keep_messages)
    """
    if not message_history:
        return [], []

    user_prompt_indices: list[int] = []
    for i, msg in enumerate(message_history):
        if not isinstance(msg, ModelRequest):
            continue
        if any(isinstance(p, UserPromptPart) for p in msg.parts) and not any(
            isinstance(p, ToolReturnPart) for p in msg.parts
        ):
            user_prompt_indices.append(i)
    if not user_prompt_indices:
        # No user prompt in history, keep all
        return [], message_history

    if not n:
        # Keep current user prompt and compact all
        keep_messages: list[ModelMessage] = []
        last_model_request = message_history[user_prompt_indices[-1]]
        keep_messages.append(last_model_request)
        if any(isinstance(p, ToolReturnPart) for p in message_history[-1].parts):
            # Include last tool-call and tool-return pair
            keep_messages.extend(message_history[-2:])
        return message_history, keep_messages

    if len(user_prompt_indices) < n:
        # No enough history to keep
        return [], message_history
    return (
        message_history[: user_prompt_indices[-n]],
        message_history[user_prompt_indices[-n] :],
    )


def split_history(
    message_history: list[ModelMessage],
    compact_strategy: CompactStrategy = CompactStrategy.last_two,
) -> tuple[list[ModelMessage], list[ModelMessage]]:
    if compact_strategy == CompactStrategy.none:
        # Only current 1
        history_messages, keep_messages = _split_history(message_history, 1)
    elif compact_strategy == CompactStrategy.last_two:
        # Previous 2 + current 1
        history_messages, keep_messages = _split_history(message_history, 3)
    elif compact_strategy == CompactStrategy.in_conversation:
        history_messages, keep_messages = _split_history(message_history, 0)
    else:
        raise NotImplementedError(f"Compact strategy {compact_strategy} not implemented")

    return history_messages, keep_messages
