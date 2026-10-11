"""
Negative tests: REST failures surface correctly from thin SDK wrappers.

- Most modules pass through ``HttpError`` from ``intapp_rest_client``.
- Methods decorated with ``@with_error_handling`` (e.g. template reports, schema
  ``get_objects``) map ``HttpError`` to ``DealCloud*Error`` subclasses.
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.backups.dealcloud_backups import DealCloudBackups
from dealcloud_sdk.dealcloud import DealCloud
from dealcloud_sdk.history.dealcloud_history import DealCloudHistory
from dealcloud_sdk.merge.dealcloud_merge import DealCloudMerge
from dealcloud_sdk.publications.dealcloud_publications import DealCloudPublications
from dealcloud_sdk.relationshipintelligence.dealcloud_ri import DealCloudRelationshipIntelligence
from dealcloud_sdk.reports.dealcloud_reports import DealCloudReports
from dealcloud_sdk.schema.dealcloud_schema import DealCloudSchema
from dealcloud_sdk.usermanagement.dealcloud_usermanagement import DealCloudUserManagement
from dealcloud_sdk.utils.process_response_errors import (
    DealCloudApiError,
    DealCloudAuthError,
    DealCloudRateLimitError,
    DealCloudValidationError,
    handle_http_error,
    transform_http_error,
)

SITE = "test.dealcloud.com"
CREDS = {"site_url": SITE, "client_id": "cid", "client_secret": "sec"}


def _http_error(
    status: int,
    *,
    body: dict | None = None,
    headers: dict | None = None,
) -> HttpError:
    return HttpError(
        status,
        "request failed",
        body if body is not None else {"message": "error"},
        headers or {},
    )


# ---------------------------------------------------------------------------
# Backups, merge, publications, history, RI, user mgmt — raw HttpError
# ---------------------------------------------------------------------------


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestBackupsHttpErrors:
    def test_request_backup_post_http_error(self, mock_class):
        err = _http_error(400, body={"message": "backup refused"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post_no_retry429.side_effect = err
        mock_class.return_value = inner

        b = DealCloudBackups(**CREDS)
        with pytest.raises(HttpError) as ei:
            b.request_backup(api_names=["Company"])
        assert ei.value.status_code == 400
        assert ei.value.response_body == {"message": "backup refused"}

    def test_list_backups_get_http_error(self, mock_class):
        err = _http_error(503)
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.get.side_effect = err
        mock_class.return_value = inner

        b = DealCloudBackups(**CREDS)
        with pytest.raises(HttpError) as ei:
            b.list_backups()
        assert ei.value.status_code == 503

    def test_download_backup_download_file_http_error(self, mock_class, tmp_path):
        err = _http_error(500, body={"error": "download failed"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.get.return_value = {
            "model": [{"name": "b.zip", "link": "https://blob.example.com/x?sas=1"}],
        }
        inner.download_file.side_effect = err
        mock_class.return_value = inner

        b = DealCloudBackups(**CREDS)
        out = tmp_path / "x.zip"
        with pytest.raises(HttpError) as ei:
            b.download_backup(str(out), file_name="b.zip")
        assert ei.value.status_code == 500

    def test_delete_backup_post_http_error(self, mock_class):
        err = _http_error(404, body={"message": "no such backup"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        b = DealCloudBackups(**CREDS)
        with pytest.raises(HttpError) as ei:
            b.delete_backup("missing.zip")
        assert ei.value.status_code == 404


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestMergeHttpErrors:
    def test_merge_entries_post_http_error(self, mock_class):
        err = _http_error(409, body={"message": "merge conflict"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        m = DealCloudMerge(**CREDS)
        with pytest.raises(HttpError) as ei:
            m.merge_entries("Company", 1, [2])
        assert ei.value.status_code == 409


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestPublicationsHttpErrors:
    def test_get_topics_get_http_error(self, mock_class):
        err = _http_error(401)
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.get.side_effect = err
        mock_class.return_value = inner

        p = DealCloudPublications(**CREDS)
        with pytest.raises(HttpError) as ei:
            p.get_topics()
        assert ei.value.status_code == 401

    def test_poll_events_post_http_error(self, mock_class):
        err = _http_error(429, headers={"Retry-After": "30"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        p = DealCloudPublications(**CREDS)
        with pytest.raises(HttpError) as ei:
            p.poll_events(topics=["data"], time_out_ms=30_000)
        assert ei.value.status_code == 429

    def test_acknowledge_topic_offsets_post_http_error(self, mock_class):
        err = _http_error(400)
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        p = DealCloudPublications(**CREDS)
        with pytest.raises(HttpError) as ei:
            p.acknowledge_topic_offsets([{"name": "data", "offset": 1}])
        assert ei.value.status_code == 400

    def test_init_bootstrap_post_http_error(self, mock_class):
        err = _http_error(403, body={"message": "forbidden"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        p = DealCloudPublications(**CREDS)
        with pytest.raises(HttpError) as ei:
            p.init_bootstrap(entity_type=1, entity_format=0)
        assert ei.value.status_code == 403


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestHistoryHttpErrors:
    def test_get_history_get_http_error(self, mock_class):
        err = _http_error(502)
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.get.side_effect = err
        mock_class.return_value = inner

        h = DealCloudHistory(**CREDS)
        with pytest.raises(HttpError) as ei:
            h.get_history("Company", modified_since=datetime(2024, 1, 1))
        assert ei.value.status_code == 502

    def test_get_historical_data_post_http_error(self, mock_class):
        err = _http_error(400, body={"message": "bad window"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        h = DealCloudHistory(**CREDS)
        with pytest.raises(HttpError) as ei:
            h.get_historical_data("Company", [1], as_of_date=datetime(2024, 6, 1))
        assert ei.value.status_code == 400


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestRelationshipIntelligenceHttpErrors:
    def test_import_emails_post_http_error(self, mock_class):
        err = _http_error(422, body={"message": "invalid payload"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        ri = DealCloudRelationshipIntelligence(**CREDS)
        with pytest.raises(HttpError) as ei:
            ri.import_emails([])
        assert ei.value.status_code == 422


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestUserManagementHttpErrors:
    def test_create_user_post_http_error(self, mock_class):
        err = _http_error(400, body={"message": "email taken"})
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.post.side_effect = err
        mock_class.return_value = inner

        u = DealCloudUserManagement(**CREDS)
        with pytest.raises(HttpError) as ei:
            u.create_user("a@b.com", "A", "B")
        assert ei.value.status_code == 400


@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
class TestDealCloudFacadeHttpErrors:
    """Top-level DealCloud inherits backups + everything else."""

    def test_list_backups_on_dealcloud_client(self, mock_class):
        err = _http_error(500)
        inner = MagicMock()
        inner._get_auth_headers_sync.return_value = {}
        inner.get.side_effect = err
        mock_class.return_value = inner

        # DealCloud.__init__ loads schema via get_schema() unless skipped — avoid extra GETs.
        with patch.object(DealCloud, "get_schema", return_value=MagicMock()):
            dc = DealCloud(**CREDS)
        with pytest.raises(HttpError) as ei:
            dc.list_backups()
        assert ei.value.status_code == 500


# ---------------------------------------------------------------------------
# @with_error_handling — HttpError mapped to DealCloud*Error
# ---------------------------------------------------------------------------


def _reports_invoke(r: DealCloudReports, which: str) -> None:
    if which == "get_report_templates":
        r.get_report_templates()
    elif which == "generate_report":
        r.generate_report(template_id=99)
    elif which == "get_report_status":
        r.get_report_status("550e8400-e29b-41d4-a716-446655440000")
    else:  # pragma: no cover
        raise AssertionError(which)


@pytest.mark.parametrize(
    "which,status,exc_type",
    [
        ("get_report_templates", 400, DealCloudValidationError),
        ("get_report_templates", 401, DealCloudAuthError),
        ("get_report_templates", 403, DealCloudAuthError),
        ("get_report_templates", 404, DealCloudApiError),
        ("get_report_templates", 429, DealCloudRateLimitError),
        ("get_report_templates", 500, DealCloudApiError),
        ("generate_report", 400, DealCloudValidationError),
        ("generate_report", 401, DealCloudAuthError),
        ("generate_report", 404, DealCloudApiError),
        ("generate_report", 429, DealCloudRateLimitError),
        ("get_report_status", 403, DealCloudAuthError),
        ("get_report_status", 404, DealCloudApiError),
        ("get_report_status", 429, DealCloudRateLimitError),
        ("get_report_status", 502, DealCloudApiError),
    ],
    ids=[
        "get_report_templates_400",
        "get_report_templates_401",
        "get_report_templates_403",
        "get_report_templates_404",
        "get_report_templates_429",
        "get_report_templates_500",
        "generate_report_400",
        "generate_report_401",
        "generate_report_404",
        "generate_report_429",
        "get_report_status_403",
        "get_report_status_404",
        "get_report_status_429",
        "get_report_status_502",
    ],
)
@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
def test_reports_with_error_handling_maps_status(
    mock_class, which: str, status: int, exc_type: type[Exception]
):
    headers = {"Retry-After": "15"} if status == 429 else {}
    err = _http_error(status, body={"message": "x"}, headers=headers)
    inner = MagicMock()
    inner._get_auth_headers_sync.return_value = {}
    inner.get.side_effect = err
    inner.post.side_effect = err
    mock_class.return_value = inner

    r = DealCloudReports(**CREDS)
    with pytest.raises(exc_type) as ei:
        _reports_invoke(r, which)
    assert ei.value.status_code == status
    if status == 429:
        assert ei.value.retry_after == 15


@pytest.mark.parametrize(
    "status,exc_type",
    [
        (400, DealCloudValidationError),
        (401, DealCloudAuthError),
        (403, DealCloudAuthError),
        (404, DealCloudApiError),
        (429, DealCloudRateLimitError),
        (500, DealCloudApiError),
    ],
    ids=[
        "get_objects_400",
        "get_objects_401",
        "get_objects_403",
        "get_objects_404",
        "get_objects_429",
        "get_objects_500",
    ],
)
@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
def test_get_objects_with_error_handling_maps_status(
    mock_class, status: int, exc_type: type[Exception]
):
    headers = {"Retry-After": "7"} if status == 429 else {}
    err = _http_error(status, body={"message": "schema"}, headers=headers)
    inner = MagicMock()
    inner._get_auth_headers_sync.return_value = {}
    inner.get.side_effect = err
    mock_class.return_value = inner

    s = DealCloudSchema(**CREDS)
    with pytest.raises(exc_type) as ei:
        s.get_objects()
    assert ei.value.status_code == status
    if status == 429:
        assert ei.value.retry_after == 7


@pytest.mark.parametrize(
    "status,exc_type",
    [
        (400, DealCloudValidationError),
        (401, DealCloudAuthError),
        (404, DealCloudApiError),
        (429, DealCloudRateLimitError),
        (503, DealCloudApiError),
    ],
    ids=[
        "get_currencies_400",
        "get_currencies_401",
        "get_currencies_404",
        "get_currencies_429",
        "get_currencies_503",
    ],
)
@patch("dealcloud_sdk.base.dealcloud_base.RestClient")
def test_get_currencies_with_error_handling_maps_status(
    mock_class, status: int, exc_type: type[Exception]
):
    headers = {"Retry-After": "3"} if status == 429 else {}
    err = _http_error(status, body={"message": "curr"}, headers=headers)
    inner = MagicMock()
    inner._get_auth_headers_sync.return_value = {}
    inner.get.side_effect = err
    mock_class.return_value = inner

    s = DealCloudSchema(**CREDS)
    with pytest.raises(exc_type) as ei:
        s.get_currencies()
    assert ei.value.status_code == status
    if status == 429:
        assert ei.value.retry_after == 3


class TestTransformHttpErrorEdges:
    """Direct coverage for ``transform_http_error`` / ``handle_http_error``."""

    def test_rate_limit_without_retry_after(self):
        with pytest.raises(DealCloudRateLimitError) as ei:
            handle_http_error(429, {"message": "slow"}, {})
        assert ei.value.retry_after is None

    def test_rate_limit_retry_after_lowercase_header(self):
        with pytest.raises(DealCloudRateLimitError) as ei:
            handle_http_error(429, {}, {"retry-after": "99"})
        assert ei.value.retry_after == 99

    def test_validation_error_uses_nested_errors_array(self):
        body = {
            "message": "root",
            "errors": [{"message": "e1", "errorCode": "C1"}],
        }
        with pytest.raises(DealCloudValidationError) as ei:
            handle_http_error(400, body, {})
        assert "e1" in str(ei.value)
        assert ei.value.status_code == 400

    def test_transform_http_error_from_intapp(self):
        err = HttpError(
            403,
            "nope",
            {"message": "denied"},
            {"X-Request-ID": "abc"},
        )
        with pytest.raises(DealCloudAuthError):
            transform_http_error(err)
