from __future__ import annotations

import threading
from typing import Iterator
from typing import List
from typing import Sequence
from typing import Tuple

import pyarrow

from tecton_core.embeddings import execution_utils
from tecton_core.vendor import queue


QUEUE_TIMEOUT_SECS = 5

# NOTE: we set a max record batch size when using multiple model inference workers
# to better parallelize across our workers. The default max record batch size we get
# from the DuckDB SQL output is 1_000_000, which is quite large for embeddings inference
# since embedding 1M strings could take tens of minutes on longer strings.
#
# WARN: Setting this lower is not necessarily a 'free' speedup, since smaller record batches
# on high variance token lengths gives us less opportunity to optimize the batch size.
MULTITHREADED_MAX_RECORD_BATCH_SIZE = 250_000


def data_coordinator_thread_func(
    data_iter: pyarrow.RecordBatchReader,
    output_queue: queue.ClosableQueue,
    max_record_batch_size: int = MULTITHREADED_MAX_RECORD_BATCH_SIZE,
) -> None:
    for data in data_iter:
        if max_record_batch_size is None or len(data) < max_record_batch_size:
            output_queue.put(data)
        else:
            for offset in range(0, len(data), max_record_batch_size):
                length = min(len(data) - offset, max_record_batch_size)
                output_queue.put(data.slice(offset, length))

    output_queue.close()


def iterator_over_queue(q: queue.ClosableQueue) -> Iterator:
    while True:
        try:
            yield q.get(timeout=QUEUE_TIMEOUT_SECS)
        except queue.Closed as e:
            # NOTE: we are done if our input is closed!
            break
        except queue.Empty:
            continue


def _inference_on_record_batch(
    batch: pyarrow.RecordBatch,
    preprocess_func: execution_utils.PreprocessorCallable,
    preprocess_kwargs: execution_utils.P.kwargs,
    inference_func: execution_utils.ModelCallable,
    inference_kwargs: execution_utils.P.kwargs,
) -> Tuple[List[pyarrow.RecordBatch], List[execution_utils.ExceptionWrapper]]:
    token_batches = execution_utils.data_preprocessor_one_step(batch, preprocess_func, preprocess_kwargs)
    inference_results: List[pyarrow.RecordBatch] = []
    exceptions: List[execution_utils.ExceptionWrapper] = []
    for token_batch in token_batches:
        result = execution_utils.model_inference_one_step(token_batch, inference_func, inference_kwargs)
        if isinstance(result, execution_utils.ExceptionWrapper):
            exceptions.append(result)
        else:
            inference_results.append(result)
    if len(inference_results) > 0:
        # The dynamic token batching in preprocessing will likely increase the number of batches relative to the inputs.
        # This is to consolidate the results and prevent the # of batches from increasing.
        inference_results = pyarrow.Table.from_batches(inference_results).combine_chunks().to_batches()
    return inference_results, exceptions


def threaded_inference_func(
    input_queue: queue.ClosableQueue,
    output_queue: queue.ClosableQueue,
    preprocess_info: Tuple[execution_utils.PreprocessorCallable, execution_utils.FuncConfig],
    inference_info: Tuple[execution_utils.ModelCallable, execution_utils.FuncConfig],
) -> None:
    preprocess_func, preprocess_config = preprocess_info
    inference_func, inference_func_config = inference_info
    preprocess_kwargs = preprocess_config.load().kwargs()
    inference_kwargs = inference_func_config.load().kwargs()

    for batch in iterator_over_queue(input_queue):
        inference_results, exceptions = _inference_on_record_batch(
            batch, preprocess_func, preprocess_kwargs, inference_func, inference_kwargs
        )
        for result in (*inference_results, *exceptions):
            output_queue.put(result)


def execute_multithreaded(
    data_source: pyarrow.RecordBatchReader,
    preprocess_info: Tuple[execution_utils.PreprocessorCallable, execution_utils.FuncConfig],
    inference_info: Tuple[execution_utils.ModelCallable, Sequence[execution_utils.FuncConfig]],
) -> Iterator[pyarrow.RecordBatch]:
    # NOTE: for now this assumes that all data fits in memory. We will re-evaluate that in the future.
    input_queue = queue.ClosableQueue()  # Queue between coordinator and preprocessors
    output_queue = queue.ClosableQueue()  # Queue between preprocessors and model workers

    inference_func, inference_func_configs = inference_info

    # Start data coordinator
    coordinator = threading.Thread(target=data_coordinator_thread_func, args=(data_source, input_queue))
    coordinator.start()

    # Start model workers
    model_workers = [
        threading.Thread(
            target=threaded_inference_func,
            args=(
                input_queue,
                output_queue,
                preprocess_info,
                (inference_func, func_config),
            ),
            daemon=True,
        )
        for func_config in inference_func_configs
    ]
    for worker in model_workers:
        worker.start()

    coordinator.join()

    for worker in model_workers:
        worker.join()

    num_items = output_queue.qsize()

    # NOTE: this line means that we cannot work with larger than memory data.
    # We will come back to this later.
    output_batches = [output_queue.get() for _ in range(num_items)]

    for output_item in output_batches:
        if isinstance(output_item, execution_utils.ExceptionWrapper):
            output_item.reraise()

    yield from output_batches


def execute_singlethreaded(
    data_source: pyarrow.RecordBatchReader,
    preprocess_info: Tuple[execution_utils.PreprocessorCallable, execution_utils.FuncConfig],
    inference_info: Tuple[execution_utils.ModelCallable, Sequence[execution_utils.FuncConfig]],
) -> Iterator[pyarrow.RecordBatch]:
    preprocess_func, preprocess_config = preprocess_info
    preprocess_kwargs = preprocess_config.load().kwargs()

    inference_func, inference_config = inference_info
    if len(inference_config) > 1:
        msg = "Single threaded execution only supports one inference configuration"
        raise ValueError(msg)
    inference_kwargs = inference_config[0].load().kwargs()

    for batch in data_source:
        results, exceptions = _inference_on_record_batch(
            batch, preprocess_func, preprocess_kwargs, inference_func, inference_kwargs
        )
        if len(exceptions) > 0:
            exceptions[0].reraise()
        for result in results:
            yield result
