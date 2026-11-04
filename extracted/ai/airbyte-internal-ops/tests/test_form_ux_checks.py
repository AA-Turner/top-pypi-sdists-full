from io import StringIO
from pathlib import Path
from unittest.mock import Mock

import cyclopts
import pytest
import yaml
from rich.console import Console

from airbyte_ops_mcp.cli import local as local_cli
from airbyte_ops_mcp.cli.app import app
from airbyte_ops_mcp.connector_ops.utils import ConnectorLanguage
from airbyte_ops_mcp.connector_qa.checks.form_ux import (
    ENABLED_CHECKS,
    HANDBOOK_URL,
    CheckFormUx01,
    CheckFormUx02,
    CheckFormUx03,
    CheckFormUx06,
    CheckFormUx09,
    CheckFormUx10,
    CheckFormUx11,
    CheckFormUx12,
    FormUxContext,
    _resolve_spec_cached,
    load_resolved_spec,
    render_form_ux_summary,
    walk_form_fields,
)
from airbyte_ops_mcp.connector_qa.models import CheckResult, CheckStatus, Finding

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "form_ux"


@pytest.fixture(autouse=True)
def clear_resolved_spec_cache():
    _resolve_spec_cached.cache_clear()
    yield
    _resolve_spec_cached.cache_clear()


def _connector_from_manifest(manifest_path: Path, manifest: dict) -> Mock:
    connector = Mock()
    connector.ab_internal_sl = 0
    connector.connector_spec_file_content = manifest.get("spec")
    connector.connector_type = "source"
    connector.is_released = False
    connector.language = ConnectorLanguage.MANIFEST_ONLY
    connector.manifest_path = manifest_path
    connector.metadata = {"name": "Example Connector"}
    connector.name_from_metadata = "Example Connector"
    connector.technical_name = "source-example"
    return connector


def _fixture_connector(name: str) -> Mock:
    manifest_path = FIXTURE_DIR / name
    manifest = yaml.safe_load(manifest_path.read_text())
    return _connector_from_manifest(manifest_path, manifest)


def _make_spec(properties: dict, required: list[str] | None = None) -> dict:
    return {
        "connection_specification": {
            "type": "object",
            "required": required or [],
            "properties": properties,
        }
    }


def test_all_form_ux_checks_pass_for_good_manifest():
    connector = _fixture_connector("good_manifest.yaml")

    results = {check.rule_id: check.run(connector) for check in ENABLED_CHECKS}

    assert set(results) == {
        f"UX-{number:02d}" for number in range(1, 13) if number != 7
    }
    assert all(result.status == CheckStatus.PASSED for result in results.values())


def test_each_form_ux_check_reports_only_expected_poor_manifest_paths():
    connector = _fixture_connector("poor_manifest.yaml")
    expected_paths = {
        "UX-01": {"missing_details"},
        "UX-02": {"credentials.oneOf[0].client_id"},
        "UX-03": {"repeated_description"},
        "UX-04": {"safe_boolean"},
        "UX-05": {"bad_pattern"},
        "UX-06": {"api_key"},
        "UX-08": {"batch_size"},
        "UX-09": {"workspace_id", "access_key"},
        "UX-10": {"api_docs"},
        "UX-11": {"credentials"},
        "UX-12": {"start_date"},
    }

    for check in ENABLED_CHECKS:
        result = check.run(connector)
        assert result.status == CheckStatus.FAILED, check.rule_id
        assert {finding.field_path for finding in result.findings} == expected_paths[
            check.rule_id
        ], check.rule_id
        assert {
            (finding.rule_id, finding.field_path) for finding in result.findings
        } == {(check.rule_id, path) for path in expected_paths[check.rule_id]}


def _invoke_qa_cli(connector_directory: Path) -> int:
    try:
        app(
            tokens=[
                "local",
                "connector",
                "qa",
                "--connector-directory",
                str(connector_directory),
            ],
            exit_on_error=False,
        )
    except cyclopts.exceptions.CycloptsError:
        return 1
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


def test_local_qa_does_not_fail_for_form_ux_findings(monkeypatch, tmp_path):
    connector = _fixture_connector("poor_manifest.yaml")
    output = StringIO()
    summary_path = tmp_path / "summary.md"
    monkeypatch.setattr(
        local_cli,
        "get_all_connectors_in_directory",
        lambda _: [connector],
    )
    monkeypatch.setattr(local_cli, "ENABLED_CHECKS", [CheckFormUx01()])
    monkeypatch.setattr(local_cli, "console", Console(file=output, width=200))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary_path))

    exit_code = _invoke_qa_cli(FIXTURE_DIR)

    warning = (
        "These are warnings. They don't fail the QA checks or block merge. "
        "Fix them in a separate PR, not in an unrelated change such as a version bump."
    )
    assert exit_code == 0
    assert "⚠️ WARN" in output.getvalue()
    assert warning in output.getvalue()
    assert f"## Form UX findings\n\n{warning}" in summary_path.read_text()


