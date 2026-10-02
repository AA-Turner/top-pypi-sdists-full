import logging
import re as regex_extractor
import traceback
from typing import Optional

from newtools.optional_imports import json_log_formatter

"""
Constant keys for the persistent fields to be logged by every application.
"""
APPLICATION_DOMAIN_KEY = 'application_domain'
APPLICATION_NAME_KEY = 'application_name'
USE_CASE_NAME_KEY = 'use_case_name'
APPLICATION_REQUEST_ID_KEY = 'application_request_id'

START_TIME_KEY = 'start_time'
END_TIME_KEY = 'end_time'
TOTAL_EXEC_TIME_IN_SECS_KEY = 'total_execution_time_in_secs'
TOTAL_EXEC_TIME_IN_MILLI_SECS_KEY = 'total_execution_time_in_milli_secs'

APPLICATION_STATUS_KEY = 'application_status'

APPLICATION_STATUS_SUCCESS_KEY = 'Success'
APPLICATION_STATUS_FAILURE_KEY = 'Failure'

TOTAL_RECORDS_PROCESSED_KEY = 'total_records_processed'
EXCESS_METRICS_KEY = 'excess_metrics'

"""
Constants used by the logger library to extract and save the error details to the error log message.
"""
CLASS_NAME = 'ClassName'
ERROR_MESSAGE = 'ErrorMessage'
ERROR_STACK_TRACE = 'ErrorStackTrace'
DEFAULT_CLASS_NAME = 'None'

CLASS_NAME_SEARCH_PATTERN = "<class '([^\'>]+)"

LOG_LEVEL_KEY = 'log_level'

LOG_LEVEL_INFO = 'INFO'
LOG_LEVEL_DEBUG = 'DEBUG'
LOG_LEVEL_WARN = 'WARN'
LOG_LEVEL_ERROR = 'ERROR'


def _extract_exception(exception_details_dict, exception_object):
    """
    This function adds the exception extracted details to the log message. This function
    overrides the current exception stack details persisted with the new exception stack details if
    provided any.

    :param exception_object: exception object to retrieve exception details and stack trace.
    """
    class_name_search = regex_extractor.search(CLASS_NAME_SEARCH_PATTERN, str(type(exception_object)))

    exception_details_dict[CLASS_NAME] = class_name_search.group(1) if class_name_search else DEFAULT_CLASS_NAME
    exception_details_dict[ERROR_MESSAGE] = str(exception_object)
    exception_details_dict[ERROR_STACK_TRACE] = str(traceback.format_exc())


