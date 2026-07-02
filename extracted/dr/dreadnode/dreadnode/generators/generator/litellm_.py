import asyncio
import base64
import datetime
import re
import typing as t
import warnings

from loguru import logger

from dreadnode.agents.tools import FunctionDefinition, ToolDefinition
from dreadnode.app.model_catalog import infer_provider
from dreadnode.generators.exceptions import GeneratorWarning, ProcessingError
from dreadnode.generators.generator.base import (
    Fixup,
    GeneratedMessage,
    GeneratedText,
    GenerateParams,
    Generator,
    Usage,
    trace_messages,
    trace_str,
    with_fixups,
)
from dreadnode.generators.message import (
    CompatibilityFlag,
    ContentAudioInput,
    ContentImageUrl,
    ContentText,
    ContentVideoUrl,
    Message,
)

if t.TYPE_CHECKING:
    from litellm.types.utils import ModelResponse, TextCompletionResponse


# Suppress pydantic serialization warnings from litellm types (Message, Choices, etc.)
# whose runtime fields don't match their declared schema.
warnings.filterwarnings("ignore", message="Pydantic serializer warnings", module="pydantic")


class OpenAIToolsWithImageURLsFixup(Fixup):
    # As of writing, openai doesn't support multi-part messages
    # associated with the `tool` role. This is complicated by
    # the fact that we need to resolve the tool call(s) in the
    # following messages. To get around this, we'll resolve the tool
    # call with empty content, and duplicate the multi-part data
    # into a user message immediately following it. We also need
    # to take care of multiple tool calls next to each other and ensure
    # we don't add the user message in between them.

    def can_fix(self, exception: Exception) -> bool:
        return (
            "Image URLs are only allowed for messages with role 'user', but this message with role 'tool' contains an image URL."
            in str(exception)
        )

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        updated_messages: list[Message] = []
        append_queue: list[Message] = []
        for message in messages:
            if message.role == "tool" and isinstance(message.content_parts, list):
                updated_messages.append(
                    message.model_copy(
                        deep=True,
                        update={"content_parts": [ContentText(text="See next message")]},
                    ),
                )
                append_queue.append(message.model_copy(deep=True, update={"role": "user"}))
            else:
                updated_messages.extend(append_queue)
                append_queue = []
                updated_messages.append(message)

        updated_messages.extend(append_queue)
        return updated_messages


class CacheTooSmallFixup(Fixup):
    # Attempt to enable caching on chat messages which
    # are below a certain threshold can result in a 400
    # error from APIs (Vertex/Gemini).

    def can_fix(self, exception: Exception) -> bool | t.Literal["once"]:
        return "once" if "Cached content is too small." in str(exception) else False

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        marked = sum(
            1
            for message in messages
            for part in message.content_parts
            if part.cache_control is not None
        )
        logger.warning(
            "CacheTooSmallFixup | provider rejected request as below cache threshold "
            "(Vertex/Gemini); stripping {} cache_control marker(s) for this call",
            marked,
        )
        return [message.cache(False) for message in messages]


class CacheControlOnEmptyTextFixup(Fixup):
    # Anthropic rejects `cache_control` attached to an empty text block with:
    #   "cache_control cannot be set for empty text blocks"
    # This can surface right after compaction when the rolling cache window
    # lands on a tool result whose last text part is empty. Message.cache()
    # defends against this directly, but as a belt-and-suspenders retry we
    # strip cache_control from every empty ContentText part and resend.

    def can_fix(self, exception: Exception) -> bool | t.Literal["once"]:
        message = str(exception)
        if "cache_control" in message and "empty text" in message:
            return "once"
        return False

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        fixed: list[Message] = []
        stripped = 0
        for message in messages:
            if any(
                isinstance(part, ContentText) and not part.text and part.cache_control is not None
                for part in message.content_parts
            ):
                cloned = message.clone()
                for part in cloned.content_parts:
                    if isinstance(part, ContentText) and not part.text:
                        if part.cache_control is not None:
                            stripped += 1
                        part.cache_control = None
                fixed.append(cloned)
            else:
                fixed.append(message)
        logger.warning(
            "CacheControlOnEmptyTextFixup | Anthropic rejected cache_control on empty "
            "text block(s); stripped {} marker(s) — likely a tool result with empty "
            "content landed in the rolling cache window",
            stripped,
        )
        return fixed


