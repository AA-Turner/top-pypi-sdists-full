"""PropertyRegistry — local authorization cache backed by the AAO registry.

Provides instant, no-network queries for property/agent authorization
relationships, with optional background sync via the change feed.
"""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from adcp.registry_sync import CursorStore, RegistrySync
from adcp.types.registry import FeedEvent

if TYPE_CHECKING:
    from adcp.registry import RegistryClient

logger = logging.getLogger(__name__)


class PropertyRegistry:
    """Local cache of property/agent authorization relationships.

    Queries are synchronous dict lookups — no network calls.
    Background sync is opt-in via ``auth_token``.

    Args:
        client: RegistryClient for API calls.
        auth_token: Bearer token for change feed access.
            If omitted, background sync is disabled (load-only mode).
        poll_interval: Seconds between feed polls (default 60).
        cursor_store: Optional CursorStore for feed cursor persistence.
    """

    def __init__(
        self,
        client: RegistryClient,
        *,
        auth_token: str | None = None,
        poll_interval: float = 60.0,
        cursor_store: CursorStore | None = None,
    ) -> None:
        self._client = client
        self._auth_token = auth_token
        self._poll_interval = poll_interval
        self._cursor_store = cursor_store
        self._domain_to_agents: dict[str, set[str]] = {}
        self._agent_to_domains: dict[str, set[str]] = {}
        self._loaded = False
        self._sync: RegistrySync | None = None
        self._task: asyncio.Task[None] | None = None

    # ------------------------------------------------------------------
    # Queries (synchronous, no network)
    # ------------------------------------------------------------------

    def is_authorized(self, agent_url: str, domain: str) -> bool:
        """Check if an agent is authorized for a domain."""
        return agent_url in self._domain_to_agents.get(domain, set())

    def get_domains(self, agent_url: str) -> frozenset[str]:
        """Get all domains authorized for an agent."""
        return frozenset(self._agent_to_domains.get(agent_url, set()))

    def get_agents(self, domain: str) -> frozenset[str]:
        """Get all agents authorized for a domain."""
        return frozenset(self._domain_to_agents.get(domain, set()))

    @property
    def agent_count(self) -> int:
        """Number of agents in the index."""
        return len(self._agent_to_domains)

    @property
    def domain_count(self) -> int:
        """Number of domains in the index."""
        return len(self._domain_to_agents)

    @property
    def loaded(self) -> bool:
        """Whether initial data has been loaded."""
        return self._loaded

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def load(self) -> None:
        """Fetch initial state from the registry API.

        Calls ``list_agents()`` and builds the bidirectional
        authorization index from each agent's ``publisher_domains``.
        """
        agents = await self._client.list_agents(properties=True)
        domain_to_agents: dict[str, set[str]] = {}
        agent_to_domains: dict[str, set[str]] = {}

        for agent in agents:
            domains = agent.publisher_domains or []
            if domains:
                agent_to_domains[agent.url] = set(domains)
                for domain in domains:
                    domain_to_agents.setdefault(domain, set()).add(agent.url)

        self._domain_to_agents = domain_to_agents
        self._agent_to_domains = agent_to_domains
        self._loaded = True
        logger.info(
            "PropertyRegistry loaded: %d agents, %d domains",
            len(agent_to_domains),
            len(domain_to_agents),
        )

    async def start(self) -> None:
        """Load initial state and start background sync.

        If ``auth_token`` was not provided, only loads initial state
        without starting the polling loop.
        """
        if not self._loaded:
            await self.load()

        if self._auth_token is None:
            logger.info(
                "PropertyRegistry: no auth_token, background sync disabled"
            )
            return

        self._sync = RegistrySync(
            self._client,
            auth_token=self._auth_token,
            poll_interval=self._poll_interval,
            cursor_store=self._cursor_store,
            types="authorization.*,agent.*,property.*",
        )
        self._sync.on_all(self._handle_event)
        self._task = asyncio.create_task(self._sync.start())

    async def stop(self) -> None:
        """Stop background sync."""
        if self._sync is not None:
            await self._sync.stop()
        if self._task is not None:
            await self._task
            self._task = None
        self._sync = None

    async def __aenter__(self) -> PropertyRegistry:
        await self.start()
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.stop()

    async def refresh(self) -> None:
        """Force a full reload from the API."""
        self._domain_to_agents.clear()
        self._agent_to_domains.clear()
        self._loaded = False
        await self.load()

    # ------------------------------------------------------------------
    # Event handling
    #
    # Trust model: events are fetched over HTTPS from the registry API
    # using a Bearer token. The events are not cryptographically signed.
    # A compromised transport or registry could inject forged events.
    # ------------------------------------------------------------------

    async def _handle_event(self, event: FeedEvent) -> None:
        """Route feed events to the appropriate handler."""
        et = event.event_type
        if et.startswith("authorization."):
            self._apply_authorization(event)
        elif et == "agent.deleted":
            self._remove_agent(event.entity_id)
        elif et in ("agent.created", "agent.updated"):
            await self._refresh_agent(event.payload.get("url", event.entity_id))
        elif et == "property.deleted":
            self._remove_domain(event.entity_id)
        # Unknown event types: ignore silently (forward compatible)

    _ADD_TYPES = {"authorization.created", "authorization.granted"}
    _REMOVE_TYPES = {"authorization.revoked", "authorization.deleted"}

    def _apply_authorization(self, event: FeedEvent) -> None:
        """Add or remove an authorization edge."""
        agent_url = event.payload.get("agent_url", "")
        domain = event.payload.get("domain", "")
        if not agent_url or not domain:
            return

        if event.event_type in self._ADD_TYPES:
            self._domain_to_agents.setdefault(domain, set()).add(agent_url)
            self._agent_to_domains.setdefault(agent_url, set()).add(domain)
        elif event.event_type in self._REMOVE_TYPES:
            self._domain_to_agents.get(domain, set()).discard(agent_url)
            self._agent_to_domains.get(agent_url, set()).discard(domain)

    def _remove_agent(self, agent_url: str) -> None:
        """Remove all authorization edges for an agent."""
        domains = self._agent_to_domains.pop(agent_url, set())
        for domain in domains:
            agents = self._domain_to_agents.get(domain)
            if agents is not None:
                agents.discard(agent_url)
                if not agents:
                    del self._domain_to_agents[domain]

    def _remove_domain(self, domain: str) -> None:
        """Remove all authorization edges for a domain."""
        agents = self._domain_to_agents.pop(domain, set())
        for agent_url in agents:
            domains = self._agent_to_domains.get(agent_url)
            if domains is not None:
                domains.discard(domain)
                if not domains:
                    del self._agent_to_domains[agent_url]

    async def _refresh_agent(self, agent_url: str) -> None:
        """Re-fetch a single agent's domains and update indexes."""
        try:
            data = await self._client.get_agent_domains(agent_url)
            new_domains = {
                p["domain"]
                for p in data.get("properties", [])
                if "domain" in p
            }
        except Exception as exc:
            logger.warning("Failed to refresh agent %s: %s", agent_url, exc)
            return

        # Remove old edges
        old_domains = self._agent_to_domains.get(agent_url, set())
        for d in old_domains:
            s = self._domain_to_agents.get(d)
            if s is not None:
                s.discard(agent_url)
                if not s:
                    del self._domain_to_agents[d]

        # Add new edges
        if new_domains:
            self._agent_to_domains[agent_url] = new_domains
            for d in new_domains:
                self._domain_to_agents.setdefault(d, set()).add(agent_url)
        else:
            self._agent_to_domains.pop(agent_url, None)
