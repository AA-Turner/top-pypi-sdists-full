from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_content_block_input import ManagedAgentsContentBlockInput
  from ..models.managed_agents_content_block_source import ManagedAgentsContentBlockSource





T = TypeVar("T", bound="ManagedAgentsContentBlock")



@_attrs_define
class ManagedAgentsContentBlock:
    """ One block of message content, following the Anthropic content-block shape: text, image, tool_use, tool_result,
    thinking, or a provider passthrough. The type field says which fields apply, and provider-native payloads are
    carried through verbatim.

        Example:
            {'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example', 'encrypted_content': 'example',
                'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True,
                'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example', 'provider':
                'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256': 'example',
                'signature': 'example', 'source': {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'},
                'summary': [], 'text': 'example', 'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'type': 'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at': '2026-02-18T09:30:00Z',
                'width': 1}

        Attributes:
            type_ (str): Anthropic-style block discriminator: text, image, document (a user-sent block naming a file by id,
                inlined as text when the message is accepted), tool_use, tool_result, thinking, redacted_thinking, or a provider
                passthrough type. Which of the other fields apply depends on this value.
            byte_size (int | Unset): Decoded image byte size.
            content (list[ManagedAgentsContentBlock] | Unset): Nested blocks carrying a tool_result payload, so a tool can
                return both text and images.
            context (str | Unset): A document block's context: what the model should know about the document before reading
                it, disclosed as its first paragraph.
            data (str | Unset): Base64 image bytes. Omitted from default reads and present only for legacy storage or
                explicit hydrate=images responses.
            encrypted_content (str | Unset): Sealed reasoning payload for providers that return reasoning encrypted (OpenAI
                encrypted reasoning items). Opaque to clients; replay it verbatim.
            height (int | Unset): Validated image height in pixels.
            id (str | Unset): Provider-assigned id of a tool_use block. Echo it back as tool_use_id on the matching
                tool_result.
            input_ (ManagedAgentsContentBlockInput | Unset): Tool arguments the model produced for a tool_use block,
                matching that tool's input schema.
            is_error (bool | Unset): True when a tool_result reports that the tool call failed; the nested content then
                carries the error detail.
            media_type (str | Unset): Declared media type; inline computer-use images allow image/jpeg, image/png, and
                image/webp.
            name (str | Unset): Name of the tool the model is invoking, on a tool_use block.
            omitted_bytes (int | Unset): Original byte count reported by a redacted image placeholder.
            payload (Any | Unset): Provider-native block body, stored verbatim for block types this schema does not model.
                Passed through unchanged.
            provider (str | Unset): Provider that emitted a passthrough block, e.g. anthropic or openai, telling readers how
                to interpret payload.
            provider_payload (Any | Unset): Original provider block exactly as received, kept alongside the normalized
                fields for lossless replay.
            redacted (bool | Unset): True when the block's content was withheld (redacted thinking, or an image dropped by
                redaction); the remaining fields describe what was removed.
            semantic_hint (str | Unset): Coarse hint about what an unmodeled provider block represents, so a reader can
                render it without provider-specific logic.
            sha256 (str | Unset): Lowercase SHA-256 digest of decoded image bytes.
            signature (str | Unset): Provider-issued signature over a thinking block, or the thought signature a Gemini
                tool_use block was issued with, required for the provider to accept that block on a later turn. Opaque; replay
                it verbatim.
            source (ManagedAgentsContentBlockSource | Unset): Where a user-sent image or document block takes its bytes from
                when the caller names a file instead of carrying them: a file from the organization's catalog, read and copied
                into the session when the message is accepted, so the block the transcript keeps names both the source and the
                copy. Example: {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}.
            summary (list[ManagedAgentsContentBlock] | Unset): Readable summary blocks a provider returns alongside sealed
                or long-form reasoning.
            text (str | Unset): Text of a text block, or the reasoning text of a thinking block.
            title (str | Unset): A document block's title, disclosed to the model beside the document.
            tool_use_id (str | Unset): Id of the tool_use block that this tool_result answers.
            uri (str | Unset): Private typed content reference. Fetch through the authenticated session image proxy; clients
                cannot read this gs:// URI directly.
            url (str | Unset): Short-lived HTTPS URL for the image bytes. Present only when the read asked for
                image_urls=signed and the deployment has signing configured. Never stored; fetch a fresh read after
                url_expires_at.
            url_expires_at (datetime.datetime | Unset): When url stops working. Absent whenever url is.
            width (int | Unset): Validated image width in pixels.
     """

    type_: str
    byte_size: int | Unset = UNSET
    content: list[ManagedAgentsContentBlock] | Unset = UNSET
    context: str | Unset = UNSET
    data: str | Unset = UNSET
    encrypted_content: str | Unset = UNSET
    height: int | Unset = UNSET
    id: str | Unset = UNSET
    input_: ManagedAgentsContentBlockInput | Unset = UNSET
    is_error: bool | Unset = UNSET
    media_type: str | Unset = UNSET
    name: str | Unset = UNSET
    omitted_bytes: int | Unset = UNSET
    payload: Any | Unset = UNSET
    provider: str | Unset = UNSET
    provider_payload: Any | Unset = UNSET
    redacted: bool | Unset = UNSET
    semantic_hint: str | Unset = UNSET
    sha256: str | Unset = UNSET
    signature: str | Unset = UNSET
    source: ManagedAgentsContentBlockSource | Unset = UNSET
    summary: list[ManagedAgentsContentBlock] | Unset = UNSET
    text: str | Unset = UNSET
    title: str | Unset = UNSET
    tool_use_id: str | Unset = UNSET
    uri: str | Unset = UNSET
    url: str | Unset = UNSET
    url_expires_at: datetime.datetime | Unset = UNSET
    width: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_content_block_input import ManagedAgentsContentBlockInput # noqa: PLC0415
        from ..models.managed_agents_content_block_source import ManagedAgentsContentBlockSource # noqa: PLC0415
        type_ = self.type_

        byte_size = self.byte_size

        content: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item = content_item_data.to_dict()
                content.append(content_item)



        context = self.context

        data = self.data

        encrypted_content = self.encrypted_content

        height = self.height

        id = self.id

        input_: dict[str, Any] | Unset = UNSET
        if not isinstance(self.input_, Unset):
            input_ = self.input_.to_dict()

        is_error = self.is_error

        media_type = self.media_type

        name = self.name

        omitted_bytes = self.omitted_bytes

        payload = self.payload

        provider = self.provider

        provider_payload = self.provider_payload

        redacted = self.redacted

        semantic_hint = self.semantic_hint

        sha256 = self.sha256

        signature = self.signature

        source: dict[str, Any] | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        summary: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.summary, Unset):
            summary = []
            for summary_item_data in self.summary:
                summary_item = summary_item_data.to_dict()
                summary.append(summary_item)



        text = self.text

        title = self.title

        tool_use_id = self.tool_use_id

        uri = self.uri

        url = self.url

        url_expires_at: str | Unset = UNSET
        if not isinstance(self.url_expires_at, Unset):
            url_expires_at = self.url_expires_at.isoformat()

        width = self.width


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if byte_size is not UNSET:
            field_dict["byte_size"] = byte_size
        if content is not UNSET:
            field_dict["content"] = content
        if context is not UNSET:
            field_dict["context"] = context
        if data is not UNSET:
            field_dict["data"] = data
        if encrypted_content is not UNSET:
            field_dict["encrypted_content"] = encrypted_content
        if height is not UNSET:
            field_dict["height"] = height
        if id is not UNSET:
            field_dict["id"] = id
        if input_ is not UNSET:
            field_dict["input"] = input_
        if is_error is not UNSET:
            field_dict["is_error"] = is_error
        if media_type is not UNSET:
            field_dict["media_type"] = media_type
        if name is not UNSET:
            field_dict["name"] = name
        if omitted_bytes is not UNSET:
            field_dict["omitted_bytes"] = omitted_bytes
        if payload is not UNSET:
            field_dict["payload"] = payload
        if provider is not UNSET:
            field_dict["provider"] = provider
        if provider_payload is not UNSET:
            field_dict["provider_payload"] = provider_payload
        if redacted is not UNSET:
            field_dict["redacted"] = redacted
        if semantic_hint is not UNSET:
            field_dict["semantic_hint"] = semantic_hint
        if sha256 is not UNSET:
            field_dict["sha256"] = sha256
        if signature is not UNSET:
            field_dict["signature"] = signature
        if source is not UNSET:
            field_dict["source"] = source
        if summary is not UNSET:
            field_dict["summary"] = summary
        if text is not UNSET:
            field_dict["text"] = text
        if title is not UNSET:
            field_dict["title"] = title
        if tool_use_id is not UNSET:
            field_dict["tool_use_id"] = tool_use_id
        if uri is not UNSET:
            field_dict["uri"] = uri
        if url is not UNSET:
            field_dict["url"] = url
        if url_expires_at is not UNSET:
            field_dict["url_expires_at"] = url_expires_at
        if width is not UNSET:
            field_dict["width"] = width

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_content_block_input import ManagedAgentsContentBlockInput # noqa: PLC0415
        from ..models.managed_agents_content_block_source import ManagedAgentsContentBlockSource # noqa: PLC0415
        d = dict(src_dict)
        type_ = d.pop("type")

        byte_size = d.pop("byte_size", UNSET)

        _content = d.pop("content", UNSET)
        content: list[ManagedAgentsContentBlock] | Unset = UNSET
        if _content is not UNSET:
            content = []
            for content_item_data in _content:
                content_item = ManagedAgentsContentBlock.from_dict(content_item_data)



                content.append(content_item)


        context = d.pop("context", UNSET)

        data = d.pop("data", UNSET)

        encrypted_content = d.pop("encrypted_content", UNSET)

        height = d.pop("height", UNSET)

        id = d.pop("id", UNSET)

        _input_ = d.pop("input", UNSET)
        input_: ManagedAgentsContentBlockInput | Unset
        if isinstance(_input_,  Unset):
            input_ = UNSET
        else:
            input_ = ManagedAgentsContentBlockInput.from_dict(_input_)




        is_error = d.pop("is_error", UNSET)

        media_type = d.pop("media_type", UNSET)

        name = d.pop("name", UNSET)

        omitted_bytes = d.pop("omitted_bytes", UNSET)

        payload = d.pop("payload", UNSET)

        provider = d.pop("provider", UNSET)

        provider_payload = d.pop("provider_payload", UNSET)

        redacted = d.pop("redacted", UNSET)

        semantic_hint = d.pop("semantic_hint", UNSET)

        sha256 = d.pop("sha256", UNSET)

        signature = d.pop("signature", UNSET)

        _source = d.pop("source", UNSET)
        source: ManagedAgentsContentBlockSource | Unset
        if isinstance(_source,  Unset):
            source = UNSET
        else:
            source = ManagedAgentsContentBlockSource.from_dict(_source)




        _summary = d.pop("summary", UNSET)
        summary: list[ManagedAgentsContentBlock] | Unset = UNSET
        if _summary is not UNSET:
            summary = []
            for summary_item_data in _summary:
                summary_item = ManagedAgentsContentBlock.from_dict(summary_item_data)



                summary.append(summary_item)


        text = d.pop("text", UNSET)

        title = d.pop("title", UNSET)

        tool_use_id = d.pop("tool_use_id", UNSET)

        uri = d.pop("uri", UNSET)

        url = d.pop("url", UNSET)

        _url_expires_at = d.pop("url_expires_at", UNSET)
        url_expires_at: datetime.datetime | Unset
        if isinstance(_url_expires_at,  Unset):
            url_expires_at = UNSET
        else:
            url_expires_at = datetime.datetime.fromisoformat(_url_expires_at)




        width = d.pop("width", UNSET)

        managed_agents_content_block = cls(
            type_=type_,
            byte_size=byte_size,
            content=content,
            context=context,
            data=data,
            encrypted_content=encrypted_content,
            height=height,
            id=id,
            input_=input_,
            is_error=is_error,
            media_type=media_type,
            name=name,
            omitted_bytes=omitted_bytes,
            payload=payload,
            provider=provider,
            provider_payload=provider_payload,
            redacted=redacted,
            semantic_hint=semantic_hint,
            sha256=sha256,
            signature=signature,
            source=source,
            summary=summary,
            text=text,
            title=title,
            tool_use_id=tool_use_id,
            uri=uri,
            url=url,
            url_expires_at=url_expires_at,
            width=width,
        )


        managed_agents_content_block.additional_properties = d
        return managed_agents_content_block

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