def test_local_qa_still_fails_for_blocking_checks(monkeypatch):
    class BlockingFormUxCheck(CheckFormUx01):
        blocking = True

    connector = _fixture_connector("poor_manifest.yaml")
    monkeypatch.setattr(
        local_cli,
        "get_all_connectors_in_directory",
        lambda _: [connector],
    )
    monkeypatch.setattr(local_cli, "ENABLED_CHECKS", [BlockingFormUxCheck()])
    monkeypatch.setattr(local_cli, "console", Console(file=StringIO(), width=200))
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)

    assert _invoke_qa_cli(FIXTURE_DIR) == 1


def test_field_walker_tracks_oneof_and_array_paths_without_markers_in_config_path():
    spec = _make_spec(
        {
            "credentials": {
                "type": "object",
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "auth_type": {"type": "string", "const": "api_key"},
                            "client_id": {"type": "string"},
                        },
                    }
                ],
            },
            "members": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["team_id"],
                    "properties": {"team_id": {"type": "string"}},
                },
            },
            "ignored_schema": "string",
        }
    )

    fields = {field.path: field for field in walk_form_fields(spec)}

    assert fields["credentials.oneOf[0].client_id"].config_path == (
        "credentials",
        "client_id",
    )
    assert fields["credentials.oneOf[0].auth_type"].is_discriminator is True
    assert fields["members[].team_id"].config_path == ("members", "team_id")
    assert fields["members[].team_id"].required is True
    assert "ignored_schema" not in fields


def test_ux02_skips_children_of_hidden_objects_and_oneof_options():
    spec = _make_spec(
        {
            "hidden_object": {
                "type": "object",
                "airbyte_hidden": True,
                "properties": {
                    "bad_child": {
                        "type": "string",
                        "title": "Bad Child",
                        "description": "A description that adds information.",
                    }
                },
            },
            "hidden_option": {
                "type": "object",
                "oneOf": [
                    {
                        "type": "object",
                        "airbyte_hidden": True,
                        "properties": {
                            "bad_option_child": {
                                "type": "string",
                                "title": "Bad Option Child",
                                "description": "A description that adds information.",
                            }
                        },
                    }
                ],
            },
        }
    )

    findings = CheckFormUx02().find(spec, FormUxContext(frozenset(), frozenset()))

    assert findings == []


@pytest.mark.parametrize(
    "pattern, field_format, expected_violation",
    [
        pytest.param(r"\d{4}-\d{2}-\d{2}", "date", False, id="date-pattern-date"),
        pytest.param(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}",
            "date-time",
            False,
            id="timestamp-pattern-date-time",
        ),
        pytest.param(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}",
            "date",
            True,
            id="timestamp-pattern-date-format",
        ),
        pytest.param(
            r"\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}",
            "date",
            True,
            id="whitespace-time-pattern-date-format",
        ),
    ],
)
def test_ux12_matches_format_to_date_or_timestamp_pattern(
    pattern, field_format, expected_violation
):
    spec = _make_spec(
        {
            "event_time": {
                "type": "string",
                "format": field_format,
                "pattern": pattern,
            }
        }
    )

    findings = CheckFormUx12().find(spec, FormUxContext(frozenset(), frozenset()))

    assert bool(findings) is expected_violation


def test_ux12_does_not_report_date_format_without_pattern():
    spec = _make_spec(
        {
            "event_date": {
                "type": "string",
                "format": "date",
            }
        }
    )

    assert CheckFormUx12().find(spec, FormUxContext(frozenset(), frozenset())) == []


@pytest.mark.parametrize(
    "title, expected_violation",
    [
        pytest.param("Azure Blob Storage", False, id="azure-blob-storage"),
        pytest.param("Google Ads", False, id="google-ads"),
        pytest.param("Google Sheets", False, id="google-sheets"),
        pytest.param("Amazon Seller Partner", False, id="amazon-seller-partner"),
        pytest.param("API key", False, id="acronym"),
        pytest.param("OAuth token", False, id="internal-capital"),
        pytest.param("iOS token", False, id="lowercase-internal-capital"),
        pytest.param("Start Widget", False, id="connector-name-word"),
        pytest.param("Start January", False, id="month-name"),
        pytest.param("start date", True, id="lowercase-first-word"),
        pytest.param("Client Id", True, id="client-id"),
        pytest.param("Personal Access Token", True, id="not-an-allowlisted-phrase"),
    ],
)
def test_ux02_sentence_case_allowlist_and_token_rules(title, expected_violation):
    spec = _make_spec(
        {
            "field": {
                "type": "string",
                "title": title,
                "description": "A descriptive value used to configure this connector.",
            }
        }
    )
    context = FormUxContext(
        connector_name_words=frozenset({"example", "connector", "widget"}),
        oauth_config_paths=frozenset(),
    )

    findings = CheckFormUx02().find(spec, context)

    assert bool(findings) is expected_violation
    if title == "Client Id":
        assert 'try "Client id"' in findings[0].message
    if title == "start date":
        assert 'try "Start date"' in findings[0].message