class GroqAssistantContentFixup(Fixup):
    # Groq can complain if we try to send fully
    # structured content parts when working with
    # the assistant role.
    #
    # Compatibility flags are a poor workaround for the
    # fact that we don't have direct control over the
    # conversion to the OpenAI spec.

    def can_fix(self, exception: Exception) -> bool:
        return "Groq" in str(exception) and "content' : value must be a string" in str(exception)

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        updated_messages: list[Message] = []
        for message in messages:
            if message.role == "assistant":
                message = message.clone()  # noqa: PLW2901
                message.compatibility_flags.add("content_as_str")
            updated_messages.append(message)
        return updated_messages


class ReservedToolNameFixup(Fixup):
    # OpenAI reasoning models (o3, o4-mini, etc.) reserve certain function
    # names like "python" for built-in tools. When this error is detected,
    # rename the conflicting tools in outbound requests and reverse-map
    # the names in responses so the rest of the system is unaffected.

    _RESERVED: t.ClassVar[dict[str, str]] = {"python": "python_exec"}
    _REVERSE: t.ClassVar[dict[str, str]] = {"python_exec": "python"}

    def can_fix(self, exception: Exception) -> bool:
        return "is reserved for use by this model" in str(exception)

    @staticmethod
    def _rename_tool_calls(
        tool_calls: list[t.Any],
        mapping: dict[str, str],
    ) -> tuple[list[t.Any], bool]:
        """Rename function names in a tool_calls list, returning (new_list, changed)."""
        new_calls: list[t.Any] = []
        changed = False
        for tc in tool_calls:
            tc_dict = tc if isinstance(tc, dict) else {}
            fn = tc_dict.get("function", {}) if isinstance(tc_dict, dict) else {}
            fn_name = fn.get("name", "") if isinstance(fn, dict) else ""
            if fn_name in mapping:
                new_fn = {**fn, "name": mapping[fn_name]}
                new_calls.append({**tc_dict, "function": new_fn})
                changed = True
            else:
                new_calls.append(tc)
        return new_calls, changed

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        # Rename function names in prior assistant tool_calls so the
        # model sees consistent naming in the conversation history.
        updated: list[Message] = []
        for message in messages:
            if message.role == "assistant" and message.tool_calls:
                new_calls, changed = self._rename_tool_calls(message.tool_calls, self._RESERVED)
                if changed:
                    updated.append(message.model_copy(deep=True, update={"tool_calls": new_calls}))
                else:
                    updated.append(message)
            else:
                updated.append(message)
        return updated

    def fix_params(self, params: GenerateParams) -> GenerateParams:
        if not params.tools:
            return params
        new_tools: list[ToolDefinition] = []
        changed = False
        for td in params.tools:
            if td.function.name in self._RESERVED:
                new_tools.append(
                    ToolDefinition(
                        type=td.type,
                        function=FunctionDefinition(
                            name=self._RESERVED[td.function.name],
                            description=td.function.description,
                            parameters=td.function.parameters,
                        ),
                    )
                )
                changed = True
            else:
                new_tools.append(td)
        if not changed:
            return params
        return params.model_copy(update={"tools": new_tools})

    def fix_result(self, result: t.Any) -> t.Any:
        if not isinstance(result, GeneratedMessage):
            return result
        if not result.message.tool_calls:
            return result
        new_calls, changed = self._rename_tool_calls(result.message.tool_calls, self._REVERSE)
        if changed:
            result.message.tool_calls = new_calls
        return result


class AnthropicToolResultFixup(Fixup):
    # Anthropic requires that every tool_use block has a corresponding
    # tool_result block immediately after. This fixup removes orphaned
    # tool_use blocks that don't have corresponding tool_results.

    def can_fix(self, exception: Exception) -> bool:
        return "tool_use" in str(exception) and "tool_result" in str(exception)

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        # Build a set of tool_call_ids that have results
        tool_result_ids: set[str] = set()
        for message in messages:
            if message.role == "tool" and message.tool_call_id:
                tool_result_ids.add(message.tool_call_id)

        # Now filter messages, removing tool_calls that don't have results
        updated_messages: list[Message] = []
        for message in messages:
            if message.role == "assistant" and message.tool_calls:
                # Filter tool_calls to only include those with results
                valid_tool_calls = [tc for tc in message.tool_calls if tc.id in tool_result_ids]
                if valid_tool_calls or message.content:
                    # Clone and update tool_calls
                    new_message = message.clone()
                    new_message.tool_calls = valid_tool_calls or None
                    updated_messages.append(new_message)
                # If no valid tool_calls and no content, skip this message entirely
            else:
                updated_messages.append(message)

        return updated_messages


