"""Converters between Mistral chat messages and GenAI message attributes."""

from collections.abc import Mapping, Sequence
from copy import deepcopy
from typing import cast

from .models import EventAttributeValue

type JsonObject = dict[str, EventAttributeValue]
type JsonMapping = Mapping[str, EventAttributeValue]

ROLE_SYSTEM = "system"
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_TOOL = "tool"

FIELD_ARGUMENTS = "arguments"
FIELD_CLOSED = "closed"
FIELD_CONTENT = "content"
FIELD_DETAIL = "detail"
FIELD_DOCUMENT_NAME = "document_name"
FIELD_DOCUMENT_URL = "document_url"
FIELD_FILE_ID = "file_id"
FIELD_FINISH_REASON = "finish_reason"
FIELD_FUNCTION = "function"
FIELD_ID = "id"
FIELD_IMAGE_URL = "image_url"
FIELD_INDEX = "index"
FIELD_INPUT_AUDIO = "input_audio"
FIELD_MESSAGE = "message"
FIELD_MODALITY = "modality"
FIELD_NAME = "name"
FIELD_PARTS = "parts"
FIELD_PREFIX = "prefix"
FIELD_RESPONSE = "response"
FIELD_ROLE = "role"
FIELD_TEXT = "text"
FIELD_THINKING = "thinking"
FIELD_TOOL_CALL_ID = "tool_call_id"
FIELD_TOOL_CALLS = "tool_calls"
FIELD_TYPE = "type"
FIELD_URI = "uri"
FIELD_URL = "url"

MISTRAL_FIELD_CLOSED = "mistral.closed"
MISTRAL_FIELD_DETAIL = "mistral.detail"
MISTRAL_FIELD_DOCUMENT_NAME = "mistral.document_name"
MISTRAL_FIELD_INDEX = "mistral.index"
MISTRAL_FIELD_NAME = "mistral.name"
MISTRAL_FIELD_PREFIX = "mistral.prefix"
MISTRAL_FIELD_THINKING = "mistral.thinking"
MISTRAL_FIELD_TYPE = "mistral.type"

TYPE_BLOB = "blob"
TYPE_DOCUMENT_URL = "document_url"
TYPE_FILE = "file"
TYPE_IMAGE_URL = "image_url"
TYPE_INPUT_AUDIO = "input_audio"
TYPE_REASONING = "reasoning"
TYPE_REFERENCE = "reference"
TYPE_SERVER_TOOL_CALL = "server_tool_call"
TYPE_SERVER_TOOL_CALL_RESPONSE = "server_tool_call_response"
TYPE_TEXT = "text"
TYPE_THINKING = "thinking"
TYPE_TOOL_CALL = "tool_call"
TYPE_TOOL_CALL_RESPONSE = "tool_call_response"
TYPE_URI = "uri"

TOOL_CALL_TYPE_FUNCTION = "function"

MODALITY_AUDIO = "audio"
MODALITY_DOCUMENT = "document"
MODALITY_IMAGE = "image"
MODALITY_VIDEO = "video"

FINISH_REASON_TOOL_CALLS = "tool_calls"


class MistralConversionError(ValueError):
    """Raised when a Mistral or GenAI message cannot be converted safely."""


class UnsupportedMistralMappingError(MistralConversionError):
    """Raised when a conversion would lose data that must be preserved."""


def mistral_messages_to_otel_input_messages(messages: Sequence[JsonMapping]) -> list[JsonObject]:
    """Convert Mistral request messages to `gen_ai.input.messages` values."""
    return [_mistral_message_to_chat_message(message, index) for index, message in enumerate(messages)]


def mistral_choices_to_otel_output_messages(choices: Sequence[JsonMapping]) -> list[JsonObject]:
    """Convert Mistral response choices to `gen_ai.output.messages` values."""
    return [_mistral_choice_to_output_message(choice, index) for index, choice in enumerate(choices)]


