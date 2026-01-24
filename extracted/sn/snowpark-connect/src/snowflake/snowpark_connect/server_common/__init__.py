#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""
Common server utilities shared between SAS server and client server.

This module contains shared constants, global state management, URL handling,
gRPC configuration, and session management code that is used by both
the main SAS server (server.py) and the thin client's server (client/server.py).
"""

import atexit
import os
import re
import signal
import socket
import subprocess
import tempfile
import threading
import urllib.parse
from contextlib import suppress
from typing import Any, Dict, List, Optional, Tuple

import grpc
import pyspark
from pyspark.conf import SparkConf
from pyspark.errors import PySparkValueError
from pyspark.sql.connect.client.core import ChannelBuilder
from pyspark.sql.connect.session import SparkSession

from packaging import version
from snowflake import snowpark
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.utils.env_utils import get_int_from_env
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

DEFAULT_PORT = 15002

# https://github.com/apache/spark/blob/v3.5.3/connector/connect/common/src/main/scala/org/apache/spark/sql/connect/common/config/ConnectCommon.scala#L21
_SPARK_CONNECT_GRPC_MAX_MESSAGE_SIZE = 128 * 1024 * 1024
# TODO: Verify if we want to configure it via env variables.
_SPARK_CONNECT_GRPC_MAX_METADATA_SIZE = 64 * 1024  # 64kb

# Thread-local storage for client telemetry context
_client_telemetry_context = threading.local()

_server_running: threading.Event = threading.Event()
_server_error: bool = False
_server_url: Optional[str] = None
_client_url: Optional[str] = None


def get_server_running() -> threading.Event:
    """Get the server running event."""
    return _server_running


def get_server_error() -> bool:
    """Get the server error flag."""
    return _server_error


def set_server_error(error: bool) -> None:
    """Set the server error flag."""
    global _server_error
    _server_error = error


def _reset_server_run_state() -> None:
    """
    Reset server global state to the initial blank slate state.
    Called after the startup error is caught and handled/logged.
    """
    global _server_running, _server_error, _server_url, _client_url
    _server_running.clear()
    _server_error = False
    _server_url = None
    _client_url = None


def _stop_server(stop_event: threading.Event, server: grpc.Server) -> None:
    """Wait for stop event and then stop the server."""
    stop_event.wait()
    server.stop(0)
    _reset_server_run_state()
    logger.info("server stop sent")


def _get_default_grpc_options() -> List[Tuple[str, Any]]:
    """Get default gRPC server options."""
    grpc_max_msg_size = get_int_from_env(
        "SNOWFLAKE_GRPC_MAX_MESSAGE_SIZE",
        _SPARK_CONNECT_GRPC_MAX_MESSAGE_SIZE,
    )
    grpc_max_metadata_size = get_int_from_env(
        "SNOWFLAKE_GRPC_MAX_METADATA_SIZE",
        _SPARK_CONNECT_GRPC_MAX_METADATA_SIZE,
    )
    server_options = [
        (
            "grpc.max_send_message_length",
            grpc_max_msg_size,
        ),
        (
            "grpc.max_receive_message_length",
            grpc_max_msg_size,
        ),
        (
            "grpc.max_metadata_size",
            grpc_max_metadata_size,
        ),
        (
            "grpc.absolute_max_metadata_size",
            grpc_max_metadata_size * 2,
        ),
    ]

    # try to adjust max message size for clients in the same process
    from pyspark.sql.connect.client import ChannelBuilder

    ChannelBuilder.MAX_MESSAGE_LENGTH = grpc_max_msg_size

    return server_options


def get_grpc_max_message_size() -> int:
    """Get the current gRPC max message size."""
    return _SPARK_CONNECT_GRPC_MAX_MESSAGE_SIZE


def set_grpc_max_message_size(size: int) -> None:
    """Set the gRPC max message size."""
    global _SPARK_CONNECT_GRPC_MAX_MESSAGE_SIZE
    _SPARK_CONNECT_GRPC_MAX_MESSAGE_SIZE = size


def get_server_url() -> str:
    """Get the server URL."""
    global _server_url
    if not _server_url:
        exception = RuntimeError("Server URL not set")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
    return _server_url


def get_client_url() -> str:
    """Get the client URL."""
    global _client_url
    if not _client_url:
        exception = RuntimeError("Client URL not set")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
    return _client_url


def _check_port_is_free(port: int) -> None:
    """Check if a TCP port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        if s.connect_ex(("127.0.0.1", port)) == 0:
            exception = RuntimeError(f"TCP port {port} is already in use")
            attach_custom_error_code(exception, ErrorCodes.TCP_PORT_ALREADY_IN_USE)
            raise exception


