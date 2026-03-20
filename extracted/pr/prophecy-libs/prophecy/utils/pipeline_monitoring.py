import base64 as base64_std
import gzip
import json
import logging
import re
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
from typing import Optional, List

from prophecy.executionmetrics.schemas.em import (
    SerializableException,
    TimestampedOutput,
)
from prophecy.executionmetrics.utils.common import get_spark_property
from prophecy.jsonrpc.models import NotificationMessage, SparkEventNotification
from prophecy.config.config_base import is_serverless


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(handler)


# --- constants --------------------------------------------------------------

SPARK_CONF_PIPELINE_CODE_KEY = "spark.prophecy.metadata.pipeline.code"
RecursiveDirectoryContent = Dict[str, str]  # ⇐ Scala type alias


_PING_INTERVAL_SECS = 15


class _LockedWsSender:
    """Thread-safe wrapper that serialises all send() calls through a lock."""
    def __init__(self, ws, lock):
        self._ws = ws
        self._lock = lock

    def send(self, data):
        if self._lock:
            with self._lock:
                self._ws.send(data)
        else:
            self._ws.send(data)


class InteractiveEventSender:
    def __init__(self):
        self._ws_url: Optional[str] = None
        self._session: Optional[str] = None
        self._ws_connection = None
        self._ws_lock = None
        self._receiver_thread = None
        self._ws_running = False

    def is_connected(self) -> bool:
        return self._ws_connection is not None

    def initialize(self, execution_url: str, session: str):
        import threading

        if (
            self._ws_connection is not None
            and self._session == session
            and self._ws_url == execution_url
        ):
            try:
                self._ws_connection.ping("")
                return
            except Exception:
                logger.debug("Existing connection dead, will reconnect")

        if self._ws_connection is not None or self._receiver_thread is not None:
            self.shutdown()

        self._ws_url = execution_url
        self._session = session
        self._ws_lock = threading.Lock()

        try:
            import websocket
            ws_url = f"{execution_url}/{session}"
            self._ws_connection = websocket.create_connection(ws_url, timeout=30)
            self._ws_running = True
            self._receiver_thread = threading.Thread(
                target=self._receiver_loop,
                daemon=True,
                name="interactive-ws-receiver"
            )
            self._receiver_thread.start()
        except ImportError:
            self._ws_connection = None
        except Exception as e:
            self._ws_connection = None

    def shutdown(self):
        self._ws_running = False

        if self._receiver_thread is not None:
            self._receiver_thread.join(timeout=2.0)
            self._receiver_thread = None

        if self._ws_connection is not None:
            try:
                self._ws_connection.close()
            except Exception:
                pass
            self._ws_connection = None

    def send(self, json_msg: str):
        final_notification = NotificationMessage(SparkEventNotification(json_msg))
        final_message = final_notification.to_json()

        if is_serverless:
            try:
                from websocket_runner import send_message_via_ws
                send_message_via_ws(final_message)
            except Exception as e:
                logger.error(f"Exception while sending event: {e}")
            return

        if self._ws_connection is not None:
            try:
                self._locked_send(final_message)
            except Exception as e:
                self._reconnect()
                try:
                    if self._ws_connection is not None:
                        self._locked_send(final_message)
                except Exception as retry_e:
                    logger.debug(f"Failed to send event after reconnect: {retry_e}")
            return

    def _locked_send(self, message: str):
        if self._ws_lock:
            with self._ws_lock:
                self._ws_connection.send(message)
        else:
            self._ws_connection.send(message)

    def _reconnect(self):
        if self._ws_url and self._session:
            try:
                import websocket
                ws_url = f"{self._ws_url}/{self._session}"
                new_conn = websocket.create_connection(ws_url, timeout=30)
                if self._ws_lock:
                    with self._ws_lock:
                        self._ws_connection = new_conn
                else:
                    self._ws_connection = new_conn
            except Exception as e:
                self._ws_connection = None

    def _receiver_loop(self):
        idle_seconds = 0

        while self._ws_running and self._ws_connection is not None:
            try:
                self._ws_connection.settimeout(1.0)
                message = self._ws_connection.recv()
                if message:
                    self._handle_incoming_message(self._ws_connection, message)
                idle_seconds = 0
            except Exception as e:
                error_str = str(e).lower()
                if 'timed out' in error_str or 'timeout' in error_str:
                    idle_seconds += 1
                    if idle_seconds >= _PING_INTERVAL_SECS:
                        if not self._send_keepalive_ping():
                            break
                        idle_seconds = 0
                    continue
                if 'connection' in error_str and ('closed' in error_str or 'reset' in error_str):
                    break

    def _send_keepalive_ping(self) -> bool:
        try:
            if self._ws_lock:
                with self._ws_lock:
                    self._ws_connection.ping("")
            else:
                self._ws_connection.ping("")
            return True
        except Exception:
            return False

    def _handle_incoming_message(self, ws, message: str):
        try:
            data = json.loads(message)

            if 'method' in data and 'id' in data:
                try:
                    from prophecy.utils.request_processor import _process_request
                    locked_sender = _LockedWsSender(ws, self._ws_lock)
                    _process_request(message, locked_sender)
                except ImportError as ie:
                    logger.warning(f"Request_processor not available: {ie}")
                except Exception as e:
                    logger.error(f"Error processing request: {e}")
            else:
                logger.debug(f"Received non-request message: {message[:200]}")
        except json.JSONDecodeError:
            logger.debug(f"Received non-JSON message: {message[:200]}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")