def otel_input_messages_to_mistral_messages(messages: Sequence[JsonMapping]) -> list[JsonObject]:
    """Convert `gen_ai.input.messages` values back to Mistral request messages."""
    return [_chat_message_to_mistral_message(message, index) for index, message in enumerate(messages)]


def otel_output_messages_to_mistral_choices(messages: Sequence[JsonMapping]) -> list[JsonObject]:
    """Convert `gen_ai.output.messages` values back to Mistral response choices."""
    return [_output_message_to_mistral_choice(message, index) for index, message in enumerate(messages)]


def _mistral_message_to_chat_message(message: JsonMapping, index: int) -> JsonObject:
    try:
        _validate_mistral_message(message)
        role = _string(message.get(FIELD_ROLE))
        chat_message: JsonObject = {FIELD_ROLE: role}

        name = _string(message.get(FIELD_NAME))
        if name:
            chat_message[FIELD_NAME] = name
            chat_message[MISTRAL_FIELD_NAME] = name

        if role == ROLE_ASSISTANT and bool(message.get(FIELD_PREFIX)):
            chat_message[MISTRAL_FIELD_PREFIX] = True

        if role == ROLE_ASSISTANT:
            chat_message[FIELD_PARTS] = _assistant_message_to_parts(message)
        elif role == ROLE_TOOL:
            chat_message[FIELD_PARTS] = [_tool_message_to_part(message)]
        else:
            chat_message[FIELD_PARTS] = _content_to_parts(message.get(FIELD_CONTENT))

        return chat_message
    except MistralConversionError as exc:
        message_text = f"message {index}: {exc}"
        raise MistralConversionError(message_text) from exc


def _mistral_choice_to_output_message(choice: JsonMapping, index: int) -> JsonObject:
    try:
        chat_message = _mistral_message_to_chat_message(_mapping(choice.get(FIELD_MESSAGE)), index)
    except MistralConversionError as exc:
        message_text = f"choice {index}: {exc}"
        raise MistralConversionError(message_text) from exc

    return {
        FIELD_ROLE: chat_message[FIELD_ROLE],
        FIELD_PARTS: chat_message[FIELD_PARTS],
        FIELD_FINISH_REASON: _string(choice.get(FIELD_FINISH_REASON)),
        MISTRAL_FIELD_INDEX: _int(choice.get(FIELD_INDEX)),
    }


def _chat_message_to_mistral_message(message: JsonMapping, index: int) -> JsonObject:
    try:
        role = _string(message.get(FIELD_ROLE))
        parts = _parts(message.get(FIELD_PARTS))
        mistral_message: JsonObject = {FIELD_ROLE: role}

        name = _string(message.get(MISTRAL_FIELD_NAME)) or _string(message.get(FIELD_NAME))
        if name:
            mistral_message[FIELD_NAME] = name

        if role == ROLE_ASSISTANT:
            if bool(message.get(MISTRAL_FIELD_PREFIX)):
                mistral_message[FIELD_PREFIX] = True
            content, tool_calls = _parts_to_assistant(parts)
            mistral_message[FIELD_CONTENT] = content
            if tool_calls:
                mistral_message[FIELD_TOOL_CALLS] = tool_calls
        elif role == ROLE_TOOL:
            tool_call_id, content = _parts_to_tool_message(parts)
            mistral_message[FIELD_TOOL_CALL_ID] = tool_call_id
            mistral_message[FIELD_CONTENT] = content
        else:
            mistral_message[FIELD_CONTENT] = _parts_to_content(parts)

        _validate_mistral_message(mistral_message)
        return mistral_message
    except MistralConversionError as exc:
        message_text = f"message {index}: {exc}"
        raise MistralConversionError(message_text) from exc


