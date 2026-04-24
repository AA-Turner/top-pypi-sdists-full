import json
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

pytest.importorskip("package_release_metadata_client")

from utf_queue_client.scripts.package_release_metadata_cli import (  # noqa: E402
    enquiry_cli_entrypoint,
    manifest_read_cli_entrypoint,
    manifest_write_cli_entrypoint,
    update_cli_entrypoint,
)

runner = CliRunner()

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

REQUIRED_UPDATE_ARGS = [
    "--release-name",
    "2.4.1",
    "--build-number",
    "42",
    "--job-url",
    "https://ci/build/1",
    "--stack-name",
    "zigbee",
    "--test-result-type",
    "sanity",
    "--status",
    "pass",
    "--run-num",
    "1",
]

REQUIRED_MANIFEST_WRITE_ARGS = [
    "--release-name",
    "2.4.1",
    "--build-number",
    "42",
]


def _qs_client_mock(create_data=None, latest_data=None, list_data=None):
    """Return a MagicMock QualityStatusClient with pre-configured .data on each method."""
    client = MagicMock()
    if create_data is not None:
        client.create_quality_status.return_value = MagicMock(data=create_data)
    if latest_data is not None:
        client.get_latest_quality_status.return_value = MagicMock(data=latest_data)
    if list_data is not None:
        client.list_quality_status.return_value = MagicMock(data=list_data)
    return client


def _manifest_client_mock(create_data=None, latest_data=None):
    """Return a MagicMock ManifestClient with pre-configured .data on each method."""
    client = MagicMock()
    if create_data is not None:
        client.create_manifest.return_value = MagicMock(data=create_data)
    if latest_data is not None:
        client.get_latest_manifest.return_value = MagicMock(data=latest_data)
    return client


# ---------------------------------------------------------------------------
# pkgrelease_manifest_read — argument validation
# ---------------------------------------------------------------------------


def test_manifest_read_help_exits_cleanly():
    result = runner.invoke(manifest_read_cli_entrypoint, ["--help"])
    assert result.exit_code == 0
    assert "ManifestRead" in result.output


def test_manifest_read_missing_release_name_fails():
    result = runner.invoke(manifest_read_cli_entrypoint, [])
    assert result.exit_code != 0
    assert "Missing option" in result.output


# ---------------------------------------------------------------------------
# pkgrelease_manifest_read — API routing and output
# ---------------------------------------------------------------------------


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_read_targets_prod_by_default(mock_make):
    data = MagicMock(manifest_id="uuid-1", to_dict=lambda: {"manifest_id": "uuid-1"})
    mock_make.return_value = _manifest_client_mock(latest_data=data)
    runner.invoke(manifest_read_cli_entrypoint, ["--release-name", "2.4.1"])
    mock_make.assert_called_once_with(False)


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_read_dev_flag_targets_dev(mock_make):
    data = MagicMock(manifest_id="uuid-1", to_dict=lambda: {"manifest_id": "uuid-1"})
    mock_make.return_value = _manifest_client_mock(latest_data=data)
    runner.invoke(manifest_read_cli_entrypoint, ["--release-name", "2.4.1", "--dev"])
    mock_make.assert_called_once_with(True)


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_read_calls_get_latest_manifest(mock_make):
    data = MagicMock(manifest_id="uuid-1", to_dict=lambda: {"manifest_id": "uuid-1"})
    client = _manifest_client_mock(latest_data=data)
    mock_make.return_value = client
    result = runner.invoke(manifest_read_cli_entrypoint, ["--release-name", "2.4.1"])
    assert result.exit_code == 0
    client.get_latest_manifest.assert_called_once_with("2.4.1")


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_read_output_is_json(mock_make):
    data = MagicMock(
        manifest_id="uuid-abc",
        to_dict=lambda: {"manifest_id": "uuid-abc", "release_name": "2.4.1"},
    )
    mock_make.return_value = _manifest_client_mock(latest_data=data)
    result = runner.invoke(manifest_read_cli_entrypoint, ["--release-name", "2.4.1"])
    assert result.exit_code == 0
    parsed = json.loads(result.output)
    assert parsed["manifest_id"] == "uuid-abc"


