"""
Vortex Producer client for sending data to Kafka.

This module provides the VortexProducerClient which handles sending messages to Kafka
in the format expected by the Vortex consumer service.

The behavior of the producer can be controlled by setting a few environment variables:

- `VORTEX_DEV_MODE` (default `False`): If set to `true`, the producer will write messages to a JSONL
  file so you can manually inspect them. In dev mode, the producer will not send any messages
  to Vortex.
- `VORTEX_DEV_MODE_OUTPUT_PATH`: The path to the file to write messages to if `VORTEX_DEV_MODE` is
  set to `true`. Note that this file will be appended to, not overwritten, so it can grow quite
  large!
- `VORTEX_IN_CLUSTER_MODE`
- `VORTEX_BASE_URL` (default `https://p.vx.dbt.com`): The base URL of the Vortex API.
- `DD_SERVICE`: The name of the service using this client
- `DD_VERSION`: The version of the service using this client
"""

from __future__ import annotations

import importlib.metadata
import logging
import os
import threading
import time
import uuid
from enum import Enum
from queue import Empty, Full, Queue
from typing import Optional

import google.protobuf.any_pb2
import google.protobuf.message
import requests
from dbtlabs.proto.public.v1.events.vortex_pb2 import VortexMessage, VortexMessageBatch
from google.protobuf.json_format import MessageToJson
from google.protobuf.timestamp_pb2 import Timestamp

from dbtlabs_vortex.common.exceptions import ProducerError, ValidationError
from dbtlabs_vortex.producer.ddtrace import trace

logger = logging.getLogger(__name__)


def _get_import_version(package_name: str) -> str:
    """Get the version of an imported package."""
    try:
        return importlib.metadata.version(package_name)
    except Exception as e:
        logger.warning(f"Failed to get {package_name} version: {e}")
        return "0.0.0"


class ErrorMode(Enum):
    """
    Enum for the error mode of the Vortex producer. There are two modes:

    LOG_AND_CONTINUE (default): Log the error and continue. This is recommended for most
    producers because it allows them to continue processing messages even if one fails
    to send.

    LOG_AND_RAISE: Log the error and raise an exception. This is useful for producers
    that want to surface failures in their work if a message fails to send.
    """

    LOG_AND_CONTINUE = "log_and_continue"
    LOG_AND_RAISE = "log_and_raise"


def log_proto(
    message: google.protobuf.message.Message,
    error_mode: ErrorMode = ErrorMode.LOG_AND_CONTINUE,
    wait_seconds: float = 0.0,
) -> None:
    """
    Utility function for sending a protobuf message to Vortex without calling into the client. Will
    only raise an exception if `error_mode` is `LOG_AND_RAISE`. Otherwise it will log all errors
    and continue so as not to interrupt the program.

    Args:
        message: The protobuf message to log
        error_mode: The error behavior if the message fails to send.
        wait_seconds: The number of seconds to wait for the message to be sent. If the queue
            is full, the message will be dropped. If 0, the send will be non-blocking.

    Returns:
        None

    Example:
    ```python
    from dbtlabs_vortex.producer import log_proto
    from dbtlabs.proto.private.v1.fields.ip_rule_pb2 import Cidr

    log_proto(Cidr(cidr="192.168.1.0/24", ...))
    ```
    """
    VortexProducerClient.log_proto(message, error_mode, wait_seconds)


def shutdown(timeout_seconds: float = 10.0) -> None:
    """
    Shutdown the client.

    This will stop the worker thread and close the queue. It will wait at most
    `timeout_seconds` for the worker thread to flush any unsent messages and close down.

    `timeout_seconds` can be set to fractional seconds if you need to exit quickly.

    If `timeout_seconds` is set to 0 or a negative number, the method will return immediately and
    will not wait for the worker thread to flush any unsent messages.

    Args:
        timeout_seconds: The timeout for the worker thread to shut down.
    """
    VortexProducerClient.shutdown(timeout_seconds)


