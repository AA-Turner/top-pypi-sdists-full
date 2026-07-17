"""HTTP request/response transport: declarative body template + JSONPath response."""

import json

import httpx

from dreadnode.airt.targets.auth import apply_auth
from dreadnode.airt.targets.message import extract_media_bytes, extract_parts, extract_response_text
from dreadnode.airt.targets.spec import TargetSpec
from dreadnode.core.task import Task, task
from dreadnode.generators.message import Message


def _render_body(template: str, parts: dict[str, str]) -> dict:
    body_str = template
    for key, value in parts.items():
        token = "{" + key + "}"
        # JSON-escape the (untrusted) prompt; base64 is already safe.
        replacement = json.dumps(value)[1:-1] if key == "prompt" else value
        body_str = body_str.replace(token, replacement)
    return json.loads(body_str)


async def http_call(message: Message, spec: TargetSpec) -> str:
    """Serialize the message, POST it to the endpoint with auth, and extract the reply.

    Kept free of the ``@task`` wrapper so the request/response logic is unit testable
    without the tracing/storage a Task invocation requires.
    """
    if spec.request_format == "raw_audio":
        content = extract_media_bytes(message, "audio")
        content_type = spec.raw_content_type
    else:
        body = _render_body(spec.request_template, extract_parts(message))
        content = json.dumps(body).encode("utf-8")
        content_type = "application/json"
    headers = apply_auth(spec, {"Content-Type": content_type}, spec.endpoint, content)

    async with httpx.AsyncClient(timeout=spec.timeout_s) as client:
        resp = await client.post(spec.endpoint, content=content, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    return extract_response_text(data, spec.response_text_path)


def http_target(spec: TargetSpec) -> Task[..., str]:
    async def target(message: Message) -> str:
        return await http_call(message, spec)

    return task(target, name=spec.name)
