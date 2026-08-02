"""Builtin web_fetch tool for the Vibe SDK."""

from functools import cache
from typing import Any

import httpx

from mistralai.vibe.sdk.capabilities import tool
from mistralai.vibe.sdk.capabilities.builtins.web_fetch.types import WebFetchArgs, WebFetchResult
from mistralai.vibe.sdk.capabilities.http import build_ssl_context

MAX_CONTENT_BYTES = 120_000
_HONEST_USER_AGENT = "vibe-cli"
_HTTP_FORBIDDEN = 403
_DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


@tool(
    name="web_fetch",
    description="Fetch content from a URL. Converts HTML to markdown for readability.",
    input_schema=WebFetchArgs,
)
async def web_fetch(args: WebFetchArgs) -> WebFetchResult:
    content, content_type, download_was_truncated = await _fetch_url(args.url, args.timeout)

    if "text/html" in content_type:
        content = html_to_markdown(content)

    content_bytes = content.encode("utf-8")
    output_was_truncated = len(content_bytes) > MAX_CONTENT_BYTES
    if output_was_truncated:
        content = content_bytes[:MAX_CONTENT_BYTES].decode("utf-8", errors="ignore")

    was_truncated = download_was_truncated or output_was_truncated
    if was_truncated:
        content += "\n\n[Content truncated due to size limit]"

    return WebFetchResult(
        url=args.url,
        content=content,
        content_type=content_type,
        was_truncated=was_truncated,
    )


async def _fetch_url(url: str, timeout: int) -> tuple[str, str, bool]:
    headers = {
        "User-Agent": _DEFAULT_USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }

    try:
        content_bytes, content_type, was_truncated = await _do_fetch(url, timeout, headers)
    except httpx.TimeoutException:
        raise ValueError(f"Request timed out after {timeout} seconds") from None
    except httpx.RequestError as exc:
        raise ValueError(f"Failed to fetch URL: {exc}") from exc

    content = content_bytes.decode("utf-8", errors="ignore")
    return content, content_type, was_truncated


async def _do_fetch(
    url: str,
    timeout: int,
    headers: dict[str, str],
) -> tuple[bytes, str, bool]:
    async with httpx.AsyncClient(
        follow_redirects=True,
        timeout=httpx.Timeout(timeout),
        verify=build_ssl_context(),
    ) as client:
        async with client.stream("GET", url, headers=headers) as response:
            if (
                response.status_code == _HTTP_FORBIDDEN
                and response.headers.get("cf-mitigated") == "challenge"
            ):
                headers["User-Agent"] = _HONEST_USER_AGENT
            else:
                return await _read_response(response)

        async with client.stream("GET", url, headers=headers) as response:
            return await _read_response(response)


async def _read_response(response: httpx.Response) -> tuple[bytes, str, bool]:
    if response.is_error:
        raise ValueError(f"HTTP error {response.status_code}: {response.reason_phrase}")

    chunks: list[bytes] = []
    total_bytes = 0
    byte_limit_with_sentinel = MAX_CONTENT_BYTES + 1

    async for chunk in response.aiter_bytes():
        if not chunk:
            continue

        remaining = byte_limit_with_sentinel - total_bytes
        if remaining <= 0:
            break

        chunks.append(chunk[:remaining])
        total_bytes += min(len(chunk), remaining)

        if total_bytes > MAX_CONTENT_BYTES:
            break

    content = b"".join(chunks)
    content_type = response.headers.get("Content-Type", "text/plain")
    if len(content) <= MAX_CONTENT_BYTES:
        return content, content_type, False
    return content[:MAX_CONTENT_BYTES], content_type, True


@cache
def _make_converter_class() -> type[Any]:
    from markdownify import MarkdownConverter

    class _Converter(MarkdownConverter):  # type: ignore[misc]
        convert_script = convert_style = convert_noscript = convert_iframe = convert_object = (
            convert_embed
        ) = lambda *_, **__: ""

    return _Converter


def html_to_markdown(html: str) -> str:
    converter_class = _make_converter_class()
    return converter_class(heading_style="ATX", bullets="-").convert(html)
