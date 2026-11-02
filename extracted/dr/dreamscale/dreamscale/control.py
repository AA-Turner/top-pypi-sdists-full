"""Control-plane HTTP client (master REST contract, spec §5.1)."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any

import httpx

from dreamscale import errors
from dreamscale.config import API_KEY_ENV
from dreamscale.model_names import internal_model
from dreamscale.policy.config import RTC_KINDS, OptimizationConfig, ResolvedOptimizationConfig
from dreamscale.policy.deployment import CLIENT_FEATURES, in_use_session_id

_DELETE_ATTEMPTS = 3
_GATEWAY_STATUSES = frozenset({502, 503, 504})


@dataclass(frozen=True)
class DataPlane:
    transport: str
    url: str

    @classmethod
    def from_json(cls, data: dict[str, Any] | None) -> DataPlane | None:
        if not data:
            return None
        transport = str(data.get("transport") or "")
        url = str(data.get("url") or "")
        if transport != "wss_tunnel" or not url:
            raise ValueError("unsupported session data-plane descriptor")
        return cls(transport=transport, url=url)


@dataclass(frozen=True)
class Session:
    session_id: str
    status: str
    model: str | None = None
    region: str | None = None
    target_key: str | None = None
    eta_s: int | None = None
    startup_phase: str | None = None
    startup_timeout_s: float | None = None
    created_at: float | None = None
    worker_addr: str | None = None
    port: int | None = None
    cert_fingerprint: str | None = None
    session_token: str | None = None
    lease_ttl_s: int | None = None
    error: dict[str, Any] | None = None
    routed_region: str | None = None
    region_notice: bool = False
    region_mode: str | None = None
    region_probe_status: str | None = None
    region_probe_confident_winner: str | None = None
    resolved_profile_id: str | None = None
    selection_reason: str | None = None
    low_balance: bool = False
    reason: str | None = None
    data_plane: DataPlane | None = None
    requested_optimization_config: OptimizationConfig = OptimizationConfig()
    resolved_optimization_config: ResolvedOptimizationConfig = ResolvedOptimizationConfig()
    provider: str | None = None
    requested_provider: str | None = None
    speed: str | None = None
    # QUIC upload mode chosen by the control plane; anything unrecognised
    # (including a value from a newer server) means "standard".
    upload: str = "standard"
    # Modal sessions: the control plane allows upgrading the WebSocket tunnel to
    # punched QUIC (dreamscale_transport.punch) and names the upload mode.
    modal_quic: str | None = None
    # Shared models: this session's place in its pool's queue (1 = next).
    queue_position: int | None = None
    queue_eta_s: int | None = None
    # While its region is full and a server starts in the next-closest region instead (region
    # fallback): that region, and what the control plane says about it.
    starting_region: str | None = None
    starting_note: str | None = None
    # π0.5 deployment sessions: the robot the deployment serves ({id, preset, cameras,
    # state_dim, action_dim, executed_actions, action_hz, rtc_method}), as the server sent it.
    deployment: dict[str, Any] | None = None
    # A deployment session: its deployment's keep-warm (off, 10m … always); None from a
    # control plane that doesn't say. Kept warm, the policy skips its idle release.
    deployment_keep_warm: str | None = None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Session:
        return cls(
            session_id=data["session_id"],
            status=data["status"],
            # The SDK keys its per-model behaviour on internal ids (model_names).
            model=internal_model(data["model"]) if data.get("model") else data.get("model"),
            region=data.get("region"),
            target_key=data.get("target_key"),
            provider=data.get("provider"),
            requested_provider=data.get("requested_provider"),
            speed=data.get("speed"),
            eta_s=data.get("eta_s"),
            startup_phase=data.get("startup_phase"),
            startup_timeout_s=data.get("startup_timeout_s"),
            created_at=data.get("created_at"),
            worker_addr=data.get("worker_addr"),
            port=data.get("port"),
            cert_fingerprint=data.get("cert_fingerprint"),
            session_token=data.get("session_token"),
            lease_ttl_s=data.get("lease_ttl_s"),
            error=data.get("error"),
            routed_region=data.get("routed_region"),
            region_notice=bool(data.get("region_notice", False)),
            region_mode=data.get("region_mode"),
            region_probe_status=data.get("region_probe_status"),
            region_probe_confident_winner=data.get(
                "region_probe_confident_winner"
            ),
            resolved_profile_id=data.get("resolved_profile_id"),
            selection_reason=data.get("selection_reason"),
            low_balance=bool(data.get("low_balance", False)),
            reason=data.get("reason"),
            data_plane=DataPlane.from_json(data.get("data_plane")),
            requested_optimization_config=OptimizationConfig.from_wire(
                data.get("requested_optimization_config")
            ),
            resolved_optimization_config=ResolvedOptimizationConfig.from_wire(
                data.get("resolved_optimization_config")
            ),
            upload="steady" if data.get("upload") == "steady" else "standard",
            modal_quic=(
                data["modal_quic"] if data.get("modal_quic") in ("standard", "steady") else None
            ),
            queue_position=data.get("queue_position"),
            queue_eta_s=data.get("queue_eta_s"),
            starting_region=(
                data["starting_region"] if isinstance(data.get("starting_region"), str) else None
            ),
            starting_note=(
                data["starting_note"] if isinstance(data.get("starting_note"), str) else None
            ),
            deployment=(
                data["deployment"] if isinstance(data.get("deployment"), dict) else None
            ),
            deployment_keep_warm=(
                data["deployment_keep_warm"]
                if isinstance(data.get("deployment_keep_warm"), str) else None
            ),
        )


# The RTC wire contracts this run loop implements (dreamscale.policy.runtime.rtc). Shared
# models whose fixed profile is train-time RTC admit clients that list theirs.
CLIENT_RTC_CONTRACTS = ("dynamic_full_horizon_v1", "isaac05_late_bound_prefix_v1")
# Shared-endpoint refusals that carry their own problem and fix.
SHARED_ERROR_CODES = frozenset(
    {
        "capacity_exhausted",
        "shared_session_limit",
        "shared_profile_mismatch",
        "region_unavailable",
        "sdk_upgrade_required",
        # A π0.5 deployment host at its GPU ceiling (503): no capacity, never retried here.
        "deployment_capacity_unavailable",
    }
)

DEPLOYMENTS_PATH = "/v1/deployments"
# The older name for the same routes, on control planes from before deployments.
ENDPOINTS_PATH = "/v1/endpoints"
DEFAULT_DEPLOYMENT_REGION = "us-west"
TRAININGS_PATH = "/v1/trainings"
UPLOADS_PATH = "/v1/uploads"
DATASETS_PATH = "/v1/datasets"
HUGGING_FACE_PATH = "/v1/integrations/hugging-face"

# Who is calling, for the control plane's usage analytics: the command line sets "cli" when it
# starts (cli.main); Python code using the SDK stays "sdk". Sent with the version, nothing else.
CLIENT = "sdk"


def user_agent() -> str:
    from dreamscale import __version__

    return f"dreamscale-{CLIENT}/{__version__}"


class ControlPlaneClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._provider_capabilities: set[tuple[str, str]] = set()
        self._api_key = api_key
        self._deployments_path = DEPLOYMENTS_PATH
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={"Authorization": f"Bearer {api_key}", "User-Agent": user_agent()},
            # Live session creation may synchronously kick EC2/reconciler work before
            # returning a starting lease, so the generic 10s default is too tight.
            timeout=httpx.Timeout(60.0, connect=10.0),
            transport=transport,
        )

    async def close(self) -> None:
        await self._client.aclose()

    def relay_url(self, session_id: str) -> str:
        base = str(self._client.base_url).rstrip("/")
        if base.startswith("https://"):
            base = "wss://" + base[len("https://"):]
        elif base.startswith("http://"):
            base = "ws://" + base[len("http://"):]
        return f"{base}/v1/sessions/{session_id}/relay"

    async def connect_relay(self, session: Session):
        from dreamscale_transport import RelayClient

        if not session.session_token:
            raise errors.catalog("session_expired")
        return await RelayClient.connect(
            self.relay_url(session.session_id),
            api_key=self._api_key,
            session_id=session.session_id,
            session_token=session.session_token,
        )

    async def connect_data_plane(self, session: Session):
        from dreamscale_transport import H264WebSocketClient, WebSocketClient, catalog

        if (
            session.data_plane is None
            or session.data_plane.transport != "wss_tunnel"
            or not session.session_token
        ):
            raise errors.catalog("session_expired")
        client_type = (
            H264WebSocketClient if session.model == "dreamzero-yam" else WebSocketClient
        )
        codec_options = {}
        if session.model in catalog.camera_codec_models():
            from dreamscale.camera_codec import codec_settings

            settings = codec_settings(session.model)
            if settings is not None:
                from dreamscale_transport.codec_client import CodecWebSocketClient

                client_type, codec_options = CodecWebSocketClient, {"codec": settings}
        # YAM's measured Modal tunnel latency falls when protocol pings keep
        # traffic flowing between predictions. Use native keepalive so its
        # timeout and teardown stay owned by the WebSocket connection.
        # Which models: their catalog entries' ``client.keepalive``.
        entry = catalog.entry(session.model)
        transport_options = (
            {"ping_interval": 0.075} if entry is not None and entry.client.keepalive else {}
        )
        # A ready worker's tunnel can transiently time out during opening.
        # Retry attachment to this exact allocation; never create another lease
        # or retry authentication/protocol failures. Bound subscription as well
        # as the HTTP upgrade, which the transport bounds independently.
        for attempt in range(3):
            try:
                async with asyncio.timeout(10):
                    return await client_type.connect(
                        session.data_plane.url,
                        session_id=session.session_id,
                        session_token=session.session_token,
                        **transport_options,
                        **codec_options,
                    )
            except (TimeoutError, ConnectionError):
                if attempt == 2:
                    raise
                await asyncio.sleep(0.25 * (attempt + 1))
        raise AssertionError("unreachable")

    async def report_transport(
        self,
        session_id: str,
        *,
        transport_protocol: str,
        fallback_used: bool = False,
        fallback_reason: str | None = None,
        primary_preflight_status: str | None = None,
        diagnostic_preflight_status: str | None = None,
    ) -> None:
        resp = await self._client.post(
            f"/v1/sessions/{session_id}/transport",
            json={
                "transport_protocol": transport_protocol,
                "fallback_used": fallback_used,
                "fallback_reason": fallback_reason,
                "primary_preflight_status": primary_preflight_status,
                "diagnostic_preflight_status": diagnostic_preflight_status,
            },
        )
        _raise_for_auth(resp)
        if resp.status_code == 404:
            raise errors.catalog("session_expired")
        _raise_for_status(resp)

    async def create_session(
        self,
        model: str,
        preferred_region: str | None = None,
        *,
        region_pin: bool = False,
        region_order: list[str] | None = None,
        region_order_source: str | None = None,
        region_mode: str | None = None,
        provider: str | None = None,
        region_measurements: list[dict[str, Any]] | None = None,
        region_probe_status: str | None = None,
        region_probe_confident_winner: str | None = None,
        idle_timeout: int | None = None,
        keep_warm: int = 0,
        optimization_config: OptimizationConfig | dict[str, Any] | None = None,
        speed: str | None = None,
        checkpoint: str | None = None,
    ) -> Session:
        fast = speed == "fast"
        if speed not in (None, "standard", "fast"):
            raise ValueError('speed must be "standard" or "fast"')
        if fast and (model, "speed:fast") not in self._provider_capabilities:
            # Older servers ignore unknown fields; never let one bill or route a
            # fast request as standard without acknowledging it first.
            await self.probe_candidates(
                model, optimization_config=optimization_config, provider=provider, speed="fast"
            )
        if provider is not None:
            from dreamscale.region_probe import validate_provider_selection

            validate_provider_selection(
                model, provider, preferred_region if region_pin else "available"
            )
            # Require explicit acknowledgement before creating compute. Older
            # servers ignore unknown JSON fields; they must never silently route
            # a constrained request through their ordinary allocation path.
            if (model, provider) not in self._provider_capabilities:
                await self.probe_candidates(
                    model, optimization_config=optimization_config, provider=provider
                )
        body: dict[str, Any] = {
            "model": model,
            "client_rtc_contracts": list(CLIENT_RTC_CONTRACTS),
            # Older control planes ignore it; π0.5 deployment sessions require it.
            "client_features": list(CLIENT_FEATURES),
        }
        if provider is not None:
            body["provider"] = provider
        if fast:
            body["speed"] = "fast"
        if preferred_region:
            body["preferred_region"] = preferred_region
        if region_pin:
            body["region_pin"] = True
        if region_order:
            body["region_order"] = region_order
        if region_order_source:
            body["region_order_source"] = region_order_source
        if region_mode:
            body["region_mode"] = region_mode
        if region_measurements is not None:
            body["region_measurements"] = region_measurements
        if region_probe_status:
            body["region_probe_status"] = region_probe_status
        if region_probe_confident_winner:
            body["region_probe_confident_winner"] = (
                region_probe_confident_winner
            )
        if idle_timeout is not None:
            body["idle_timeout"] = idle_timeout
        if keep_warm:
            body["keep_warm"] = keep_warm
        if checkpoint is not None:
            # A deployment id (or "base"). `deployment` is the current name; older control
            # planes ignore it and read `checkpoint`, which newer ones accept as an alias.
            body["deployment"] = checkpoint
            body["checkpoint"] = checkpoint
        if optimization_config is not None:
            if isinstance(optimization_config, OptimizationConfig):
                body["optimization_config"] = optimization_config.to_wire()
            else:
                body["optimization_config"] = OptimizationConfig.from_wire(
                    optimization_config
                ).to_wire()
        resp = await self._client.post("/v1/sessions", json=body)
        _raise_for_auth(resp)
        if resp.status_code >= 400 and _error_code(resp) in SHARED_ERROR_CODES:
            raise errors.from_payload(resp.json())
        if resp.status_code == 426:
            raise errors.catalog(errors.SDK_UPGRADE_REQUIRED, model=model)
        if resp.status_code == 409 and _error_code(resp) == "deployment_in_use":
            raise _deployment_in_use(resp)
        if resp.status_code == 402:
            raise errors.catalog("insufficient_credits")
        if resp.status_code in (404, 409) and _error_code(resp).startswith("checkpoint"):
            raise errors.from_payload(resp.json())
        unavailable = _unavailable_code(model)
        if unavailable is not None and _base_unknown(resp):
            # A control plane from before this base's deployments: no such model, or no route
            # to it.
            raise errors.catalog(unavailable)
        if resp.status_code == 404:
            raise errors.catalog("unknown_model", model=model)
        if resp.status_code == 429:
            raise _rate_limited(resp)
        if resp.status_code == 503 and _error_code(resp) == "deployment_requalifying":
            # Retryable: open_policy_connection waits it out (REQUALIFYING_WAIT_S).
            raise _with_retry_after(errors.from_payload(resp.json()), resp)
        if resp.status_code == 422:
            raise _unprocessable(resp, optimization_config)
        _raise_for_status(resp)
        session = Session.from_json(resp.json())
        kind = _requested_rtc_kind(optimization_config)
        if kind is not None and session.resolved_optimization_config.effective_rtc_mode != kind:
            # Never run a session in another RTC kind than the one asked for.
            await self.delete_session(session.session_id)
            raise RuntimeError(f"control plane did not apply rtc={kind}")
        if provider is not None and session.requested_provider != provider:
            # A rolling deployment may have acknowledged support on a newer
            # replica but created the session on an older one.
            await self.delete_session(session.session_id)
            raise RuntimeError("control plane did not enforce the requested provider")
        if fast and session.speed != "fast":
            await self.delete_session(session.session_id)
            raise RuntimeError('control plane did not apply speed="fast"')
        return session

    async def probe_candidates(
        self,
        model: str,
        *,
        optimization_config: OptimizationConfig | dict[str, Any] | None = None,
        provider: str | None = None,
        speed: str | None = None,
        client_features: list[str] | None = None,
    ) -> list[dict[str, str]]:
        body: dict[str, Any] = {"model": model}
        if provider is not None:
            body["provider"] = provider
        if speed == "fast":
            body["speed"] = "fast"
        if client_features:
            # region_probes_v1: also the region record's probes on Modal routes (DSL-359).
            # Older control planes ignore it.
            body["client_features"] = list(client_features)
        if optimization_config is not None:
            if isinstance(optimization_config, OptimizationConfig):
                body["optimization_config"] = optimization_config.to_wire()
            else:
                body["optimization_config"] = OptimizationConfig.from_wire(
                    optimization_config
                ).to_wire()
        resp = await self._client.post("/v1/regions/probe-candidates", json=body)
        _raise_for_auth(resp)
        if resp.status_code == 404:
            raise errors.catalog("unknown_model", model=model)
        if resp.status_code == 422:
            raise _unprocessable(resp, optimization_config)
        _raise_for_status(resp)
        payload = resp.json()
        if provider is not None and payload.get("provider") != provider:
            raise RuntimeError("control plane does not support explicit provider selection")
        if speed == "fast" and payload.get("speed") != "fast":
            raise RuntimeError('control plane does not support speed="fast" for this model')
        if provider is not None:
            self._provider_capabilities.add((model, provider))
        if speed == "fast":
            self._provider_capabilities.add((model, "speed:fast"))
        return list(payload.get("candidates") or [])

    async def get_session(self, session_id: str) -> Session:
        resp = await self._client.get(f"/v1/sessions/{session_id}")
        _raise_for_auth(resp)
        if resp.status_code == 404:
            raise errors.catalog("session_expired")
        _raise_for_status(resp)
        return Session.from_json(resp.json())

    async def heartbeat(self, session_id: str) -> dict[str, Any] | None:
        """Refresh the lease. Returns the session as the control plane sees it now (None if
        the answer isn't a JSON object)."""
        resp = await self._client.post(f"/v1/sessions/{session_id}/heartbeat")
        _raise_for_auth(resp)
        if resp.status_code == 404:
            raise errors.catalog("session_expired")
        _raise_for_status(resp)
        try:
            body = resp.json()
        except ValueError:
            return None
        return body if isinstance(body, dict) else None

    async def delete_session(self, session_id: str) -> None:
        # DELETE is idempotent and 404 means already closed, so a gateway error or a
        # dropped connection is safe to retry. A close that never lands leaves the
        # session open (billing) and its deployment locked.
        for attempt in range(_DELETE_ATTEMPTS):
            last = attempt == _DELETE_ATTEMPTS - 1
            try:
                resp = await self._client.delete(f"/v1/sessions/{session_id}")
            except httpx.TransportError:
                if last:
                    raise
            else:
                if resp.status_code == 404:  # idempotent close (master contract)
                    return
                if resp.status_code not in _GATEWAY_STATUSES or last:
                    _raise_for_auth(resp)
                    _raise_for_status(resp)
                    return
            await asyncio.sleep(0.5 * (attempt + 1))

    async def detach_session(self, session_id: str) -> dict[str, Any] | None:
        resp = await self._client.post(f"/v1/sessions/{session_id}/detach")
        if resp.status_code == 404:
            return
        _raise_for_auth(resp)
        _raise_for_status(resp)
        return resp.json()

    async def list_sessions(self) -> list[dict]:
        resp = await self._client.get("/v1/sessions")
        _raise_for_auth(resp)
        _raise_for_status(resp)
        return resp.json()["sessions"]

    # --- deployments: your fine-tunes on a base model (bring your own weights) ------------

    async def _deployment_call(
        self, method: str, suffix: str = "", *, older_error: str | None = None, **kwargs: Any
    ) -> dict:
        """`/v1/deployments{suffix}`, or `/v1/endpoints{suffix}` on an older control plane.

        A bare 404 (no error code) is a missing route, never a missing deployment: retry
        once on the older path, unless `older_error` says the older path can't do this call.
        """
        path = DEPLOYMENTS_PATH if older_error else self._deployments_path
        resp = await self._client.request(method, f"{path}{suffix}", **kwargs)
        _raise_for_auth(resp)
        if path == DEPLOYMENTS_PATH and resp.status_code == 404 and not _error_code(resp):
            if older_error:
                raise errors.catalog(older_error)
            resp = await self._client.request(method, f"{ENDPOINTS_PATH}{suffix}", **kwargs)
            _raise_for_auth(resp)
            if resp.status_code != 404 or _error_code(resp):
                self._deployments_path = ENDPOINTS_PATH
        return _deployment_response(resp)

    async def add_checkpoint(
        self,
        model: str,
        repo: str | None,
        *,
        revision: str | None = None,
        name: str | None = None,
        hf_token: str | None = None,
        embodiment: dict[str, Any] | None = None,
        region: str | None = None,
        source_path: str | None = None,
        rtc_method: str | None = None,
        rtc_max_delay: int | None = None,
        keep_warm: str | None = None,
        slug: str | None = None,
        upload_id: str | None = None,
        source_format: str | None = None,
        region_fallback: bool | None = None,
    ) -> dict[str, Any]:
        """Create a deployment (your weights + the embodiment they serve, in a region).

        π0.5 deployments also name the checkpoint inside the repo (``source_path``) and
        their RTC method (``rtc_method``: off, test_time or trained, + ``rtc_max_delay``);
        a local folder's is its complete ``upload_id`` (no repo) and the ``source_format``
        Detect found. ``region_fallback``: whether a server may start in the next-closest
        region when the deployment's own is full (None: the server's default, on).
        """
        body: dict[str, Any] = {"model": model}
        for key, value in (
            ("repo", repo), ("upload_id", upload_id), ("source_format", source_format),
            ("revision", revision), ("name", name), ("hf_token", hf_token),
            ("embodiment", embodiment), ("region", region), ("source_path", source_path),
            ("rtc_method", rtc_method), ("rtc_max_delay", rtc_max_delay),
            ("keep_warm", keep_warm), ("slug", slug), ("region_fallback", region_fallback),
        ):
            if value is not None:
                body[key] = value
        # Older control planes drop an unknown `region` and build in us-west; never let
        # one place another region's deployment there silently.
        older_error = (
            None if region in (None, DEFAULT_DEPLOYMENT_REGION)
            else "deployment_region_unavailable"
        )
        # An older control plane ignores `region_fallback`: it starts no server in another
        # region anyway, so the deployment behaves as asked.
        return await self._deployment_call("POST", json=body, older_error=older_error)

    async def inspect_endpoint_repo(
        self,
        repo: str | None,
        *,
        revision: str | None = None,
        hf_token: str | None = None,
        model: str | None = None,
        path: str | None = None,
        local: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """The embodiment a repo declares and the training datasets its stats cover.

        ``model="pi0.5"`` reads it as a π0.5 checkpoint instead (its format, checkpoints,
        detected fields and RTC); ``path`` picks one checkpoint inside the repo. ``local``
        (π0.5, no repo): a local folder's listing (``dreamscale.local_checkpoint``); the
        answer's ``upload`` names the files a build reads.
        """
        body: dict[str, Any] = {}
        for key, value in (
            ("repo", repo), ("local", local), ("revision", revision), ("hf_token", hf_token),
            ("model", model), ("source_path", path),
        ):
            if value is not None:
                body[key] = value
        # A cold read starts a CPU container and fetches the repo's stats; the server allows
        # it 300 s, so the 60 s default would cut off a slow one.
        return await self._deployment_call(
            "POST", "/inspect", json=body, timeout=httpx.Timeout(300.0, connect=10.0)
        )

    async def list_regions(self) -> dict[str, Any] | None:
        """``GET /v1/regions``: the live regions, with their probe URLs (DSL-354). None from a
        control plane that predates regions."""
        resp = await self._client.get("/v1/regions")
        if resp.status_code == 404:
            return None
        _raise_for_status(resp)
        return resp.json()

    async def resolve_region(
        self, *, measurements: list[dict[str, Any]], offered: list[str] | None = None
    ) -> dict[str, Any] | None:
        """``POST /v1/regions/resolve``: where ``auto`` lands, from these measurements and where
        the control plane locates this machine. None from a control plane that predates it."""
        body: dict[str, Any] = {"measurements": measurements}
        if offered is not None:
            body["offered"] = offered
        resp = await self._client.post("/v1/regions/resolve", json=body)
        if resp.status_code == 404:
            return None
        _raise_for_status(resp)
        return resp.json()

    async def list_checkpoints(self, model: str | None = None) -> dict[str, Any]:
        params = {"model": model} if model else None
        return await self._deployment_call("GET", params=params)

    async def get_checkpoint(self, checkpoint_id: str) -> dict[str, Any]:
        return await self._deployment_call("GET", f"/{checkpoint_id}")

    async def set_default_checkpoint(self, model: str, checkpoint: str) -> dict[str, Any]:
        # Every control plane has /v1/endpoints/default; /v1/deployments/default is a newer
        # alias of it.
        resp = await self._client.put(
            f"{ENDPOINTS_PATH}/default", json={"model": model, "checkpoint": checkpoint}
        )
        _raise_for_auth(resp)
        return _deployment_response(resp)

    async def delete_checkpoint(self, checkpoint_id: str) -> dict[str, Any]:
        return await self._deployment_call("DELETE", f"/{checkpoint_id}")

    async def set_deployment_keep_warm(
        self,
        checkpoint_id: str,
        keep_warm: str,
        *,
        take_over_from: str | None = None,
        robots: int | None = None,
        now: bool = False,
    ) -> dict[str, Any]:
        """How long the deployment's server stays up with no robot connected (off … always).

        ``take_over_from``: move Always-on from that deployment once this one is warm.
        ``robots``: on an autoscaling deployment, how many robots it keeps ready (1-64).
        ``now``: start it now rather than at the first robot, held for the keep-warm from
        now; the answer carries ``warm_now`` when the control plane took it (then poll
        ``get_checkpoint`` until ``warm.state`` is ``warm``).
        """
        body: dict[str, Any] = {"keep_warm": keep_warm}
        if take_over_from is not None:
            body["take_over_from"] = take_over_from
        if robots is not None:
            body["keep_warm_robots"] = robots
        if now:
            body["warm_now"] = True
        resp = await self._client.patch(f"{DEPLOYMENTS_PATH}/{checkpoint_id}", json=body)
        if now and resp.status_code == 422 and "warm_now" in resp.text:
            # A control plane from before warm-now refuses the field: set the keep-warm
            # alone (its answer then has no warm_now, which says so).
            del body["warm_now"]
            resp = await self._client.patch(f"{DEPLOYMENTS_PATH}/{checkpoint_id}", json=body)
        _raise_for_auth(resp)
        if resp.status_code == 405 or (resp.status_code == 404 and not _error_code(resp)):
            raise errors.catalog("deployment_keep_warm_unavailable")
        return _deployment_response(resp)

    async def restart_deployment(self, checkpoint_id: str) -> dict[str, Any]:
        """Stop the deployment's servers now (a connected robot's too: its next request
        reconnects); with Always on a fresh one starts at once. The response's ``restart``
        counts the servers stopped and how many had a robot on."""
        return await self._server_action(checkpoint_id, "restart")

    async def stop_deployment(self, checkpoint_id: str) -> dict[str, Any]:
        """Stop the deployment's servers now and keep none warm (turns its keep-warm off).
        The response's ``stopped`` counts the servers stopped and how many had a robot on."""
        return await self._server_action(checkpoint_id, "stop")

    async def _server_action(self, checkpoint_id: str, action: str) -> dict[str, Any]:
        resp = await self._client.post(f"{DEPLOYMENTS_PATH}/{checkpoint_id}/{action}")
        _raise_for_auth(resp)
        if resp.status_code == 405 or (resp.status_code == 404 and not _error_code(resp)):
            raise errors.catalog("deployment_keep_warm_unavailable")
        return _deployment_response(resp)

    async def set_deployment_rtc(
        self, checkpoint_id: str, rtc_method: str, *, max_delay: int | None = None
    ) -> dict[str, Any]:
        """A π0.5 deployment's RTC method (off, test_time, trained + the trained max delay),
        for its new sessions; no rebuild."""
        body: dict[str, Any] = {"rtc_method": rtc_method}
        if max_delay is not None:
            body["rtc_max_delay"] = max_delay
        resp = await self._client.patch(f"{DEPLOYMENTS_PATH}/{checkpoint_id}", json=body)
        _raise_for_auth(resp)
        if (
            resp.status_code == 405
            or (resp.status_code == 404 and not _error_code(resp))
            or (resp.status_code == 422 and "rtc_method" in _error_problem(resp)
                and "not permitted" in _error_problem(resp))
        ):
            # Older control planes forbid fields they don't know on this PATCH.
            raise errors.catalog("pi05_deployments_unavailable")
        return _deployment_response(resp)

    async def set_deployment_region_fallback(
        self, checkpoint_id: str, region_fallback: bool
    ) -> dict[str, Any]:
        """Whether the deployment's servers may start in the next-closest region when its own
        is full; for its next server, no rebuild."""
        resp = await self._client.patch(
            f"{DEPLOYMENTS_PATH}/{checkpoint_id}", json={"region_fallback": region_fallback}
        )
        _raise_for_auth(resp)
        if (
            resp.status_code == 405
            or (resp.status_code == 404 and not _error_code(resp))
            or (resp.status_code == 422 and "region_fallback" in _error_problem(resp))
        ):
            raise errors.catalog("region_fallback_unavailable")
        return _deployment_response(resp)

    async def rename_deployment(
        self, checkpoint_id: str, name: str | None = None, *, slug: str | None = None
    ) -> dict[str, Any]:
        """Rename the deployment: its slug, the <model> of <account>/<model> (``name`` is the
        older way, which the control plane turns into a slug)."""
        body = {key: value for key, value in (("name", name), ("slug", slug)) if value is not None}
        resp = await self._client.patch(f"{DEPLOYMENTS_PATH}/{checkpoint_id}", json=body)
        _raise_for_auth(resp)
        if resp.status_code == 405 or (resp.status_code == 404 and not _error_code(resp)):
            raise errors.catalog("deployment_rename_unavailable")
        return _deployment_response(resp)

    # --- training: fine-tune π0.5 on a LeRobot dataset (dreamscale train) ------------------

    async def _training_call(
        self, method: str, path: str, *, run_id: str | None = None, **kwargs: Any
    ) -> dict:
        resp = await self._client.request(method, path, **kwargs)
        _raise_for_auth(resp)
        if resp.status_code == 404 and _error_code(resp) in ("", "not_found"):
            # Training answers 404 to organizations it isn't open to, as if it didn't exist.
            if run_id is not None:
                raise errors.catalog("training_run_not_found", run_id=run_id)
            raise errors.catalog("training_unavailable")
        if resp.status_code == 402:
            payload = _error_payload(resp)
            raise errors.catalog(
                "training_credits_required",
                detail=str(payload.get("problem") or payload.get("message") or ""),
                amount_fix=str(payload.get("fix") or ""),
            )
        _raise_for_status(resp)
        return resp.json()

    async def estimate_training(self, body: dict[str, Any]) -> dict[str, Any]:
        """The run's summary, contract and exact quote, with the balance (nothing starts)."""
        return await self._training_call("POST", f"{TRAININGS_PATH}/estimate", json=body)

    async def create_training(self, body: dict[str, Any], *, idempotency_key: str) -> dict:
        """Start a run. The same key from the same organization returns the same run."""
        return await self._training_call(
            "POST", TRAININGS_PATH, json=body, headers={"Idempotency-Key": idempotency_key}
        )

    async def list_trainings(self) -> dict[str, Any]:
        return await self._training_call("GET", TRAININGS_PATH)

    async def get_training(self, run_id: str, *, since_step: int | None = None) -> dict:
        params = {"since_step": since_step} if since_step is not None else None
        return await self._training_call(
            "GET", f"{TRAININGS_PATH}/{run_id}", run_id=run_id, params=params
        )

    async def cancel_training(self, run_id: str) -> dict[str, Any]:
        return await self._training_call(
            "POST", f"{TRAININGS_PATH}/{run_id}/cancel", run_id=run_id
        )

    async def stop_training(self, run_id: str) -> dict[str, Any]:
        """Stop a run: one still training saves and stops (resumable, when Stop and Resume is
        on); one not training yet is canceled."""
        return await self._training_call(
            "POST", f"{TRAININGS_PATH}/{run_id}/stop", run_id=run_id
        )

    async def resume_training(
        self, run_id: str, *, accept_usd: str, idempotency_key: str
    ) -> dict[str, Any]:
        """Resume a stopped run for its remaining steps at ``accept_usd`` (a higher price is
        refused); the same key resumes it once."""
        return await self._training_call(
            "POST", f"{TRAININGS_PATH}/{run_id}/resume", run_id=run_id,
            json={"accept_usd": accept_usd}, headers={"idempotency-key": idempotency_key},
        )

    async def delete_training(self, run_id: str) -> dict[str, Any]:
        """Permanently delete a run; one still going is canceled first (charged its steps)."""
        return await self._training_call("DELETE", f"{TRAININGS_PATH}/{run_id}", run_id=run_id)

    async def deploy_training(
        self, run_id: str, *, step: int | None = None, region: str | None = None,
        region_fallback: bool | None = None,
    ) -> dict[str, Any]:
        """A Deployment of one of the run's checkpoints (default the latest); 1-based step.
        ``region_fallback`` as for ``add_checkpoint`` (None: the server's default, on)."""
        body: dict[str, Any] = {
            key: value for key, value in (("step", step), ("region", region)) if value
        }
        if region_fallback is not None:
            body["region_fallback"] = region_fallback
        return await self._training_call(
            "POST", f"{TRAININGS_PATH}/{run_id}/deploy", run_id=run_id, json=body
        )

    async def download_training(self, run_id: str, *, step: int | None = None) -> dict[str, Any]:
        """A signed link to one of the run's checkpoints (default the latest; 1-based step) as
        an openpi checkpoint; ``status`` is "preparing" until it's packed, then "ready"."""
        body = {"step": step} if step else {}
        return await self._training_call(
            "POST", f"{TRAININGS_PATH}/{run_id}/download", run_id=run_id, json=body
        )

    async def _upload_call(self, kind: str, method: str, path: str, **kwargs: Any) -> dict:
        """A dataset upload answers as training does; a checkpoint upload as deployments do
        (its own gate: π0.5 deployments and credits)."""
        if kind == "dataset":
            return await self._training_call(method, path, **kwargs)
        resp = await self._client.request(method, path, **kwargs)
        _raise_for_auth(resp)
        return _deployment_response(resp)

    async def create_upload(
        self, files: list[dict[str, Any]], *, kind: str = "dataset", base_model: str | None = None
    ) -> dict[str, Any]:
        """An upload of these files ({path, size, sha256}); `missing` lists the blobs to send.
        ``kind``: a dataset to train on, or a local folder's π0.5 ``checkpoint``."""
        return await self._upload_call(
            kind, "POST", UPLOADS_PATH,
            json={"kind": kind, "files": files,
                  **({"base_model": base_model} if base_model is not None else {})},
            timeout=httpx.Timeout(120.0, connect=10.0),
        )

    async def complete_upload(
        self, upload_id: str, parts: dict[str, list[dict[str, Any]]], *, kind: str = "dataset"
    ) -> dict[str, Any]:
        return await self._upload_call(
            kind, "POST", f"{UPLOADS_PATH}/{upload_id}/complete", json={"parts": parts},
            timeout=httpx.Timeout(300.0, connect=10.0),
        )

    async def training_bases(self) -> list[str]:
        """The bases your organization can start a run from."""
        answer = await self._training_call("GET", f"{TRAININGS_PATH}/bases")
        return list(answer.get("bases") or [])

    # --- datasets: named, versioned datasets kept on Dreamscale -------------------------------

    async def _dataset_call(self, method: str, path: str, **kwargs: Any) -> Any:
        resp = await self._client.request(method, path, **kwargs)
        _raise_for_auth(resp)
        if resp.status_code == 404 and _error_code(resp) in ("", "not_found"):
            raise errors.catalog("datasets_unavailable")
        if resp.status_code == 402:
            payload = _error_payload(resp)
            raise errors.catalog(
                "training_credits_required",
                detail=str(payload.get("problem") or payload.get("message") or ""),
                amount_fix=str(payload.get("fix") or ""),
            )
        _raise_for_status(resp)
        return resp.json()

    async def list_datasets(self) -> list[dict[str, Any]]:
        return (await self._dataset_call("GET", DATASETS_PATH)).get("datasets") or []

    async def get_dataset(self, ref: str) -> dict[str, Any]:
        return await self._dataset_call("GET", f"{DATASETS_PATH}/{ref}")

    async def create_dataset(self, name: str) -> dict[str, Any]:
        return await self._dataset_call("POST", DATASETS_PATH, json={"name": name})

    async def rename_dataset(self, ref: str, name: str) -> dict[str, Any]:
        return await self._dataset_call("PATCH", f"{DATASETS_PATH}/{ref}", json={"name": name})

    async def delete_dataset(self, ref: str) -> dict[str, Any]:
        return await self._dataset_call("DELETE", f"{DATASETS_PATH}/{ref}")

    async def delete_dataset_version(self, ref: str, version: int) -> dict[str, Any]:
        return await self._dataset_call("DELETE", f"{DATASETS_PATH}/{ref}/versions/{version}")

    async def create_dataset_upload(
        self, ref: str, *, size: int | None = None, files: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        """An upload into the dataset; ``size``: the folder's total, known before it's hashed."""
        body: dict[str, Any] = {}
        if size is not None:
            body["bytes"] = size
        if files:
            body["files"] = files
        return await self._dataset_call(
            "POST", f"{DATASETS_PATH}/{ref}/uploads", json=body,
            timeout=httpx.Timeout(120.0, connect=10.0),
        )

    async def add_dataset_upload_files(
        self, ref: str, upload_id: str, files: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """A batch of the manifest (up to 1,000); ``missing`` lists its blobs still to send, with
        fresh links, so sending a batch again is how an expired link is renewed."""
        return await self._dataset_call(
            "POST", f"{DATASETS_PATH}/{ref}/uploads/{upload_id}/files", json={"files": files},
            timeout=httpx.Timeout(120.0, connect=10.0),
        )

    async def complete_dataset_upload(
        self, ref: str, upload_id: str, parts: dict[str, list[dict[str, Any]]],
        **measured: Any,
    ) -> dict[str, Any]:
        return await self._dataset_call(
            "POST", f"{DATASETS_PATH}/{ref}/uploads/{upload_id}/complete",
            json={"parts": parts, **measured}, timeout=httpx.Timeout(300.0, connect=10.0),
        )

    async def dataset_files(
        self, ref: str, version: int, *, cursor: int | None = None, links: bool = False
    ) -> dict[str, Any]:
        params: dict[str, str] = {}
        if cursor is not None:
            params["cursor"] = str(cursor)
        if links:
            params["links"] = "true"
        return await self._dataset_call(
            "GET", f"{DATASETS_PATH}/{ref}/versions/{version}/files", params=params
        )

    async def create_dataset_import(
        self, ref: str, *, repo: str, revision: str | None = None, path: str | None = None,
        hf_token: str | None = None,
    ) -> dict[str, Any]:
        body = {k: v for k, v in (("repo", repo), ("revision", revision), ("path", path),
                                  ("hf_token", hf_token)) if v}
        return await self._dataset_call(
            "POST", f"{DATASETS_PATH}/{ref}/imports", json=body,
            timeout=httpx.Timeout(120.0, connect=10.0),
        )

    async def get_dataset_import(self, ref: str, import_id: str) -> dict[str, Any]:
        return await self._dataset_call("GET", f"{DATASETS_PATH}/{ref}/imports/{import_id}")

    async def cancel_dataset_import(self, ref: str, import_id: str) -> dict[str, Any]:
        return await self._dataset_call("DELETE", f"{DATASETS_PATH}/{ref}/imports/{import_id}")

    # --- integrations: the Hugging Face read token Dreamscale keeps for your account --------

    async def _hugging_face_call(self, method: str, **kwargs: Any) -> dict[str, Any]:
        resp = await self._client.request(method, HUGGING_FACE_PATH, **kwargs)
        _raise_for_auth(resp)
        code = _error_code(resp)
        if resp.status_code >= 400 and code and code not in ("internal_error", "not_found"):
            # Its refusals (hf_token_rejected, hf_token_can_write) and Hugging Face being
            # unreachable (502) or down (503) carry their own problem and fix.
            raise errors.from_payload(resp.json())
        if resp.status_code in (404, 405):
            raise errors.catalog("hugging_face_connect_unavailable")
        _raise_for_status(resp)
        return resp.json()

    async def hugging_face_status(self) -> dict[str, Any]:
        """``{"connected": false}``, or the connected account: username, orgs, role,
        token_hint, created_at, last_used_at and failed_at (Hugging Face refused it)."""
        return await self._hugging_face_call("GET")

    async def connect_hugging_face(self, token: str) -> dict[str, Any]:
        """Check a read token with Hugging Face and keep it for your account (replacing one)."""
        return await self._hugging_face_call("PUT", json={"token": token})

    async def disconnect_hugging_face(self) -> dict[str, Any]:
        return await self._hugging_face_call("DELETE")

    async def list_models(self) -> list[dict[str, Any]]:
        resp = await self._client.get("/v1/models")
        _raise_for_auth(resp)
        if resp.status_code == 404:
            raise errors.catalog("models_unavailable")
        _raise_for_status(resp)
        # Public names in, internal ids for the SDK's own tables (model_names).
        return [{**model, "id": internal_model(model["id"])} for model in resp.json()["models"]]

    async def status(self) -> dict[str, Any]:
        resp = await self._client.get("/v1/status")
        _raise_for_auth(resp)
        _raise_for_status(resp)
        # Live envelope (binding): {"models": {<model>: {instance_state,
        # active_sessions}}} — unwrap to the per-model map callers iterate, keyed by the
        # SDK's internal ids (model_names).
        return {internal_model(model): info for model, info in resp.json()["models"].items()}


def _deployment_response(resp: httpx.Response) -> dict[str, Any]:
    if resp.status_code >= 400 and _error_code(resp):
        raise errors.from_payload(resp.json())
    if resp.status_code == 402:
        raise errors.catalog("insufficient_credits")
    if resp.status_code == 404:
        # A bare 404 on both paths: this control plane predates deployments.
        raise errors.catalog("deployments_unavailable")
    _raise_for_status(resp)
    return resp.json()


def _raise_for_status(resp: httpx.Response) -> None:
    """Every unexpected status becomes a Dreamscale error, never an httpx traceback: the
    server's own payload when the body carries one, otherwise ``server_error``."""
    if resp.status_code < 400:
        return
    if resp.status_code >= 500:
        # Always a ServerError (transient for heartbeat and polls), even when the
        # control plane's catch-all wraps it as {"error": {"code": "internal_error"}}.
        payload = _error_payload(resp)
        raise errors.server_error(
            status=resp.status_code,
            request_id=resp.headers.get("x-request-id"),
            server_code=str(payload.get("code") or "") or None,
            detail=str(payload.get("problem") or payload.get("detail") or "") or None,
        )
    if _error_code(resp):
        raise errors.from_payload(resp.json())
    raise errors.server_error(
        status=resp.status_code, request_id=resp.headers.get("x-request-id")
    )


def _with_retry_after(err: errors.DreamscaleError, resp: httpx.Response):
    retry_after = resp.headers.get("retry-after")
    try:
        err.retry_after_s = float(retry_after) if retry_after is not None else None
    except ValueError:
        err.retry_after_s = None
    return err


def _rate_limited(resp: httpx.Response) -> errors.DreamscaleError:
    return _with_retry_after(errors.catalog("rate_limited"), resp)


def _error_payload(resp: httpx.Response) -> dict[str, Any]:
    try:
        payload = resp.json()
    except ValueError:
        return {}
    error = payload.get("error") if isinstance(payload, dict) else None
    return error if isinstance(error, dict) else {}


def _error_code(resp: httpx.Response) -> str:
    return str(_error_payload(resp).get("code", ""))


def _error_problem(resp: httpx.Response) -> str:
    return str(_error_payload(resp).get("problem", ""))


def _unavailable_code(model: str) -> str | None:
    """The error a deployment base's sessions get from a control plane that predates them
    (``DeployBase.unavailable``), by the name the session opens it by."""
    from dreamscale import deploy_bases

    base = deploy_bases.of_model(model)
    return base.unavailable if base is not None else None


def _base_unknown(resp: httpx.Response) -> bool:
    """A refusal that means the control plane doesn't know the base's deployments: a bare 404
    or an unknown model, or a 422 on the request's model."""
    code = _error_code(resp)
    if resp.status_code == 404:
        return code in ("", "unknown_model", "model_not_found")
    return (
        resp.status_code == 422 and code == "invalid_request" and "model" in _error_problem(resp)
    )


def _deployment_in_use(resp: httpx.Response) -> errors.DreamscaleError:
    """409 ``deployment_in_use``: the server's problem, with the command that frees it."""
    payload = resp.json()
    error = errors.from_payload(payload)
    session_id = in_use_session_id(error, payload)
    return errors.catalog(
        "deployment_in_use",
        detail=error.info.problem,
        **({"session_id": session_id} if session_id else {}),
    )


def _raise_for_auth(resp: httpx.Response) -> None:
    if resp.status_code == 401:
        raise errors.catalog(
            "invalid_api_key",
            key_source=_key_source(resp),
            other_organization=_error_code(resp) == "api_key_other_organization",
        )


def _key_source(resp: httpx.Response) -> str | None:
    """"DREAMSCALE_API_KEY" when the rejected request carried the environment's key."""
    env_key = os.environ.get(API_KEY_ENV, "").strip()
    try:
        sent = resp.request.headers.get("authorization", "")
    except RuntimeError:  # a response built without a request
        return None
    return API_KEY_ENV if env_key and sent == f"Bearer {env_key}" else None


def _requested_rtc_kind(
    optimization_config: OptimizationConfig | dict[str, Any] | None,
) -> str | None:
    """inference_time or train_time when the request names one RTC kind."""
    if isinstance(optimization_config, OptimizationConfig):
        rtc = optimization_config.rtc
    elif isinstance(optimization_config, dict):
        rtc = optimization_config.get("rtc")
    else:
        return None
    return rtc if rtc in RTC_KINDS else None


def _unprocessable(
    resp: httpx.Response, optimization_config: OptimizationConfig | dict[str, Any] | None
) -> errors.DreamscaleError:
    payload = resp.json()
    kind = _requested_rtc_kind(optimization_config)
    error = payload.get("error") if isinstance(payload, dict) else None
    problem = str(error.get("problem", "")) if isinstance(error, dict) else ""
    if kind is not None and "optimization_config.rtc" in problem:
        # A control plane from before the RTC kinds rejects the value itself.
        return errors.catalog("rtc_kind_unavailable", kind=kind)
    return errors.from_payload(payload)
