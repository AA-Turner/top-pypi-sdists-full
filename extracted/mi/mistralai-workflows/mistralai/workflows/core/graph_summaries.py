"""LLM-generated summaries for Atlas workflow graph nodes.

Source snippets from user workflow code are included in LLM prompts to help summarise
``unknown`` nodes.  String literal values are redacted to '...' before the snippet is
sent so that credentials or other secrets embedded as string constants do not leave the
user's environment.
"""

import asyncio
import io
import json
import re
import tokenize as _tokenize
from collections import defaultdict
from dataclasses import dataclass
from functools import cache
from typing import Literal

import structlog
from mistralai.client import Mistral
from mistralai.client.errors import MistralError
from mistralai.client.models import ChatCompletionRequestMessage, SystemMessage, UserMessage
from mistralai.client.utils import BackoffStrategy, RetryConfig
from pydantic import BaseModel, Field, RootModel, ValidationError

from mistralai.workflows.client import get_mistral_client
from mistralai.workflows.core.config import config
from mistralai.workflows.core.wire_format import AtlasWireFormat, FlatNode

logger = structlog.get_logger()


class SummariseError(Exception):
    """Raised when summarise_workflow fails after exhausting retries."""


@dataclass(frozen=True, slots=True)
class SummaryResult:
    status: Literal["ready", "disabled"]
    summaries: dict[str, "NodeSummary"]


_SKIP_TYPES = {"workflow", "entrypoint", "output"}
_SOURCE_SNIPPET_LIMIT = 600

_SYSTEM_PROMPT = (
    "You are a technical writer summarising a Mistral AI workflow graph.\n\n"
    "For each node id, produce:\n"
    '- "short": a ≤8-word noun phrase capturing what the node does '
    '(e.g. "fetch customer data", "validate payment intent").\n'
    '- "long": 1-2 sentences of prose describing the node\'s role in the workflow.\n\n'
    "Guidelines:\n"
    "- Write in present tense.\n"
    "- Focus on business/domain logic, not implementation details.\n"
    "- Do not repeat the node id or type verbatim.\n"
    "- Nodes with type=unknown represent Python code; "
    "describe what that code does based on its 'source' field. "
    "Never skip them — every node id must appear in your response.\n\n"
    "Respond with a single JSON object whose keys are node ids and whose values are "
    'objects with exactly "short" and "long" string fields.\n'
    "Only include node ids that appear in the user message."
)

_LLM_TIMEOUT_S = 60

# Transient API failures (HTTP 429 rate limits and 5xx) are retried inside the Mistral
# SDK with exponential backoff that honours any ``Retry-After`` header. Supplying a
# RetryConfig is what activates this — without one the SDK performs no retries at all.
# ``max_elapsed_time`` bounds only the cumulative backoff sleeps, not per-request time.
# Graph upload runs as a background task (see worker._run_worker), off the startup
# critical path, so we can afford a generous budget to ride out sustained rate limits.
_RETRY_MAX_ELAPSED_S = 300
_RETRY_CONFIG = RetryConfig(
    strategy="backoff",
    backoff=BackoffStrategy(
        initial_interval=500,
        max_interval=8000,
        exponent=1.5,
        max_elapsed_time=_RETRY_MAX_ELAPSED_S * 1000,
    ),
    retry_connection_errors=True,
)


# Cached so we don't rebuild the client (and its httpx clients) on every workflow
# registration. get_mistral_client resolves server_url, CA bundle, headers and hooks
# from config, so summaries share the same transport setup as every other SDK call.
@cache
def _get_client(api_key: str) -> Mistral:
    return get_mistral_client(api_key=api_key)


def _redact_string_literals(source: str) -> str:
    """Replace string literal values with '...' to avoid leaking embedded secrets."""
    try:
        tokens = []
        for tok in _tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type == _tokenize.STRING:
                tokens.append(_tokenize.TokenInfo(tok.type, "'...'", tok.start, tok.end, tok.line))
            else:
                tokens.append(tok)
        return _tokenize.untokenize(tokens)
    except (_tokenize.TokenError, SyntaxError):
        # Best-effort regex redaction for code fragments the tokenizer rejects
        # (e.g. bare elif blocks). Handles triple-quoted, escaped, and simple strings.
        s = re.sub(r'"""[\s\S]*?"""', "'...'", source)
        s = re.sub(r"'''[\s\S]*?'''", "'...'", s)
        s = re.sub(r'"(?:[^"\\]|\\.)*"', "'...'", s)
        s = re.sub(r"'(?:[^'\\]|\\.)*'", "'...'", s)
        return s


class NodeSummary(BaseModel):
    long: str = Field(max_length=500)
    short: str = Field(max_length=80)


class WorkflowSummaries(RootModel[dict[str, NodeSummary]]):
    pass


