from unittest.mock import MagicMock, patch
from click.testing import CliRunner
import pytest

from agilicus import main as main_module
from agilicus.metrics_commands import metrics as metrics_module
from agilicus.metrics_commands import metrics_main
from agilicus.tests.test_main_handwritten import _cli_auth_mocks


class MockUsageMetricBucket:
    def __init__(self, **kwargs):
        self._data = kwargs
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return dict(self._data)

    def get(self, key, default=None):
        return self._data.get(key, default)


class MockUsageMetricsResponse:
    def __init__(
        self,
        data=None,
        breakdown_by=None,
        total_buckets=None,
        bucket_size="P1D",
        page_info=None,
    ):
        self.data = data or []
        self.breakdown_by = breakdown_by or []
        self.total_buckets = (
            total_buckets if total_buckets is not None else len(self.data)
        )
        self.time_from = "2026-09-15T00:00:00Z"
        self.time_to = "2026-10-15T00:00:00Z"
        self.bucket_size = bucket_size
        self.page_info = page_info

    def to_dict(self):
        return {
            "data": [b.to_dict() if hasattr(b, "to_dict") else b for b in self.data],
            "total_buckets": self.total_buckets,
            "time_from": self.time_from,
            "time_to": self.time_to,
            "bucket_size": self.bucket_size,
            "breakdown_by": self.breakdown_by,
            "page_info": (
                self.page_info.to_dict()
                if hasattr(self.page_info, "to_dict")
                else self.page_info
            ),
        }


@pytest.fixture(autouse=True)
def setup_cli_commands():
    main_module.metrics_main.add_commands(main_module.cli)


@pytest.fixture
def mock_ctx():
    ctx = MagicMock()
    ctx.obj = {
        "output_format": "console",
        "ORG_ID": "default-org-uuid",
        "ADMIN_MODE": False,
    }
    return ctx


def test_query_usage_default_org(mock_ctx):
    mock_api = MagicMock()
    mock_api.metrics_api.list_usage_metrics.return_value = MockUsageMetricsResponse()

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ), patch("agilicus.metrics.context.get_org_id", return_value="default-org-uuid"):
        res = metrics_module.query_usage(mock_ctx)

    mock_api.metrics_api.list_usage_metrics.assert_called_once_with(
        org_id="default-org-uuid",
        limit=500,
    )
    assert res.total_buckets == 0


def test_query_usage_custom_params(mock_ctx):
    mock_api = MagicMock()
    mock_api.metrics_api.list_usage_metrics.return_value = MockUsageMetricsResponse()

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ):
        metrics_module.query_usage(
            mock_ctx,
            org_id="explicit-org",
            dt_from="2026-01-01T00:00:00Z",
            dt_to="2026-06-01T00:00:00Z",
            bucket_size="P1W",
            breakdown_by=["user_id", "resource_type"],
            sort_by="access_count",
            sort_order="desc",
            limit=100,
        )

    mock_api.metrics_api.list_usage_metrics.assert_called_once_with(
        org_id="explicit-org",
        dt_from="2026-01-01T00:00:00Z",
        dt_to="2026-06-01T00:00:00Z",
        bucket_size="P1W",
        breakdown_by=["user_id", "resource_type"],
        sort_by="access_count",
        sort_order="descending",
        limit=100,
    )


def test_query_usage_all_orgs_fleetwide(mock_ctx):
    mock_api = MagicMock()
    mock_api.metrics_api.list_usage_metrics.return_value = MockUsageMetricsResponse()

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ):
        metrics_module.query_usage(
            mock_ctx,
            all_orgs=True,
            breakdown_by="org_id",
            bucket_size="P1M",
        )

    # org_id should NOT be passed for fleetwide query
    mock_api.metrics_api.list_usage_metrics.assert_called_once_with(
        bucket_size="P1M",
        breakdown_by=["org_id"],
        limit=500,
    )


def test_query_usage_org_ids_list_and_string(mock_ctx):
    mock_api = MagicMock()
    mock_api.metrics_api.list_usage_metrics.return_value = MockUsageMetricsResponse()

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ):
        metrics_module.query_usage(
            mock_ctx,
            org_ids="org-1, org-2",
        )

    mock_api.metrics_api.list_usage_metrics.assert_called_once_with(
        org_ids=["org-1", "org-2"],
        limit=500,
    )


def test_query_usage_presets(mock_ctx):
    mock_api = MagicMock()
    mock_api.metrics_api.list_usage_metrics.return_value = MockUsageMetricsResponse()

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ), patch("agilicus.metrics.context.get_org_id", return_value="default-org"):
        metrics_module.query_usage(mock_ctx, preset="user-usage")

    mock_api.metrics_api.list_usage_metrics.assert_called_once_with(
        org_id="default-org",
        breakdown_by=["user_id"],
        sort_by="access_count",
        sort_order="descending",
        limit=500,
    )


