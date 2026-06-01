import pydantic

import mistralai.workflows as workflows


class Utf8Params(pydantic.BaseModel):
    message: str = pydantic.Field(description="Message with UTF-8 characters")


class Utf8Result(pydantic.BaseModel):
    original_message: str = pydantic.Field(description="Original message echoed back")
    message_length: int = pydantic.Field(description="Length of the message in characters")
    contains_emoji: bool = pydantic.Field(description="Whether the message contains emoji")


@workflows.activity()
async def echo_utf8_activity(message: str) -> Utf8Result:
    contains_emoji = any(ord(c) > 0x1F000 for c in message)
    return Utf8Result(
        original_message=message,
        message_length=len(message),
        contains_emoji=contains_emoji,
    )


@workflows.workflow.define(
    name="utf8-encoding-test-workflow",
    workflow_display_name="UTF-8 Encoding Test",
    workflow_description="Tests UTF-8 encoding with emojis and special characters",
)
class Utf8EncodingTestWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, params: Utf8Params) -> Utf8Result:
        return await echo_utf8_activity(params.message)
