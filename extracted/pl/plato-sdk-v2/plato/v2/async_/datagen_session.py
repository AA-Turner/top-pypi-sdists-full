"""Plato SDK v2 (async) - DatagenSession.

See :mod:`plato.v2.sync.datagen_session` for the sync counterpart.
"""

from __future__ import annotations

import asyncio
import logging

import httpx

from plato._generated.api.v2.artifacts import get_artifact
from plato._generated.api.v2.sessions import close as sessions_close
from plato._generated.api.v2.sessions import wait_for_ready as sessions_wait_for_ready
from plato.v2._datagen_launch import (
    REST_PORT,
    RUNTIME_ENV_ALIAS,
    DatagenResponse,
    build_launch_config,
)
from plato.v2._wait_for_ready import poll_until_ready_async
from plato.v2.async_.session import Session
from plato.v2.types import EnvFromArtifact, EnvFromResource, EnvFromSimulator

logger = logging.getLogger(__name__)


class DatagenSession(Session):
    """Async DatagenSession — see :class:`plato.v2.sync.datagen_session.DatagenSession`."""

    _runtime_connect_url: str | None = None

    @classmethod
    async def from_envs(  # type: ignore[override]
        cls,
        http_client: httpx.AsyncClient,
        api_key: str,
        envs: list[EnvFromSimulator | EnvFromArtifact | EnvFromResource],
        *,
        experiment: str,
        instruction: str,
        allow_prerelease: bool = True,
        timeout: int = 1800,
    ) -> DatagenSession:
        """Async DatagenSession.from_envs — see sync counterpart."""
        from plato.chronos.sdk import AsyncChronos

        base_url = str(http_client.base_url).rstrip("/")
        # build_launch_config uses sync httpx for the experiment + db_config
        # GETs (one-shot, fast). Re-using a tiny sync client keeps the
        # signature symmetric across sync/async without an async fork.
        with httpx.Client(base_url=base_url, timeout=30.0) as sync_http:
            template = build_launch_config(
                envs,
                experiment=experiment,
                http_client=sync_http,
                api_key=api_key,
                base_url=base_url,
                instruction=instruction,
            )
        world = template["world"]

        chronos = AsyncChronos(api_key=api_key)
        try:
            launch = await chronos.launch(
                package=world["package"],
                config=world["config"],
                runtime=world.get("runtime"),
                tags=(template.get("tags") or []) + ["datagen-session"],
                allow_prerelease=allow_prerelease,
            )
        finally:
            await chronos.close()

        session_id = launch.session_id
        logger.info(f"[DatagenSession] Chronos launched session={session_id}; waiting for Plato envs to be ready")

        try:
            session = await cls._hydrate_from_session_id(http_client, api_key, session_id, timeout=timeout)
        except Exception:
            try:
                cleanup = AsyncChronos(api_key=api_key)
                try:
                    await cleanup.stop(session_id)
                finally:
                    await cleanup.close()
            except Exception as stop_err:
                logger.warning(f"[DatagenSession] Failed to stop chronos session after hydrate failure: {stop_err}")
            raise

        runtime_env = session.get_env(RUNTIME_ENV_ALIAS)
        if runtime_env is None:
            raise RuntimeError(
                f"[DatagenSession] No '{RUNTIME_ENV_ALIAS}' env in session "
                f"after Chronos launch — got aliases "
                f"{[e.alias for e in session.envs]}"
            )
        session._runtime_connect_url = f"https://{runtime_env.job_id}--{REST_PORT}.connect.plato.so"
        logger.info(f"[DatagenSession] runtime connect URL: {session._runtime_connect_url}")

        await session._wait_for_rest_ready(timeout=timeout)
        # The world's reset() adds the customer's envs after our initial
        # wait_for_ready returned. Re-poll so session.get_env(alias) sees
        # them.
        try:
            await session.wait_until_ready(timeout=30.0)
        except Exception as exc:
            logger.warning(f"[DatagenSession] post-launch env refresh failed: {exc}")
        return session

    @classmethod
    async def _hydrate_from_session_id(
        cls,
        http_client: httpx.AsyncClient,
        api_key: str,
        session_id: str,
        timeout: int = 1800,
    ) -> DatagenSession:
        """Adopt an already-created Plato session (e.g. one Chronos launched)."""
        try:
            ready_response = await poll_until_ready_async(
                lambda per_call: sessions_wait_for_ready.asyncio(
                    client=http_client,
                    session_id=session_id,
                    timeout=per_call,
                    x_api_key=api_key,
                ),
                timeout=int(timeout),
            )
            context = cls._check_ready_response(ready_response, timeout)
        except (TimeoutError, RuntimeError):
            try:
                await sessions_close.asyncio(
                    client=http_client,
                    session_id=session_id,
                    x_api_key=api_key,
                )
            except Exception as close_err:
                logger.warning(f"Failed to close session after hydrate failure: {close_err}")
            raise

        if context.envs:
            for env_ctx in context.envs:
                if not env_ctx.simulator and env_ctx.artifact_id:
                    try:
                        artifact_info = await get_artifact.asyncio(
                            client=http_client,
                            artifact_id=env_ctx.artifact_id,
                            x_api_key=api_key,
                        )
                        env_ctx.simulator = artifact_info.simulator_name
                    except Exception:
                        pass

        session = cls(http_client=http_client, api_key=api_key, context=context)
        session._started = True
        await session.start_heartbeat()
        return session

    # ------------------------------------------------------------------
    # REST calls
    # ------------------------------------------------------------------

    async def _wait_for_rest_ready(self, timeout: float = 300.0) -> None:
        """Poll the runtime VM's REST server until it answers our health probe.

        Hits ``/api/health`` rather than ``/health`` because the connect.plato.so
        nginx router intercepts ``/health`` with its own response and would
        false-pass before the world's app is up.
        """
        assert self._runtime_connect_url is not None

        deadline = asyncio.get_event_loop().time() + timeout
        last_error: str | None = None
        while asyncio.get_event_loop().time() < deadline:
            try:
                resp = await self._http.get(
                    f"{self._runtime_connect_url}/api/health",
                    timeout=10.0,
                )
                if resp.status_code == 200 and "structured-execution-rest" in resp.text:
                    logger.info("[DatagenSession] REST server ready")
                    return
                last_error = f"status={resp.status_code} body={resp.text[:120]!r}"
            except Exception as exc:
                last_error = str(exc)
            await asyncio.sleep(2.0)
        raise TimeoutError(
            f"[DatagenSession] REST server on {self._runtime_connect_url} "
            f"did not become ready within {timeout}s (last: {last_error})"
        )

    async def send_message(self, prompt: str, *, env: str | None = None) -> None:
        """Async ``send_message`` — see sync counterpart."""
        self._check_closed()
        if self._runtime_connect_url is None:
            raise RuntimeError(
                "DatagenSession.send_message requires a DatagenSession created via DatagenSession.from_envs()."
            )
        resp = await self._http.post(
            f"{self._runtime_connect_url}/send_message",
            json={"prompt": prompt, "env_alias": env},
            timeout=30.0,
        )
        if resp.status_code == 409:
            raise RuntimeError(resp.json().get("detail", "send_message rejected"))
        resp.raise_for_status()

    async def poll_message(self) -> DatagenResponse:
        """Async ``poll_message`` — see sync counterpart."""
        self._check_closed()
        if self._runtime_connect_url is None:
            raise RuntimeError(
                "DatagenSession.poll_message requires a DatagenSession created via DatagenSession.from_envs()."
            )
        resp = await self._http.post(
            f"{self._runtime_connect_url}/poll_message",
            timeout=30.0,
        )
        resp.raise_for_status()
        return DatagenResponse.model_validate(resp.json())

    async def stop_conversation(self, *, timeout: float = 60.0) -> None:
        self._check_closed()
        if self._runtime_connect_url is None:
            raise RuntimeError(
                "DatagenSession.stop_conversation requires a DatagenSession created via DatagenSession.from_envs()."
            )
        resp = await self._http.post(
            f"{self._runtime_connect_url}/terminate_step",
            timeout=timeout,
        )
        if resp.status_code == 409:
            return
        resp.raise_for_status()

    # ------------------------------------------------------------------
    # Inherited Session methods that don't apply to a DatagenSession.
    # See the sync counterpart for rationale on each.
    # ------------------------------------------------------------------

    _UNSUPPORTED_MSG = (
        "DatagenSession.{op} is not supported — {reason}. "
        "Use plato.datagen_sessions.create(envs=..., experiment=...) to open a "
        "new session with different state."
    )

    async def reset(self, *args, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            self._UNSUPPORTED_MSG.format(
                op="reset()",
                reason="it would tear down the runtime VM the agent loop is attached to",
            )
        )

    async def add_env(self, *args, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            self._UNSUPPORTED_MSG.format(
                op="add_env()",
                reason="envs are fixed at launch",
            )
        )

    async def remove_env(self, *args, **kwargs):
        raise NotImplementedError(self._UNSUPPORTED_MSG.format(op="remove_env()", reason="envs are fixed at launch"))

    async def evaluate(self, *args, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.evaluate() is not supported — evaluation is tied to "
            "test-case scoring. DatagenSession isn't created from a test case."
        )

    async def link_testcase(self, *args, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.link_testcase() is not supported — DatagenSession isn't "
            "created from a test case and doesn't carry testcase scoring."
        )

    async def setup_sandbox(self, *args, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.setup_sandbox() is not supported — sandbox setup runs "
            "at world-launch time, not after the session is up."
        )

    @classmethod
    async def from_testcase(cls, *args, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.from_testcase() is not supported. Use "
            "plato.datagen_sessions.create(envs=..., experiment=...)."
        )

    @classmethod
    async def from_artifacts(cls, *args, **kwargs):  # type: ignore[override]
        raise NotImplementedError(
            "DatagenSession.from_artifacts() is not supported. Use "
            "plato.datagen_sessions.create(envs=[Env.artifact(...), ...], "
            "experiment=...)."
        )

    async def login(self, *args, **kwargs):  # type: ignore[override]
        """Login to all sim envs, skipping the agent's ``runtime`` env.

        See sync counterpart for rationale.
        """
        original = self._envs
        if original is not None:
            sim_envs = [e for e in original if e.alias != RUNTIME_ENV_ALIAS]
        else:
            sim_envs = [e for e in self.envs if e.alias != RUNTIME_ENV_ALIAS]
        self._envs = sim_envs
        try:
            return await super().login(*args, **kwargs)
        finally:
            self._envs = original

    def __repr__(self) -> str:
        env_count = len(self._context.envs) if self._context.envs else 0
        return f"DatagenSession(session_id={self.session_id!r}, envs={env_count})"
