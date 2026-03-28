from __future__ import annotations

from textwrap import dedent
from types import SimpleNamespace

from rich.console import Console

import plato.v2.sync.sandbox as sandbox_module
from plato._generated.models import (
    DatabaseMutationListenerConfig,
    ProxyMutationListenerConfig,
    VMManagementRequest,
)
from plato.v2.sync.sandbox import SandboxClient

PLATO_CONFIG_WITH_MODERN_LISTENERS = dedent(
    """
    service: trudesk
    datasets:
      base:
        compute:
          cpus: 1
          memory: 2048
          disk: 10240
          app_port: 8080
          plato_messaging_port: 7000
        metadata:
          name: Trudesk
          description: Sandbox test config
        services: {}
        listeners:
          db:
            type: db
            db_type: postgresql
            db_host: localhost
            db_port: 5432
            db_user: postgres
            db_password: secret
            db_database: trudesk
            db_schema: audit
            audit_ignore_tables:
              - migrations
              - users:
                  - last_login
          proxy:
            type: proxy
            sim_name: trudesk
            dataset: base
            proxy_host: proxy.internal
            proxy_port: 9000
            passthrough_all_ood_requests: false
            replay_sessions:
              - id: replay-1
                start_path: /
    """
).strip()


def test_start_worker_preserves_modern_listener_fields_from_local_config(tmp_path, monkeypatch) -> None:
    (tmp_path / "plato-config.yml").write_text(PLATO_CONFIG_WITH_MODERN_LISTENERS)

    captured: dict[str, object] = {}

    def fake_start_worker_sync(*, client, public_id, body, x_api_key):
        captured["public_id"] = public_id
        captured["body"] = body
        return SimpleNamespace(status="in_progress", correlation_id="corr-1")

    monkeypatch.setattr(sandbox_module.start_worker, "sync", fake_start_worker_sync)

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.start_worker(job_id="job-123", simulator="trudesk", dataset="base", wait_timeout=0)
    finally:
        client.close()

    request = captured.get("body")
    assert isinstance(request, VMManagementRequest)
    assert captured["public_id"] == "job-123"

    listeners = request.plato_dataset_config.listeners
    assert listeners is not None

    db_listener = listeners["db"]
    assert isinstance(db_listener, DatabaseMutationListenerConfig)
    assert db_listener.db_schema == "audit"
    assert db_listener.audit_ignore_tables == ["migrations", {"users": ["last_login"]}]

    proxy_listener = listeners["proxy"]
    assert isinstance(proxy_listener, ProxyMutationListenerConfig)
    assert proxy_listener.proxy_host == "proxy.internal"
    assert proxy_listener.proxy_port == 9000
    assert proxy_listener.passthrough_all_ood_requests is False
    assert proxy_listener.replay_sessions == [{"id": "replay-1", "start_path": "/"}]


def test_start_worker_preserves_modern_listener_fields_from_api_config(tmp_path, monkeypatch) -> None:
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        sandbox_module.env_get_simulator_by_name,
        "sync",
        lambda **kwargs: SimpleNamespace(versionTag="stable"),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_simulator_versions,
        "sync",
        lambda **kwargs: SimpleNamespace(
            versions=[
                SimpleNamespace(
                    dataset="base",
                    tags=["stable"],
                    created_at="2026-03-13T00:00:00Z",
                    artifact_id="artifact-123",
                )
            ]
        ),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=PLATO_CONFIG_WITH_MODERN_LISTENERS),
    )

    def fake_start_worker_sync(*, client, public_id, body, x_api_key):
        captured["public_id"] = public_id
        captured["body"] = body
        return SimpleNamespace(status="in_progress", correlation_id="corr-2")

    monkeypatch.setattr(sandbox_module.start_worker, "sync", fake_start_worker_sync)

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.start_worker(
            job_id="job-456",
            simulator="trudesk",
            dataset="base",
            wait_timeout=0,
            use_api=True,
        )
    finally:
        client.close()

    request = captured.get("body")
    assert isinstance(request, VMManagementRequest)
    assert captured["public_id"] == "job-456"

    listeners = request.plato_dataset_config.listeners
    assert listeners is not None

    db_listener = listeners["db"]
    assert isinstance(db_listener, DatabaseMutationListenerConfig)
    assert db_listener.db_schema == "audit"
    assert db_listener.audit_ignore_tables == ["migrations", {"users": ["last_login"]}]

    proxy_listener = listeners["proxy"]
    assert isinstance(proxy_listener, ProxyMutationListenerConfig)
    assert proxy_listener.proxy_host == "proxy.internal"
    assert proxy_listener.proxy_port == 9000
