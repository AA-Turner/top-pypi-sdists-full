import dataclasses
from dataclasses import dataclass, field
from typing import Any, Optional, Union

from matrx_utils import vcprint
from openai.types.responses import (
    ResponseOutputItem as OpenAIResponseOutputItem,
)

from .enums import Role
from .extra_config import (
    CodeExecutionContent,
    CodeExecutionResultContent,
    WebSearchCallContent,
)
from .media_config import (
    AudioContent,
    ImageContent,
    VideoContent,
    YouTubeVideoContent,
    reconstruct_media_content,
)
from .structured_input_config import (
    STRUCTURED_INPUT_TYPE_MAP,
    _StructuredInputBase,
    reconstruct_structured_input,
)
from .tool_result_guard import (
    LAYER_SANITIZE,
    report_nonadjacent_tool_uses,
    report_tool_result_duplicates,
    result_block_is_empty,
)
from .tools_config import ToolCallContent, ToolResultContent
from .unified_content import (
    TextContent,
    ThinkingContent,
    UnifiedContent,
    reconstruct_content,
)

# Marker embedded in a tool_result truncated by the Layer-2 absolute-ceiling pass.
# Used to make that pass idempotent (a block already carrying it is skipped, so the
# ceiling alarm fires once per event, not once per provider call).
_CEILING_TRUNCATION_MARKER = "TRUNCATED AT THE ABSOLUTE SIZE CEILING"


class MessageSanitizationError(ValueError):
    pass


def _raise_sanitized_empty(
    *,
    pass_name: str,
    messages: list["UnifiedMessage"],
) -> None:
    shapes = [
        {
            "id": msg.id,
            "role": str(msg.role),
            "visible": getattr(msg, "is_visible_to_model", True),
            "content_types": [type(content).__name__ for content in msg.content],
        }
        for msg in messages[:20]
    ]
    vcprint(
        data={
            "emptying_pass": pass_name,
            "input_message_count": len(messages),
            "message_shapes": shapes,
            "shape_list_truncated": len(messages) > len(shapes),
        },
        title="🚨 MessageList.sanitize collapsed a non-empty conversation",
        color="red",
    )
    raise MessageSanitizationError(
        "MessageList.sanitize refused to collapse a non-empty conversation to "
        f"zero provider messages (emptying_pass={pass_name}, "
        f"input_message_count={len(messages)})."
    )


