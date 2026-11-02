import asyncio
import gzip
import json
import logging
import warnings
from typing import Any, ClassVar, Literal
from uuid import UUID, uuid4

import httpx
import httpx_aiohttp
from aviary.env import Frame
from pydantic import BaseModel
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from edison_client.clients.state_blobs import means_v0d2_routes_absent
from edison_client.models.app import Stage
from edison_client.models.rest import (
    AgentStateInitRequest,
    EnvironmentFrameInitRequest,
    FinalEnvironmentRequest,
    PermittedAccessors,
    ShareStatus,
    StateFinalizeRequest,
    StateUploadInitResponse,
    StoreAgentStatePostRequest,
    StoreEnvironmentFrameRequest,
    TrajectoryPatchRequest,
)
from edison_client.utils.monitoring import log_timing

logger = logging.getLogger(__name__)


def _is_transient_error(exc: BaseException) -> bool:
    """Retry timeouts, network drops, and 5xx; client errors (4xx) are final."""
    if isinstance(exc, (httpx.TimeoutException, httpx.NetworkError)):
        return True
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.is_server_error


class JobClient:
    REQUEST_TIMEOUT: ClassVar[float] = 30.0  # sec
    LARGE_PAYLOAD_TIMEOUT: ClassVar[float] = 120.0  # sec, for streaming uploads
    MAX_RETRY_ATTEMPTS: ClassVar[int] = 3
    RETRY_MULTIPLIER: ClassVar[int] = 1
    MAX_RETRY_WAIT: ClassVar[int] = 10

    def __init__(
        self,
        environment: str,
        agent: str,
        auth_token: str,
        base_uri: str = Stage.LOCAL.value,
        trajectory_id: str | UUID | None = None,
    ):
        self.base_uri = base_uri
        self.agent = agent
        self.environment = environment
        self.oauth_jwt = auth_token
        self.current_timestep = 0
        self.current_step: str | None = None
        # Flipped to False the first time the server proves it has no v0.2
        # routes (a framework-level 404/405 on init), so later stores skip the
        # doomed init round-trip. An application 404 — e.g. the trajectory does
        # not exist yet — does NOT flip it, so a transient missing row can't
        # permanently force inline v0.1 writes.
        self._object_store_supported = True
        try:
            self.trajectory_id = self._cast_trajectory_id(trajectory_id)
            logger.info(
                f"Initialized JobClient for agent {agent} with trajectory_id {self.trajectory_id}",
            )
        except ValueError:
            logger.exception("Failed to initialize JobClient")
            raise

    @staticmethod
    def _cast_trajectory_id(provided_trajectory_id: str | UUID | None) -> str:
        if provided_trajectory_id is None:
            return str(uuid4())
        if isinstance(provided_trajectory_id, str):
            return provided_trajectory_id
        if isinstance(provided_trajectory_id, UUID):
            return str(provided_trajectory_id)
        raise ValueError("Invalid trajectory ID provided")

    async def finalize_environment(self, status: str) -> None:
        data = FinalEnvironmentRequest(status=status)
        try:
            async with httpx_aiohttp.HttpxAiohttpClient(
                timeout=self.REQUEST_TIMEOUT
            ) as client:
                url = f"{self.base_uri}/v0.1/trajectories/{self.trajectory_id}/environment-frame"
                headers = {
                    "Authorization": f"Bearer {self.oauth_jwt}",
                    "x-trajectory-id": self.trajectory_id,
                }

                response = await client.patch(
                    url=url,
                    json=data.model_dump(mode="json"),
                    headers=headers,
                )

                response.raise_for_status()
                logger.debug(f"Environment updated with status {status}")
        except httpx.HTTPStatusError:
            logger.exception(
                f"HTTP error while finalizing environment. "
                f"Status code: {response.status_code}, "
                f"Response: {response.text}",
            )
        except httpx.TimeoutException:
            logger.exception(
                f"Timeout while finalizing environment after {self.REQUEST_TIMEOUT}s",
            )
            raise
        except httpx.NetworkError:
            logger.exception("Network error while finalizing environment")
            raise
        except Exception:
            logger.exception("Unexpected error while finalizing environment")
            raise

    # ------------------------------------------------------------------
    # v0.2 — object-storage-backed writes (default for new SDK).
    #
    # Three legs per call: POST init -> PUT signed URL -> POST finalize.
    # Each leg retries independently on transient failures (timeouts,
    # network drops, 5xx) and the init result is reused across those
    # retries, so a flaky finalize never re-uploads the blob. Re-finalizing
    # a COMPLETE row is a 204 no-op, so a retry that lost the finalize
    # response is safe.
    #
    # The init is idempotent via a client-supplied ``id``: every retry
    # sends the same id, the server creates the row (and object key) from
    # it, so an init whose response was lost after the server already
    # inserted the row never strands a duplicate PENDING row.
    #
    # The uploaded blob is the bare ``state`` value — NOT the v0.1 POST
    # request envelope. GET readers (server-side inlining on v0.1, the
    # browser on v0.2) splice the parsed blob verbatim into the row's
    # ``state`` field, so any wrapper would come back double-nested.
    # Row metadata travels in the init request instead.
    #
    # If the server predates the v0.2 routes (a framework-level 404/405 on
    # init), we fall back to the inline v0.1 endpoints for the rest of this
    # client's life. An application 404 (the trajectory itself is missing)
    # is re-raised instead, since the route exists and may succeed once the
    # trajectory appears.
    # ------------------------------------------------------------------

    @staticmethod
    def _serialize_and_compress(payload: Any) -> tuple[bytes, int]:
        with log_timing("serialize_json"):
            json_bytes = json.dumps(payload).encode("utf-8")
        with log_timing("gzip", raw_bytes=len(json_bytes)):
            compressed = gzip.compress(json_bytes)
        return compressed, len(json_bytes)

    async def store_agent_state(self, step: str, state: BaseModel | dict) -> None:
        """Store agent state via the v0.2 object-storage flow."""
        self.current_step = step

        trace_params: dict[str, str | int] = {
            "trajectory_id": self.trajectory_id,
            "agent": self.agent,
            "environment": self.environment,
            "step": step,
        }
        with log_timing("agent_state.model_dump", **trace_params) as timing:
            state_data = (
                state.model_dump(mode="json", context={"include_info": True})
                if isinstance(state, BaseModel)
                else state
            )

            if state_data and state_data.get("transition"):
                timestep = state_data.get("transition", {}).get("timestep")
                if timestep is not None:
                    self.current_timestep = timestep
            timing["timestep"] = self.current_timestep
        trace_params["timestep"] = self.current_timestep

        if not self._object_store_supported:
            await self._store_agent_state_inline(state_data)
            return

        with log_timing("agent_state.serialize_compress", **trace_params) as timing:
            compressed, raw_size = await asyncio.to_thread(
                self._serialize_and_compress, state_data
            )
            timing.update(raw_bytes=raw_size, compressed_bytes=len(compressed))
        logger.debug(
            f"Compressed agent state payload: {raw_size} -> {len(compressed)} bytes "
            f"({len(compressed) / raw_size:.1%})",
        )

        init_request = AgentStateInitRequest(
            id=uuid4(),
            agent_id=self.agent,
            trajectory_timestep=self.current_timestep,
            step=self.current_step,
            content_encoding="gzip",
            size_bytes=raw_size,
        )

        try:
            stored = await self._store_via_object_store(
                resource="agent-state",
                init_payload=init_request.model_dump(mode="json"),
                blob=compressed,
                raw_size=raw_size,
                operation_prefix="store_agent_state",
                trace_params=trace_params,
            )
        except Exception:
            logger.exception(f"Failed to store agent state for step {step}")
            raise

        if stored:
            logger.info(f"Successfully stored agent state for step {step}")
            return

        logger.warning(
            "Server has no v0.2 trajectory state routes; falling back to "
            "inline v0.1 agent-state storage for this client."
        )
        self._object_store_supported = False
        await self._store_agent_state_inline(state_data)

    async def store_environment_frame(self, state: Frame) -> None:
        """Store environment frame via the v0.2 object-storage flow."""
        state_identifier = None
        if self.current_step is not None:
            state_identifier = (
                f"{self.agent}-{self.current_step}-{self.current_timestep}"
            )

        logger.debug(f"Storing environment frame for state {state_identifier}")

        trace_params: dict[str, str | int] = {
            "trajectory_id": self.trajectory_id,
            "agent": self.agent,
            "environment": self.environment,
            "timestep": self.current_timestep,
        }
        if self.current_step:
            trace_params["step"] = self.current_step
        if state_identifier:
            trace_params["state_identifier"] = state_identifier

        with log_timing("environment_frame.model_dump", **trace_params):
            frame_data = state.model_dump(mode="json")

        if not self._object_store_supported:
            await self._store_environment_frame_inline(frame_data, state_identifier)
            return

        with log_timing(
            "environment_frame.serialize_compress", **trace_params
        ) as timing:
            compressed, raw_size = await asyncio.to_thread(
                self._serialize_and_compress, frame_data
            )
            timing.update(raw_bytes=raw_size, compressed_bytes=len(compressed))

        init_request = EnvironmentFrameInitRequest(
            id=uuid4(),
            agent_state_point_in_time=state_identifier,
            current_agent_step=self.current_step,
            trajectory_timestep=self.current_timestep,
            content_encoding="gzip",
            size_bytes=raw_size,
        )

        try:
            stored = await self._store_via_object_store(
                resource="environment-frame",
                init_payload=init_request.model_dump(mode="json"),
                blob=compressed,
                raw_size=raw_size,
                operation_prefix="store_environment_frame",
                trace_params=trace_params,
            )
        except Exception:
            logger.exception(
                f"Failed to store environment frame for state {state_identifier}"
            )
            raise

        if stored:
            logger.debug(
                f"Successfully stored environment frame for state {state_identifier}",
            )
            return

        logger.warning(
            "Server has no v0.2 trajectory state routes; falling back to "
            "inline v0.1 environment-frame storage for this client."
        )
        self._object_store_supported = False
        await self._store_environment_frame_inline(frame_data, state_identifier)

    async def _store_via_object_store(
        self,
        *,
        resource: Literal["agent-state", "environment-frame"],
        init_payload: dict,
        blob: bytes,
        raw_size: int,
        operation_prefix: str,
        trace_params: dict,
    ) -> bool:
        """Run the init -> upload -> finalize legs against the v0.2 routes.

        One shared HTTP client serves all three legs. Returns ``False``
        (before uploading anything) only when the server proves it has no v0.2
        routes — a framework-level 404/405 on init (see
        ``means_v0d2_routes_absent``) — so the caller falls back to the inline
        v0.1 path. An application 404 (the trajectory itself is missing) is
        re-raised instead of swallowed, so one early missing-row failure never
        permanently forces inline v0.1 writes for this client.
        """
        base_path = f"/v0.2/trajectories/{self.trajectory_id}/{resource}"
        # LARGE_PAYLOAD_TIMEOUT accommodates the blob PUT; the two small
        # POST legs just finish well within it.
        async with httpx_aiohttp.HttpxAiohttpClient(
            timeout=self.LARGE_PAYLOAD_TIMEOUT
        ) as client:
            try:
                with log_timing(f"{operation_prefix}.init", **trace_params):
                    init = await self._post_state_init(
                        client,
                        base_path,
                        init_payload,
                    )
            except httpx.HTTPStatusError as e:
                if means_v0d2_routes_absent(e.response):
                    return False
                raise
            with log_timing(
                f"{operation_prefix}.upload",
                **trace_params,
                raw_bytes=raw_size,
                compressed_bytes=len(blob),
            ):
                await self._put_state_blob(
                    client,
                    init.upload_url,
                    blob,
                )
            with log_timing(f"{operation_prefix}.finalize", **trace_params):
                await self._post_state_finalize(
                    client,
                    f"{base_path}/{init.id}/finalize",
                    StateFinalizeRequest(size_bytes=raw_size).model_dump(mode="json"),
                )
        return True

    @retry(
        retry=retry_if_exception(_is_transient_error),
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _post_state_init(
        self,
        client: httpx.AsyncClient,
        path: str,
        payload: dict,
    ) -> StateUploadInitResponse:
        url = f"{self.base_uri}{path}"
        headers = {
            "Authorization": f"Bearer {self.oauth_jwt}",
            "Content-Type": "application/json",
            "x-trajectory-id": self.trajectory_id,
        }
        response = await client.post(
            url=url,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        return StateUploadInitResponse.model_validate(response.json())

    @staticmethod
    @retry(
        retry=retry_if_exception(_is_transient_error),
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _put_state_blob(
        client: httpx.AsyncClient,
        upload_url: str,
        body: bytes,
    ) -> None:
        # Direct PUT to the signed URL — bypasses the API gateway entirely.
        # ``Authorization`` must NOT be sent: the signed URL carries its own
        # credentials, and a Bearer token here would be rejected by GCS / S3.
        headers = {
            "Content-Type": "application/json",
            "Content-Encoding": "gzip",
        }
        response = await client.put(
            url=upload_url,
            content=body,
            headers=headers,
        )
        response.raise_for_status()

    @retry(
        retry=retry_if_exception(_is_transient_error),
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _post_state_finalize(
        self,
        client: httpx.AsyncClient,
        path: str,
        payload: dict,
    ) -> None:
        url = f"{self.base_uri}{path}"
        headers = {
            "Authorization": f"Bearer {self.oauth_jwt}",
            "Content-Type": "application/json",
            "x-trajectory-id": self.trajectory_id,
        }
        response = await client.post(
            url=url,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()

    # ------------------------------------------------------------------
    # Inline v0.1 writes. Used as the automatic fallback when the server
    # has no v0.2 routes; the ``_v0d1`` wrappers below are deprecated
    # escape hatches for callers explicitly pinning to this path.
    # ------------------------------------------------------------------

    @retry(
        retry=retry_if_exception(_is_transient_error),
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _store_agent_state_inline(self, state_data: Any) -> None:
        """POST the full agent state body to the inline v0.1 endpoint."""
        data = StoreAgentStatePostRequest(
            agent_id=self.agent,
            step=self.current_step,
            state=state_data,
            trajectory_timestep=self.current_timestep,
        )

        compressed, _ = await asyncio.to_thread(
            self._serialize_and_compress, data.model_dump(mode="json")
        )

        try:
            async with httpx_aiohttp.HttpxAiohttpClient(
                timeout=self.LARGE_PAYLOAD_TIMEOUT
            ) as client:
                url = f"{self.base_uri}/v0.1/trajectories/{self.trajectory_id}/agent-state"
                headers = {
                    "Authorization": f"Bearer {self.oauth_jwt}",
                    "Content-Type": "application/json",
                    "Content-Encoding": "gzip",
                    "x-trajectory-id": self.trajectory_id,
                }

                response = await client.post(
                    url=url,
                    content=compressed,
                    headers=headers,
                )
                response.raise_for_status()
                logger.info(
                    f"Successfully stored agent state for step {self.current_step}"
                )
        except Exception:
            logger.exception(
                f"Failed to store agent state inline for step {self.current_step}"
            )
            raise

    @retry(
        retry=retry_if_exception(_is_transient_error),
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_MULTIPLIER, max=MAX_RETRY_WAIT),
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def _store_environment_frame_inline(
        self, frame_data: Any, state_identifier: str | None
    ) -> None:
        """POST the full environment frame body to the inline v0.1 endpoint."""
        data = StoreEnvironmentFrameRequest(
            agent_state_point_in_time=state_identifier,
            current_agent_step=self.current_step,
            state=frame_data,
            trajectory_timestep=self.current_timestep,
        )

        try:
            async with httpx_aiohttp.HttpxAiohttpClient(
                timeout=self.REQUEST_TIMEOUT
            ) as client:
                url = f"{self.base_uri}/v0.1/trajectories/{self.trajectory_id}/environment-frame"
                headers = {
                    "Authorization": f"Bearer {self.oauth_jwt}",
                    "x-trajectory-id": self.trajectory_id,
                }
                response = await client.post(
                    url=url,
                    json=data.model_dump(mode="json"),
                    headers=headers,
                )
                response.raise_for_status()
                logger.debug(
                    f"Successfully stored environment frame for state {state_identifier}",
                )
        except Exception:
            logger.exception(
                f"Failed to store environment frame inline for state {state_identifier}",
            )
            raise

    # ------------------------------------------------------------------
    # v0.1 escape hatches. Deprecated; will be removed once all
    # deployments have v0.2 support and we've confirmed no callers
    # are pinning to these paths.
    # ------------------------------------------------------------------

    async def _store_agent_state_v0d1(self, step: str, state: BaseModel | dict) -> None:
        """Deprecated: send the full state inline to the v0.1 endpoint."""
        warnings.warn(
            "_store_agent_state_v0d1 is deprecated; use store_agent_state.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.current_step = step

        state_data = (
            state.model_dump(mode="json", context={"include_info": True})
            if isinstance(state, BaseModel)
            else state
        )

        if state_data and state_data.get("transition"):
            timestep = state_data.get("transition", {}).get("timestep")
            if timestep is not None:
                self.current_timestep = timestep

        await self._store_agent_state_inline(state_data)

    async def _store_environment_frame_v0d1(self, state: Frame) -> None:
        """Deprecated: send the full state inline to the v0.1 endpoint."""
        warnings.warn(
            "_store_environment_frame_v0d1 is deprecated; use store_environment_frame.",
            DeprecationWarning,
            stacklevel=2,
        )
        state_identifier = None
        if self.current_step is not None:
            state_identifier = (
                f"{self.agent}-{self.current_step}-{self.current_timestep}"
            )

        await self._store_environment_frame_inline(
            state.model_dump(mode="json"), state_identifier
        )

    async def patch_trajectory(  # noqa: PLR0917
        self,
        share_status: ShareStatus | str | None = None,
        permitted_accessors: PermittedAccessors | None = None,
        notification_enabled: bool | None = None,
        notification_type: str | None = None,
        min_estimated_time: float | None = None,
        max_estimated_time: float | None = None,
    ) -> None:
        share_status_enum = (
            ShareStatus(share_status) if isinstance(share_status, str) else share_status
        )

        data = TrajectoryPatchRequest(
            share_status=share_status_enum,
            permitted_accessors=permitted_accessors,
            notification_enabled=notification_enabled,
            notification_type=notification_type,
            min_estimated_time=min_estimated_time,
            max_estimated_time=max_estimated_time,
        )
        try:
            async with httpx_aiohttp.HttpxAiohttpClient(
                timeout=self.REQUEST_TIMEOUT
            ) as client:
                url = f"{self.base_uri}/v0.1/trajectories/{self.trajectory_id}"
                headers = {
                    "Authorization": f"Bearer {self.oauth_jwt}",
                    "x-trajectory-id": self.trajectory_id,
                }
                response = await client.patch(
                    url=url,
                    json=data.model_dump(mode="json", exclude_none=True),
                    headers=headers,
                )
                response.raise_for_status()
                logger.debug("Trajectory updated successfully")
        except httpx.HTTPStatusError as e:
            logger.exception(
                "HTTP error while patching trajectory. "
                f"Status code: {e.response.status_code}, "
                f"Response: {e.response.text}",
            )
        except httpx.TimeoutException:
            logger.exception(
                f"Timeout while patching trajectory after {self.REQUEST_TIMEOUT}s",
            )
            raise
        except httpx.NetworkError:
            logger.exception("Network error while patching trajectory")
            raise
        except Exception:
            logger.exception("Unexpected error while patching trajectory")
            raise
