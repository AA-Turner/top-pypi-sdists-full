import os
import time
from contextlib import AbstractContextManager, ExitStack, contextmanager
from threading import Thread
from typing import Optional
from urllib import parse

import ndjson
import pytest
from otel_extensions_pytest import TelemetryOptions, instrumented_fixture
from stopwatch import Stopwatch

from utf_queue_client.clients.async_consumer import AsyncConsumerBase, MessageContainer
from utf_queue_client.models import (
    SqaAppBuildResult,
    SqaTestResult,
    SqaTestSession,
)
from utf_queue_client.models.schemas.utf_queue_models.models.python.generated_models import (
    TestRailResult,
    XrayImportTestExecution,
    XrayInfo,
    XrayTestExecUpdate,
)

pytest_plugins = ("otel_extensions",)


def pytest_addoption(parser, pluginmanager):
    if "UTF_QUEUE_HOSTNAME" not in os.environ:
        os.environ["UTF_QUEUE_HOSTNAME"] = "utf-queue-central.silabs.net"
    options = TelemetryOptions()
    options.OTEL_SERVICE_NAME = "utf_queue_client_python"
    options.OTEL_SESSION_NAME = "unit tests pytest session"

    # Normally these options should be set by the pipeline, but if running locally we can use these defaults
    if options.OTEL_EXPORTER_OTLP_ENDPOINT is None:
        options.OTEL_EXPORTER_OTLP_ENDPOINT = "https://otel-collector-http.silabs.net/"
        options.OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"


@pytest.fixture()
def sqa_app_build_result():
    yield SqaAppBuildResult(
        session_pk_id="22072702-3430-2721-5681-2ae58836aea1",
        app_name="app name",
        app_description="",
        test_suite_name="",
        test_result_type="BUILDAPP",
        executor_name="",
        feature_name="",
        module_name="",
        phy_name="",
        test_result="pass",
        engineer_name="",
        Exception="",
        iot_req_id="",
        tool_chain="",
        notes="",
        test_duration_sec=12,
    )


@pytest.fixture()
def sqa_test_result():
    yield SqaTestResult(
        session_pk_id="123445667",
        test_case_id="asdf",
        test_case_version_num=1,
        test_suite_name="",
        test_description="",
        test_result_type="duration",
        test_parametric_date="",
        test_case_name="asdfg",
        executor_name="executor_name",
        feature_name="feature_name",
        test_creation_date="2000-01-01",
        testbed_name="utf-testbed",
        module_name="module_name",
        phy_name="",
        test_result="pass",
        engineer_name="",
        exception_msg="",
        iot_req_id="12345",
        tool_chain="tool_chain",
        vendor_name="",
        vendor_build="",
        vendor_result="",
        notes="",
        test_duration_sec=5.4,
        test_bed_label="",
        req_id="req_123",
        product_line="RS9117",
        product_type="NCP",
        customer_type="wearables",
        jenkins_test_case_results_url="dummy",
        test_case_uuid="23122702-2334-4323-6723-822dee7f8168",
    )


@pytest.fixture()
def sqa_test_session():
    yield SqaTestSession(
        PK_ID="123445667",
        startTime="2020-01-01",
        stopTime="2022-01-01",
        jenkinsJobStatus="COMPLETE",
        duration=123,
        jobType="",
        releaseName="release",
        branchName="branch",
        stackName="stack",
        SDKBuildNum=1,
        SDKUrl="localhost.com/SDK",
        studioUrl="localhost.com/Studio",
        totalTests=5,
        PASS_cnt=2,
        FAIL_cnt=1,
        SKIP_cnt=2,
        BLOCK_cnt=0,
        jenkinsServerName="jenkins",
        jenkinRunNum=0,
        jenkinsJobName="job",
        jenkinsTestResultsUrl="localhost.com/jenkins",
        traceId="TraceID",
        SDKVersion="4.3",
        test_run_by="tevunnam",
    )


@pytest.fixture()
def test_rail_add_test_result():
    yield TestRailResult(
        id="C123",
        run_id="1234",
        status="pass",
        comment="testing",
        version="v1",
        defects="",
        custom_props={"custom_evk_version": "v2", "custom_interface_type": "gcc"},
    )


@pytest.fixture()
def xray_import_test_execution_data():
    yield XrayImportTestExecution(
        test_execution_key="DUMMY_EXEC",
        add_tests_to_plan=True,
        info=XrayInfo(project="DUMMY", test_plan_key="DUMMY_PLAN"),
        tests=[
            XrayTestExecUpdate(
                comment="",
                executed_by="test",
                finish="2025-02-11T07:39:25+00:00",
                start="2025-02-11T07:39:23+00:00",
                status="PASS",
                test_key="TC1234567890",
            )
        ],
    )


@pytest.fixture()
def data_lake_tenant_key():
    return "dummy_key"


@pytest.fixture(params=[False, True])
def csv_file_path(tmp_path, request):
    path = os.path.join(tmp_path, "test.csv")
    with open(path, "w") as f:
        if request.param:
            f.write("t" * 256)
        else:
            f.write("test")
    return path