def _set_remote_url(remote_url: str):
    """Set server and client URLs from a remote URL string."""
    global _server_url, _client_url
    _client_url = remote_url
    parsed_url = urllib.parse.urlparse(remote_url)
    if parsed_url.scheme == "sc":
        _server_url = parsed_url.netloc
        server_port = parsed_url.port or DEFAULT_PORT
        _check_port_is_free(server_port)
    elif parsed_url.scheme == "unix":
        _server_url = remote_url.split("/;")[0]
    else:
        exception = RuntimeError(f"Invalid Snowpark Connect URL: {remote_url}")
        attach_custom_error_code(exception, ErrorCodes.INVALID_SPARK_CONNECT_URL)
        raise exception


def _set_server_tcp_port(server_port: int):
    """Set server and client URLs from a TCP port."""
    global _server_url, _client_url
    _check_port_is_free(server_port)
    _server_url = f"[::]:{server_port}"
    _client_url = f"sc://127.0.0.1:{server_port}"


def _set_server_unix_domain_socket(path: str):
    """Set server and client URLs from a Unix domain socket path."""
    global _server_url, _client_url
    _server_url = f"unix:{path}"
    _client_url = f"unix:{path}"


def _make_unix_domain_socket() -> str:
    """Create a unique Unix domain socket path."""
    parent_dir = tempfile.mkdtemp()
    server_path = os.path.join(parent_dir, "snowflake_sas_grpc.sock")
    atexit.register(_cleanup_unix_domain_socket, server_path)
    return server_path


def _cleanup_unix_domain_socket(server_path: str) -> None:
    """Clean up a Unix domain socket and its parent directory."""
    parent_dir = os.path.dirname(server_path)
    if os.path.exists(server_path):
        os.remove(server_path)
    if os.path.exists(parent_dir):
        os.rmdir(parent_dir)


class UnixDomainSocketChannelBuilder(ChannelBuilder):
    """
    Spark Connect gRPC channel builder for Unix domain sockets.
    """

    def __init__(
        self, url: str = None, channelOptions: Optional[List[Tuple[str, Any]]] = None
    ) -> None:
        if url is None:
            url = get_client_url()
        if url[:6] != "unix:/" or len(url) < 7:
            exception = PySparkValueError(
                error_class="INVALID_CONNECT_URL",
                message_parameters={
                    "detail": "The URL must start with 'unix://'. Please update the URL to follow the correct format, e.g., 'unix://unix_domain_socket_path'.",
                },
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_SPARK_CONNECT_URL)
            raise exception

        # Rewrite the URL to use http as the scheme so that we can leverage
        # Python's built-in parser to parse URL parameters
        fake_url = "http://" + url[6:]
        self.url = urllib.parse.urlparse(fake_url)
        self.params: Dict[str, str] = {}
        self._extract_attributes()

        # Now parse the real unix domain socket URL
        self.url = urllib.parse.urlparse(url)

        GRPC_DEFAULT_OPTIONS = _get_default_grpc_options()

        if channelOptions is None:
            self._channel_options = GRPC_DEFAULT_OPTIONS
        else:
            for option in channelOptions:
                if (
                    option[0] == "grpc.max_send_message_length"
                    or option[0] == "grpc.max_receive_message_length"
                ):
                    # try to adjust max message size for clients in the same process
                    from pyspark.sql.connect.client import ChannelBuilder

                    ChannelBuilder.MAX_MESSAGE_LENGTH = max(
                        ChannelBuilder.MAX_MESSAGE_LENGTH, option[1]
                    )
            self._channel_options = GRPC_DEFAULT_OPTIONS + channelOptions
        # For Spark 4.0 support, but also backwards compatible.
        self._params = self.params

    def _extract_attributes(self) -> None:
        """Extract attributes from parameters.

        This method was copied from
        https://github.com/apache/spark/blob/branch-3.5/python/pyspark/sql/connect/client/core.py

        This is required for Spark 4.0 support, since it is dropped in favor of moving
        the extraction logic into the constructor.
        """
        if len(self.url.params) > 0:
            parts = self.url.params.split(";")
            for p in parts:
                kv = p.split("=")
                if len(kv) != 2:
                    exception = PySparkValueError(
                        error_class="INVALID_CONNECT_URL",
                        message_parameters={
                            "detail": f"Parameter '{p}' should be provided as a "
                            f"key-value pair separated by an equal sign (=). Please update "
                            f"the parameter to follow the correct format, e.g., 'key=value'.",
                        },
                    )
                    attach_custom_error_code(
                        exception, ErrorCodes.INVALID_SPARK_CONNECT_URL
                    )
                    raise exception
                self.params[kv[0]] = urllib.parse.unquote(kv[1])

        netloc = self.url.netloc.split(":")
        if len(netloc) == 1:
            self.host = netloc[0]
            if version.parse(pyspark.__version__) >= version.parse("4.0.0"):
                from pyspark.sql.connect.client.core import DefaultChannelBuilder

                self.port = DefaultChannelBuilder.default_port()
            else:
                self.port = ChannelBuilder.default_port()
        elif len(netloc) == 2:
            self.host = netloc[0]
            self.port = int(netloc[1])
        else:
            exception = PySparkValueError(
                error_class="INVALID_CONNECT_URL",
                message_parameters={
                    "detail": f"Target destination '{self.url.netloc}' should match the "
                    f"'<host>:<port>' pattern. Please update the destination to follow "
                    f"the correct format, e.g., 'hostname:port'.",
                },
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_SPARK_CONNECT_URL)
            raise exception

    # We override this to enable compatibility with Spark 4.0
    host = None

    @property
    def endpoint(self) -> str:
        return f"{self.url.scheme}:{self.url.path}"

    def toChannel(self) -> grpc.Channel:
        return grpc.insecure_channel(self.endpoint, options=self._channel_options)


