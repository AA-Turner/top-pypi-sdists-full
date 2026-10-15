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
