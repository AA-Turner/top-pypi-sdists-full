"""Live Mistral completion example covering chat, tools, logs, and metrics."""

import json
import os
import secrets
from dataclasses import dataclass
from pprint import pprint

from mistralai.client import Mistral
from mistralai.client.models.assistantmessage import AssistantMessageTypedDict
from mistralai.client.models.chatcompletionrequest import ChatCompletionRequestMessageTypedDict
from mistralai.client.models.chatcompletionresponse import ChatCompletionResponse
from mistralai.client.models.tool import ToolTypedDict
from mistralai.client.models.toolcall import ToolCallTypedDict
from mistralai.client.models.toolmessage import ToolMessageTypedDict

from mistralai.observability.otel import Features, observability
from mistralai.observability.otel import semconv_constants as genai

MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "mistral-completion-example")
CONVERSATION_ID = os.getenv("MISTRAL_CONVERSATION_ID", f"example-weather-session-{secrets.token_urlsafe(8)}")
MISTRAL_API_ENDPOINT = os.getenv("MISTRAL_API_ENDPOINT")
MISTRAL_TELEMETRY_ENDPOINT = os.getenv("MISTRAL_TELEMETRY_ENDPOINT", "https://api.mistral.ai/telemetry")
WEATHER_TOOL_NAME = "get_weather"
WEATHER_TOOL: ToolTypedDict = {
    "type": "function",
    "function": {
        "name": WEATHER_TOOL_NAME,
        "description": "Return the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name, for example Paris.",
                }
            },
            "required": ["city"],
        },
    },
}


@dataclass(frozen=True, slots=True)
class ParsedWeatherToolCall:
    """Validated weather tool call extracted from a Mistral response."""

    call_id: str
    name: str
    arguments: dict[str, str]
    city: str


def get_weather(city: str) -> dict[str, str]:
    """Return deterministic weather data for the example tool call."""
    # Keep the tool deterministic so the example focuses on the telemetry
    # boundary. Real code would call a database, service, or MCP tool here.
    return {
        "city": city,
        "forecast": "sunny",
        "temperature": "21 C",
    }


def parse_weather_tool_call(response: ChatCompletionResponse) -> ParsedWeatherToolCall:
    """Extract the first weather tool call and validate its city argument."""
    if not response.choices:
        error_message = "Mistral response did not include any choices"
        raise RuntimeError(error_message)

    tool_response_message = response.choices[0].message
    if tool_response_message is None or not tool_response_message.tool_calls:
        error_message = "Mistral response did not include a tool call"
        raise RuntimeError(error_message)

    tool_call = tool_response_message.tool_calls[0]
    tool_call_id = tool_call.id
    if tool_call_id is None:
        error_message = "Mistral response tool call did not include an id"
        raise RuntimeError(error_message)

    raw_arguments: object = tool_call.function.arguments
    if isinstance(raw_arguments, str):
        decoded_arguments: object = json.loads(raw_arguments)
    else:
        decoded_arguments = raw_arguments

    match decoded_arguments:
        case {"city": str(city_argument)}:
            weather_arguments = {"city": city_argument}
        case _:
            error_message = "Mistral response tool arguments must include a string 'city' field"
            raise TypeError(error_message)

    return ParsedWeatherToolCall(
        call_id=tool_call_id,
        name=tool_call.function.name,
        arguments=weather_arguments,
        city=city_argument,
    )


