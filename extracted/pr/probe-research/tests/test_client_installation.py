"""Explicit setup-time client installation registration."""

from __future__ import annotations

from probe.cli import client_installation
from probe.cli.capabilities import Capabilities
from probe.sdk import errors
from probe.sdk.client import Client
from probe.sdk.config import Settings


class _Nameable:
    """Naming is a best-effort step every register() makes, so the fakes inherit
    it and each test states only what it is actually about. `named` records the
    hostname that was sent, for the tests that care."""

    named: dict | None = None

    def name_client_installation(self, **kwargs):
        self.named = kwargs
        return {"installation_id": "i", "name": "Probe Research CLI · box", "renamed": True}


def test_snapshot_reports_installation_not_runtime_health() -> None:
    installed_but_logged_out = Capabilities(
        tracking_plugin_installed=True,
        logged_in_as=None,
        auto_update_enabled=True,
    )

    assert client_installation.snapshot(installed_but_logged_out) == {
        "schema_version": 2,
        "auto_update": "on",
        "tracking": "installed",
        "capture": "absent",
    }


def test_snapshot_marks_an_unfinished_run_unknown_not_absent() -> None:
    """An install that did not finish must not look like one that finished with
    tracking off. Both leave the plugin uninstalled; only the second is a
    decision, and the dashboard advances onboarding on the difference."""
    nothing_applied = Capabilities(
        tracking_plugin_installed=False,
        logged_in_as=None,
        auto_update_enabled=True,
    )

    assert client_installation.snapshot(nothing_applied, complete=False) == {
        "schema_version": 2,
        "auto_update": "on",
        "tracking": "unknown",
        "capture": "unknown",
    }
    # The deliberate no-tracking install still reports a settled `absent`.
    assert client_installation.snapshot(nothing_applied) == {
        "schema_version": 2,
        "auto_update": "on",
        "tracking": "absent",
        "capture": "absent",
    }


def test_register_still_runs_on_an_unfinished_install(monkeypatch) -> None:
    """The unfinished path must keep REGISTERING -- that write is what adopts a
    legacy MCP credential -- and only change what it reports."""
    bodies: list[dict] = []

    class FakeClient(_Nameable):
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return None

        def register_client_capabilities(self, **body):
            bodies.append(body)
            return {"installation_id": "install-1"}

    monkeypatch.setattr(client_installation, "Client", FakeClient)
    settings = Settings(base_url="https://api.test", token="probe_pat_x", mcp_token=None)

    assert client_installation.register(
        Capabilities(tracking_plugin_installed=False, auto_update_enabled=True),
        settings=settings,
        complete=False,
    ) == []
    assert bodies == [{
        "schema_version": 2,
        "auto_update": "on",
        "tracking": "unknown",
        "capture": "unknown",
    }]


def test_register_links_api_and_mcp_tokens_to_one_installation(monkeypatch) -> None:
    calls: list[tuple] = []

    class FakeClient(_Nameable):
        def __init__(self, **kwargs):
            self.token = kwargs["token"]

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return None

        def register_client_capabilities(self, **body):
            calls.append(("register", self.token, body))
            return {"installation_id": "install-1"}

        def create_credential_attachment_grant(self, installation_id):
            calls.append(("grant", self.token, installation_id))
            return {"grant": "join-secret"}

        def attach_current_credential(self, installation_id, *, grant):
            calls.append(("attach", self.token, installation_id, grant))
            return {}

    monkeypatch.setattr(client_installation, "Client", FakeClient)
    settings = Settings(
        base_url="https://api.test",
        token="api-secret",
        mcp_token="mcp-secret",
    )

    warnings = client_installation.register(
        Capabilities(tracking_plugin_installed=True),
        settings=settings,
    )

    assert warnings == []
    assert calls == [
        (
            "register",
            "api-secret",
            {
        "schema_version": 2,
        "auto_update": "off",
        "tracking": "installed",
        "capture": "absent",
    },
        ),
        ("grant", "api-secret", "install-1"),
        ("attach", "mcp-secret", "install-1", "join-secret"),
    ]