def _output_message_to_mistral_choice(message: JsonMapping, index: int) -> JsonObject:
    try:
        mistral_message = _chat_message_to_mistral_message(
            {FIELD_ROLE: message.get(FIELD_ROLE), FIELD_PARTS: message.get(FIELD_PARTS)},
            index,
        )
    except MistralConversionError as exc:
        message_text = f"output message {index}: {exc}"
        raise MistralConversionError(message_text) from exc

    return {
        FIELD_INDEX: _int(message.get(MISTRAL_FIELD_INDEX)),
        FIELD_MESSAGE: mistral_message,
        FIELD_FINISH_REASON: _string(message.get(FIELD_FINISH_REASON)),
    }


def _assistant_message_to_parts(message: JsonMapping) -> list[JsonObject]:
    parts: list[JsonObject] = []
    content = message.get(FIELD_CONTENT)
    if content is not None:
        parts.extend(_content_to_parts(content))

    for tool_call in _sequence(message.get(FIELD_TOOL_CALLS)):
        tool_call_mapping = _mapping(tool_call)
        function = _mapping(tool_call_mapping.get(FIELD_FUNCTION))
        part: JsonObject = {
            FIELD_TYPE: TYPE_TOOL_CALL,
            FIELD_NAME: _string(function.get(FIELD_NAME)),
            MISTRAL_FIELD_INDEX: _int(tool_call_mapping.get(FIELD_INDEX)),
        }
        _set_if_truthy(part, FIELD_ID, tool_call_mapping.get(FIELD_ID))
        if FIELD_ARGUMENTS in function:
            part[FIELD_ARGUMENTS] = deepcopy(function[FIELD_ARGUMENTS])
        _set_if_truthy(part, MISTRAL_FIELD_TYPE, tool_call_mapping.get(FIELD_TYPE))
        parts.append(part)

    return parts


def _tool_message_to_part(message: JsonMapping) -> JsonObject:
    return {
        FIELD_TYPE: TYPE_TOOL_CALL_RESPONSE,
        FIELD_ID: _string(message.get(FIELD_TOOL_CALL_ID)),
        FIELD_RESPONSE: deepcopy(message.get(FIELD_CONTENT)),
    }


def _content_to_parts(content: object) -> list[JsonObject]:
    if content is None:
        return []
    elif isinstance(content, str):
        return [{FIELD_TYPE: TYPE_TEXT, FIELD_CONTENT: content}]
    else:
        return [_chunk_to_part(_mapping(chunk)) for chunk in _sequence(content)]


def _parts_to_assistant(parts: Sequence[JsonMapping]) -> tuple[EventAttributeValue, list[JsonObject]]:
    content_parts: list[JsonMapping] = []
    tool_calls: list[JsonObject] = []

    for part in parts:
        if _string(part.get(FIELD_TYPE)) != TYPE_TOOL_CALL:
            content_parts.append(part)
            continue

        tool_call: JsonObject = {
            FIELD_FUNCTION: {
                FIELD_NAME: _string(part.get(FIELD_NAME)),
            },
            FIELD_INDEX: _int(part.get(MISTRAL_FIELD_INDEX)),
        }
        _set_if_truthy(tool_call, FIELD_ID, part.get(FIELD_ID))
        _set_if_truthy(tool_call, FIELD_TYPE, part.get(MISTRAL_FIELD_TYPE))
        if FIELD_ARGUMENTS in part:
            cast(JsonObject, tool_call[FIELD_FUNCTION])[FIELD_ARGUMENTS] = deepcopy(part[FIELD_ARGUMENTS])
        tool_calls.append(tool_call)

    return _parts_to_content(content_parts), tool_calls


def _parts_to_tool_message(parts: Sequence[JsonMapping]) -> tuple[str, EventAttributeValue]:
    response_part: JsonMapping | None = None
    for part in parts:
        if _string(part.get(FIELD_TYPE)) != TYPE_TOOL_CALL_RESPONSE:
            continue
        if response_part is not None:
            message_text = "tool message must have exactly one tool_call_response part"
            raise MistralConversionError(message_text)
        response_part = part

    if response_part is None:
        message_text = "tool message must contain one tool_call_response part"
        raise MistralConversionError(message_text)

    tool_call_id = _string(response_part.get(FIELD_ID))
    content = deepcopy(response_part.get(FIELD_RESPONSE))
    if isinstance(content, str):
        content = [{FIELD_TYPE: TYPE_TEXT, FIELD_TEXT: content}]
    return tool_call_id, content


