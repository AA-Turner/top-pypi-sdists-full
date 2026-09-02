"""Tests for OpenClaw at-rest detection and runtime signatures."""

import os
from unittest import mock

from runlayer_cli.scan import agent_scan
from runlayer_cli.scan.agents.install import INSTALL_PROBES, InstallProbe
from runlayer_cli.scan.agents.openclaw_detector import (
    DEFAULT_GATEWAY_PORT,
    OpenClawDetection,
    build_openclaw_agent,
    detect_openclaw,
    openclaw_gateway_ports,
    openclaw_launchd_labels,
    openclaw_systemd_units,
)
from runlayer_cli.scan.processes.classify import ClassifierContext, classify_processes
from runlayer_cli.scan.processes.models import ProcessCandidate


def _openclaw_probes(detection: OpenClawDetection) -> tuple[InstallProbe, ...]:
    return (
        InstallProbe(
            name="openclaw",
            detect=lambda: detection,
            build_agent=build_openclaw_agent,
            runtime=INSTALL_PROBES[0].runtime,
        ),
    )


class TestOpenClawDetection:
    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector._find_macos_app_bundle",
        return_value=None,
    )
    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector._locate_cli", return_value=None
    )
    @mock.patch("runlayer_cli.scan.agents.openclaw_detector._get_state_path")
    def test_not_installed(self, mock_state, mock_cli, mock_app, tmp_path):
        mock_state.return_value = tmp_path / ".openclaw-missing"

        result = detect_openclaw()

        assert result.detected is False
        assert result.summary == "not-installed"

    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector._find_macos_app_bundle",
        return_value=None,
    )
    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector.get_cli_version",
        return_value="2026.1.15",
    )
    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector._locate_cli",
        return_value="/usr/local/bin/openclaw",
    )
    @mock.patch("runlayer_cli.scan.agents.openclaw_detector._get_state_path")
    def test_cli_artifact_is_installed(
        self, mock_state, mock_cli, mock_version, mock_app, tmp_path
    ):
        mock_state.return_value = tmp_path / ".openclaw-missing"

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed"
        assert result.cli_path == "/usr/local/bin/openclaw"
        assert result.cli_version == "2026.1.15"

    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector._find_macos_app_bundle",
        return_value=None,
    )
    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector._locate_cli", return_value=None
    )
    @mock.patch("runlayer_cli.scan.agents.openclaw_detector._get_state_path")
    def test_state_and_config_artifacts(self, mock_state, mock_cli, mock_app, tmp_path):
        state_dir = tmp_path / ".openclaw"
        state_dir.mkdir()
        config = state_dir / "openclaw.json"
        config.write_text('{"port": 19999}')
        mock_state.return_value = state_dir

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed"
        assert result.state_dir == str(state_dir)
        assert result.config_path == str(config)


class TestOpenClawRuntimeSignatures:
    @mock.patch("runlayer_cli.scan.agents.openclaw_detector._get_state_path")
    def test_custom_gateway_port(self, mock_state, tmp_path):
        state_dir = tmp_path / ".openclaw"
        state_dir.mkdir()
        (state_dir / "openclaw.json").write_text('{"port": 19999}')
        mock_state.return_value = state_dir

        assert openclaw_gateway_ports() == (19999,)

    @mock.patch("runlayer_cli.scan.agents.openclaw_detector._get_state_path")
    def test_default_gateway_port(self, mock_state, tmp_path):
        mock_state.return_value = tmp_path / ".openclaw-missing"

        assert openclaw_gateway_ports() == (DEFAULT_GATEWAY_PORT,)

    @mock.patch.dict(os.environ, {"OPENCLAW_PROFILE": "dev"})
    def test_profile_service_names(self):
        assert openclaw_launchd_labels() == ("bot.molt.gateway.dev",)
        assert openclaw_systemd_units() == ("openclaw-gateway-dev.service",)

    @mock.patch.dict(os.environ, {"OPENCLAW_PROFILE": "customer-project"})
    def test_profile_name_is_not_serialized(self):
        installed = build_openclaw_agent(
            OpenClawDetection(
                detected=True,
                summary="installed",
                state_dir="/Users/dev/.openclaw-customer-project",
                config_path="/Users/dev/.openclaw-customer-project/openclaw.json",
            )
        )
        runtime = classify_processes(
            [ProcessCandidate(pid=42, argv=["openclaw", "serve"])],
            ClassifierContext(),
            usernames=["dev"],
        )[0]

        assert installed is not None
        serialized = repr(installed.to_api_payload(usernames=["dev"])) + repr(
            runtime.to_dict()
        )
        assert "customer-project" not in serialized

    def test_registry_runtime_signature(self):
        signature = INSTALL_PROBES[0].runtime

        assert signature.framework_id == "openclaw"
        assert "openclaw" in signature.argv_markers
        assert signature.docker_markers == ("openclaw",)

    @mock.patch(
        "runlayer_cli.scan.agents.openclaw_detector._get_state_path",
        return_value="/Users/dev/.openclaw",
    )
    def test_runtime_identity_matches_at_rest_identity(self, mock_state):
        installed = build_openclaw_agent(
            OpenClawDetection(
                detected=True,
                summary="installed",
                cli_path="/usr/local/bin/openclaw",
            )
        )
        runtime = classify_processes(
            [
                ProcessCandidate(
                    pid=-1,
                    discovery_source="runtime_probe",
                    agent_runtime_signals={"openclaw": ["service:launchd"]},
                )
            ],
            ClassifierContext(),
            usernames=["dev"],
        )[0]

        assert installed is not None
        assert runtime.agent_fingerprint == installed.agent_fingerprint
        assert runtime.agent_root_path == "runtime:openclaw"


