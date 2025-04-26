import atexit
import logging
import os
import platform
import traceback
from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Optional

import tecton_core.tecton_pendulum as pendulum
from tecton import version
from tecton._internals import metadata_service
from tecton._internals.env_utils import get_current_username
from tecton_core import conf
from tecton_proto.amplitude import client_logging__client_pb2 as client_logging_pb2
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


SINGLE_POSITIONAL_RETURN_VALUE_NAME = "0"

logger = logging.getLogger(__name__)


@dataclass
class StateUpdateEventMetrics:
    """Metrics to log to Amplitude for tecton plan, apply, delete."""

    num_total_fcos: int
    num_fcos_changed: int
    suppress_recreates: bool
    json_out: bool
    error_message: Optional[str]
    num_warnings: int

    @classmethod
    def from_error_message(cls, error_message: str, suppress_recreates: bool = False, json_out: bool = False):
        return cls(-1, -1, suppress_recreates, json_out, error_message, 0)


@dataclass
class StateUpdateResult:
    """Contains metrics to log to amplitude, and fields to verify correctness in tests"""

    # Used in production - event sent to amplitude
    state_update_event_metrics: StateUpdateEventMetrics

    # Only used in tests - to verify plan output correctness, check for warnings, etc.
    success_response: Optional[metadata_service_pb2.QueryStateUpdateResponseV2]
    error_message: Optional[str] = None

    @classmethod
    def from_error_message(cls, error_message: str, suppress_recreates: bool = False, json_out: bool = False):
        return cls(
            state_update_event_metrics=StateUpdateEventMetrics.from_error_message(
                error_message, suppress_recreates, json_out
            ),
            success_response=None,
            error_message=error_message,
        )