def main() -> None:
    """Run the live telemetry example."""
    api_key = os.environ["MISTRAL_API_KEY"]

    client = Mistral(api_key=api_key, server_url=MISTRAL_API_ENDPOINT)
    observability.configure_mistral(
        service_name=SERVICE_NAME,
        api_key=api_key,
        endpoint=MISTRAL_TELEMETRY_ENDPOINT,
    )

    try:
        # `conversation.id` correlates separate traces that belong to the same
        # application session. Use a real session/thread id in production; the
        # SDK deliberately never generates fallback conversation identifiers.
        with (
            observability.conversation(CONVERSATION_ID),
            # The outer chat span is the main request. `include_content=True`
            # opts in to recording input/output messages on the span for this
            # smoke example.
            observability.operation(
                genai.OPERATION_NAME_CHAT,
                model=MODEL,
                provider=genai.PROVIDER_NAME_MISTRAL_AI,
                include_content=True,
                features=Features(moderation=True),
            ) as parent_op,
        ):
            messages: list[ChatCompletionRequestMessageTypedDict] = [
                {"role": "user", "content": "Say hello in French in one short sentence."}
            ]
            response = client.chat.complete(model=MODEL, messages=messages)
            parent_op.mistral_completion(response, messages=messages)
            parent_op.log("chat completion recorded")

            # This second chat runs while the first operation is still active,
            # so it becomes a child span through the current OpenTelemetry
            # context.
            with observability.operation(
                genai.OPERATION_NAME_CHAT,
                model=MODEL,
                provider=genai.PROVIDER_NAME_MISTRAL_AI,
                include_content=True,
            ) as child_op:
                followup_messages: list[ChatCompletionRequestMessageTypedDict] = [
                    {"role": "user", "content": "Say hello in Spanish in one short sentence."}
                ]
                child_response = client.chat.complete(model=MODEL, messages=followup_messages)
                child_op.mistral_completion(child_response, messages=followup_messages)

            # The tool scenario has one chat span for the model request and a
            # child `execute_tool` span for local code invoked by the tool call.
            # It inherits the conversation id through the active conversation
            # context.
            with observability.operation(
                genai.OPERATION_NAME_CHAT,
                model=MODEL,
                provider=genai.PROVIDER_NAME_MISTRAL_AI,
                include_content=True,
            ) as tool_chat:
                tool_messages: list[ChatCompletionRequestMessageTypedDict] = [
                    {"role": "user", "content": "What is the weather in Paris? Use the available tool."}
                ]
                tool_response = client.chat.complete(
                    model=MODEL,
                    messages=tool_messages,
                    tools=[WEATHER_TOOL],
                    tool_choice="auto",
                )
                tool_chat.mistral_completion(tool_response, messages=tool_messages)

                # The first response asks for a tool. That response is still
                # recorded on the chat span; the local tool execution is a
                # separate child span so its duration and attributes are visible.
                parsed_tool_call = parse_weather_tool_call(tool_response)

                with observability.tool(
                    parsed_tool_call.name,
                    parent=tool_chat,
                    call_id=parsed_tool_call.call_id,
                    tool_type=genai.TOOL_TYPE_FUNCTION,
                    arguments=parsed_tool_call.arguments,
                    agent_name="Mistral chat completion",
                ) as tool_op:
                    tool_result = get_weather(parsed_tool_call.city)
                    tool_op.set_attribute(genai.ATTR_GEN_AI_TOOL_CALL_RESULT, json.dumps(tool_result))

                # Send the assistant tool call and the tool result back to the
                # model. This final completion enriches the same chat span with
                # the final response metadata and content.
                assistant_tool_call: ToolCallTypedDict = {
                    "id": parsed_tool_call.call_id,
                    "type": "function",
                    "function": {
                        "name": parsed_tool_call.name,
                        "arguments": parsed_tool_call.arguments,
                    },
                }
                assistant_message: AssistantMessageTypedDict = {
                    "role": "assistant",
                    "tool_calls": [assistant_tool_call],
                }
                tool_message: ToolMessageTypedDict = {
                    "role": "tool",
                    "tool_call_id": parsed_tool_call.call_id,
                    "name": parsed_tool_call.name,
                    "content": json.dumps(tool_result),
                }
                final_tool_messages: list[ChatCompletionRequestMessageTypedDict] = [
                    *tool_messages,
                    assistant_message,
                    tool_message,
                ]
                final_tool_response = client.chat.complete(model=MODEL, messages=final_tool_messages)
                tool_chat.mistral_completion(final_tool_response, messages=final_tool_messages)

        # Evaluation can happen after the span ended. The operation object keeps
        # its trace/span identifiers and conversation id, so the log still
        # attaches to the completed chat operation and the same conversation.
        parent_op.evaluation_result(
            "manual-review",
            score_label="pass",
            explanation="Delayed evaluation attached to the completed chat operation.",
        )

        # Print identifiers that make it easy to inspect the trace relationships
        # in the configured backend after running the example.
        pprint(
            {
                "main": {
                    "conversation_id": parent_op.conversation_id,
                    "trace_id": parent_op.trace_id,
                    "span_id": parent_op.span_id,
                    "response_id": response.id,
                },
                "child": {
                    "conversation_id": child_op.conversation_id,
                    "trace_id": child_op.trace_id,
                    "span_id": child_op.span_id,
                    "response_id": child_response.id,
                },
                "tool_chat": {
                    "conversation_id": tool_chat.conversation_id,
                    "trace_id": tool_chat.trace_id,
                    "span_id": tool_chat.span_id,
                    "response_id": final_tool_response.id,
                },
            }
        )
    finally:
        observability.shutdown()


if __name__ == "__main__":
    main()
