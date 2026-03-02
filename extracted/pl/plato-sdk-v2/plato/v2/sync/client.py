"""Plato SDK v2 - Synchronous Client."""

from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv

from plato.v2.sync.artifact import ArtifactManager
from plato.v2.sync.session import Session
from plato.v2.types import EnvFromArtifact, EnvFromResource, EnvFromSimulator

load_dotenv()

DEFAULT_BASE_URL = "https://plato.so"
DEFAULT_TIMEOUT = 600.0


class SessionManager:
    """Manager for session operations, accessed via plato.sessions."""

    def __init__(self, http_client: httpx.Client, api_key: str):
        self._http = http_client
        self._api_key = api_key

    def create(
        self,
        *,
        envs: list[EnvFromSimulator | EnvFromArtifact | EnvFromResource] | None = None,
        task: str | None = None,
        timeout: int = 1800,
        connect_network: bool = True,
    ) -> Session:
        """Create a new session.

        Provide either `envs` or `task`, not both.

        Args:
            envs: List of environment configurations (use Env.simulator(), Env.artifact(), or Env.resource())
            task: Task public ID to create session from
            timeout: VM timeout in seconds
            connect_network: If True, automatically connect all VMs to a WireGuard network

        Returns:
            A new Session instance with all environments ready

        Raises:
            ValueError: If both envs and task are provided, or neither
            RuntimeError: If any environment fails to create or become ready
            TimeoutError: If environments don't become ready within timeout

        Examples:
            >>> from plato.v2 import Plato, Env
            >>> plato = Plato()
            >>>
            >>> # From environments
            >>> session = plato.sessions.create(envs=[Env.simulator("espocrm")])
            >>>
            >>> # From task
            >>> session = plato.sessions.create(task="abc123")
            >>>
            >>> # With networking enabled automatically
            >>> session = plato.sessions.create(envs=[...], connect_network=True)
        """
        if envs is not None and task is not None:
            raise ValueError("Cannot specify both envs and task")

        if task is not None:
            session = Session.from_task(
                http_client=self._http,
                api_key=self._api_key,
                task_id=task,
                timeout=timeout,
            )
        elif envs is not None:
            session = Session.from_envs(
                http_client=self._http,
                api_key=self._api_key,
                envs=envs,
                timeout=timeout,
            )
        else:
            raise ValueError("Must specify either envs or task")

        if connect_network:
            try:
                session.connect_network()
            except Exception:
                # Clean up session if network connection fails
                import logging

                logging.getLogger(__name__).info(f"Network connection failed, closing session {session.session_id}")
                try:
                    session.close()
                    logging.getLogger(__name__).info(f"Session {session.session_id} closed")
                except Exception as close_err:
                    logging.getLogger(__name__).warning(f"Failed to close session: {close_err}")
                raise

        return session


class Plato:
    """Synchronous Plato client for v2 API.

    Usage:
        from plato.v2 import Plato, Env

        plato = Plato()
        session = plato.sessions.create(envs=[Env.simulator("espocrm")])
        session.start_heartbeat()

        session.reset()
        state = session.get_state()

        for env in session.envs:
            result = env.execute("ls -la")

        session.close()
        plato.close()
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        http_client: httpx.Client | None = None,
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

        self._owns_http = http_client is None
        self._http = http_client or httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
        )

        self.sessions = SessionManager(self._http, self.api_key)
        self.artifacts = ArtifactManager(self._http, self.api_key)

    def close(self) -> None:
        """Close the underlying HTTP client (if we own it)."""
        if self._owns_http:
            self._http.close()