# ---------------------------------------------------------------------------
# pkgrelease_manifest_write — argument validation
# ---------------------------------------------------------------------------


def test_manifest_write_help_exits_cleanly():
    result = runner.invoke(manifest_write_cli_entrypoint, ["--help"])
    assert result.exit_code == 0
    assert "ManifestRead" in result.output


def test_manifest_write_missing_release_name_fails():
    result = runner.invoke(manifest_write_cli_entrypoint, ["--build-number", "42"])
    assert result.exit_code != 0
    assert "Missing option" in result.output


def test_manifest_write_missing_build_number_fails():
    result = runner.invoke(manifest_write_cli_entrypoint, ["--release-name", "2.4.1"])
    assert result.exit_code != 0
    assert "Missing option" in result.output


# ---------------------------------------------------------------------------
# pkgrelease_manifest_write — API routing and output
# ---------------------------------------------------------------------------


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_write_targets_prod_by_default(mock_make):
    data = MagicMock(manifest_id="uuid-1", to_dict=lambda: {"manifest_id": "uuid-1"})
    mock_make.return_value = _manifest_client_mock(create_data=data)
    runner.invoke(manifest_write_cli_entrypoint, REQUIRED_MANIFEST_WRITE_ARGS)
    mock_make.assert_called_once_with(False)


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_write_dev_flag_targets_dev(mock_make):
    data = MagicMock(manifest_id="uuid-1", to_dict=lambda: {"manifest_id": "uuid-1"})
    mock_make.return_value = _manifest_client_mock(create_data=data)
    runner.invoke(
        manifest_write_cli_entrypoint, REQUIRED_MANIFEST_WRITE_ARGS + ["--dev"]
    )
    mock_make.assert_called_once_with(True)


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_write_calls_create_manifest(mock_make):
    data = MagicMock(
        manifest_id="uuid-new", to_dict=lambda: {"manifest_id": "uuid-new"}
    )
    client = _manifest_client_mock(create_data=data)
    mock_make.return_value = client
    result = runner.invoke(manifest_write_cli_entrypoint, REQUIRED_MANIFEST_WRITE_ARGS)
    assert result.exit_code == 0
    client.create_manifest.assert_called_once()
    payload = client.create_manifest.call_args[0][0]
    assert payload.release_name == "2.4.1"
    assert payload.build_number == 42


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_write_optional_artifactory_url_forwarded(mock_make):
    data = MagicMock(
        manifest_id="uuid-new", to_dict=lambda: {"manifest_id": "uuid-new"}
    )
    client = _manifest_client_mock(create_data=data)
    mock_make.return_value = client
    result = runner.invoke(
        manifest_write_cli_entrypoint,
        REQUIRED_MANIFEST_WRITE_ARGS
        + ["--artifactory-url", "https://art.example.com/pkg"],
    )
    assert result.exit_code == 0
    payload = client.create_manifest.call_args[0][0]
    assert payload.artifactory_url == "https://art.example.com/pkg"


@patch("utf_queue_client.scripts.package_release_metadata_cli._make_manifest_client")
def test_manifest_write_output_is_json(mock_make):
    data = MagicMock(
        manifest_id="uuid-new",
        to_dict=lambda: {
            "manifest_id": "uuid-new",
            "release_name": "2.4.1",
            "build_number": 42,
        },
    )
    mock_make.return_value = _manifest_client_mock(create_data=data)
    result = runner.invoke(manifest_write_cli_entrypoint, REQUIRED_MANIFEST_WRITE_ARGS)
    assert result.exit_code == 0
    parsed = json.loads(result.output)
    assert parsed["manifest_id"] == "uuid-new"
    assert parsed["build_number"] == 42


# ---------------------------------------------------------------------------
# pkgrelease_quality_status_update — argument validation
# ---------------------------------------------------------------------------


def test_update_help_exits_cleanly():
    result = runner.invoke(update_cli_entrypoint, ["--help"])
    assert result.exit_code == 0
    assert "QualityStatusRead" in result.output


