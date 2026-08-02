"""Bedrock model wrapper that enables Anthropic-style prompt caching.

agno's stock :class:`~agno.models.aws.bedrock.AwsBedrock` (boto3 ``converse``)
reads ``cacheReadInputTokens`` / ``cacheWriteInputTokens`` from responses but
never emits a ``cachePoint`` block, so nothing is ever cached. Without caching,
the large static prefix (system prompt + tool definitions) is re-billed at full
input price on every turn of an agentic run — the root cause of runaway run
costs on Bedrock.

This subclass injects a ``cachePoint`` breakpoint into the ``system`` block and
the ``toolConfig.tools`` list so the static prefix is cached. It keeps the
bearer-token (``AWS_BEARER_TOKEN_BEDROCK``) auth path unchanged — unlike
``agno.models.aws.claude.Claude``, which requires IAM credentials.

Bedrock rejects ``cachePoint`` on models that do not support prompt caching, so
injection is gated to Claude / Nova model ids.
"""

from os import getenv
from typing import Any, Dict, List, Optional, Tuple

from boto3 import client as AwsClient
from botocore.config import Config as BotocoreConfig

from agno.models.aws.bedrock import AwsBedrock
from agno.models.message import Message
from agno.utils.log import log_error

from xpander_sdk.modules.backend.frameworks._cache_split import (
    resolve_volatile,
    split_system_text,
)
from xpander_sdk.modules.backend.utils.prompt_budget import log_wire_budget

# Bedrock model families that accept a ``cachePoint`` block.
_CACHE_SUPPORTED_MODELS = ("claude", "nova")

_CACHE_POINT = {"cachePoint": {"type": "default"}}

# Bedrock Converse rejects any ``{"text": ""}`` (empty / whitespace-only) content
# block with ``ValidationException: messages: text content blocks must be
# non-empty``. agno's serializer can emit these for a user/assistant message
# whose ``content`` is an empty string and which has no tool_calls/images. It
# also rejects an empty ``content`` array, so a block dropped down to nothing
# must be backfilled with a minimal placeholder.
_EMPTY_TEXT_PLACEHOLDER = {"text": "."}


def _is_empty_text_block(block: Any) -> bool:
    """True for a ``{"text": ...}`` block whose value is empty / whitespace-only."""
    if not isinstance(block, dict) or "text" not in block:
        return False
    value = block["text"]
    return value is None or str(value).strip() == ""


def _sanitize_empty_text_blocks(content_blocks: Any) -> None:
    """Drop empty text blocks from a Converse content list, in place.

    Removes every ``{"text": ""}`` / whitespace-only text block. If that empties
    the list, leaves a single minimal placeholder so Bedrock does not reject an
    empty ``content`` array. Non-text blocks (toolUse, toolResult, json, image,
    document) are left untouched.
    """
    if not isinstance(content_blocks, list):
        return
    kept = [b for b in content_blocks if not _is_empty_text_block(b)]
    if not kept:
        kept = [dict(_EMPTY_TEXT_PLACEHOLDER)]
    content_blocks[:] = kept


# Bedrock ``converse`` is non-streaming: the socket read blocks until the FULL
# response body lands, which on large structured-output / big-context turns
# easily exceeds botocore's 60s default read_timeout -> "Read timeout on
# endpoint URL". agno's stock AwsBedrock builds its boto3/aioboto3 client with
# no botocore Config, so that 60s default applies and its retry layer just
# re-hits the same wall. Mirror the 12h read budget the other providers use
# (agno.py LLM_REQUEST_TIMEOUT_SECONDS); keep a short connect budget since
# establishing the TCP/TLS connection should be fast. Defined locally (not
# imported from agno.py) to avoid a circular import — agno.py imports this
# module.
BEDROCK_READ_TIMEOUT_SECONDS = 12 * 60 * 60  # 43200s, matches other providers
BEDROCK_CONNECT_TIMEOUT_SECONDS = 60


def _split_system_blocks(
    blocks: List[Dict[str, Any]], volatile: Optional[str]
) -> List[Dict[str, Any]]:
    """Insert a cachePoint between the stable instructions and the per-request tail.

    Returns *blocks* untouched when there is nothing worth splitting; the
    concatenated text is identical either way. A split request sits at the
    four-breakpoint ceiling (tools, system-stable, system-tail, last message) —
    do not add a fifth.
    """
    for position, block in enumerate(blocks):
        if not isinstance(block, dict):
            continue
        split = split_system_text(block.get("text"), volatile)
        if not split:
            continue
        stable, tail = split
        return (
            blocks[:position]
            + [{"text": stable}, dict(_CACHE_POINT), {"text": tail}]
            + blocks[position + 1 :]
        )
    return blocks


