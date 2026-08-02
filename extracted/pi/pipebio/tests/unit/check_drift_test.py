"""Unit tests for scripts/check_drift.py."""

import ast
import importlib.util
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "openapi-sample.json"


def _load_check_drift():
    spec = importlib.util.spec_from_file_location(
        "check_drift", REPO_ROOT / "scripts" / "check_drift.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_drift = _load_check_drift()


def test_normalize_path_strips_prefix_and_collapses_params():
    assert check_drift._normalize_path("/api/v2/entities/{entityId}") == "entities/{}"
    assert check_drift._normalize_path("entities/{id}/fields") == "entities/{}/fields"
    assert check_drift._normalize_path("/jobs?organizationId=1") == "jobs"
    assert check_drift._normalize_path("/api/v2/me") == "me"


def test_normalize_path_truncates_inline_interpolation():
    # An inline {expr} glued to segment text (an appended query string in the
    # SDK, e.g. f"sequences/import-signed-upload{query_string}") is not a path
    # parameter and must not become a spurious "{}" segment.
    assert check_drift._normalize_path("sequences/import-signed-upload{}") == "sequences/import-signed-upload"
    # A {expr} that occupies a whole segment is still a real path parameter.
    assert check_drift._normalize_path("entities/{}/_merge") == "entities/{}/_merge"
    assert check_drift._normalize_path("entities/{entityId}/_merge") == "entities/{}/_merge"


def test_extract_spec_endpoints():
    spec = json.loads(FIXTURE.read_text(encoding="utf-8"))
    endpoints = check_drift.extract_spec_endpoints(spec)
    assert ("GET", "entities/{}") in endpoints
    assert ("PATCH", "entities/{}") in endpoints
    assert ("POST", "entities") in endpoints
    assert ("DELETE", "entities") in endpoints
    assert ("GET", "me") in endpoints
    assert ("GET", "brand-new-endpoint") in endpoints


def test_extract_sdk_endpoints_resolves_known_paths():
    resolved, _unresolved = check_drift.extract_sdk_endpoints(check_drift.PACKAGE_DIR)
    # Paths built from self._url + f-strings should resolve.
    assert ("GET", "entities/{}") in resolved
    assert ("GET", "me") in resolved
    assert ("POST", "jobs") in resolved
    assert ("GET", "jobs/{}") in resolved


def test_local_vars_do_not_leak_between_methods():
    # A `path` assigned in one method must not resolve a call in a sibling
    # method that never assigned it; otherwise we would fabricate an endpoint.
    source = (
        "class Client:\n"
        "    def __init__(self):\n"
        "        self._url = 'entities'\n"
        "    def first(self):\n"
        "        path = f'{self._url}/special'\n"
        "        return self._session.get(path)\n"
        "    def second(self):\n"
        "        return self._session.get(path)\n"
    )
    visitor = check_drift._EndpointVisitor()
    visitor.visit(ast.parse(source))
    # The first method resolves to a concrete path.
    assert ("GET", "entities/special") in visitor.resolved
    # The second method's `path` is undefined there. With per-function scoping it
    # is reported unresolved; a leak would instead silently resolve it.
    assert "GET <unresolved>" in visitor.unresolved


def test_sdk_calls_are_covered_by_sample_spec_subset():
    """Every sample-spec endpoint except the unwrapped one is called by the SDK.

    This exercises the comparison direction used to flag removed/renamed
    endpoints: every (method, path) in the curated sample must exist in the SDK,
    except ``brand-new-endpoint``, which is intentionally left unwrapped to
    represent a server endpoint the SDK does not yet cover (a warning, not a
    failure).
    """
    spec = json.loads(FIXTURE.read_text(encoding="utf-8"))
    spec_endpoints = check_drift.extract_spec_endpoints(spec)
    sdk_endpoints, _ = check_drift.extract_sdk_endpoints(check_drift.PACKAGE_DIR)

    # "brand-new-endpoint" is intentionally not wrapped by the SDK (warning case).
    not_wrapped = {ep for ep in spec_endpoints if ep not in sdk_endpoints}
    assert ("GET", "brand-new-endpoint") in not_wrapped

    # Every other sample endpoint is wrapped by the SDK.
    expected_wrapped = spec_endpoints - {("GET", "brand-new-endpoint")}
    assert expected_wrapped <= sdk_endpoints