def test_register_is_quiet_for_an_older_backend(monkeypatch) -> None:
    class OldBackendClient(_Nameable):
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return None

        def register_client_capabilities(self, **body):
            raise errors.NotFoundError("route not found", status=404)

    monkeypatch.setattr(client_installation, "Client", OldBackendClient)
    assert (
        client_installation.register(
            Capabilities(),
            settings=Settings(base_url="https://old.test", token="api-secret"),
        )
        == []
    )


def test_register_without_an_api_token_never_opens_a_client(monkeypatch) -> None:
    def fail(**kwargs):
        raise AssertionError("Client must not be constructed")

    monkeypatch.setattr(client_installation, "Client", fail)
    assert (
        client_installation.register(
            Capabilities(),
            settings=Settings(base_url="https://api.test"),
        )
        == []
    )


def test_register_without_mcp_token_stops_after_capability_snapshot(monkeypatch) -> None:
    calls = []

    class ApiOnlyClient(_Nameable):
        def __init__(self, **kwargs):
            calls.append(("open", kwargs["token"]))

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return None

        def register_client_capabilities(self, **body):
            calls.append(("register", body))
            return {"installation_id": "install-1"}

    monkeypatch.setattr(client_installation, "Client", ApiOnlyClient)

    warnings = client_installation.register(
        Capabilities(),
        settings=Settings(base_url="https://api.test", token="api-secret"),
    )

    assert warnings == []
    assert calls == [
        ("open", "api-secret"),
        (
            "register",
            {
        "schema_version": 2,
        "auto_update": "off",
        "tracking": "absent",
        "capture": "absent",
    },
        ),
    ]


def test_register_reports_attachment_grant_failure(monkeypatch) -> None:
    class GrantFailureClient(_Nameable):
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return None

        def register_client_capabilities(self, **body):
            return {"installation_id": "install-1"}

        def create_credential_attachment_grant(self, installation_id):
            raise errors.ScopeError("write scope required", status=403)

    monkeypatch.setattr(client_installation, "Client", GrantFailureClient)

    warnings = client_installation.register(
        Capabilities(),
        settings=Settings(
            base_url="https://api.test",
            token="api-secret",
            mcp_token="mcp-secret",
        ),
    )

    assert warnings == [
        "! could not authorize the MCP credential association: write scope required"
    ]


def test_register_reports_mcp_attachment_failure(monkeypatch) -> None:
    class AttachmentFailureClient(_Nameable):
        def __init__(self, **kwargs):
            self.token = kwargs["token"]

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return None

        def register_client_capabilities(self, **body):
            return {"installation_id": "install-1"}

        def create_credential_attachment_grant(self, installation_id):
            return {"grant": "join-secret"}

        def attach_current_credential(self, installation_id, *, grant):
            raise errors.ConflictError("already linked")

    monkeypatch.setattr(client_installation, "Client", AttachmentFailureClient)

    warnings = client_installation.register(
        Capabilities(),
        settings=Settings(
            base_url="https://api.test",
            token="api-secret",
            mcp_token="mcp-secret",
        ),
    )

    assert warnings == [
        "! could not associate the MCP credential with this installation: already linked"
    ]


def test_sdk_methods_send_only_the_allowlisted_contract() -> None:
    class RecordingTransport:
        def __init__(self):
            self.calls = []

        def put(self, path, body):
            self.calls.append(("PUT", path, body))
            return {"installation_id": "install-1"}

        def post(self, path, body=None):
            self.calls.append(("POST", path, body))
            return {"grant": "join-secret"}

        def get(self, path):
            self.calls.append(("GET", path, None))
            return {"installations": []}

    transport = RecordingTransport()
    client = Client(
        settings=Settings(base_url="https://api.test", token="secret"),
        transport=transport,
    )

    client.register_client_capabilities(
        auto_update="on",
        tracking="installed",
        capture="absent",
    )
    client.create_credential_attachment_grant("install-1")
    client.attach_current_credential("install-1", grant="join-secret")
    client.list_client_installations()

    assert transport.calls == [
        (
            "PUT",
            "/v1/client-installations/current/capabilities",
            {
                "schema_version": 2,
                "auto_update": "on",
                "tracking": "installed",
                "capture": "absent",
            },
        ),
        (
            "POST",
            "/v1/client-installations/install-1/credential-attachment-grants",
            None,
        ),
        (
            "PUT",
            "/v1/client-installations/install-1/credentials/current",
            {"grant": "join-secret"},
        ),
        ("GET", "/v1/client-installations", None),
    ]


