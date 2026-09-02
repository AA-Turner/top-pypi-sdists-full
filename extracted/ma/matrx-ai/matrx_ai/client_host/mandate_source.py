"""Mandate resolution for matrx-ai running as a CLIENT.

THE DISTINCTION THAT MATTERS (Arman, 2026-08-16): there is no "with a database"
vs "without a database" mode. matrx-ai ALWAYS has a database and everything
always persists. The distinction is **running as a SERVER vs running as a
CLIENT**. As a server it reads platform tables through the ORM. As a client
(inside matrx-local) it has full access to its own client-side data — its own
database — but cannot reach server-only tables directly, so it does over an API
exactly what it would otherwise do over the ORM.

`agent.mandate` is server-only. Before this module a client had no way
to ask which agent a mandate points at, so `run_mandated` fell back to an id frozen
in the class body — a paid call against an agent nobody chose. That fallback is
deleted (`MandateResolutionUnavailable`), and this is its replacement: the client
asks the server the same question the server asks itself, and gets the same
answer through the same precedence (system default -> org binding -> user
binding). A user's rebind reaches the desktop app with no deploy, which is the
whole promise of mandates.

Wire it with ``matrx_ai.configure(server_url=..., get_jwt=...)`` — that install
is automatic; see ``matrx_ai.configure``.
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from matrx_ai.agents.named import AgentRecordSource
from matrx_ai.mandates import MandateResolution, OfferedValueSpec


class MandateSourceFetchError(RuntimeError):
    """A server-backed mandate resolution failed (network / HTTP / payload shape).

    Raised, never swallowed: ``run_mandated`` turns it into the same loud
    ``MandateResolutionUnavailable`` refusal a server-side failure produces. A
    client that cannot learn which agent to run must refuse, exactly like a
    server that cannot.
    """


class ServerMandateSource:
    """Resolve Mandates against the AIDream server.

    ``GET {server_url}/api/mandates/{mandate_key}/resolution`` — authenticated,
    because the answer depends on the CALLER (their user and org bindings). An
    anonymous fetch would silently return the system default and quietly ignore
    the user's own rebind, so a missing JWT is an error here rather than a
    downgrade.
    """

    def __init__(
        self,
        server_url: str,
        get_jwt: Any = None,
        *,
        # A mandate resolves once per agent run, in front of a model call that
        # costs far more than this request. Short enough that a black-holed
        # network fails fast rather than hanging a user's run.
        timeout_seconds: float = 8.0,
    ) -> None:
        self._base = server_url.rstrip("/")
        self._get_jwt = get_jwt
        self._timeout = timeout_seconds

    def url_for(self, mandate_key: str) -> str:
        return f"{self._base}/api/mandates/{quote(mandate_key, safe='')}/resolution"

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        token = None
        if callable(self._get_jwt):
            try:
                token = self._get_jwt()
            except Exception as exc:  # noqa: BLE001 — report, never fetch anonymously
                raise MandateSourceFetchError(
                    f"get_jwt() raised {type(exc).__name__}: {exc}; refusing to resolve a "
                    f"mandate anonymously — the answer depends on the caller's bindings"
                ) from exc
            import inspect

            if inspect.iscoroutine(token):
                token.close()
                raise MandateSourceFetchError(
                    "get_jwt is async (returned a coroutine); the seam requires a SYNC "
                    "zero-arg callable. Fix the host's configure(get_jwt=...)."
                )
        if not token:
            raise MandateSourceFetchError(
                "no JWT available; mandate resolution is per-caller (user and org bindings "
                "decide the agent), so an anonymous fetch would silently ignore the "
                "user's own rebind"
            )
        headers["Authorization"] = f"Bearer {token}"
        return headers

    async def __call__(self, mandate_key: str) -> MandateResolution:
        import httpx

        url = self.url_for(mandate_key)
        try:
            async with httpx.AsyncClient(timeout=self._timeout, follow_redirects=True) as client:
                resp = await client.get(url, headers=self._headers())
        except httpx.HTTPError as exc:
            raise MandateSourceFetchError(
                f"mandate resolution failed: GET {url} → {type(exc).__name__}: {exc}"
            ) from exc
        if resp.status_code != 200:
            raise MandateSourceFetchError(
                f"mandate resolution failed: GET {url} → HTTP {resp.status_code}: "
                f"{resp.text[:500]}"
            )
        try:
            payload = resp.json()
        except ValueError as exc:
            raise MandateSourceFetchError(
                f"mandate resolution returned non-JSON: GET {url}: {exc}"
            ) from exc
        if not isinstance(payload, dict):
            raise MandateSourceFetchError(
                f"mandate resolution returned {type(payload).__name__}, expected an object: GET {url}"
            )
        agent_id = payload.get("agent_id")
        if not isinstance(agent_id, str) or not agent_id:
            raise MandateSourceFetchError(
                f"mandate resolution payload has no usable agent_id: GET {url}: {payload!r:.300}"
            )
        # `is_version` is DB state — the client never decides it, and never
        # defaults it to a guess. A payload that omits it is malformed.
        is_version = payload.get("is_version")
        if not isinstance(is_version, bool):
            raise MandateSourceFetchError(
                f"mandate resolution payload has no boolean is_version: GET {url}"
            )
        overrides = payload.get("config_overrides")
        contract = payload.get("contract")
        contract = contract if isinstance(contract, dict) else {}
        raw_spill = contract.get("spill_variables")
        raw_mapping = contract.get("variable_mapping")
        # THE INPUT SIDE, exactly as the server resolved it. A client that
        # dropped these ran every mandate on the legacy variable flow, silently
        # ignoring the binding's deliberate variable/context routing.
        provision_key = payload.get("provision_key")
        raw_offered = payload.get("offered_values")
        offered_values: tuple[OfferedValueSpec, ...] = ()
        if isinstance(raw_offered, list):
            offered_values = tuple(
                OfferedValueSpec(
                    name=item["name"],
                    kind=item["kind"],
                    guaranteed=bool(item.get("guaranteed", True)),
                    lazy=bool(item.get("lazy", False)),
                )
                for item in raw_offered
                if isinstance(item, dict)
                and isinstance(item.get("name"), str)
                and isinstance(item.get("kind"), str)
            )
        consumption_map = payload.get("consumption_map")
        return MandateResolution(
            source=AgentRecordSource(agent_id=agent_id, is_version=is_version),
            config_overrides=overrides if isinstance(overrides, dict) else None,
            variable_mapping=raw_mapping if isinstance(raw_mapping, dict) else None,
            spill_variables=frozenset(
                item for item in (raw_spill or []) if isinstance(item, str)
            ),
            provision_key=provision_key if isinstance(provision_key, str) else None,
            offered_values=offered_values,
            consumption_map=consumption_map if isinstance(consumption_map, dict) else None,
            output_kind=(
                payload.get("output_kind")
                if isinstance(payload.get("output_kind"), str)
                else None
            ),
        )


__all__ = ["ServerMandateSource", "MandateSourceFetchError"]
