# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Tests for the static SaaS Sandbox support check.

The sandbox CLI is replaced by an executable on `PATH` that answers the
offline discovery commands from a JSON file, so the code under test spawns a
real process.
"""

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

import pytest

from airbyte_ops_mcp.regression_tests import sandbox_support
from airbyte_ops_mcp.regression_tests.sandbox_support import (
    SandboxDiscovery,
    check_sandbox_support,
    load_connector_files,
    run_sandbox_support_check,
)

pytestmark = pytest.mark.unit

CONNECTOR_DIR = (
    Path(__file__).parent / "fixtures" / "sandbox_support" / "source-example"
)


def _operation(
    path: str,
    parameters: list[str],
    *,
    status: str = "supported",
    max_limit: int | None = 1000,
) -> dict:
    operation = {
        "id": "get.api." + path,
        "method": "GET",
        "path": "/api/" + path,
        "status": status,
        "parameters": [{"name": name, "in": "query"} for name in parameters],
    }
    if max_limit is not None:
        operation["pagination"] = {"limit_param": "limit", "max_limit": max_limit}
    return operation


DISCOVERY = {
    "providers": {
        "providers": [
            {
                "id": "github",
                "hosts": ["api.github.com"],
                "unknown_parameters": "ignore",
            },
            {"id": "slack", "hosts": ["slack.com"], "unknown_parameters": "reject"},
        ]
    },
    "operations slack": {
        "schema_version": 1,
        "provider": "slack",
        "operations": [
            _operation("conversations.list", ["cursor", "limit", "types"]),
            _operation(
                "conversations.history",
                ["channel", "cursor", "limit", "oldest", "latest"],
            ),
            _operation("conversations.members", [], status="unsupported"),
        ],
    },
    "entities slack": {"entities": [{"name": "channels"}, {"name": "messages"}]},
    # The shape `sandbox schema PROVIDER ENTITY` prints: the entity's dataset
    # input schema references the record definition.
    "schema slack messages": {
        "name": "messages",
        "inputs": {
            "apply": {
                "collection_key": "messages",
                "schema": {
                    "$ref": "#/$defs/message",
                    "$defs": {
                        "message": {
                            "properties": {
                                "channel": {},
                                "ts": {},
                                "thread_ts": {},
                                "text": {},
                            }
                        }
                    },
                },
            }
        },
    },
}

_FAKE_SANDBOX = """\
import json, os, sys
args = sys.argv[1:]
if args[-1] != "--offline":
    sys.exit(2)
discovery = json.load(open(os.environ["FAKE_DISCOVERY"]))
key = " ".join(args[:-1])
if key not in discovery:
    print("unknown provider", file=sys.stderr)
    sys.exit(1)
print(json.dumps(discovery[key]))
"""


@pytest.fixture
def discovery(tmp_path, monkeypatch):
    """A fake `sandbox` on PATH serving `DISCOVERY`; returns a writer to change it."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    executable = bin_dir / "sandbox"
    executable.write_text(f"#!{sys.executable}\n{_FAKE_SANDBOX}")
    executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
    data = tmp_path / "discovery.json"
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FAKE_DISCOVERY", str(data))

    def write(overrides: dict | None = None) -> SandboxDiscovery:
        data.write_text(json.dumps({**DISCOVERY, **(overrides or {})}))
        return SandboxDiscovery()

    return write


@pytest.fixture
def connector():
    return load_connector_files(CONNECTOR_DIR)


def test_a_stream_and_its_parent_are_checked_against_the_twin(discovery, connector):
    report = check_sandbox_support(*connector, discovery(), streams=["messages"])

    assert report.result == "supported"
    assert report.provider == "slack"
    operations = {(op.stream, op.path): op for op in report.operations}
    assert set(operations) == {
        ("messages", "/api/conversations.history"),
        ("channels", "/api/conversations.list"),
    }
    history = operations[("messages", "/api/conversations.history")]
    assert history.parameters == ["channel", "cursor", "limit", "oldest"]
    assert history.page_size == 1000
    assert history.twin_operation == "get.api.conversations.history"
    # The custom requester is reported, not silently trusted.
    assert any("MessagesRequester" in warning for warning in report.warnings)


def test_an_undeclared_parameter_is_unsupported(discovery, connector):
    catalog = json.loads(json.dumps(DISCOVERY["operations slack"]))
    catalog["operations"][1] = _operation(
        "conversations.history", ["channel", "cursor", "limit"]
    )

    report = check_sandbox_support(
        *connector, discovery({"operations slack": catalog}), streams=["messages"]
    )

    assert report.result == "unsupported"
    assert any("'oldest' is not declared" in reason for reason in report.reasons)


def test_a_page_size_above_the_twins_maximum_is_unsupported(discovery, connector):
    catalog = json.loads(json.dumps(DISCOVERY["operations slack"]))
    catalog["operations"][0] = _operation(
        "conversations.list", ["cursor", "limit", "types"], max_limit=999
    )

    report = check_sandbox_support(
        *connector, discovery({"operations slack": catalog}), streams=["channels"]
    )

    assert report.result == "unsupported"
    assert any("exceeds the twin's maximum 999" in r for r in report.reasons)