_sender = InteractiveEventSender()


def has_interactive_event_sender() -> bool:
    return _sender.is_connected()


def init_interactive_event_sender(execution_url: str, session: str):
    _sender.initialize(execution_url, session)


def shutdown_interactive_event_sender():
    _sender.shutdown()

# --- tiny utility helpers ---------------------------------------------------


def get_session_appended_key(key: str, session: str) -> str:
    """Prophecy convention:  foo.bar.<session-id>"""
    return f"{key}.{session}"


def decompress(encoded: str) -> str:
    """
    Placeholder implementation: assumes each part is
    base64-encoded + gzipped bytes of UTF-8 JSON text.
    """
    raw: bytes = base64_std.b64decode(encoded)
    return gzip.decompress(raw).decode("utf-8")


def parse_json_fallback(raw: str) -> Dict[str, str]:
    """
    Second-chance JSON parser.  You can plug in ujson, rapidjson,
    or any schema-aware parser here.
    """
    return json.loads(raw)


# --- main translation -------------------------------------------------------


def get_session_hack(spark) -> str:
    prefix = "spark.prophecy.metadata.pipeline.uuid"
    
    if hasattr(spark, '_jsparkSession'):
        try:
            all_sql_conf = spark._jsparkSession.conf().getAll()
            iterator = all_sql_conf.iterator()
            while iterator.hasNext():
                entry = iterator.next()
                key = entry._1()
                if isinstance(key, str) and key.startswith(prefix):
                    return key.replace(f"{prefix}.", "")
        except Exception:
            pass

    if hasattr(spark, 'sparkContext') and spark.sparkContext is not None:
        spark_conf = spark.sparkContext.getConf()
        if spark_conf is not None:
            all_conf = spark_conf.getAll()
            if all_conf is not None:
                for key, value in all_conf:
                    if isinstance(key, str) and key.startswith(prefix):
                        return key.replace(f"{prefix}.", "")
    
    
    if hasattr(spark.conf, '_conf_override') and spark.conf._conf_override is not None:
        for key in spark.conf._conf_override:
            if isinstance(key, str) and key.startswith(prefix):
                return key.replace(f"{prefix}.", "")
    
    if hasattr(spark, 'sparkContext') and hasattr(spark.sparkContext, 'getLocalProperty'):
        local_props_str = str(spark.sparkContext._jsc.sc().localProperties()) if hasattr(spark.sparkContext, '_jsc') else ""
        if prefix in local_props_str:
            match = re.search(rf'{prefix}\.([a-zA-Z0-9_-]+)', local_props_str)
            if match:
                return match.group(1)
    
    return ""


