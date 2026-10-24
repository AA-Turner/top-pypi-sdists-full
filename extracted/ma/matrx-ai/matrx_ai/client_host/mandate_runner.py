"""The mandate runner for matrx-ai running as a CLIENT (runner plan 25, step 6).

SERVER vs CLIENT (Arman, 2026-08-16) — never "with a database" vs "without one". As a server,
aidream installs its ONE runner (``aidream.services.mandate_runner``) as matrx-ai's
:class:`~matrx_ai.mandates.MandateRunnerPort`. A client (matrx-local) has no aidream, so package
code that reaches a mandate through ``get_mandate_runner()`` — the conversation labeler, observational
memory, the judges, the summarize/research tools — needs a client runner, exactly as the tool registry
needs :class:`~matrx_ai.tools.tool_source.ServerToolSource`. This is it, installed by
``matrx_ai.configure(server_url=..., get_jwt=...)`` when the host installed no runner of its own:

* ``prepare`` / ``finish`` — a raw-request site's held call. Which Holder answers (``agent.mandate``,
  server-only) is asked over the API by the installed resolver (``ServerMandateSource``:
  ``GET {server_url}/api/mandates/{key}/resolution``, per caller); the held call itself is built and
  sent here, on the client's own providers, keys and conversation store — like every client turn.
* ``run`` — a typed NamedAgent call goes to the server's mandate door,
  ``POST {server_url}/ai/mandates/{key}`` (the door every client starts a mandated run through), with
  the offer's values; the streamed answer comes back as the class's ``AgentRunResult``.
* ``resolve`` — the resolver's answer for ``key``.

``who`` is never asserted to the server: the server reads the caller from the JWT. Its organization
rides ``X-Organization-Id`` when the carried principal names one. ``system`` is the client's own
system-job principal (no person, no organization): a client never claims the platform's SYSTEM identity.
"""

from __future__ import annotations

import inspect
import json
import uuid
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

from matrx_ai import mandates as _mandates


class MandateDoorError(RuntimeError):
    """The server's mandate door refused or failed a client run (transport, HTTP status, stream error)."""


@dataclass
class ClientPrepared:
    """A prepared client run: the held call the site sends itself."""

    mandate_key: str
    who: _mandates.Principal
    opts: _mandates.RunOptions
    held: Any

    def held_call(self) -> Any:
        return self.held


@dataclass
class ClientMandateRun:
    """One finished client mandate run (the server runner's ``MandateRun`` read surface)."""

    mandate_key: str
    door: str
    success: bool
    output: str = ""
    parsed: Any = None
    error: str | None = None
    raw: Any = None


#: The principal a client's system job carries: no person, no organization. The server assigns the
#: identity from the caller's token; a client never asserts the platform's SYSTEM principal.
CLIENT_SYSTEM = _mandates.Principal(user_id=None, org_id="")


async def _plain_values(offer: Mapping[str, Any] | None) -> dict[str, Any]:
    """The offer's values as plain values: a client has no compute-rule pipeline, so every builder runs."""
    values: dict[str, Any] = {}
    for name, value in dict(offer or {}).items():
        if isinstance(value, _mandates.Offered):
            value = await _mandates.run_offered(value)
        if value is not None:
            values[name] = value
    return values