def test_an_unsupported_twin_operation_is_unsupported(discovery, connector):
    report = check_sandbox_support(*connector, discovery(), streams=["members"])

    assert report.result == "unsupported"
    assert any("is unsupported" in reason for reason in report.reasons)


def test_a_twin_that_ignores_unknown_parameters_accepts_them(discovery, connector):
    providers = {
        "providers": [
            {"id": "slack", "hosts": ["slack.com"], "unknown_parameters": "ignore"}
        ]
    }
    catalog = json.loads(json.dumps(DISCOVERY["operations slack"]))
    catalog["operations"][1] = _operation("conversations.history", ["channel"])

    report = check_sandbox_support(
        *connector,
        discovery({"providers": providers, "operations slack": catalog}),
        streams=["messages"],
    )

    assert report.result == "supported"


def test_a_host_no_provider_serves_is_unsupported(discovery):
    metadata = {"data": {"allowedHosts": {"hosts": ["api.example.com"]}}}

    report = check_sandbox_support(metadata, {}, discovery())

    assert report.result == "unsupported"
    assert report.provider is None


def test_a_connector_without_a_manifest_is_unknown(discovery, connector):
    metadata, _manifest = connector

    report = check_sandbox_support(metadata, None, discovery())

    assert (report.result, report.provider) == ("unknown", "slack")


def test_a_stream_missing_from_the_manifest_is_unknown(discovery, connector):
    report = check_sandbox_support(*connector, discovery(), streams=["nope"])

    assert report.result == "unknown"


@pytest.mark.parametrize(
    "needs,expected",
    [
        (["messages.thread_ts"], "supported"),
        (["messages.reactions"], "unsupported"),
        (["files"], "unsupported"),
    ],
)
def test_dataset_needs_are_checked_against_the_twin_schema(
    discovery, connector, needs, expected
):
    report = check_sandbox_support(
        *connector, discovery(), streams=["channels"], dataset_needs=needs
    )

    assert report.result == expected


def test_a_missing_sandbox_cli_makes_the_check_unknown(monkeypatch, tmp_path):
    monkeypatch.setenv("PATH", str(tmp_path))

    report = run_sandbox_support_check(
        connector_name="source-example", connector_dir=CONNECTOR_DIR
    )

    assert report["result"] == "unknown"
    assert "sandbox" in report["reasons"][0]


def test_without_a_connector_dir_the_files_are_read_from_github(discovery, monkeypatch):
    discovery()
    calls: list[tuple[str, str]] = []

    def fake_fetch(connector_name, ref, token):
        calls.append((connector_name, ref))
        return load_connector_files(CONNECTOR_DIR)

    monkeypatch.setattr(sandbox_support, "fetch_connector_files", fake_fetch)

    report = run_sandbox_support_check(
        connector_name="source-example", streams=["messages"], ref="abc123"
    )

    assert calls == [("source-example", "abc123")]
    assert report["result"] == "supported"
    assert report["connector"] == "source-example"


def _manifest(stream: dict) -> dict:
    return {"version": "6.60.5", "type": "DeclarativeSource", "streams": [stream]}


def _stream(name: str, path: str, **requester: object) -> dict:
    return {
        "type": "DeclarativeStream",
        "name": name,
        "retriever": {
            "type": "SimpleRetriever",
            "requester": {
                "type": "HttpRequester",
                "url_base": "https://slack.com/api/",
                "path": path,
                **requester,
            },
            "record_selector": {
                "type": "RecordSelector",
                "extractor": {"type": "DpathExtractor", "field_path": []},
            },
        },
    }


SLACK_METADATA = {"data": {"allowedHosts": {"hosts": ["slack.com"]}}}


@pytest.mark.parametrize(
    "hosts,expected",
    [
        (["${subdomain}.slack.com", "slack.com"], "slack"),
        (["*.slack.com"], "slack"),
    ],
)
def test_config_placeholders_and_wildcards_in_allowed_hosts_match(
    discovery, hosts, expected
):
    report = check_sandbox_support(
        {"data": {"allowedHosts": {"hosts": hosts}}}, None, discovery()
    )

    assert report.provider == expected


def test_a_host_taken_entirely_from_config_is_unknown(discovery):
    report = check_sandbox_support(
        {"data": {"allowedHosts": {"hosts": ["${api_url}"]}}}, {}, discovery()
    )

    assert report.result == "unknown"


def test_a_broken_manifest_reference_is_unknown_not_a_crash(discovery, tmp_path):
    discovery()
    connector = tmp_path / "source-broken"
    connector.mkdir()
    (connector / "metadata.yaml").write_text(json.dumps(SLACK_METADATA))
    (connector / "manifest.yaml").write_text(
        json.dumps({"streams": [{"$ref": "#/definitions/missing"}]})
    )

    report = run_sandbox_support_check(
        connector_name="source-broken", connector_dir=connector
    )

    assert report["result"] == "unknown"


