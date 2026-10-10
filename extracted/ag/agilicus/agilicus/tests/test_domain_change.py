"""Tests for the organisation domain-change report (agilicus.domain_change)."""

import json

import pytest
from click.testing import CliRunner

from agilicus.agilicus_api import ApiException
from agilicus.domain_change import domain_change as domain_change_module
from agilicus.domain_change import domain_change_main


class FakeApiClient:
    """Captures ``call_api`` invocations and returns a canned payload."""

    def __init__(self, result=None, error=None):
        self.calls = []
        self.result = result if result is not None else {"org_id": "o"}
        self.error = error

    def call_api(self, path, method, **kwargs):
        self.calls.append({"path": path, "method": method, **kwargs})
        if self.error is not None:
            raise self.error
        return self.result


class FakeOrgApi:
    def __init__(self, api_client):
        self.api_client = api_client


class FakeApiHelper:
    def __init__(self, api_client):
        self.org_api = FakeOrgApi(api_client)


def _patch_client(monkeypatch, api_client):
    monkeypatch.setattr(
        domain_change_module.context,
        "get_apiclient",
        lambda ctx, *args, **kwargs: FakeApiHelper(api_client),
    )


def test_get_domain_change_uses_raw_get(monkeypatch):
    api_client = FakeApiClient(result={"counts": {"issuer": 1}})
    _patch_client(monkeypatch, api_client)

    report = domain_change_module.get_domain_change(object(), "org-1", "new")

    assert report == {"counts": {"issuer": 1}}
    (call,) = api_client.calls
    assert call["path"] == "/v1/orgs/{org_id}/domain_change"
    assert call["method"] == "GET"
    assert call["path_params"] == {"org_id": "org-1"}
    assert call["query_params"] == [("new_subdomain", "new")]
    assert call["body"] is None
    assert call["auth_settings"] == ["token-valid"]


def test_create_domain_change_posts_the_body(monkeypatch):
    api_client = FakeApiClient()
    _patch_client(monkeypatch, api_client)

    domain_change_module.create_domain_change(
        object(), "org-1", "new", issuer_url="https://auth.new", dry_run=False
    )

    (call,) = api_client.calls
    assert call["method"] == "POST"
    assert call["path_params"] == {"org_id": "org-1"}
    assert call["body"] == {
        "subdomain": "new",
        "issuer_url": "https://auth.new",
        "dry_run": False,
    }
    assert call["header_params"]["Content-Type"] == "application/json"


def test_plan_domain_change_dry_run_uses_get(monkeypatch):
    api_client = FakeApiClient()
    _patch_client(monkeypatch, api_client)

    domain_change_module.plan_domain_change(object(), "org-1", "new")

    (call,) = api_client.calls
    assert call["method"] == "GET"


def test_plan_domain_change_with_issuer_posts_dry_run(monkeypatch):
    api_client = FakeApiClient()
    _patch_client(monkeypatch, api_client)

    domain_change_module.plan_domain_change(
        object(), "org-1", "new", issuer_url="https://auth.new"
    )

    (call,) = api_client.calls
    assert call["method"] == "POST"
    assert call["body"]["dry_run"] is True
    assert call["body"]["issuer_url"] == "https://auth.new"


def test_plan_domain_change_no_dry_run_posts_execute(monkeypatch):
    api_client = FakeApiClient()
    _patch_client(monkeypatch, api_client)

    domain_change_module.plan_domain_change(object(), "org-1", "new", dry_run=False)

    (call,) = api_client.calls
    assert call["method"] == "POST"
    assert call["body"]["dry_run"] is False


def test_plan_domain_change_requires_a_subdomain():
    with pytest.raises(ValueError, match="subdomain"):
        domain_change_module.plan_domain_change(object(), "org-1", "")


def test_domain_change_maps_api_exception(monkeypatch):
    api_client = FakeApiClient(error=ApiException(status=404, reason="Not Found"))
    _patch_client(monkeypatch, api_client)

    with pytest.raises(domain_change_module.DomainChangeError):
        domain_change_module.get_domain_change(object(), "org-1", "new")


def test_ordered_counts_uses_the_shared_vocabulary():
    report = {"counts": {"connector": 4, "issuer_client": 115, "custom": 1}}
    ordered = domain_change_module.ordered_counts(report)
    assert ordered[:3] == [
        ("issuer_client", 115),
        ("connector", 4),
        ("custom", 1),
    ]


def test_cli_domain_change_json_prints_report_body(monkeypatch):
    report = {
        "schema_version": 1,
        "org_id": "o",
        "counts": {"issuer_client": 115},
        "changes": [],
        "warnings": [],
    }
    monkeypatch.setattr(
        domain_change_main.domain_change,
        "plan_domain_change",
        lambda ctx, **kwargs: report,
    )
    runner = CliRunner()
    result = runner.invoke(
        domain_change_main.cli_command_domain_change,
        ["--org-id", "o", "--new-subdomain", "new"],
        obj={"output_format": "json"},
    )
    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == report


def test_cli_domain_change_prints_counts_table(monkeypatch):
    report = {
        "org_id": "o",
        "old_domain": "old.example",
        "new_domain": "new.example",
        "dry_run": True,
        "counts": {"issuer_client": 115, "connector": 4},
        "changes": [1, 2, 3],
        "warnings": [
            {
                "object_type": "webauthn_enrollment",
                "object_id": "wa-1",
                "reason": "must re-enrol",
            }
        ],
        "summary": {"totals": {"objects": 119}},
    }
    monkeypatch.setattr(
        domain_change_main.domain_change,
        "plan_domain_change",
        lambda ctx, **kwargs: report,
    )
    runner = CliRunner()
    result = runner.invoke(
        domain_change_main.cli_command_domain_change,
        ["--org-id", "o", "--new-subdomain", "new"],
        obj={"output_format": "console"},
    )
    assert result.exit_code == 0, result.output
    assert "issuer_client" in result.output
    assert "115" in result.output
    assert "connector" in result.output
    assert "webauthn_enrollment" in result.output
    assert "dry run" in result.output


