from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field
import json
import time

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.matchers import path_type
from syrupy.types import PropertyMatcher, PropertyPath, SerializableData
from testcontainers.generic.server import ServerContainer
from conftest import local_path


@pytest.mark.parametrize("endpoint", ["/clock/", "/sleep/"])
def test_system_commands(
    observe_django_app: ServerContainer,
    snapshot_json: SnapshotAssertion,
    endpoint: str,
):
    client = observe_django_app.get_client()

    response = client.get(endpoint)
    assert response.status_code == 200, "Failed to connect to Django app"

    trace = find_trace_for_path(endpoint)
    assert_trace_snapshot(snapshot_json, trace)


def test_file_opens_write(
    observe_django_app: ServerContainer, snapshot_json: SnapshotAssertion
):
    client = observe_django_app.get_client()

    post_name = "test_post.txt"
    post_content = "This is a test post."
    create_response = client.post(f"/posts/{post_name}/", content=post_content)
    assert create_response.status_code == 200

    trace = find_trace_for_path(f"/posts/{post_name}/")
    assert_trace_snapshot(snapshot_json, trace)


def test_file_opens_read(
    observe_django_app: ServerContainer, snapshot_json: SnapshotAssertion
):
    client = observe_django_app.get_client()

    retrieve_response = client.get("/posts/example.txt/")
    assert retrieve_response.status_code == 200

    trace = find_trace_for_path("/posts/example.txt/")
    assert_trace_snapshot(snapshot_json, trace)


def test_file_opens_list(
    observe_django_app: ServerContainer, snapshot_json: SnapshotAssertion
):
    client = observe_django_app.get_client()

    list_response = client.get("/posts/")
    assert list_response.status_code == 200

    # Listing a directoy doesn't open any files, so there shouldn't be
    # any file-open-create spans.
    trace = find_trace_for_path("/posts/")
    assert_trace_snapshot(snapshot_json, trace)


def test_storage_query(
    observe_django_app: ServerContainer, snapshot_json: SnapshotAssertion
):
    client = observe_django_app.get_client()

    # Create a new message
    msg_text = "Hello, database!"
    create_response = client.post(
        "/messages/",
        content=json.dumps({"text": msg_text}),
        headers={"Content-Type": "application/json"},
    )
    assert create_response.status_code == 201, create_response.content

    # Query all messages
    list_response = client.get("/messages/")
    assert list_response.status_code == 200

    trace = find_trace_for_path("/messages/")
    assert_trace_snapshot(snapshot_json, trace)


def assert_trace_snapshot(snapshot_json: SnapshotAssertion, trace: dict):
    assert (
        snapshot_json(
            matcher=multi_matcher(
                attributes_sorter,
                attribute_stabilizer("service.instance.id"),
                attribute_stabilizer("service.name"),  # includes agent version
                path_type(
                    {
                        r"resourceSpans.\d+.scopeSpans.\d+.spans.\d+.startTimeUnixNano": (
                            str,
                        ),
                        r"resourceSpans.\d+.scopeSpans.\d+.spans.\d+.endTimeUnixNano": (
                            str,
                        ),
                        r"resourceSpans.\d+.scopeSpans.\d+.scope.version": (str,),
                    },
                    regex=True,
                ),
                TraceSpanIDsMatcher(),
            )
        )
        == trace
    )


def attributes_sorter(data: SerializableData, path: PropertyPath) -> SerializableData:
    """
    A syrupy matcher that sorts the attributes dictionary by key.
    This is useful for ensuring consistent snapshots when the order of attributes
    may vary between runs.
    """
    if path and path[-1] == ("attributes", list):
        return list(sorted(data, key=lambda item: item["key"]))

    return data


def attribute_stabilizer(attr_name: str) -> PropertyMatcher:
    """
    Creates a syrupy matcher that replaces the named attribute if it matches the expected type.
    """

    def replacer(data: SerializableData, path: PropertyPath) -> SerializableData:
        if len(path) >= 2 and path[-1] == ("attributes", list):

            def replaced_data(key, value):
                if key == attr_name:
                    return {"key": key, "value": {"stringValue": f"<stable-{key}>"}}
                else:
                    return {"key": key, "value": value}

            return [replaced_data(kv["key"], kv["value"]) for kv in data]
        return data

    return replacer