def test_a_path_matching_several_twin_operations_equally_is_unknown(discovery):
    catalog = {
        "operations": [
            {"id": "a", "method": "GET", "path": "/api/{x}", "status": "supported"},
            {"id": "b", "method": "GET", "path": "/api/{y}", "status": "supported"},
        ]
    }
    manifest = _manifest(_stream("s", "{{ config['endpoint'] }}"))

    report = check_sandbox_support(
        SLACK_METADATA, manifest, discovery({"operations slack": catalog})
    )

    assert report.result == "unknown"
    assert any("several twin operations" in reason for reason in report.reasons)


def test_an_exact_path_wins_over_a_template(discovery):
    catalog = {
        "operations": [
            {"id": "t", "method": "GET", "path": "/api/{x}", "status": "supported"},
            {
                "id": "e",
                "method": "GET",
                "path": "/api/users.list",
                "status": "supported",
            },
        ]
    }

    report = check_sandbox_support(
        SLACK_METADATA,
        _manifest(_stream("users", "users.list")),
        discovery({"operations slack": catalog}),
    )

    assert report.operations[0].twin_operation == "e"


def test_a_query_parameter_api_key_counts_as_a_sent_parameter(discovery):
    stream = _stream(
        "users",
        "conversations.list",
        authenticator={
            "type": "ApiKeyAuthenticator",
            "api_token": "{{ config['key'] }}",
            "inject_into": {
                "type": "RequestOption",
                "inject_into": "request_parameter",
                "field_name": "token",
            },
        },
    )

    report = check_sandbox_support(SLACK_METADATA, _manifest(stream), discovery())

    assert report.result == "unsupported"
    assert any("'token' is not declared" in reason for reason in report.reasons)


def test_interpolated_request_parameters_are_unknown_with_a_reason(discovery):
    stream = _stream(
        "users", "conversations.list", request_parameters="{{ config['params'] }}"
    )

    report = check_sandbox_support(SLACK_METADATA, _manifest(stream), discovery())

    assert report.result == "unknown"
    assert any("interpolated" in reason for reason in report.reasons)


def test_a_state_delegating_stream_is_checked_through_both_streams(discovery):
    stream = {
        "type": "StateDelegatingStream",
        "name": "channels",
        "full_refresh_stream": _stream("channels", "conversations.list"),
        "incremental_stream": _stream("channels", "conversations.history"),
    }

    report = check_sandbox_support(SLACK_METADATA, _manifest(stream), discovery())

    assert {op.path for op in report.operations} == {
        "/api/conversations.list",
        "/api/conversations.history",
    }
    assert report.result == "supported"


def test_inner_streams_sharing_an_operation_are_checked_together(discovery):
    # Both inner streams call conversations.list; only the incremental one
    # sends `oldest`, which the twin does not declare there and rejects.
    stream = {
        "type": "StateDelegatingStream",
        "name": "channels",
        "full_refresh_stream": _stream(
            "channels", "conversations.list", request_parameters={"types": "x"}
        ),
        "incremental_stream": _stream(
            "channels",
            "conversations.list",
            request_parameters={"types": "x", "oldest": "{{ stream_interval.start }}"},
        ),
    }

    report = check_sandbox_support(SLACK_METADATA, _manifest(stream), discovery())

    (operation,) = report.operations
    assert operation.parameters == ["types", "oldest"]
    assert report.result == "unsupported"
    assert any("oldest" in reason for reason in report.reasons)


def test_a_templated_host_label_matches_the_twin_host(discovery):
    stream = _stream("users", "conversations.list")
    stream["retriever"]["requester"]["url_base"] = (
        "https://{{ config['workspace'] }}.slack.com/api/"
    )
    providers = {"providers": [{"id": "slack", "hosts": ["acme.slack.com"]}]}

    report = check_sandbox_support(
        {"data": {"allowedHosts": {"hosts": ["${workspace}.slack.com"]}}},
        _manifest(stream),
        discovery({"providers": providers}),
    )

    assert report.result == "supported"
    assert report.operations[0].host == "{{ config['workspace'] }}.slack.com"


def test_twin_operations_tied_on_score_and_id_are_ambiguous_not_a_crash(discovery):
    duplicate = _operation("conversations.list", ["cursor", "limit", "types"])
    operations = {
        **DISCOVERY["operations slack"],
        "operations": [duplicate, dict(duplicate)],
    }
    stream = _stream("channels", "conversations.list")

    report = check_sandbox_support(
        SLACK_METADATA,
        _manifest(stream),
        discovery({"operations slack": operations}),
    )

    assert report.result == "unknown"
    assert "matches several twin operations equally" in report.reasons[0]


def _unreadable_page_size_stream(path: str = "conversations.list") -> dict:
    stream = _stream("channels", path)
    stream["retriever"]["paginator"] = {
        "type": "DefaultPaginator",
        "pagination_strategy": {
            "type": "CursorPagination",
            "page_size": "{{ config['page_size'] }}",
            "cursor_value": "{{ response.next_cursor }}",
        },
    }
    return stream