def _bedrock_client_config() -> BotocoreConfig:
    """botocore Config lifting the per-request read timeout off the 60s default.

    retries are left at the botocore default — agno's ``Model.retries`` (3, with
    exponential backoff) already owns provider-level retry; we only lift the
    per-attempt timeout so a single long call doesn't trip the 60s wall.
    """
    return BotocoreConfig(
        read_timeout=BEDROCK_READ_TIMEOUT_SECONDS,
        connect_timeout=BEDROCK_CONNECT_TIMEOUT_SECONDS,
    )


class CachingAwsBedrock(AwsBedrock):
    """``AwsBedrock`` that caches the static prefix (system + tools)."""

    # Per-request system tail, set by the agno builder once additional_context is
    # final. Splitting on it keeps the stable instructions cacheable across turns.
    xp_volatile_system: Optional[str] = None

    def get_client(self) -> AwsClient:
        """Build the sync bedrock-runtime client with a lifted read timeout.

        Faithful copy of ``AwsBedrock.get_client`` (agno 2.5.14) with
        ``config=_bedrock_client_config()`` injected into every client
        constructor. We can't call ``super()`` and retrofit the config: the base
        returns an already-built client with no seam to attach a Config. Keeps
        the bearer-token (``AWS_BEARER_TOKEN_BEDROCK``) auth path unchanged.
        """
        # When using a boto3 session, always recreate the client so
        # session credentials can be refreshed (IAM roles, EKS, STS).
        if not self.session and self.client is not None:
            return self.client

        # Return directly (not via self.client) so concurrent callers
        # on the same model instance each get their own client.
        if self.session:
            return self.session.client(
                "bedrock-runtime",
                region_name=self.aws_region or self.session.region_name,
                config=_bedrock_client_config(),
            )

        self.aws_access_key_id = self.aws_access_key_id or getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = self.aws_secret_access_key or getenv(
            "AWS_SECRET_ACCESS_KEY"
        )
        self.aws_session_token = self.aws_session_token or getenv("AWS_SESSION_TOKEN")
        self.aws_region = self.aws_region or getenv("AWS_REGION")

        if self.aws_sso_auth:
            self.client = AwsClient(
                service_name="bedrock-runtime",
                region_name=self.aws_region,
                config=_bedrock_client_config(),
            )
        else:
            if not self.aws_access_key_id or not self.aws_secret_access_key:
                # Bearer-token auth (AWS_BEARER_TOKEN_BEDROCK) has no access/secret
                # key, so this branch is expected for our default path — log at the
                # same level agno does but don't treat it as fatal.
                log_error(
                    "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and "
                    "AWS_SECRET_ACCESS_KEY environment variables or provide a boto3 "
                    "session."
                )

            self.client = AwsClient(
                service_name="bedrock-runtime",
                region_name=self.aws_region,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                aws_session_token=self.aws_session_token,
                config=_bedrock_client_config(),
            )
        return self.client

    def get_async_client(self):
        """Build the async bedrock-runtime client with a lifted read timeout.

        Faithful copy of ``AwsBedrock.get_async_client`` (agno 2.5.14) with
        ``config=_bedrock_client_config()`` injected. This is the path that
        matters most: the SDK's default agno run is async, so the observed
        read-timeouts originate here. aioboto3's ``session.client`` forwards
        ``config`` to botocore.
        """
        try:
            import aioboto3
        except ImportError:
            raise ImportError(
                "`aioboto3` not installed. Please install using `pip install "
                "aioboto3` for async support."
            )

        # When using a boto3 session, create the aioboto3 session from it
        # so that session credentials (IAM roles, EKS, STS) are respected.
        if self.session:
            credentials = self.session.get_credentials()
            if credentials is None:
                raise ValueError(
                    "boto3 session has no credentials. Check your AWS configuration "
                    "(environment variables, config files, IAM role, etc.)."
                )
            # Use local variables (not self.async_session) so concurrent
            # callers each get their own session and client.
            frozen = credentials.get_frozen_credentials()
            async_session = aioboto3.Session(
                aws_access_key_id=frozen.access_key,
                aws_secret_access_key=frozen.secret_key,
                aws_session_token=frozen.token,
                region_name=self.aws_region or self.session.region_name,
            )
            return async_session.client(
                "bedrock-runtime", config=_bedrock_client_config()
            )

        if self.async_session is None:
            self.aws_access_key_id = self.aws_access_key_id or getenv(
                "AWS_ACCESS_KEY_ID"
            )
            self.aws_secret_access_key = self.aws_secret_access_key or getenv(
                "AWS_SECRET_ACCESS_KEY"
            )
            self.aws_session_token = self.aws_session_token or getenv(
                "AWS_SESSION_TOKEN"
            )
            self.aws_region = self.aws_region or getenv("AWS_REGION")

            self.async_session = aioboto3.Session()

        client_kwargs: Dict[str, Any] = {
            "service_name": "bedrock-runtime",
            "region_name": self.aws_region,
            "config": _bedrock_client_config(),
        }

        if self.aws_sso_auth:
            pass
        else:
            if not self.aws_access_key_id or not self.aws_secret_access_key:
                import os

                env_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
                env_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
                env_session_token = os.environ.get("AWS_SESSION_TOKEN")
                env_region = os.environ.get("AWS_REGION")

                if env_access_key and env_secret_key:
                    self.aws_access_key_id = env_access_key
                    self.aws_secret_access_key = env_secret_key
                    self.aws_session_token = env_session_token
                    if env_region:
                        self.aws_region = env_region
                        client_kwargs["region_name"] = self.aws_region

            if self.aws_access_key_id and self.aws_secret_access_key:
                client_kwargs["aws_access_key_id"] = self.aws_access_key_id
                client_kwargs["aws_secret_access_key"] = self.aws_secret_access_key
                if self.aws_session_token:
                    client_kwargs["aws_session_token"] = self.aws_session_token

        return self.async_session.client(**client_kwargs)

    def _supports_cache(self) -> bool:
        model_id = (self.id or "").lower()
        return any(name in model_id for name in _CACHE_SUPPORTED_MODELS)

    def _format_messages(
        self, messages: List[Message], compress_tool_results: bool = False
    ) -> Tuple[List[Dict[str, Any]], Optional[List[Dict[str, Any]]]]:
        formatted_messages, system_message = super()._format_messages(
            messages, compress_tool_results=compress_tool_results
        )
        # Strip empty text blocks before they reach Bedrock — see
        # _sanitize_empty_text_blocks for the ValidationException it prevents.
        for formatted in formatted_messages:
            _sanitize_empty_text_blocks(formatted.get("content"))
        _sanitize_empty_text_blocks(system_message)
        if system_message and self._supports_cache():
            # Interior breakpoint first: it survives a changing per-request tail,
            # where the trailing one only holds across a single arun's tool calls.
            system_message = _split_system_blocks(
                list(system_message), resolve_volatile(self.xp_volatile_system)
            )
            # Cache everything up to and including the system block.
            system_message = system_message + [_CACHE_POINT]
        # Stash only - agno formats messages BEFORE tools, so emitting here would
        # always report zero tools and the fingerprint dedup would pin that first
        # wrong line for the whole run.
        self._xp_wire_system = "".join(
            b.get("text", "")
            for b in (system_message or [])
            if isinstance(b, dict) and "text" in b
        )
        if formatted_messages and self._supports_cache():
            # Rolling breakpoint on the last message caches the growing conversation
            # prefix too (system + tools are covered above); Bedrock reads the longest
            # previously-cached prefix, so each turn reads the prior turn's write.
            last_content = formatted_messages[-1].get("content")
            if isinstance(last_content, list):
                last_content.append(dict(_CACHE_POINT))
        return formatted_messages, system_message

    def _format_tools_for_request(
        self, tools: Optional[List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        parsed_tools = super()._format_tools_for_request(tools)
        # Emit here, not in _format_messages: this runs second, so it is the first
        # point that holds both halves of what the provider is actually billed for.
        log_wire_budget(
            provider="bedrock",
            system_text=getattr(self, "_xp_wire_system", "") or "",
            tools=parsed_tools,
        )
        if parsed_tools and self._supports_cache():
            # Cache the (static) tool definitions too.
            parsed_tools = list(parsed_tools) + [_CACHE_POINT]
        return parsed_tools
