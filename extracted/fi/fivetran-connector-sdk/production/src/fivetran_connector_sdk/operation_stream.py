import queue
import threading
import time

from fivetran_connector_sdk_common.constants import (
    QUEUE_SIZE,
    MAX_RECORDS_IN_BATCH,
    MAX_BATCH_SIZE_IN_BYTES,
    CHECKPOINT_OP_TIMEOUT_IN_SEC,
    JAVA_LONG_MAX_VALUE,
)
from fivetran_connector_sdk.constants import CAPTURE_PERFORMANCE_METRICS_ENABLED, NANOS_PER_MILLI
from fivetran_connector_sdk.protos import connector_sdk_pb2
from fivetran_connector_sdk.protos import common_pb2


class _OperationStream:
    """
    A simple iterator-based stream backed by a queue for producing and consuming operations.

    This class allows adding data items into a queue and consuming them using standard iteration.
    It uses a sentinel object to signal the end of the stream.

    Example:
        stream = _OperationStream()
        stream.add("response1")
        stream.mark_done()

        for response in stream:
            print(response)  # prints "response1"
    """

    def __init__(self):
        """
        Initializes the operation stream with a queue and a sentinel object.
        """
        self._queue = queue.Queue(maxsize=QUEUE_SIZE)
        self._sentinel = object()
        self._is_done = False
        self._buffer = []
        self._buffer_record_count = 0
        self._buffer_size_bytes = 0
        self._checkpoint_lock = threading.Lock()
        self._producer_lock = threading.Lock()
        self._checkpoint_flush_signal = threading.Event()
        self._checkpoint_flush_signal.set()
        # Perf timing accumulators: initialized to 0 so downstream reads never hit AttributeError
        # regardless of CAPTURE_PERFORMANCE_METRICS_ENABLED.
        self._sdk_build_ns = 0
        self._queue_wait_ns = 0
        self._queue_backpressure_ns = 0
        self._checkpoint_wait_ns = 0
        self._sdk_batch_assembly_ns = 0
        self._grpc_first_send_ms = 0
        self._grpc_send_relative_total_ms = 0
        self._grpc_send_count = 0
        self._grpc_timestamp_overflow = False
        self._producer_wall_ns = 0

    def _enqueue(self, item):
        """Puts an item onto the internal queue, timing how long the put blocks when
        CAPTURE_PERFORMANCE_METRICS_ENABLED is true. Blocking here means the queue was full, i.e. the
        Connector SDK/Java side is the bottleneck, not the customer's code.
        """
        if not CAPTURE_PERFORMANCE_METRICS_ENABLED:
            self._queue.put(item)
            return
        t0 = time.perf_counter_ns()
        self._queue.put(item)
        self._queue_backpressure_ns += time.perf_counter_ns() - t0

    def _dequeue(self):
        """Gets the next item off the internal queue, timing how long the get blocks when
        CAPTURE_PERFORMANCE_METRICS_ENABLED is true. Blocking here means the consumer is waiting on
        the producer (or on a sentinel/checkpoint/etc.) rather than doing Connector SDK work.
        """
        if not CAPTURE_PERFORMANCE_METRICS_ENABLED:
            return self._queue.get()
        t0 = time.perf_counter_ns()
        operation = self._queue.get()
        self._queue_wait_ns += time.perf_counter_ns() - t0
        return operation

    def _append_to_buffer(self, operation):
        """Appends a record to the batch buffer, timing the assembly work when
        CAPTURE_PERFORMANCE_METRICS_ENABLED is true.
        """
        if not CAPTURE_PERFORMANCE_METRICS_ENABLED:
            self._buffer_record_count += 1
            self._buffer_size_bytes += operation.ByteSize()
            self._buffer.append(operation)
            return
        t0 = time.perf_counter_ns()
        self._buffer_record_count += 1
        self._buffer_size_bytes += operation.ByteSize()
        self._buffer.append(operation)
        self._sdk_batch_assembly_ns += time.perf_counter_ns() - t0

    def record_grpc_send_timestamp(self):
        """Records a relative millisecond send timestamp without summing epoch timestamps."""
        if not CAPTURE_PERFORMANCE_METRICS_ENABLED or self._grpc_timestamp_overflow:
            return
        timestamp_ms = time.time_ns() // NANOS_PER_MILLI
        if self._grpc_send_count == 0:
            self._grpc_first_send_ms = timestamp_ms
        try:
            self._grpc_send_relative_total_ms += (timestamp_ms - self._grpc_first_send_ms)
            self._grpc_send_count += 1
            if self._grpc_send_relative_total_ms > JAVA_LONG_MAX_VALUE:
                self._grpc_timestamp_overflow = True
        except OverflowError:
            # Metrics must not interrupt a sync; Java omits only grpc_transport_ms in this case.
            self._grpc_timestamp_overflow = True

    def __iter__(self):
        """
        Returns the iterator instance itself.
        """
        return self

    def add_checkpoint(self, checkpoint):
        """
        Adds a checkpoint to the stream. Guarantees that operations within a single thread are processed in the order.

        In multithreaded environment if a thread initiates a checkpoint, it's producer is blocked until the
        checkpoint flush is complete. This block is localized, other threads
        remain unblocked and can continue to perform other operations
        (such as upserts, updates, deletes), but they are prevented from initiating a new checkpoint
        until the existing one is finished.

        Args:
            checkpoint (object): The data item to add to the stream.
        """
        with self._checkpoint_lock:
            # clear the signal to indicate checkpoint operation is being processed.
            self._checkpoint_flush_signal.clear()
            with self._producer_lock:
                self._enqueue(checkpoint)
            # wait until the consumer flushes the buffer and sets the flag. This waits for a
            # full consumer flush + gRPC send round trip, not just queue capacity, so it is
            # timed separately from _queue_backpressure_ns.
            if not CAPTURE_PERFORMANCE_METRICS_ENABLED:
                flushed = self._checkpoint_flush_signal.wait(CHECKPOINT_OP_TIMEOUT_IN_SEC)
            else:
                t0 = time.perf_counter_ns()
                flushed = self._checkpoint_flush_signal.wait(CHECKPOINT_OP_TIMEOUT_IN_SEC)
                self._checkpoint_wait_ns += time.perf_counter_ns() - t0
            if not flushed:
                raise TimeoutError(
                    "Checkpoint flush timed out. Consumer may have failed to process checkpoint."
                )

    def add_record(self, record):
        """Adds a record to the stream. Guarantees that operations within a single thread are processed in the order.

        Args:
            record (object): The data item to add to the stream.
        """
        with self._producer_lock:
            self._enqueue(record)

    def add_task(self, task):
        """Adds a task to the stream. Guarantees that operations within a single thread are processed in the order.

        Args:
            task (common_pb2.Task): The task operation to add to the stream.
        """
        with self._producer_lock:
            self._enqueue(task)

    def add_warning(self, warning):
        """Adds a warning to the stream. Guarantees that operations within a single thread are processed in the order.

        Args:
            warning (common_pb2.Warning): The warning operation to add to the stream.
        """
        with self._producer_lock:
            self._enqueue(warning)

    def add_file_upload(self, chunks, metadata_record):
        """
        Adds file upload chunks and the metadata record contiguously to the stream.

        Args:
            chunks (Iterable[connector_sdk_pb2.UnstructuredRecord]): The file chunks to add to the stream.
            metadata_record (connector_sdk_pb2.StructuredRecord): The metadata record to add after all chunks.
        """
        with self._producer_lock:
            for chunk in chunks:
                self._enqueue(chunk)
            self._enqueue(metadata_record)

    def unblock(self):
        """
        Unblocks the queue, called by consumer after the checkpoint flush is completed.
        """
        self._checkpoint_flush_signal.set()

    def mark_done(self):
        """
        Marks the end of the stream by putting a sentinel in the queue.
        """
        with self._producer_lock:
            self._queue.put(self._sentinel)

    def __next__(self):
        """
        Retrieves the next item from the stream. Raises StopIteration when the sentinel is encountered.

        Returns:
            object: The next item in the stream.

        Raises:
            StopIteration: If the sentinel object is encountered.
        """
        # If stream is completed and buffer is empty, raise StopIteration. Else flush the buffer.
        if self._is_done and not self._buffer:
            raise StopIteration

        if self._is_done:
            return self._flush_buffer()

        return self._build_next_batch()

    def _build_next_batch(self):
        """
        Core logic to build the batch. The loop continues until the buffer is full,
        but can be interrupted by a checkpoint, warning, task, file upload chunk, or a sentinel from the producer.

        Returns:
            connector_sdk_pb2.UpdateResponse or list[connector_sdk_pb2.UpdateResponse]: Either a single response
            containing records, or a list of responses when flushing buffered records ahead of a checkpoint,
            warning, task, or file upload chunk.

        """
        while self._buffer_record_count < MAX_RECORDS_IN_BATCH and self._buffer_size_bytes < MAX_BATCH_SIZE_IN_BYTES:
            operation = self._dequeue()

            # Case 1: If operation is sentinel, mark the stream as done, flush the buffer.
            if operation is self._sentinel:
                self._is_done = True
                if self._buffer:
                    return self._flush_buffer()
                else:
                    raise StopIteration

            # Case 2: if operation is a Checkpoint, flush the buffer and send the checkpoint.
            elif isinstance(operation, connector_sdk_pb2.Checkpoint):
                return self._flush_buffer_on_checkpoint(operation)
            # Case 3: if operation is a Warning, flush the buffer and send the warning.
            elif isinstance(operation, common_pb2.Warning):
                return self._flush_buffer_on_warning(operation)
            # Case 4: if operation is a Task, flush the buffer and send the task.
            elif isinstance(operation, common_pb2.Task):
                return self._flush_buffer_on_task(operation)

            # Case 5: if operation is a UnstructuredRecord, flush the buffer and send the chunk on its own.
            # It must not be batched into StructuredRecords like a regular record.
            elif isinstance(operation, connector_sdk_pb2.UnstructuredRecord):
                return self._flush_buffer_on_file_upload_chunk(operation)

            # it is record, buffer it to flush in batches
            self._append_to_buffer(operation)

        # Case 6: If buffer size limit is reached, flush the buffer and return the response.
        return self._flush_buffer()

    def _flush_buffer_on_checkpoint(self, checkpoint: connector_sdk_pb2.Checkpoint):
        """
        Creates the responses containing the checkpoint and buffered records.

        Args:
            checkpoint (object): Checkpoint operation to be added to the response.
        """
        return self._flush_buffer_before(connector_sdk_pb2.UpdateResponse(checkpoint=checkpoint))

    def _flush_buffer_on_file_upload_chunk(self, chunk: connector_sdk_pb2.UnstructuredRecord):
        """
        Creates the responses containing the buffered records (if any) followed by the file upload chunk.

        Args:
            chunk (connector_sdk_pb2.UnstructuredRecord): File upload chunk operation to add to the response.
        """
        return self._flush_buffer_before(connector_sdk_pb2.UpdateResponse(unstructured_record=chunk))

    def _flush_buffer_before(self, response: connector_sdk_pb2.UpdateResponse):
        """
        Returns any buffered records before the given response, preserving stream order.

        Args:
            response (connector_sdk_pb2.UpdateResponse): The response to place after any buffered records.
        """
        responses = []
        if self._buffer:
            responses.append(self._flush_buffer())

        responses.append(response)
        return responses

    def _flush_buffer_on_warning(self, warning: common_pb2.Warning):
        """
        Creates the responses containing the buffered records (if any) followed by the warning.

        Args:
            warning (common_pb2.Warning): Warning operation to be added to the response.
        """
        return self._flush_buffer_before(connector_sdk_pb2.UpdateResponse(warning=warning))

    def _flush_buffer_on_task(self, task: common_pb2.Task):
        """
        Creates the responses containing the buffered records (if any) followed by the task.

        Args:
            task (common_pb2.Task): Task operation to be added to the response.
        """
        return self._flush_buffer_before(connector_sdk_pb2.UpdateResponse(task=task))

    def _flush_buffer(self):
        """
        Flushes the current buffer and returns a response containing the buffered records.

        Returns:
            connector_sdk_pb2.UpdateResponse: A response containing the buffered records.
        """
        batch_to_flush = self._buffer
        self._buffer = []
        self._buffer_record_count = 0
        self._buffer_size_bytes = 0
        if not CAPTURE_PERFORMANCE_METRICS_ENABLED:
            response = connector_sdk_pb2.UpdateResponse()
            response.structured_records.structured_records.extend(batch_to_flush)
        else:
            t0 = time.perf_counter_ns()
            response = connector_sdk_pb2.UpdateResponse()
            response.structured_records.structured_records.extend(batch_to_flush)
            self._sdk_batch_assembly_ns += time.perf_counter_ns() - t0
        return response
