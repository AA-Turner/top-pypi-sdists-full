"""Ask Agent Auth, with the pod's token, which agent this deployment runs as."""

from __future__ import annotations

import asyncio
import math
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from time import monotonic, time
from typing import TYPE_CHECKING, Any

import httpx
import jwt
import structlog

from langgraph_api import config
from langgraph_api.errors import AgentDisabledError

if TYPE_CHECKING:
    from langchain_core.runnables import RunnableConfig

logger = structlog.stdlib.get_logger(__name__)

AGENT_RUNTIME_AUDIENCE = "urn:langsmith:agent-runtime"
RUN_AGENT_IDENTIFIER = "run_agent_identifier"
_AGENT_DISABLED = "agent_disabled"
_TOKEN_EXCHANGE_GRANT_TYPE = "urn:ietf:params:oauth:grant-type:token-exchange"
_POD_TOKEN_TYPE = "urn:ietf:params:oauth:token-type:jwt"
_ACCESS_TOKEN_TYPE = "at+jwt"
_SIGNING_ALGORITHM = "RS256"
_KEY_HEADERS = ("jku", "jwk", "x5u")
_CLOCK_SKEW_SECONDS = 60
# The longest a run start waits on Agent Auth, for the token and the keys together.
_CHECK_TIMEOUT_SECONDS = 2.0
# A refusal, such as a deployment bound to no agent, lasts; ask again after a run token's lifetime.
_REFUSAL_PAUSE_SECONDS = 300.0
# An outage is short; Agent Auth's Retry-After is honoured within these bounds.
_OUTAGE_PAUSE_SECONDS = 5.0
_MAX_OUTAGE_PAUSE_SECONDS = 60.0
# A token signed by an untrusted key refetches the keys, but only once they're this old.
_KEY_REFRESH_INTERVAL_SECONDS = 30.0
# Runs reuse a verified agent this long, so a disabled agent can start runs this long after.
_VERIFIED_AGENT_TTL_SECONDS = 60.0


class AgentAuthRefused(Exception):
    """Agent Auth issued no token, either because it said no or because it couldn't answer.

    ``reason`` is its ``ls_error``, the HTTP status, or the transport error's name.
    ``outage`` is true when it couldn't answer; ``retry_after`` is how many seconds
    it then asked callers to wait.
    """

    def __init__(
        self, reason: str, *, outage: bool = False, retry_after: float | None = None
    ) -> None:
        super().__init__(reason)
        self.reason = reason
        self.outage = outage
        self.retry_after = retry_after