def _parts_to_content(parts: Sequence[JsonMapping]) -> EventAttributeValue:
    if not parts:
        return None

    chunks: list[JsonObject] = []
    for part in parts:
        try:
            chunks.append(_part_to_chunk(part))
        except UnsupportedMistralMappingError:
            continue

    if not chunks:
        return None
    return chunks


def _chunk_to_part(chunk: JsonMapping) -> JsonObject:
    chunk_type = _string(chunk.get(FIELD_TYPE))
    if chunk_type == TYPE_TEXT:
        return {FIELD_TYPE: TYPE_TEXT, FIELD_CONTENT: _string(chunk.get(FIELD_TEXT))}
    elif chunk_type == TYPE_IMAGE_URL:
        return _image_url_chunk_to_part(chunk)
    elif chunk_type == TYPE_DOCUMENT_URL:
        return _document_url_chunk_to_part(chunk)
    elif chunk_type == TYPE_INPUT_AUDIO:
        return {
            FIELD_TYPE: TYPE_BLOB,
            FIELD_MODALITY: MODALITY_AUDIO,
            FIELD_CONTENT: _string(chunk.get(FIELD_INPUT_AUDIO)),
            MISTRAL_FIELD_TYPE: TYPE_INPUT_AUDIO,
        }
    elif chunk_type == TYPE_THINKING:
        return _thinking_chunk_to_reasoning_part(chunk)
    elif chunk_type == TYPE_FILE:
        return _file_chunk_to_part(chunk)

    part = dict(deepcopy(chunk))
    if not chunk_type:
        message_text = "chunk has no type field"
        raise MistralConversionError(message_text)
    part[FIELD_TYPE] = chunk_type
    return part


def _image_url_chunk_to_part(chunk: JsonMapping) -> JsonObject:
    image_url = chunk.get(FIELD_IMAGE_URL)
    if isinstance(image_url, str):
        url = image_url
        detail = ""
    else:
        image = _mapping(image_url)
        url = _string(image.get(FIELD_URL))
        detail = _string(image.get(FIELD_DETAIL))
    if not url:
        message_text = "image_url chunk has no image_url field"
        raise MistralConversionError(message_text)
    part: JsonObject = {FIELD_TYPE: TYPE_URI, FIELD_MODALITY: MODALITY_IMAGE, FIELD_URI: url}
    _set_if_truthy(part, MISTRAL_FIELD_DETAIL, detail)
    return part


def _document_url_chunk_to_part(chunk: JsonMapping) -> JsonObject:
    uri = _string(chunk.get(FIELD_DOCUMENT_URL))
    if not uri:
        message_text = "document_url chunk has no document_url field"
        raise MistralConversionError(message_text)
    part: JsonObject = {FIELD_TYPE: TYPE_URI, FIELD_MODALITY: MODALITY_DOCUMENT, FIELD_URI: uri}
    _set_if_truthy(part, MISTRAL_FIELD_DOCUMENT_NAME, chunk.get(FIELD_DOCUMENT_NAME))
    return part


def _file_chunk_to_part(chunk: JsonMapping) -> JsonObject:
    file_id = _string(chunk.get(FIELD_FILE_ID))
    if not file_id:
        message_text = "file chunk has no file_id field"
        raise MistralConversionError(message_text)
    return {FIELD_TYPE: TYPE_FILE, FIELD_MODALITY: MODALITY_DOCUMENT, FIELD_FILE_ID: file_id}