def get_running_code(spark, session: str) -> RecursiveDirectoryContent:
    """
    Re-assembles (and un-compresses) the pipeline code that Prophecy stores in
    Spark conf, handling both the single-value and the multi-part layout.
    """
    # 1️⃣  Multi-part branch ---------------------------------------------------

    logger.debug(f"Got session: {session}")

    logger.debug(f"Got spark_type: {type(spark)}")
    logger.debug(f"Got spark.conf type: {type(spark.conf)}")

    if not session:
        session = get_session_hack(spark)

    logger.debug(f"Our personal session id: {session}")

    parts_key = (
        f"{get_session_appended_key(SPARK_CONF_PIPELINE_CODE_KEY, session)}_parts"
    )
    logger.debug(f"Got parts_key: {parts_key}")

    parts = get_spark_property(parts_key, spark)
    logger.debug(f"Got parts: {parts}")

    if parts is not None:  # ⇐ Some(parts) in Scala
        logger.debug("Got code split in %s parts", parts)

        # Gather every chunk into an in-memory list
        compressed_chunks: list[str] = []
        for part_id in range(int(parts)):
            part_key = f"{get_session_appended_key(SPARK_CONF_PIPELINE_CODE_KEY, session)}_{part_id}"
            chunk = get_spark_property(part_key, spark)
            if chunk is not None:  # ⇐ .map(...)
                compressed_chunks.append(chunk)

        decompressed_code = decompress("".join(compressed_chunks))

        # Parse JSON with two layers of defence (matches Try/Fallback logic)
        try:
            rdc: RecursiveDirectoryContent = json.loads(decompressed_code)
        except Exception as exc1:
            logger.error(
                "Failed to parse JSON with stdlib json; trying fallback", exc_info=exc1
            )
            try:
                rdc = parse_json_fallback(decompressed_code)
            except Exception as exc2:
                logger.error("Fallback JSON parser failed as well", exc_info=exc2)
                rdc = {}

        logger.debug("Final code size = %d bytes", len(str(rdc).encode()))
        return rdc

    # 2️⃣  Single-value branch -------------------------------------------------
    single_key = get_session_appended_key(SPARK_CONF_PIPELINE_CODE_KEY, session)
    compressed_value = get_spark_property(single_key, spark)

    if compressed_value:
        return json.loads(decompress(compressed_value))

    # No code stored for this session
    return {}


def get_process_from_gem2(spark, gemName: str, userSession: str) -> str:
    rdc = get_running_code(spark, userSession)
    
    if not rdc:
        logger.warning("RDC is empty. Using gemName as process ID.")
        return gemName
    
    logger.debug(f"RDC Keys - {list(rdc.keys())}")

    workflow_key = ".prophecy/workflow.latest.json"
    workflow_content = rdc.get(workflow_key)
    
    if workflow_content is None:
        logger.warning(f"Workflow metadata not found in rdc (keys: {list(rdc.keys())}). Using gemName as process ID.")
        return gemName
    
    # Parse workflow JSON
    if not isinstance(workflow_content, str):
        logger.warning(f"Workflow content is not a string (type: {type(workflow_content)}). Using gemName as process ID.")
        return gemName
    
    wflow_file_json = json.loads(workflow_content)
    
    if not isinstance(wflow_file_json, dict):
        logger.warning(f"Parsed workflow is not a dict (type: {type(wflow_file_json)}). Using gemName as process ID.")
        return gemName
    
    def search_processes(processes, slug):
        """Recursively search for process ID by slug."""
        if not isinstance(processes, dict):
            return None
        
        for proc_id, proc_val in processes.items():
            if not isinstance(proc_val, dict):
                continue
            
            metadata = proc_val.get("metadata")
            if isinstance(metadata, dict) and metadata.get("slug") == slug:
                return proc_id
            
            # Recursively search nested processes
            nested = proc_val.get("processes")
            if isinstance(nested, dict):
                found = search_processes(nested, slug)
                if found:
                    return found
        
        return None
    
    processes = wflow_file_json.get("processes", {})
    result = search_processes(processes, gemName)
    
    if result:
        return result
    
    return gemName


@dataclass
class ProphecyGemProgressEvent:
    session: str
    processId: Optional[str]
    taskState: str
    startTime: int
    endTime: Optional[int] = None
    stdout: Optional[List["TimestampedOutput"]] = None
    stderr: Optional[List["TimestampedOutput"]] = None
    exception: Optional["SerializableException"] = None
    # gemProgressEventJsonField: str = field(init=False, default="ProphecyGemProgressEvent")

    def to_dict(self):
        # Convert nested objects to dicts if needed
        def serialize_list(lst):
            if lst is None:
                return None
            return [
                item.to_dict() if hasattr(item, "to_dict") else item for item in lst
            ]

        return {
            "session": self.session,
            "processId": self.processId,
            "taskState": self.taskState,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "stdout": serialize_list(self.stdout),
            "stderr": serialize_list(self.stderr),
            "exception": (
                self.exception.to_dict()
                if self.exception and hasattr(self.exception, "to_dict")
                else None
            ),
        }

    def to_json(self):
        return json.dumps(
            {
                "Event": "ProphecyGemProgressEvent",
                "ProphecyGemProgressEvent": self.to_dict(),
            }
        )


# gemProgressEventJsonField: str = field(init=False, default="ProphecyGemProgressEvent")


