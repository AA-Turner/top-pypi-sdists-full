"""Internal per-service HTTP transport construction.

The top-level :class:`smplkit.SmplClient` / :class:`smplkit.AsyncSmplClient`
needs one authenticated transport per backend service (app, config, flags,
logging, jobs) plus a context-registration buffer that ``client.platform``
owns. This module builds them in one place so the construction is
side-effect-free (transports connect lazily on first call) and shared by both
the sync and async top-level clients.

There is no audit transport here — ``client.audit`` owns its own.
"""

from __future__ import annotations

from dataclasses import dataclass

from smplkit._config import ResolvedConfig, ResolvedClientConfig, _service_url
from smplkit._generated.app.client import AuthenticatedClient as _AppAuthClient
from smplkit._generated.config.client import AuthenticatedClient as _ConfigAuthClient
from smplkit._generated.flags.client import AuthenticatedClient as _FlagsAuthClient
from smplkit._generated.jobs.client import AuthenticatedClient as _JobsAuthClient
from smplkit._generated.logging.client import AuthenticatedClient as _LoggingAuthClient


def _to_transport_config(cfg: ResolvedConfig, extra_headers: dict[str, str] | None = None) -> ResolvedClientConfig:
    """Project the runtime :class:`ResolvedConfig` down to the transport subset.

    SmplClient's resolved config is a superset of what the transports need;
    this drops the runtime-only fields (environment, service, telemetry).
    """
    return ResolvedClientConfig(
        api_key=cfg.api_key,
        base_domain=cfg.base_domain,
        scheme=cfg.scheme,
        debug=cfg.debug,
        extra_headers=extra_headers,
    )


@dataclass
class _ServiceTransports:
    """The per-service authenticated transports built for a top-level client.

    Construction is side-effect-free: each transport connects lazily on its
    first call. ``app_url`` is carried alongside so the account settings
    client (which uses httpx directly) and the WebSocket can reach the app
    service. ``close`` / ``aclose`` tear down the underlying httpx pools.
    """

    app_url: str
    api_key: str
    app_http: _AppAuthClient
    config_http: _ConfigAuthClient
    flags_http: _FlagsAuthClient
    logging_http: _LoggingAuthClient
    jobs_http: _JobsAuthClient

    def _all(self) -> tuple[object, ...]:
        return (
            self.app_http,
            self.config_http,
            self.flags_http,
            self.logging_http,
            self.jobs_http,
        )

    def close(self) -> None:
        """Close the per-service sync transport pools."""
        for http in self._all():
            client = http._client  # type: ignore[attr-defined]
            if client is not None:
                client.close()
                http._client = None  # type: ignore[attr-defined]

    async def aclose(self) -> None:
        """Close the per-service async transport pools."""
        for http in self._all():
            ac = http._async_client  # type: ignore[attr-defined]
            if ac is not None:
                await ac.aclose()
                http._async_client = None  # type: ignore[attr-defined]


def build_service_transports(cfg: ResolvedClientConfig) -> _ServiceTransports:
    """Build the five per-service transports from a resolved transport config.

    Side-effect-free — the underlying httpx clients are created lazily on the
    first request. Smpl Jobs is JSON:API, so its transport carries the
    ``application/vnd.api+json`` Accept header.
    """
    config_url = _service_url(cfg.scheme, "config", cfg.base_domain)
    app_url = _service_url(cfg.scheme, "app", cfg.base_domain)
    flags_url = _service_url(cfg.scheme, "flags", cfg.base_domain)
    logging_url = _service_url(cfg.scheme, "logging", cfg.base_domain)
    jobs_url = _service_url(cfg.scheme, "jobs", cfg.base_domain)

    extra = {**(cfg.extra_headers or {})}
    return _ServiceTransports(
        app_url=app_url,
        api_key=cfg.api_key,
        app_http=_AppAuthClient(base_url=app_url, token=cfg.api_key, headers=extra),
        config_http=_ConfigAuthClient(base_url=config_url, token=cfg.api_key, headers=extra),
        flags_http=_FlagsAuthClient(base_url=flags_url, token=cfg.api_key, headers=extra),
        logging_http=_LoggingAuthClient(base_url=logging_url, token=cfg.api_key, headers=extra),
        jobs_http=_JobsAuthClient(
            base_url=jobs_url,
            token=cfg.api_key,
            headers={**extra, "Accept": "application/vnd.api+json"},
        ),
    )
