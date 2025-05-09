import asyncio
import logging
import queue
import threading
import time
import traceback
from typing import TYPE_CHECKING, Callable, List, Optional

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from literalai.api import LiteralAPI
    from literalai.observability.step import StepDict

DEFAULT_SLEEP_TIME = 0.2


# to_thread is a backport of asyncio.to_thread from Python 3.9
async def to_thread(func, /, *args, **kwargs):
    import contextvars
    import functools

    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)


class EventProcessor:
    event_queue: queue.Queue
    batch: List["StepDict"]
    batch_timeout: float = 5.0

    def __init__(
        self,
        api: "LiteralAPI",
        batch_size: int = 1,
        disabled: bool = False,
        preprocess_steps_function: Optional[
            Callable[[List["StepDict"]], List["StepDict"]]
        ] = None,
    ):
        self.stop_event = threading.Event()
        self.batch_size = batch_size
        self.api = api
        self.event_queue = queue.Queue()
        self.disabled = disabled
        self.processing_counter = 0
        self.counter_lock = threading.Lock()
        self.last_batch_time = time.time()
        self.preprocess_steps_function = preprocess_steps_function
        self.processing_thread = threading.Thread(
            target=self._process_events, daemon=True
        )
        if not self.disabled:
            self.processing_thread.start()

    def add_event(self, event: "StepDict"):
        with self.counter_lock:
            self.processing_counter += 1
        self.event_queue.put(event)

    async def a_add_events(self, event: "StepDict"):
        with self.counter_lock:
            self.processing_counter += 1
        await to_thread(self.event_queue.put, event)

    def set_preprocess_steps_function(
        self,
        preprocess_steps_function: Optional[
            Callable[[List["StepDict"]], List["StepDict"]]
        ],
    ):
        """
        Set a function that will preprocess steps before sending them to the API.
        The function should take a list of StepDict objects and return a list of processed StepDict objects.
        This can be used for tasks like PII removal.

        Args:
            preprocess_steps_function (Callable[[List["StepDict"]], List["StepDict"]]): The preprocessing function
        """
        self.preprocess_steps_function = preprocess_steps_function

    def _process_events(self):
        while True:
            batch = []
            start_time = time.time()
            try:
                elapsed_time = time.time() - start_time
                # Try to fill the batch up to the batch_size
                while (
                    len(batch) < self.batch_size and elapsed_time < self.batch_timeout
                ):
                    # Attempt to get events with a timeout
                    event = self.event_queue.get(timeout=0.5)
                    batch.append(event)
            except queue.Empty:
                # No more events at the moment, proceed with processing what's in the batch
                pass

            # Process the batch if any events are present
            if batch:
                self._process_batch(batch)

            # Stop if the stop_event is set and the queue is empty
            if self.stop_event.is_set() and self.event_queue.empty():
                break

    def _try_process_batch(self, batch: List):
        try:
            # Apply preprocessing function if it exists
            if self.preprocess_steps_function is not None:
                try:
                    processed_batch = self.preprocess_steps_function(batch)
                    # Only use the processed batch if it's valid
                    if processed_batch is not None and isinstance(
                        processed_batch, list
                    ):
                        batch = processed_batch
                    else:
                        logger.warning(
                            "Preprocess function returned invalid result, using original batch"
                        )
                except Exception as e:
                    logger.error(f"Error in preprocess function: {str(e)}")
                    logger.error(traceback.format_exc())
                    # Continue with the original batch

            return self.api.send_steps(batch)
        except Exception:
            logger.error(f"Failed to send steps: {traceback.format_exc()}")
        return None

    def _process_batch(self, batch: List):
        # Simple one-try retry in case of network failure (no retry on graphql errors)
        retries = 0
        while not self._try_process_batch(batch) and retries < 1:
            retries += 1
            time.sleep(DEFAULT_SLEEP_TIME)
        with self.counter_lock:
            self.processing_counter -= len(batch)

    def flush_and_stop(self):
        self.stop_event.set()
        if not self.disabled:
            self.processing_thread.join()

    async def aflush(self):
        while not self.event_queue.empty() or self._is_processing():
            await asyncio.sleep(DEFAULT_SLEEP_TIME)

    def flush(self):
        while not self.event_queue.empty() or self._is_processing():
            time.sleep(DEFAULT_SLEEP_TIME)

    def _is_processing(self):
        with self.counter_lock:
            return self.processing_counter > 0

    def __del__(self):
        self.flush_and_stop()
