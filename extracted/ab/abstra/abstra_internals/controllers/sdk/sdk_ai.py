from __future__ import annotations

import base64
import io
import json
import pathlib
from typing import Any, Callable, Union

import puremagic

from abstra_internals.contracts_generated import (
    CloudApiCliAgentsPostRequestBodyResponse,
    CloudApiCliAgentsPostRequestBodyStart,
    CloudApiCliAgentsPostRequestBodyStartToolsItem,
    CloudApiCliAiV2PromptPostRequest,
    CloudApiCliAiV2PromptPostRequestMessages,
    CloudApiCliAiV2PromptPostRequestMessagesItem,
    CloudApiCliAiV2PromptPostRequestMessagesItemContentItemImage,
    CloudApiCliAiV2PromptPostRequestMessagesItemContentItemImageImageUrl,
    CloudApiCliAiV2PromptPostRequestMessagesItemContentItemText,
    CloudApiCliAiV2PromptPostRequestTools,
    CloudApiCliAiV2PromptPostRequestToolsItem,
)
from abstra_internals.entities.forms.widgets.response_types import AbstractFileResponse
from abstra_internals.interface.sdk.forms.deprecated.widgets.response_abc import (
    AbstractFileResponse as DeprecatedAbstractFileResponse,
)
from abstra_internals.repositories.ai import AIRepository
from abstra_internals.utils import b64
from abstra_internals.utils.ai import build_function_tool_call
from abstra_internals.utils.image import constrain_image_size

Prompt = Union[
    str, io.IOBase, pathlib.Path, AbstractFileResponse, DeprecatedAbstractFileResponse
]
Format = dict[str, object]