def test_update_missing_required_args_fails():
    result = runner.invoke(update_cli_entrypoint, ["--release-name", "2.4.1"])
    assert result.exit_code != 0
    assert "Missing option" in result.output


def test_update_invalid_status_rejected():
    args = REQUIRED_UPDATE_ARGS[:]
    args[args.index("pass")] = "passed"
    result = runner.invoke(update_cli_entrypoint, args)
    assert result.exit_code != 0
    assert "'passed' is not" in result.output


@pytest.mark.parametrize("status", ["pass", "fail", "aborted"])
def test_update_all_valid_statuses_accepted(status):
    args = REQUIRED_UPDATE_ARGS[:]
    args[args.index("pass")] = status
    data = MagicMock(id=1, to_dict=lambda: {"id": 1})
    with patch(
        "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
    ) as mock_make:
        mock_make.return_value = _qs_client_mock(create_data=data)
        result = runner.invoke(update_cli_entrypoint, args)
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# pkgrelease_quality_status_update — API routing and output
# ---------------------------------------------------------------------------


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_update_targets_prod_by_default(mock_make):
    data = MagicMock(id=1, to_dict=lambda: {"id": 1})
    mock_make.return_value = _qs_client_mock(create_data=data)
    runner.invoke(update_cli_entrypoint, REQUIRED_UPDATE_ARGS)
    mock_make.assert_called_once_with(False)


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_update_dev_flag_targets_dev(mock_make):
    data = MagicMock(id=1, to_dict=lambda: {"id": 1})
    mock_make.return_value = _qs_client_mock(create_data=data)
    runner.invoke(update_cli_entrypoint, REQUIRED_UPDATE_ARGS + ["--dev"])
    mock_make.assert_called_once_with(True)


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_update_calls_create_quality_status(mock_make):
    data = MagicMock(id=99, to_dict=lambda: {"id": 99})
    client = _qs_client_mock(create_data=data)
    mock_make.return_value = client
    result = runner.invoke(update_cli_entrypoint, REQUIRED_UPDATE_ARGS)
    assert result.exit_code == 0
    client.create_quality_status.assert_called_once()


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_update_optional_fields_forwarded(mock_make):
    data = MagicMock(id=1, to_dict=lambda: {"id": 1})
    client = _qs_client_mock(create_data=data)
    mock_make.return_value = client
    result = runner.invoke(
        update_cli_entrypoint,
        REQUIRED_UPDATE_ARGS
        + [
            "--pass-cnt",
            "80",
            "--fail-cnt",
            "20",
            "--total-cnt",
            "100",
            "--pass-pct",
            "80.0",
            "--sub-stack",
            "core",
        ],
    )
    assert result.exit_code == 0
    payload = client.create_quality_status.call_args[0][0]
    assert payload.pass_cnt == 80
    assert payload.fail_cnt == 20
    assert payload.sub_stack == "core"


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_update_output_is_json(mock_make):
    data = MagicMock(id=7, to_dict=lambda: {"id": 7, "status": "pass"})
    mock_make.return_value = _qs_client_mock(create_data=data)
    result = runner.invoke(update_cli_entrypoint, REQUIRED_UPDATE_ARGS)
    assert result.exit_code == 0
    parsed = json.loads(result.output)
    assert parsed["id"] == 7


# ---------------------------------------------------------------------------
# pkgrelease_quality_status_enquiry — argument validation
# ---------------------------------------------------------------------------


def test_enquiry_help_exits_cleanly():
    result = runner.invoke(enquiry_cli_entrypoint, ["--help"])
    assert result.exit_code == 0
    assert "LatestQualityStatusResponse" in result.output
    assert "List[QualityStatusRead]" in result.output


def test_enquiry_missing_release_name_fails():
    result = runner.invoke(enquiry_cli_entrypoint, [])
    assert result.exit_code != 0
    assert "Missing option" in result.output


