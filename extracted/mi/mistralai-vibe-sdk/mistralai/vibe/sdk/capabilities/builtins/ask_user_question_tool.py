"""Client-handled ask-user-question tool for interactive hosts."""

from pydantic import BaseModel, Field

from mistralai.vibe.sdk.capabilities import client_tool


class Choice(BaseModel):
    label: str = Field(description="Short label for the choice (1-5 words)")
    description: str = Field(default="", description="Optional explanation of this choice")


class Question(BaseModel):
    question: str = Field(description="The question text")
    header: str = Field(
        default="",
        description="Short header for the question (1-2 words, e.g. 'Auth')",
        max_length=12,
    )
    options: list[Choice] = Field(
        description=(
            "Available options (2-4, not including 'Other'). An 'Other' option for "
            "free text is automatically added."
        ),
        min_length=2,
        max_length=4,
    )
    multi_select: bool = Field(
        default=False, description="If true, user can select multiple options"
    )
    hide_other: bool = Field(
        default=False, description="If true, hide the 'Other' free text option"
    )


class AskUserQuestionArgs(BaseModel):
    questions: list[Question] = Field(
        description="Questions to ask (1-4). Displayed as tabs if multiple.",
        min_length=1,
        max_length=4,
    )
    content_preview: str | None = Field(
        default=None,
        description="Optional text content to display in a scrollable area above the questions.",
    )


class Answer(BaseModel):
    question: str = Field(description="The original question")
    answer: str = Field(description="The user's answer")
    is_other: bool = Field(
        default=False, description="True if user typed a custom answer via 'Other'"
    )


class AskUserQuestionResult(BaseModel):
    answers: list[Answer] = Field(description="List of answers")
    cancelled: bool = Field(default=False, description="True if user cancelled without answering")


@client_tool(
    name="ask_user_question",
    description=(
        "Ask the user one or more questions and wait for their responses. "
        "Each question has 2-4 choices plus an automatic 'Other' option for free text. "
        "Use this to gather preferences, clarify requirements, or get decisions."
    ),
    input_schema=AskUserQuestionArgs,
    output_schema=AskUserQuestionResult,
)
def ask_user_question(_args: AskUserQuestionArgs) -> AskUserQuestionResult:
    raise RuntimeError("ask_user_question requires a host handler")
