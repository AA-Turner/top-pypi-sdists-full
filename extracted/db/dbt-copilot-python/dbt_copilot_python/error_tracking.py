import logging
import os
import sys
import traceback
from functools import lru_cache

from ddtrace.trace import tracer


class DatadogErrorTrackingFilter(logging.Filter):
    def __init__(self, name: str = "") -> None:
        self._working_directory = os.getcwd()
        super().__init__(name)

    def filter(self, record):
        if record.levelno >= logging.ERROR:
            # Escape quickly if inside of a handled exception, use native
            # functionality to surface handled errors
            # https://docs.datadoghq.com/error_tracking/backend/capturing_handled_errors/python/#automatic-instrumentation
            exc_info = sys.exc_info()
            if any(exc_info):
                return True

            span = tracer.current_span()
            if span:
                span.record_exception(
                    BaseException(record.msg),
                    attributes={
                        "exception.stacktrace": "".join(traceback.format_stack(limit=20)),
                        "exception.type": f"{self._calculate_module_path(record.pathname, record.module, record.funcName)}.LoggedError",
                    },
                )

        return True

    @lru_cache(maxsize=32)
    def _calculate_module_path(self, pathname: str, module: str, func_name: str) -> str:
        path_from_project_root = pathname.replace(self._working_directory, "")

        if path_from_project_root != pathname:
            module_path_with_function = path_from_project_root.split("/")[1:-1]
        else:
            module_path_with_function = path_from_project_root.split("/")[1:]

        module_path_with_function.extend([module, func_name])

        return ".".join(module_path_with_function)