@dataclass
class UnifiedMessage:
    """Pure message - no AI Matrix specifics"""

    role: str
    content: list[UnifiedContent] = field(default_factory=list)
    # cx_message.id (UUID) ONLY — set for messages loaded from the DB or for
    # rows whose UUID was deliberately reserved (executor reservation channel /
    # handoff synthetic row). NEVER a provider response id: those live on
    # TokenUsage.response_id. A provider id stamped here once became a
    # cx_message PK and 500'd the turn (2026-07-02).
    id: str | None = None
    name: str | None = None
    timestamp: int | None = None
    status: str = "active"
    # Whether this message is sent to the MODEL. False = persisted and shown to
    # the user (a failed turn, or a system-compacted message) but NEVER replayed
    # to the provider. Carried from cx_message.is_visible_to_model so the
    # provider-payload backstop (MessageList.sanitize) enforces the
    # "hidden from agent" invariant even for any path that bypasses
    # rebuild_conversation_messages. Default True (new/synthetic messages are
    # visible). See docs/persistence/STATUS_AND_ERROR_FIELDS.md.
    is_visible_to_model: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    # Position within the source conversation (cx_message.position). Carried
    # through ``from_cx_message`` so downstream consumers (turn counters,
    # context trimmers, debug panels) can reason about ordering without
    # re-querying the DB. Optional because freshly-constructed in-memory
    # messages (e.g. a new user turn before persistence) don't have one yet.
    position: int | None = None

    @staticmethod
    def _filter_kwargs(cls_obj: Any, item: dict[str, Any]) -> dict[str, Any]:
        """Keep only keys that match the dataclass' declared fields.

        Client payloads often include transport-level extras like `details`,
        `localId`, `subCategory`, etc. that are not part of the content model.
        Passing them through as **kwargs would raise TypeError.
        """
        try:
            allowed = {f.name for f in dataclasses.fields(cls_obj)}
        except TypeError:
            return item
        return {k: v for k, v in item.items() if k in allowed}

    @staticmethod
    def parse_content(content_data: str | list[Any]) -> list[UnifiedContent]:
        """Parse content data (string or list) into a list of UnifiedContent objects.

        Can be used standalone or by from_dict and other methods.
        """
        parsed_content: list[UnifiedContent] = []
        _filter = UnifiedMessage._filter_kwargs

        if isinstance(content_data, str):
            # Simple string content
            parsed_content = [TextContent(text=content_data)]
        elif isinstance(content_data, list):
            # Array of content objects
            for item in content_data:
                # vcprint(item, "--Item", color="green")
                if isinstance(item, str):
                    parsed_content.append(TextContent(text=item))
                elif isinstance(item, dict):
                    content_type = item.get("type", "text")
                    if (
                        content_type == "text"
                        or content_type == "input_text"
                        or content_type == "output_text"
                    ):
                        # ONE DESERIALIZER (see the canonical-types note in
                        # the tool_call branch below): reconstruct_content
                        # owns citation normalization + metadata preservation.
                        parsed_content.append(reconstruct_content({**item, "type": "text"}))
                    elif (
                        content_type == "image"
                        or content_type == "input_image"
                        or content_type == "output_image"
                    ):
                        # Normalize image_url to url if present
                        if "image_url" in item and "url" not in item:
                            item = {**item, "url": item["image_url"]}
                            item.pop("image_url", None)
                        parsed_content.append(ImageContent(**_filter(ImageContent, item)))
                    elif (
                        content_type == "audio"
                        or content_type == "input_audio"
                        or content_type == "output_audio"
                    ):
                        if "audio_url" in item and "url" not in item:
                            item = {**item, "url": item["audio_url"]}
                            item.pop("audio_url", None)
                        parsed_content.append(AudioContent(**_filter(AudioContent, item)))
                    elif (
                        content_type == "video"
                        or content_type == "input_video"
                        or content_type == "output_video"
                    ):
                        if "video_url" in item and "url" not in item:
                            item = {**item, "url": item["video_url"]}
                            item.pop("video_url", None)
                        parsed_content.append(VideoContent(**_filter(VideoContent, item)))
                    elif content_type == "youtube_video":
                        if "youtube_url" in item and "url" not in item:
                            item = {**item, "url": item["youtube_url"]}
                            item.pop("youtube_url", None)
                        parsed_content.append(
                            YouTubeVideoContent(**_filter(YouTubeVideoContent, item))
                        )
                    elif (
                        content_type == "document"
                        # "input_document" is overloaded: a FILE attachment (PDF/docx,
                        # has a url/file payload) AND the cloud-document resource block
                        # (carries document_ids → handled by the structured-input path
                        # below). Disambiguate by payload so each routes correctly.
                        or (content_type == "input_document" and "document_ids" not in item)
                        or content_type == "input_file"
                        or content_type == "output_document"
                        or content_type == "pdf"
                        or content_type == "file"
                    ):
                        if "file_url" in item and "url" not in item:
                            item = {**item, "url": item["file_url"]}
                            item.pop("file_url", None)
                        elif "document_url" in item and "url" not in item:
                            item = {**item, "url": item["document_url"]}
                            item.pop("document_url", None)
                        # Normalize the wire alias, then delegate to the ONE
                        # media deserializer. It reconciles stale generic
                        # "document" labels against a definitive MIME before
                        # provider routing (e.g. image/jpeg → ImageContent).
                        reconstructed = reconstruct_media_content(
                            {**item, "type": "media", "kind": "document"}
                        )
                        if reconstructed is not None:
                            parsed_content.append(reconstructed)
                    elif content_type == "media":
                        # Unified storage format: dispatch by kind
                        reconstructed = reconstruct_media_content(item)
                        if reconstructed is not None:
                            parsed_content.append(reconstructed)
                    # ── ONE DESERIALIZER FOR THE CANONICAL STORAGE TYPES ──
                    # These branches used to rebuild the dataclass themselves via
                    # ``_filter``, which keeps ONLY keys whose name matches a
                    # dataclass field — so every storage key that is spelled
                    # differently (``call_id`` → ``id``) or needs decoding
                    # (``<key>__b64`` → bytes) was SILENTLY DROPPED. That made
                    # ``parse_content`` a second, drifting deserializer of the
                    # same shape ``reconstruct_content`` already owns, and the
                    # drift caused three separate production incidents in three
                    # days: citations erased (2026-07-16), tool_use ``call_id``
                    # erased → Anthropic 400 on every later turn (2026-07-18),
                    # and Gemini's ``thoughtSignature`` erased → 400 on replay.
                    # There is now ONE deserializer; these branches only
                    # normalize wire aliases and delegate to it.
                    elif content_type == "tool_call" or content_type == "function_call":
                        parsed_content.append(reconstruct_content({**item, "type": "tool_call"}))
                    elif (
                        content_type == "tool_result"
                        or content_type == "function_result"
                        or content_type == "tool_call_result"
                    ):
                        parsed_content.append(reconstruct_content({**item, "type": "tool_result"}))
                    elif content_type == "thinking" or content_type == "reasoning":
                        parsed_content.append(reconstruct_content({**item, "type": "thinking"}))
                    # These two were the last _filter users among the canonical
                    # storage types — the exact antipattern the comment above
                    # names. They also cross a spelling boundary: the dataclass
                    # discriminator is "code_execution" while to_storage_dict
                    # writes "code_exec", so normalize the alias and delegate,
                    # the same way the tool_call branch does.
                    elif content_type in ("code_execution", "code_exec"):
                        parsed_content.append(reconstruct_content({**item, "type": "code_exec"}))
                    elif content_type in ("code_execution_result", "code_result"):
                        parsed_content.append(reconstruct_content({**item, "type": "code_result"}))
                    elif content_type in STRUCTURED_INPUT_TYPE_MAP:
                        obj = reconstruct_structured_input(item)
                        if obj is not None:
                            parsed_content.append(obj)
                    else:
                        vcprint(
                            item,
                            f"WARNING: Unknown content type: {content_type}",
                            color="red",
                        )

        return parsed_content

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UnifiedMessage":
        """Create UnifiedMessage from dictionary (e.g., from API)"""
        content_data = data.get("content", [])
        parsed_content = cls.parse_content(content_data)

        return cls(
            role=data.get("role", "user"),
            content=parsed_content,
            id=data.get("id"),
            name=data.get("name"),
            timestamp=data.get("timestamp"),
            status=data.get("status", "active"),
            metadata=dict(data.get("metadata") or {}),
            position=data.get("position"),
        )

    @classmethod
    def from_cx_message(cls, message) -> "UnifiedMessage":
        """Create UnifiedMessage from CxMessage"""
        content = [reconstruct_content(item) for item in (message.content or [])]

        return cls(
            role=message.role,
            content=content,
            id=message.id,
            timestamp=message.created_at.isoformat() if message.created_at else None,
            status=message.status,
            is_visible_to_model=bool(getattr(message, "is_visible_to_model", True)),
            metadata=dict(message.metadata or {}),
            position=getattr(message, "position", None),
        )

    @classmethod
    def from_openai_item(cls, item: OpenAIResponseOutputItem) -> Optional["UnifiedMessage"]:
        content = []
        assigned_role = "output"
        item_type = item.type

        if item_type == "message":
            assigned_role = "assistant"
            for content_item in item.content or []:
                content_type = content_item.type
                if content_type == "output_text":
                    content.append(TextContent.from_openai(content_item, item.id))
                else:
                    vcprint(
                        content_item,
                        f"WARNING: Unknown OpenAI content item type: {content_type}",
                        color="yellow",
                    )
        elif item_type == "reasoning":
            content.append(ThinkingContent.from_openai(item))
        elif item_type == "function_call":
            assigned_role = "tool"
            new_content = ToolCallContent.from_openai(item)
            # rich.print("\n\n[UNIFIED MESSAGE FROM OPENAI ITEM] NEW TOOL CALL CONTENT FROM OPENAI ITEM", new_content)
            content.append(new_content)
        elif item_type == "web_search_call":
            assigned_role = "tool"
            content.append(WebSearchCallContent.from_openai(item))
        else:
            vcprint(item, f"WARNING: Unknown OpenAI item type: {item_type}", color="red")

        return cls(
            id=item.id,
            role=assigned_role,
            content=content,
        )

    @classmethod
    def from_openai_modified(cls, items: list[dict[str, Any]]) -> Optional["UnifiedMessage"]:
        content_blocks = []
        final_merged_id = "openai_merged"

        for item in items:
            print("\n============= [UNIFIED MESSAGE FROM OPENAI MODIFIED] =================\n")
            vcprint(item, "[UNIFIED MESSAGE FROM OPENAI MODIFIED] Item", color="cyan")
            item_id = item.get("id")
            item_type = item.get("item_type")
            internal_item_content = item.get("content")
            final_merged_id += "_" + item_id

            if item_type == "message":
                new_content = TextContent.from_openai_modified(item)
                vcprint(
                    new_content, "[UNIFIED MESSAGE FROM OPENAI MODIFIED] New Content", color="cyan"
                )
                content_blocks.append(new_content)

            elif item_type == "reasoning":
                new_content = ThinkingContent.from_openai(internal_item_content)
                vcprint(
                    new_content, "[UNIFIED MESSAGE FROM OPENAI MODIFIED] New Content", color="cyan"
                )
                content_blocks.append(new_content)
            elif item_type == "function_call":
                new_content = ToolCallContent.from_openai(internal_item_content)
                vcprint(
                    new_content, "[UNIFIED MESSAGE FROM OPENAI MODIFIED] New Content", color="cyan"
                )
                content_blocks.append(new_content)
            elif item_type == "web_search_call":
                new_content = WebSearchCallContent.from_openai(internal_item_content)
                vcprint(
                    new_content, "[UNIFIED MESSAGE FROM OPENAI MODIFIED] New Content", color="cyan"
                )
                content_blocks.append(new_content)
            else:
                vcprint(item, f"WARNING: Unknown OpenAI item type: {item_type}", color="red")

        return cls(
            id=final_merged_id,
            role="assistant",
            content=content_blocks,
        )

    @classmethod
    def from_anthropic_content(
        cls, role: str, content: list[dict[str, Any]]
    ) -> Optional["UnifiedMessage"]:
        """Create UnifiedMessage from Anthropic content blocks"""
        content_blocks = []

        for block in content:
            block_type = block.get("type")
            if block_type == "text":
                content_blocks.append(TextContent.from_anthropic(block))
            elif block_type == "tool_use":
                content_blocks.append(ToolCallContent.from_anthropic(block))
            elif block_type == "thinking":
                content_blocks.append(ThinkingContent.from_anthropic(block))
            elif block_type in {"server_tool_use", "web_search_tool_result"}:
                # Provider-hosted tool state. It is preserved in raw_response
                # and, on pause_turn, replayed directly to Anthropic by the
                # provider adapter. Never turn it into ToolCallContent or the
                # local executor would try to dispatch a provider-owned call.
                continue
            else:
                vcprint(
                    block,
                    "WARNING: Unknown Anthropic content block type",
                    color="yellow",
                )

        # No id: UnifiedMessage.id is cx_message.id only. The message earns its
        # UUID through the executor's reservation channel or at persist time.
        return cls(role=role, content=content_blocks)

    def to_google_content(self) -> dict[str, Any] | None:
        """Convert message to Google Gemini content format.

        Returns dict with 'role' and 'parts', or None if no valid parts.
        """
        # Convert all content items using their to_google() methods
        parts = []
        for content in self.content:
            if isinstance(content, ToolResultContent):
                parts.extend(content.to_google_parts())
            else:
                part = content.to_google()
                if part:  # Only add if conversion succeeded
                    parts.append(part)

        if not parts:
            return None

        # Map role to Google's expected values
        if self.role == "assistant":
            google_role = "model"
        elif self.role in ("user", "tool"):
            google_role = "user"
        else:
            raise ValueError(
                f"Unknown role '{self.role}'. Valid roles are: 'user', 'assistant', 'tool'"
            )

        return {
            "role": google_role,
            "parts": parts,
        }

    def to_openai_items(
        self,
    ) -> list[dict[str, Any]] | dict[str, Any] | None:
        """
        Convert message to OpenAI Responses API format items.

        Returns a list because:
        - Tool calls become separate function_call items
        - Thinking becomes separate reasoning items
        - Tool results become function_call_output items
        - Regular messages stay as message items

        Assistant messages that originated from the Responses API (i.e. have an id
        like "msg_...") must be serialized as raw output-objects:
            {"type": "message", "role": "assistant", "id": "...", "content": [...]}
        rather than the chat-style wrapper {"role": "assistant", "content": [...]}.
        This is required so that a preceding "reasoning" item and its paired
        "message" item are both flat output-objects, satisfying OpenAI's rule that
        a reasoning item must be immediately followed by its associated output item.
        """

        converted = []
        text_content_id = None
        for content in self.content:
            result = None
            if isinstance(content, TextContent):
                result = content.to_openai(role=self.role)
                text_content_id = content.id
            else:
                result = content.to_openai()

            if result is not None:
                converted.append(result)

        if converted and self.role in (Role.OUTPUT, Role.TOOL):
            vcprint(
                converted,
                "[UNIFIED MESSAGE] to_openai_items converted output or tool role",
                color="yellow",
                verbose=True,
            )
            return converted  # Returns list: [item1, item2, item3] & without role, etc.

        elif converted and self.role == Role.ASSISTANT and text_content_id:
            # Prior Responses API output — must be a raw output-object so it is
            # adjacent to any preceding reasoning item in the input array.
            return [
                {
                    "type": "message",
                    "role": "assistant",
                    "id": text_content_id,
                    "content": converted,
                }
            ]

        elif converted:
            return {"role": self.role, "content": converted}
        else:
            vcprint(
                converted,
                "[UNIFIED MESSAGE] to_openai_items converted None role",
                color="red",
                verbose=True,
            )
            return None

    def to_openai_items_modified(self) -> list[dict[str, Any]]:
        """
        Convert message to OpenAI Responses API format as a flat list of top-level
        input items. Each content block becomes its own item at the input array level.

        OpenAI Responses API expects:
        - reasoning items as top-level: {"type": "reasoning", "id": "...", ...}
        - function_call items as top-level: {"type": "function_call", "id": "...", ...}
        - function_call_output as top-level: {"type": "function_call_output", ...}
        - web_search_call as top-level: {"type": "web_search_call", "id": "...", ...}
        - message items wrapping text: {"type": "message", "role": "...", "content": [...]}
        - user input as: {"role": "user", "content": [...]}

        Non-OpenAI thinking content (no signature) is included as input_text so
        the reasoning context is preserved. Assistant text from any provider is
        always emitted — with an id-bearing message wrapper when available, or a
        plain role-based wrapper otherwise.
        """
        items: list[dict[str, Any]] = []
        text_parts: list[dict[str, Any]] = []
        tool_media_parts: list[dict[str, Any]] = []
        text_content_id: str | None = None

        for content in self.content:
            if isinstance(content, ThinkingContent):
                if content.provider == "openai" and content.signature:
                    items.append(
                        {
                            "type": "reasoning",
                            "id": content.id,
                            "summary": content.summary,
                            "encrypted_content": content.signature,
                        }
                    )
                elif content.text:
                    text_parts.append({"type": "input_text", "text": content.text})

            elif isinstance(content, ToolCallContent):
                item = content.to_openai()
                if content.metadata.get("status"):
                    item["status"] = content.metadata["status"]
                items.append(item)

            elif isinstance(content, ToolResultContent):
                # Delegate to ToolResultContent.to_openai() so typed-block
                # tool results (ImageContent + TextContent from image-bearing
                # tools like take_screenshot) are serialized through the
                # canonical _is_typed_block_list path instead of crashing
                # json.dumps on a dataclass instance.
                items.append(content.to_openai())
                for media_block in content.extract_media_blocks():
                    media_part = media_block.to_openai()
                    if isinstance(media_part, dict):
                        tool_media_parts.append(media_part)

            elif isinstance(content, WebSearchCallContent):
                item = {
                    "type": "web_search_call",
                    "id": content.id,
                    "status": content.status,
                }
                if content.action:
                    item["action"] = content.action
                items.append(item)

            elif isinstance(content, TextContent):
                text_type = "output_text" if self.role == Role.ASSISTANT else "input_text"
                text_parts.append({"type": text_type, "text": content.text})
                if not text_content_id and content.id:
                    text_content_id = content.id

            else:
                result = content.to_openai()
                if result is None:
                    continue
                # Media blocks (ImageContent → input_image, DocumentContent →
                # input_file) are CONTENT-level parts: they belong inside a
                # message's `content` array, NOT as top-level Responses API
                # input items. Appending them at the top level makes OpenAI
                # reject the whole request with
                #   Invalid value: 'input_image'. Supported values are: ...
                # Fold them into the same content array the text parts use.
                if isinstance(result, dict) and result.get("type") in (
                    "input_image",
                    "input_file",
                    "input_text",
                ):
                    text_parts.append(result)
                else:
                    items.append(result)

        if text_parts:
            if self.role == Role.ASSISTANT and text_content_id:
                items.append(
                    {
                        "type": "message",
                        "role": "assistant",
                        "id": text_content_id,
                        "content": text_parts,
                    }
                )
            elif self.role == Role.ASSISTANT:
                items.append(
                    {
                        "role": "assistant",
                        "content": text_parts,
                    }
                )
            elif self.role in (Role.USER, Role.SYSTEM, Role.DEVELOPER):
                role_str = self.role.value if hasattr(self.role, "value") else self.role
                items.append(
                    {
                        "role": role_str,
                        "content": text_parts,
                    }
                )

        if tool_media_parts:
            items.append({"role": "user", "content": tool_media_parts})

        return items

    def to_anthropic_blocks(self) -> list[dict[str, Any]]:
        """
        Convert message content to Anthropic format blocks.

        Returns list of content blocks for Anthropic messages.
        """
        # Sanity check - should never happen in UnifiedConfig
        if self.role in (Role.SYSTEM, Role.DEVELOPER, "system", "developer"):
            vcprint(
                "[WARNING] System/developer message found in UnifiedMessage.to_anthropic_blocks(). This should not happen!",
                color="red",
            )
            return []

        content_blocks = []
        for content in self.content:
            converted = content.to_anthropic()
            if converted:
                content_blocks.append(converted)

        return content_blocks

    def replace_variables(self, variables: dict[str, Any]) -> None:
        """Substitute {{variable_name}} patterns in all content blocks.

        - TextContent: substitution is in-place (no return value).
        - Media content (Image / Audio / Video / Document / YouTubeVideo):
          substitutes into the url/file_id/file_uri fields then re-routes
          to the canonical MediaRef field per the value's classification
          (UUID → file_id, s3:// → file_uri, otherwise url). Returns True
          when the block carried only a `{{var}}` template that the user
          left unfilled — in that case we DROP the block entirely so we
          don't pass an empty image/video/etc to the provider.

        Other content types without a ``replace_variables`` method are
        passed through untouched.
        """
        from matrx_ai.config.media_config import (
            AudioContent,
            DocumentContent,
            ImageContent,
            VideoContent,
            YouTubeVideoContent,
        )

        kept: list[Any] = []
        for content in self.content:
            if isinstance(content, TextContent):
                # TextContent now also returns drop-bool: role-tagged
                # text (e.g. negative_prompt) that resolved to empty
                # gets dropped so we don't pass empty role-text to
                # providers. Untagged TextContent always returns False.
                drop = bool(content.replace_variables(variables))
                if not drop:
                    kept.append(content)
            elif isinstance(
                content,
                ImageContent | AudioContent | VideoContent | DocumentContent | YouTubeVideoContent,
            ):
                drop = content.replace_variables(variables)
                if not drop:
                    kept.append(content)
                # else: skipped — optional media slot the user didn't fill
            elif hasattr(content, "replace_variables"):
                # Future content types that opt into substitution. Honor
                # the same drop-on-True contract.
                drop = content.replace_variables(variables)
                if not drop:
                    kept.append(content)
            else:
                kept.append(content)
        self.content = kept

    def to_storage_dict(self) -> dict[str, Any]:
        """Serialize to storage format for database persistence (cx_message row).

        Returns dict with 'role', 'status', and 'content' (list of storage-format blocks).
        Content blocks use each item's to_storage_dict() for the cx_message.content JSONB.
        """
        content_storage_dicts = [
            content.to_storage_dict()
            for content in self.content
            if not (isinstance(content, TextContent) and content.is_ephemeral_only())
        ]
        # vcprint(
        #     content_storage_dicts,
        #     "[UnifiedMessage] Content Storage Dicts",
        #     color="yellow",
        # )
        result: dict[str, Any] = {
            "role": self.role.value if hasattr(self.role, "value") else self.role,
            "content": content_storage_dicts,
        }
        # Carry the existing cx_message.id (set for messages loaded from the DB)
        # so persistence can recognize an already-persisted message and not
        # re-INSERT it (retry duplicate-user-message guard).
        if self.id:
            result["id"] = self.id
        if self.status != "active":
            result["status"] = self.status
        # Round-trip message-level metadata to cx_message.metadata. from_cx_message
        # already loads it back; this completes the write side. Only emitted when
        # non-empty so plain messages don't clobber the column's {} default.
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    def get_output(self) -> str:
        """Get the OUTPUT (answer) text of the message.

        Thinking/reasoning is deliberately EXCLUDED. ``get_output()`` is the
        canonical "what did the model actually answer" accessor — it feeds
        ``get_last_output()`` → ``result.output``, which every non-streaming
        consumer parses (``parse_agent_output`` / ``extract_json``), persists as
        ``raw_response``, and emits as the ``STRUCTURED_OUTPUT`` event.

        ThinkingContent flattened into this string is the bug class that (a)
        surfaced reasoning as undifferentiated plain text and (b) let a JSON
        draft written INSIDE the model's thinking win over the real final
        answer during extraction. Reasoning is never output — read it via
        ``get_thinking()`` when you explicitly want it.
        """
        parts: list[str] = []
        for content in self.content:
            if isinstance(content, ThinkingContent):
                continue
            piece = content.get_output()
            if piece:
                parts.append(piece)
        return "".join(parts)

    def get_thinking(self) -> str:
        """Return the message's reasoning text only (ThinkingContent blocks),
        joined with blank lines. Empty string when the model did no visible
        thinking. The deliberate counterpart to ``get_output()`` for the rare
        caller that wants reasoning rather than the answer."""
        parts: list[str] = []
        for content in self.content:
            if isinstance(content, ThinkingContent):
                piece = content.get_output()
                if piece:
                    parts.append(piece)
        return "\n\n".join(parts)

    def attach_ephemeral(self, block: str, *, slot: str = "default") -> None:
        """Stage a platform block in front of this message's first TextContent.

        The block lands before the user's text, inside the ``<turn_context>``
        provenance frame (see TextContent.attach_ephemeral). ``slot`` names an
        independent block so multiple per-turn contributors accumulate instead of
        overwriting each other. If no TextContent exists, one is created and
        appended to the content list.
        """
        leased_item = getattr(self, "_ephemeral_text_content", None)
        if isinstance(leased_item, TextContent) and any(
            item is leased_item for item in self.content
        ):
            leased_item.attach_ephemeral(block, slot=slot)
            return
        for item in self.content:
            if isinstance(item, TextContent):
                item.attach_ephemeral(block, slot=slot)
                setattr(self, "_ephemeral_text_content", item)
                return
        new_tc = TextContent(text="")
        new_tc.attach_ephemeral(block, slot=slot, synthetic_carrier=True)
        self.content.append(new_tc)
        setattr(self, "_ephemeral_text_content", new_tc)

    def detach_ephemeral(self) -> None:
        """Remove the ephemeral block from this message's first TextContent."""
        had_leased_item = hasattr(self, "_ephemeral_text_content")
        leased_item = getattr(self, "_ephemeral_text_content", None)
        if had_leased_item:
            delattr(self, "_ephemeral_text_content")
        if isinstance(leased_item, TextContent):
            for index, item in enumerate(self.content):
                if item is leased_item:
                    if item.detach_ephemeral():
                        self.content.pop(index)
                    return
        if had_leased_item:
            return
        for item in self.content:
            if isinstance(item, TextContent):
                item.detach_ephemeral()
                return

    def is_ephemeral_only(self) -> bool:
        """True when this message exists solely to carry transient context."""
        if not getattr(self, "_ephemeral_synthetic_message", False):
            return False
        return not any(
            not (isinstance(content, TextContent) and content.is_ephemeral_only())
            for content in self.content
        )

    def strip_keep_fresh_blocks(self) -> list[UnifiedContent]:
        """Remove all keep_fresh=True structured input blocks from this message's content.

        Returns the stripped blocks so the caller can store them separately if needed.
        The resolved_text they injected into the provider payload is gone — only
        the block's structural definition (type, IDs, keep_fresh=True) is preserved
        via to_storage_dict(), which the persistence layer writes to the DB so
        the next turn knows to re-fetch them.
        """
        kept: list[UnifiedContent] = []
        stripped: list[UnifiedContent] = []
        for item in self.content:
            if isinstance(item, _StructuredInputBase) and item.keep_fresh:
                stripped.append(item)
            else:
                kept.append(item)
        self.content = kept
        return stripped