def test_a_page_size_that_cannot_be_read_is_unknown(discovery):
    report = check_sandbox_support(
        SLACK_METADATA, _manifest(_unreadable_page_size_stream()), discovery()
    )

    assert report.result == "unknown"
    assert report.reasons == [
        "channels GET /api/conversations.list: page size "
        "\"{{ config['page_size'] }}\" could not be read, so the twin's maximum "
        "1000 was not checked"
    ]


def test_an_unreadable_page_size_is_only_a_warning_without_a_twin_maximum(discovery):
    catalog = json.loads(json.dumps(DISCOVERY["operations slack"]))
    catalog["operations"][0] = _operation(
        "conversations.list", ["cursor", "limit", "types"], max_limit=None
    )

    report = check_sandbox_support(
        SLACK_METADATA,
        _manifest(_unreadable_page_size_stream()),
        discovery({"operations slack": catalog}),
    )

    assert report.result == "supported"
    assert any("the twin declares no maximum" in w for w in report.warnings)


def test_a_definite_gap_wins_over_an_unreadable_page_size(discovery):
    report = check_sandbox_support(
        SLACK_METADATA,
        _manifest(_unreadable_page_size_stream("conversations.members")),
        discovery(),
    )

    assert report.result == "unsupported"


def test_a_host_placeholder_resolves_from_the_spec_default(discovery):
    manifest = {
        **_manifest(_stream("channels", "conversations.list")),
        "spec": {
            "connection_specification": {
                "properties": {
                    "api_url": {"type": "string", "default": "https://api.github.com/"}
                }
            }
        },
    }

    report = check_sandbox_support(
        {"data": {"allowedHosts": {"hosts": ["${api_url}"]}}},
        manifest,
        discovery(),
        host_only=True,
    )

    assert (report.result, report.provider) == ("supported", "github")


def _oauth(endpoint: str) -> dict:
    return {
        "type": "OAuthAuthenticator",
        "client_id": "{{ config['client_id'] }}",
        "client_secret": "{{ config['client_secret'] }}",
        "refresh_token": "{{ config['refresh_token'] }}",
        "token_refresh_endpoint": endpoint,
    }


def _token_operation(status: str = "supported") -> dict:
    return {
        "id": "post.api.oauth.v2.access",
        "method": "POST",
        "path": "/api/oauth.v2.access",
        "status": status,
        "parameters": [],
    }


def _slack_operations(*extra: dict) -> dict:
    operations = DISCOVERY["operations slack"]
    return {
        "operations slack": {
            **operations,
            "operations": [*operations["operations"], *extra],
        }
    }


@pytest.mark.parametrize(
    "authenticator",
    [
        _oauth("https://slack.com/api/oauth.v2.access"),
        # A SelectiveAuthenticator picks one authenticator from config.
        {
            "type": "SelectiveAuthenticator",
            "authenticator_selection_path": ["credentials", "option"],
            "authenticators": {
                "oauth": _oauth("https://slack.com/api/oauth.v2.access")
            },
        },
    ],
)
def test_an_authenticators_token_endpoint_is_checked(discovery, authenticator):
    manifest = _manifest(
        _stream("channels", "conversations.list", authenticator=authenticator)
    )

    report = check_sandbox_support(
        SLACK_METADATA, manifest, discovery(_slack_operations(_token_operation()))
    )

    assert report.result == "supported"
    token = [need for need in report.operations if need.token_endpoint]
    assert [(need.method, need.path, need.twin_operation) for need in token] == [
        ("POST", "/api/oauth.v2.access", "post.api.oauth.v2.access")
    ]


@pytest.mark.parametrize(
    "endpoint,operations,result,reason",
    [
        # Served by another host than any the twin serves.
        (
            "https://oauth2.example.com/token",
            (),
            "unsupported",
            "not served by the twin",
        ),
        (
            "https://slack.com/api/oauth.v2.access",
            (_token_operation("unsupported"),),
            "unsupported",
            "is unsupported",
        ),
        # Twins may serve a token endpoint without listing it; the run decides.
        ("https://slack.com/api/oauth.v2.access", (), "supported", None),
    ],
)
def test_a_token_endpoint_the_twin_does_not_cover(
    discovery, endpoint, operations, result, reason
):
    manifest = _manifest(
        _stream("channels", "conversations.list", authenticator=_oauth(endpoint))
    )

    report = check_sandbox_support(
        SLACK_METADATA, manifest, discovery(_slack_operations(*operations))
    )

    assert report.result == result
    if reason is None:
        assert any("token endpoint" in warning for warning in report.warnings)
    else:
        assert any(reason in text for text in report.reasons)


def test_a_database_source_without_a_manifest_is_unsupported(discovery):
    metadata = {
        "data": {"allowedHosts": {"hosts": ["${host}"]}, "connectorSubtype": "database"}
    }

    report = check_sandbox_support(metadata, None, discovery())

    assert report.result == "unsupported"
    assert "JDBC" in report.reasons[0]


