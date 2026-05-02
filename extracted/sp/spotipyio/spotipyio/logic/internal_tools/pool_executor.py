from functools import partial
from typing import Sized, Any, Awaitable, Callable, List, Optional, Type

from asyncio_pool import AioPool
from tqdm import tqdm

from spotipyio.logic.internal_tools.logging import logger


class PoolExecutor:
    def __init__(self, pool_size: int = 5, validate_results: bool = True):
        self._pool_size = pool_size
        self._validate_results = validate_results

    async def run(
        self, iterable: Sized, func: Callable[..., Awaitable[Any]], expected_type: Optional[Type] = None
    ) -> List[Any]:
        if not iterable:
            logger.warning("PoolExecutor did not receive any values in iterable. Returning empty list by default")
            return []

        return await self._execute_in_pool(iterable=iterable, func=func, expected_type=expected_type)

    async def _execute_in_pool(
        self, iterable: Sized, func: Callable[..., Awaitable[Any]], expected_type: Optional[Type] = None
    ) -> List[Any]:
        pool = AioPool(self._pool_size)

        with tqdm(total=len(iterable)) as progress_bar:
            monitored_func = partial(self._execute_single, progress_bar, func)
            results = await pool.map(monitored_func, iterable)

        if self._validate_results:
            return self._filter_out_invalid_results(results, expected_type)

        return results

    @staticmethod
    async def _execute_single(progress_bar: tqdm, func: Callable[..., Awaitable[Any]], value: Any) -> Any:
        try:
            return await func(value)

        except Exception as e:
            logger.exception("PoolExecutor encountered exception")
            return e

        finally:
            progress_bar.update(1)

    @staticmethod
    def _filter_out_invalid_results(results: List[Any], expected_type: Type) -> List[Any]:
        valid_results = [result for result in results if isinstance(result, expected_type)]
        logger.info(f"Successfully retrieved {len(valid_results)} valid results out of {len(results)} total requests")

        return valid_results
