"""HTTP(s) delivery handler (for logstash, vector etc),
the built-in HTTPHandler posts stuff as form data, we do not like that, also it has no connection pooling etc"""

from typing import Sequence, Optional, Mapping, Any, Union, Generator, Dict, cast, List
import logging
from logging.handlers import MemoryHandler
import json
from concurrent.futures import ThreadPoolExecutor, Future, CancelledError  # pylint: disable=W0611
import copy
import os
import time

import requests
from frozendict import frozendict

from .common import UTCISOFormatter, DEFAULT_LOG_FORMAT, DEFAULT_LOGGING_CONFIG, DEFAULT_RECORD_DIR
from ..hashinghelpers import immobilize, ForgivingEncoder, HandledSubTypes

APPLOGFORMAT_HEADER = "libadvian"
# DictConfig with the default HTTP stuff
HTTP_LOGGING_CONFIG = cast(Dict[str, Any], copy.deepcopy(DEFAULT_LOGGING_CONFIG))
HTTP_LOGGING_CONFIG["handlers"].update(
    {
        "http": {
            "class": "libadvian.logging.httpmulti.BufferedHTTPMultiRecordHandler",
            "formatter": "utc",
        },
    }
)
HTTP_LOGGING_CONFIG["root"]["handlers"].append("http")

# Shorthand
MultiRecordType = Union[Generator[logging.LogRecord, None, None], Sequence[logging.LogRecord]]


class MultiRecordHandlerBase(logging.Handler):
    """mixin to add emit_multiple and handle_multiple methods"""

    def __init__(self) -> None:
        super().__init__()

    def wait_inflight(self, timeout: float = 5.0) -> None:
        """Wait out any background tasks (NOOP in this baseclass)"""
        _, _ = (timeout, self)

    def emit(self, record: logging.LogRecord) -> None:
        """backwards compatibility, wraps the single record into a sequence"""
        self.emit_multiple((record,))

    def emit_multiple(self, records: MultiRecordType) -> None:
        """
        Do whatever it takes to actually log the specified logging records.

        This version is intended to be implemented by subclasses and so
        raises a NotImplementedError.
        """
        raise NotImplementedError("emit_multiple must be implemented by Handler subclasses")

    def handle_multiple(self, records: MultiRecordType) -> bool:
        """
        Conditionally emit the specified logging record.

        Emission depends on filters which may have been added to the handler.
        Wrap the actual emission of the record with acquisition/release of
        the I/O thread lock. Returns whether the filter passed the record for
        emission.
        """
        filtered = [record for record in records if self.filter(record)]  # generators are always true, use list
        if filtered:
            self.acquire()
            try:
                self.emit_multiple(filtered)
            finally:
                self.release()
        return bool(filtered)


class BufferedHandleMultiple(MemoryHandler):
    """Memoryhandler but targets emit gets a list of events if there are multiple"""

    def __init__(  # pylint: disable=R0917,R0913
        self,
        capacity: int,
        flushLevel: int = logging.ERROR,
        target: Optional[MultiRecordHandlerBase] = None,
        flushOnClose: bool = True,
        flush_interval: float = 10.0,
    ):
        super().__init__(capacity=capacity, flushLevel=flushLevel, flushOnClose=flushOnClose)
        self._flushexcecutor = ThreadPoolExecutor(thread_name_prefix="BufferedHandleMultiple")
        self.target = target
        self._interval = flush_interval
        self._interval_should_stop = False
        self._interval_task = self._flushexcecutor.submit(self._flush_thread_handler)

    def _flush_thread_handler(self) -> None:
        """Call flush periodically"""
        last_flush = time.time()
        try:
            while not self._interval_should_stop and self.target:
                time.sleep(0.5)
                if (time.time() - last_flush) < self._interval:
                    continue
                self.flush()
                last_flush = time.time()
        except CancelledError:
            pass

    def flush(self) -> None:
        """
        For a MemoryHandler, flushing means just sending the buffered
        records to the target
        The record buffer is also cleared by this operation.
        """
        self.target = cast(Optional[MultiRecordHandlerBase], self.target)
        self.acquire()
        try:
            if self.target:
                self.target.handle_multiple(self.buffer)
                self.buffer = []
        finally:
            self.release()

    def close(self) -> None:
        """
        Close flush and the target first
        """
        self._interval_should_stop = True
        if self.flushOnClose:
            self.flush()
        if self.target:
            self.target.close()
        super().close()
        if not self._interval_task.done():
            self._interval_task.cancel()
        self._flushexcecutor.shutdown(wait=True)