@dataclass
class TraceSpanIDsMatcher:
    """
    A matcher that normalizes trace and span IDs in the data.

    OTel trace and span IDs are unique identifiers that aren't stable across runs.
    This matcher replaces them with a stable string representation based on their
    order of appearance in the data. This allows for consistent snapshots without
    losing the uniqueness of the IDs.

    If the order of spans or traces changes, the backend may still be able to render
    the trace correctly, but this matcher will fail. This is taking the simple approach
    first, and we can improve it later if needed.
    """

    trace_ids: dict[str, str] = field(default_factory=dict)
    span_ids: dict[str, str] = field(default_factory=dict)

    def __call__(self, data: SerializableData, path: PropertyPath) -> SerializableData:
        if not path:
            return data

        if path[-1] == ("traceId", str):
            bucket = self.trace_ids
        elif path[-1] in [("spanId", str), ("parentSpanId", str)]:
            bucket = self.span_ids
        else:
            return data

        if data in bucket:
            return bucket[data]
        elif path[-1] == ("parentSpanId", str) and data == "":
            return data  # Keep empty parentSpanId as is
        else:
            normalized_id = bucket[data] = str(len(bucket))
            return normalized_id


def multi_matcher(*matchers: PropertyMatcher) -> PropertyMatcher:
    """
    Combines multiple matchers into a single matcher.
    """

    def combined_replacer(
        data: SerializableData, path: PropertyPath
    ) -> SerializableData:
        for matcher in matchers:
            new_data = matcher(data=data, path=path)
            if new_data is not data:
                data = new_data
        return data

    return combined_replacer


def poll_traces(timeout=10, poll_interval=1):
    """
    Generator that yields the current traces every poll_interval seconds, up to timeout seconds.
    """
    start = time.time()
    while time.time() - start < timeout:
        traces = [
            load_json_from_file(log_file)
            for log_file in local_path("logs/messages/requests").glob(
                "*-observability-traces-teamserver.json"
            )
        ]
        yield traces
        time.sleep(poll_interval)


def find_trace_for_path(path: str, timeout: int = 10) -> dict:
    """
    Search for and return the OpenTelemetry trace containing all spans for a given HTTP path.

    This function scans the proxy logs for batch trace files, searching for a span whose "url.path"
    attribute matches the provided path. Once found, it filters the trace batch to include only the
    spans that match the specified path.
    """
    for traces in poll_traces(timeout=timeout):
        (batch_trace, request_trace_ids) = find_trace_id(traces, path)
        if batch_trace and request_trace_ids:
            matching_resource_spans = []
            for resource_span in batch_trace.get("resourceSpans", []):
                matching_scope_spans = []
                for scope_span in resource_span.get("scopeSpans", []):
                    matching_spans = [
                        span
                        for span in scope_span.get("spans", [])
                        if span.get("traceId") in request_trace_ids
                    ]
                    if matching_spans:
                        scope_span_copy = copy(scope_span)
                        scope_span_copy["spans"] = matching_spans
                        matching_scope_spans.append(scope_span_copy)
                if matching_scope_spans:
                    resource_span_copy = copy(resource_span)
                    resource_span_copy["scopeSpans"] = matching_scope_spans
                    matching_resource_spans.append(resource_span_copy)
            batch_trace_copy = copy(batch_trace)
            batch_trace_copy["resourceSpans"] = matching_resource_spans
            return batch_trace_copy

    raise TimeoutError(
        f"No observe trace requests found for path '{path}' within the {timeout} seconds."
    )


def find_trace_id(batch_traces, path):
    """
    Find all trace IDs for the given path in the traces.
    Returns the first matching batch_trace and a list of all matching trace IDs, or (None, None) if not found.
    """
    for batch_trace in batch_traces:
        trace_ids = []
        for resource_span in batch_trace.get("resourceSpans", []):
            for scope_span in resource_span.get("scopeSpans", []):
                for span in scope_span.get("spans", []):
                    for attr in span.get("attributes", []):
                        if (
                            attr.get("key") == "url.path"
                            and attr.get("value", {}).get("stringValue") == path
                        ):
                            trace_id = span["traceId"]
                            if trace_id not in trace_ids:
                                trace_ids.append(trace_id)
        if trace_ids:
            return batch_trace, trace_ids
    return None, None


def load_json_from_file(path):
    with open(path) as f:
        return json.load(f)