def test_check_streams_selects_what_the_manifests_check_reads(discovery):
    manifest = {
        **_manifest(_stream("channels", "conversations.list")),
        "check": {"type": "CheckStream", "stream_names": ["channels"]},
    }
    manifest["streams"].append(_stream("history", "conversations.history"))

    report = check_sandbox_support(
        SLACK_METADATA, manifest, discovery(), streams=["history"], check_streams=True
    )

    assert [need.stream for need in report.operations] == ["channels"]


def test_a_host_only_check_reads_no_stream(discovery):
    report = check_sandbox_support(SLACK_METADATA, None, discovery(), host_only=True)

    assert (report.result, report.provider, report.operations) == (
        "supported",
        "slack",
        [],
    )


MANIFEST_ONLY = {"data": {"tags": ["language:manifest-only"]}}


def test_manifest_stream_names(connector):
    _metadata, manifest = connector

    assert sandbox_support.manifest_stream_names(MANIFEST_ONLY, manifest) == {
        "channels",
        "members",
        "messages",
    }
    # Python streams would be invisible in the manifest.
    assert sandbox_support.manifest_stream_names({"data": {}}, manifest) is None
    assert sandbox_support.manifest_stream_names(MANIFEST_ONLY, None) is None


def test_dynamic_streams_cannot_be_listed(connector):
    _metadata, manifest = connector

    with pytest.raises(ValueError, match="dynamic_streams"):
        sandbox_support.manifest_stream_names(
            MANIFEST_ONLY,
            {**manifest, "dynamic_streams": [{"type": "DynamicDeclarativeStream"}]},
        )


def test_an_unserved_token_host_of_one_authenticator_option_is_a_warning(discovery):
    authenticator = {
        "type": "SelectiveAuthenticator",
        "authenticator_selection_path": ["credentials", "option"],
        "authenticators": {
            "oauth": _oauth("https://oauth2.example.com/token"),
            "token": {
                "type": "BearerAuthenticator",
                "api_token": "{{ config['token'] }}",
            },
        },
    }
    manifest = _manifest(
        _stream("channels", "conversations.list", authenticator=authenticator)
    )

    report = check_sandbox_support(SLACK_METADATA, manifest, discovery())

    assert report.result == "supported"
    assert any("one authenticator option" in warning for warning in report.warnings)


def test_an_unsupported_token_operation_of_one_authenticator_option_is_a_warning(
    discovery,
):
    authenticator = {
        "type": "SelectiveAuthenticator",
        "authenticator_selection_path": ["credentials", "option"],
        "authenticators": {
            "oauth": _oauth("https://slack.com/api/oauth.v2.access"),
            "token": {
                "type": "BearerAuthenticator",
                "api_token": "{{ config['token'] }}",
            },
        },
    }
    manifest = _manifest(
        _stream("channels", "conversations.list", authenticator=authenticator)
    )

    report = check_sandbox_support(
        SLACK_METADATA,
        manifest,
        discovery(_slack_operations(_token_operation("unsupported"))),
    )

    assert report.result == "supported"
    assert any("is unsupported (one authenticator option" in w for w in report.warnings)


@pytest.mark.parametrize("order", [["selective", "direct"], ["direct", "selective"]])
def test_a_token_endpoint_one_stream_requires_stays_required(discovery, order):
    endpoint = "https://oauth2.example.com/token"
    authenticators = {
        "selective": {
            "type": "SelectiveAuthenticator",
            "authenticator_selection_path": ["credentials", "option"],
            "authenticators": {"oauth": _oauth(endpoint)},
        },
        "direct": _oauth(endpoint),
    }
    manifest = _manifest(
        _stream(order[0], "conversations.list", authenticator=authenticators[order[0]])
    )
    manifest["streams"].append(
        _stream(order[1], "conversations.list", authenticator=authenticators[order[1]])
    )

    report = check_sandbox_support(SLACK_METADATA, manifest, discovery(), streams=order)

    assert report.result == "unsupported"


@pytest.mark.parametrize(
    "spec",
    [
        {"connection_specification": {"properties": {"api_url": True}}},
        {"connection_specification": "x"},
        "x",
    ],
)
def test_an_odd_spec_leaves_host_placeholders_alone(discovery, spec):
    report = check_sandbox_support(
        {"data": {"allowedHosts": {"hosts": ["${api_url}"]}}},
        {**_manifest(_stream("channels", "conversations.list")), "spec": spec},
        discovery(),
        host_only=True,
    )

    assert report.result == "unknown"


HYBRID_DIR = Path(__file__).parent / "fixtures" / "sandbox_support" / "source-hybrid"
GITHUB_OPERATIONS = {
    "operations github": {
        "provider": "github",
        "operations": [
            {
                "id": "get.repos.owner.repo.issues",
                "method": "GET",
                "path": "/repos/{owner}/{repo}/issues",
                "status": "supported",
                "parameters": [],
            }
        ],
    }
}