@dataclass
class MessageList:
    """
    Wrapper for list[UnifiedMessage] that encapsulates message-related logic.

    Provides list-like interface for backward compatibility while adding
    helper methods for common message operations.

    Core Principle:
    - System/Developer messages are NEVER stored here in UnifiedConfig
    - System instructions live in UnifiedConfig.system_instruction field
    - Only during API conversion do we create system/developer messages
    """

    _messages: list["UnifiedMessage"] = field(default_factory=list)
    _deferred_empty_messages: list["UnifiedMessage"] = field(
        default_factory=list,
        init=False,
        repr=False,
        compare=False,
    )
    _deferred_emptying_pass: str | None = field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self):
        """Normalize messages - convert dicts to UnifiedMessage objects."""
        normalized = []
        for msg in self._messages:
            if isinstance(msg, dict):
                normalized.append(UnifiedMessage.from_dict(msg))
            elif isinstance(msg, UnifiedMessage):
                normalized.append(msg)
            else:
                raise TypeError(f"Invalid message type: {type(msg)}")
        self._messages = normalized

    # ========================================================================
    # List Protocol Methods (for backward compatibility)
    # ========================================================================

    def __iter__(self):
        """Allow iteration: for msg in message_list"""
        return iter(self._messages)

    def __len__(self):
        """Allow len(): len(message_list)"""
        return len(self._messages)

    def __getitem__(self, index):
        """Allow indexing: message_list[0]"""
        return self._messages[index]

    def __setitem__(self, index, value):
        """Allow item assignment: message_list[0] = msg"""
        if isinstance(value, dict):
            value = UnifiedMessage.from_dict(value)
        self._messages[index] = value

    def append(self, message: Union["UnifiedMessage", dict[str, Any]]) -> None:
        """Append a message to the list"""
        if isinstance(message, dict):
            message = UnifiedMessage.from_dict(message)
        self._messages.append(message)

    def extend(self, messages: Union[list["UnifiedMessage"], "MessageList"]) -> None:
        """Extend with multiple messages"""
        if isinstance(messages, MessageList):
            self._messages.extend(messages._messages)
        else:
            for msg in messages:
                self.append(msg)

    def insert(self, index: int, message: Union["UnifiedMessage", dict[str, Any]]) -> None:
        """Insert a message at a specific position"""
        if isinstance(message, dict):
            message = UnifiedMessage.from_dict(message)
        self._messages.insert(index, message)

    def pop(self, index: int = -1) -> "UnifiedMessage":
        """Remove and return a message at index (default last)"""
        return self._messages.pop(index)

    def remove(self, message: "UnifiedMessage") -> None:
        """Remove first occurrence of message"""
        self._messages.remove(message)

    def clear(self) -> None:
        """Remove all messages"""
        self._messages.clear()

    # ========================================================================
    # Helper Methods (new functionality)
    # ========================================================================

    def filter_by_role(self, *roles: str) -> "MessageList":
        """Return new MessageList with only messages matching the given roles."""
        filtered = [msg for msg in self._messages if msg.role in roles]
        return MessageList(_messages=filtered)

    def exclude_roles(self, *roles: str) -> "MessageList":
        """Return new MessageList excluding messages with given roles."""
        filtered = [msg for msg in self._messages if msg.role not in roles]
        return MessageList(_messages=filtered)

    def has_role(self, role: str) -> bool:
        """Check if any message has the given role."""
        return any(msg.role == role for msg in self._messages)

    def get_last_by_role(self, role: str) -> Optional["UnifiedMessage"]:
        """Get the last message with the given role, or None."""
        for msg in reversed(self._messages):
            if msg.role == role:
                return msg
        return None

    def get_last_output(self) -> str:
        """Get the output of the last assistant message."""
        last_assistant_message = self.get_last_by_role(Role.ASSISTANT)
        if last_assistant_message:
            return last_assistant_message.get_output()
        return ""

    def count_by_role(self, role: str) -> int:
        """Count messages with the given role."""
        return sum(1 for msg in self._messages if msg.role == role)

    def attach_ephemeral_to_last_user(self, block: str, *, slot: str = "default") -> None:
        """Stage a platform block in front of the last user message.

        The block is placed before the user's text, inside the ``<turn_context>``
        provenance frame, so the user's actual request stays last and stays the only
        thing the model reads as the user speaking. If no user message exists, a
        runtime-only one is created.

        ``slot`` names an independent block: separate contributors (context engine,
        deferred-context manifest, skills, observational memory, safety notes) must
        each pass their own slot, or a later one silently deletes an earlier one's
        instructions. Reversible via detach_ephemeral_from_last_user(); synthetic
        carriers are omitted from storage even if persistence runs before detachment.
        """
        if not block:
            return
        last_user = getattr(self, "_ephemeral_user_message", None)
        if not isinstance(last_user, UnifiedMessage) or not any(
            message is last_user for message in self._messages
        ):
            last_user = self.get_last_by_role(Role.USER)
        if last_user is None:
            last_user = UnifiedMessage(role=Role.USER, content=[])
            setattr(last_user, "_ephemeral_synthetic_message", True)
            self._messages.append(last_user)
        last_user.attach_ephemeral(block, slot=slot)
        setattr(self, "_ephemeral_user_message", last_user)

    def detach_ephemeral_from_last_user(self) -> None:
        """Remove the ephemeral block from the last user message."""
        had_leased_message = hasattr(self, "_ephemeral_user_message")
        last_user = getattr(self, "_ephemeral_user_message", None)
        if had_leased_message:
            delattr(self, "_ephemeral_user_message")
        leased_message_is_present = isinstance(last_user, UnifiedMessage) and any(
            message is last_user for message in self._messages
        )
        if had_leased_message and not leased_message_is_present:
            return
        if not leased_message_is_present:
            last_user = self.get_last_by_role(Role.USER)
        if last_user is not None:
            last_user.detach_ephemeral()
            if getattr(last_user, "_ephemeral_synthetic_message", False):
                delattr(last_user, "_ephemeral_synthetic_message")
                if not last_user.content:
                    self._messages.remove(last_user)

    def merge_metadata_into_last_user(self, updates: dict[str, Any]) -> None:
        """Shallow-merge ``updates`` into the last user message's metadata.

        Unlike the ephemeral text block (which is stripped before persistence),
        message metadata IS persisted to cx_message.metadata and round-trips via
        from_cx_message. Use this to durably record per-turn facts ABOUT the user
        message (e.g. the context manifest that was presented) without touching
        the message text. No-op when there is no user message or no updates.
        """
        if not updates:
            return
        last_user = self.get_last_by_role(Role.USER)
        if last_user is not None:
            last_user.metadata.update(updates)

    def sanitize(self, *, allow_empty: bool = False) -> None:
        """Provider-agnostic message hygiene — the last-line guard before any
        provider call.

        ``allow_empty`` is for pre-execution config hydration, where an authored
        agent may legitimately contain only an empty user placeholder that will
        receive request input later. If sanitation collapses a non-empty list in
        that phase, the failure is retained as deferred state. A later strict
        call still raises unless real content has been added, so config loading
        can be permissive without allowing an empty payload to reach a provider.

        Passes, in order:

        1. **Visibility:** drop ``is_visible_to_model=False`` messages (failed
           turns, system-compacted messages) — the model must never see them.
        2. **Duplicate tool_result:** at most ONE ``tool_result`` may carry a
           given ``tool_use_id``. Two of them 400 the WHOLE request ("each
           tool_use must have a single result") and then kill every future turn
           of the conversation. A duplicate reaching here means an upstream
           invariant already broke (see ``conversation_rebuild`` synthetic
           pairing + a ``cx_tool_call.message_id = NULL`` row); we keep the
           best block, drop the rest, and SCREAM (red banner + durable app_log
           ERROR) rather than fail the turn.
        3. **Tool-pairing coherence (ADJACENCY-aware):** every ``tool_use`` MUST
           have its ``tool_result`` in the IMMEDIATELY-following message, and
           vice-versa — or the provider rejects the WHOLE request ("tool_use ids
           were found without tool_result blocks"). Two failure shapes: a tool
           that never produced a result (true orphan — delegated timeout, errored
           server tool, incomplete turn re-fed on retry), and the MIRROR of the
           duplicate-tool_result bug — one assistant message carrying tool_uses
           that belong to LATER turns (the surplus ids re-emitted, and adjacently
           paired, there). A naive "does a result exist anywhere" check passes the
           latter and 400s. We keep only the adjacently-paired copy, drop the rest
           (true orphan → yellow; non-adjacent duplicate → loud red + app_log), so
           a corrupted graph can't 400 every future turn.
        4. **Empty scrub:** drop empty/whitespace TextContent, then drop any
           message left with no content. (Anthropic rejects empty text blocks.)
        """
        original_messages = list(self._messages)

        if not allow_empty and not original_messages and self._deferred_emptying_pass is not None:
            _raise_sanitized_empty(
                pass_name=self._deferred_emptying_pass,
                messages=self._deferred_empty_messages,
            )

        # Pass 1 — visibility.
        visible: list[UnifiedMessage] = []
        for msg in self._messages:
            if not getattr(msg, "is_visible_to_model", True):
                vcprint(
                    f"[MessageList.sanitize] Dropped is_visible_to_model=False "
                    f"message from provider payload (role={msg.role!r}, id={msg.id!r}).",
                    color="yellow",
                )
                continue
            visible.append(msg)
        visibility_emptied = bool(original_messages and not visible)
        if visibility_emptied and not allow_empty:
            _raise_sanitized_empty(
                pass_name="visibility",
                messages=original_messages,
            )

        # Pass 1.5 — ID-LESS tool_use repair. Every guard below keys off
        # ``c.id`` — a tool_use with an EMPTY id is invisible to all pairing
        # passes and reaches the provider verbatim, where Anthropic 400s the
        # whole request ("tool_use.id: String should match pattern") while the
        # paired tool_result (which still carries the real id) gets dropped as
        # an "orphan". This happens when a rogue writer rewrites a cx_message
        # row through a serializer that drops call_id. Repair: adopt the id of
        # the unique matching tool_result in the adjacent following
        # non-assistant run (same name, id unclaimed by any other tool_use).
        # Ambiguous or unmatched → drop the block; an empty id must NEVER
        # reach a provider. Either way SCREAM — the DB row is corrupt.
        _claimed_ids: set[str] = {
            c.id for m in visible for c in m.content if isinstance(c, ToolCallContent) and c.id
        }
        for _i, _msg in enumerate(visible):
            _idless = [c for c in _msg.content if isinstance(c, ToolCallContent) and not c.id]
            if not _idless:
                continue
            # Adjacent window: the run of non-assistant messages after _i.
            _window_results: list[ToolResultContent] = []
            _j = _i + 1
            while _j < len(visible):
                _r = getattr(visible[_j], "role", None)
                if _r == "assistant" or getattr(_r, "value", None) == "assistant":
                    break
                _window_results.extend(
                    c for c in visible[_j].content if isinstance(c, ToolResultContent)
                )
                _j += 1
            for _call in _idless:
                _candidates = {
                    (r.tool_use_id or r.call_id)
                    for r in _window_results
                    if (r.tool_use_id or r.call_id)
                    and (r.tool_use_id or r.call_id) not in _claimed_ids
                    and (not _call.name or not r.name or r.name == _call.name)
                }
                if len(_candidates) == 1:
                    _adopted = next(iter(_candidates))
                    _call.id = _adopted
                    _claimed_ids.add(_adopted)
                    vcprint(
                        f"[MessageList.sanitize] 🚨 REPAIRED id-less tool_use "
                        f"{_call.name!r} by adopting adjacent tool_result id "
                        f"{_adopted!r}. The cx_message row lost its call_id to a "
                        f"rogue content rewrite — repair the row and find the "
                        f"writer (see reconstruct_content banner).",
                        color="red",
                    )
                else:
                    _msg.content = [c for c in _msg.content if c is not _call]
                    vcprint(
                        f"[MessageList.sanitize] 🚨 Dropped id-less tool_use "
                        f"{_call.name!r} — no unambiguous adjacent tool_result to "
                        f"adopt an id from ({len(_candidates)} candidates). An "
                        f"empty tool_use.id 400s the whole request at the "
                        f"provider; the row's call_id was destroyed upstream.",
                        color="red",
                    )

        # Pass 2 — EXCESS tool_result detection (provider-agnostic, lossless).
        # A tool_result is a true duplicate only when there are MORE results for
        # an id than there are tool_use blocks for that id. This is the key that
        # keeps it safe across providers that disagree about id uniqueness:
        #   • Anthropic mints globally-unique ``toolu_…`` ids — one tool_use per
        #     id — so a second result for that id IS the 400 bug; drop the excess.
        #   • Gemini REUSES deterministic call_ids across turns — N tool_use
        #     blocks share one id, each with its OWN legitimate result — so N
        #     results for that id is balanced, NOT a duplicate; keep them all.
        # We use the ids we already carry (call_id / tool_use_id) + their counts;
        # no new id is minted, and a legitimate reused-id result is never lost.
        tool_use_count: dict[str, int] = {}
        for msg in visible:
            for c in msg.content:
                if isinstance(c, ToolCallContent) and c.id:
                    tool_use_count[c.id] = tool_use_count.get(c.id, 0) + 1

        results_by_id: dict[str, list[ToolResultContent]] = {}
        total_tool_results = 0
        for msg in visible:
            for c in msg.content:
                if isinstance(c, ToolResultContent):
                    total_tool_results += 1
                    rid = c.tool_use_id or c.call_id
                    if rid:
                        results_by_id.setdefault(rid, []).append(c)
        drop_ids: set[int] = set()  # id() of the EXCESS blocks to remove
        dup_report: list[dict[str, Any]] = []
        for rid, blocks in results_by_id.items():
            allowed = tool_use_count.get(rid, 0)
            # No matching tool_use (allowed==0) → an orphan, handled by Pass 3.
            # results <= tool_uses → balanced/legitimate (incl. Gemini reuse).
            if allowed == 0 or len(blocks) <= allowed:
                continue
            # Keep the `allowed` best (non-empty beats an empty pointer stub,
            # stable otherwise); the rest are the excess that 400s the request.
            ordered = sorted(blocks, key=lambda b: result_block_is_empty(b.content))
            keeper_ids = {id(b) for b in ordered[:allowed]}
            for b in blocks:
                if id(b) not in keeper_ids:
                    drop_ids.add(id(b))
            dup_report.append(
                {
                    "tool_use_id": rid,
                    "name": next((b.name for b in blocks if b.name), None),
                    "count": len(blocks),
                    "dropped": len(blocks) - allowed,
                }
            )
        if dup_report:
            report_tool_result_duplicates(
                layer=LAYER_SANITIZE,
                duplicates=dup_report,
                total_tool_results=total_tool_results,
            )

        # Pass 3 prep — ADJACENCY-aware pairing. The provider's rule is strict:
        # an assistant's tool_results must be in the IMMEDIATELY-following message,
        # not merely SOMEWHERE. A global "does a result exist" check misses the
        # MIRROR of the duplicate-tool_result bug — one assistant message carrying
        # tool_uses that belong to LATER turns (the surplus ids re-emitted, and
        # adjacently paired, in those later turns). So:
        #   • next_results[i]    = surviving result ids in the message AFTER i.
        #   • a tool_use survives iff its id is in next_results[i] (adjacent).
        #   • surviving_use_ids  = ids of the tool_uses that survived adjacency; a
        #     tool_result survives iff its id is in THAT set (so a result whose
        #     only tool_use was dropped is dropped too — no orphan on either side).
        # results_for (global) only decides the VERDICT for a dropped tool_use:
        # result-exists-elsewhere ⇒ a corrupted DUPLICATE (scream); none ⇒ a plain
        # orphan (a tool that never produced a result).
        results_for: set[str] = set()
        result_ids_by_msg: list[set[str]] = []
        for msg in visible:
            per_msg: set[str] = set()
            for c in msg.content:
                if isinstance(c, ToolResultContent):
                    if c.tool_use_id:
                        results_for.add(c.tool_use_id)
                    if c.call_id:
                        results_for.add(c.call_id)
                    rid = c.tool_use_id or c.call_id
                    if rid and id(c) not in drop_ids:
                        per_msg.add(rid)
            result_ids_by_msg.append(per_msg)

        # The provider MERGES the consecutive run of tool/user messages after an
        # assistant into ONE turn, so an assistant's results may legitimately be
        # spread across that whole run (e.g. an empty pointer stub + a content-
        # bearing watchdog result in two separate tool messages) — but NEVER past
        # the next ASSISTANT message. The adjacency window for message i = the
        # union of surviving result ids in that following non-assistant run.
        def _is_assistant(m: UnifiedMessage) -> bool:
            r = getattr(m, "role", None)
            return r == "assistant" or getattr(r, "value", None) == "assistant"

        n = len(visible)
        window_after: list[set[str]] = [set() for _ in range(n)]
        for i in range(n):
            acc: set[str] = set()
            j = i + 1
            while j < n and not _is_assistant(visible[j]):
                acc |= result_ids_by_msg[j]
                j += 1
            window_after[i] = acc

        surviving_use_ids: set[str] = set()
        for i, msg in enumerate(visible):
            for c in msg.content:
                if isinstance(c, ToolCallContent) and c.id and c.id in window_after[i]:
                    surviving_use_ids.add(c.id)

        def _drop_reason(i: int, call_id: str) -> str:
            """Classify WHY a tool_use at index ``i`` lost adjacency.

            Two very different bugs land in the same drop, and calling both
            "duplicate" is how 251 of these alarms went unread before the
            2026-08-11 incident (the OpenAI translator emitting the assistant
            TEXT message between a tool_use and its result — see
            ``OpenAIResponseTranslator._build_unified_messages``):

            * ``separated``  — this id's result comes LATER with no competing
              tool_use for it in between: ONE call, ONE result, wrong ORDER.
              A producer put a message between them. Nothing is duplicated.
            * ``duplicated`` — another tool_use carrying the same id appears
              first, and THAT copy is the adjacently-paired one. This message
              absorbed a tool_use belonging to another turn.
            """
            for j in range(i + 1, n):
                for other in visible[j].content:
                    if isinstance(other, ToolCallContent) and other.id == call_id:
                        return "duplicated"
                if call_id in result_ids_by_msg[j]:
                    return "separated"
            return "duplicated"

        # Pass 2-drop + 3 + 4 — drop duplicate/orphan/non-adjacent tool blocks +
        # empty text, then drop any message left with no content.
        nonadjacent_uses: list[dict[str, Any]] = []
        orphan_blocks_dropped = 0
        empty_text_blocks_dropped = 0
        cleaned: list[UnifiedMessage] = []
        for i, msg in enumerate(visible):
            next_results = window_after[i]
            new_content: list[UnifiedContent] = []
            for c in msg.content:
                if isinstance(c, TextContent) and not c.text.strip():
                    empty_text_blocks_dropped += 1
                    continue
                if isinstance(c, ToolCallContent) and c.id:
                    # ADJACENCY: a tool_use is paired ONLY if its result is in the
                    # very next message. A result that exists but sits LATER (the
                    # same id re-emitted in a later, adjacently-paired turn) makes
                    # this a corrupted/duplicate tool_use — drop the non-adjacent
                    # copy; the adjacently-paired one survives.
                    if c.id not in next_results:
                        if c.id in results_for:
                            nonadjacent_uses.append(
                                {
                                    "tool_use_id": c.id,
                                    "name": getattr(c, "name", None),
                                    "reason": _drop_reason(i, c.id),
                                }
                            )
                        else:
                            vcprint(
                                f"[MessageList.sanitize] Dropped ORPHAN tool_use "
                                f"{c.id!r} (no matching tool_result) — satisfies the "
                                f"provider's tool_use/tool_result pairing rule.",
                                color="yellow",
                            )
                        orphan_blocks_dropped += 1
                        continue
                if isinstance(c, ToolResultContent):
                    # Drop an EXCESS duplicate tool_result (already reported in
                    # Pass 2) — keeps tool_use_count of them per id, so legitimate
                    # reused-id (Gemini) results are never lost.
                    if id(c) in drop_ids:
                        continue
                    _rid = c.tool_use_id or c.call_id
                    if _rid and _rid not in surviving_use_ids:
                        vcprint(
                            f"[MessageList.sanitize] Dropped ORPHAN tool_result "
                            f"{_rid!r} (no surviving matching tool_use).",
                            color="yellow",
                        )
                        orphan_blocks_dropped += 1
                        continue
                new_content.append(c)
            if new_content:
                msg.content = new_content
                cleaned.append(msg)
            else:
                vcprint(
                    f"[MessageList.sanitize] Dropped message with no remaining content (role={msg.role!r})",
                    color="yellow",
                )
        self._messages = cleaned
        if nonadjacent_uses:
            report_nonadjacent_tool_uses(layer=LAYER_SANITIZE, dropped=nonadjacent_uses)

        if original_messages and not cleaned:
            pass_name = (
                "visibility"
                if visibility_emptied
                else "tool_pairing"
                if orphan_blocks_dropped or nonadjacent_uses
                else "empty_scrub"
                if empty_text_blocks_dropped
                else "content_scrub"
            )
            if allow_empty:
                self._deferred_emptying_pass = pass_name
                self._deferred_empty_messages = original_messages
                vcprint(
                    f"[MessageList.sanitize] Deferred empty-conversation failure "
                    f"during config hydration (emptying_pass={pass_name}). A strict "
                    f"provider-bound sanitation pass will reject it unless runtime "
                    f"content is added.",
                    color="yellow",
                )
            else:
                _raise_sanitized_empty(
                    pass_name=pass_name,
                    messages=original_messages,
                )
        elif cleaned:
            self._deferred_emptying_pass = None
            self._deferred_empty_messages = []

        # Pass 5 — absolute size ceiling (Layer 2 of the tool-result size gate).
        self._enforce_absolute_tool_result_ceiling()

    def _enforce_absolute_tool_result_ceiling(self) -> None:
        """Hard-cap any single tool_result that exceeds the absolute ceiling.

        Source-agnostic backstop: the executor's Layer 1 caps results it
        dispatches, but a tool_result can reach the message list another way — a
        client-posted delegated result, a rebuilt-from-DB row, a raw /chat message
        whose tool_result content is a non-string dict/list. This pass enforces
        TOOL_RESULT_ABSOLUTE_CEILING_CHARS on EVERY tool_result (measuring a dict/
        list exactly as the provider serializer will — ``json.dumps`` — so a giant
        dict can't slip past) before any provider call, so a runaway payload (and
        its re-billing on every iteration) can never reach a provider. A tool may
        raise its own ceiling for one result via ``approved_max_chars``.

        Firing here is the LOUDEST alarm — it means Layer 1 was bypassed, or a
        self-managed tool authorized nothing yet went past the ceiling. Best-
        effort and defensive: a backstop must never break the turn it protects.
        Idempotent — a block already truncated by a prior pass is skipped, so the
        alarm fires once per event, not once per provider call.
        """
        import json as _json

        try:
            from matrx_ai.config.tools_config import _is_typed_block_list
            from matrx_ai.tools.output_caps import TOOL_RESULT_ABSOLUTE_CEILING_CHARS
        except Exception:
            return  # constant unavailable (import-order edge) — skip, never crash

        conv_id: str | None = None
        user_id: str | None = None
        try:
            from matrx_ai.context.app_context import try_get_app_context

            actx = try_get_app_context()
            if actx is not None:
                conv_id = getattr(actx, "conversation_id", None)
                user_id = getattr(actx, "user_id", None) or None
        except Exception:
            pass

        for msg in self._messages:
            for block in msg.content:
                if not isinstance(block, ToolResultContent):
                    continue
                content = block.content
                # Media typed blocks carry bounded references the model needs
                # intact — but SearchResultContent passages are unbounded TEXT
                # and must not ride the typed-list exemption (the builders cap
                # themselves; this is the loud backstop for a builder that
                # doesn't). Trim whole passage blocks from the end, alarm red.
                if _is_typed_block_list(content):
                    text_total = sum(
                        len(getattr(b, "get_output", lambda: "")() or "")
                        for b in content
                        if getattr(b, "type", "") == "search_result"
                    )
                    ceiling = TOOL_RESULT_ABSOLUTE_CEILING_CHARS
                    if block.approved_max_chars and int(block.approved_max_chars) > ceiling:
                        ceiling = int(block.approved_max_chars)
                    if text_total > ceiling:
                        kept: list[Any] = []
                        running = 0
                        dropped = 0
                        for b in content:
                            if getattr(b, "type", "") == "search_result":
                                b_chars = len(getattr(b, "get_output", lambda: "")() or "")
                                if running + b_chars > ceiling:
                                    dropped += 1
                                    continue
                                running += b_chars
                            kept.append(b)
                        block.content = kept
                        vcprint(
                            f"[citations] ABSOLUTE CEILING: tool result "
                            f"'{block.name}' carried {text_total:,} chars of citable "
                            f"passages (ceiling {ceiling:,}) — dropped {dropped} "
                            "passage block(s). The emitting tool must cap itself "
                            "(cap_citable_blocks); this backstop firing is a tool "
                            "defect.",
                            color="red",
                        )
                    continue
                # Measure what the provider will ACTUALLY send: a str as-is, a
                # dict/list as it will be json.dumps'd downstream (to_anthropic/
                # to_openai/to_google all stringify non-str content).
                if isinstance(content, str):
                    # Idempotency: a prior pass already truncated this block.
                    if _CEILING_TRUNCATION_MARKER in content[-400:]:
                        continue
                    measured = content
                else:
                    try:
                        measured = _json.dumps(content, default=str)
                    except Exception:
                        continue  # unserializable — leave it for the serializer

                ceiling = TOOL_RESULT_ABSOLUTE_CEILING_CHARS
                if block.approved_max_chars and int(block.approved_max_chars) > ceiling:
                    ceiling = int(block.approved_max_chars)
                total = len(measured)
                if total <= ceiling:
                    continue
                block.content = (
                    measured[:ceiling] + f"\n\n[⚠️ {_CEILING_TRUNCATION_MARKER} — {ceiling:,} of "
                    f"{total:,} chars. This result bypassed the normal size gate; re-run "
                    f"the source tool with narrower parameters to get a usable slice.]"
                )
                try:
                    from matrx_ai.tools.result_gate import ToolResultGateEvent, _emit

                    _emit(
                        ToolResultGateEvent(
                            tier="ceiling_fired",
                            tool_name=block.name or "<unknown>",
                            tool_kind="unknown",
                            output_chars=total,
                            limit=ceiling,
                            conversation_id=conv_id,
                            call_id=(block.call_id or block.tool_use_id or None),
                            user_id=user_id,
                        )
                    )
                except Exception:
                    pass

    def strip_keep_fresh_from_last_user(self) -> list:
        """Remove all keep_fresh=True structured input blocks from the last user message.

        Called by the persistence layer immediately before writing messages to the DB.
        The blocks' structural definitions (type, IDs, keep_fresh=True) are still
        serialized via to_storage_dict() so the next turn knows to re-fetch them.
        Returns the stripped blocks (currently unused by callers but available for logging).
        """
        last_user = self.get_last_by_role(Role.USER)
        if last_user is not None:
            return last_user.strip_keep_fresh_blocks()
        return []

    def append_user_text(self, text: str, **kwargs) -> None:
        """
        Helper to append a simple user text message.

        Args:
            text: The text content
            **kwargs: Additional UnifiedMessage fields (id, name, timestamp, metadata)
        """
        user_message = UnifiedMessage(role=Role.USER, content=[TextContent(text=text)], **kwargs)
        self.append(user_message)

    def append_or_extend_user_text(self, text: str, **kwargs) -> None:
        """
        Add user text to the message list.

        If the last message is already a user message (not yet sent), append the text
        to the existing message with a line break.

        If the last message is not a user message, create a new user message.

        Args:
            text: The text content to add
            **kwargs: Additional UnifiedMessage fields (only used when creating new message)
        """
        if self._is_last_message_user():
            # Last message is user - append to existing text
            last_message = self._messages[-1]

            # Find the text content block and append
            for content in last_message.content:
                if isinstance(content, TextContent):
                    content.append_text(text)
                    break
            else:
                # No TextContent found (e.g. template with only structured blocks) — create one
                last_message.content.insert(0, TextContent(text=text))
        else:
            # Last message is not user (or no messages) - create new user message
            self.append_user_text(text, **kwargs)

    def append_or_extend_user_items(self, items: list[dict[str, Any]]) -> None:
        """
        items ex:
        [
            { "type": "input_text", "text": "what is in this image?" },
            { "type": "input_image", "image_url": "https://..." }
        ]

        """
        vcprint(items, "append_or_extend_user_input items", color="magenta")

        if self._is_last_message_user():
            # Last message is user - append to existing text
            last_message = self._messages[-1]
            text = ""
            items_without_text = []
            for item in items:
                if item["type"] in ("text", "input_text"):
                    text += item["text"] + "\n"
                else:
                    items_without_text.append(item)
            if text:
                for content in last_message.content:
                    if isinstance(content, TextContent):
                        content.append_text(text)
                        break
                else:
                    # No TextContent found — create one rather than silently dropping the text
                    last_message.content.insert(0, TextContent(text=text))
            if items_without_text:
                last_message.content.extend(UnifiedMessage.parse_content(items_without_text))
        else:
            user_message = UnifiedMessage.from_dict(
                {
                    "role": Role.USER,
                    "content": items,
                }
            )
            self.append(user_message)

    def append_or_extend_user_input(self, user_input: str | list[dict[str, Any]]) -> None:
        """
        Add user input to the message list.
        """
        if isinstance(user_input, str):
            self.append_or_extend_user_text(user_input)
        elif isinstance(user_input, list):
            self.append_or_extend_user_items(user_input)
        else:
            raise ValueError(f"Invalid user input type: {type(user_input)}")

    def _is_last_message_user(self) -> bool:
        """Check if the last message in the list is from a user."""
        if not self._messages:
            return False
        return self._messages[-1].role == Role.USER

    def append_assistant_text(self, text: str, **kwargs) -> None:
        """
        Helper to append a simple assistant text message.

        Args:
            text: The text content
            **kwargs: Additional UnifiedMessage fields (id, name, timestamp, metadata)
        """
        assistant_message = UnifiedMessage(
            role=Role.ASSISTANT, content=[TextContent(text=text)], **kwargs
        )
        self.append(assistant_message)

    def to_list(self) -> list["UnifiedMessage"]:
        """
        Get underlying list (for operations that need a raw list).
        Useful for spread operations: *message_list.to_list()
        """
        return self._messages

    def to_dict_list(self) -> list[dict[str, Any]]:
        """Convert all messages to dictionaries.

        🚨 Each content block is serialized by ITS OWN ``to_dict()`` — never by
        dumping ``__dict__``. This list is what ``UnifiedConfig.to_dict()``
        emits, which is what ``AIMatrixRequest.to_dict()`` emits, which is what
        ``chat.request_snapshot.unified_payload`` STORES — the one sanctioned
        re-entry point for wire replay. A raw ``__dict__`` dump is a second,
        drifting serializer of a shape ``to_dict``/``to_storage_dict`` already
        own: it leaks private runtime fields, and it emitted binary
        provider-continuity material (Gemini's ``google_thought_signature``) as
        raw ``bytes``, which the snapshot writer's ``_json_safe`` coercion then
        replaced with the unusable string ``<bytes len=N>``. Every recorded
        Gemini call carrying a thought signature was un-replayable as a result
        (2026-08-16 defect; 151 SDK validation errors before the request left
        the process). Blocks with no ``to_dict`` keep the legacy dump.
        """
        return [
            {
                "role": msg.role,
                "content": [
                    content.to_dict()
                    if hasattr(content, "to_dict")
                    else {
                        k: v
                        for k, v in content.__dict__.items()
                        if v is not None and v != {} and v != []
                    }
                    for content in msg.content
                ],
                **({"id": msg.id} if msg.id else {}),
                **({"name": msg.name} if msg.name else {}),
                **({"timestamp": msg.timestamp} if msg.timestamp else {}),
                **({"metadata": msg.metadata} if msg.metadata else {}),
            }
            for msg in self._messages
        ]

    def replace_variables(self, variables: dict[str, Any]) -> None:
        """
        Replace variables in all messages.

        Args:
            variables: dict mapping variable names to their values
        """
        for message in self._messages:
            message.replace_variables(variables)


