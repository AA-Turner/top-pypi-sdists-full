"""Tests for _prefetch_certs."""

import os
from unittest.mock import patch

import pytest

from agentic_devtools.cli.setup import commands


@pytest.fixture(autouse=True)
def mock_setup_network():
    """Override the conftest autouse mock to test _prefetch_certs directly."""
    yield


@pytest.fixture(autouse=True)
def isolate_os_environ():
    """Keep test environment variables isolated per test case."""
    original_env = os.environ.copy()
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original_env)


class TestPrefetchCerts:
    """Tests for _prefetch_certs."""

    def test_prints_cached_message_when_bundles_exist(self, monkeypatch, capsys, tmp_path):
        """Prints cached messages when ensure_ca_bundle returns paths."""
        pem_path = str(tmp_path / "cert.pem")
        monkeypatch.delenv("NPM_CONFIG_USERCONFIG", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    mock_npmrc.__str__.return_value = str(tmp_path / ".agdt" / "npmrc")
                    commands._prefetch_certs(npm_enabled=True)

        out = capsys.readouterr().out
        assert "CA bundle cached for api.github.com" in out
        assert "CA bundle cached for github.com" in out
        assert "CA bundle cached for dev.azure.com" in out
        assert "CA bundle cached for release-assets.githubusercontent.com" in out
        assert "CA bundle cached for registry.npmjs.org" in out

    def test_includes_jira_hostname(self, capsys, tmp_path):
        """Fetches cert for the Jira hostname resolved from get_jira_base_url."""
        pem_path = str(tmp_path / "cert.pem")

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path) as mock_ensure:
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch("agentic_devtools.cli.setup.commands.Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    # Patch at definition point; all imports see the mock
                    with patch(
                        "agentic_devtools.cli.jira.config.get_jira_base_url", return_value="https://jira.example.com"
                    ):
                        commands._prefetch_certs(npm_enabled=True)

        called_hostnames = [c.args[0] for c in mock_ensure.call_args_list]
        assert "jira.example.com" in called_hostnames

    def test_strips_port_from_jira_hostname(self, capsys, tmp_path):
        """Strips port from Jira URL so ensure_ca_bundle receives a clean hostname."""
        pem_path = str(tmp_path / "cert.pem")

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path) as mock_ensure:
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch("agentic_devtools.cli.setup.commands.Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    with patch(
                        "agentic_devtools.cli.jira.config.get_jira_base_url",
                        return_value="https://jira.example.com:8443",
                    ):
                        commands._prefetch_certs(npm_enabled=True)

        called_hostnames = [c.args[0] for c in mock_ensure.call_args_list]
        # Must be the bare hostname without port
        assert "jira.example.com" in called_hostnames
        assert "jira.example.com:8443" not in called_hostnames

    def test_handles_schemeless_jira_hostname(self, capsys, tmp_path):
        """Extracts hostname from scheme-less Jira URL like 'jira.example.com'."""
        pem_path = str(tmp_path / "cert.pem")

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path) as mock_ensure:
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch("agentic_devtools.cli.setup.commands.Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    with patch(
                        "agentic_devtools.cli.jira.config.get_jira_base_url",
                        return_value="jira.example.com",
                    ):
                        commands._prefetch_certs(npm_enabled=True)

        called_hostnames = [c.args[0] for c in mock_ensure.call_args_list]
        assert "jira.example.com" in called_hostnames

    def test_handles_schemeless_jira_hostname_with_port(self, capsys, tmp_path):
        """Extracts hostname from scheme-less Jira URL like 'jira.example.com:8443'."""
        pem_path = str(tmp_path / "cert.pem")

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path) as mock_ensure:
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch("agentic_devtools.cli.setup.commands.Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    with patch(
                        "agentic_devtools.cli.jira.config.get_jira_base_url",
                        return_value="jira.example.com:8443",
                    ):
                        commands._prefetch_certs(npm_enabled=True)

        called_hostnames = [c.args[0] for c in mock_ensure.call_args_list]
        assert "jira.example.com" in called_hostnames
        assert "jira.example.com:8443" not in called_hostnames

    def test_populates_selected_hosts_with_effective_host_set(self, tmp_path):
        """The optional host-output list mirrors the phase's selected hosts."""
        pem_path = str(tmp_path / "cert.pem")
        selected_hosts: list[str] = []

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch("agentic_devtools.cli.setup.commands.Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    with patch(
                        "agentic_devtools.cli.jira.config.get_jira_base_url",
                        return_value="https://jira.example.com",
                    ):
                        commands._prefetch_certs(npm_enabled=True, selected_hosts_out=selected_hosts)

        assert selected_hosts == [
            "api.github.com",
            "github.com",
            "dev.azure.com",
            "release-assets.githubusercontent.com",
            "jira.example.com",
            "registry.npmjs.org",
        ]

    def test_prints_warning_message_when_bundles_missing(self, capsys):
        """Prints warning messages when ensure_ca_bundle returns None."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                commands._prefetch_certs(npm_enabled=True)

        out = capsys.readouterr().out
        assert "Could not cache CA bundle for api.github.com" in out
        assert "Could not cache CA bundle for github.com" in out
        assert "Could not cache CA bundle for dev.azure.com" in out
        assert "Could not cache CA bundle for release-assets.githubusercontent.com" in out
        assert "Could not cache CA bundle for registry.npmjs.org" in out

    def test_prints_warning_for_dynamic_jira_host_when_cert_fails(self, capsys):
        """Prints warning when _ensure_ca_bundle returns None for a dynamic Jira host."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch(
                    "agentic_devtools.cli.jira.config.get_jira_base_url",
                    return_value="https://jira.example.com",
                ):
                    commands._prefetch_certs(npm_enabled=True)

        out = capsys.readouterr().out
        assert "Could not cache CA bundle for jira.example.com" in out

    def test_writes_npmrc_when_npm_cert_cached(self, monkeypatch, capsys, tmp_path):
        """Writes ~/.agdt/npmrc with cafile when npm registry cert is cached."""
        pem_path = str(tmp_path / "registry.npmjs.org.pem")
        npmrc_path = tmp_path / "npmrc"
        monkeypatch.delenv("NPM_CONFIG_USERCONFIG", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    mock_npmrc.__str__.return_value = str(tmp_path / ".agdt" / "npmrc")
                    mock_npmrc.write_text = npmrc_path.write_text
                    commands._prefetch_certs(npm_enabled=True)

        content = npmrc_path.read_text(encoding="utf-8")
        assert f"cafile={pem_path}" in content

    def test_prints_unified_bundle_hint_when_built(self, monkeypatch, capsys, tmp_path):
        """Prints unified bundle success messages when the bundle is built."""
        pem_path = str(tmp_path / "some-host.pem")
        unified_path = tmp_path / "unified-ca-bundle.pem"
        unified_path.write_text("# placeholder\n", encoding="utf-8")
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
        monkeypatch.delenv("NODE_EXTRA_CA_CERTS", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified_path):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    commands._prefetch_certs(npm_enabled=True)

        out = capsys.readouterr().out
        assert "Unified CA bundle written to ~/.agdt/certs/unified-ca-bundle.pem" in out
        assert "REQUESTS_CA_BUNDLE set for this session" in out
        assert "NODE_EXTRA_CA_CERTS set for this session" in out

    def test_handles_exception_from_get_jira_base_url(self, capsys):
        """Does not raise when get_jira_base_url() raises; prints progress to stdout."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch(
                    "agentic_devtools.cli.jira.config.get_jira_base_url",
                    side_effect=Exception("config error"),
                ):
                    # Should not raise
                    commands._prefetch_certs(npm_enabled=True)

        out = capsys.readouterr().out
        assert "Fetching CA certificates" in out

    def test_no_pip_hint_when_no_unified_bundle(self, capsys, tmp_path):
        """Does not print REQUESTS_CA_BUNDLE hint when unified bundle could not be built."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                commands._prefetch_certs(npm_enabled=True)

        out = capsys.readouterr().out
        assert "REQUESTS_CA_BUNDLE" not in out

    def test_sets_requests_ca_bundle_when_unified_built(self, monkeypatch, capsys, tmp_path):
        """Sets REQUESTS_CA_BUNDLE env var when unified bundle is built and not already set."""
        pem_path = str(tmp_path / "cert.pem")
        unified_path = tmp_path / "unified-ca-bundle.pem"
        unified_path.write_text("-----BEGIN CERTIFICATE-----\ntest\n-----END CERTIFICATE-----\n", encoding="utf-8")
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified_path):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    commands._prefetch_certs(npm_enabled=True)

        assert os.environ.get("REQUESTS_CA_BUNDLE") == str(unified_path)
        out = capsys.readouterr().out
        assert "REQUESTS_CA_BUNDLE set for this session" in out

    def test_does_not_overwrite_existing_requests_ca_bundle(self, monkeypatch, capsys, tmp_path):
        """Does not overwrite REQUESTS_CA_BUNDLE if already set by user."""
        pem_path = str(tmp_path / "cert.pem")
        unified_path = tmp_path / "unified-ca-bundle.pem"
        unified_path.write_text("-----BEGIN CERTIFICATE-----\ntest\n-----END CERTIFICATE-----\n", encoding="utf-8")
        user_bundle = str(tmp_path / "user-ca.pem")
        monkeypatch.setenv("REQUESTS_CA_BUNDLE", user_bundle)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified_path):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    commands._prefetch_certs(npm_enabled=True)

        assert os.environ.get("REQUESTS_CA_BUNDLE") == user_bundle
        out = capsys.readouterr().out
        assert "REQUESTS_CA_BUNDLE set for this session" not in out

    def test_returns_unified_path_when_built(self, tmp_path):
        """Returns the unified bundle path when _build_unified_ca_bundle succeeds."""
        pem_path = str(tmp_path / "cert.pem")
        unified_path = tmp_path / "unified-ca-bundle.pem"
        unified_path.write_text("cert\n", encoding="utf-8")

        with patch.dict(os.environ, {}, clear=False):
            with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
                with patch.object(commands, "_build_unified_ca_bundle", return_value=unified_path):
                    with patch.object(commands, "Path") as mock_path_cls:
                        mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                        mock_npmrc.parent = tmp_path
                        result = commands._prefetch_certs(npm_enabled=True)

        assert result[0] == unified_path
        assert result[1] is not None  # npmrc path returned when npm_enabled

    def test_returns_none_when_no_unified_bundle(self):
        """Returns None when _build_unified_ca_bundle returns None."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                result = commands._prefetch_certs(npm_enabled=True)

        assert result[0] is None
        assert result[1] is None  # no npmrc without a CA bundle

    def test_sets_npm_config_userconfig_when_npmrc_written(self, monkeypatch, capsys, tmp_path):
        """Sets NPM_CONFIG_USERCONFIG env var when npmrc is written and not already set."""
        pem_path = str(tmp_path / "cert.pem")
        monkeypatch.delenv("NPM_CONFIG_USERCONFIG", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    commands._prefetch_certs(npm_enabled=True)

        assert os.environ.get("NPM_CONFIG_USERCONFIG") is not None
        out = capsys.readouterr().out
        assert "NPM_CONFIG_USERCONFIG set for this session" in out

    def test_does_not_overwrite_existing_npm_config_userconfig(self, monkeypatch, capsys, tmp_path):
        """Does not overwrite NPM_CONFIG_USERCONFIG if already set by user."""
        pem_path = str(tmp_path / "cert.pem")
        user_npmrc = str(tmp_path / "user-npmrc")
        monkeypatch.setenv("NPM_CONFIG_USERCONFIG", user_npmrc)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    commands._prefetch_certs(npm_enabled=True)

        assert os.environ.get("NPM_CONFIG_USERCONFIG") == user_npmrc
        out = capsys.readouterr().out
        assert "NPM_CONFIG_USERCONFIG set for this session" not in out

    def test_sets_node_extra_ca_certs_when_unified_built(self, monkeypatch, capsys, tmp_path):
        """Sets NODE_EXTRA_CA_CERTS env var when unified bundle is built and not already set."""
        pem_path = str(tmp_path / "cert.pem")
        unified_path = tmp_path / "unified-ca-bundle.pem"
        unified_path.write_text("cert\n", encoding="utf-8")
        monkeypatch.delenv("NODE_EXTRA_CA_CERTS", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified_path):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    commands._prefetch_certs(npm_enabled=True)

        assert os.environ.get("NODE_EXTRA_CA_CERTS") == str(unified_path)
        out = capsys.readouterr().out
        assert "NODE_EXTRA_CA_CERTS set for this session" in out

    def test_does_not_overwrite_existing_node_extra_ca_certs(self, monkeypatch, capsys, tmp_path):
        """Does not overwrite NODE_EXTRA_CA_CERTS if already set by user."""
        pem_path = str(tmp_path / "cert.pem")
        unified_path = tmp_path / "unified-ca-bundle.pem"
        unified_path.write_text("cert\n", encoding="utf-8")
        user_certs = str(tmp_path / "user-certs.pem")
        monkeypatch.setenv("NODE_EXTRA_CA_CERTS", user_certs)

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified_path):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    commands._prefetch_certs(npm_enabled=True)

        assert os.environ.get("NODE_EXTRA_CA_CERTS") == user_certs
        out = capsys.readouterr().out
        assert "NODE_EXTRA_CA_CERTS set for this session" not in out

    def test_skips_jira_when_hostname_is_empty(self, capsys, tmp_path):
        """Does not add Jira host when URL resolves to empty hostname."""
        pem_path = str(tmp_path / "cert.pem")

        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path) as mock_ensure:
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                with patch("agentic_devtools.cli.setup.commands.Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    # An empty string URL produces a None hostname from urlparse
                    with patch(
                        "agentic_devtools.cli.jira.config.get_jira_base_url",
                        return_value="",
                    ):
                        commands._prefetch_certs(npm_enabled=True)

        # Only the fixed setup hosts + npm should be called, not any Jira host
        called_hostnames = [c.args[0] for c in mock_ensure.call_args_list]
        expected = set(commands._SETUP_HOSTS) | {"registry.npmjs.org"}
        assert set(called_hostnames) == expected

    def test_npm_disabled_skips_registry_fetch(self, capsys):
        """When npm_enabled=False, does not fetch registry.npmjs.org cert."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None) as mock_ensure:
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                commands._prefetch_certs(npm_enabled=False)

        called_hostnames = [c.args[0] for c in mock_ensure.call_args_list]
        assert "registry.npmjs.org" not in called_hostnames

    def test_npm_disabled_does_not_write_npmrc(self, capsys, tmp_path):
        """When npm_enabled=False, does not write ~/.agdt/npmrc."""
        with patch("pathlib.Path.home", return_value=tmp_path):
            with patch.object(commands, "_ensure_ca_bundle", return_value=None):
                with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                    commands._prefetch_certs(npm_enabled=False)
        npmrc_path = tmp_path / ".agdt" / "npmrc"
        assert not npmrc_path.exists()

    def test_npm_disabled_prints_skip_message(self, capsys):
        """When npm_enabled=False, prints skip warning."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                commands._prefetch_certs(npm_enabled=False)
        out = capsys.readouterr().out
        assert "⚠ npm certificate work skipped" in out

    def test_npm_disabled_does_not_set_node_extra_ca_certs(self, monkeypatch, capsys, tmp_path):
        """When npm_enabled=False, does not set NODE_EXTRA_CA_CERTS even with unified bundle."""
        unified = tmp_path / "unified.pem"
        unified.write_text("cert\n", encoding="utf-8")
        monkeypatch.delenv("NODE_EXTRA_CA_CERTS", raising=False)
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified):
                commands._prefetch_certs(npm_enabled=False)

        assert os.environ.get("NODE_EXTRA_CA_CERTS") is None

    def test_npm_disabled_still_sets_requests_ca_bundle(self, monkeypatch, capsys, tmp_path):
        """When npm_enabled=False, still sets REQUESTS_CA_BUNDLE for non-npm HTTPS."""
        unified = tmp_path / "unified.pem"
        unified.write_text("cert\n", encoding="utf-8")
        monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
        monkeypatch.delenv("NODE_EXTRA_CA_CERTS", raising=False)

        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified):
                commands._prefetch_certs(npm_enabled=False)

        assert os.environ.get("REQUESTS_CA_BUNDLE") == str(unified)

    def test_npm_disabled_still_fetches_other_hosts(self, capsys):
        """When npm_enabled=False, still fetches certs for all non-npm setup hosts."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None) as mock_ensure:
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                commands._prefetch_certs(npm_enabled=False)

        called_hostnames = [c.args[0] for c in mock_ensure.call_args_list]
        for hostname in commands._SETUP_HOSTS:
            assert hostname in called_hostnames

    def test_npm_enabled_with_fetch_failure_still_writes_npmrc(self, monkeypatch, capsys, tmp_path):
        """When npm_enabled=True but npm cert fails, still writes npmrc with unified bundle."""
        unified = tmp_path / "unified.pem"
        unified.write_text("cert\n", encoding="utf-8")

        def mock_ensure(hostname):
            if hostname == "registry.npmjs.org":
                return None  # npm cert fetch fails
            return str(tmp_path / f"{hostname}.pem")

        monkeypatch.delenv("NPM_CONFIG_USERCONFIG", raising=False)
        with patch.object(commands, "_ensure_ca_bundle", side_effect=mock_ensure):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    mock_npmrc.__str__.return_value = str(tmp_path / ".agdt" / "npmrc")
                    _, npmrc_result = commands._prefetch_certs(npm_enabled=True)

        # npmrc should still be written because unified bundle exists
        mock_npmrc.write_text.assert_called_once()
        written_content = mock_npmrc.write_text.call_args[0][0]
        assert f"cafile={unified}" in written_content

    def test_npm_disabled_returns_none_for_npmrc(self, capsys):
        """When npm_enabled=False, returns None for the npmrc_path."""
        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                _, npmrc_result = commands._prefetch_certs(npm_enabled=False)
        assert npmrc_result is None

    def test_npm_disabled_preserves_existing_npmrc(self, monkeypatch, tmp_path, capsys):
        """When npm_enabled=False, pre-existing ~/.agdt/npmrc is not touched."""
        # Create a pre-existing npmrc under the patched home directory
        npmrc_dir = tmp_path / ".agdt"
        npmrc_dir.mkdir(parents=True)
        npmrc_file = npmrc_dir / "npmrc"
        npmrc_file.write_text("cafile=/old/path.pem\n", encoding="utf-8")

        with patch("pathlib.Path.home", return_value=tmp_path):
            with patch.object(commands, "_ensure_ca_bundle", return_value=None):
                with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                    commands._prefetch_certs(npm_enabled=False)

        # The file should still contain the old content (unchanged)
        assert npmrc_file.read_text(encoding="utf-8") == "cafile=/old/path.pem\n"

    def test_npm_disabled_preserves_existing_npm_config_env(self, monkeypatch, capsys):
        """When npm_enabled=False, pre-existing NPM_CONFIG_USERCONFIG env var is not touched."""
        monkeypatch.setenv("NPM_CONFIG_USERCONFIG", "/existing/npmrc")

        with patch.object(commands, "_ensure_ca_bundle", return_value=None):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=None):
                commands._prefetch_certs(npm_enabled=False)

        assert os.environ["NPM_CONFIG_USERCONFIG"] == "/existing/npmrc"

    def test_npm_enabled_refreshes_existing_npmrc(self, monkeypatch, capsys, tmp_path):
        """When npm_enabled=True, existing npmrc is overwritten with new cafile value."""
        pem_path = str(tmp_path / "registry.npmjs.org.pem")
        unified = tmp_path / "unified.pem"
        unified.write_text("cert\n", encoding="utf-8")

        monkeypatch.delenv("NPM_CONFIG_USERCONFIG", raising=False)
        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    mock_npmrc.__str__.return_value = str(tmp_path / ".agdt" / "npmrc")
                    commands._prefetch_certs(npm_enabled=True)

        mock_npmrc.write_text.assert_called_once()
        written_content = mock_npmrc.write_text.call_args[0][0]
        assert f"cafile={unified}" in written_content

    def test_npm_enabled_write_failure_is_best_effort(self, monkeypatch, capsys, tmp_path):
        """When npmrc write fails, continues without setting NPM_CONFIG_USERCONFIG."""
        pem_path = str(tmp_path / "registry.npmjs.org.pem")
        unified = tmp_path / "unified.pem"
        unified.write_text("cert\n", encoding="utf-8")

        monkeypatch.delenv("NPM_CONFIG_USERCONFIG", raising=False)
        with patch.object(commands, "_ensure_ca_bundle", return_value=pem_path):
            with patch.object(commands, "_build_unified_ca_bundle", return_value=unified):
                with patch.object(commands, "Path") as mock_path_cls:
                    mock_npmrc = mock_path_cls.home.return_value.__truediv__.return_value.__truediv__.return_value
                    mock_npmrc.parent = tmp_path
                    mock_npmrc.__str__.return_value = str(tmp_path / ".agdt" / "npmrc")
                    mock_npmrc.write_text.side_effect = OSError("not writable")
                    _, npmrc_result = commands._prefetch_certs(npm_enabled=True)

        assert npmrc_result is None
        assert os.environ.get("NPM_CONFIG_USERCONFIG") is None
        assert "Could not write npm CA config" in capsys.readouterr().err