@pytest.mark.parametrize(
    "title, description, expected_violation",
    [
        pytest.param("Start Date", "Start date", True, id="same-words"),
        pytest.param(
            "Start date",
            "[Start date](https://example.test/guide)",
            True,
            id="markdown-link-text-is-retained",
        ),
        pytest.param("Start date", "<p>Start date</p>", True, id="html-is-stripped"),
        pytest.param("Start date", "and", True, id="empty-normalized-description"),
        pytest.param(
            "Start date",
            "Choose a date to begin reading records from the provider.",
            False,
            id="description-adds-context",
        ),
    ],
)
def test_ux03_description_word_subset(title, description, expected_violation):
    spec = _make_spec(
        {
            "field": {
                "type": "string",
                "title": title,
                "description": description,
            }
        }
    )
    context = FormUxContext(frozenset(), frozenset())

    findings = CheckFormUx03().find(spec, context)

    assert bool(findings) is expected_violation


def test_ux06_does_not_flag_access_key_id():
    spec = _make_spec(
        {
            "access_key_id": {
                "type": "string",
                "title": "Access key ID",
                "description": "Find this value in the provider's dashboard.",
            }
        }
    )

    assert CheckFormUx06().find(spec, FormUxContext(frozenset(), frozenset())) == []


def test_ux06_does_not_flag_expiry_dates_as_secrets():
    spec = _make_spec(
        {
            "token_expiry_date": {
                "type": "string",
                "format": "date-time",
                "title": "Token expiry date",
                "description": "The date when the token expires.",
            },
            "oauth_token_expiry_date": {
                "type": "string",
                "title": "OAuth token expiry date",
                "description": "The date when the OAuth token expires.",
            },
            "api_token_value": {
                "type": "string",
                "format": "date-time",
                "title": "API token value",
                "description": "A date-formatted API token value.",
            },
        }
    )

    assert CheckFormUx06().find(spec, FormUxContext(frozenset(), frozenset())) == []


@pytest.mark.parametrize("date_format", ["date", "date-time"])
def test_ux06_skips_secret_named_fields_with_date_formats(date_format):
    spec = _make_spec(
        {
            "api_token_value": {
                "type": "string",
                "format": date_format,
                "title": "API token value",
                "description": "A date-formatted API token value.",
            }
        }
    )

    assert CheckFormUx06().find(spec, FormUxContext(frozenset(), frozenset())) == []


@pytest.mark.parametrize(
    "description", [None, "", "   "], ids=["missing", "empty", "blank"]
)
def test_ux09_skips_fields_without_a_description(description):
    spec = _make_spec(
        {
            "workspace_id": {
                "type": "string",
                "title": "Workspace ID",
                "description": description,
            }
        }
    )

    assert CheckFormUx09().find(spec, FormUxContext(frozenset(), frozenset())) == []


def test_ux09_does_not_treat_http_as_a_url():
    spec = _make_spec(
        {
            "api_token": {
                "type": "string",
                "title": "API token",
                "description": "Use the HTTP API token",
            }
        }
    )

    findings = CheckFormUx09().find(spec, FormUxContext(frozenset(), frozenset()))

    assert {finding.field_path for finding in findings} == {"api_token"}


@pytest.mark.parametrize(
    "description, expected_violation",
    [
        pytest.param(
            "Malformed links: https://(www.)url.domain and https://",
            False,
            id="malformed-hosts",
        ),
        pytest.param(
            "Generate a token at https://github.com/settings/tokens",
            False,
            id="account-settings-url",
        ),
        pytest.param(
            "Read the docs at https://docs.airbyte.com/integrations/sources/slack",
            True,
            id="documentation-link-without-anchor",
        ),
        pytest.param(
            "Read the docs at https://docs.airbyte.com/integrations/sources/slack#prerequisites",
            False,
            id="documentation-link-with-anchor",
        ),
    ],
)
def test_ux10_only_reports_documentation_urls_without_anchors(
    description, expected_violation
):
    spec = _make_spec(
        {
            "documentation_url": {
                "type": "string",
                "title": "Documentation URL",
                "description": description,
            }
        }
    )

    findings = CheckFormUx10().find(spec, FormUxContext(frozenset(), frozenset()))

    assert bool(findings) is expected_violation
    if expected_violation:
        assert (
            "https://docs.airbyte.com/integrations/sources/slack" in findings[0].message
        )