# ----------------------------------------------------------------------
# Role-tagged content helpers
# ----------------------------------------------------------------------
#
# Agent message templates can attach a `metadata.role` to any content
# block to flag it for a specific translator purpose:
#
#   - Text roles:  "negative_prompt", "style_prompt"
#   - Image roles: "start_image", "end_image", "reference", "mask"
#   - (Future) audio/video roles as needed.
#
# Translators read these via the helpers below so the same agent template
# works across providers — each provider's translator picks up the roles
# it cares about, ignores the rest. Untagged content (no metadata.role)
# is the "main" content (e.g., the user's primary text prompt, a generic
# image input).
#
# All helpers iterate the most recent user message first (most specific
# intent for the current run). They never look at assistant messages.


def _iter_user_content(messages: Any):
    """Yield (message, content_block) pairs from user messages, most recent first."""
    if messages is None:
        return
    try:
        msgs = list(messages)
    except TypeError:
        return
    for msg in reversed(msgs):
        if getattr(msg, "role", None) != "user":
            continue
        for content in getattr(msg, "content", None) or []:
            yield msg, content


def _content_role(content: Any) -> str | None:
    meta = getattr(content, "metadata", None)
    if not isinstance(meta, dict):
        return None
    role = meta.get("role")
    return role if isinstance(role, str) and role else None