class SingleTurnFlattenFixup(Fixup):
    """Flatten multi-turn conversations for endpoints that only support user/system roles.

    Some providers (e.g. Microsoft MAI) expose chat-shaped endpoints that reject
    ``assistant`` and ``tool`` roles entirely. When litellm's ``drop_params`` retry
    loop swallows the 422 and returns ``None``, we detect it here and collapse the
    entire message history into system + single user message with role markers
    preserving the conversation context.

    Tools are stripped from the API call because the flattened single-turn format
    is incompatible with structured function calling — models that receive tools
    alongside flattened messages produce tool calls with empty arguments. The model
    can still describe tool usage in its text response.
    """

    def can_fix(self, exception: Exception) -> bool:
        return "None response" in str(exception)

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        system_parts: list[str] = []
        conversation_parts: list[str] = []

        for message in messages:
            text = message.content.strip() if message.content else ""
            if message.role == "system":
                system_parts.append(text)
            elif message.role == "assistant":
                if text:
                    conversation_parts.append(f"[assistant]\n{text}\n[/assistant]")
            # user and tool roles both become user turns
            elif text:
                conversation_parts.append(f"[user]\n{text}\n[/user]")

        result: list[Message] = []
        if system_parts:
            result.append(Message(role="system", content="\n\n".join(system_parts)))
        result.append(Message(role="user", content="\n".join(conversation_parts)))

        logger.debug(
            "SingleTurnFlattenFixup | flattened {} messages -> {}", len(messages), len(result)
        )
        return result

    def fix_params(self, params: GenerateParams) -> GenerateParams:
        """Strip tools when flattening — structured function calling is incompatible
        with single-turn flattened messages and causes empty tool call arguments."""
        if not params.tools:
            return params
        logger.debug(
            "SingleTurnFlattenFixup | stripping {} tools from flattened request",
            len(params.tools),
        )
        return params.model_copy(update={"tools": None, "tool_choice": None})


