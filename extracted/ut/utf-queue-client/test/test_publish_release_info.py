import os
import subprocess
import sys
from unittest import mock
from unittest.mock import MagicMock, patch

import pytest
import requests
from otel_extensions import inject_context_to_env, instrumented

from utf_queue_client.scripts.publish_release_info_cli import (
    cli,
    publish_release_information,
    update_artifacts_retention_days_to_keep_forever,
)


@pytest.fixture
def publish_release_info():
    yield [
        ("releaseDate", "2023-06-16"),
        ("branchName", "release/gecko_sdk_3.2"),
        ("releaseType", "GA"),
        ("releaseName", "23Q2-GA"),
        ("SDKBuildNum", "407"),
        (
            "installerURLSDK",
            "https://jenkins-cbs-gecko-sdk.silabs.net/job/Gecko_SDK_Suite_super/job/release%252F21q4/284/",
        ),
        ("IARVersionNum", "9.20.4"),
        ("GCCVersionNum", "10.3.1"),
        ("CommanderVersionNum", "v1.8.1"),
        ("SEVersionNum", "1.2.4"),
        ("WSTKFirmwareVersionNum", "v1.4.4"),
    ]


@instrumented
def test_publish_release_info(request, publish_release_info):
    args = ["--username", "svc_sqabot", "--password", "password"]
    for k, v in publish_release_info:
        args += ["--data", k, v]

    base_dir = os.path.dirname(os.path.dirname(__file__))

    @inject_context_to_env
    def call_cli_script():
        assert "TRACEPARENT" in os.environ
        process = subprocess.Popen(
            [
                sys.executable,
                os.path.join(
                    base_dir,
                    "utf_queue_client",
                    "scripts",
                    "publish_release_info_cli.py",
                ),
            ]
            + args,
        )
        process.communicate()
        assert process.poll() == 0

    call_cli_script()


def test_publish_release_information():
    requests_post = requests.post
    requests.post = MagicMock()
    publish_release_information("", "", {})
    assert requests.post.call_count == 2
    requests.post = requests_post


def test_publish_release_cli_insufficient_params():
    requests_post = requests.post
    requests_post_mock = MagicMock()
    requests.post = requests_post_mock
    cli("", "", {})
    assert requests.post.call_count == 0
    requests.post = requests_post


def test_publish_release_cli():
    requests_post = requests.post
    requests_post_mock = MagicMock()
    requests.post = requests_post_mock
    cli("", "", {("branchName", "test"), ("releaseData", "")})
    assert requests_post_mock.call_count == 2
    post_params = requests_post_mock.call_args.kwargs.get("json")
    assert post_params.get("branchName") == "test"
    assert post_params.get("releaseData") is None
    requests.post = requests_post


def test_update_artifacts_retention_days_to_keep_forever():
    requests_patch = requests.patch
    requests.patch = MagicMock()
    data_dict = {"branchName": "release/gec", "SDKBuildNum": "407"}
    update_artifacts_retention_days_to_keep_forever(data_dict)
    assert requests.patch.call_count == 1
    requests.patch = requests_patch
    patch_response = MagicMock()
    _ = mock.patch.object(requests, "patch", return_value=patch_response)
    patch_response.status_code = 200
    update_artifacts_retention_days_to_keep_forever(data_dict)


@patch("requests.post")
def test_publish_release_information_success(mock_post):
    mock_response_auth = MagicMock()
    mock_response_auth.json.return_value = {"access_token": "test_token"}
    mock_response_auth.raise_for_status.return_value = None

    mock_response_release = MagicMock()
    mock_response_release.status_code = 201
    mock_response_release.json.return_value = {"message": "success"}

    mock_post.side_effect = [mock_response_auth, mock_response_release]

    result = publish_release_information(
        "test_username", "test_password", {"test_key": "test_value"}
    )
    assert mock_response_release.json.called
    assert result


@patch("requests.post")
def test_publish_release_information_release_fail(mock_post):
    # Mock the responses
    mock_response_auth = MagicMock()
    mock_response_auth.json.return_value = {"access_token": "test_token"}
    mock_response_auth.raise_for_status.return_value = None

    mock_response_release = MagicMock()
    mock_response_release.status_code = 400
    mock_response_release.text = "Release failed"

    mock_post.side_effect = [mock_response_auth, mock_response_release]

    result = publish_release_information(
        "test_username", "test_password", {"test_key": "test_value"}
    )
    assert result is None


@patch("requests.post")
def test_publish_release_information_release_fail_422(mock_post):
    # Mock the responses
    mock_response_auth = MagicMock()
    mock_response_auth.json.return_value = {"access_token": "test_token"}
    mock_response_auth.raise_for_status.return_value = None

    mock_response_release = MagicMock()
    mock_response_release.status_code = 422
    mock_response_release.json.return_value = {
        "detail": [{"loc": ["", "test_field"], "msg": "test_error"}]
    }

    mock_post.side_effect = [mock_response_auth, mock_response_release]

    # Call the function
    result = publish_release_information(
        "test_username", "test_password", {"test_key": "test_value"}
    )
    assert mock_response_release.json.called
    assert result is None
