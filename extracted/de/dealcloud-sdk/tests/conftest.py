"""
Shared fixtures and configuration for DealCloud SDK tests.

This conftest.py provides:
- Custom pytest markers for test categorization
- Shared fixtures for mocked unit tests
- Integration test fixtures (require API access)
- Sample data fixtures

Integration tests:
    Apply ``@pytest.mark.integration`` on a class or test function (typical pattern under
    ``tests/integration/``). Optionally use module-level
    ``pytestmark = [pytest.mark.integration, ...]`` when **every** test in the file shares
    the same markers. Both are equivalent for ``--run-integration`` and for static analysis
    that looks for the marker.

Tests require the **pinned** ``intapp-rest-client`` from ``pyproject.toml`` (including
``ErrorHandling`` in ``intapp_rest_client.models``). There is no fallback: a wrong or
incomplete client install fails on ``import dealcloud_sdk`` or collection—fix the
environment or the pin instead of masking import errors.
"""

# Load .env from project root so integration tests can use DC_* without exporting
try:
    from pathlib import Path
    from dotenv import load_dotenv
    _root = Path(__file__).resolve().parent.parent
    load_dotenv(_root / ".env")
except ImportError:
    pass  # python-dotenv not installed; rely on environment only

import json
import os
import pytest
from unittest.mock import MagicMock, patch


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "integration: integration tests (API or mocked HTTP); use class/method decorator or "
        "module-level pytestmark (see conftest module docstring)",
    )
    config.addinivalue_line(
        "markers", "integration_429: 429 / rate-limit integration tests (respx-mocked)"
    )
    config.addinivalue_line(
        "markers", "integration_auth: authentication integration tests"
    )
    config.addinivalue_line(
        "markers",
        "integration_token_refresh: OAuth2 proactive token refresh (live token endpoint; ~1 min)",
    )
    config.addinivalue_line(
        "markers",
        "integration_token_refresh_long: manual-only ~40m+ OAuth2 refresh; excluded from test-integration and test-live",
    )
    config.addinivalue_line(
        "markers", "integration_cells: cells API integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_data: data (rows, read/write/delete, pagination) integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_history: history API integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_schema: schema API integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_usermanagement: user management integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_relationshipintelligence: Relationship Intelligence (RI) integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_backups: site backups API integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_publications: publications API integration tests"
    )
    config.addinivalue_line(
        "markers",
        "integration_publications_init_bootstrap: optional manual init_bootstrap matrix (not run with integration_publications)",
    )
    config.addinivalue_line(
        "markers", "integration_merge: merge API integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_polars: Polars output integration tests"
    )
    config.addinivalue_line(
        "markers", "integration_excel: Excel utilities integration tests (API data + export/read)"
    )
    config.addinivalue_line(
        "markers", "integration_files: files API integration tests (upload/download/delete, find file fields)"
    )
    config.addinivalue_line(
        "markers", "integration_reports: template reports API integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )

    config.addinivalue_line(
        "markers",
        "integration_negative: negative-path integration tests (errors, HttpError); "
        "optional filter: pytest --run-integration -m integration_negative",
    )
    config.addinivalue_line(
        "markers",
        "integration_negative_http: Phase 1 negative tests (HTTP 4xx/5xx or client validation)",
    )
    config.addinivalue_line(
        "markers",
        "integration_negative_body: Phase 2 negative tests (HTTP 2xx with body-level failures)",
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests from original SDK"
    )


def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless --run-integration is passed.

    Module-level ``pytestmark = [pytest.mark.integration, ...]`` applies the marker to each
    collected test in that module, so those tests are skipped here the same as decorated tests.
    """
    if not config.getoption("--run-integration", default=False):
        skip_integration = pytest.mark.skip(reason="need --run-integration option to run")
        for item in items:
            # Exact marker only — substrings like integration_negative_http are not skipped here.
            if item.get_closest_marker("integration"):
                item.add_marker(skip_integration)


def pytest_addoption(parser):
    """Add command line options."""
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests (requires API access)"
    )
    parser.addoption(
        "--run-doc-example-execute",
        action="store_true",
        default=False,
        help=(
            "run Tier2 subprocess execution for runnable doc examples from api-doc "
            "(may call network; use with care)"
        ),
    )


# =============================================================================
# SAMPLE DATA FIXTURES (for unit tests)
# =============================================================================

@pytest.fixture
def sample_objects():
    """Sample objects response from API."""
    return [
        {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
        {"apiName": "Contact", "singularName": "Contact", "pluralName": "Contacts", "id": 2, "entryListId": 200},
        {"apiName": "Deal", "singularName": "Deal", "pluralName": "Deals", "id": 3, "entryListId": 300},
        {"apiName": "PythonSDKTestObject", "singularName": "SDK Test Object", "pluralName": "SDK Test Objects", "id": 4, "entryListId": 400},
    ]


@pytest.fixture
def sample_fields():
    """Sample fields response from API."""
    return [
        {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        {"apiName": "Status", "name": "Status", "fieldType": 2, "id": 11, "entryListId": 100,
         "choiceValues": [{"name": "Active", "id": 1}, {"name": "Inactive", "id": 2}]},
        {"apiName": "Revenue", "name": "Revenue", "fieldType": 4, "id": 12, "entryListId": 100},
        {"apiName": "PrimaryContact", "name": "Primary Contact", "fieldType": 6, "id": 13, "entryListId": 100},
        # PythonSDKTestObject fields
        {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 40, "entryListId": 400},
        {"apiName": "TEST_TEXT", "name": "Test Text", "fieldType": 1, "id": 41, "entryListId": 400},
        {"apiName": "TEST_CHOICE", "name": "Test Choice", "fieldType": 2, "id": 42, "entryListId": 400,
         "choiceValues": [{"name": "CHOICE1", "id": 101}, {"name": "CHOICE2", "id": 102}]},
        {"apiName": "TEST_NUMBER", "name": "Test Number", "fieldType": 4, "id": 43, "entryListId": 400},
    ]


@pytest.fixture
def sample_users():
    """Sample users response from API."""
    return [
        {"id": 1, "name": "John Doe", "email": "john.doe@gmail.co", "entryListId": 500},
        {"id": 2, "name": "Jane Smith", "email": "jane.smith@gmail.co", "entryListId": 500},
    ]


@pytest.fixture
def sample_rows():
    """Sample rows response from API."""
    return {
        "totalRecords": 3,
        "rows": [
            {"EntryId": 101, "Name": "Company A", "Status": [1]},
            {"EntryId": 102, "Name": "Company B", "Status": [2]},
            {"EntryId": 103, "Name": "Company C", "Status": [1]},
        ]
    }


@pytest.fixture
def sample_rows_empty():
    """Empty rows response for pagination end."""
    return {"totalRecords": 0, "rows": []}


# =============================================================================
# MOCK FIXTURES (for unit tests)
# =============================================================================

@pytest.fixture
def mock_rest_client():
    """Create a mocked RestClient that doesn't make real HTTP calls."""
    with patch('dealcloud_sdk.base.dealcloud_base.RestClient') as MockClient:
        mock_instance = MagicMock()
        mock_instance._get_auth_headers_sync.return_value = {"Authorization": "Bearer test_token"}
        mock_instance._client = MagicMock()
        MockClient.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_dealcloud(mock_rest_client, sample_objects, sample_fields, sample_users):
    """
    Pre-configured DealCloud instance with mocked client.
    
    Use this for unit tests that don't need real API access.
    """
    from dealcloud_sdk import DealCloud
    
    def get_side_effect(url):
        if "entryTypes" in url:
            return sample_objects
        elif "allfields" in url or "/fields" in url:
            return sample_fields
        elif "users" in url:
            return sample_users
        return {}
    
    mock_rest_client.get.side_effect = get_side_effect
    
    dc = DealCloud(
        site_url="test.dealcloud.com",
        client_id="12345",
        client_secret="secret123"
    )
    
    # Reset mocks after init so tests can configure their own responses
    mock_rest_client.reset_mock()
    
    return dc


# =============================================================================
# TEMP FILE FIXTURES
# =============================================================================

@pytest.fixture
def temp_json_config(tmp_path):
    """Create a temporary JSON config file."""
    config = {
        "siteUrl": "test.dealcloud.com",
        "clientId": "12345",
        "clientSecret": "secret123",
    }
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    return str(path)


@pytest.fixture
def temp_yaml_config(tmp_path):
    """Create a temporary YAML config file."""
    try:
        import yaml
        config = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret123",
        }
        path = tmp_path / "config.yaml"
        path.write_text(yaml.dump(config))
        return str(path)
    except ImportError:
        pytest.skip("PyYAML not installed")