def pick_text_by_role(messages: Any, role: str | None) -> str | None:
    """Find the most recent user TextContent matching the given role.

    - ``role=None`` → returns the FIRST UN-TAGGED TextContent's text
      (the main user prompt). This is what every translator uses to
      build the prompt — it correctly skips role-tagged auxiliary text
      like negative_prompt.
    - ``role="negative_prompt"`` (or any other role string) → returns
      the text of the matching TextContent, or None if not present.

    Returns None when no matching TextContent exists. Empty string is
    NOT returned (role-tagged-and-empty content is dropped at
    substitution time).
    """
    for _, content in _iter_user_content(messages):
        if not isinstance(content, TextContent):
            continue
        text = getattr(content, "text", None)
        if not text:
            continue
        content_role = _content_role(content)
        if role is None:
            if content_role is None:
                return text
        else:
            if content_role == role:
                return text
    return None


def pick_image_by_role(messages: Any, role: str | None) -> Any:
    """Find the most recent user ImageContent matching the given role.

    - ``role="start_image"`` / ``"end_image"`` / ``"mask"`` etc. →
      returns the ImageContent whose ``metadata.role`` matches.
    - ``role=None`` → returns the FIRST UN-TAGGED ImageContent (the
      generic image input, e.g. for image-to-image edits).

    Returns None when no matching ImageContent exists.
    """
    from matrx_ai.config.media_config import ImageContent

    for _, content in _iter_user_content(messages):
        if not isinstance(content, ImageContent):
            continue
        content_role = _content_role(content)
        if role is None:
            if content_role is None:
                return content
        else:
            if content_role == role:
                return content
    return None


def iter_images_by_role(messages: Any, role: str | None):
    """Yield user ImageContent blocks matching the given role, most
    recent message first. Useful for multi-reference inputs where any
    number of images can carry e.g. ``metadata.role = "reference"``.
    """
    from matrx_ai.config.media_config import ImageContent

    for _, content in _iter_user_content(messages):
        if not isinstance(content, ImageContent):
            continue
        content_role = _content_role(content)
        if role is None:
            if content_role is None:
                yield content
        else:
            if content_role == role:
                yield content
