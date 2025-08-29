import atexit
import json
import os
import os.path
import re
import sys
import time
from contextlib import contextmanager
from copy import copy
from fnmatch import fnmatch
from io import BytesIO
from typing import Any, Dict, List, Union
from unittest.mock import create_autospec
from zipfile import ZipFile

from comet_ml import Experiment
from comet_ml.config import (
    OFFLINE_EXPERIMENT_JSON_FILE_NAME,
    OFFLINE_EXPERIMENT_MESSAGES_JSON_FILE_NAME,
    get_backend_address,
    get_comet_timeout_http,
    get_global_experiment,
    set_global_experiment,
)
from comet_ml.connection import RestApiClient, RestServerConnection
from comet_ml.experiment import CometExperiment
from comet_ml.feature_toggles import FeatureToggles
from comet_ml.messages import (
    MetricMessage,
    ParameterMessage,
    UploadFileMessage,
    UploadInMemoryMessage,
    WebSocketMessage,
)
from comet_ml.offline import (
    get_experiment_file_validator,
    get_parameter_msg_validator,
    get_upload_msg_validator,
    get_ws_msg_validator,
)
from comet_ml.testlib.dummy import DummyHeartBeatThread, DummyStreamer
from comet_ml.testlib.predicates import AlwaysEquals
from comet_ml.utils import url_join

import multipart
from responses import RequestsMock

from .mock_http import rest_api_v2_url_prefix
from .test_constants import (
    FLUSH_INITIAL_DATA_LOGGER_TIMEOUT,
    MAX_TRY_SECONDS,
    SOME_API_KEY,
    SOME_PROJECT_ID,
    SOME_RUN_ID,
)


def experiment_builder(
        api_key=SOME_API_KEY,
        cls=Experiment,
        streamer=None,
        feature_toggles=None,
        allow_report=False,
        upload_web_asset_url_prefix="",
        upload_web_image_url_prefix="",
        upload_api_asset_url_prefix="",
        upload_api_image_url_prefix="",
        log_git_metadata=False,
        log_git_patch=False,
        log_env_cpu=False,
        **kwargs
):
    class _TestingExperiment(cls):
        def _setup_http_handler(self):
            self.http_handler = None

        def _setup_streamer(self, *args, **kwargs):
            if streamer is None:
                self.streamer = DummyStreamer(
                    api_key=SOME_API_KEY, run_id=SOME_RUN_ID, project_id=SOME_PROJECT_ID
                )
            else:
                self.streamer = streamer

            if feature_toggles is None:
                self.feature_toggles = FeatureToggles({}, self.config)
            else:
                self.feature_toggles = FeatureToggles(feature_toggles, self.config)

            self.upload_web_asset_url_prefix = upload_web_asset_url_prefix
            self.upload_web_image_url_prefix = upload_web_image_url_prefix
            self.upload_api_asset_url_prefix = upload_api_asset_url_prefix
            self.upload_api_image_url_prefix = upload_api_image_url_prefix

            # Create a Connection for the cases where we need to test the reports
            # fixme does this code work/run?
            if allow_report:
                self.connection = RestServerConnection(
                    self.api_key,
                    self.id,
                    get_backend_address(),
                    get_comet_timeout_http(self.config),
                    verify_tls=True,
                )

            self.rest_api_client = create_autospec(RestApiClient)

            self._heartbeat_thread = DummyHeartBeatThread()

            return True

        def _mark_as_started(self):
            pass

        def _mark_as_ended(self):
            pass

        def add_tag(self, *args, **kwargs):
            return CometExperiment.add_tag(self, *args, **kwargs)

        def add_tags(self, *args, **kwargs):
            return CometExperiment.add_tags(self, *args, **kwargs)

        def _report(self, *args, **kwargs):
            if not allow_report:
                return None

            return super(_TestingExperiment, self)._report(*args, **kwargs)

        def _register_callback_remotely(self, *args, **kwargs):
            pass

        def send_notification(self, title, status=None, additional_data=None):
            pass

        def _check_experiment_throttled(self):
            return False

    result = _TestingExperiment(
        api_key,
        log_git_metadata=log_git_metadata,
        log_git_patch=log_git_patch,
        log_env_cpu=log_env_cpu,
        **kwargs
    )

    return result