def test_query_usage_pagination_keyset(mock_ctx):
    mock_api = MagicMock()
    mock_api.metrics_api.list_usage_metrics.return_value = MockUsageMetricsResponse()

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ):
        metrics_module.query_usage(
            mock_ctx,
            org_id="org-1",
            page_on=["time", "user_id"],
            page_at_key=["2026-10-15T00:00:00Z", "u-123"],
            page_sort=["desc", "asc"],
        )

    mock_api.metrics_api.list_usage_metrics.assert_called_once_with(
        org_id="org-1",
        page_on=["time", "user_id"],
        page_at_key=["2026-10-15T00:00:00Z", "u-123"],
        page_sort=["desc", "asc"],
        limit=500,
    )


def test_query_usage_auto_paging_get_all(mock_ctx):
    mock_api = MagicMock()
    mock_iter = MagicMock()
    mock_iter.all.return_value = [
        MockUsageMetricBucket(time="2026-10-15T00:00:00Z", access_count=1),
        MockUsageMetricBucket(time="2026-10-16T00:00:00Z", access_count=2),
    ]
    mock_api.metrics_api.list_usage_metrics.auto_paging_iter.return_value = mock_iter

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ):
        res = metrics_module.query_usage(
            mock_ctx,
            org_id="org-1",
            breakdown_by=["resource_id"],
            get_all=True,
        )

    mock_api.metrics_api.list_usage_metrics.auto_paging_iter.assert_called_once_with(
        limit=None,
        page_on=["time", "resource_id"],
        org_id="org-1",
        breakdown_by=["resource_id"],
    )
    assert len(res) == 2


def test_query_usage_auto_paging_with_explicit_page_on(mock_ctx):
    mock_api = MagicMock()
    mock_iter = MagicMock()
    mock_iter.all.return_value = [
        MockUsageMetricBucket(time="2026-10-15T00:00:00Z", access_count=1),
    ]
    mock_api.metrics_api.list_usage_metrics.auto_paging_iter.return_value = mock_iter

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ):
        res = metrics_module.query_usage(
            mock_ctx,
            org_id="org-1",
            page_on=["time", "user_id"],
            get_all=True,
        )

    mock_api.metrics_api.list_usage_metrics.auto_paging_iter.assert_called_once_with(
        limit=None,
        page_on=["time", "user_id"],
        org_id="org-1",
    )
    assert len(res) == 1


def test_query_convenience_functions(mock_ctx):
    mock_api = MagicMock()
    mock_api.metrics_api.list_usage_metrics.return_value = MockUsageMetricsResponse()

    with patch("agilicus.metrics.context.get_token", return_value="tok"), patch(
        "agilicus.metrics.context.get_apiclient", return_value=mock_api
    ), patch("agilicus.metrics.context.get_org_id", return_value="default-org"):
        metrics_module.query_user_usage(mock_ctx, sort_by=None, breakdown_by=None)
        metrics_module.query_resource_usage(mock_ctx, sort_by=None, breakdown_by=None)
        metrics_module.query_adoption(mock_ctx, bucket_size=None, dt_from=None)
        metrics_module.query_fleet_usage(mock_ctx, bucket_size=None, breakdown_by=None)

    assert mock_api.metrics_api.list_usage_metrics.call_count == 4
    calls = mock_api.metrics_api.list_usage_metrics.call_args_list

    # query_user_usage defaults
    assert calls[0].kwargs["breakdown_by"] == ["user_id"]
    assert calls[0].kwargs["sort_by"] == "access_count"
    assert calls[0].kwargs["sort_order"] == "descending"

    # query_resource_usage defaults
    assert calls[1].kwargs["breakdown_by"] == ["resource_id", "resource_type"]
    assert calls[1].kwargs["sort_by"] == "access_count"
    assert calls[1].kwargs["sort_order"] == "ascending"

    # query_adoption defaults
    assert calls[2].kwargs["bucket_size"] == "P1D"
    assert calls[2].kwargs["dt_from"] == "now-30d"

    # query_fleet_usage defaults
    assert calls[3].kwargs["breakdown_by"] == ["org_id"]
    assert calls[3].kwargs["bucket_size"] == "P1M"
    assert "org_id" not in calls[3].kwargs


def test_format_usage_metrics_table_and_json(mock_ctx, capsys):
    bucket = MockUsageMetricBucket(
        time="2026-10-15T00:00:00Z",
        user_id="user-1",
        email="user1@example.com",
        access_count=100,
        unique_users=1,
        unique_resources=3,
    )
    resp = MockUsageMetricsResponse(data=[bucket], breakdown_by=["user_id"])

    # Console / PrettyTable
    table = metrics_module.format_usage_metrics(mock_ctx, resp)
    print(table)
    out = capsys.readouterr().out
    assert "user_id" in out
    assert "email" in out
    assert "user-1" in out
    assert "100" in out

    # JSON format
    mock_ctx.obj["output_format"] = "json"
    with patch("agilicus.context.output_json", return_value=True):
        out_json = metrics_module.format_usage_metrics(mock_ctx, resp)
        print(out_json)
    out = capsys.readouterr().out
    assert '"access_count": 100' in out