def test_a_hybrid_connectors_manifest_is_read_from_its_package(discovery):
    metadata, manifest = load_connector_files(HYBRID_DIR)

    assert manifest is not None
    # `${api_url}` resolves from the packaged manifest's spec, and the url_base
    # read from config renders with the same default.
    report = check_sandbox_support(
        metadata, manifest, discovery(GITHUB_OPERATIONS), streams=["issues"]
    )

    assert (report.result, report.provider) == ("supported", "github")
    (need,) = report.operations
    assert (need.host, need.path, need.twin_operation) == (
        "api.github.com",
        "/repos/{{ config['owner'] }}/{{ config['repo'] }}/issues",
        "get.repos.owner.repo.issues",
    )


def test_a_hybrid_connectors_manifest_is_fetched_from_its_package(
    discovery, monkeypatch
):
    discovery(GITHUB_OPERATIONS)
    base = "airbyte-integrations/connectors/source-hybrid/"
    requested: list[str] = []

    def contents_at_ref(owner, repo, path, ref, token):
        # GitHub at `ref`, serving the fixture's files.
        requested.append(path)
        local = HYBRID_DIR / path.removeprefix(base)
        return local.read_text() if local.is_file() else None

    monkeypatch.setattr(sandbox_support, "get_file_contents_at_ref", contents_at_ref)

    report = run_sandbox_support_check(
        connector_name="source-hybrid", streams=["issues"], ref="abc123"
    )

    assert report["result"] == "supported"
    assert requested == [
        f"{base}metadata.yaml",
        f"{base}manifest.yaml",
        f"{base}source_hybrid/manifest.yaml",
    ]


def test_a_python_connector_without_any_manifest_has_none(tmp_path):
    (tmp_path / "metadata.yaml").write_text(json.dumps(SLACK_METADATA))
    (tmp_path / "source_x").mkdir()

    assert load_connector_files(tmp_path)[1] is None


def _spec(**properties: dict) -> dict:
    return {"connection_specification": {"properties": properties}}


@pytest.mark.parametrize(
    "url_base,spec,result",
    [
        # The spec's default.
        (
            "{{ config['api_url'] }}",
            _spec(api_url={"default": "https://slack.com/api/"}),
            "supported",
        ),
        (
            "{{ config.get('api_url', 'https://other.example.com').rstrip('/') }}",
            _spec(api_url={"default": "https://slack.com/api/"}),
            "supported",
        ),
        # Without a spec default the key's value is unknown, whatever the
        # manifest falls back to: a case's config may set it.
        ("{{ config['api_url'] }}", _spec(api_url={"type": "string"}), "unknown"),
        ("{{ config['api_url'] }}", _spec(api_url={"default": ""}), "unknown"),
        (
            "{{ config.get('api_url', 'https://slack.com/api').rstrip('/') }}",
            {},
            "unknown",
        ),
        # A template the CDK cannot render comes back unchanged.
        (
            "https://{{ config['n'] + 'x' }}/api",
            _spec(n={"default": 5}),
            "unknown",
        ),
        # A key inside an object default has no default of its own.
        (
            "{{ config['endpoint'].get('url', 'https://slack.com/api/') }}",
            _spec(endpoint={"default": {}}),
            "unknown",
        ),
        # A condition on a key without a default could take either branch.
        (
            "{{ 'https://slack.com/api' if config['sandbox'] else "
            "'https://other.example.com/api' }}",
            {},
            "unknown",
        ),
        (
            "{{ 'https://slack.com/api' if 'sandbox' in config else "
            "'https://other.example.com/api' }}",
            {},
            "unknown",
        ),
    ],
)
def test_a_url_base_read_from_config_renders_with_its_defaults(
    discovery, url_base, spec, result
):
    stream = _stream("channels", "conversations.list")
    stream["retriever"]["requester"]["url_base"] = url_base

    report = check_sandbox_support(
        SLACK_METADATA, {**_manifest(stream), "spec": spec}, discovery()
    )

    assert report.result == result
    if result == "supported":
        assert report.operations[0].twin_operation == "get.api.conversations.list"
    else:
        assert any("has no static host" in reason for reason in report.reasons)


def _jobs_stream(url_base: str = "https://youtubereporting.googleapis.com/v1/") -> dict:
    stream = _stream("reports", "jobs")
    stream["retriever"]["requester"]["url_base"] = url_base
    return stream


def _download_stream(url_base: str, parent: dict | None) -> dict:
    """A stream reading files whose URLs its parent's records carry (YouTube reports)."""
    stream = _stream("report_rows", "")
    stream["retriever"]["requester"]["url_base"] = url_base
    if parent is not None:
        stream["retriever"]["partition_router"] = {
            "type": "SubstreamPartitionRouter",
            "parent_stream_configs": [
                {
                    "type": "ParentStreamConfig",
                    "parent_key": "id",
                    "partition_field": "id",
                    "extra_fields": [["downloadUrl"]],
                    "stream": parent,
                }
            ],
        }
    return stream