def get_session(url: Optional[str] = None, conf: SparkConf = None) -> SparkSession:
    """
    Returns spark connect session.

    Parameters:
        url (Optional[str]): Spark connect server URL. Uses default server URL if none is provided.
        conf (SparkConf): Optional Spark configuration.

    Returns:
        A new spark connect session.

    Raises:
        RuntimeError: If Spark Connect server is not started.
    """
    try:
        if not url:
            url = get_client_url()

        if url.startswith("unix:/"):
            b = SparkSession.builder.channelBuilder(UnixDomainSocketChannelBuilder())
        else:
            b = SparkSession.builder.remote(url)

        if conf is not None:
            for k, v in conf.getAll():
                b.config(k, v)

        return b.getOrCreate()
    except Exception as e:
        _reset_server_run_state()
        logger.error(e, exc_info=True)
        attach_custom_error_code(e, ErrorCodes.INTERNAL_ERROR)
        raise e


def _setup_spark_environment(setup_java_home: bool = True) -> None:
    """
    Set up environment variables required for Spark Connect.

    Parameters:
        setup_java_home: If True, configures JAVA_HOME. Set to False for
                        lightweight client servers that don't need JVM.
    """
    if setup_java_home:
        java_home = os.environ.get("JAVA_HOME")
        if java_home is None:
            try:
                # For Notebooks on SPCS
                from jdk4py import JAVA_HOME

                os.environ["JAVA_HOME"] = str(JAVA_HOME)
            except ModuleNotFoundError:
                # For notebooks on Warehouse
                conda_prefix = os.environ.get("CONDA_PREFIX")
                if conda_prefix is not None:
                    os.environ["JAVA_HOME"] = conda_prefix
                    os.environ["JAVA_LD_LIBRARY_PATH"] = os.path.join(
                        conda_prefix, "lib", "server"
                    )
        elif os.name == "nt":
            # We need to check the version of the java executable for Windows
            version = None
            major_version = None
            with suppress(Exception):
                # Construct path to java executable under JAVA_HOME
                java_executable = os.path.join(java_home, "bin", "java.exe")

                result = subprocess.run(
                    [java_executable, "-version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                # java -version outputs to stderr
                version_output = (
                    result.stderr.split("\n")[0]
                    if result.stderr
                    else result.stdout.split("\n")[0]
                )

                version_match = re.search(r'version "([^"]+)"', version_output)
                version = version_match.group(1) if version_match else "unknown"
                logger.info(f"Java version: {version_output}")
                major_version = version.split(".")[0]

            if major_version is None:
                raise RuntimeError(
                    f"Could not determine Java version for JAVA_HOME={java_home}"
                )
            elif int(major_version) < 17:
                raise RuntimeError(
                    f"Java version {version} is not supported (minimum required: Java 17). "
                    "Please set JAVA_HOME to point to Java 17 or higher, or unset JAVA_HOME "
                    f"to use the default Java installation. Current JAVA_HOME={java_home}"
                )
            else:
                logger.warning(
                    f"Using customized Java version for JAVA_HOME={java_home}: {version}"
                )
        logger.info("JAVA_HOME=%s", os.environ.get("JAVA_HOME", "Not defined"))

    os.environ["SPARK_LOCAL_HOSTNAME"] = "127.0.0.1"
    os.environ["SPARK_CONNECT_MODE_ENABLED"] = "1"


def _disable_protobuf_recursion_limit() -> None:
    """
    Disable protobuf recursion limit.

    https://github.com/protocolbuffers/protobuf/blob/960e79087b332583c80537c949621108a85aa442/src/google/protobuf/io/coded_stream.h#L616
    Disable protobuf recursion limit (default 100) because Spark workloads often
    produce deeply nested execution plans. For example:
    - Queries with many unions
    - Complex expressions with multiple levels of nesting
    Without this, legitimate Spark queries would fail with
    `(DecodeError) Error parsing message with type 'spark.connect.Relation'` error.
    See test_sql_resulting_in_nested_protobuf
    """
    from google.protobuf.pyext import cpp_message

    cpp_message._message.SetAllowOversizeProtos(True)


def setup_signal_handlers(stop_event: threading.Event) -> None:
    """Set up signal handlers for graceful shutdown."""

    def make_signal_handler(stop_event):
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, stopping server gracefully...")
            stop_event.set()

        return signal_handler

    try:
        signal_handler = make_signal_handler(stop_event)
        signal.signal(signal.SIGTERM, signal_handler)  # kill <pid>
        signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
        if hasattr(signal, "SIGHUP"):
            signal.signal(signal.SIGHUP, signal_handler)  # Terminal hangup
        logger.info("Signal handlers registered for graceful shutdown")
    except Exception as e:
        logger.warning(f"Failed to register signal handlers: {e}")


def configure_server_url(
    remote_url: Optional[str] = None,
    tcp_port: Optional[int] = None,
    unix_domain_socket: Optional[str] = None,
) -> Optional[str]:
    """
    Configure server URL based on provided parameters or environment.

    Returns the unix_domain_socket path if one was created, None otherwise.
    """
    if len(list(filter(None, [remote_url, tcp_port, unix_domain_socket]))) > 1:
        exception = RuntimeError(
            "Can only set at most one of remote_url, tcp_port, and unix_domain_socket"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_STARTUP_INPUT)
        raise exception

    url_from_env = os.environ.get("SPARK_REMOTE", None)
    created_socket = None

    if remote_url:
        _set_remote_url(remote_url)
    elif tcp_port:
        _set_server_tcp_port(tcp_port)
    elif unix_domain_socket:
        _set_server_unix_domain_socket(unix_domain_socket)
    elif url_from_env:
        # Spark clients use environment variable SPARK_REMOTE to figure out Spark Connect URL
        _set_remote_url(url_from_env)
    else:
        # No connection properties can be found - use Unix Domain Socket as fallback
        if os.name == "nt":
            # Windows does not support unix domain sockets
            _set_server_tcp_port(DEFAULT_PORT)
        else:
            # Generate unique, random UDS port
            created_socket = _make_unix_domain_socket()
            _set_server_unix_domain_socket(created_socket)

    return created_socket


def validate_startup_parameters(
    snowpark_session: Optional[snowpark.Session],
    connection_parameters: Optional[Dict[str, str]],
) -> Optional[snowpark.Session]:
    """
    Validate startup parameters and create snowpark session if needed.

    Returns the snowpark session to use.
    """
    if os.environ.get("SPARK_ENV_LOADED"):
        exception = RuntimeError(
            "Snowpark Connect cannot be run inside of a Spark environment"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_STARTUP_OPERATION)
        raise exception

    if connection_parameters is not None:
        if snowpark_session is not None:
            exception = ValueError(
                "Only specify one of snowpark_session and connection_parameters"
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_STARTUP_INPUT)
            raise exception
        snowpark_session = snowpark.Session.builder.configs(
            connection_parameters
        ).create()

    return snowpark_session