@pytest.mark.parametrize(
    "properties, required, expected_paths",
    [
        pytest.param(
            {"credentials": {"type": "object", "oneOf": []}},
            [],
            {"credentials"},
            id="optional-selector",
        ),
        pytest.param(
            {"api_key": {"type": "string", "airbyte_secret": True}},
            [],
            {"connection_specification"},
            id="optional-secrets-without-selector",
        ),
        pytest.param(
            {"credentials": {"type": "object", "oneOf": []}},
            ["credentials"],
            set(),
            id="required-selector",
        ),
    ],
)
def test_ux11_auth_selector_and_optional_secret_cases(
    properties, required, expected_paths
):
    spec = _make_spec(properties, required)

    findings = CheckFormUx11().find(spec, FormUxContext(frozenset(), frozenset()))

    assert {finding.field_path for finding in findings} == expected_paths
    for finding in findings:
        assert finding.message.endswith(
            "If credentials are deliberately optional (for example, a public API), you can ignore this."
        )


def test_undefined_reference_fails_with_cdk_error_message(tmp_path):
    manifest = {
        "spec": {
            "connection_specification": {
                "type": "object",
                "properties": {"field": {"$ref": "#/definitions/not_found"}},
            }
        }
    }
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest))
    connector = _connector_from_manifest(manifest_path, manifest)

    result = CheckFormUx01().run(connector)

    assert result.status == CheckStatus.FAILED
    assert result.message.startswith("Undefined reference")
    assert result.findings == []


def test_resolved_spec_cache_invalidates_when_manifest_content_changes(tmp_path):
    manifest = {
        "definitions": {
            "shared_field": {
                "type": "string",
                "title": "Original title",
            }
        },
        "spec": _make_spec({"field": {"$ref": "#/definitions/shared_field"}}),
    }
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest))
    connector = _connector_from_manifest(manifest_path, manifest)

    first_spec = load_resolved_spec(connector)
    manifest["definitions"]["shared_field"]["title"] = "Updated title"
    manifest_path.write_text(yaml.safe_dump(manifest))
    second_spec = load_resolved_spec(connector)

    assert (
        first_spec["connection_specification"]["properties"]["field"]["title"]
        == "Original title"
    )
    assert (
        second_spec["connection_specification"]["properties"]["field"]["title"]
        == "Updated title"
    )


def test_missing_spec_fails_with_manifest_message():
    connector = _fixture_connector("good_manifest.yaml")
    connector.connector_spec_file_content = None

    result = CheckFormUx01().run(connector)

    assert result.status == CheckStatus.FAILED
    assert result.message == "No spec found in good_manifest.yaml"


def test_non_manifest_connector_is_skipped():
    connector = _fixture_connector("good_manifest.yaml")
    connector.language = ConnectorLanguage.PYTHON

    result = CheckFormUx01().run(connector)

    assert result.status == CheckStatus.SKIPPED


def test_form_ux_summary_groups_by_connector_and_rule():
    connector_a = _fixture_connector("poor_manifest.yaml")
    connector_a.technical_name = "source-alpha"
    connector_b = _fixture_connector("poor_manifest.yaml")
    connector_b.technical_name = "source-beta"
    check_01 = CheckFormUx01()
    check_02 = CheckFormUx02()
    results = [
        CheckResult(
            check=check_01,
            connector=connector_a,
            status=CheckStatus.FAILED,
            message="",
            findings=[
                Finding("UX-01", "region", "Missing title", check_01.anchor),
            ],
        ),
        CheckResult(
            check=check_02,
            connector=connector_a,
            status=CheckStatus.FAILED,
            message="",
            findings=[
                Finding("UX-02", "start_date", "Title case", check_02.anchor),
                Finding("UX-02", "end_date", "Title case", check_02.anchor),
            ],
        ),
        CheckResult(
            check=check_01,
            connector=connector_b,
            status=CheckStatus.FAILED,
            message="",
            findings=[
                Finding("UX-01", "api_key", "Missing description", check_01.anchor),
            ],
        ),
        CheckResult(
            check=check_02,
            connector=connector_b,
            status=CheckStatus.PASSED,
            message="",
        ),
    ]

    summary = render_form_ux_summary(results)

    assert summary.count("### Form UX:") == 2
    assert "### Form UX: source-alpha" in summary
    assert "### Form UX: source-beta" in summary
    assert "| UX-01 | 1 | [Handbook](" + HANDBOOK_URL + "#ux-01) |" in summary
    assert "| UX-02 | 2 | [Handbook](" + HANDBOOK_URL + "#ux-02) |" in summary
    assert "<summary>UX-02 (2)</summary>" in summary
    assert "- start_date: Title case" in summary
    assert "- end_date: Title case" in summary
    assert "UX-03" not in summary