class ServerMandateRunner:
    """:class:`~matrx_ai.mandates.MandateRunnerPort` for a CLIENT host, backed by the AIDream server."""

    system = CLIENT_SYSTEM

    def __init__(
        self,
        server_url: str,
        get_jwt: Any,
        *,
        # A server run streams a whole agent turn; a black-holed network still fails rather than hangs.
        timeout_seconds: float = 300.0,
    ) -> None:
        self._base = server_url.rstrip("/")
        self._get_jwt = get_jwt
        self._timeout = timeout_seconds

    def door_url(self, mandate_key: str) -> str:
        return f"{self._base}/ai/mandates/{quote(mandate_key, safe='')}"

    async def _headers(self, who: _mandates.Principal | None) -> dict[str, str]:
        if not callable(self._get_jwt):
            raise MandateDoorError(
                "no JWT provider is configured; a mandate run belongs to the signed-in caller, so it is never "
                "sent anonymously"
            )
        try:
            token = self._get_jwt()
            if inspect.isawaitable(token):
                token = await token
        except Exception:  # noqa: BLE001 — never expose provider values in errors
            raise MandateDoorError("JWT provider failed; refusing to run a mandate anonymously") from None
        if not isinstance(token, str) or not token:
            raise MandateDoorError("no usable JWT available; refusing to run a mandate anonymously")
        headers = {"Accept": "application/x-ndjson", "Authorization": f"Bearer {token}"}
        org_id = getattr(who, "org_id", "") or ""
        try:
            headers["X-Organization-Id"] = str(uuid.UUID(org_id))
        except ValueError:
            pass  # the client's system job names no organization; the server reads the caller's
        return headers

    # ── the held call (raw-request sites) ────────────────────────────────────────────────────

    async def prepare(
        self, key: str, offer: Mapping[str, Any] | None, *, who: _mandates.Principal, opts: _mandates.RunOptions
    ) -> ClientPrepared:
        if opts.holder is not None:
            raise MandateDoorError("a run-scope Holder override runs on the server (the try door), never on a client")
        # Looked up on the module at call time: the installed resolver (ServerMandateSource) answers which
        # Holder runs; the held call is built here from that answer.
        held = await _mandates.hold_code_call(
            key,
            consumer=opts.consumer or f"mandate_runner:{opts.door}",
            variables=await _plain_values(offer) if offer else None,
            metadata=dict(opts.metadata) if opts.metadata else None,
        )
        return ClientPrepared(mandate_key=key, who=who, opts=opts, held=held)

    async def finish(self, prepared: ClientPrepared, result: Any) -> ClientMandateRun:
        door = prepared.opts.door
        if isinstance(result, BaseException):
            error = f"{type(result).__name__}: {result}"
            await prepared.held.finish("", success=False, error=error)
            return ClientMandateRun(mandate_key=prepared.mandate_key, door=door, success=False, error=error, raw=result)
        output, parsed = _mandates.engine_output(result)
        await prepared.held.finish(output, parsed=parsed)
        return ClientMandateRun(
            mandate_key=prepared.mandate_key, door=door, success=True, output=output, parsed=parsed, raw=result
        )

    async def resolve(self, key: str, *, who: _mandates.Principal, holder: _mandates.HolderRef | None = None) -> Any:
        if holder is not None:
            # The HTTP resolver answers the ladder; a run-scope pick is the server's to apply (refused, never dropped).
            raise _mandates.MandateRunnerUnavailable(
                f"a run-scope Holder for {key!r} is resolved on the server; this client runner cannot apply it"
            )
        return await _mandates.resolve_mandate_by_key(key, consumer="mandate_runner:resolve")

    # ── a typed NamedAgent call → the server's mandate door ──────────────────────────────────

    async def run(
        self, key: str, offer: Mapping[str, Any] | None, *, who: _mandates.Principal, opts: _mandates.RunOptions
    ) -> ClientMandateRun:
        import httpx

        from matrx_ai.agents.executor import AgentRunResult

        named = getattr(offer, "named", None)
        if named is not None and named.runner is not None:
            raise MandateDoorError(
                f"{named.agent_cls.__name__} runs its own runner, which the server's mandate door cannot run"
            )
        user_input = opts.user_input
        if named is not None and user_input is None:
            user_input = named.kwargs.get("user_input")
        body: dict[str, Any] = {"variables": await _plain_values(offer), "stream": True}
        if isinstance(user_input, str) and user_input:
            body["user_input"] = user_input
        url = self.door_url(key)
        chunks: list[str] = []
        error: str | None = None
        ended = False
        try:
            async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True) as client:
                async with client.stream("POST", url, json=body, headers=await self._headers(who)) as resp:
                    if resp.status_code != 200:
                        raw = (await resp.aread()).decode("utf-8", "replace")
                        raise MandateDoorError(f"mandate door refused: POST {url} → HTTP {resp.status_code}: {raw[:500]}")
                    async for line in resp.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            event = json.loads(line)
                        except ValueError:
                            continue
                        if event.get("e") == "c":  # the compact text chunk
                            chunks.append(str(event.get("t") or ""))
                        elif event.get("event") == "error":
                            data = event.get("data") or {}
                            error = str(data.get("user_message") or data.get("message") or data or "stream error")
                        elif event.get("event") == "end":
                            ended = True
        except httpx.HTTPError as exc:
            raise MandateDoorError(f"mandate door failed: POST {url} → {type(exc).__name__}: {exc}") from exc
        if error is None and not ended:
            error = f"the mandate door stream for {key!r} did not end cleanly"
        output = "".join(chunks)
        parsed, parse_error = (None, None)
        output_cls = getattr(named.agent_cls, "Output", None) if named is not None else None
        if error is None and output_cls is not None and hasattr(output_cls, "model_validate_json"):
            try:
                parsed = output_cls.model_validate_json(output)
            except ValueError as exc:
                parse_error = str(exc)[:500]
        result = AgentRunResult(
            success=error is None,
            output=output,
            error=error,
            error_kind="execution" if error is not None else ("parse" if parse_error else None),
            parsed=parsed,
            parse_error=parse_error,
        )
        return ClientMandateRun(
            mandate_key=key, door=opts.door, success=result.success, output=output, parsed=parsed, error=error, raw=result
        )


__all__ = ["CLIENT_SYSTEM", "ClientMandateRun", "ClientPrepared", "MandateDoorError", "ServerMandateRunner"]
