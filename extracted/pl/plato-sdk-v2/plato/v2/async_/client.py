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
        task: str | None = None,
        timeout: int = 1800,
        agent_artifact_id: str | None = None,
        connect_network: bool = True,
        wait: bool = True,
    ) -> Session:
        """Create a new session.

        Provide either `envs` or `task`, not both.

        Args:
            envs: List of environment configurations (use Env.simulator(), Env.artifact(), or Env.resource())
            task: Task public ID to create session from
            timeout: VM timeout in seconds
            agent_artifact_id: Optional agent artifact ID to associate with the session
            connect_network: If True, automatically connect all VMs to a WireGuard network
            wait: If True (default), block until all environments are ready. If False,
                return immediately after session creation — the caller must call
                ``await session.wait_until_ready()`` before accessing environments,
                and ``await session.connect_network()`` / ``await session.start_heartbeat()``
                manually.

        Returns:
            A new Session instance. When ``wait=False`` environments may not be ready yet.

        Raises:
            ValueError: If both envs and task are provided, or neither
            RuntimeError: If any environment fails to create or become ready
            TimeoutError: If environments don't become ready within timeout

        Examples:
            >>> from plato.v2 import AsyncPlato, Env
            >>> plato = AsyncPlato()
            >>>
            >>> # From environments
            >>> session = await plato.sessions.create(envs=[Env.simulator("espocrm")])
            >>>
            >>> # From task
            >>> session = await plato.sessions.create(task="abc123")
            >>>
            >>> # Non-blocking: get session ID immediately, wait later
            >>> session = await plato.sessions.create(envs=[...], wait=False)
            >>> print(session.session_id)  # available immediately
            >>> await session.wait()  # waits for VMs, starts heartbeat, connects network
        """
        if envs is not None and task is not None:
            raise ValueError("Cannot specify both envs and task")

        if task is not None:
            session = await Session.from_task(
                http_client=self._http,
                api_key=self._api_key,
                task_id=task,
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
            )
        else:
            raise ValueError("Must specify either envs or task")

        if not wait:
            return session

        if connect_network:
            try:
                await session.connect_network()
            except Exception:
                # Clean up session if network connection fails
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
    ):
        self.api_key = api_key or os.environ.get("PLATO_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set PLATO_API_KEY or pass api_key=")

        # Compose base URL, strip trailing '/api' if present, then trailing slashes
        url = base_url or os.environ.get("PLATO_BASE_URL", DEFAULT_BASE_URL)
        if url.endswith("/api"):
            url = url[:-4]
        self.base_url = url.rstrip("/")
        self.timeout = timeout

        self._http = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
        )

        self.sessions = AsyncSessionManager(self._http, self.api_key)
        self.artifacts = AsyncArtifactManager(self._http, self.api_key)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.aclose()
