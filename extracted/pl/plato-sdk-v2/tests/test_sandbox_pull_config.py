from __future__ import annotations

from textwrap import dedent
from types import SimpleNamespace

import yaml
from rich.console import Console

import plato.v2.sync.sandbox as sandbox_module
from plato.v2.sync.sandbox import SandboxClient

PLATO_CONFIG_YAML = dedent(
    """
    service: seafile
    datasets:
      base:
        compute:
          cpus: 1
          memory: 2048
          disk: 10240
          app_port: 80
          plato_messaging_port: 7000
        metadata:
          name: Seafile
          description: Cloud storage
          flows_path: base/flows.yml
          variables:
            - name: username
              value: me@example.com
            - name: password
              value: asecret
        listeners:
          db:
            type: db
            db_type: mysql
            db_host: 127.0.0.1
            db_port: 3306
            db_user: seafile
            db_password: seafile_pass
            db_database: seahub_db
            audit_ignore_tables:
              - django_session
              - django_migrations
    """
).strip()

FLOWS_API_RESPONSE = [
    {
        "name": "login",
        "steps": [
            {"type": "fill", "selector": "input[name='login']", "value": "me@example.com"},
            {"type": "fill", "selector": "input[name='password']", "value": "asecret"},
            {"type": "click", "selector": "button[type='submit']"},
            {
                "type": "verify",
                "verify_type": "element_visible",
                "selector": ".side-nav-con",
                "timeout": 15000,
            },
        ],
    }
]


def test_pull_config_downloads_plato_config(tmp_path, monkeypatch) -> None:
    """pull_config writes plato-config.yml from the artifact API."""
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=PLATO_CONFIG_YAML),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: None,  # no flows
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        result = client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    assert result["plato_config_written"] is True
    assert result["flows_written"] is False

    config_path = tmp_path / "plato-config.yml"
    assert config_path.exists()
    parsed = yaml.safe_load(config_path.read_text())
    assert parsed["service"] == "seafile"
    assert parsed["datasets"]["base"]["metadata"]["flows_path"] == "base/flows.yml"


def test_pull_config_downloads_flows_to_correct_path(tmp_path, monkeypatch) -> None:
    """pull_config writes flows.yml to the path specified in plato-config metadata."""
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=PLATO_CONFIG_YAML),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: FLOWS_API_RESPONSE,
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    flows_path = tmp_path / "base" / "flows.yml"
    assert flows_path.exists()

    parsed = yaml.safe_load(flows_path.read_text())
    assert "flows" in parsed
    assert len(parsed["flows"]) == 1
    assert parsed["flows"][0]["name"] == "login"
    assert len(parsed["flows"][0]["steps"]) == 4
    assert parsed["flows"][0]["steps"][0]["type"] == "fill"


def test_pull_config_creates_parent_dirs(tmp_path, monkeypatch) -> None:
    """pull_config creates parent directories for flows_path (e.g., base/)."""
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=PLATO_CONFIG_YAML),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: FLOWS_API_RESPONSE,
    )

    # Ensure base/ doesn't exist yet
    assert not (tmp_path / "base").exists()

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    assert (tmp_path / "base").is_dir()
    assert (tmp_path / "base" / "flows.yml").exists()


def test_pull_config_defaults_flows_path_when_no_config(tmp_path, monkeypatch) -> None:
    """When plato-config has no flows_path, flows default to base/flows.yml."""
    config_no_flows_path = dedent(
        """
        service: myapp
        datasets:
          base:
            compute:
              cpus: 1
              memory: 1024
              disk: 5120
            metadata:
              name: MyApp
              description: Test app
        """
    ).strip()

    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=config_no_flows_path),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: FLOWS_API_RESPONSE,
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    # Should default to base/flows.yml
    assert (tmp_path / "base" / "flows.yml").exists()


def test_pull_config_handles_dict_response_with_flows_key(tmp_path, monkeypatch) -> None:
    """API might return {"flows": [...]} instead of a bare list."""
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=PLATO_CONFIG_YAML),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: {"flows": FLOWS_API_RESPONSE},
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    parsed = yaml.safe_load((tmp_path / "base" / "flows.yml").read_text())
    assert parsed["flows"][0]["name"] == "login"


def test_pull_config_passes_artifact_id_to_api(tmp_path, monkeypatch) -> None:
    """Verify the correct artifact_id is passed to both API calls."""
    captured: dict[str, list] = {"config_calls": [], "flows_calls": []}

    def fake_get_config(**kwargs):
        captured["config_calls"].append(kwargs.get("artifact_id"))
        return SimpleNamespace(plato_config=PLATO_CONFIG_YAML)

    def fake_get_flows(**kwargs):
        captured["flows_calls"].append(kwargs.get("artifact_id"))
        return FLOWS_API_RESPONSE

    monkeypatch.setattr(sandbox_module.simulator_get_plato_config, "sync", fake_get_config)
    monkeypatch.setattr(sandbox_module.simulator_get_env_flows, "sync", fake_get_flows)

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-specific-id", dataset="base")
    finally:
        client.close()

    assert captured["config_calls"] == ["art-specific-id"]
    assert captured["flows_calls"] == ["art-specific-id"]