class VortexProducerClient:
    """
    Client for sending messages to Vortex Kafka topics.

    This client is a singleton that handles buffering messages, batching them, and
    sending them to Vortex.

    You do not need to instantiate this class directly. Instead, call `log_proto` with
    any valid protobuf message from Google's well-known types, or from the dbtlabs
    proto repo.

    Example:
    ```python
    from dbtlabs_vortex import producer
    from dbtlabs.proto.private.v1.fields.ip_rule_pb2 import Cidr

    producer.log_proto(Cidr(cidr="192.168.1.0/24", ...))
    ```
    """

    queue: Queue[Optional[VortexMessage]]
    thread: threading.Thread

    initialized: bool = False
    queue_closed: bool = False
    logs_suppressed: bool = False

    @classmethod
    def log_proto(
        cls,
        message: google.protobuf.message.Message,
        error_mode: ErrorMode = ErrorMode.LOG_AND_CONTINUE,
        wait_seconds: float = 0.0,
    ) -> None:
        """
        Send a protobuf message to Vortex.

        When this method is called, the message is added to an internal queue and a
        background worker thread is started if it is not already running. The background
        worker thread will send the message to Vortex in the background, or if something
        goes wrong, it will follow the error mode specified.

        The default behavior is to never block. If you want to apply backpressure,
        use the `wait_seconds` parameter to block for a fixed interval until the
        queue clears.

        In either case, if the internal queue is full, and a new message cannot be
        added within the specified timeout, the message will be dropped and an error
        will be logged.

        Args:
            message: The protobuf message to log
            error_mode: The error behavior if the message fails to send.
            wait_seconds: The number of seconds to wait for the message to be sent. If the queue
                is full, the message will be dropped.

        Raises:
            `ValidationError`: If the message doesn't meet validation requirements
            `ProducerError`: If there is an error sending the message to Kafka
        """
        with trace("vortex-producer.python.log_proto"):
            try:
                if os.getenv("VORTEX_DEV_MODE") == "true":
                    write_file_path = os.getenv(
                        "VORTEX_DEV_MODE_OUTPUT_PATH", "/tmp/vortex_dev_mode_output.jsonl"
                    )
                    logger.debug("Vortex is in dev mode, writing message to file")
                    converted_message = MessageToJson(message, indent=None).replace("\n", "")
                    with open(write_file_path, "a") as f:
                        f.write(
                            f'{{"type_url": "/{message.DESCRIPTOR.full_name}", "value": {converted_message}}}\n'
                        )

                else:
                    cls._initialize()

                    if cls.queue_closed:
                        if error_mode == ErrorMode.LOG_AND_RAISE:
                            raise ProducerError("Producer is shutting down")
                        else:
                            logger.error("Producer is shutting down")
                            return

                    # wrap the proto in a VortexMessage
                    timestamp = Timestamp()
                    timestamp.GetCurrentTime()
                    message = VortexMessage(
                        any=google.protobuf.any_pb2.Any(
                            type_url="{}/{}".format("", message.DESCRIPTOR.full_name),
                            value=message.SerializeToString(),
                        ),
                        vortex_event_created_at=timestamp,
                    )

                    if wait_seconds > 0:
                        cls.queue.put(message, block=True, timeout=wait_seconds)
                    else:
                        cls.queue.put(message, block=False)

            except Full:
                logger.error("Queue is full, message dropped!")
                return
            except ValueError as e:
                if error_mode == ErrorMode.LOG_AND_RAISE:
                    raise ValidationError(f"Invalid message format: {e}")
                else:
                    logger.error(f"Invalid message format: {e}")
            except Exception as e:
                if error_mode == ErrorMode.LOG_AND_RAISE:
                    raise ProducerError(f"Unknown error: {e}")
                else:
                    logger.error(f"Unknown error: {e}")

    @classmethod
    def shutdown(cls, timeout_seconds: float = 10.0) -> None:
        """
        Shutdown the client.

        This will stop the worker thread and close the queue. It will wait at most
        `timeout_seconds` for the worker thread to shut down.

        Args:
            timeout_seconds: The timeout for the worker thread to shut down.
        """
        with trace("vortex-producer.python.shutdown"):
            if not cls.initialized:
                return

            logger.debug("Starting shutdown.")
            cls.initialized = False
            # cls.queue_closed = True

            try:
                start_seconds = time.time()

                logger.debug(
                    f"Putting shutdown sentinel in queue. Timeout: {timeout_seconds} seconds"
                )
                if timeout_seconds > 0:
                    # None is a sentinel value to indicate the worker should shut down
                    cls.queue.put(None, block=True, timeout=timeout_seconds)
                elif timeout_seconds == 0:
                    cls.queue.put(None, block=False)
                else:
                    logger.warning(
                        "shutdown: timeout_seconds must be greater than 0. Default to non-blocking"
                    )
                    cls.queue.put(None, block=False)

                duration_seconds = time.time() - start_seconds

                if duration_seconds >= timeout_seconds:
                    return

                logger.debug("Waiting for worker thread to shut down.")

                cls.thread.join(timeout=timeout_seconds - duration_seconds)

            except Exception:
                logger.warning(
                    "Failed to shut down properly. Some messages may not have been sent."
                )
                return

    @classmethod
    def _initialize(cls, max_queue_size: int = 10000) -> None:
        """
        Initialize the client.

        This will start a worker thread that will send messages to Vortex in the background.

        In normal use, there is no need to call this method. The client will automatically
        initialize when the first message is logged.

        Args:
            max_queue_size: The maximum number of messages to buffer in the queue.
            log_level: The log level to set for the client. Default is WARNING. Set to some value
                above 50 (CRITICAL) to suppress all logs.
        """
        logger.debug("Initializing Vortex producer client")

        if cls.initialized:
            return

        try:
            cls.initialized = True
            cls.queue_closed = False
            cls.queue = Queue(maxsize=max_queue_size)

            # start worker thread
            cls.thread = threading.Thread(target=cls._worker)
            cls.thread.daemon = True
            cls.thread.start()
        except Exception:
            logger.warning("Failed to initialize Vortex producer client!")

    @classmethod
    def _reset(cls) -> None:
        """
        Forcibly reset the client to its initial state.

        This will stop the worker thread and close the queue.

        In normal use, there is no need to call this method.
        """
        if cls.initialized:
            cls.shutdown()

        if getattr(cls, "thread", None) is not None:
            cls.thread.join()

        cls.initialized = False
        cls.queue_closed = False

        if getattr(cls, "queue", None) is not None:
            del cls.queue

        if getattr(cls, "thread", None) is not None:
            del cls.thread

    @classmethod
    def _send_proto(cls, message: VortexMessageBatch) -> requests.Response:
        """
        Send a protobuf message to Vortex.

        This is a helper method that sends a message to Vortex. It is used by the worker
        thread to send messages to Vortex.
        """
        with trace("vortex-producer.python.send_proto"):
            # populate timestamps just before sending
            logger.debug(f"Sending a batch of {len(message.payload)} messages!")
            base_url: str = os.getenv("VORTEX_BASE_URL", "https://p.vx.dbt.com")
            ingest_endpoint: str = os.getenv("VORTEX_INGEST_ENDPOINT", "/v1/ingest/protobuf")

            # Get service info from environment variables
            service_name = os.getenv("DD_SERVICE", "vortex-client-python")
            service_version = os.getenv("DD_VERSION", _get_import_version("dbtlabs-vortex"))

            # Get client info from project metadata
            client_name = "vortex-client-python"
            client_version = _get_import_version("dbtlabs-vortex")

            # Get proto library info
            proto_library = "proto-python"
            proto_version = _get_import_version("dbt-protos")

            client_platform_header = f"{service_name}/{service_version} {client_name}/{client_version} {proto_library}/{proto_version}"
            return requests.post(
                f"{base_url}{ingest_endpoint}",
                headers={
                    "Content-Type": "application/vnd.google.protobuf",
                    "X-Vortex-Client-Platform": client_platform_header,
                },
                data=message.SerializeToString(),
            )

    @classmethod
    def _worker(cls) -> None:
        """
        Worker method that sends messages to Vortex in the background.
        """
        flush_interval_ms = 5000
        max_batch_size_bytes = 1024 * 400  # max 400kb batches
        while not cls.queue_closed:
            try:
                messages: list[VortexMessage] = []
                bytes_buffered = 0
                start_time = time.time()

                while bytes_buffered < max_batch_size_bytes:
                    try:
                        elapsed = time.time() - start_time

                        # if we've waited longer than flush_interval_ms, break out of the loop
                        # and flush what we have so far
                        if elapsed > (flush_interval_ms / 1000):
                            break

                        # don't block for longer than flush_interval_ms
                        message = cls.queue.get(timeout=(flush_interval_ms / 1000) - elapsed)

                        if message is None:
                            logger.debug("Worker thread received shutdown sentinel.")
                            cls.queue_closed = True
                            break
                        else:
                            bytes_buffered += message.ByteSize()
                            messages.append(message)

                    except Empty:
                        # this is expected. continue here, and then the very first thing we do on
                        # the next iteration is check if we should exit out of the loop and flush.
                        continue

                logger.debug(f"Flushing {len(messages)} messages ({bytes_buffered} bytes)!")

                for i, message in enumerate(messages):
                    timestamp = Timestamp()
                    timestamp.GetCurrentTime()

                    # repack the event, it's readonly for some reason!
                    message = VortexMessage(
                        any=message.any,
                        vortex_event_created_at=message.vortex_event_created_at,
                        vortex_client_sent_at=timestamp,
                    )

                    messages[i] = message

                if len(messages) > 0:
                    message_batch = VortexMessageBatch(
                        request_id=str(uuid.uuid4()),
                        payload=messages,
                    )
                    send_result = cls._send_proto(message_batch)

                    if send_result.status_code != 202:
                        logger.warning(
                            f"Failed to send message: {send_result.status_code} {send_result.text}"
                        )

                    else:
                        logger.debug("Sent one message to Vortex successfully.")

            except Exception as e:
                logger.error(f"Error logging message: {e}")