def test_cli_domain_change_requires_new_subdomain():
    runner = CliRunner()
    result = runner.invoke(
        domain_change_main.cli_command_domain_change,
        ["--org-id", "o"],
        obj={"output_format": "console"},
    )
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# IAF-2371 ergonomics: aliases, per-component output, 409 preflight
# ---------------------------------------------------------------------------
def _api_exception(status, body):
    """Build an ApiException carrying a JSON body (the 409 preflight shape)."""
    exc = ApiException(status=status, reason="Conflict")
    exc.body = body
    return exc


def test_cli_domain_change_help():
    runner = CliRunner()
    result = runner.invoke(domain_change_main.cli_command_domain_change, ["--help"])
    assert result.exit_code == 0
    assert "--subdomain" in result.output
    assert "--issuer" in result.output
    assert "--dry-run" in result.output


def test_domain_change_posts_body(monkeypatch):
    api_client = FakeApiClient()
    _patch_client(monkeypatch, api_client)

    domain_change_module.plan_domain_change(
        object(),
        "org-1",
        "YYY.com",
        issuer_url="https://auth.YYY.com",
        dry_run=False,
    )

    (call,) = api_client.calls
    assert call["method"] == "POST"
    assert call["path"] == "/v1/orgs/{org_id}/domain_change"
    assert call["path_params"] == {"org_id": "org-1"}
    assert call["body"] == {
        "subdomain": "YYY.com",
        "issuer_url": "https://auth.YYY.com",
        "dry_run": False,
    }


def test_domain_change_dry_run_does_not_mutate(monkeypatch):
    api_client = FakeApiClient()
    _patch_client(monkeypatch, api_client)

    domain_change_module.plan_domain_change(
        object(),
        "org-1",
        "new",
        issuer_url="https://auth.new",
        dry_run=True,
    )

    (call,) = api_client.calls
    assert call["method"] == "POST"
    assert call["body"]["dry_run"] is True


def test_domain_change_409_raises_preflight(monkeypatch):
    body = '[{"component": "dns", "host": "auth.YYY.com", "ok": false}]'
    _patch_client(monkeypatch, FakeApiClient(error=_api_exception(409, body)))

    with pytest.raises(domain_change_module.DomainChangePreflightError) as info:
        domain_change_module.get_domain_change(object(), "org-1", "new")

    assert info.value.components[0]["host"] == "auth.YYY.com"


def test_domain_change_409_nonzero(monkeypatch):
    body = '[{"component": "dns", "host": "auth.YYY.com", "ok": false}]'
    monkeypatch.setattr(
        domain_change_main.domain_change,
        "plan_domain_change",
        lambda ctx, **kwargs: (_ for _ in ()).throw(_api_exception(409, body)),
    )
    runner = CliRunner()
    result = runner.invoke(
        domain_change_main.cli_command_domain_change,
        ["--org-id", "o", "--subdomain", "new", "--issuer", "https://auth.new"],
        obj={"output_format": "console"},
    )
    assert result.exit_code != 0
    assert "dns" in result.stderr
    assert "auth.YYY.com" in result.stderr


def test_domain_change_json_error(monkeypatch):
    body = '[{"component": "dns", "host": "auth.YYY.com", "ok": false}]'
    monkeypatch.setattr(
        domain_change_main.domain_change,
        "plan_domain_change",
        lambda ctx, **kwargs: (_ for _ in ()).throw(_api_exception(409, body)),
    )
    runner = CliRunner()
    result = runner.invoke(
        domain_change_main.cli_command_domain_change,
        ["--org-id", "o", "--subdomain", "new", "--issuer", "https://auth.new"],
        obj={"output_format": "json"},
    )
    assert result.exit_code != 0
    payload = json.loads(result.stderr)
    assert payload["error"] == "preflight_failed"
    assert payload["components"][0]["component"] == "dns"


def test_cli_domain_change_prints_component_table(monkeypatch):
    report = {
        "org_id": "o",
        "dry_run": False,
        "components": [
            {"name": "dns", "state": "succeeded", "detail": "auth.new"},
            {"name": "issuer", "state": "failed", "error": "client rewrite refused"},
            {"name": "connectors", "state": "skipped"},
        ],
        "warnings": [],
    }
    monkeypatch.setattr(
        domain_change_main.domain_change,
        "plan_domain_change",
        lambda ctx, **kwargs: report,
    )
    runner = CliRunner()
    result = runner.invoke(
        domain_change_main.cli_command_domain_change,
        ["--org-id", "o", "--subdomain", "new", "--issuer", "https://auth.new"],
        obj={"output_format": "console"},
    )
    assert result.exit_code == 0, result.output
    assert "dns" in result.output
    assert "succeeded" in result.output
    assert "issuer" in result.output
    assert "failed" in result.output
    assert "client rewrite refused" in result.output
    assert "skipped" in result.output


def test_component_state_tolerates_the_older_shape():
    assert domain_change_main._component_state({"ok": True}) == "succeeded"
    assert domain_change_main._component_state({"ok": False}) == "failed"
    assert domain_change_main._component_state({"status": "created"}) == "created"
    assert domain_change_main._component_state({"name": "dns"}) is None
    assert domain_change_main._failed_components([{"ok": False}, {"ok": True}]) == [
        {"ok": False}
    ]
    assert domain_change_main._failed_components(
        [{"name": "dns", "state": "failed"}]
    ) == [{"name": "dns", "state": "failed"}]