DOWNLOAD_URL = "{{ stream_partition['extra_fields']['downloadUrl'] }}"
YOUTUBE_METADATA = {
    "data": {
        "allowedHosts": {"hosts": ["*.googleapis.com"]},
        "tags": ["language:manifest-only"],
    }
}
YOUTUBE_DISCOVERY = {
    "providers": {
        "providers": [
            {
                "id": "youtube_analytics",
                "hosts": ["youtubereporting.googleapis.com"],
                "unknown_parameters": "ignore",
            }
        ]
    },
    "operations youtube_analytics": {
        "provider": "youtube_analytics",
        "operations": [
            {
                "id": "get.v1.jobs",
                "method": "GET",
                "path": "/v1/jobs",
                "status": "supported",
                "parameters": [],
            }
        ],
    },
}


def test_a_url_the_twin_generates_in_parent_records_is_a_warning(discovery):
    stream = _download_stream(DOWNLOAD_URL, _jobs_stream())

    report = check_sandbox_support(
        YOUTUBE_METADATA, _manifest(stream), discovery(YOUTUBE_DISCOVERY)
    )

    assert report.result == "supported"
    # Only the parent's request can be checked.
    assert [need.stream for need in report.operations] == ["reports"]
    assert report.warnings == [
        f"report_rows: url_base {DOWNLOAD_URL!r} takes its host from reports "
        "records (downloadUrl), so its requests were not checked here. The case "
        "lane's twin-gap gate covers them when they reach the twin; a URL on a "
        "host the twin does not serve fails inside the sandbox (no egress) and "
        "is not reported as a twin gap"
    ]


@pytest.mark.parametrize(
    "url_base,parent,reason",
    [
        # The parent's own host is unknown, so nothing says the URLs are the twin's.
        (
            DOWNLOAD_URL,
            _jobs_stream("{{ config['host'] }}"),
            "not every parent is served by the twin",
        ),
        # Partition data without a parent stream to take it from.
        (DOWNLOAD_URL, None, "has no static host"),
        # A partition key, not an extra field: a `partition_field` named
        # downloadUrl would carry the parent's (dataset-chosen) id.
        ("{{ stream_partition['downloadUrl'] }}", _jobs_stream(), "has no static host"),
        # A host of its own before the parent's value.
        (
            f"files.example.com/{DOWNLOAD_URL}",
            _jobs_stream(),
            "has no static host",
        ),
        (f"https://{DOWNLOAD_URL}", _jobs_stream(), "has no static host"),
        # An extra field no parent stream config declares.
        (
            "{{ stream_partition['extra_fields']['fileUrl'] }}",
            _jobs_stream(),
            "has no static host",
        ),
        # Not only parent records: config, or a literal host of its own.
        (
            "{{ config['scheme'] }}://{{ stream_partition['host'] }}",
            _jobs_stream(),
            "has no static host",
        ),
        (
            "{{ 'https://files.example.com/' ~ stream_partition['downloadUrl'] }}",
            _jobs_stream(),
            "has no static host",
        ),
    ],
)
def test_a_url_base_from_records_stays_unknown_unless_the_twin_generates_it(
    discovery, url_base, parent, reason
):
    stream = _download_stream(url_base, parent)

    report = check_sandbox_support(
        YOUTUBE_METADATA, _manifest(stream), discovery(YOUTUBE_DISCOVERY)
    )

    assert report.result == "unknown"
    assert any(
        text.startswith("report_rows:") and reason in text for text in report.reasons
    )


def test_a_url_in_dataset_records_of_another_twin_stays_unknown(discovery):
    stream = _download_stream(DOWNLOAD_URL, _stream("channels", "conversations.list"))

    report = check_sandbox_support(SLACK_METADATA, _manifest(stream), discovery())

    assert report.result == "unknown"
    assert any("not known to generate" in reason for reason in report.reasons)


def test_a_connector_with_python_code_is_warned_about(discovery):
    metadata, manifest = load_connector_files(HYBRID_DIR)

    report = check_sandbox_support(
        metadata, manifest, discovery(GITHUB_OPERATIONS), streams=["issues"]
    )

    assert any("not manifest-only" in warning for warning in report.warnings)


@pytest.mark.parametrize(
    "url_base",
    [
        "https://{{ config['workspace'] }}.{{ config['domain'] }}/api",
        "https://{{ config['workspace'] }}-{{ config['domain'] }}/api",
        "https://{{ config.get('workspace') }}/api",
    ],
)
def test_a_config_key_without_a_default_leaves_the_host_unknown(discovery, url_base):
    stream = _stream("channels", "conversations.list")
    stream["retriever"]["requester"]["url_base"] = url_base
    spec = _spec(domain={"default": "slack.com"})

    report = check_sandbox_support(
        SLACK_METADATA, {**_manifest(stream), "spec": spec}, discovery()
    )

    assert report.result == "unknown"