class AnalyticsLogger(object):
    """
    Conventions for logging parameters and return values:
    - `self` object of instance methods is logged under "self" name
    - Positional return values are logged under position index names, e.g., "0", "1", etc.
    """

    _shutting_down = False

    def __init__(self):
        # This executor submits requests to MDS via RPC in a different thread; however when the process is terminated
        # the executor joins on all outstanding threads and this may but the process in a bad state and
        # prevent shutdown. This happens most commonly on CI environments, where we don't need analytics events.
        # So we choose to disable the analytics logging there.
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._enabled = os.getenv("TEST_WORKSPACE") is None

        def cleanup():
            self._shutting_down = True

        atexit.register(cleanup)

    def _submit(self, request: metadata_service_pb2.IngestClientLogsRequest):
        if not self._enabled:
            return
        self._executor.submit(self._send_sdk_logs_to_mds, request)

    def log_method_entry(self, trace_id, obj, method, args, kwargs, arg_names):
        try:
            request = self._create_method_entry_request(trace_id, obj, method, args, kwargs, arg_names)
            self._submit(request)
        except Exception as e:
            logger.debug("Logging error: %s", e)

    def log_method_return(self, trace_id, obj, method, return_value, execution_time, exception: Optional[Exception]):
        try:
            request = self._create_method_return_request(trace_id, obj, method, return_value, execution_time, exception)
            self._submit(request)
        except Exception as e:
            logger.debug("Logging error: %s", e)

    @staticmethod
    def _create_sdk_base_request(trace_id, obj, method) -> metadata_service_pb2.IngestClientLogsRequest:
        """
        NOTE: do not use `conf.py` here as this will increase the latency for SDK calls
        """
        request = metadata_service_pb2.IngestClientLogsRequest()
        data = request.sdk_method_invocation
        data.trace_id = trace_id
        data.time.FromDatetime(pendulum.now("UTC"))
        data.user_id = get_current_username()
        data.log_level = logging.getLevelName(logging.getLogger("tecton").getEffectiveLevel())
        data.sdk_version = version.get_semantic_version()
        data.python_version = platform.python_version()
        if obj:
            method_class = obj if isinstance(obj, type) else type(obj)
            data.class_name = method_class.__name__
            data.method_name = method.__name__
            # Checking the type of the object causes a dependency conflict.
            if hasattr(obj, "info"):
                data.is_local_fco = obj.info._is_local_object
            else:
                data.is_local_fco = False
        else:
            data.method_name = method.__qualname__
        return request

    @staticmethod
    def _create_method_entry_request(
        trace_id, obj, method, args, kwargs, arg_names
    ) -> metadata_service_pb2.IngestClientLogsRequest:
        """
        NOTE: do not use `conf.py` here as this will increase the latency for SDK calls
        """
        request = AnalyticsLogger._create_sdk_base_request(trace_id, obj, method)
        data = request.sdk_method_invocation
        data.type = client_logging_pb2.CLIENT_LOG_MESSAGE_TYPE_METHOD_ENTRY
        is_class_method = isinstance(obj, type)
        if not is_class_method:
            # the method might be a constructor, in that case __str__ may not yet work in an
            # uninitialized object
            try:
                self_str = str(obj)
            except Exception as e:
                self_str = f"<failed to convert {type(obj)} to str>"
            AnalyticsLogger._add_value(data, "self", self_str)

        AnalyticsLogger._add_values(data, args, arg_names)
        AnalyticsLogger._add_values(data, kwargs)
        return request

    @staticmethod
    def _create_method_return_request(
        trace_id, obj, method, return_value, execution_time, exception: Optional[Exception]
    ) -> metadata_service_pb2.IngestClientLogsRequest:
        """
        NOTE: do not use `conf.py` here as this will increase the latency for SDK calls
        """
        request = AnalyticsLogger._create_sdk_base_request(trace_id, obj, method)
        data = request.sdk_method_invocation
        data.type = client_logging_pb2.CLIENT_LOG_MESSAGE_TYPE_METHOD_RETURN
        data.execution_time.FromTimedelta(execution_time)
        AnalyticsLogger._add_values(data, return_value)
        if exception:
            AnalyticsLogger._set_error(data.error, exception)
        return request

    def _send_sdk_logs_to_mds(self, request: metadata_service_pb2.IngestClientLogsRequest):
        if self._shutting_down:
            return
        try:
            metadata_service.instance().IngestClientLogs(request, timeout_sec=5.0)
        except Exception as e:
            logger.debug("Logging error: %s", e)

    @staticmethod
    def _add_values(data: client_logging_pb2.SDKMethodInvocation, values, positional_value_names=None):
        if values is None:
            return
        if isinstance(values, str):
            AnalyticsLogger._add_value(data, SINGLE_POSITIONAL_RETURN_VALUE_NAME, values)
        elif isinstance(values, dict):
            for k, v in values.items():
                AnalyticsLogger._add_value(data, k, v)
        elif isinstance(values, Iterable):
            for i, value in enumerate(values):
                name = positional_value_names[i] if positional_value_names else str(i)
                AnalyticsLogger._add_value(data, name, value)
        else:
            AnalyticsLogger._add_value(data, SINGLE_POSITIONAL_RETURN_VALUE_NAME, values)

    @staticmethod
    def _add_value(data: client_logging_pb2.SDKMethodInvocation, name, value):
        value_record = data.params_or_return_values.add()
        value_record.name = name
        value_record.value = str(value)

    @staticmethod
    def _set_error(data: client_logging_pb2.ErrorLog, e: BaseException):
        data.message = str(e)
        data.stacktrace = str(traceback.format_tb(e.__traceback__))
        if e.__cause__:
            AnalyticsLogger._set_error(data.cause, e.__cause__)

    def log_cli_event(
        self,
        event_name: str,
        execution_time: pendulum.Period,
        options: Optional[Dict[str, Any]],
        state_update_event: Optional[StateUpdateEventMetrics] = None,
    ):
        request = metadata_service_pb2.IngestAnalyticsRequest(workspace=conf.get_or_none("TECTON_WORKSPACE"))
        event = request.events.add()
        # We do not populate user_id since it is not available in the CLI, we will backfill it in the backend
        event.event_type = event_name
        event.platform = "CLI"
        event.timestamp = int(pendulum.now("UTC").timestamp()) * 1000
        event.os_name = platform.system()
        event.os_version = platform.release()
        event.event_properties.sdk_version = version.get_semantic_version()
        event.event_properties.python_version = platform.python_version()
        event.event_properties.execution_time.FromTimedelta(execution_time)
        if options is not None:
            for k, v in options.items():
                event.event_properties.params[k] = str(v)
        if state_update_event:
            if state_update_event.error_message:
                event.event_properties.success = False
                event.event_properties.error_message = state_update_event.error_message
                event.event_properties.suppress_recreates = state_update_event.suppress_recreates
            else:
                event.event_properties.success = True
                event.event_properties.num_total_fcos = state_update_event.num_total_fcos
                event.event_properties.num_fcos_changed = state_update_event.num_fcos_changed
                event.event_properties.suppress_recreates = state_update_event.suppress_recreates
                event.event_properties.json_out = state_update_event.json_out
                event.event_properties.num_warnings = state_update_event.num_warnings
        # Not using the async threadpool since CLI is a not a long-running process and we would lose events on exit
        self._send_cli_logs_to_mds(request)

    def _send_cli_logs_to_mds(self, request: metadata_service_pb2.IngestAnalyticsRequest):
        if self._shutting_down:
            return
        try:
            metadata_service.instance().IngestAnalytics(request, timeout_sec=5.0)
        except Exception as e:
            logger.debug("Logging error (cli): %s", e)
