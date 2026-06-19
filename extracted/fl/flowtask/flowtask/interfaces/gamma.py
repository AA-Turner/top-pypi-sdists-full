"""
gamma.py — Async client for the Gamma.app public GraphQL API.

Provides GammaClient (cookie warm-up, GetCurrentPage, GetSnapshot),
the ProseMirror-style JSON → Markdown parser, and extract_doc_id().
"""
import re
import json
import logging
from typing import Optional

import aiohttp
from aiohttp import CookieJar, ClientSession

from ..exceptions import ComponentError
from .credentials import CredentialsInterface


logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────

GRAPHQL_URL = "https://api.gamma.app/graphql"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:151.0) Gecko/20100101 Firefox/151.0"
)

QUERY_CURRENT_PAGE = """
query GetCurrentPage($id: ID!, $password: String) {
  currentPage(id: $id, password: $password) {
    file { title __typename }
    page { id title currentSnapshotId __typename }
    __typename
  }
}
"""

QUERY_SNAPSHOT = """
query GetSnapshot($snapshotId: ID!, $password: String) {
  snapshot(id: $snapshotId, password: $password) {
    id content schemaVersion __typename
  }
}
"""

_WARMUP_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
}

_GQL_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "*/*",
    "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
    "content-type": "application/json",
    "share-token": "",
    "Origin": "https://gamma.app",
    "Referer": "https://gamma.app/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def extract_doc_id(url_or_slug: str) -> str:
    """Extract the Gamma document ID from a full URL or bare slug.

    Args:
        url_or_slug: Full Gamma URL or bare document slug.

    Returns:
        The trailing alphanumeric token (≥10 chars) from the path, or the
        entire slug if no such token is found.

    Examples:
        >>> extract_doc_id("https://gamma.app/docs/My-Doc-0aituhbc1mupp5b")
        '0aituhbc1mupp5b'
        >>> extract_doc_id("My-Doc-0aituhbc1mupp5b")
        '0aituhbc1mupp5b'
    """
    path = url_or_slug.split("?")[0].split("#")[0]
    slug = path.rstrip("/").split("/")[-1]
    match = re.search(r"([a-z0-9]{10,})$", slug)
    return match.group(1) if match else slug


# ── Parser ─────────────────────────────────────────────────────────────────────

def text_from_inline(nodes: list) -> str:
    """Render a list of ProseMirror inline nodes to a Markdown string.

    Args:
        nodes: List of inline node dicts from the snapshot content.

    Returns:
        Markdown-formatted string with bold, italic, code marks applied.
    """
    parts = []
    for node in nodes:
        t = node.get("type", "")
        if t == "text":
            raw = node.get("text", "")
            marks = {m["type"] for m in node.get("marks", [])}
            if "bold" in marks and "italic" in marks:
                raw = f"***{raw}***"
            elif "bold" in marks:
                raw = f"**{raw}**"
            elif "italic" in marks:
                raw = f"*{raw}*"
            elif "code" in marks:
                raw = f"`{raw}`"
            parts.append(raw)
        elif t == "emoji":
            parts.append(node.get("attrs", {}).get("native", ""))
        elif t == "hardBreak":
            parts.append("\n")
    return "".join(parts)


