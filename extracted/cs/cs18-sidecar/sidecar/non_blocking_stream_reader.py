from queue import Queue, Empty
from threading import Thread
from logging import Logger

import time
from sidecar.utils import TimeoutUtils


class NonBlockingStreamReader:

    def __init__(self, stream, interval=1.0, logger: Logger = None):
        self._stream = stream
        self._queue = Queue()
        self._to_break = False
        self._interval = interval
        self._logger = logger

        self._thread = Thread(target=self.populate_queue, daemon=True)
        self._thread.start()  # start collecting lines from the stream

    def populate_queue(self):
        while not self._to_break:
            line = self._safely_read_line_from_stream()
            if line:
                self._queue.put(line)

            time.sleep(self._interval)

    def _safely_read_line_from_stream(self):
        try:
            return self._stream.readline().rstrip("\n\r")
        except:
            pass

    def _drain_stream(self):
        line = self._safely_read_line_from_stream()
        while line:
            self._queue.put(line)
            line = self._safely_read_line_from_stream()

    def stop(self):
        # stop the 'self._queue' from receiving any more lines from the healthCheck script
        self._to_break = True
        self._thread.join(timeout=self._interval * 2)

    # ============  IMPORTANT  ============ :
    # This function must be called only after the connection was closed,
    # Otherwise there may be a scenario that the connection is alive and write lines in a loop and never finish
    # and so the drain will never stop.
    def drain_stream(self):
        # drain any leftovers lines from the healthCheck script to the 'self._queue'
        self._drain_stream()

    def read_line(self, timeout):
        try:
            return self._queue.get(block=True, timeout=timeout)
        except Empty:
            return None

    def read_lines(self):
        items = []
        try:
            while not self._queue.empty():
                items.append(self._queue.get(block=False))
        except Empty:
            pass
        return items


class UnexpectedEndOfStream(Exception):
    pass