class TestBuildOpenClawAgent:
    def test_returns_none_when_not_detected(self):
        assert build_openclaw_agent(OpenClawDetection(detected=False)) is None

    def test_agent_contains_only_at_rest_evidence(self):
        detection = OpenClawDetection(
            detected=True,
            summary="installed",
            cli_path="/usr/local/bin/openclaw",
            state_dir="/Users/dev/.openclaw",
        )

        agent = build_openclaw_agent(detection)

        assert agent is not None
        assert agent.framework_id == "openclaw"
        assert agent.detection_method == "install"
        assert {e.kind for e in agent.evidence} == {"install_artifact"}
        assert agent.agent_fingerprint and len(agent.agent_fingerprint) == 64

    def test_agent_fingerprint_excludes_ephemeral_paths(self):
        a = build_openclaw_agent(
            OpenClawDetection(
                detected=True, summary="installed", cli_path="/a/openclaw"
            )
        )
        b = build_openclaw_agent(
            OpenClawDetection(
                detected=True,
                summary="installed",
                cli_path="/totally/different/openclaw",
            )
        )

        assert a is not None and b is not None
        assert a.agent_fingerprint == b.agent_fingerprint

    def test_agent_fingerprint_is_stable_as_artifacts_appear(self):
        cli_only = build_openclaw_agent(
            OpenClawDetection(
                detected=True,
                summary="installed",
                cli_path="/usr/local/bin/openclaw",
            )
        )
        fully_initialized = build_openclaw_agent(
            OpenClawDetection(
                detected=True,
                summary="installed",
                cli_path="/usr/local/bin/openclaw",
                state_dir="/Users/dev/.openclaw",
                config_path="/Users/dev/.openclaw/openclaw.json",
            )
        )

        assert cli_only is not None and fully_initialized is not None
        assert cli_only.agent_fingerprint == fully_initialized.agent_fingerprint


class TestScanServiceIntegration:
    @mock.patch.object(
        agent_scan,
        "INSTALL_PROBES",
        _openclaw_probes(
            OpenClawDetection(
                detected=True,
                summary="installed",
                cli_path="/usr/local/bin/openclaw",
            )
        ),
    )
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.orchestrator.get_clients_with_project_configs",
        return_value=[],
    )
    def test_openclaw_agent_when_detected(self, mock_project_clients, mock_clients):
        from runlayer_cli.scan.service import scan_all_clients

        result = scan_all_clients(scan_projects=False)

        openclaw_agents = [a for a in result.agents if a.framework_id == "openclaw"]
        assert len(openclaw_agents) == 1
        assert openclaw_agents[0].detection_method == "install"
        assert [c for c in result.configurations if c.client == "openclaw"] == []

    @mock.patch.object(
        agent_scan,
        "INSTALL_PROBES",
        _openclaw_probes(OpenClawDetection(detected=False)),
    )
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.orchestrator.get_clients_with_project_configs",
        return_value=[],
    )
    def test_openclaw_excluded_when_not_detected(
        self, mock_project_clients, mock_clients
    ):
        from runlayer_cli.scan.service import scan_all_clients

        result = scan_all_clients(scan_projects=False)

        assert [a for a in result.agents if a.framework_id == "openclaw"] == []

    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.orchestrator.get_clients_with_project_configs",
        return_value=[],
    )
    def test_detect_agents_false_gates_openclaw(
        self, mock_project_clients, mock_clients
    ):
        from runlayer_cli.scan.service import scan_all_clients

        detect_spy = mock.Mock(
            return_value=OpenClawDetection(
                detected=True,
                summary="installed",
                cli_path="/usr/local/bin/openclaw",
            )
        )
        probes = (
            InstallProbe(
                name="openclaw",
                detect=detect_spy,
                build_agent=build_openclaw_agent,
                runtime=INSTALL_PROBES[0].runtime,
            ),
        )

        with mock.patch.object(agent_scan, "INSTALL_PROBES", probes):
            result = scan_all_clients(scan_projects=False, detect_agents=False)

        detect_spy.assert_not_called()
        assert result.agents == []