class JSONLogger:
    """
    This is a wrapper of logging library where the logs are displayed in the json format.

    This wrapper has the feature of Persistent logging and can be used optionally as well.
    """

    def __init__(
        self,
        logger_name: str,
        logging_level: Optional = logging.INFO,
        log_file_path: Optional[str] = None,
        file_only: Optional[bool] = False
    ):
        """
        This class creates a logging instance with json formatted messages and adds an optional feature
        for persisting any fields onto the log messages as and when required.

        :param logger_name: Any string with valid understandable name.
        :param logging_level: Any kind of logging level from where the lowest prioritized log level is required
            if used logging.DEBUG - All levels Debug, Info, Warning and Error logs are logged.
            if used logging.INFO - levels Info, Warning and Error logs are logged.
            if used logging.WARNING - levels Warning and Error logs are logged.
            if used logging.ERROR - Only Error logs are logged.
        :param log_file_path: In case to save the logs onto a json file.
        :param file_only: Whether to only save to the log file path (by default we save to the log file and stream)
        """
        self._persistent_fields = dict()

        self._application_name = logger_name

        logger_instance = logging.getLogger(self._application_name)
        # Disabled propagation of logs on to console by the root logger
        logger_instance.propagate = False
        # Cleared all the pre-existing handlers in the logger
        logger_instance.handlers.clear()
        # Setting log level to the one specified by the requestor or defaulted to INFO
        logger_instance.setLevel(logging_level)

        self.json_formatter = json_log_formatter.JSONFormatter()

        generic_handler = logging.StreamHandler()
        generic_handler.setFormatter(self.json_formatter)

        if not file_only:
            logger_instance.addHandler(generic_handler)
        if log_file_path:
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(self.json_formatter)
            logger_instance.addHandler(file_handler)

        self._log_instance = logger_instance
        self.add_persistent_field(APPLICATION_NAME_KEY, self._application_name)

    def get_all_persistent_fields(self):
        return self._persistent_fields

    def remove_persistent_field(self, field_name):
        """
        This function helps in removing a key value pair to the persistent field dictionary.

        :param field_name: key to be removed from the persistent field dictionary.

        :return: None
        """
        if APPLICATION_NAME_KEY != field_name:
            self._persistent_fields.pop(field_name, None)

    def remove_all_persistent_fields(self):
        """
        This function helps in removing all key value pairs in the persistent field dictionary.

        :return: None
        """
        self._persistent_fields = dict()
        self.add_persistent_field(APPLICATION_NAME_KEY, self._application_name)

    def add_persistent_field(self, field_name, field_value):
        """
        This function helps in adding a key value pair to the persistent field dictionary.

        :param field_name: key to be saved in the persistent field dictionary.
        :param field_value: value to be saved for the given key

        :return: None
        """
        self._persistent_fields[field_name] = field_value

    def add_persistent_fields(self, **fields):
        """
        This function helps in adding a set of key value pairs to the persistent field dictionary.

        :param fields: A set of keyword arguments to be saved to the persistent field dictionary.

        :return: None
        """
        self._persistent_fields = {**self._persistent_fields, **fields}

    def generate_time_spent(self, application_start_time, application_end_time, in_milli_secs=False):
        """
        This function helps in calculating the total execution time of the application and adds it to the persistent
        fields of the logger.
        :param application_start_time: datetime.datetime: start time of the application execution.
        :param application_end_time: datetime.datetime: end time of the application execution.
        :param in_milli_secs: Whether to generate time spent in milliseconds or in seconds.
            True for Milli and False for seconds which is default
        """
        if application_start_time and application_end_time:
            total_seconds = (application_end_time - application_start_time).total_seconds()
            if in_milli_secs:
                self._persistent_fields[TOTAL_EXEC_TIME_IN_MILLI_SECS_KEY] = int(total_seconds * 1000)
            else:
                self._persistent_fields[TOTAL_EXEC_TIME_IN_SECS_KEY] = round(total_seconds, 2)
            self._persistent_fields[START_TIME_KEY] = str(application_start_time)
            self._persistent_fields[END_TIME_KEY] = str(application_end_time)

    def _handle_log_parameters(self, excess_persistent_dict, kwargs):
        """
        This function adds excess persistent fields provided to the debug, info, error, warning. Apart from that
        any excess non-persistent fields passed to the below methods will be logged but not persisted.

        :param excess_persistent_dict: excess persistent dict to be added to instance persistence dictionary.
        :param kwargs: Excess non-persistent dict to be logged with the log message called for with below methods.

        :return: All persistent and non-persistent key value pairs which are to be logged.
        """
        if excess_persistent_dict is not None:
            self.add_persistent_fields(**excess_persistent_dict)
        logging_params = {**self._persistent_fields, **kwargs}
        return logging_params

    def _process_extra_parameters(self, exception_object, excess_persistent_dict, kwargs):
        exception_details_dict = dict()
        if exception_object is not None:
            _extract_exception(exception_details_dict, exception_object)
        logging_params = self._handle_log_parameters(excess_persistent_dict, {**kwargs, **exception_details_dict})
        return logging_params

    def debug(self, message, excess_persistent_dict=None, **kwargs):
        logging_params = self._handle_log_parameters(excess_persistent_dict, kwargs)
        logging_params[LOG_LEVEL_KEY] = LOG_LEVEL_DEBUG
        self._log_instance.debug(message, extra=logging_params)

    def info(self, message, excess_persistent_dict=None, **kwargs):
        logging_params = self._handle_log_parameters(excess_persistent_dict, kwargs)
        logging_params[LOG_LEVEL_KEY] = LOG_LEVEL_INFO
        self._log_instance.info(message, extra=logging_params)

    def warning(self, message, excess_persistent_dict=None, exception_object=None, **kwargs):
        logging_params = self._process_extra_parameters(exception_object, excess_persistent_dict, kwargs)
        logging_params[LOG_LEVEL_KEY] = LOG_LEVEL_WARN
        self._log_instance.warning(message, extra=logging_params)

    def error(self, message, excess_persistent_dict=None, exception_object=None, **kwargs):
        logging_params = self._process_extra_parameters(exception_object, excess_persistent_dict, kwargs)
        logging_params[LOG_LEVEL_KEY] = LOG_LEVEL_ERROR
        self._log_instance.error(message, extra=logging_params)