def test_register_names_the_installation_after_this_machine(monkeypatch) -> None:
    """The CLI is the ONLY party that knows the machine's hostname. A legacy
    installation is named after whatever PAT it adopted, so without this the
    dashboard shows a credential's name where a computer's name belongs."""
    sent: list[dict] = []

    class FakeClient(_Nameable):
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def register_client_capabilities(self, **kwargs):
            return {"installation_id": "install-1"}

        def name_client_installation(self, **kwargs):
            sent.append(kwargs)
            return {"installation_id": "install-1", "name": "x", "renamed": True}

    monkeypatch.setattr(client_installation, "Client", FakeClient)
    monkeypatch.setattr(client_installation, "hostname", lambda: "prbe-devbox")

    warnings = client_installation.register(
        Capabilities(tracking_plugin_installed=True, logged_in_as=None, auto_update_enabled=True),
        settings=Settings(base_url="https://x", token="api-secret", mcp_token=None),
    )

    assert sent == [{"hostname": "prbe-devbox"}]
    assert warnings == []


def test_a_backend_that_cannot_name_still_completes_the_install(monkeypatch) -> None:
    """An older or self-hosted backend has no naming route. That is not a failed
    install, so it must be silent; a route that exists but ERRORS is worth a
    word, but still must not abort the run."""

    class OldBackend(_Nameable):
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def register_client_capabilities(self, **kwargs):
            return {"installation_id": "install-1"}

        def name_client_installation(self, **kwargs):
            raise errors.NotFoundError("no such route")

    class BrokenNaming(OldBackend):
        def name_client_installation(self, **kwargs):
            raise errors.RosError("boom")

    settings = Settings(base_url="https://x", token="api-secret", mcp_token=None)
    caps = Capabilities(
        tracking_plugin_installed=True, logged_in_as=None, auto_update_enabled=True
    )

    monkeypatch.setattr(client_installation, "Client", OldBackend)
    assert client_installation.register(caps, settings=settings) == []

    monkeypatch.setattr(client_installation, "Client", BrokenNaming)
    warnings = client_installation.register(caps, settings=settings)
    assert warnings == ["! could not record this machine's name: boom"]


def test_snapshot_reports_capture_as_what_actually_runs() -> None:
    """`capture_on`, not `capture_plugin_installed`.

    An installed plugin that is killswitched, or has no credential, ships
    nothing. Reporting that as `installed` would overstate what is running on
    the machine -- and this is the field the consent story rests on, so
    overstating it is the one direction that must never happen.
    """
    from probe.cli.capabilities import TokenSource

    killswitched = Capabilities(
        tracking_plugin_installed=True,
        auto_update_enabled=True,
        capture_plugin_installed=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
        capture_killswitched=True,
    )
    assert client_installation.snapshot(killswitched)["capture"] == "absent"

    no_credential = Capabilities(
        tracking_plugin_installed=True,
        auto_update_enabled=True,
        capture_plugin_installed=True,
        capture_token_sources=(),
    )
    assert client_installation.snapshot(no_credential)["capture"] == "absent"

    running = Capabilities(
        tracking_plugin_installed=True,
        auto_update_enabled=True,
        capture_plugin_installed=True,
        capture_token_sources=(TokenSource.PAIRED_FILE,),
    )
    assert client_installation.snapshot(running)["capture"] == "installed"


def test_an_unfinished_run_says_unknown_for_capture_too() -> None:
    """The whole point of `complete=False` is that nothing on the machine is a
    decision yet. Reporting capture as `absent` there would look like someone
    chose to turn session tracking off."""
    caps = Capabilities(
        tracking_plugin_installed=True,
        auto_update_enabled=True,
        capture_plugin_installed=True,
        capture_killswitched=False,
    )
    partial = client_installation.snapshot(caps, complete=False)
    assert partial["tracking"] == "unknown"
    assert partial["capture"] == "unknown"
