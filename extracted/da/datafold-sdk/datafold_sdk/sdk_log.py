import queue
import threading
import time
import logging
import socket
import atexit
import os
from typing import Dict, Tuple, List, Any
import requests
import pydantic

from datafold_sdk.cli.context import DATAFOLD_HOST, DATAFOLD_API_KEY, DATAFOLD_APIKEY

DF_HOST = 'https://app.datafold.com'
DF_API_KEY = os.environ.get(DATAFOLD_API_KEY) or os.environ.get(DATAFOLD_APIKEY)

override_host = os.environ.get(DATAFOLD_HOST)
if override_host:
    DF_HOST = override_host

SDK_LOGS_ENDPOINT = f"{DF_HOST.rstrip('/')}/api/internal/sdk/log"

class SDKLog(pydantic.BaseModel):
    message: str
    created: float
    line_no: int
    level_no: int
    level_name: str
    func_name: str
    filename: str


class SDKLogHandler(logging.Handler):
    _queue: queue.Queue = queue.Queue()
    shutdown_indicator : queue.Queue = queue.Queue()
    worker_thread = None
    lock = threading.Lock()

    def __init__(self):
        super().__init__()
        with SDKLogHandler.lock:
            if SDKLogHandler.worker_thread is None:
                SDKLogHandler.worker_thread = threading.Thread(target=self.process_logs)
                self.worker_thread.daemon = True
                self.worker_thread.start()
                atexit.register(self.shutdown)

    def emit(self, record) -> None:
        message = self.format(record)
        filename = record.filename
        line_no = record.lineno
        level_no = record.levelno
        level_name = record.levelname
        func_name = record.funcName
        created = record.created

        log_data = SDKLog(message=message,
            created=created,
            line_no=line_no,
            level_no=level_no,
            level_name=level_name,
            func_name=func_name,
            filename=filename
        )
        self._queue.put(log_data)

    def shutdown(self) -> None:
        self._queue.put(None)
        self.shutdown_indicator.get()

    def _get_batch(self) -> Tuple[List[Dict[Any, Any]], bool]:
        batch : List[Dict[Any, Any]] = []
        wait_till = None
        while 1:
            if len(batch) == 100:
                return batch, False

            if wait_till is None:
                timeout = None
            else:
                timeout = max(0, wait_till - time.monotonic())

            try:
                log = self._queue.get(timeout=timeout)
                if log is None:
                    return batch, True

                batch.append(log.model_dump())
                if wait_till is None:
                    wait_till = time.monotonic() + 1.0

            except queue.Empty:
                return batch, False
            except Exception: # pylint: disable=broad-exception-caught
                pass

    def process_logs(self) -> None:
        stop = False
        while not stop:
            batch, stop = self._get_batch()
            if batch:
                self.push_logs(batch)
        self.shutdown_indicator.put(None)

    @staticmethod
    def push_logs(batch) -> None:
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Key {DF_API_KEY}'
            }
            log_data = {'hostname': socket.gethostname(), 'service' : 'datafold-sdk', 'logs': batch}
            requests.post(SDK_LOGS_ENDPOINT, json=log_data, headers=headers, timeout=5)
        except Exception: # pylint: disable=broad-exception-caught
            pass