def node_to_md(node: dict, depth: int = 0) -> str:
    """Recursively convert a ProseMirror-style snapshot node to Markdown.

    Args:
        node: A snapshot content node dict.
        depth: Current nesting depth (used for layout cells).

    Returns:
        Markdown string for this node and all its descendants.
    """
    t = node.get("type", "")
    content = node.get("content", [])
    attrs = node.get("attrs", {})
    lines = []

    if t == "document":
        for child in content:
            lines.append(node_to_md(child, depth))

    elif t == "card":
        lines.append("\n---\n")
        for child in content:
            lines.append(node_to_md(child, depth))

    elif t in ("cardLayoutItem", "cardAccentLayoutItem", "gridCell"):
        for child in content:
            lines.append(node_to_md(child, depth))

    elif t == "heading":
        level = attrs.get("level", 1)
        text = text_from_inline(content)
        lines.append(f"{'#' * level} {text}\n")

    elif t == "paragraph":
        text = text_from_inline(content)
        if text.strip():
            lines.append(f"{text}\n")

    elif t == "bullet":
        text = text_from_inline(content)
        indent = "  " * attrs.get("indent", 0)
        lines.append(f"{indent}- {text}")

    elif t == "blockquote":
        for child in content:
            inner = node_to_md(child, depth).strip()
            for line in inner.splitlines():
                lines.append(f"> {line}")
        lines.append("")

    elif t == "calloutBox":
        variant = attrs.get("variant", "info")
        icon = {
            "info": "ℹ️",
            "warning": "⚠️",
            "danger": "🚫",
            "success": "✅",
        }.get(variant, "💬")
        for child in content:
            inner = node_to_md(child, depth).strip()
            lines.append(f"> {icon} {inner}\n")

    elif t == "labelGroup":
        labels = []
        for child in content:
            if child.get("type") == "label":
                labels.append(text_from_inline(child.get("content", [])))
        if labels:
            lines.append("**" + "** · **".join(labels) + "**\n")

    elif t == "label":
        text = text_from_inline(content)
        lines.append(f"**{text}**")

    elif t in ("smartLayout", "gridLayout"):
        for child in content:
            lines.append(node_to_md(child, depth + 1))

    elif t == "smartLayoutCell":
        cell_lines = []
        for child in content:
            cell_lines.append(node_to_md(child, depth))
        combined = "\n".join(ln for ln in cell_lines if ln.strip())
        if combined.strip():
            lines.append(combined + "\n")

    elif t == "smartDiagram":
        data = attrs.get("data", {})
        steps = data.get("step", [])
        if steps:
            lines.append("**Diagrama:**\n")
            for i, step in enumerate(steps, 1):
                text = re.sub(r"<[^>]+>", " ", step.get("text", "")).strip()
                text = re.sub(r"\s+", " ", text)
                lines.append(f"{i}. {text}")
            lines.append("")

    elif t == "codeBlock":
        lang = attrs.get("language", "")
        code = text_from_inline(content)
        lines.append(f"```{lang}\n{code}\n```\n")

    elif t == "horizontalRule":
        lines.append("---\n")

    else:
        for child in content:
            lines.append(node_to_md(child, depth))

    return "\n".join(ln for ln in lines if ln is not None)


def snapshot_to_markdown(title: str, snapshot_content: dict) -> str:
    """Convert a Gamma snapshot content dict to a Markdown document.

    Args:
        title: Document title used as the top-level H1 heading.
        snapshot_content: Decoded snapshot content dict. May be nested under
            a ``"default"`` key, as returned by some Gamma document versions.

    Returns:
        A Markdown string ending with a single newline, with runs of three or
        more consecutive blank lines collapsed to two.
    """
    doc_node = snapshot_content.get("default", snapshot_content)
    md_parts = [f"# {title}\n"]
    for node in doc_node.get("content", []):
        md_parts.append(node_to_md(node))
    md = "\n".join(md_parts)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


# ── GammaClient ────────────────────────────────────────────────────────────────