def _part_to_chunk(part: JsonMapping) -> JsonObject:
    part_type = _string(part.get(FIELD_TYPE))
    if part_type == TYPE_TEXT:
        return {FIELD_TYPE: TYPE_TEXT, FIELD_TEXT: _string(part.get(FIELD_CONTENT))}
    elif part_type == TYPE_URI:
        return _uri_part_to_chunk(part)
    elif part_type == TYPE_BLOB:
        return _blob_part_to_chunk(part)
    elif part_type == TYPE_FILE:
        return {FIELD_TYPE: TYPE_FILE, FIELD_FILE_ID: _string(part.get(FIELD_FILE_ID))}
    elif part_type == TYPE_REASONING:
        return _reasoning_part_to_thinking_chunk(part)
    elif part_type in {TYPE_TOOL_CALL, TYPE_TOOL_CALL_RESPONSE}:
        message_text = f"{part_type} part cannot be represented as content"
        raise UnsupportedMistralMappingError(message_text)
    elif part_type in {TYPE_SERVER_TOOL_CALL, TYPE_SERVER_TOOL_CALL_RESPONSE}:
        message_text = f"{part_type} part cannot be represented in Mistral"
        raise UnsupportedMistralMappingError(message_text)
    elif not part_type:
        message_text = "part has no type field"
        raise MistralConversionError(message_text)
    else:
        return dict(deepcopy(part))


def _uri_part_to_chunk(part: JsonMapping) -> JsonObject:
    modality = _string(part.get(FIELD_MODALITY))
    if modality == MODALITY_IMAGE:
        image_url: JsonObject = {FIELD_URL: _string(part.get(FIELD_URI))}
        _set_if_truthy(image_url, FIELD_DETAIL, part.get(MISTRAL_FIELD_DETAIL))
        return {FIELD_TYPE: TYPE_IMAGE_URL, FIELD_IMAGE_URL: image_url}
    elif modality == MODALITY_DOCUMENT:
        chunk: JsonObject = {FIELD_TYPE: TYPE_DOCUMENT_URL, FIELD_DOCUMENT_URL: _string(part.get(FIELD_URI))}
        _set_if_truthy(chunk, FIELD_DOCUMENT_NAME, part.get(MISTRAL_FIELD_DOCUMENT_NAME))
        return chunk
    else:
        message_text = f"uri part with modality {modality!r}"
        raise UnsupportedMistralMappingError(message_text)


def _blob_part_to_chunk(part: JsonMapping) -> JsonObject:
    modality = _string(part.get(FIELD_MODALITY))
    if modality == MODALITY_AUDIO:
        return {FIELD_TYPE: TYPE_INPUT_AUDIO, FIELD_INPUT_AUDIO: _string(part.get(FIELD_CONTENT))}
    else:
        message_text = f"blob part with modality {modality!r}"
        raise UnsupportedMistralMappingError(message_text)


def _thinking_chunk_to_reasoning_part(chunk: JsonMapping) -> JsonObject:
    thinking = _sequence(chunk.get(FIELD_THINKING)) if FIELD_THINKING in chunk else []
    part: JsonObject = {
        FIELD_TYPE: TYPE_REASONING,
        FIELD_CONTENT: _flatten_thinking_text(thinking),
    }
    if FIELD_CLOSED in chunk:
        part[MISTRAL_FIELD_CLOSED] = bool(chunk[FIELD_CLOSED])
    if FIELD_THINKING in chunk:
        part[MISTRAL_FIELD_THINKING] = deepcopy(thinking)
    return part


def _reasoning_part_to_thinking_chunk(part: JsonMapping) -> JsonObject:
    chunk: JsonObject = {FIELD_TYPE: TYPE_THINKING}
    if MISTRAL_FIELD_CLOSED in part:
        chunk[FIELD_CLOSED] = bool(part[MISTRAL_FIELD_CLOSED])
    if MISTRAL_FIELD_THINKING in part:
        chunk[FIELD_THINKING] = deepcopy(_sequence(part[MISTRAL_FIELD_THINKING]))
    else:
        chunk[FIELD_THINKING] = [{FIELD_TYPE: TYPE_TEXT, FIELD_TEXT: _string(part.get(FIELD_CONTENT))}]
    return chunk