@pytest.mark.parametrize(
    "config,result",
    [
        # No case: the spec's default.
        (None, "supported"),
        # A case leaving the key out: the spec's default.
        ({"repo": "x"}, "supported"),
        ({"api_url": "https://api.github.com/"}, "supported"),
        # The host the connector would request is not the twin's.
        ({"api_url": "https://github.example.com/api/v3/"}, "unsupported"),
        # Not a value the check can know.
        ({"api_url": "${SANDBOX_CREDENTIAL}"}, "unknown"),
    ],
)
def test_a_cases_config_decides_a_hybrid_connectors_hosts(discovery, config, result):
    metadata, manifest = load_connector_files(HYBRID_DIR)

    report = check_sandbox_support(
        metadata,
        manifest,
        discovery(GITHUB_OPERATIONS),
        streams=["issues"],
        config=config,
    )

    assert report.result == result


SLACK_SPEC = _spec(api_url={"default": "https://slack.com/api/"})
GET_API_URL = "{{ config.get('api_url', 'https://slack.com/api/') }}"


@pytest.mark.parametrize(
    "url_base,config,result,reason",
    [
        (GET_API_URL, {"api_url": "https://slack.com/api/"}, "supported", None),
        (
            GET_API_URL,
            {"api_url": "https://files.example.com/api/"},
            "unsupported",
            "host files.example.com is not served by the twin",
        ),
        # A key the case leaves out: the connector takes the manifest's
        # fallback. The CDK fills in no spec defaults, so without a fallback
        # the host is unknown.
        (GET_API_URL, {}, "supported", None),
        ("{{ config['api_url'] }}", {}, "unknown", "has no static host"),
        # A placeholder, or a value the gate cannot read statically.
        (GET_API_URL, {"api_url": "{{ secret }}"}, "unknown", "has no static host"),
        (
            GET_API_URL,
            {"api_url": {"url": "https://slack.com/api/"}},
            "unknown",
            "has no static host",
        ),
    ],
)
def test_a_url_base_read_from_config_uses_the_cases_value(
    discovery, url_base, config, result, reason
):
    stream = _stream("channels", "conversations.list")
    stream["retriever"]["requester"]["url_base"] = url_base

    report = check_sandbox_support(
        SLACK_METADATA,
        {**_manifest(stream), "spec": SLACK_SPEC},
        discovery(),
        config=config,
    )

    assert report.result == result
    if reason is not None:
        assert any(reason in text for text in report.reasons)


@pytest.mark.parametrize(
    "config,result",
    [
        # Without a case any workspace label may be the twin's.
        (None, "supported"),
        ({"workspace": "acme"}, "supported"),
        ({"workspace": "other"}, "unsupported"),
        ({"workspace": "${SANDBOX_CREDENTIAL}"}, "unknown"),
        ({}, "unknown"),
        # A value that would also move the request path or add userinfo.
        ({"workspace": "acme.slack.com/x"}, "unknown"),
        ({"workspace": "user@acme"}, "unknown"),
    ],
)
def test_a_templated_host_label_uses_the_cases_value(discovery, config, result):
    stream = _stream("users", "conversations.list")
    stream["retriever"]["requester"]["url_base"] = (
        "https://{{ config['workspace'] }}.slack.com/api/"
    )
    # Without a case the label is not read from the spec's default either.
    stream = {**_manifest(stream), "spec": _spec(workspace={"default": "other"})}
    providers = {"providers": [{"id": "slack", "hosts": ["acme.slack.com"]}]}

    report = check_sandbox_support(
        {"data": {"allowedHosts": {"hosts": ["*.slack.com"]}}},
        stream,
        discovery({"providers": providers}),
        config=config,
    )

    assert report.result == result


def test_a_templated_token_endpoint_host_uses_the_cases_value(discovery):
    stream = _stream(
        "users",
        "conversations.list",
        authenticator=_oauth(
            "https://{{ config['workspace'] }}.slack.com/api/oauth.v2.access"
        ),
    )
    stream["retriever"]["requester"]["url_base"] = (
        "https://{{ config['workspace'] }}.slack.com/api/"
    )
    providers = {"providers": [{"id": "slack", "hosts": ["acme.slack.com"]}]}

    report = check_sandbox_support(
        {"data": {"allowedHosts": {"hosts": ["*.slack.com"]}}},
        _manifest(stream),
        discovery({"providers": providers, **_slack_operations(_token_operation())}),
        config={"workspace": "acme"},
    )

    assert report.result == "supported"
    assert {need.host for need in report.operations} == {"acme.slack.com"}


@pytest.mark.parametrize(
    "url_base",
    [
        "{{ 'https://slack.com/api/' if not config else 'https://other.example.com/api/' }}",
        "{{ 'https://slack.com/api/' if config|length < 2 else 'https://other.example.com/api/' }}",
        "{{ 'https://slack.com/api/' if config.items()|list else 'https://other.example.com/api/' }}",
    ],
)
@pytest.mark.parametrize("config", [None, {"start_date": "2023-10-01"}])
def test_a_url_base_reading_the_whole_config_is_unknown(discovery, url_base, config):
    stream = _stream("channels", "conversations.list")
    stream["retriever"]["requester"]["url_base"] = url_base

    report = check_sandbox_support(
        SLACK_METADATA, _manifest(stream), discovery(), config=config
    )

    assert report.result == "unknown"
    assert any("has no static host" in reason for reason in report.reasons)