# =============================================================================
# INTEGRATION TEST FIXTURES
# =============================================================================

@pytest.fixture(scope="session")
def integration_credentials():
    """
    Load integration test credentials from environment variables.
    
    Required environment variables:
    - DC_SITE_URL: DealCloud site URL (e.g., "client.dealcloud.com")
    - DC_CLIENT_ID: API client ID
    - DC_API_KEY: API client secret/key
    
    Optional:
    - DC_TEST_OBJECT: Test object API name (default: "PythonSDKTestObject")

    Some suites use dedicated clients with extra OAuth scopes (e.g. publications request
    ``publish``; backups request ``backup``; RI requests ``ri_import``). The API client must
    allow those scopes.
    """
    site_url = os.getenv("DC_SITE_URL")
    client_id = os.getenv("DC_CLIENT_ID")
    client_secret = os.getenv("DC_API_KEY")
    
    if not all([site_url, client_id, client_secret]):
        pytest.fail(
            "Integration test credentials not configured. "
            "Set DC_SITE_URL, DC_CLIENT_ID, and DC_API_KEY environment variables."
        )

    from dealcloud_sdk.factories.from_env import normalize_site_url
    site_url = normalize_site_url(site_url)

    return {
        "site_url": site_url,
        "client_id": client_id,
        "client_secret": client_secret,
        "test_object": os.getenv("DC_TEST_OBJECT", "PythonSDKTestObject"),
    }