class _InvalidRunToken(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class _UntrustedKey(_InvalidRunToken):
    """The token's key isn't among Agent Auth's cached keys, which may be stale."""


@dataclass(frozen=True)
class _VerifiedAgent:
    identifier: str
    expires_at: float


@dataclass(frozen=True)
class _AgentAuthKeys:
    issuer: str
    keys: dict[str, jwt.PyJWK]
    fetched_at: float


_paused_until = 0.0
_verified_agent: _VerifiedAgent | None = None
_agent_auth_keys_cache: _AgentAuthKeys | None = None


async def verify_and_strip(
    config: RunnableConfig, context: Any
) -> tuple[RunnableConfig, Any, str | None]:
    """Verify this deployment's agent with Agent Auth, and strip any caller's ``run_agent_identifier``.

    Returns copies of config and context without the key, and the verified
    identifier to stamp, or None. Raises ``AgentDisabledError`` when Agent Auth
    reports the agent disabled.
    """
    run_agent_identifier = await verified_run_agent_identifier()
    config, context = _without_run_agent_identifier(config, context)
    return config, context, run_agent_identifier


def _without_run_agent_identifier(
    config: RunnableConfig, context: Any
) -> tuple[RunnableConfig, Any]:
    """Copies of a run's config and context without ``run_agent_identifier``, which only the server sets.

    The top level of config counts too: ``ensure_config`` moves unknown keys there into configurable.
    """
    config = {
        **_without_identifier(config),
        "metadata": _without_identifier(config.get("metadata") or {}),
        "configurable": _without_identifier(config.get("configurable") or {}),
    }
    if isinstance(context, dict):
        context = _without_identifier(context)
    return config, context


def _without_identifier(values: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in values.items() if k != RUN_AGENT_IDENTIFIER}


async def verified_run_agent_identifier() -> str | None:
    """The agent a verified run token from Agent Auth names, or None.

    A verified agent is reused until ``_VERIFIED_AGENT_TTL_SECONDS`` pass or its
    run token expires. Raises ``AgentDisabledError`` when Agent Auth reports the
    agent disabled.
    """
    global _verified_agent
    if not config.LANGSMITH_AGENT_AUTH_POD_TOKEN_PATH:
        return None
    verified = _verified_agent
    if verified is not None and monotonic() < verified.expires_at:
        return verified.identifier
    if monotonic() < _paused_until:
        await logger.ainfo(
            "Run agent access token check paused", agent_access_token="paused"
        )
        return None
    try:
        claims = await _fresh_run_claims()
    except AgentAuthRefused as refusal:
        if refusal.reason == _AGENT_DISABLED:
            await logger.awarning(
                "Agent Auth reports the agent disabled",
                agent_access_token=_AGENT_DISABLED,
            )
            raise AgentDisabledError from None
        _pause(
            _outage_pause(refusal.retry_after)
            if refusal.outage
            else _REFUSAL_PAUSE_SECONDS
        )
        await logger.awarning(
            "Run agent access token unavailable",
            agent_access_token="unavailable",
            agent_access_token_error=refusal.reason,
        )
        return None
    except _InvalidRunToken as invalid:
        await logger.aerror(
            "Run agent access token rejected",
            agent_access_token="invalid",
            agent_access_token_error=invalid.reason,
        )
        return None
    except Exception as error:
        _pause(_OUTAGE_PAUSE_SECONDS)
        await logger.awarning(
            "Run agent access token unavailable",
            agent_access_token="unavailable",
            agent_access_token_error=type(error).__name__,
            exc_info=error,
        )
        return None
    await logger.ainfo(
        "Run agent access token verified",
        agent_access_token="verified",
        agent_access_token_jti=claims["jti"],
    )
    _verified_agent = _VerifiedAgent(
        identifier=str(claims["sub"]),
        expires_at=monotonic()
        + min(_VERIFIED_AGENT_TTL_SECONDS, claims["exp"] - time()),
    )
    return _verified_agent.identifier


async def _fresh_run_claims() -> dict[str, Any]:
    try:
        async with asyncio.timeout(_CHECK_TIMEOUT_SECONDS):
            # A client per check: with BG_JOB_ISOLATED_LOOPS, runs start on their own event loops.
            async with httpx.AsyncClient(
                timeout=_CHECK_TIMEOUT_SECONDS, follow_redirects=False
            ) as client:
                token = await exchange_pod_token(client, AGENT_RUNTIME_AUDIENCE)
                return await _verified_claims(client, token)
    except TimeoutError:
        raise AgentAuthRefused("timeout", outage=True) from None


def _pause(seconds: float) -> None:
    global _paused_until
    _paused_until = monotonic() + seconds


def _outage_pause(retry_after: float | None) -> float:
    return min(
        max(retry_after or 0.0, _OUTAGE_PAUSE_SECONDS), _MAX_OUTAGE_PAUSE_SECONDS
    )


async def exchange_pod_token(client: httpx.AsyncClient, audience: str) -> str:
    """Trade the pod's token for an Agent Auth token for ``audience``."""
    try:
        form = await pod_token_form(audience)
    except FileNotFoundError:
        raise AgentAuthRefused("pod_token_missing") from None
    except OSError as error:
        raise AgentAuthRefused(f"pod_token_unreadable:{type(error).__name__}") from None
    body = await _agent_auth_answer(
        client, "POST", config.langsmith_api_url("/agent-auth/token"), data=form
    )
    token = body.get("access_token")
    if not isinstance(token, str) or not token:
        raise AgentAuthRefused("malformed_token_response", outage=True)
    return token


async def pod_token_form(audience: str) -> dict[str, str]:
    return {
        "grant_type": _TOKEN_EXCHANGE_GRANT_TYPE,
        "subject_token": await asyncio.to_thread(_read_pod_token),
        "subject_token_type": _POD_TOKEN_TYPE,
        "resource": audience,
    }


async def _agent_auth_answer(
    client: httpx.AsyncClient, method: str, url: str, **kwargs: Any
) -> dict[str, Any]:
    """Agent Auth's JSON answer, or ``AgentAuthRefused`` when it says no or can't answer."""
    try:
        response = await client.request(method, url, **kwargs)
    except httpx.HTTPError as error:
        raise AgentAuthRefused(type(error).__name__, outage=True) from None
    if response.status_code != httpx.codes.OK:
        raise _refusal(response)
    try:
        body = response.json()
    except ValueError:
        raise AgentAuthRefused("malformed_response", outage=True) from None
    if not isinstance(body, dict):
        raise AgentAuthRefused("malformed_response", outage=True)
    return body


def _refusal(response: httpx.Response) -> AgentAuthRefused:
    status = response.status_code
    outage = (
        status in (httpx.codes.REQUEST_TIMEOUT, httpx.codes.TOO_MANY_REQUESTS)
        or status >= 500
    )
    return AgentAuthRefused(
        _ls_error(response) or str(status),
        outage=outage,
        retry_after=_retry_after_seconds(response) if outage else None,
    )


def _retry_after_seconds(response: httpx.Response) -> float | None:
    """Retry-After in seconds, given either as seconds or as an HTTP date."""
    header = response.headers.get("Retry-After", "")
    try:
        seconds = float(header)
    except ValueError:
        try:
            seconds = (
                parsedate_to_datetime(header) - datetime.now(UTC)
            ).total_seconds()
        except (TypeError, ValueError):
            return None
    return seconds if math.isfinite(seconds) else None


def _ls_error(response: httpx.Response) -> str | None:
    try:
        body = response.json()
    except ValueError:
        return None
    value = body.get("ls_error") if isinstance(body, dict) else None
    return value if isinstance(value, str) else None


def _read_pod_token() -> str:
    # Kubernetes rotates the token in place, so read it fresh each time.
    return Path(config.LANGSMITH_AGENT_AUTH_POD_TOKEN_PATH or "").read_text().strip()


async def _verified_claims(client: httpx.AsyncClient, token: str) -> dict[str, Any]:
    """Claims checked as Agent Auth's own verifier checks them, for this deployment."""
    kid = _checked_header(token)
    try:
        claims = _decoded(token, kid, await _agent_auth_keys(client, refresh=False))
    except _UntrustedKey:
        claims = _decoded(token, kid, await _agent_auth_keys(client, refresh=True))
    for claim, expected in (
        ("ls_deployment_id", config.LANGSMITH_HOST_PROJECT_ID),
        ("ls_workspace_id", config.LANGSMITH_TENANT_ID),
    ):
        if not expected or claims.get(claim) != expected:
            raise _InvalidRunToken(f"{claim}_mismatch")
    return claims


def _checked_header(token: str) -> str:
    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError as error:
        raise _InvalidRunToken(type(error).__name__) from None
    token_type = str(header.get("typ", "")).lower().removeprefix("application/")
    if token_type != _ACCESS_TOKEN_TYPE:
        raise _InvalidRunToken("typ_not_access_token")
    if any(name in header for name in _KEY_HEADERS):
        raise _InvalidRunToken("key_header_not_allowed")
    return str(header.get("kid", ""))


def _decoded(token: str, kid: str, agent_auth: _AgentAuthKeys) -> dict[str, Any]:
    key = agent_auth.keys.get(kid)
    if key is None:
        raise _UntrustedKey("kid_not_trusted")
    try:
        return jwt.decode(
            token,
            key.key,
            algorithms=[_SIGNING_ALGORITHM],
            audience=AGENT_RUNTIME_AUDIENCE,
            issuer=agent_auth.issuer,
            leeway=_CLOCK_SKEW_SECONDS,
            options={"require": ["exp", "iat", "iss", "aud", "sub", "jti"]},
        )
    except jwt.InvalidSignatureError:
        raise _UntrustedKey("InvalidSignatureError") from None
    except jwt.InvalidTokenError as error:
        raise _InvalidRunToken(type(error).__name__) from None


async def _agent_auth_keys(
    client: httpx.AsyncClient, *, refresh: bool
) -> _AgentAuthKeys:
    """The issuer and RSA signing keys of the Agent Auth that minted the run token."""
    global _agent_auth_keys_cache
    cached = _agent_auth_keys_cache
    if cached is not None and (
        not refresh or monotonic() < cached.fetched_at + _KEY_REFRESH_INTERVAL_SECONDS
    ):
        return cached
    base = config.langsmith_api_url("/agent-auth")
    discovery = await _agent_auth_answer(
        client, "GET", f"{base}/.well-known/openid-configuration"
    )
    jwks = jwt.PyJWKSet.from_dict(
        await _agent_auth_answer(client, "GET", f"{base}/.well-known/jwks.json")
    )
    issuer = discovery.get("issuer")
    if not isinstance(issuer, str) or not issuer:
        raise AgentAuthRefused("malformed_response", outage=True)
    _agent_auth_keys_cache = _AgentAuthKeys(
        issuer=issuer,
        keys={
            key.key_id: key for key in jwks.keys if key.key_id and key.key_type == "RSA"
        },
        fetched_at=monotonic(),
    )
    return _agent_auth_keys_cache