class AiSDKController:
    def __init__(self, ai_client: AIRepository):
        self.ai_client = ai_client

    def _extract_pdf_images(self, file: Prompt) -> list[io.BytesIO]:
        import pypdfium2 as pdfium

        images = []
        for page in pdfium.PdfDocument(file):
            bitmap = page.render(
                scale=4,  # 288 dpi
                rotation=0,
            )
            pil_image = bitmap.to_pil()
            pil_image = constrain_image_size(pil_image)
            image_io = io.BytesIO()
            pil_image.save(image_io, format="png")
            images.append(image_io)
        return images

    def _make_image_url_message(
        self, url: str
    ) -> CloudApiCliAiV2PromptPostRequestMessagesItem:
        return CloudApiCliAiV2PromptPostRequestMessagesItem(
            role="user",
            content=[
                CloudApiCliAiV2PromptPostRequestMessagesItemContentItemImage(
                    type="image_url",
                    image_url=CloudApiCliAiV2PromptPostRequestMessagesItemContentItemImageImageUrl(
                        url=url
                    ),
                )
            ],
        )

    def _make_text_message(
        self, text: str
    ) -> CloudApiCliAiV2PromptPostRequestMessagesItem:
        return CloudApiCliAiV2PromptPostRequestMessagesItem(
            role="user",
            content=[
                CloudApiCliAiV2PromptPostRequestMessagesItemContentItemText(
                    type="text", text=text
                )
            ],
        )

    def _try_extract_images(self, input: io.IOBase) -> list[io.BytesIO] | None:
        try:
            images = self._extract_pdf_images(input)
            return images
        except Exception:
            return None

    @staticmethod
    def _describe_unreadable(raw: bytes) -> str:
        """Human-friendly label for bytes we can't send as an image, so the
        error tells the user what they actually passed (e.g. an HTML error page
        saved with a `.pdf` name) instead of a provider's opaque rejection."""
        if not raw:
            return "an empty file"
        if raw[:5] == b"%PDF-":
            return "a PDF that could not be rendered (it may be corrupt, truncated, or password-protected)"
        if raw[:4] == b"PK\x03\x04":
            return "a ZIP archive"
        head = raw[:512].lstrip().lower()
        if head.startswith(b"<!doctype html") or head.startswith(b"<html"):
            return "an HTML page"
        if head.startswith(b"<?xml"):
            return "an XML document"
        return "data that is not a supported image or readable PDF"

    def _binary_file_messages(
        self, file: io.IOBase, label: str
    ) -> CloudApiCliAiV2PromptPostRequestMessages:
        """Turn a binary file into image messages: render PDFs to page images,
        pass through supported images, and raise a clear error for anything else
        rather than silently shipping raw bytes the AI provider will reject."""
        if images := self._try_extract_images(file):
            return [
                self._make_image_url_message(b64.encode_base_64(image))
                for image in images
            ]

        file.seek(0)
        raw = file.read()
        try:
            image_type = puremagic.what(None, h=raw)
        except Exception:
            image_type = None

        if image_type in ("png", "jpeg", "gif", "webp"):
            return [self._make_image_url_message(b64.encode_base_64(io.BytesIO(raw)))]

        raise ValueError(
            f"Cannot use '{label}' as an AI prompt: it is {self._describe_unreadable(raw)}. "
            "Only images (PNG, JPEG, GIF, WebP) and readable PDFs are supported."
        )

    def _make_messages(
        self, prompt: Prompt
    ) -> CloudApiCliAiV2PromptPostRequestMessages:
        if isinstance(prompt, pathlib.Path):
            if prompt.suffix[1:] == "txt":
                with open(prompt, "r", encoding="utf-8") as f:
                    return [self._make_text_message(f.read())]

            with prompt.open("rb") as f:
                return self._binary_file_messages(f, str(prompt))

        if isinstance(prompt, (AbstractFileResponse, DeprecatedAbstractFileResponse)):
            if prompt.path.suffix[1:] == "txt":
                return [self._make_text_message(prompt.content.decode("utf-8"))]

            return self._binary_file_messages(prompt.file, str(prompt.path))

        if isinstance(prompt, io.IOBase):
            prompt.seek(0)
            return self._binary_file_messages(prompt, "<file>")

        if isinstance(prompt, str) and (
            b64.is_base_64(prompt) or prompt.startswith("http")
        ):
            if prompt.endswith(".pdf"):
                raise ValueError("PDF URLs are not supported")

            return [self._make_image_url_message(prompt)]

        try:
            is_existing_path = isinstance(prompt, str) and pathlib.Path(prompt).exists()
        except OSError:  # Path contructor can raise OSError on long strings
            is_existing_path = False
        if is_existing_path:
            with open(prompt, "rb") as f:  # type: ignore[arg-type]
                return self._binary_file_messages(f, str(prompt))

        try:
            from PIL.Image import Image as PILImage
        except ImportError:
            PILImage = type(None)  # type: ignore[assignment,misc]
        if isinstance(prompt, PILImage):
            image_io = io.BytesIO()
            prompt.save(image_io, format="PNG")
            image_io.seek(0)
            encoded_str = b64.encode_base_64(image_io)
            return [self._make_image_url_message(encoded_str)]

        if isinstance(prompt, str):
            return [self._make_text_message(prompt)]

        raise ValueError(f"Invalid prompt: {prompt}")

    def prompt(
        self,
        prompts: list[Prompt],
        instructions: list[str],
        format: Format | None,
        temperature: float,
    ):
        messages: CloudApiCliAiV2PromptPostRequestMessages = []

        for instruction in instructions:
            messages.append(
                CloudApiCliAiV2PromptPostRequestMessagesItem(
                    role="system",
                    content=[
                        CloudApiCliAiV2PromptPostRequestMessagesItemContentItemText(
                            type="text", text=instruction
                        )
                    ],
                )
            )

        for prompt in prompts:
            messages.extend(self._make_messages(prompt))

        tools: CloudApiCliAiV2PromptPostRequestTools = []
        if format:
            function = build_function_tool_call(format)
            tools.append(
                CloudApiCliAiV2PromptPostRequestToolsItem(
                    type="function", function=function
                )
            )

        response = self.ai_client.prompt(
            prompt_request_body=CloudApiCliAiV2PromptPostRequest(
                messages=messages,
                tools=tools,
                temperature=temperature,
            )
        )

        if response.get("error"):
            err = response["error"]
            try:
                if isinstance(err, list):
                    msg = "\n".join(f"[{e['supplier']}] {e['error']}" for e in err)
                else:
                    msg = str(err)
            except Exception:
                msg = str(err)
            raise Exception(msg)

        if format:
            parameters_dict = response["tool_calls"][0]["function"]["arguments"]
            try:
                return json.loads(parameters_dict)
            except json.JSONDecodeError:
                raise Exception(f"Error parsing JSON: {parameters_dict}")

        return response["content"]

    def run_agent(
        self,
        prompts: list[Prompt],
        max_steps: int,
        tool_callables: dict[str, Callable[..., Any]] | None = None,
        tool_items: "list[CloudApiCliAgentsPostRequestBodyStartToolsItem] | None" = None,
    ) -> dict:
        messages: CloudApiCliAiV2PromptPostRequestMessages = []
        for prompt in prompts:
            messages.extend(self._make_messages(prompt))

        body = CloudApiCliAgentsPostRequestBodyStart(
            type="start",
            prompt=messages,
            tools=tool_items,
            max_steps=max_steps,
        )

        response = self.ai_client.run_agent(body=body)

        while response.get("status") == "function-call":
            print(
                f"[Agent] requested tool call: {response['functionName']} with arguments {response.get('arguments', {})}"
            )
            function_name = response["functionName"]
            arguments = response.get("arguments", {})
            session_id = response["sessionId"]

            func = (tool_callables or {}).get(function_name)
            if func is None:
                raise ValueError(f"Agent requested unknown tool: '{function_name}'")

            def trucate(txt: str):
                if len(txt) > 100:
                    return txt[:100] + "..."
                return txt

            try:
                value = func(**arguments)
                print(f"[Agent] Tool call result: {trucate(repr(value))}")
                result = {"status": "success", "value": value}
            except Exception as e:
                error_msg = str(e)
                is_fatal = error_msg.startswith("FATAL:")
                result = {"status": "error", "error": error_msg, "fatal": is_fatal}
                print(f"[Agent] Tool call error: {trucate(repr(e))}")

            if result["status"] == "success" and isinstance(
                value := result["value"], pathlib.Path
            ):
                response_body = CloudApiCliAgentsPostRequestBodyResponse(
                    type="response",
                    session_id=session_id,
                    value=base64.b64encode(value.read_bytes()).decode("utf-8"),
                    encoding="image/base64",
                )
            else:
                response_body = CloudApiCliAgentsPostRequestBodyResponse(
                    type="response",
                    session_id=session_id,
                    value=result,
                    encoding="explicit",
                )
            response = self.ai_client.run_agent(body=response_body)

        return response

    def parse_document(self, document_path: pathlib.Path | str, model: str) -> dict:
        if isinstance(document_path, str):
            document_path = pathlib.Path(document_path)

        if document_path.suffix.lower() == ".pdf":
            mime_type = "application/pdf"
        elif document_path.suffix.lower() in [".jpeg", ".jpg"]:
            mime_type = "image/jpeg"
        elif document_path.suffix.lower() == ".png":
            mime_type = "image/png"
        else:
            raise ValueError(
                f"Unsupported file type: {document_path.suffix}. Supported types are: .pdf, .jpeg, .jpg, .png"
            )

        file_bytes = document_path.read_bytes()
        response = self.ai_client.parse_document(
            model=model,
            file_content=file_bytes,
            mime_type=mime_type,
        )

        if isinstance(response, dict) and response.get("error"):
            err = response["error"]
            try:
                if isinstance(err, list):
                    msg = "\n".join(f"[{e['supplier']}] {e['error']}" for e in err)
                else:
                    msg = str(err)
            except Exception:
                msg = str(err)
            raise Exception(msg)

        return response