class GammaClient(CredentialsInterface):
    """Async client for the Gamma.app public GraphQL API.

    Handles Cloudflare cookie warm-up, document metadata retrieval
    (``GetCurrentPage``) and snapshot download (``GetSnapshot``).
    All HTTP traffic goes through a single ``aiohttp.ClientSession``
    backed by a shared ``CookieJar``.

    Inherits from ``CredentialsInterface`` so that ``DownloadFromBase.start()``
    can call ``processing_credentials()``; Gamma requires no credentials for
    public documents, so the inherited no-op is sufficient.

    Intended to be used as a mixin with ``DownloadFromBase``::

        class DownloadFromGamma(GammaClient, DownloadFromBase):
            ...
    """

    def __init__(self, *args, **kwargs) -> None:
        self._gamma_jar: CookieJar = CookieJar(unsafe=True)
        self._gamma_session: Optional[ClientSession] = None
        super().__init__(*args, **kwargs)

    async def _get_gamma_session(self) -> ClientSession:
        """Return (or lazily create) the shared aiohttp session.

        Returns:
            An open ``aiohttp.ClientSession`` with the shared cookie jar.
        """
        if self._gamma_session is None or self._gamma_session.closed:
            self._gamma_session = ClientSession(cookie_jar=self._gamma_jar)
        return self._gamma_session

    async def warm_up(self, url: str) -> None:
        """Visit the public Gamma URL to harvest Cloudflare session cookies.

        Failures are silently logged at DEBUG level; the GraphQL calls are
        attempted regardless, matching the behaviour of the reference script.

        Args:
            url: Full public URL of the Gamma document.
        """
        session = await self._get_gamma_session()
        try:
            async with session.get(
                url,
                headers=_WARMUP_HEADERS,
                allow_redirects=True,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                await resp.read()
                logger.debug(
                    "GammaClient.warm_up: %s → HTTP %s", url, resp.status
                )
        except Exception as exc:
            logger.debug("GammaClient.warm_up: tolerated error for %s: %s", url, exc)

    async def _graphql(self, query: str, variables: dict) -> dict:
        """Execute a GraphQL POST against the Gamma API.

        Args:
            query: GraphQL query string.
            variables: Query variables dict.

        Returns:
            Parsed JSON response dict.

        Raises:
            ComponentError: On HTTP 403 or any non-2xx response.
        """
        session = await self._get_gamma_session()
        payload = json.dumps({"query": query, "variables": variables}).encode()
        try:
            async with session.post(
                GRAPHQL_URL,
                data=payload,
                headers=_GQL_HEADERS,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status == 403:
                    raise ComponentError(
                        "DownloadFromGamma: document is not publicly accessible (HTTP 403)"
                    )
                resp.raise_for_status()
                return await resp.json(content_type=None)
        except ComponentError:
            raise
        except aiohttp.ClientResponseError as exc:
            raise ComponentError(
                f"DownloadFromGamma: HTTP {exc.status} from Gamma API"
            ) from exc
        except Exception as exc:
            raise ComponentError(
                f"DownloadFromGamma: error calling Gamma API: {exc}"
            ) from exc

    async def get_document(self, doc_id: str) -> dict:
        """Fetch document metadata via the ``GetCurrentPage`` GraphQL query.

        Args:
            doc_id: Gamma document ID (the trailing token from the URL slug).

        Returns:
            Dict with ``title`` (str) and ``snapshot_id`` (str).

        Raises:
            ComponentError: If the GraphQL response contains errors.
        """
        resp = await self._graphql(QUERY_CURRENT_PAGE, {"id": doc_id})
        if "errors" in resp:
            msg = "; ".join(e.get("message", str(e)) for e in resp["errors"])
            raise ComponentError(f"DownloadFromGamma: GraphQL error — {msg}")
        page_data = resp["data"]["currentPage"]
        return {
            "title": page_data["file"]["title"],
            "snapshot_id": page_data["page"]["currentSnapshotId"],
        }

    async def get_snapshot(self, snapshot_id: str) -> dict:
        """Fetch and decode the document snapshot via ``GetSnapshot``.

        Args:
            snapshot_id: Snapshot ID returned by ``get_document()``.

        Returns:
            Decoded snapshot content dict (unwrapped from ``"default"`` key
            if present).

        Raises:
            ComponentError: If the GraphQL response contains errors or the
                document is not publicly accessible (HTTP 403).
        """
        resp = await self._graphql(QUERY_SNAPSHOT, {"snapshotId": snapshot_id})
        if "errors" in resp:
            msg = "; ".join(e.get("message", str(e)) for e in resp["errors"])
            raise ComponentError(f"DownloadFromGamma: GraphQL error — {msg}")
        raw_content = resp["data"]["snapshot"]["content"]
        if isinstance(raw_content, str):
            raw_content = json.loads(raw_content)
        return raw_content

    async def close(self) -> None:
        """Close the underlying aiohttp session.

        Returns:
            None
        """
        if self._gamma_session and not self._gamma_session.closed:
            await self._gamma_session.close()
            self._gamma_session = None
