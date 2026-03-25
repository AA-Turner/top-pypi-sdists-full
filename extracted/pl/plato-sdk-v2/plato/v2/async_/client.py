"""Plato SDK v2 - Asynchronous Client."""

from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv

from plato.v2.async_.artifact import AsyncArtifactManager
from plato.v2.async_.session import Session
from plato.v2.types import EnvFromArtifact, EnvFromResource, EnvFromSimulator

load_dotenv()

DEFAULT_BASE_URL = "https://plato.so"
DEFAULT_TIMEOUT = 600.0


class AsyncSessionManager:
    """Manager for async session operations, accessed via plato.sessions."""

    def __init__(self, http_client: httpx.AsyncClient, api_key: str):
        self._http = http_client
        self._api_key = api_key

    async def create(
        self,
        *,
        envs: list[EnvFromSimulator | EnvFromArtifact | EnvFromResource] | None = None,
        testcase: str | None = None,
        artifacts: list[str] | None = None,
        timeout: int = 1800,
        agent_artifact_id: str | None = None,
        connect_network: bool = True,
        wait: bool = True,
        shutdown_callback_url: str | None = None,
        shutdown_callback_token: str | None = None,
    ) -> Session:
        """Create a new session.

        Provide exactly one of ``testcase``, ``envs``, or ``artifacts``.

        - **testcase**: Derives environments from the test case's artifacts,
          waits for readiness, and automatically resets for mutation logging.
        - **envs**: Creates from explicit environment configs. Does NOT
          auto-reset; call ``await session.reset()`` when ready.
        - **artifacts**: Creates from artifact IDs directly. Does NOT
          auto-reset; call ``await session.reset()`` when ready.

        Args:
            envs: List of environment configurations (use Env.simulator(), Env.artifact(), or Env.resource())
            testcase: Test case public ID to create session from (auto-resets)
            artifacts: List of simulator artifact IDs to create session from
            timeout: VM timeout in seconds
            agent_artifact_id: Optional agent artifact ID to associate with the session
            connect_network: If True, automatically connect all VMs to a WireGuard network
            wait: If True (default), block until all environments are ready. If False,
                return immediately after session creation -- the caller must call
                ``await session.wait_until_ready()`` before accessing environments.

        Returns:
            A new Session instance. When ``wait=False`` environments may not be ready yet.

        Raises:
            ValueError: If more than one of envs/testcase/artifacts is provided, or none
            RuntimeError: If any environment fails to create or become ready
            TimeoutError: If environments don't become ready within timeout

        Examples:
            >>> from plato.v2 import AsyncPlato, Env
            >>> plato = AsyncPlato()
            >>>
            >>> # From test case (auto-resets)
            >>> session = await plato.sessions.create(testcase="tc_abc123")
            >>>
            >>> # From environments (manual reset)
            >>> session = await plato.sessions.create(envs=[Env.simulator("espocrm")])
            >>> await session.reset()
            >>>
            >>> # From artifacts (manual reset)
            >>> session = await plato.sessions.create(artifacts=["artifact-1", "artifact-2"])
            >>> await session.reset()
        """
        provided = sum(x is not None for x in (envs, testcase, artifacts))
        if provided != 1:
            raise ValueError("Must specify exactly one of: envs, testcase, or artifacts")

        if testcase is not None:
            session = await Session.from_testcase(
                http_client=self._http,
                api_key=self._api_key,
                testcase_id=testcase,
                timeout=timeout,
            )
        elif artifacts is not None:
            session = await Session.from_artifacts(
                http_client=self._http,
                api_key=self._api_key,
                artifact_ids=artifacts,
                timeout=timeout,
            )
        elif envs is not None:
            session = await Session.from_envs(
                http_client=self._http,
                api_key=self._api_key,
                envs=envs,
                timeout=timeout,
                agent_artifact_id=agent_artifact_id,
                wait=wait,
                shutdown_callback_url=shutdown_callback_url,
                shutdown_callback_token=shutdown_callback_token,
            )
        else:
            raise ValueError("Must specify exactly one of: envs, testcase, or artifacts")

        if not wait:
            return session

        if connect_network:
            try:
                await session.connect_network()
            except Exception:
                import logging

                logging.getLogger(__name__).info(f"Network connection failed, closing session {session.session_id}")
                try:
                    await session.close()
                    logging.getLogger(__name__).info(f"Session {session.session_id} closed")
                except Exception as close_err:
                    logging.getLogger(__name__).warning(f"Failed to close session: {close_err}")
                raise

        return session


class AsyncPlato:
    """Asynchronous Plato client for v2 API.

    Usage:
        from plato.v2 import AsyncPlato, Env

        plato = AsyncPlato()
        session = await plato.sessions.create(envs=[Env.simulator("espocrm")])
        await session.start_heartbeat()

        await session.reset()
        state = await session.get_state()

        for env in session.envs:
            result = await env.execute("ls -la")

        await session.close()
        await plato.close()
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        authorization: str | None = None,
    ):
        self.api_key = api_key or os.environ.get("PLATO_API_KEY")
        if not self.api_key and not authorization:
            raise ValueError("API key required. Set PLATO_API_KEY or pass api_key=")
        # When using authorization, provide a placeholder api_key for internal use
        if not self.api_key:
            self.api_key = "authorization-auth"

        # Compose base URL, strip trailing '/api' if present, then trailing slashes
        url = base_url or os.environ.get("PLATO_BASE_URL", DEFAULT_BASE_URL)
        if url.endswith("/api"):
            url = url[:-4]
        self.base_url = url.rstrip("/")
        self.timeout = timeout

        headers: dict[str, str] = {}
        if authorization:
            headers["Authorization"] = authorization

        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
            headers=headers,
        )

        self.sessions = AsyncSessionManager(self._http, self.api_key)
        self.artifacts = AsyncArtifactManager(self._http, self.api_key)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()