@dataclass
class ProphecyPipelineProgressEvent:
    session: str
    pipelineId: str
    state: str
    submissionTime: Optional[int]
    startTime: int
    endTime: Optional[int] = None
    exception: Optional[SerializableException] = None
    # pipelineProgressEventJsonField: str = field(init=False, default="ProphecyPipelineProgressEvent")

    # ── public API ─────────────────────────────────────────────────────────────
    def to_dict(self) -> dict:
        return {
            "session": self.session,
            "pipelineId": self.pipelineId,
            "state": self.state,
            "submissionTime": self.submissionTime,
            "startTime": self.startTime,
            "endTime": self.endTime,
            "exception": (
                self.exception.to_dict()
                if self.exception and hasattr(self.exception, "to_dict")
                else None
            ),
        }

    def to_json(self) -> str:
        wrapper = {
            "Event": "ProphecyPipelineProgressEvent",
            "ProphecyPipelineProgressEvent": self.to_dict(),
        }
        return json.dumps(wrapper)


def sendGemProgressEvent3(
    spark,
    userSession,
    process_id,
    state,
    startTime,
    endTime,
    stdout,
    stderr,
    exception_type,
    msg,
    cause_msg,
    stack_trace,
):

    import time as time_module

    current_time = int(time_module.time() * 1000)
    serializableException = SerializableException(
        exception_type, msg, cause_msg, stack_trace, current_time
    )
    sendGemProgressEvent2(
        spark,
        userSession,
        process_id,
        state,
        startTime,
        endTime,
        stdout,
        stderr,
        serializableException,
    )


def sendGemProgressEvent2(
    spark, userSession, process_id, state, startTime, endTime, stdout, stderr, exception
):
    endTime = int(endTime) if endTime else None
    startTime = int(startTime) if startTime else None

    def parse_output(output):
        import json

        if output is None:
            return None
        try:
            # Try to parse as JSON list of dicts
            parsed = json.loads(output)
            if isinstance(parsed, list):
                return [TimestampedOutput.from_dict(item).to_dict() for item in parsed]
            elif isinstance(parsed, dict):
                # Single dict
                return [TimestampedOutput.from_dict(parsed).to_dict()]
            else:
                # Fallback: treat as string
                return [TimestampedOutput.from_content(str(output)).to_dict()]
        except Exception:
            # Not JSON, treat as plain string
            return [TimestampedOutput.from_content(str(output)).to_dict()]

    _stdout = parse_output(stdout)
    _stderr = parse_output(stderr)

    serializable_exception = None
    if exception is not None:
        if isinstance(exception, SerializableException):
            serializable_exception = exception
        else:
            serializable_exception = SerializableException.from_exception(exception)

    gem_event = ProphecyGemProgressEvent(
        session=get_session_hack(spark),
        processId=process_id,
        taskState=state,
        startTime=startTime,
        endTime=endTime,
        stdout=_stdout,
        stderr=_stderr,
        exception=serializable_exception,
    )

    send_ws_message(gem_event.to_json())


# ---------------------- PipelineProgressEvent ------------------------------------
#
#
# ---------------------------------------------------------------------------------


def sendPipelineProgressEvent3(
    spark,
    userSession: str,
    pipelineId: str,
    state: str,
    startTime: str,
    endTime: str,
    exception_type,
    msg,
    cause_msg,
    stack_trace,
):
    import time as time_module

    current_time = int(time_module.time() * 1000)
    serializableException = SerializableException(
        exception_type, msg, cause_msg, stack_trace, current_time
    )
    sendPipelineProgressEvent2(
        spark, userSession, pipelineId, state, startTime, endTime, serializableException
    )


def sendPipelineProgressEvent2(
    spark,
    userSession: str,
    pipelineId: str,
    state: str,
    startTime: str,
    endTime: str = "",
    exception: Optional[Any] = None,
):

    submission_time = spark.conf.get(
        f"spark.prophecy.pipeline.submission-time.{userSession}"
    )

    submission_time_int = int(submission_time) if submission_time else None

    endTime = int(endTime) if endTime else None
    startTime = int(startTime) if startTime else None

    pipeline_progress_event = ProphecyPipelineProgressEvent(
        session=userSession,
        pipelineId=pipelineId,
        state=state,
        submissionTime=submission_time_int,
        startTime=startTime,
        endTime=endTime,
        exception=exception,
    )

    send_ws_message(pipeline_progress_event.to_json())


def send_ws_message(json_msg: str):
    _sender.send(json_msg)