class ImageInputUnsupportedFixup(Fixup):
    # Text-only endpoints return a 404 or similar error when the
    # request contains ``image_url`` content parts. Rather than killing
    # the sample, we replace visual parts with a textual representation
    # containing image metadata (dimensions, format, EXIF, PNG chunks)
    # and a hex dump of the file head/tail so the model can still reason
    # about the file contents.
    #
    # The ``read`` tool already produces a short caption alongside every
    # image (e.g. "Read image · PNG · 42.5 KB") which is preserved as-is.
    #
    # NOTE: metadata + hex dump is one interpretation of how to present an
    # image to a text-only model, chosen because the failing tasks are CTF
    # forensics where flags hide in EXIF/embedded bytes. Revisit once we have
    # evidence on what representation actually helps text-only models across
    # task types — this likely belongs closer to the tool/eval layer than to a
    # litellm error-recovery fixup (see CAP-1076).

    _IMAGE_REJECT_PATTERNS: t.ClassVar[list[str]] = [
        "No endpoints found that support image input",
        "does not support image input",
        "does not support vision",
        "image_url is not supported",
        "Content type image_url is not supported",
    ]

    _HEX_HEAD_SIZE: t.ClassVar[int] = 256
    _HEX_TAIL_SIZE: t.ClassVar[int] = 128
    _INFO_VALUE_MAX_LEN: t.ClassVar[int] = 500
    _EXIF_VALUE_MAX_LEN: t.ClassVar[int] = 300

    def can_fix(self, exception: Exception) -> bool:
        error_str = str(exception)
        return any(pattern in error_str for pattern in self._IMAGE_REJECT_PATTERNS)

    def fix(self, messages: t.Sequence[Message]) -> t.Sequence[Message]:
        updated: list[Message] = []
        stripped_count = 0

        for message in messages:
            has_visual = any(
                isinstance(part, (ContentImageUrl, ContentVideoUrl))
                for part in message.content_parts
            )
            if not has_visual:
                updated.append(message)
                continue

            new_parts: list[ContentText | ContentAudioInput] = []
            for part in message.content_parts:
                if isinstance(part, (ContentImageUrl, ContentVideoUrl)):
                    stripped_count += 1
                    description = self._describe_visual_part(part)
                    label = "Image" if isinstance(part, ContentImageUrl) else "Video"
                    new_parts.append(
                        ContentText(
                            text=(
                                f"[{label} content replaced — model does not support visual input. "
                                f"Textual representation follows]\n{description}"
                            )
                        )
                    )
                else:
                    # Preserve ContentText and ContentAudioInput as-is
                    new_parts.append(part)

            updated.append(message.model_copy(deep=True, update={"content_parts": new_parts}))

        if stripped_count:
            logger.warning(
                "ImageInputUnsupportedFixup | replaced {} visual content part(s) with "
                "textual descriptions — provider does not support image input",
                stripped_count,
            )

        return updated

    # -- helpers --

    @staticmethod
    def _hex_block(data: bytes, label: str) -> list[str]:
        block: list[str] = [f"{label} ({len(data)} bytes):"]
        for offset in range(0, len(data), 16):
            chunk = data[offset : offset + 16]
            hex_part = " ".join(f"{b:02x}" for b in chunk)
            ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            block.append(f"  {offset:08x}  {hex_part:<48s}  |{ascii_part}|")
        return block

    @classmethod
    def _hex_dump(cls, raw: bytes) -> list[str]:
        lines = cls._hex_block(raw[: cls._HEX_HEAD_SIZE], "Hex head")
        if len(raw) > cls._HEX_HEAD_SIZE + cls._HEX_TAIL_SIZE:
            lines.append(
                f"... ({len(raw) - cls._HEX_HEAD_SIZE - cls._HEX_TAIL_SIZE} bytes omitted) ..."
            )
            lines.extend(cls._hex_block(raw[-cls._HEX_TAIL_SIZE :], "Hex tail"))
        elif len(raw) > cls._HEX_HEAD_SIZE:
            lines.extend(cls._hex_block(raw[cls._HEX_HEAD_SIZE :], "Hex tail"))
        return lines

    @classmethod
    def _describe_image_bytes(cls, raw: bytes) -> str:
        import io

        lines: list[str] = []

        try:
            from PIL import Image
            from PIL.ExifTags import TAGS

            with Image.open(io.BytesIO(raw)) as img:
                lines.append(f"Format: {img.format or 'unknown'}")
                lines.append(f"Size: {img.size[0]}x{img.size[1]}")
                lines.append(f"Mode: {img.mode}")

                if img.info:
                    for key, value in img.info.items():
                        val_str = str(value)
                        if len(val_str) > cls._INFO_VALUE_MAX_LEN:
                            val_str = val_str[: cls._INFO_VALUE_MAX_LEN] + "…"
                        lines.append(f"Info[{key}]: {val_str}")

                exif = img.getexif()
                if exif:
                    lines.append("EXIF:")
                    for tag_id, value in exif.items():
                        tag_name = TAGS.get(tag_id, f"Tag{tag_id}")
                        val_str = str(value)
                        if len(val_str) > cls._EXIF_VALUE_MAX_LEN:
                            val_str = val_str[: cls._EXIF_VALUE_MAX_LEN] + "…"
                        lines.append(f"  {tag_name}: {val_str}")
        except Exception as exc:
            lines.append(f"[metadata extraction failed: {exc}]")

        lines.extend(cls._hex_dump(raw))
        return "\n".join(lines)

    @classmethod
    def _describe_visual_part(cls, part: ContentImageUrl | ContentVideoUrl) -> str:
        try:
            if isinstance(part, ContentImageUrl):
                # Remote (non-data) URLs can't be inlined; surface the URL so the
                # model at least knows an image existed and where it lives.
                if not part.image_url.url.startswith("data:"):
                    return f"[remote image at {part.image_url.url} — content not inlined]"
                return cls._describe_image_bytes(part.to_bytes())
            # ContentVideoUrl.to_bytes() handles both raw base64 and data URLs.
            raw = part.to_bytes()
            lines = [f"Video file ({len(raw)} bytes)"]
            lines.extend(cls._hex_dump(raw))
            return "\n".join(lines)
        except Exception as exc:
            return f"[failed to describe visual content: {exc}]"


g_fixups = [
    OpenAIToolsWithImageURLsFixup(),
    CacheTooSmallFixup(),
    CacheControlOnEmptyTextFixup(),
    GroqAssistantContentFixup(),
    AnthropicToolResultFixup(),
    ReservedToolNameFixup(),
    SingleTurnFlattenFixup(),
    ImageInputUnsupportedFixup(),
]

vertex_image_pattern = re.compile(r"(data:[\w/]+?;base64,[A-Za-z0-9+/=]+)")