def _flatten_thinking_text(thinking: Sequence[EventAttributeValue]) -> str:
    chunks: list[str] = []
    for part in thinking:
        part_mapping = _mapping(part)
        if _string(part_mapping.get(FIELD_TYPE)) == TYPE_TEXT:
            chunks.append(_string(part_mapping.get(FIELD_TEXT)))
    return "".join(chunks)


def _validate_mistral_message(message: JsonMapping) -> None:
    role = _string(message.get(FIELD_ROLE))
    if role == ROLE_SYSTEM:
        _validate_system_message(message)
    elif role == ROLE_USER:
        _validate_user_message(message)
    elif role == ROLE_ASSISTANT:
        _validate_assistant_message(message)
    elif role == ROLE_TOOL:
        _validate_tool_message(message)


def _validate_system_message(message: JsonMapping) -> None:
    if message.get(FIELD_CONTENT) is None:
        message_text = "system message content must not be null"
        raise MistralConversionError(message_text)
    if _sequence(message.get(FIELD_TOOL_CALLS)):
        message_text = "system message must not contain tool_calls"
        raise MistralConversionError(message_text)
    if _string(message.get(FIELD_TOOL_CALL_ID)):
        message_text = "system message must not contain tool_call_id"
        raise MistralConversionError(message_text)
    if _string(message.get(FIELD_NAME)):
        message_text = "system message must not contain name"
        raise MistralConversionError(message_text)
    if bool(message.get(FIELD_PREFIX)):
        message_text = "system message must not contain prefix"
        raise MistralConversionError(message_text)


def _validate_user_message(message: JsonMapping) -> None:
    if _sequence(message.get(FIELD_TOOL_CALLS)):
        message_text = "user message must not contain tool_calls"
        raise MistralConversionError(message_text)
    if _string(message.get(FIELD_TOOL_CALL_ID)):
        message_text = "user message must not contain tool_call_id"
        raise MistralConversionError(message_text)
    if bool(message.get(FIELD_PREFIX)):
        message_text = "user message must not contain prefix"
        raise MistralConversionError(message_text)


def _validate_assistant_message(message: JsonMapping) -> None:
    if _string(message.get(FIELD_TOOL_CALL_ID)):
        message_text = "assistant message must not contain tool_call_id"
        raise MistralConversionError(message_text)
    if _string(message.get(FIELD_NAME)):
        message_text = "assistant message must not contain name"
        raise MistralConversionError(message_text)


def _validate_tool_message(message: JsonMapping) -> None:
    if not _string(message.get(FIELD_TOOL_CALL_ID)):
        message_text = "tool message must have tool_call_id"
        raise MistralConversionError(message_text)
    if _sequence(message.get(FIELD_TOOL_CALLS)):
        message_text = "tool message must not contain tool_calls"
        raise MistralConversionError(message_text)
    if bool(message.get(FIELD_PREFIX)):
        message_text = "tool message must not contain prefix"
        raise MistralConversionError(message_text)


def _set_if_truthy(target: JsonObject, key: str, value: EventAttributeValue) -> None:
    if value:
        target[key] = deepcopy(value)


def _string(value: object) -> str:
    if isinstance(value, str):
        return value
    else:
        return ""


def _int(value: object) -> int:
    if isinstance(value, int):
        return value
    else:
        return 0


def _mapping(value: object) -> JsonMapping:
    if isinstance(value, Mapping):
        return cast(JsonMapping, value)
    else:
        return {}


def _parts(value: object) -> list[JsonMapping]:
    return [_mapping(part) for part in _sequence(value)]


def _sequence(value: object) -> list[EventAttributeValue]:
    if isinstance(value, list):
        return cast(list[EventAttributeValue], value)
    elif isinstance(value, tuple):
        return list(cast(tuple[EventAttributeValue, ...], value))
    else:
        return []
