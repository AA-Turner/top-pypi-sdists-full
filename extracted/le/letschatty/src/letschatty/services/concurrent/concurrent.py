from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Iterable, TypeVar, Optional, List, Any
import asyncio
from tqdm import tqdm
T = TypeVar('T')
R = TypeVar('R')

T = TypeVar('T')
R = TypeVar('R')

def concurrent_first_result(func: Callable[..., Optional[R]], iterable: Iterable[T], **kwargs: Any) -> Optional[R]:
    """
    Executes a function concurrently on an iterable with additional keyword parameters and returns the first non-None result.

    Args:
        func (Callable[..., Optional[R]]): The function to execute on each item, potentially taking additional parameters.
        iterable (Iterable[T]): The iterable to process.
        **kwargs: Variable keyword arguments to pass to the function.

    Returns:
        Optional[R]: The first non-None result, or None if all results are None.
    """
    def execute_func(item: T) -> Optional[R]:
        return func(item, **kwargs)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_func, item) for item in iterable]
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                return result
    return None

def concurrent_completed(func: Callable[..., R], iterable: Iterable[T], **kwargs: Any) -> List[R]:
    """
    Executes a function concurrently on an iterable with additional keyword parameters and returns all results.

    Args:
        func (Callable[..., R]): The function to execute on each item, potentially taking additional parameters.
        iterable (Iterable[T]): The iterable to process.
        **kwargs: Variable keyword arguments to pass to the function.

    Returns:
        List[R]: A list containing all the results.
    """
    def execute_func(item: T) -> R:
        return func(item, **kwargs)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_func, item) for item in iterable]
        return [future.result() for future in as_completed(futures)]

async def concurrent_completed_async(func: Callable[..., R], iterable: Iterable[T], **kwargs: Any) -> List[R]:
    """
    Executes an async function concurrently on an iterable with additional keyword parameters and returns all results.

    Args:
        func (Callable[..., R]): The async function to execute on each item, potentially taking additional parameters.
        iterable (Iterable[T]): The iterable to process.
        **kwargs: Variable keyword arguments to pass to the function.

    Returns:
        List[R]: A list containing all the results.
    """
    async def execute_func(item: T) -> R:
        return await func(item, **kwargs)

    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(execute_func(item)) for item in tqdm(iterable, total=len(iterable))]
        return await asyncio.gather(*tasks)