def _compatibility_flags_for_model(model: str) -> set[CompatibilityFlag]:
    """Return message serialization flags needed by LiteLLM provider adapters."""
    normalized = model.lower()
    if infer_provider(model) == "google" or normalized.startswith(
        ("vertex_ai/", "vertex_ai_beta/")
    ):
        return {"file_data_as_data_url"}
    return set()


class LiteLLMGenerator(Generator):
    """
    Generator backed by the LiteLLM library.

    Find more information about supported models and formats [in their docs.](https://docs.litellm.ai/docs/providers).

    Note:
        Batching support is not performant and simply a loop over inputs.

    Warning:
        While some providers support passing `n` to produce a batch
        of completions per request, we don't currently use this in the
        implementation due to it's brittle requirements.

    Tip:
        Consider setting [`max_connections`][rigging.generator.litellm_.LiteLLMGenerator.max_connections]
        or [`min_delay_between_requests`][rigging.generator.litellm_.LiteLLMGenerator.min_delay_between_requests
        if you run into API limits. You can pass this directly in the generator id:

        ```
        get_generator("litellm!openai/gpt-4o,max_connections=2,min_delay_between_requests=1000")
        ```
    """

    max_connections: int = 10
    """
    How many simultaneous requests to pool at one time.
    This is useful to set when you run into API limits at a provider.

    Set to 0 to remove the limit.
    """

    min_delay_between_requests: float = 0.0
    """
    Minimum time (ms) between each request.
    This is useful to set when you run into API limits at a provider.
    """

    _semaphore: asyncio.Semaphore | None = None
    _last_request_time: datetime.datetime | None = None
    _supports_function_calling: bool | None = None
    _supports_prompt_caching: bool | None = None

    def __post_model_init__(self, _: t.Any) -> None:
        import litellm

        # We should probably let people configure
        # this independently, but for now we'll
        # fix it to prevent confusion
        litellm.drop_params = True

        # Allow litellm to automatically handle thinking/tool-calling
        # incompatibilities (e.g. dropping thinking params when
        # thinking_blocks are missing from prior assistant messages).
        litellm.modify_params = True

        # Prevent the small debug statements
        # from being printed to the console
        litellm.suppress_debug_info = True  # ty: ignore[invalid-assignment]

    @property
    def semaphore(self) -> asyncio.Semaphore:
        if self._semaphore is None:
            # TODO(nick): This is hacky.
            max_connections = self.max_connections if self.max_connections > 0 else 10_000
            self._semaphore = asyncio.Semaphore(max_connections)
        return self._semaphore

    def _capability_lookup_models(self) -> list[str]:
        """Model names to try when probing litellm's static capability tables.

        We always try ``self.model`` verbatim first — the routing-meaningful
        name. As a *narrow* fallback, when this generator is configured for
        Dreadnode's litellm-proxy route (``custom_llm_provider="litellm_proxy"``
        in extra params, set by ``model_resolution.build_turn_generator``),
        the leading segment is a Dreadnode-internal alias (e.g. ``dn/...``)
        that hides the underlying model from litellm's tables. In *that*
        case only, also try the suffix once. We never strip prefixes for
        unrouted models — ``bedrock/``, ``azure/``, ``openrouter/``, etc.
        carry routing/cost meaning and stripping them would silently
        change the answer.
        """
        candidates = [self.model]
        extra = self.params.extra if self.params is not None else {}
        if (
            isinstance(extra, dict)
            and extra.get("custom_llm_provider") == "litellm_proxy"
            and "/" in self.model
        ):
            candidates.append("/".join(self.model.split("/")[1:]))
        return candidates

    async def supports_function_calling(self) -> bool | None:
        import litellm.utils

        import dreadnode as dn

        if self._supports_function_calling is not None:
            return self._supports_function_calling

        for candidate in self._capability_lookup_models():
            if litellm.utils.supports_function_calling(candidate):
                self._supports_function_calling = True
                return self._supports_function_calling

        self._supports_function_calling = False

        # Otherwise we'll run a small check to see if we can

        with dn.span(f"Checking '{self.model}' for function calling support") as span:
            try:
                generated = await self.generate_messages(
                    [[Message(role="user", content="Call the test function")]],
                    [
                        GenerateParams(
                            tools=[
                                ToolDefinition(
                                    function=FunctionDefinition(
                                        name="test_function",
                                        description="Test function",
                                    ),
                                ),
                            ],
                        ),
                    ],
                )

                if generated:
                    if isinstance(generated[0], BaseException):
                        raise generated[0]  # noqa: TRY301 - intentional routing through shared probe warning/span path

                    if (
                        isinstance(generated[0], GeneratedMessage)
                        and generated[0].message.tool_calls
                    ):
                        self._supports_function_calling = True
            except Exception as e:
                # Include exception type for easier debugging; the str(e) from
                # litellm is often empty (e.g. "AnthropicException - .").
                cause = getattr(e, "__cause__", None) or getattr(e, "__context__", None)
                detail = f"{type(e).__name__}: {e}" + (f" (cause: {cause})" if cause else "")
                logger.warning("Failed to check for function calling support: {}", detail)
                span.set_attribute("error", detail)

            span.set_attribute("supports_function_calling", self._supports_function_calling)

        return self._supports_function_calling

    def supports_prompt_caching(self) -> bool:
        import litellm.utils

        if self._supports_prompt_caching is not None:
            return self._supports_prompt_caching

        self._supports_prompt_caching = False
        for candidate in self._capability_lookup_models():
            try:
                if litellm.utils.supports_prompt_caching(candidate):
                    self._supports_prompt_caching = True
                    break
            except Exception as e:
                logger.debug("Failed to check prompt caching support for '{}': {}", candidate, e)

        return self._supports_prompt_caching

    async def _ensure_delay_between_requests(self) -> None:
        if self._last_request_time is None:
            return

        delta = datetime.datetime.now(tz=datetime.UTC) - self._last_request_time
        delta_ms = delta.total_seconds() * 1000

        if delta_ms < self.min_delay_between_requests:
            wait_seconds = (self.min_delay_between_requests - delta_ms) / 1000
            logger.trace(f"Waiting {wait_seconds} seconds")
            await asyncio.sleep(wait_seconds)

    # TODO(nick): Some model providers support using `n` as a batch
    # parameter to generate multiple completions at once. Which
    # could help us optimize run_many calls.
    #
    # If we wanted this, we'd need to check the model provider
    # and see if it was supported, and all our messages/texts
    # were equal before overriding that parameter to the call.
    #
    # This seems like a brittle feature at the moment, so we'll
    # leave it out for now.

    def _warn_on_input_truncation(
        self, messages: list[Message], response: "GeneratedMessage"
    ) -> None:
        # Ollama has a known behavior where it performs silent truncation
        # of input messages rather than return an error or any API indication.
        #
        # This code attempts to detect such truncation by comparing the expected
        # input length with the reported usage - but it's not foolproof.
        #
        # See:
        # - https://github.com/ollama/ollama/issues/7043
        # - https://github.com/ollama/ollama/issues/7987
        # - https://github.com/ollama/ollama/issues/4967

        # Not perfect
        if "ollama" not in self.model.lower():
            return

        # We can't check with usage info
        if not response.usage:
            return

        # Get a general view of how long we might expect the input prompt to
        # We'll use a gracious 10 char per token estimate
        input_tokens_estimate = int(sum(len(message.content) for message in messages) / 10)

        # Check if the response reports that accepted input tokens are less than this
        if response.usage.input_tokens < input_tokens_estimate:
            warnings.warn(
                f"Input messages may have been truncated - see https://github.com/ollama/ollama/issues/7043 "
                f"(input tokens: {response.usage.input_tokens} < estimate: {input_tokens_estimate})",
                GeneratorWarning,
                stacklevel=2,
            )

    def _trace_generation_meta(self, generated: GeneratedMessage) -> None:
        """Log trace-level metadata about thinking/reasoning in a generation response."""
        usage = generated.usage
        extra = generated.extra or {}

        parts: list[str] = [f"model={self.model}"]

        if usage is not None:
            parts.append(f"input={usage.input_tokens}")
            parts.append(f"output={usage.output_tokens}")

            # Reasoning tokens (nested in completion_tokens_details for some providers)
            details = getattr(usage, "completion_tokens_details", None)
            if details:
                reasoning_tokens = (
                    details.get("reasoning_tokens")
                    if isinstance(details, dict)
                    else getattr(details, "reasoning_tokens", None)
                )
                if reasoning_tokens:
                    parts.append(f"reasoning_tokens={reasoning_tokens}")

            # Cache stats (Anthropic-style)
            if cache_creation := getattr(usage, "cache_creation_input_tokens", None):
                parts.append(f"cache_creation={cache_creation}")
            if cache_read := getattr(usage, "cache_read_input_tokens", None):
                parts.append(f"cache_read={cache_read}")

        # Thinking content presence
        if reasoning_content := extra.get("reasoning_content"):
            parts.append(f"reasoning_content={len(reasoning_content)}ch")
        if thinking_blocks := extra.get("thinking_blocks"):
            parts.append(f"thinking_blocks={len(thinking_blocks)}")

        if extra.get("provider"):
            parts.append(f"provider={extra['provider']}")

        logger.debug("Generation meta | {}", " | ".join(parts))

    def _parse_model_response(
        self,
        response: "ModelResponse",
    ) -> GeneratedMessage:
        import litellm.types.utils

        if not response:
            raise ProcessingError("Empty response from provider")

        if not response.choices:
            raise ProcessingError(f"No choices in model response: {response.model_dump()}")

        choice = response.choices[-1]
        usage = None
        response_usage = getattr(response, "usage", None)
        if response_usage is not None:
            usage = response_usage.model_dump()
            usage["input_tokens"] = usage.pop("prompt_tokens")
            usage["output_tokens"] = usage.pop("completion_tokens")
            for field in (
                "input_tokens",
                "output_tokens",
                "total_tokens",
                "cache_read_input_tokens",
                "cache_creation_input_tokens",
            ):
                if usage.get(field) is None:
                    usage[field] = 0
            # litellm computes the per-provider cost in its post-call
            # logging path and stashes it on ``_hidden_params`` — handles
            # cache reads/writes, reasoning tokens, region/tier multipliers
            # that the naive input_cost_per_token math can't. Falls back to
            # ``None`` for providers/models without a rate entry.
            hidden_params = getattr(response, "_hidden_params", None) or {}
            response_cost = hidden_params.get("response_cost")
            if response_cost is not None:
                usage["cost_usd"] = float(response_cost)

        if isinstance(choice, litellm.types.utils.StreamingChoices):
            raise TypeError("Streaming choices are not supported")

        tool_calls: list[dict[str, t.Any]] | None = None
        if (
            isinstance(choice.message, litellm.types.utils.Message)
            and choice.message.tool_calls is not None
            and all(
                isinstance(call, litellm.types.utils.ChatCompletionMessageToolCall)
                for call in choice.message.tool_calls
            )
        ):
            tool_calls = [call.model_dump() for call in choice.message.tool_calls]

        extra: dict[str, t.Any] = {"response_id": response.id}
        if hasattr(response, "provider"):
            extra["provider"] = response.provider
        if (
            hasattr(choice.message, "provider_specific_fields")
            and choice.message.provider_specific_fields is not None
        ):
            extra.update(choice.message.provider_specific_fields)
        if (
            hasattr(choice.message, "reasoning_content")
            and choice.message.reasoning_content is not None
        ):
            extra["reasoning_content"] = choice.message.reasoning_content
        if (
            hasattr(choice.message, "thinking_blocks")
            and choice.message.thinking_blocks is not None
        ):
            extra["thinking_blocks"] = choice.message.thinking_blocks

        message = Message(
            role="assistant",
            content=[],
            tool_calls=tool_calls,
        )

        if choice.message.content is not None:
            # Check for lazy litellm handling
            # https://github.com/BerriAI/litellm/blob/0f9ebc23a5c1e386195267dfc8d91ba7169c4508/litellm/llms/vertex_ai/gemini/vertex_and_google_ai_studio_gemini.py#L578C1-L599C48
            if match := vertex_image_pattern.match(choice.message.content):
                encoded_data = match.group(1)
                choice.message.content = choice.message.content.replace(encoded_data, "").strip()
                message.content_parts.append(ContentImageUrl.from_url(encoded_data))

            message.content_parts.append(
                ContentText(
                    text=choice.message.content,
                ),
            )

        if hasattr(choice.message, "audio") and choice.message.audio is not None:
            message.content_parts.append(
                ContentAudioInput.from_bytes(
                    base64.b64decode(choice.message.audio.data),
                    transcript=choice.message.audio.transcript,
                ),
            )

        return GeneratedMessage(
            message=message,
            stop_reason=choice.finish_reason or "unknown",
            usage=usage,
            extra=extra,
        )

    def _parse_text_completion_response(
        self,
        response: "TextCompletionResponse",
    ) -> GeneratedText:
        choice = response.choices[-1]
        usage = None
        if response.usage is not None:
            usage_dict = response.usage.model_dump()
            usage = Usage(
                input_tokens=usage_dict.get("prompt_tokens", 0),
                output_tokens=usage_dict.get("completion_tokens", 0),
                total_tokens=usage_dict.get("total_tokens", 0),
            )
        return GeneratedText(
            text=choice["text"],
            stop_reason=choice.finish_reason,
            usage=usage,
            extra={"response_id": response.id},
        )

    @with_fixups(*g_fixups)
    async def _generate_message(
        self,
        messages: t.Sequence[Message],
        params: GenerateParams,
    ) -> GeneratedMessage:
        import litellm

        async with self.semaphore:
            # if params.max_tokens is None:
            #     params.max_tokens = get_max_tokens_for_model(self.model)
            await self._ensure_delay_between_requests()

            acompletion = litellm.acompletion
            if self._wrap is not None:
                acompletion = self._wrap(acompletion)

            merged = self.params.merge_with(params).to_dict()

            # When reasoning_effort is set for Anthropic models, litellm enables
            # extended thinking with a budget_tokens that may exceed max_tokens.
            # Ensure max_tokens is large enough to accommodate the thinking budget.
            if "reasoning_effort" in merged and (
                merged.get("max_tokens") is None or merged.get("max_tokens", 0) < 16000
            ):
                merged["max_tokens"] = 16000

            logger.debug(
                "LiteLLM request | model={} | params={}",
                self.model,
                {k: v for k, v in merged.items() if k not in ("tools",)},
            )

            compatibility_flags = _compatibility_flags_for_model(self.model)
            response = await acompletion(
                model=self.model,
                messages=[
                    message.to_openai(compatibility_flags=compatibility_flags)
                    for message in messages
                ],
                api_key=self.api_key,
                **merged,
            )

            self._last_request_time = datetime.datetime.now(tz=datetime.UTC)

            if response is None:
                raise ProcessingError("LiteLLM returned a None response")

            choices = response.choices
            logger.debug(
                "Raw LiteLLM response | model={} | usage={} | message_keys={}",
                self.model,
                getattr(response, "usage", None),
                list(choices[-1].message.__dict__) if choices else [],
            )

            generated = self._parse_model_response(response)
            self._trace_generation_meta(generated)
            self._warn_on_input_truncation(list(messages), generated)
            return generated

    async def _generate_text(self, text: str, params: GenerateParams) -> GeneratedText:
        import litellm

        async with self.semaphore:
            # if params.max_tokens is None:
            #     params.max_tokens = get_max_tokens_for_model(self.model)
            await self._ensure_delay_between_requests()

            atext_completion = litellm.atext_completion
            if self._wrap is not None:
                atext_completion = self._wrap(atext_completion)

            response = await atext_completion(
                prompt=text,
                model=self.model,
                api_key=self.api_key,
                **self.params.merge_with(params).to_dict(),
            )

            self._last_request_time = datetime.datetime.now(tz=datetime.UTC)
            return self._parse_text_completion_response(response)

    async def generate_messages(
        self,
        messages: t.Sequence[t.Sequence[Message]],
        params: t.Sequence[GenerateParams],
    ) -> t.Sequence[GeneratedMessage | BaseException]:
        coros = [
            self._generate_message(_messages, _params)
            for _messages, _params in zip(messages, params, strict=True)
        ]
        generated = await asyncio.gather(*coros, return_exceptions=True)

        for i, (_messages, response) in enumerate(zip(messages, generated, strict=True)):
            trace_messages(_messages, f"Messages {i + 1}/{len(messages)}")
            if isinstance(response, BaseException):
                trace_str(str(response), f"Response {i + 1}/{len(messages)}")
            else:
                trace_messages([response], f"Response {i + 1}/{len(messages)}")

        return generated

    async def generate_texts(
        self,
        texts: t.Sequence[str],
        params: t.Sequence[GenerateParams],
    ) -> t.Sequence[GeneratedText | BaseException]:
        coros = [
            self._generate_text(text, _params) for text, _params in zip(texts, params, strict=True)
        ]
        generated = await asyncio.gather(*coros, return_exceptions=True)

        for i, (text, response) in enumerate(zip(texts, generated, strict=True)):
            trace_str(text, f"Text {i + 1}/{len(texts)}")
            trace_str(response, f"Response {i + 1}/{len(texts)}")

        return generated


def get_max_tokens_for_model(model: str) -> int | None:
    """
    Try to get the maximum number of tokens for a model from litellm mappings.

    Args:
        model: The model name.

    Returns:
        The maximum number of tokens.
    """
    import litellm

    while model not in litellm.model_cost:
        if "/" not in model:
            return None
        model = "/".join(model.split("/")[1:])

    return litellm.model_cost[model].get("max_tokens")