# ---------------------------------------------------------------------------
# pkgrelease_quality_status_enquiry — API routing
# ---------------------------------------------------------------------------


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_enquiry_release_name_only_calls_latest(mock_make):
    data = MagicMock(
        to_dict=lambda: {"release_name": "2.4.1", "build_number": 42, "stacks": []}
    )
    client = _qs_client_mock(latest_data=data)
    mock_make.return_value = client
    result = runner.invoke(enquiry_cli_entrypoint, ["--release-name", "2.4.1"])
    assert result.exit_code == 0
    client.get_latest_quality_status.assert_called_once_with(
        release_name="2.4.1", build_number=None
    )


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_enquiry_with_build_num_calls_latest(mock_make):
    data = MagicMock(to_dict=lambda: {})
    client = _qs_client_mock(latest_data=data)
    mock_make.return_value = client
    result = runner.invoke(
        enquiry_cli_entrypoint, ["--release-name", "2.4.1", "--build-num", "42"]
    )
    assert result.exit_code == 0
    client.get_latest_quality_status.assert_called_once_with(
        release_name="2.4.1", build_number=42
    )


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_enquiry_with_stack_name_calls_list(mock_make):
    client = _qs_client_mock(list_data=[])
    mock_make.return_value = client
    result = runner.invoke(
        enquiry_cli_entrypoint, ["--release-name", "2.4.1", "--stack-name", "zigbee"]
    )
    assert result.exit_code == 0
    client.list_quality_status.assert_called_once_with(
        release_name="2.4.1",
        build_number=None,
        stack_name="zigbee",
        test_result_type=None,
    )


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_enquiry_with_test_result_type_calls_list(mock_make):
    client = _qs_client_mock(list_data=[])
    mock_make.return_value = client
    result = runner.invoke(
        enquiry_cli_entrypoint,
        ["--release-name", "2.4.1", "--test-result-type", "sanity"],
    )
    assert result.exit_code == 0
    client.list_quality_status.assert_called_once_with(
        release_name="2.4.1",
        build_number=None,
        stack_name=None,
        test_result_type="sanity",
    )


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_enquiry_targets_prod_by_default(mock_make):
    data = MagicMock(to_dict=lambda: {})
    mock_make.return_value = _qs_client_mock(latest_data=data)
    runner.invoke(enquiry_cli_entrypoint, ["--release-name", "2.4.1"])
    mock_make.assert_called_once_with(False)


@patch(
    "utf_queue_client.scripts.package_release_metadata_cli._make_quality_status_client"
)
def test_enquiry_dev_flag_targets_dev(mock_make):
    data = MagicMock(to_dict=lambda: {})
    mock_make.return_value = _qs_client_mock(latest_data=data)
    runner.invoke(enquiry_cli_entrypoint, ["--release-name", "2.4.1", "--dev"])
    mock_make.assert_called_once_with(True)


# ---------------------------------------------------------------------------
# _make_manifest_client / _make_quality_status_client — construction
# ---------------------------------------------------------------------------


@patch("utf_queue_client.scripts.package_release_metadata_cli.ManifestClient")
def test_make_manifest_client_prod_by_default(mock_cls):
    from utf_queue_client.scripts.package_release_metadata_cli import (
        _make_manifest_client,
    )

    _make_manifest_client(dev=False)
    mock_cls.assert_called_once_with(dev=False)


@patch("utf_queue_client.scripts.package_release_metadata_cli.ManifestClient")
def test_make_manifest_client_dev_flag(mock_cls):
    from utf_queue_client.scripts.package_release_metadata_cli import (
        _make_manifest_client,
    )

    _make_manifest_client(dev=True)
    mock_cls.assert_called_once_with(dev=True)


@patch("utf_queue_client.scripts.package_release_metadata_cli.QualityStatusClient")
def test_make_quality_status_client_prod_by_default(mock_cls):
    from utf_queue_client.scripts.package_release_metadata_cli import (
        _make_quality_status_client,
    )

    _make_quality_status_client(dev=False)
    mock_cls.assert_called_once_with(dev=False)


@patch("utf_queue_client.scripts.package_release_metadata_cli.QualityStatusClient")
def test_make_quality_status_client_dev_flag(mock_cls):
    from utf_queue_client.scripts.package_release_metadata_cli import (
        _make_quality_status_client,
    )

    _make_quality_status_client(dev=True)
    mock_cls.assert_called_once_with(dev=True)
