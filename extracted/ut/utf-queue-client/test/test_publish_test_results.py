import json
import os
import subprocess
import sys
from datetime import datetime
from unittest import mock
from uuid import UUID, uuid4

import pytest
from otel_extensions import inject_context_to_env, instrumented

from utf_queue_client.scripts.publish_test_results_cli import (
    normalize_to_json,
    publish_test_results_through_queue,
)


@pytest.fixture
def session_start_data():
    yield [
        ("startTime", datetime.now().isoformat()),
        ("jenkinsJobStatus", "IN PROGRESS"),
        ("releaseName", "22Q3-GA"),
        ("branchName", "release/22q3"),
        ("stackName", "WIFI"),
        ("SDKBuildNum", "1111"),
        ("jenkinsServerName", "LOCAL-RUN"),
        ("jenkinRunNum", "1111"),
        ("jenkinsJobName", "LOCAL-RUN"),
        ("jenkinsTestResultsUrl", "LOCAL-RUN"),
        ("testFramework", "UTF"),
    ]


@pytest.fixture
def session_stop_data():
    yield [
        ("startTime", datetime.now().isoformat()),
        ("stopTime", datetime.now().isoformat()),
        ("jenkinsJobStatus", "COMPLETE"),
        ("duration", "42"),
        ("jobType", "MyJob"),
        ("releaseName", "22Q3-GA"),
        ("branchName", "release/22q3"),
        ("stackName", "WIFI"),
        ("SDKBuildNum", "1111"),
        ("SDKUrl", "localhost.com/SDK"),
        ("studioURL", "localhost.com/studio"),
        ("totalTests", "4"),
        ("PASS_cnt", "2"),
        ("FAIL_cnt", "1"),
        ("SKIP_cnt", "1"),
        ("BLOCK_cnt", "0"),
        ("jenkinsServerName", "LOCAL-RUN"),
        ("jenkinRunNum", "1111"),
        ("jenkinsJobName", "LOCAL-RUN"),
        ("jenkinsTestResultsUrl", "LOCAL-RUN"),
        ("traceId", "QWERTY12345"),
        ("testFramework", "UTF"),
    ]


@pytest.fixture
def app_build_results_data():
    yield [
        ("app_name", "queue_client"),
        ("app_description", "queue_client"),
        ("test_suite_name", "queue_client_tests"),
        ("test_result_type", "SMOKE"),
        ("executor_name", "queue_client"),
        ("feature_name", "queue_client_tests"),
        ("module_name", "queue_client_tests"),
        ("phy_name", "1"),
        ("test_result", "pass"),
        ("exception_msg", ""),
        ("iot_req_id", "IOTREQ_1234"),
        ("tool_chain", "tool_chain"),
        ("notes", "notes"),
        ("test_duration_sec", "1.0"),
    ]


def generate_uuid() -> str:
    uuid_hex = uuid4().hex
    time = datetime.now()
    uuid_date_time = time.strftime("%y%m%d%H%M%S%f")
    uuid_hex = uuid_date_time + uuid_hex[len(uuid_date_time) :]
    suid = UUID(uuid_hex)
    return str(suid)


@instrumented
def test_jobstatus_session_data(request, session_start_data, session_stop_data):
    username = os.environ.get("UTF_QUEUE_USERNAME")
    password = os.environ.get("UTF_QUEUE_PASSWORD")
    pk_id = generate_uuid()
    args = [
        "--username",
        username,
        "--password",
        password,
        "--data_type",
        "SESSION_START",
    ]
    args += ["--data", "PK_ID", pk_id]
    for k, v in session_start_data:
        args += ["--data", k, v]

    stop_args = [
        "--username",
        username,
        "--password",
        password,
        "--data_type",
        "SESSION_STOP",
    ]
    stop_args += ["--data", "PK_ID", pk_id]
    for k, v in session_stop_data:
        stop_args += ["--data", k, v]

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
                    "publish_test_results_cli.py",
                ),
            ]
            + args,
        )
        process.communicate()
        assert process.poll() == 0

        process = subprocess.Popen(
            [
                sys.executable,
                os.path.join(
                    base_dir,
                    "utf_queue_client",
                    "scripts",
                    "publish_test_results_cli.py",
                ),
            ]
            + stop_args,
        )
        process.communicate()
        assert process.poll() == 0

    call_cli_script()


@instrumented
def test_app_build_results_data(request, app_build_results_data):
    username = os.environ["UTF_QUEUE_USERNAME"]
    password = os.environ["UTF_QUEUE_PASSWORD"]
    uuid_hex = uuid4().hex
    time = datetime.now()
    uuid_date_time = time.strftime("%y%m%d%H%M%S%f")
    uuid_hex = uuid_date_time + uuid_hex[len(uuid_date_time) :]
    suid = UUID(uuid_hex)
    args = [
        "--username",
        username,
        "--password",
        password,
        "--data_type",
        "BUILD_RESULT",
    ]
    args += ["--data", "session_pk_id", str(suid)]
    for k, v in app_build_results_data:
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
                    "publish_test_results_cli.py",
                ),
            ]
            + args,
        )
        process.communicate()
        assert process.poll() == 0

    call_cli_script()


def test_normalize_json():
    package_info = '{"dependency":{"security_sxsymcrypt":"test"},"version":2}'
    parsed = normalize_to_json(raw=package_info)
    parsed_json_lock = json.loads(parsed)
    assert parsed_json_lock["version"] == 2


@pytest.mark.parametrize(
    "package_info, expected_pacakge_info",
    [('{"foo": "bar"}', '{"foo": "bar"}'), ("", "{}")],
)
@mock.patch(
    "utf_queue_client.scripts.publish_test_results_cli.SqaTestResultProducerFactory"
)
def test_publish_build_result_with_package_info(
    mock_factory, app_build_results_data, package_info, expected_pacakge_info
):
    mock_producer = mock.Mock()
    mock_factory.create_producer.return_value = mock_producer
    url = "amqp://test"
    data_type = "BUILD_RESULT"
    data_dict = {
        "session_pk_id": "A464578D-E940-4541-B666-DE164654CABC",
        "package_info": package_info,
    }
    for k, v in app_build_results_data:
        data_dict[k] = v
    publish_test_results_through_queue(url, data_type, data_dict)
    assert os.environ["UTF_QUEUE_SERVER_URL"] == url
    assert os.environ["UTF_PRODUCER_APP_ID"]
    mock_producer.publish_app_build_result.assert_called_once()
    args, kwargs = mock_producer.publish_app_build_result.call_args
    assert args[0].app_name == "queue_client"
    assert args[0].package_info == expected_pacakge_info


@mock.patch(
    "utf_queue_client.scripts.publish_test_results_cli.SqaTestResultProducerFactory"
)
def test_publish_build_result_with_invalid_package_info(
    mock_factory, app_build_results_data
):
    mock_producer = mock.Mock()
    mock_factory.create_producer.return_value = mock_producer
    url = "amqp://test"
    data_type = "BUILD_RESULT"
    data_dict = {
        "session_pk_id": "A464578D-E940-4541-B666-DE164654CABC",
        "package_info": "not a json",
    }
    for k, v in app_build_results_data:
        data_dict[k] = v
    with pytest.raises(RuntimeError, match="Package info is not a valid JSON"):
        publish_test_results_through_queue(url, data_type, data_dict)