def test_format_usage_metrics_with_list(mock_ctx, capsys):
    buckets = [
        MockUsageMetricBucket(
            time="2026-10-15T00:00:00Z",
            resource_type="ssh",
            access_count=50,
            unique_users=2,
            unique_resources=1,
        )
    ]
    table = metrics_module.format_usage_metrics(mock_ctx, buckets)
    print(table)
    out = capsys.readouterr().out
    assert "resource_type" in out
    assert "ssh" in out
    assert "50" in out


def test_cli_get_usage_metrics_help():
    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            ["get-usage-metrics", "--help"],
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert "View aggregated usage, adoption, and access metrics" in result.output
    assert "--breakdown-by" in result.output
    assert "--bucket-size" in result.output
    assert "--all-orgs" in result.output
    assert "--preset" in result.output
    assert "--get-all" in result.output
    assert "--page-on" in result.output


def test_cli_get_usage_metrics_invocation(monkeypatch):
    calls = []
    bucket = MockUsageMetricBucket(
        time="2026-10-15T00:00:00Z",
        access_count=10,
        unique_users=2,
        unique_resources=1,
    )
    resp = MockUsageMetricsResponse(data=[bucket])

    def fake_query(ctx, **kwargs):
        calls.append(kwargs)
        return resp

    monkeypatch.setattr(metrics_module, "query_usage", fake_query)

    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            [
                "--token",
                "test-token",
                "get-usage-metrics",
                "org-abc",
                "--bucket-size",
                "PT1H",
                "--breakdown-by",
                "resource_type",
                "--get-all",
            ],
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0]["org_id"] == "org-abc"
    assert calls[0]["bucket_size"] == "PT1H"
    assert "resource_type" in calls[0]["breakdown_by"]
    assert calls[0]["get_all"] is True


def test_cli_list_usage_metrics_invocation(monkeypatch):
    calls = []
    bucket = MockUsageMetricBucket(
        time="2026-10-15T00:00:00Z",
        access_count=10,
        unique_users=2,
        unique_resources=1,
    )
    resp = MockUsageMetricsResponse(data=[bucket])

    def fake_query(ctx, **kwargs):
        calls.append(kwargs)
        return resp

    monkeypatch.setattr(metrics_module, "query_usage", fake_query)

    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            [
                "--token",
                "test-token",
                "list-usage-metrics",
                "org-abc",
                "--bucket-size",
                "PT1H",
            ],
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0]["org_id"] == "org-abc"
    assert calls[0]["bucket_size"] == "PT1H"


def test_cli_get_user_usage_invocation(monkeypatch):
    calls = []
    resp = MockUsageMetricsResponse()
    monkeypatch.setattr(
        metrics_module,
        "query_user_usage",
        lambda ctx, **kwargs: (calls.append(kwargs), resp)[1],
    )

    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            ["--token", "test-token", "get-user-usage", "my-org"],
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0]["org_id"] == "my-org"


def test_cli_get_resource_usage_invocation(monkeypatch):
    calls = []
    resp = MockUsageMetricsResponse()
    monkeypatch.setattr(
        metrics_module,
        "query_resource_usage",
        lambda ctx, **kwargs: (calls.append(kwargs), resp)[1],
    )

    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            ["--token", "test-token", "get-resource-usage", "my-org"],
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0]["org_id"] == "my-org"


def test_cli_get_adoption_metrics_invocation(monkeypatch):
    calls = []
    resp = MockUsageMetricsResponse()
    monkeypatch.setattr(
        metrics_module,
        "query_adoption",
        lambda ctx, **kwargs: (calls.append(kwargs), resp)[1],
    )

    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            ["--token", "test-token", "get-adoption-metrics", "my-org"],
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0]["org_id"] == "my-org"


def test_cli_get_fleet_usage_invocation(monkeypatch):
    calls = []
    resp = MockUsageMetricsResponse()
    monkeypatch.setattr(
        metrics_module,
        "query_fleet_usage",
        lambda ctx, **kwargs: (calls.append(kwargs), resp)[1],
    )

    runner = CliRunner()
    m1, m2, m3, m4 = _cli_auth_mocks()
    with runner.isolated_filesystem(), m1, m2, m3, m4:
        result = runner.invoke(
            main_module.cli,
            ["--token", "test-token", "get-fleet-usage", "--bucket-size", "P1M"],
            catch_exceptions=False,
        )
    assert result.exit_code == 0
    assert len(calls) == 1
    assert calls[0]["bucket_size"] == "P1M"


def test_metrics_main_add_commands():
    import click

    test_cli = click.Group()
    metrics_main.add_commands(test_cli)
    expected_commands = {
        "get-usage-metrics",
        "list-usage-metrics",
        "get-user-usage",
        "get-resource-usage",
        "get-adoption-metrics",
        "get-fleet-usage",
    }
    assert expected_commands.issubset(set(test_cli.commands.keys()))