def a_live_experiment(
        api_key=SOME_API_KEY,
        run_id=SOME_RUN_ID,
        project_id=SOME_PROJECT_ID,
        auto_output_logging=None,
        flush_initial_data_logger_timeout=FLUSH_INITIAL_DATA_LOGGER_TIMEOUT,
        feature_toggles=None,
        **kwargs
):
    # this line is used for source code testing, don't remove this comment

    streamer = DummyStreamer(
        api_key=api_key,
        run_id=run_id,
        project_id=project_id,
    )
    if auto_output_logging is None:
        auto_output_logging = "simple"
    kwargs["log_env_cpu"] = kwargs.get("log_env_cpu", False)
    kwargs["log_env_gpu"] = kwargs.get("log_env_gpu", False)
    kwargs["log_env_network"] = kwargs.get("log_env_network", False)
    kwargs["log_env_disk"] = kwargs.get("log_env_disk", False)

    experiment = experiment_builder(
        api_key=api_key,
        streamer=streamer,
        auto_output_logging=auto_output_logging,
        feature_toggles=feature_toggles,
        **kwargs
    )

    # flush initial data logger thread
    experiment._flush_initial_data_logger(flush_initial_data_logger_timeout)

    return experiment


def a_live_clean_experiment(
        flush_initial_data_logger_timeout=FLUSH_INITIAL_DATA_LOGGER_TIMEOUT, *args, **kwargs
):
    """Allows to get a virgin Experiment with empty messages queue of the streamer. I.e., all initialization messages
    cleaned from the pending messages queue before this function returns."""
    experiment = a_live_experiment(*args, **kwargs)
    assert (
            experiment._flush_initial_data_logger(flush_initial_data_logger_timeout) is True
    )
    experiment.streamer.clean()
    return experiment


def clear_env_api_key():
    try:
        del os.environ["COMET_API_KEY"]
    except KeyError:
        pass


def extract_message_params(messages):
    """Extract the params key and values from message for asserting them"""
    params = {}
    for message in messages:
        if not hasattr(message, "param") or message.param is None:
            continue

        params[message.param["paramName"]] = message.param["paramValue"]
    return params


def to_bytes(data, enc="utf8"):
    return data.encode(enc) if isinstance(data, str) else data


def parse_multipart(raw_data):
    boundary = raw_data.split(b"\r")[0][2:]
    data = BytesIO(to_bytes(raw_data))
    return multipart.MultipartParser(data, boundary)


class MonkeyPatchingHelper(object):
    modules_to_patch = []

    def setup_method(self):
        # Save and alter the python path to point to our fake modules
        self.old_sys_path = copy(sys.path)
        fake_module_path = os.path.join(
            os.path.dirname(__file__), "unit", "fake_modules"
        )
        sys.path.insert(0, fake_module_path)

        # Save the meta path
        self.old_meta_path = copy(sys.meta_path)

        to_clean = []

        # Ensure we have a clean state
        for module in sys.modules:
            for clean in self.modules_to_patch:
                if fnmatch(module, clean):
                    to_clean.append(module)

        for module in to_clean:
            try:
                del sys.modules[module]
            except KeyError:
                pass

    def teardown_method(self):
        # Restore the old paths
        sys.path = self.old_sys_path
        sys.meta_path = self.old_meta_path

        to_clean = []

        # Ensure we have a clean state
        for module in sys.modules:
            for clean in self.modules_to_patch:
                if fnmatch(module, clean):
                    to_clean.append(module)

        for module in to_clean:
            try:
                del sys.modules[module]
            except KeyError:
                pass