@pytest.fixture()
def json_file_path(tmp_path):
    path = os.path.join(tmp_path, "test.json")
    with open(path, "w") as f:
        f.write("{}")
    return path


@pytest.fixture()
def parquet_file_path(tmp_path):
    path = os.path.join(tmp_path, "test.parquet")
    with open(path, "w") as f:
        f.write(".....")
    return path


@pytest.fixture()
def ndjson_file_path(tmp_path):
    path = os.path.join(tmp_path, "test.ndjson")
    with open(path, "w") as f:
        objects = [{"foo": "bar"}, {"foo": "baz"}]
        ndjson.dump(objects, f)
    return path


@pytest.fixture(params=[{}])
def set_custom_queue_params(request):
    var_map = request.param
    with temporary_environment_variables_setter(var_map):
        yield


@pytest.fixture()
def amqp_url(set_custom_queue_params):
    username = os.environ["UTF_QUEUE_USERNAME"]
    password = os.environ["UTF_QUEUE_PASSWORD"]
    hostname = os.environ.get("UTF_QUEUE_HOSTNAME")
    assert hostname is not None, "UTF_QUEUE_HOSTNAME environment variable must be set"
    scheme = os.environ.get("UTF_QUEUE_SCHEME", "amqps")
    port = os.environ.get("UTF_QUEUE_PORT", "443")
    virtual_host = os.environ.get("UTF_QUEUE_VIRTUAL_HOST", "%2f")
    url = f"{scheme}://{username}:{parse.quote(password)}@{hostname}:{port}/{virtual_host}?stack_timeout=30"
    os.environ["UTF_QUEUE_SERVER_URL"] = url
    yield url
    del os.environ["UTF_QUEUE_SERVER_URL"]


class TestConsumer(AsyncConsumerBase):
    def __init__(self, amqp_url: str, heartbeat: Optional[int] = None):
        self.messages = []
        self.callback = None
        super().__init__(
            amqp_url=amqp_url,
            queue="default",
            message_handler=self.handle_message,
            durable=True,
            heartbeat=heartbeat,
        )

    def handle_message(self, message: MessageContainer):
        self.messages.append(message)
        if self.callback is not None:
            self.callback(message)

    def expect_messages(self, num_messages: int):
        sw = Stopwatch()
        while sw.elapsed_sec < 10:
            time.sleep(0.1)
            if len(self.messages) >= num_messages:
                break
        assert len(self.messages) >= num_messages


@instrumented_fixture(params=[None])
def queue_consumer(amqp_url, request):
    consumer = TestConsumer(amqp_url, heartbeat=request.param)
    thread = Thread(target=consumer.run)
    thread.daemon = True
    thread.start()
    sw = Stopwatch()
    while sw.elapsed_sec < 20:
        time.sleep(0.1)
        if consumer.was_consuming:
            break
    if not consumer.was_consuming:
        consumer.stop()
        thread.join()
        raise RuntimeError("Error starting TestConsumer!")

    yield consumer

    consumer.stop_consuming()
    sw = Stopwatch()
    while sw.elapsed_sec < 20:
        time.sleep(0.1)
        if not consumer.consuming:
            break
    consumer.stop(force=True)
    thread.join()


class TemporaryEnvironmentVariableSetter(AbstractContextManager):
    def __init__(self, var, val):
        self.var = var
        self.val = val
        self.prev_val = None

    def __enter__(self):
        self.prev_val = os.environ.get(self.var)
        if self.val is not None:
            os.environ[self.var] = self.val
        else:
            if self.prev_val is not None:
                del os.environ[self.var]
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.prev_val is None:
            if self.val is not None and self.var in os.environ:
                del os.environ[self.var]
        else:
            os.environ[self.var] = self.prev_val


@contextmanager
def temporary_environment_variable_setter(var, val):
    with TemporaryEnvironmentVariableSetter(var, val):
        yield


@contextmanager
def temporary_environment_variables_setter(var_map: dict):
    with ExitStack() as stack:
        for var, val in var_map.items():
            context = TemporaryEnvironmentVariableSetter(var, val)
            stack.enter_context(context)
        yield


@pytest.fixture(params=[])
def set_environment_variable(request):
    assert (
        isinstance(request.param, tuple) and len(request.param) == 2
    ), "fixture param must be a tuple with two elements"
    var_name = request.param[0]
    var_value = request.param[1]
    with TemporaryEnvironmentVariableSetter(var_name, var_value):
        yield


@pytest.fixture(params=[])
def set_environment_variables(request):
    assert_message = "fixture param must be a list of tuples with two elements each"
    assert isinstance(request.param, list), assert_message
    for param_element in request.param:
        assert (
            isinstance(param_element, tuple) and len(param_element) == 2
        ), assert_message

    with ExitStack() as stack:
        for param_element in request.param:
            var_name = param_element[0]
            var_value = param_element[1]
            context = TemporaryEnvironmentVariableSetter(var_name, var_value)
            stack.enter_context(context)
        yield
