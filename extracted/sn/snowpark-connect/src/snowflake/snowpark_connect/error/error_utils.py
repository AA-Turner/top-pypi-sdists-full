#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Spark error references:
https://github.com/apache/spark/blob/master/docs/sql-error-conditions.md
https://github.com/apache/spark/tree/master/sql/catalyst/src/main/scala/org/apache/spark/sql/errors
https://github.com/apache/spark/blob/master/common/utils/src/main/resources/error/error-conditions.json
"""

import json
import pathlib
import re
import threading
import traceback

import jpype
from google.protobuf import any_pb2
from google.rpc import code_pb2, error_details_pb2, status_pb2
from pyspark.errors import TempTableAlreadyExistsException
from pyspark.errors.error_classes import ERROR_CLASSES_MAP
from pyspark.errors.exceptions.base import (
    AnalysisException,
    ArithmeticException,
    ArrayIndexOutOfBoundsException,
    IllegalArgumentException,
    NumberFormatException,
    ParseException,
    PySparkException,
    PythonException,
    SparkRuntimeException,
    UnsupportedOperationException,
)
from pyspark.errors.exceptions.connect import SparkConnectGrpcException
from snowflake.core.exceptions import NotFoundError

from snowflake.connector.errors import ProgrammingError
from snowflake.snowpark.exceptions import SnowparkClientException, SnowparkSQLException
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_mapping import ERROR_MAPPINGS_JSON

# Thread-local storage for custom error codes when we can't attach them directly to exceptions
_thread_local = threading.local()

# The JSON string in error_mapping.py is a copy of https://github.com/apache/spark/blob/master/common/utils/src/main/resources/error/error-conditions.json.
# The file doesn't have to be synced with spark latest main. Just update it when required.
current_dir = pathlib.Path(__file__).parent.resolve()
ERROR_CLASSES_MAP.update(json.loads(ERROR_MAPPINGS_JSON))

SPARK_PYTHON_TO_JAVA_EXCEPTION = {
    AnalysisException: "org.apache.spark.sql.AnalysisException",
    ParseException: "org.apache.spark.sql.catalyst.parser.ParseException",
    IllegalArgumentException: "java.lang.IllegalArgumentException",
    ArithmeticException: "java.lang.ArithmeticException",
    ArrayIndexOutOfBoundsException: "java.lang.ArrayIndexOutOfBoundsException",
    NumberFormatException: "java.lang.NumberFormatException",
    SparkRuntimeException: "org.apache.spark.SparkRuntimeException",
    SparkConnectGrpcException: "pyspark.errors.exceptions.connect.SparkConnectGrpcException",
    PythonException: "org.apache.spark.api.python.PythonException",
    UnsupportedOperationException: "java.lang.UnsupportedOperationException",
    TempTableAlreadyExistsException: "org.apache.spark.sql.catalyst.analysis.TempTableAlreadyExistsException",
}

TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS = "TABLE_OR_VIEW_NOT_FOUND"

WINDOW_FUNCTION_ANALYSIS_EXCEPTION_SQL_ERROR_CODE = {1005, 2303}
ANALYSIS_EXCEPTION_SQL_ERROR_CODE = {
    904,
    1039,
    1044,
    2002,
    *WINDOW_FUNCTION_ANALYSIS_EXCEPTION_SQL_ERROR_CODE,
}

# utdf related error messages
init_multi_args_exception_pattern = (
    r"__init__\(\) missing \d+ required positional argument"
)
terminate_multi_args_exception_pattern = (
    r"terminate\(\) missing \d+ required positional argument"
)
snowpark_connect_exception_pattern = re.compile(
    r"\[snowpark-connect-exception(?::(\w+))?\]\s*(.+?)'\s*is not recognized"
)
invalid_bit_pattern = re.compile(
    r"Invalid bit position: \d+ exceeds the bit (?:upper|lower) limit",
    re.IGNORECASE,
)
CREATE_SCHEMA_PATTERN = re.compile(r"create\s+schema", re.IGNORECASE)
CREATE_TABLE_PATTERN = re.compile(r"create\s+table", re.IGNORECASE)


def attach_custom_error_code(exception: Exception, custom_error_code: int) -> Exception:
    """
    Attach a custom error code to any exception instance.
    This allows us to add custom error codes to existing PySpark exceptions.
    """
    if not hasattr(exception, "custom_error_code"):
        try:
            exception.custom_error_code = custom_error_code
        except (AttributeError, TypeError):
            # Some exception types (like Java exceptions) don't allow setting custom attributes
            # Store the error code in thread-local storage for later retrieval
            _thread_local.pending_error_code = custom_error_code
    return exception


def contains_udtf_select(sql_string):
    # This function tries to detect if the SQL string contains a UDTF (User Defined Table Function) call.
    # Looks for select FROM TABLE(...) or FROM ( TABLE(...) )
    return bool(
        re.search(
            r"select\s+.*from\s+\(?\s*table\s*\(", sql_string, re.IGNORECASE | re.DOTALL
        )
    )


def _get_converted_known_sql_or_custom_exception(
    ex: Exception,
) -> Exception | None:
    # Use lower-case for case-insensitive matching
    msg = ex.message.lower() if hasattr(ex, "message") else str(ex).lower()
    query = ex.query if hasattr(ex, "query") else ""

    # custom exception
    if "[snowpark_connect::invalid_array_index]" in msg:
        exception = ArrayIndexOutOfBoundsException(
            message='The index <indexValue> is out of bounds. The array has <arraySize> elements. Use the SQL function `get()` to tolerate accessing element at invalid index and return NULL instead. If necessary set "spark.sql.ansi.enabled" to "false" to bypass this error.'
        )
        attach_custom_error_code(exception, ErrorCodes.ARRAY_INDEX_OUT_OF_BOUNDS)
        return exception
    if "[snowpark_connect::invalid_index_of_zero]" in msg:
        exception = SparkRuntimeException(
            message="[INVALID_INDEX_OF_ZERO] The index 0 is invalid. An index shall be either < 0 or > 0 (the first element has index 1)."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        return exception
    if "[snowpark_connect::invalid_index_of_zero_in_slice]" in msg:
        exception = SparkRuntimeException(
            message="Unexpected value for start in function slice: SQL array indices start at 1."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        return exception

    invalid_bit = invalid_bit_pattern.search(msg)
    if invalid_bit:
        exception = IllegalArgumentException(message=invalid_bit.group(0))
        attach_custom_error_code(exception, ErrorCodes.INVALID_FUNCTION_ARGUMENT)
        return exception
    match = snowpark_connect_exception_pattern.search(
        ex.message if hasattr(ex, "message") else str(ex)
    )
    if match:
        class_name = match.group(1)
        message = match.group(2)
        exception_class = (
            globals().get(class_name, SparkConnectGrpcException)
            if class_name
            else SparkConnectGrpcException
        )
        exception = exception_class(message=message)
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        return exception

    if "select with no columns" in msg and contains_udtf_select(query):
        # We try our best to detect if the SQL string contains a UDTF call and the output schema is empty.
        exception = PythonException(
            message=f"[UDTF_RETURN_SCHEMA_MISMATCH] {ex.message}"
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        return exception

    # known sql exception
    if ex.sql_error_code not in (100038, 100037, 100035, 100357):
        return None

    if "(22018): numeric value" in msg:
        exception = NumberFormatException(
            message='[CAST_INVALID_INPUT] Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary setting "spark.sql.ansi.enabled" to "false" may bypass this error.'
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
        return exception
    if "(22018): boolean value" in msg:
        exception = SparkRuntimeException(
            message='[CAST_INVALID_INPUT] Correct the value as per the syntax, or change its target type. Use `try_cast` to tolerate malformed input and return NULL instead. If necessary setting "spark.sql.ansi.enabled" to "false" may bypass this error.'
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CAST)
        return exception
    if "(22007): timestamp" in msg:
        exception = AnalysisException(
            "[DATATYPE_MISMATCH.UNEXPECTED_INPUT_TYPE] Data type mismatch"
        )
        attach_custom_error_code(exception, ErrorCodes.TYPE_MISMATCH)
        return exception

    if getattr(ex, "sql_error_code", None) == 100357:
        if re.search(init_multi_args_exception_pattern, msg):
            exception = PythonException(
                message=f"[UDTF_EXEC_ERROR] User defined table function encountered an error in the init method {ex.message}"
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            return exception
        if re.search(terminate_multi_args_exception_pattern, msg):
            exception = PythonException(
                message=f"[UDTF_EXEC_ERROR] User defined table function encountered an error in the terminate method: {ex.message}"
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            return exception

        if "failed to split string, provided pattern:" in msg:
            exception = IllegalArgumentException(
                message=f"Failed to split string using provided pattern. {ex.message}"
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            return exception

        if "100357" in msg and "wrong tuple size for returned value" in msg:
            exception = PythonException(
                message=f"[UDTF_RETURN_SCHEMA_MISMATCH] The number of columns in the result does not match the specified schema. {ex.message}"
            )
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            return exception

        if "100357 (p0000): python interpreter error:" in msg:
            if "in eval" in msg:
                exception = PythonException(
                    message=f"[UDTF_EXEC_ERROR] User defined table function encountered an error in the 'eval' method: error. {ex.message}"
                )
                attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                return exception

            if "in terminate" in msg:
                exception = PythonException(
                    message=f"[UDTF_EXEC_ERROR] User defined table function encountered an error in the 'terminate' method: terminate error. {ex.message}"
                )
                attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                return exception

            if "object is not iterable" in msg and contains_udtf_select(query):
                exception = PythonException(
                    message=f"[UDTF_RETURN_NOT_ITERABLE] {ex.message}"
                )
                attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
                return exception

            exception = PythonException(message=f"{ex.message}")
            attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
            return exception

    return None


def _sanitize_custom_error_message(msg):
    if "[snowpark_connect::unsupported_operation]" in msg:
        return (
            msg.replace("[snowpark_connect::unsupported_operation] ", ""),
            ErrorCodes.UNSUPPORTED_OPERATION,
        )
    if "[snowpark_connect::internal_error]" in msg:
        return (
            msg.replace("[snowpark_connect::internal_error] ", ""),
            ErrorCodes.INTERNAL_ERROR,
        )
    if "[snowpark_connect::invalid_operation]" in msg:
        return (
            msg.replace("[snowpark_connect::invalid_operation] ", ""),
            ErrorCodes.INVALID_OPERATION,
        )
    if "[snowpark_connect::type_mismatch]" in msg:
        return (
            msg.replace("[snowpark_connect::type_mismatch] ", ""),
            ErrorCodes.TYPE_MISMATCH,
        )
    if "[snowpark_connect::invalid_input]" in msg:
        return (
            msg.replace("[snowpark_connect::invalid_input] ", ""),
            ErrorCodes.INVALID_INPUT,
        )
    if "[snowpark_connect::unsupported_type]" in msg:
        return (
            msg.replace("[snowpark_connect::unsupported_type] ", ""),
            ErrorCodes.UNSUPPORTED_TYPE,
        )
    return msg, None


def build_grpc_error_response(ex: Exception) -> status_pb2.Status:
    # Lazy import to avoid circular dependency
    from snowflake.snowpark_connect.config import global_config

    include_stack_trace = (
        global_config.get("spark.sql.pyspark.jvmStacktrace.enabled")
        if hasattr(global_config, "spark.sql.pyspark.jvmStacktrace.enabled")
        else False
    )
    message: str | None = None

    if isinstance(ex, SnowparkClientException):
        # exceptions thrown from snowpark
        spark_java_classes = []
        match ex:
            case SnowparkSQLException():
                if ex.sql_error_code in ANALYSIS_EXCEPTION_SQL_ERROR_CODE:
                    # Creation of schema that already exists
                    if ex.sql_error_code == 2002 and "already exists" in str(ex):
                        if CREATE_SCHEMA_PATTERN.search(ex.query):
                            spark_java_classes.append(
                                "org.apache.spark.sql.catalyst.analysis.NamespaceAlreadyExistsException"
                            )
                        elif CREATE_TABLE_PATTERN.search(ex.query):
                            spark_java_classes.append(
                                "org.apache.spark.sql.catalyst.analysis.TableAlreadyExistsException"
                            )
                    # Data type mismatch, invalid window function
                    spark_java_classes.append("org.apache.spark.sql.AnalysisException")
                elif ex.sql_error_code == 100051:
                    spark_java_classes.append("java.lang.ArithmeticException")
                    ex = ArithmeticException(
                        error_class="DIVIDE_BY_ZERO",
                        message_parameters={"config": '"spark.sql.ansi.enabled"'},
                    )
                    attach_custom_error_code(ex, ErrorCodes.DIVISION_BY_ZERO)
                elif ex.sql_error_code in (100096, 100040):
                    # Spark seems to want the Java base class instead of org.apache.spark.sql.SparkDateTimeException
                    # which is what should really be thrown
                    spark_java_classes.append("java.time.DateTimeException")
                elif (
                    spark_ex := _get_converted_known_sql_or_custom_exception(ex)
                ) is not None:
                    ex = spark_ex
                    spark_java_classes.append(SPARK_PYTHON_TO_JAVA_EXCEPTION[type(ex)])
                elif ex.sql_error_code == 2043:
                    spark_java_classes.append(
                        "org.apache.spark.sql.catalyst.analysis.NoSuchDatabaseException"
                    )
                    spark_java_classes.append("org.apache.spark.sql.AnalysisException")
                    message = f"does_not_exist: {str(ex)}"
                else:
                    if ex.sql_error_code == 100357:
                        # This is to handle cases that are not covered in _get_converted_known_sql_or_custom_exception for 100357.
                        spark_java_classes.append(
                            "org.apache.spark.SparkRuntimeException"
                        )
                    else:
                        # not all SnowparkSQLException correspond to QueryExecutionException. E.g., table or view not found is
                        # AnalysisException. We can gradually build a mapping if we want. The first naive version just maps
                        # to QueryExecutionException.
                        spark_java_classes.append(
                            "org.apache.spark.sql.execution.QueryExecutionException"
                        )
            case SnowparkClientException():
                # catch all
                pass

        metadata = {"classes": json.dumps(spark_java_classes)}
        if include_stack_trace:
            metadata["stackTrace"] = "".join(
                traceback.TracebackException.from_exception(ex).format()
            )
        error_info = error_details_pb2.ErrorInfo(
            reason=ex.__class__.__name__,
            domain="snowflake.snowpark",
            metadata=metadata,
        )
    elif isinstance(ex, PySparkException):
        # pyspark exceptions thrown in sas layer

        error_derived_java_class = []
        if ex.error_class == TABLE_OR_VIEW_NOT_FOUND_ERROR_CLASS:
            error_derived_java_class.append(
                "org.apache.spark.sql.catalyst.analysis.NoSuchTableException"
            )

        classes = type(ex).__mro__
        spark_java_classes = [
            SPARK_PYTHON_TO_JAVA_EXCEPTION[clazz]
            for clazz in classes
            if clazz in SPARK_PYTHON_TO_JAVA_EXCEPTION
        ]

        metadata = {
            "classes": json.dumps(error_derived_java_class + spark_java_classes)
        }
        if include_stack_trace:
            metadata["stackTrace"] = "".join(
                traceback.TracebackException.from_exception(ex).format()
            )

        error_info = error_details_pb2.ErrorInfo(
            reason=ex.__class__.__name__,
            domain="org.apache.spark",
            metadata=metadata,
        )
    elif isinstance(ex, NotFoundError) or (
        isinstance(ex, ProgrammingError) and ex.errno == 2043
    ):
        if isinstance(ex, ProgrammingError) and ex.errno == 2043:
            message = f"does_not_exist: {str(ex)}"
        metadata = {"classes": '["org.apache.spark.sql.AnalysisException"]'}
        if include_stack_trace:
            metadata["stackTrace"] = "".join(
                traceback.TracebackException.from_exception(ex).format()
            )
        error_info = error_details_pb2.ErrorInfo(
            reason=ex.__class__.__name__,
            domain="org.apache.spark",
            metadata=metadata,
        )
    elif isinstance(ex, jpype.JException):
        java_class = ex.getClass().getName()
        metadata = {"classes": json.dumps([java_class])}
        error_info = error_details_pb2.ErrorInfo(
            reason=java_class,
            domain="org.apache.spark",
            metadata=metadata,
        )
    else:
        # unexpected exception types
        error_info = error_details_pb2.ErrorInfo(
            reason=ex.__class__.__name__,
            domain="snowflake.sas",
        )

    if message is None:
        message = str(ex)

    custom_error_code = None

    # attach error code using visa exception message
    message, custom_error_code_from_msg = _sanitize_custom_error_message(message)

    # Check if exception already has a custom error code, if not add INTERNAL_ERROR as default
    if not hasattr(ex, "custom_error_code") or ex.custom_error_code is None:
        attach_custom_error_code(
            ex,
            ErrorCodes.INTERNAL_ERROR
            if custom_error_code_from_msg is None
            else custom_error_code_from_msg,
        )

    # Get the custom error code from the exception or thread-local storage
    custom_error_code = getattr(ex, "custom_error_code", None) or getattr(
        _thread_local, "pending_error_code", None
    )

    # Clear thread-local storage after retrieving the error code
    if hasattr(_thread_local, "pending_error_code"):
        delattr(_thread_local, "pending_error_code")

    separator = "==========================================="
    error_code_added_message = f"\n{separator}\nSNOWPARK CONNECT ERROR CODE: {custom_error_code}\n{separator}\n{message}"

    detail = any_pb2.Any()
    detail.Pack(error_info)

    rich_status = status_pb2.Status(
        code=code_pb2.INTERNAL, message=error_code_added_message, details=[detail]
    )
    return rich_status


class SparkException:
    """
    This class is used to mock exceptions created by PySpark / Spark backend in SAS layer.
    """

    @staticmethod
    def unpivot_requires_value_columns():
        return AnalysisException(
            error_class="UNPIVOT_REQUIRES_VALUE_COLUMNS", message_parameters={}
        )

    @staticmethod
    def unpivot_value_data_type_mismatch(types: str):
        return AnalysisException(
            error_class="UNPIVOT_VALUE_DATA_TYPE_MISMATCH",
            message_parameters={"types": types},
        )

    @staticmethod
    def implicit_cartesian_product(join_type: str):
        return AnalysisException(
            error_class="_LEGACY_ERROR_TEMP_1211",
            message_parameters={"joinType": join_type, "leftPlan": "leftPlan"},
        )

    @staticmethod
    def invalid_ranking_function_window_frame(
        window_frame: str,
        required: str = "specifiedwindowframe(RowFrame, unboundedpreceding$(), currentrow$()",
    ):
        return AnalysisException(
            error_class="_LEGACY_ERROR_TEMP_1036",
            message_parameters={"wf": window_frame, "required": required},
        )

    @staticmethod
    def snowpark_ddl_parser_exception(ddl: str):
        return ParseException(
            error_class="UNSUPPORTED_DATA_TYPE", message_parameters={"data_type": ddl}
        )