class HTTPMultiRecordHandler(MultiRecordHandlerBase):
    """Ship multiple records in one post to logstash/vector"""

    def __init__(
        self,
        target_uri: Optional[str] = None,
        session_options: Optional[Mapping[str, Any]] = None,
        timeout: float = 2.0,
    ):
        """
        Initialize our requests session with given options and labels
        """
        super().__init__()
        self._httpexcecutor = ThreadPoolExecutor(thread_name_prefix="HTTPMultiRecordHandler")
        if not target_uri:
            target_uri = os.environ.get("LOG_HTTP_TARGET_URI")
            if not target_uri:
                raise ValueError("target_uri not given and LOG_HTTP_TARGET_URI not in ENV")
        self.in_flight: List["Future[Any]"] = []
        self._uri = target_uri
        self._session = requests.Session()
        self.timeout = timeout
        # If we have session options set them
        if session_options:
            for key in session_options.keys():
                setattr(self._session, key, session_options[key])
        self._session.headers.update({"applogformat": APPLOGFORMAT_HEADER, "Content-type": "text/plain"})
        if not self._session.auth:
            username = os.environ.get("LOG_HTTP_USERNAME")
            password = os.environ.get("LOG_HTTP_PASSWORD")
            if username and password:
                self._session.auth = (username, password)
        # use our default formatter by default
        if not self.formatter:
            self.setFormatter(UTCISOFormatter(DEFAULT_LOG_FORMAT))

    def close(self) -> None:
        """
        Flush, if appropriately configured, set the target to None and lose the
        buffer.
        """
        try:
            # schedule all messages
            self.flush()
            # Let tasks finish
            self._httpexcecutor.shutdown(wait=True)
        finally:
            super().close()

    def emit_multiple(self, records: MultiRecordType) -> None:
        """Push the records into logstash/vector as multiline POST"""
        if not self._session:
            raise ValueError("No requests session!")

        def do_post(records: MultiRecordType) -> None:  # pylint: disable=R0914
            """The actual post"""
            # Muck with loglevels to silence debug from the posts we do
            requests_logger = logging.getLogger("requests")
            requests_logger_level = requests_logger.getEffectiveLevel()
            requests_logger.setLevel(logging.CRITICAL)
            urllib3_logger = logging.getLogger("urllib3")
            urllib3_logger_level = urllib3_logger.getEffectiveLevel()
            urllib3_logger.setLevel(logging.CRITICAL)

            # Sort into batches by labels
            records_by_labels: Dict[int, List[logging.LogRecord]] = {0: []}
            for record in records:
                record_dir = set(dir(record))
                extra_keys = record_dir - DEFAULT_RECORD_DIR
                extra = frozendict({key: immobilize(getattr(record, key), True) for key in extra_keys})
                record.extra = cast(Mapping[str, HandledSubTypes], extra)
                if not extra:
                    records_by_labels[0].append(record)
                    continue
                labels_key = hash(extra)
                if labels_key not in records_by_labels:
                    records_by_labels[labels_key] = []
                records_by_labels[labels_key].append(record)
            # process the batches setting the labels to headers
            for bkey in sorted(records_by_labels.keys()):
                rbatch = records_by_labels[bkey]
                if not rbatch:
                    continue
                extra_headers = {}
                formatted = (self.format(record).replace("\n", "\\n") for record in rbatch)
                extra = getattr(rbatch[0], "extra", frozendict())
                data = "\n".join(formatted).encode("utf8")
                if extra:
                    extra_headers.update({"labels_json": json.dumps(extra, cls=ForgivingEncoder)})
                try:
                    resp = self._session.post(self._uri, headers=extra_headers, data=data, timeout=self.timeout)
                    if resp.status_code != 200:
                        # TODO: can we do anything ??
                        pass
                except (requests.HTTPError, requests.ConnectionError):
                    # TODO: can we do anything ??
                    pass

            requests_logger.setLevel(requests_logger_level)
            urllib3_logger.setLevel(urllib3_logger_level)

        try:
            fut = self._httpexcecutor.submit(do_post, records)
            fut.add_done_callback(self._done_callback)
            self.in_flight.append(fut)
        except RuntimeError:
            # Excutor is shutting down, ignore.
            pass

    def wait_inflight(self, timeout: float = 5.0) -> None:
        """Wait for all in-flight requests to finish"""
        started = time.time()
        while self.in_flight:
            for fut in self.in_flight:
                if fut.done():
                    self.in_flight.remove(fut)
            time.sleep(0.1)
            if time.time() - started > timeout:
                raise TimeoutError("Timed out while waiting for the tasks")

    def _done_callback(self, fut: "Future[Any]") -> None:
        """remove the task from -in-flight"""
        fut.result()  # raise error if one happened in the executor
        if fut not in self.in_flight:
            return
        self.in_flight.remove(fut)


class BufferedHTTPMultiRecordHandler(BufferedHandleMultiple):
    """Convenience wrapper for buffering HTTPMultiRecordHandler

    See: HTTPMultiRecordHandler and BufferedHandleMultiple"""

    def __init__(  # pylint: disable=R0917,R0913
        self,
        target_uri: Optional[str] = None,
        session_options: Optional[Mapping[str, Any]] = None,
        timeout: float = 2.0,
        capacity: int = 15,
        flushLevel: int = logging.ERROR,
        target: Optional[MultiRecordHandlerBase] = None,
        flushOnClose: bool = True,
        flush_interval: float = 10.0,
    ):
        """init with defaults"""
        if target is None:
            target = HTTPMultiRecordHandler(target_uri=target_uri, session_options=session_options, timeout=timeout)
        super().__init__(
            capacity=capacity,
            flushLevel=flushLevel,
            target=target,
            flushOnClose=flushOnClose,
            flush_interval=flush_interval,
        )

    def wait_inflight(self, timeout: float = 5.0) -> None:
        """wait out the in-progress tasks"""
        if not isinstance(self.target, MultiRecordHandlerBase):
            raise ValueError("Target is not subclass of MultiRecordHandlerBase")
        self.flush()
        self.target.wait_inflight(timeout)
