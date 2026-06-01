import asyncio
import itertools
import math
from typing import Awaitable, Callable, Coroutine, cast

import structlog
from pydantic import BaseModel

logger = structlog.get_logger(__name__)

TWO_MB = 2 * 1024 * 1024


def get_size(data: BaseModel) -> int:
    serialized = data.model_dump_json()
    encoded = serialized.encode("utf-8")
    return len(encoded)


async def run_in_batches[T: BaseModel, U: BaseModel](
    fct: Callable[[T], Awaitable[U]],
    get_params_for_batch: Callable[[int, int], T],
    n_items: int,
    n_items_for_size_estimation: int = 3,
    size_estimation_factor: float = 1.25,
) -> list[U]:
    """Run a workflow in batches to avoid exceeding the 4MB limit of the workflow parameters/results.

    Args:
        fct (Callable[[T], Awaitable[U]]): The function to run. Must be a callable that takes a parameter of type T and returns an awaitable of type U.
        get_params_for_batch (Callable[[int, int], T]): A function that returns the parameters for a batch of items.
            The function takes two arguments: the index of the first item in the batch and the number of items in the batch.
        n_items (int): The total number of items to process. Must be greater than 0.
        n_items_for_size_estimation (int, optional): The number of items to use for estimating the size of the parameters and results. Defaults to 3.
        size_estimation_factor (float, optional): The factor to adjust the estimation of the item size. Defaults to 1.25 meaning that we assume item is average 25% larger than the estimated size.

    Returns:
        list[U]: The results of the function execution.
    """  # noqa: E501
    n_items_for_size_estimation = min(n_items_for_size_estimation, n_items)

    params = get_params_for_batch(0, n_items_for_size_estimation)
    first_batch_results = await fct(params)

    n_remaining_items = n_items - n_items_for_size_estimation

    if n_remaining_items <= 0:
        return [first_batch_results]

    estimated_param_size_in_bytes = get_size(params)
    estimated_result_size_in_bytes = get_size(first_batch_results)
    estimated_item_size_in_bytes = (
        max(estimated_param_size_in_bytes, estimated_result_size_in_bytes) // n_items_for_size_estimation
    )

    # Adjust the estimated item size by the size_estimation_factor
    adjusted_estimated_item_size_in_bytes = int(estimated_item_size_in_bytes * size_estimation_factor)

    if adjusted_estimated_item_size_in_bytes > TWO_MB:
        raise ValueError(
            f"Estimated item size is too large: {adjusted_estimated_item_size_in_bytes} bytes. Maximum allowed is {TWO_MB} bytes."  # noqa: E501
        )

    batch_size = min(TWO_MB // adjusted_estimated_item_size_in_bytes, n_remaining_items)
    nb_batches = math.ceil(n_remaining_items / batch_size)
    batch_size = n_remaining_items // nb_batches

    logger.debug(
        f"Estimated item size: {adjusted_estimated_item_size_in_bytes} bytes. Batch size: {batch_size} items. Number of batches: {nb_batches}"  # noqa: E501
    )

    # Create batches using itertools.batched for the remaining items
    tasks = []
    for batch_range in itertools.batched(range(n_items_for_size_estimation, n_items), batch_size):
        start_batch_idx = batch_range[0]
        effective_batch_size = len(batch_range)
        params = get_params_for_batch(start_batch_idx, effective_batch_size)
        task = asyncio.create_task(cast(Coroutine, fct(params)))
        tasks.append(task)

    results_of_batches = await asyncio.gather(*tasks)
    results_of_batches.insert(0, first_batch_results)

    return results_of_batches