@pytest.fixture(scope="session")
def dc_integration(integration_credentials):
    """
    Create a DealCloud instance for integration tests via DealCloud.from_env().

    Uses DC_SITE_URL, DC_CLIENT_ID, DC_API_KEY from the environment (same as
    integration_credentials). Session-scoped so the same connection is reused.
    """
    from dealcloud_sdk import DealCloud

    dc = DealCloud.from_env()

    yield dc

    # Cleanup: close connection
    dc.close()


# Scope required for Relationship Intelligence API (https://api.docs.dealcloud.com/docs/token).
RI_IMPORT_SCOPE = ("data", "user_management", "ri_import")

# Publications / event-streaming API (https://api.docs.dealcloud.com/docs/token).
PUBLICATIONS_SCOPE = ("data", "user_management", "publish")

# Site backups API (https://api.docs.dealcloud.com/docs/token).
BACKUPS_SCOPE = ("data", "user_management", "backup")


@pytest.fixture(scope="session")
def dc_integration_publications(integration_credentials):
    """
    DealCloud client for publications integration tests.

    Same credentials as dc_integration but requests OAuth scope ``publish`` so
    publication endpoints (topics, poll, acknowledge) are authorized.
    """
    from dealcloud_sdk import DealCloud

    creds = integration_credentials
    dc = DealCloud(
        site_url=creds["site_url"],
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        scope=PUBLICATIONS_SCOPE,
    )
    yield dc
    dc.close()


@pytest.fixture(scope="session")
def dc_integration_backups(integration_credentials):
    """
    DealCloud client for site backups integration tests.

    Same credentials as dc_integration but requests OAuth scope ``backup`` so
    backup endpoints (list, request, download, delete) are authorized.
    """
    from dealcloud_sdk import DealCloud

    creds = integration_credentials
    dc = DealCloud(
        site_url=creds["site_url"],
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        scope=BACKUPS_SCOPE,
    )
    yield dc
    dc.close()


@pytest.fixture(scope="session")
def dc_integration_ri(integration_credentials):
    """
    DealCloud client for Relationship Intelligence integration tests.

    Same credentials as dc_integration but with scope including ri_import so
    RI endpoints (e.g. GET /api/rest/v4/ri/import/settings) are authorized.
    """
    from dealcloud_sdk import DealCloud

    creds = integration_credentials
    dc = DealCloud(
        site_url=creds["site_url"],
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        scope=RI_IMPORT_SCOPE,
    )
    yield dc
    dc.close()


@pytest.fixture
def test_object_name(integration_credentials, dc_integration):
    """
    Get the test object API name (DC_TEST_OBJECT).
    Validates that the object exists on the site; fails with a clear message if not (avoids 35
    "entryTypeId is not valid" failures and surfaces the root cause).
    """
    name = integration_credentials["test_object"]
    objects = dc_integration.get_objects()
    api_names = [getattr(o, "apiName", None) for o in objects]
    if name not in api_names:
        pytest.fail(
            f"Test object '{name}' (DC_TEST_OBJECT) is not an entry type on this site. "
            "Create the entry type in DealCloud or set DC_TEST_OBJECT to an existing object apiName."
        )
    return name


# -----------------------------------------------------------------------------
# User management integration test data (5 permanent users; groups from site)
# -----------------------------------------------------------------------------

@pytest.fixture(scope="session")
def usermanagement_permanent_data(dc_integration):
    """
    Ensure five permanent test users exist (create if missing). Groups are not
    created via API: fixture lists SDK-named groups if present, else up to five
    existing named groups on the site. Nothing is deleted in tests.
    Returns {"users": [...], "groups": [...]}.
    """
    from tests.integration.usermanagement_test_data import ensure_permanent_test_data
    return ensure_permanent_test_data(dc_integration)


@pytest.fixture
def usermanagement_generator():
    """
    Generator for unique user and group specs in create tests.
    Yields specs so tests can create via API then verify with get calls.
    """
    from tests.integration.usermanagement_test_data import UserManagementTestDataGenerator
    return UserManagementTestDataGenerator()