def test_pull_config_survives_config_api_failure(tmp_path, monkeypatch) -> None:
    """If fetching plato-config fails, it should not crash and should still try flows."""
    captured: dict[str, bool] = {"flows_called": False}

    def fail_config(**kwargs):
        raise RuntimeError("API unreachable")

    def fake_get_flows(**kwargs):
        captured["flows_called"] = True
        return FLOWS_API_RESPONSE

    monkeypatch.setattr(sandbox_module.simulator_get_plato_config, "sync", fail_config)
    monkeypatch.setattr(sandbox_module.simulator_get_env_flows, "sync", fake_get_flows)

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    assert not (tmp_path / "plato-config.yml").exists()
    assert captured["flows_called"]
    # Falls back to default path since no config to read flows_path from
    assert (tmp_path / "base" / "flows.yml").exists()


def test_pull_config_survives_flows_api_failure(tmp_path, monkeypatch) -> None:
    """If fetching flows fails, plato-config should still be written."""
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=PLATO_CONFIG_YAML),
    )

    def fail_flows(**kwargs):
        raise RuntimeError("Flows API error")

    monkeypatch.setattr(sandbox_module.simulator_get_env_flows, "sync", fail_flows)

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    assert (tmp_path / "plato-config.yml").exists()
    assert not (tmp_path / "base" / "flows.yml").exists()


def test_pull_config_roundtrips_with_run_flow_parser(tmp_path, monkeypatch) -> None:
    """Verify the written flows.yml can be parsed by run_flow's local reader."""
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=PLATO_CONFIG_YAML),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: FLOWS_API_RESPONSE,
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    # Replicate what run_flow does to parse local flows
    flows_file = tmp_path / "base" / "flows.yml"
    flow_dict = yaml.safe_load(flows_file.read_text())
    matching = [fl for fl in flow_dict.get("flows", []) if fl.get("name") == "login"]

    assert len(matching) == 1
    flow = matching[0]
    assert flow["name"] == "login"
    assert flow["steps"][0]["type"] == "fill"
    assert flow["steps"][0]["value"] == "me@example.com"
    assert flow["steps"][2]["type"] == "click"
    assert flow["steps"][3]["type"] == "verify"
    assert flow["steps"][3]["verify_type"] == "element_visible"


def test_pull_config_custom_flows_path(tmp_path, monkeypatch) -> None:
    """Flows are written to the custom flows_path from plato-config."""
    config_custom_path = dedent(
        """
        service: myapp
        datasets:
          base:
            compute:
              cpus: 1
              memory: 1024
              disk: 5120
            metadata:
              name: MyApp
              flows_path: flows/flows.yaml
        """
    ).strip()

    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=config_custom_path),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: FLOWS_API_RESPONSE,
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    assert (tmp_path / "flows" / "flows.yaml").exists()
    assert not (tmp_path / "base" / "flows.yml").exists()


def test_pull_config_rejects_path_traversal(tmp_path, monkeypatch) -> None:
    """flows_path with .. or absolute path falls back to base/flows.yml."""
    config_traversal = dedent(
        """
        service: evil
        datasets:
          base:
            compute:
              cpus: 1
              memory: 1024
              disk: 5120
            metadata:
              name: Evil
              flows_path: ../../../etc/flows.yml
        """
    ).strip()

    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=config_traversal),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: FLOWS_API_RESPONSE,
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        result = client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    # Should fall back to base/flows.yml, NOT write to ../../../etc/
    assert result["flows_written"] is True
    assert (tmp_path / "base" / "flows.yml").exists()
    # Ensure nothing was written outside working_dir
    assert not (tmp_path.parent / "etc").exists()


def test_pull_config_rejects_absolute_flows_path(tmp_path, monkeypatch) -> None:
    """Absolute flows_path falls back to base/flows.yml."""
    config_abs = dedent(
        """
        service: evil
        datasets:
          base:
            compute:
              cpus: 1
              memory: 1024
              disk: 5120
            metadata:
              name: Evil
              flows_path: /tmp/evil/flows.yml
        """
    ).strip()

    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: SimpleNamespace(plato_config=config_abs),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: FLOWS_API_RESPONSE,
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        result = client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    assert result["flows_written"] is True
    assert (tmp_path / "base" / "flows.yml").exists()


def test_pull_config_returns_both_false_on_total_failure(tmp_path, monkeypatch) -> None:
    """When both API calls fail, result reflects nothing was written."""
    monkeypatch.setattr(
        sandbox_module.simulator_get_plato_config,
        "sync",
        lambda **kwargs: (_ for _ in ()).throw(RuntimeError("fail")),
    )
    monkeypatch.setattr(
        sandbox_module.simulator_get_env_flows,
        "sync",
        lambda **kwargs: (_ for _ in ()).throw(RuntimeError("fail")),
    )

    client = SandboxClient(working_dir=tmp_path, api_key="test-key", console=Console(quiet=True))
    try:
        result = client.pull_config(artifact_id="art-123", dataset="base")
    finally:
        client.close()

    assert result["plato_config_written"] is False
    assert result["flows_written"] is False