@contextmanager
def attributes(obj, **kwargs):
    """
    Temporarily set an object's attributes to other values.

    ```
    assert object.attribute == "ABC"
    with attributes(object, attribute="XYZ"):
        assert object.attribute == "XYZ"
    assert object.attribute == "ABC"
    ```
    """
    original_values = {}
    for key in kwargs:
        original_values[key] = getattr(obj, key)
        setattr(obj, key, kwargs[key])
    yield
    for key in kwargs:
        setattr(obj, key, original_values[key])


@contextmanager
def environ(env):
    """Temporarily set environment variables inside the context manager and
    fully restore previous environment afterwards
    """
    original_env = {key: os.getenv(key) for key in env}
    os.environ.update(env)
    try:
        yield

    finally:
        for key, value in original_env.items():
            if value is None:
                del os.environ[key]
            else:
                os.environ[key] = value


def apply_updates_to_the_msg(message, updates):
    for key in updates:
        if isinstance(message["payload"][key], dict):
            message["payload"][key].update(updates[key])
        else:
            message["payload"][key] = updates[key]


def filter_messages(message_type: str, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    filtered = filter(lambda m: m["type"] == message_type, messages)
    return list(filtered)


def filter_calls(responses, expected_url):
    return [call for call in responses.calls if call.request.url == expected_url]


def filter_calls_startswith(responses, expected_url):
    return [
        call for call in responses.calls if call.request.url.startswith(expected_url)
    ]


def filter_calls_by_payload_key(responses, expected_url, message_key):
    """Filter calls by payload of response body and returns list of calls having specified message_key in the body."""
    response_calls = filter_calls(responses=responses, expected_url=expected_url)
    calls = list()
    for call in response_calls:
        body = parse_response_body(call)
        if message_key in body:
            calls.append(call)

    return calls


def debug_calls(responses):
    debug_raw_calls(responses.calls)


def debug_raw_calls(calls):
    print("%d calls" % len(calls))
    for call in calls:
        print(call)
        print("\t" + call.request.url)
        body = call.request.body
        print("\t" + repr(body))
        response = call.response
        if hasattr(response, "status_code"):
            print("\t" + str(response.status_code))
        if hasattr(response, "text"):
            print("\t" + response.text)
        print()


class NonDebuggableObject(object):
    def __str__(self):
        raise ZeroDivisionError

    def __repr__(self):
        raise ZeroDivisionError


def re_search_multiline(multi_line_text, raw_pattern):
    pattern = re.compile(raw_pattern)
    for line in multi_line_text.splitlines():
        print("Line", repr(line), pattern, pattern.search(line))
        if pattern.search(line):
            return True

    return False


def gen_metric_message(metric_name, value, step=None):
    msg = MetricMessage()
    msg.set_metric(metric_name, value, step)
    msg.local_timestamp = value
    return msg.to_message_dict()


def validate_offline_archive(archive):
    """Ensure that all the files created match the json schemas"""
    # First validate the metadata
    assert OFFLINE_EXPERIMENT_JSON_FILE_NAME in archive.namelist()

    experiment_meta_content = archive.read(OFFLINE_EXPERIMENT_JSON_FILE_NAME)
    experiment_meta = json.loads(experiment_meta_content.decode("utf-8"))

    validator = get_experiment_file_validator(allow_additional_properties=False)
    validator.validate(experiment_meta)

    ws_msg_validator = get_ws_msg_validator(allow_additional_properties=False)
    upload_msg_validator = get_upload_msg_validator(allow_additional_properties=False)
    parameter_msg_validator = get_parameter_msg_validator(
        allow_additional_properties=False
    )

    # Then the messages file
    assert OFFLINE_EXPERIMENT_MESSAGES_JSON_FILE_NAME in archive.namelist()
    messages = archive.read(OFFLINE_EXPERIMENT_MESSAGES_JSON_FILE_NAME)

    for line in messages.splitlines():
        message = json.loads(line.decode("utf-8"))

        message_type = message["type"]

        print("MSG TYPE", message_type, message)

        payload = message["payload"]
        if message_type == WebSocketMessage.type:
            ws_msg_validator.validate(payload)
        elif message_type == ParameterMessage.type:
            parameter_msg_validator.validate(payload)
        elif message_type == UploadFileMessage.type:
            upload_msg_validator.validate(payload)


def get_offline_archive(offline_dir: str, offline_archive_file_name: str):
    expected_zip_path = os.path.join(offline_dir, offline_archive_file_name)
    assert os.path.isfile(expected_zip_path)

    # Try to open the zipfile
    comet_zip = ZipFile(expected_zip_path, "r")

    # Validate the files
    validate_offline_archive(comet_zip)

    return comet_zip


def assert_files_have_same_content(file_1, file_2):
    assert os.path.isfile(file_1), "Is not a file: %r" % file_1

    with open(file_1, "rb") as original:
        original_source = original.read()

    assert os.path.isfile(file_2), "Is not a file: %r" % file_2

    with open(file_2, "rb") as uploaded:
        uploaded_source = uploaded.read()

    assert original_source == uploaded_source, "Content of files is not equal"


def until(function, sleep=0.5, max_try_seconds=MAX_TRY_SECONDS):
    """
    Try assert function(). 20 seconds max
    """
    start_time = time.time()
    while not function():
        if (time.time() - start_time) > max_try_seconds:
            return False
        time.sleep(sleep)
    return True


def assert_until_equals(function, value, sleep=0.5, max_try_seconds=MAX_TRY_SECONDS):
    """
    Try assert function(). 20 seconds max
    """
    result = function()
    start_time = time.time()
    while result != value:
        if (time.time() - start_time) > max_try_seconds:
            assert False, "%r != %r" % (result, value)
        time.sleep(sleep)
        result = function()


def assert_until_not_equals(
        function, value, sleep=0.5, max_try_seconds=MAX_TRY_SECONDS
):
    """
    Try max_tries, assert function(). 20 seconds max
    """
    result = function()
    start_time = time.time()
    while result == value:
        if (time.time() - start_time) > max_try_seconds:
            assert False
        time.sleep(sleep)
        result = function()


def until_asserts(function, sleep=0.5, max_try_seconds=MAX_TRY_SECONDS):
    """
    Try max_tries, function(). function() is expected to call assert. 20 seconds max
    """
    start_time = time.time()
    while True:
        try:
            result = function()
            return result
        except AssertionError:
            if (time.time() - start_time) > max_try_seconds:
                raise

            time.sleep(sleep)


def find_message(lines: List[str], mtype: str, first_only: bool = True):
    found_message = []
    for line in lines:
        message = json.loads(line)
        if "type" in message and mtype == message["type"]:
            if first_only:
                return message
            else:
                found_message.append(message)

    if first_only:
        return None

    return found_message


def get_all_messages(messages: List[Any], mtype: str) -> List[Any]:
    return [message for message in messages if getattr(message, mtype, None) is not None]


def get_uploads_names(upload_messages: List[Any]) -> List[str]:
    return [
        message.additional_params.get("figName", None) or message.additional_params.get("fileName", None)
        for message in upload_messages
    ]


def get_all_upload_messages(lines):
    found_messages = []
    for line in lines:
        message = json.loads(line)
        if message["type"] == UploadFileMessage.type:
            found_messages.append(message)

    return found_messages


def parse_response_body(response_call):
    body = response_call.request.body
    if hasattr(body, "decode"):
        body = body.decode("utf-8")
    return json.loads(body)


def find_streamer_messages_by_type(fake_streamer: DummyStreamer, message_type: Any) -> List[Any]:
    return [m for m in fake_streamer.messages if isinstance(m, message_type)]


def get_streamer_upload_messages(
        fake_streamer,
        asset_type: str = None
) -> List[Union[UploadFileMessage, UploadInMemoryMessage]]:
    messages = find_streamer_messages_by_type(
        fake_streamer, UploadFileMessage
    ) + find_streamer_messages_by_type(fake_streamer, UploadInMemoryMessage)

    if asset_type:
        messages = [msg for msg in messages if msg.upload_type == asset_type]

    return messages


def make_expected_confusion_matrix(**kwargs):
    expected = {
        "version": 1,
        "title": "Confusion Matrix",
        "labels": [],
        "matrix": None,
        "rowLabel": "Actual Category",
        "columnLabel": "Predicted Category",
        "maxSamplesPerCell": 25,
        "sampleMatrix": None,
        "type": None,
    }
    expected.update(kwargs)
    return expected


string_metadata_col = {
    "name": "String",
    "id": "String--metadata",
    "type": "string",
    "source": "metadata",
}
x_metadata_col = {
    "name": "x",
    "id": "x--metadata",
    "type": "double",
    "source": "metadata",
}
x_metrics_col = {"name": "x", "id": "x--metrics", "type": "double", "source": "metrics"}
x_params_col = {"name": "x", "id": "x--params", "type": "double", "source": "params"}
os_env_details_col = {
    "name": "os",
    "id": "os--env_details",
    "type": "string",
    "source": "env_details",
}
# Make sure the SDK can handle unknown items:
x_unknown_col = {"name": "x", "id": "x--unknown", "type": "string", "source": "unknown"}
x_log_other_col = {
    "name": "x",
    "id": "x--log_other",
    "type": "double",
    "source": "log_other",
}
best_tag_col = {"name": "best", "id": "best--tag", "type": "string", "source": "tag"}


def get_columns():
    """
    Mock get variable columns for query functions.
    """
    return {
        "columns": [
            string_metadata_col,
            x_metadata_col,
            x_metrics_col,
            x_params_col,
            os_env_details_col,
            x_unknown_col,
            x_log_other_col,
            best_tag_col,
        ]
    }


def sorted_list(obj):
    # type: (Any) -> List[Any]
    """Returns provided object as sorted list if the input is dictionary or list. It is useful to have ordered JSON
    object for comparison."""
    if isinstance(obj, dict):
        return sorted((k, sorted_list(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(sorted_list(x) for x in obj)
    else:
        return obj


class IPythonObject(object):
    def __init__(self, user_local=None, colab=False):
        self.kernel = True
        self.colab = colab
        if user_local is None:
            user_local = {"_ih": ["import IPython"], "_oh": {}}

        # save
        self.ns_table = {"user_local": user_local}

    def __repr__(self):
        if self.colab:
            return "<google.colab._shell.Shell object at 0x7f22f3a203d0>"
        else:
            return "<IPython.terminal.interactiveshell.TerminalInteractiveShell object at 0x7f41dfc7ca60>"


def ipython_user_local_from(source_code):
    # type: (List[str])->Dict[str, Any]
    return {"_ih": source_code, "_oh": {}}


def force_clean_global_experiment(assert_success=False):
    try:
        global_experiment = get_global_experiment()
        if global_experiment is not None:
            if not global_experiment.ended:
                # do experiment cleanup only if it's not done already
                success = global_experiment._on_end(wait=True)
                if assert_success:
                    if not success:
                        msg = "%r didn't successfully cleaned up"
                        raise Exception(msg % global_experiment)
    finally:
        set_global_experiment(None)


def create_experiment_for_fixture(
        test_experiment_fixture, experiment_class, api_key, **kwargs
):
    # Logging code, git metadata, and environment details can be slow as it involves disk-access,
    # enable only if requested explicitly
    kwargs["log_code"] = kwargs.get("log_code", False)
    kwargs["log_git_metadata"] = kwargs.get("log_git_metadata", False)
    kwargs["log_git_patch"] = kwargs.get("log_git_patch", False)
    kwargs["log_env_details"] = kwargs.get("log_env_details", False)
    exp = experiment_class(api_key=api_key, **kwargs)
    test_experiment_fixture.to_clean.append(exp)
    return exp


class TestExperimentFixture:
    def setup_method(self, method):
        # Clean current experiment to avoid calling on_end on old experiment instances
        force_clean_global_experiment()

        self.api_key = "API_KEY_%s_%s" % (self.__class__.__name__, method.__name__)
        self.run_id = "RunId"
        self.project_id = None
        self.focus_url = None

        # Test specific responses instance
        self.responses = RequestsMock(assert_all_requests_are_fired=False)
        self.responses.start()

        self.to_clean = []  # List of experiments to clean

        self.assert_success_experiment_clean = True

    def teardown_method(self):
        try:
            # Clean atexit
            if hasattr(atexit, "_clear"):
                atexit._clear()
            else:
                raise NotImplementedError()

            force_clean_global_experiment(
                assert_success=self.assert_success_experiment_clean
            )

            # Clean other experiments
            for exp in self.to_clean:
                if exp.ended:
                    continue
                print("Cleaning exp", exp)
                exp._on_end(wait=True)
                print("Exp cleaned", exp)
        finally:
            self.responses.stop()
            self.responses.reset()


def assert_experiment_error_reported(
        server_address, responses_mock, experiment_key, expected_calls_number=1, has_crashed=False
):
    expected_url = url_join(
        server_address, rest_api_v2_url_prefix, "write/experiment/update-status"
    )
    calls = filter_calls(responses_mock, expected_url)
    assert len(calls) == expected_calls_number, "wrong calls count %d, expected %d" % (
        len(calls),
        expected_calls_number,
    )
    sent_body = json.loads(calls[0].request.body.decode("utf-8"))
    print(sent_body)
    assert sent_body == {
        "experimentKey": experiment_key,
        "isAlive": True,
        "error": AlwaysEquals(),
        "hasCrashed": has_crashed,
    }
    assert sent_body["error"] is not None


def stderr_message(message):
    sys.stderr.write("%s\n" % message)


def wait_for(reason, callable, timeout):
    start = time.time()
    while True:
        duration = time.time() - start
        if callable():
            stderr_message("SUCCESS (took %s): %s" % (duration, reason))
            return

        if duration > timeout:
            assert (
                False
            ), "waited for '%s' but it did not materialize for %s seconds" % (
                reason,
                timeout,
            )

        remaining = "%d" % (timeout - duration)
        stderr_message("%s seconds left for: %s" % (remaining, reason))
        time.sleep(0.5)


def wait_for_messages(fake_streamer, message_type, minimum=1, timeout=10):
    find_messages = lambda: find_streamer_messages_by_type(fake_streamer, message_type)
    wait_for(
        "messages of type %s to be picked up" % message_type,
        lambda: len(find_messages()) >= minimum,
        timeout,
    )
    return find_messages()


def read_meta_data_from_offline_experiment_zip(offline_dir, offline_archive_file_name):
    comet_zip = get_offline_archive(offline_dir, offline_archive_file_name)

    assert OFFLINE_EXPERIMENT_JSON_FILE_NAME in comet_zip.namelist()

    experiment_meta_content = comet_zip.read(OFFLINE_EXPERIMENT_JSON_FILE_NAME)
    return json.loads(experiment_meta_content.decode("utf-8"))


def read_messages_from_offline_experiment_zip(offline_dir, offline_archive_file_name):
    comet_zip = get_offline_archive(offline_dir, offline_archive_file_name)

    assert OFFLINE_EXPERIMENT_MESSAGES_JSON_FILE_NAME in comet_zip.namelist()

    # Extract the messages.json
    comet_zip.extract(OFFLINE_EXPERIMENT_MESSAGES_JSON_FILE_NAME, path=offline_dir)

    json_file_path = os.path.join(
        offline_dir, OFFLINE_EXPERIMENT_MESSAGES_JSON_FILE_NAME
    )
    with open(json_file_path) as messages_file:
        lines = messages_file.readlines()

    return lines