def _bottom_up_order(nodes: list[FlatNode]) -> list[FlatNode]:
    """Return nodes in post-order so leaves appear before their containers."""
    node_by_id = {n.id: n for n in nodes}
    children_map: dict[str, list[str]] = defaultdict(list)

    for node in nodes:
        for child_id in node.children or []:
            children_map[node.id].append(child_id)
        for arm in node.branches or []:
            for child_id in arm:
                children_map[node.id].append(child_id)

    all_children: set[str] = {cid for cids in children_map.values() for cid in cids}
    roots = [n.id for n in nodes if n.id not in all_children]

    visited: set[str] = set()
    result: list[FlatNode] = []

    for rid in roots:
        if rid in visited:
            continue
        # Iterative post-order: push (nid, done) pairs; emit node when done=True.
        stack: list[tuple[str, bool]] = [(rid, False)]
        while stack:
            nid, done = stack.pop()
            if done:
                if nid in node_by_id:
                    result.append(node_by_id[nid])
            elif nid not in visited:
                visited.add(nid)
                stack.append((nid, True))
                for cid in children_map.get(nid, []):
                    if cid in node_by_id and cid not in visited:
                        stack.append((cid, False))

    for node in nodes:
        if node.id not in visited:
            result.append(node)

    return result


def _serialize_node(node: FlatNode, source_bytes: bytes | None = None) -> str:
    is_unknown = node.type == "unknown"
    lines = [
        f"--- node: {node.id} ---",
        f"type: {node.type}",
        f"name: {node.name if not is_unknown else '(unrecognised code)'}",
    ]
    if node.callees:
        lines.append(f"calls: {', '.join(node.callees)}")
    if node.dispatch_label:
        lines.append(f"dispatch: {node.dispatch_label}")
    if is_unknown and source_bytes is not None:
        sr = node.source_range
        if sr:
            snippet = source_bytes[sr.begin : sr.end].decode("utf-8", errors="replace")
            snippet = _redact_string_literals(snippet)
            if len(snippet) > _SOURCE_SNIPPET_LIMIT:
                snippet = snippet[:_SOURCE_SNIPPET_LIMIT] + "…"
            lines.append(f"source:\n{snippet.strip()}")
    lines.append("---")
    return "\n".join(lines)


def _concatenate_source_bytes(wire: AtlasWireFormat) -> bytes | None:
    """Reconstruct the concatenated source blob from per-file ``sources`` + ``files``."""
    sources = wire.sources
    files = wire.files
    if not sources or not files:
        return None
    ordered = sorted(files.items(), key=lambda kv: kv[1].begin)
    return b"".join(sources.get(path, "").encode("utf-8") for path, _ in ordered)


def _build_user_message(wire: AtlasWireFormat) -> str:
    nodes = wire.nodes
    source_bytes = _concatenate_source_bytes(wire)
    ordered = _bottom_up_order(nodes)
    filtered = [n for n in ordered if n.type not in _SKIP_TYPES]
    if not filtered:
        return ""
    blocks = "\n\n".join(_serialize_node(n, source_bytes) for n in filtered)
    return f"Workflow: {wire.workflow_name}\n\n{blocks}"


async def summarise_workflow(wire: AtlasWireFormat) -> SummaryResult:
    """Call the Mistral API to generate summaries for non-skipped nodes.

    Returns a SummaryResult with status ``"disabled"`` when no API key is configured,
    or ``"ready"`` with the (possibly empty) summaries dict on success.
    Raises SummariseError when the API call fails after all retries.
    """
    if not config.worker.graph.graph_summarise_enabled:
        return SummaryResult(status="disabled", summaries={})

    api_key_secret = config.common.mistral_api_key
    api_key = api_key_secret.get_secret_value() if api_key_secret else None
    if not api_key:
        return SummaryResult(status="disabled", summaries={})

    user_msg = _build_user_message(wire)
    if not user_msg:
        return SummaryResult(status="ready", summaries={})

    model = config.worker.graph.graph_summarise_model
    client = _get_client(api_key)

    logger.info(
        "Generating workflow node summaries",
        workflow_name=wire.workflow_name,
        model=model,
    )

    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            msgs: list[ChatCompletionRequestMessage] = [
                SystemMessage(content=_SYSTEM_PROMPT),
                UserMessage(content=user_msg),
            ]
            response = await asyncio.wait_for(
                client.chat.complete_async(
                    model=model,
                    temperature=0.1,
                    response_format={"type": "json_object"},
                    messages=msgs,
                    retries=_RETRY_CONFIG,
                ),
                # The ceiling must cover the SDK's internal retry/backoff budget so it
                # does not cancel legitimate 429/5xx retries before they complete.
                timeout=_LLM_TIMEOUT_S + _RETRY_MAX_ELAPSED_S,
            )
            message = response.choices[0].message if response.choices else None
            content = message.content if message is not None else None
            if not isinstance(content, str):
                raise ValueError("Unexpected non-string content from LLM response")
            raw = json.loads(content)
            return SummaryResult(status="ready", summaries=WorkflowSummaries.model_validate(raw).root)
        except (ValidationError, json.JSONDecodeError) as exc:
            last_exc = exc
            logger.warning("LLM summary validation failed", attempt=attempt + 1, exc_info=exc)
        except Exception as exc:
            # 429/5xx are already retried with backoff inside the SDK; reaching here means
            # the rate limit persisted past the retry budget. Log it distinctly so the
            # exhausted-retry case is visible rather than blending into generic API errors.
            if isinstance(exc, MistralError) and exc.status_code == 429:
                logger.warning("LLM summary rate-limited after retries", exc_info=exc)
            else:
                logger.warning("LLM summary API error", exc_info=exc)
            raise SummariseError(f"LLM API error: {exc}") from exc

    logger.warning("LLM summary failed after 3 attempts", exc_info=last_exc)
    raise SummariseError(f"Validation failed after 3 attempts: {last_exc}")
