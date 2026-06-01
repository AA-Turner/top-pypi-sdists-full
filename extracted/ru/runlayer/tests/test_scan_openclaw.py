"""Tests for OpenClaw detection."""

import os
from unittest import mock


from runlayer_cli.scan.openclaw_detector import (
    OpenClawDetection,
    build_openclaw_config,
    detect_openclaw,
)


class TestOpenClawDetection:
    """Unit tests for detect_openclaw."""

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._scan_docker", return_value=([], [])
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=False)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_not_installed(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Returns not-installed when no artifacts found."""
        mock_state.return_value = tmp_path / ".openclaw-missing"

        result = detect_openclaw()

        assert result.detected is False
        assert result.summary == "not-installed"
        assert result.cli_path is None

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._scan_docker", return_value=([], [])
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=False)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._get_cli_version", return_value="2026.1.15"
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._locate_cli",
        return_value="/usr/local/bin/openclaw",
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_installed_not_running(
        self,
        mock_state,
        mock_cli,
        mock_ver,
        mock_app,
        mock_svc,
        mock_port,
        mock_docker,
        tmp_path,
    ):
        """CLI present but gateway not running."""
        mock_state.return_value = tmp_path / ".openclaw-missing"

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-not-running"
        assert result.cli_path == "/usr/local/bin/openclaw"
        assert result.cli_version == "2026.1.15"

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._scan_docker", return_value=([], [])
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=True)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service",
        return_value="gui/501/bot.molt.gateway",
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle",
        return_value="/Applications/OpenClaw.app",
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._get_cli_version", return_value="2026.1.15"
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._locate_cli",
        return_value="/usr/local/bin/openclaw",
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_installed_and_running(
        self,
        mock_state,
        mock_cli,
        mock_ver,
        mock_app,
        mock_svc,
        mock_port,
        mock_docker,
        tmp_path,
    ):
        """Full installation with gateway running."""
        state_dir = tmp_path / ".openclaw"
        state_dir.mkdir()
        (state_dir / "openclaw.json").write_text('{"port": 18789}')
        mock_state.return_value = state_dir

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-and-running"
        assert result.cli_path == "/usr/local/bin/openclaw"
        assert result.app_bundle == "/Applications/OpenClaw.app"
        assert result.gateway_service == "gui/501/bot.molt.gateway"
        assert result.gateway_listening is True
        assert result.gateway_port == 18789
        assert result.state_dir == str(state_dir)
        assert result.config_path == str(state_dir / "openclaw.json")

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._scan_docker", return_value=([], [])
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=False)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_state_dir_only(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Only state directory present — still counts as installed."""
        state_dir = tmp_path / ".openclaw"
        state_dir.mkdir()
        mock_state.return_value = state_dir

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-not-running"
        assert result.state_dir == str(state_dir)

    @mock.patch("runlayer_cli.scan.openclaw_detector._scan_docker")
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=False)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_docker_image_detected(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Docker image counts as installed."""
        mock_state.return_value = tmp_path / ".openclaw-missing"
        mock_docker.return_value = (["openclaw/gateway:latest"], [])

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-not-running"
        assert result.docker_images == ["openclaw/gateway:latest"]

    @mock.patch("runlayer_cli.scan.openclaw_detector._scan_docker")
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=False)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_docker_container_running(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Running Docker container counts as running."""
        mock_state.return_value = tmp_path / ".openclaw-missing"
        mock_docker.return_value = (
            ["openclaw/gateway:latest"],
            ["openclaw-gw (openclaw/gateway:latest)"],
        )

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-and-running"

    @mock.patch("runlayer_cli.scan.openclaw_detector._scan_docker")
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=False)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_docker_container_without_matching_image(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Running container with no matching image still counts as installed+running."""
        mock_state.return_value = tmp_path / ".openclaw-missing"
        mock_docker.return_value = (
            [],
            ["openclaw-gw (custom-registry.io/my-image:v1)"],
        )

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-and-running"

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._scan_docker", return_value=([], [])
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=False)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service",
        return_value="gui/501/bot.molt.gateway",
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_gateway_service_only(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Gateway service alone counts as installed+running."""
        mock_state.return_value = tmp_path / ".openclaw-missing"

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-and-running"
        assert result.gateway_service == "gui/501/bot.molt.gateway"

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._scan_docker", return_value=([], [])
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=True)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_gateway_port_listening_only(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Gateway port listening alone counts as installed+running."""
        mock_state.return_value = tmp_path / ".openclaw-missing"

        result = detect_openclaw()

        assert result.detected is True
        assert result.summary == "installed-and-running"
        assert result.gateway_listening is True

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._scan_docker", return_value=([], [])
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._probe_port", return_value=True)
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._check_gateway_service", return_value=None
    )
    @mock.patch(
        "runlayer_cli.scan.openclaw_detector._find_macos_app_bundle", return_value=None
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector._locate_cli", return_value=None)
    @mock.patch("runlayer_cli.scan.openclaw_detector._get_state_path")
    def test_custom_port_from_config(
        self, mock_state, mock_cli, mock_app, mock_svc, mock_port, mock_docker, tmp_path
    ):
        """Reads custom port from openclaw.json config."""
        state_dir = tmp_path / ".openclaw"
        state_dir.mkdir()
        (state_dir / "openclaw.json").write_text('{"port": 19999}')
        mock_state.return_value = state_dir

        result = detect_openclaw()

        assert result.gateway_port == 19999
        # _probe_port is called with the custom port
        mock_port.assert_called_with(19999)


class TestCheckGatewayServiceLabel:
    """Unit tests for launchd/systemd label construction in _check_gateway_service."""

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector.platform.system", return_value="Darwin"
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector.os.getuid", return_value=501)
    @mock.patch("runlayer_cli.scan.openclaw_detector.subprocess.run")
    @mock.patch.dict(os.environ, {"OPENCLAW_PROFILE": "dev"})
    def test_macos_label_includes_gateway_with_profile(
        self, mock_run, mock_uid, mock_sys
    ):
        """macOS launchd label must include 'gateway' when OPENCLAW_PROFILE is set."""
        from runlayer_cli.scan.openclaw_detector import _check_gateway_service

        mock_run.return_value = mock.Mock(returncode=0)

        result = _check_gateway_service()

        # The label should be bot.molt.gateway.dev, NOT bot.molt.dev
        mock_run.assert_called_once()
        call_args = mock_run.call_args[0][0]
        assert call_args == ["launchctl", "print", "gui/501/bot.molt.gateway.dev"]
        assert result == "gui/501/bot.molt.gateway.dev"

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector.platform.system", return_value="Darwin"
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector.os.getuid", return_value=501)
    @mock.patch("runlayer_cli.scan.openclaw_detector.subprocess.run")
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_macos_label_default_without_profile(self, mock_run, mock_uid, mock_sys):
        """macOS launchd label defaults to bot.molt.gateway with no profile."""
        from runlayer_cli.scan.openclaw_detector import _check_gateway_service

        mock_run.return_value = mock.Mock(returncode=0)

        result = _check_gateway_service()

        call_args = mock_run.call_args[0][0]
        assert call_args == ["launchctl", "print", "gui/501/bot.molt.gateway"]
        assert result == "gui/501/bot.molt.gateway"

    @mock.patch(
        "runlayer_cli.scan.openclaw_detector.platform.system", return_value="Linux"
    )
    @mock.patch("runlayer_cli.scan.openclaw_detector.subprocess.run")
    @mock.patch.dict(os.environ, {"OPENCLAW_PROFILE": "dev"})
    def test_linux_unit_includes_gateway_with_profile(self, mock_run, mock_sys):
        """Linux systemd unit keeps 'gateway' when OPENCLAW_PROFILE is set."""
        from runlayer_cli.scan.openclaw_detector import _check_gateway_service

        mock_run.return_value = mock.Mock(returncode=0)

        result = _check_gateway_service()

        call_args = mock_run.call_args[0][0]
        assert call_args == [
            "systemctl",
            "--user",
            "is-active",
            "openclaw-gateway-dev.service",
        ]


class TestBuildOpenClawConfig:
    """Tests for build_openclaw_config."""

    def test_returns_none_when_not_detected(self):
        """Returns None if OpenClaw not detected."""
        detection = OpenClawDetection(detected=False)
        assert build_openclaw_config(detection) is None

    def test_gateway_server_entry(self):
        """Creates gateway server entry when port is listening."""
        detection = OpenClawDetection(
            detected=True,
            summary="installed-and-running",
            gateway_listening=True,
            gateway_port=18789,
        )

        config = build_openclaw_config(detection)

        assert config is not None
        assert config.client == "openclaw"
        assert config.config_scope == "global"
        gw = next(s for s in config.servers if s.name == "openclaw-gateway")
        assert gw.type == "http"
        assert gw.url == "http://localhost:18789"
        assert gw.config_hash != ""

    def test_cli_server_entry(self):
        """Creates CLI server entry when binary found."""
        detection = OpenClawDetection(
            detected=True,
            summary="installed-not-running",
            cli_path="/usr/local/bin/openclaw",
            cli_version="2026.1.15",
        )

        config = build_openclaw_config(detection)

        assert config is not None
        assert config.client_version == "2026.1.15"
        cli = next(s for s in config.servers if s.name == "openclaw-cli")
        assert cli.type == "stdio"
        assert cli.command == "/usr/local/bin/openclaw"

    def test_app_bundle_entry(self):
        """Creates app bundle entry on macOS."""
        detection = OpenClawDetection(
            detected=True,
            summary="installed-not-running",
            app_bundle="/Applications/OpenClaw.app",
        )

        config = build_openclaw_config(detection)

        assert config is not None
        app = next(s for s in config.servers if s.name == "openclaw-app")
        assert app.command == "/Applications/OpenClaw.app"

    def test_docker_container_entries(self):
        """Creates entries for running Docker containers."""
        detection = OpenClawDetection(
            detected=True,
            summary="installed-and-running",
            docker_containers=["openclaw-gw (openclaw/gateway:latest)"],
        )

        config = build_openclaw_config(detection)

        assert config is not None
        docker_servers = [s for s in config.servers if "docker" in s.name]
        assert len(docker_servers) == 1
        assert docker_servers[0].command == "docker"

    def test_placeholder_when_no_specific_artifacts(self):
        """Creates placeholder entry when detected but no specific server artifacts."""
        detection = OpenClawDetection(
            detected=True,
            summary="installed-not-running",
            state_dir="/Users/dev/.openclaw",
        )

        config = build_openclaw_config(detection)

        assert config is not None
        assert len(config.servers) == 1
        assert config.servers[0].name == "openclaw"
        assert config.servers[0].config_hash != ""

    def test_multiple_artifacts(self):
        """Creates entries for all detected artifacts."""
        detection = OpenClawDetection(
            detected=True,
            summary="installed-and-running",
            cli_path="/usr/local/bin/openclaw",
            cli_version="2026.1.15",
            app_bundle="/Applications/OpenClaw.app",
            gateway_listening=True,
            gateway_port=18789,
        )

        config = build_openclaw_config(detection)

        assert config is not None
        names = {s.name for s in config.servers}
        assert "openclaw-gateway" in names
        assert "openclaw-cli" in names
        assert "openclaw-app" in names

    def test_all_servers_have_config_hash(self):
        """All generated servers have non-empty config hashes."""
        detection = OpenClawDetection(
            detected=True,
            summary="installed-and-running",
            cli_path="/usr/local/bin/openclaw",
            gateway_listening=True,
            gateway_port=18789,
        )

        config = build_openclaw_config(detection)

        assert config is not None
        for server in config.servers:
            assert server.config_hash != ""
            assert len(server.config_hash) == 64


class TestScanServiceIntegration:
    """Test OpenClaw detection integrates with scan_all_clients."""

    @mock.patch("runlayer_cli.scan.service.detect_openclaw")
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.service.get_clients_with_project_configs", return_value=[]
    )
    def test_openclaw_included_when_detected(
        self, mock_project_clients, mock_clients, mock_detect
    ):
        """scan_all_clients includes OpenClaw config when detected."""
        from runlayer_cli.scan.service import scan_all_clients

        mock_detect.return_value = OpenClawDetection(
            detected=True,
            summary="installed-and-running",
            cli_path="/usr/local/bin/openclaw",
            cli_version="2026.1.15",
            gateway_listening=True,
            gateway_port=18789,
        )

        result = scan_all_clients(scan_projects=False)

        openclaw_configs = [c for c in result.configurations if c.client == "openclaw"]
        assert len(openclaw_configs) == 1
        assert openclaw_configs[0].client_version == "2026.1.15"
        assert len(openclaw_configs[0].servers) > 0

    @mock.patch("runlayer_cli.scan.service.detect_openclaw")
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.service.get_clients_with_project_configs", return_value=[]
    )
    def test_openclaw_excluded_when_not_detected(
        self, mock_project_clients, mock_clients, mock_detect
    ):
        """scan_all_clients excludes OpenClaw when not detected."""
        from runlayer_cli.scan.service import scan_all_clients

        mock_detect.return_value = OpenClawDetection(detected=False)

        result = scan_all_clients(scan_projects=False)

        openclaw_configs = [c for c in result.configurations if c.client == "openclaw"]
        assert len(openclaw_configs) == 0

    @mock.patch("runlayer_cli.scan.service.detect_openclaw")
    @mock.patch("runlayer_cli.scan.service.get_all_clients", return_value=[])
    @mock.patch(
        "runlayer_cli.scan.service.get_clients_with_project_configs", return_value=[]
    )
    def test_openclaw_in_api_payload(
        self, mock_project_clients, mock_clients, mock_detect
    ):
        """OpenClaw entries appear correctly in the API payload."""
        from runlayer_cli.scan.service import scan_all_clients

        mock_detect.return_value = OpenClawDetection(
            detected=True,
            summary="installed-not-running",
            cli_path="/usr/local/bin/openclaw",
        )

        result = scan_all_clients(scan_projects=False)
        payload = result.to_api_payload()

        oc_configs = [c for c in payload["configurations"] if c["client"] == "openclaw"]
        assert len(oc_configs) == 1
        assert oc_configs[0]["servers"][0]["name"] == "openclaw-cli"
        assert oc_configs[0]["servers"][0]["command"] == "/usr/local/bin/openclaw"
