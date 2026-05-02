from typing import Generator, Union, Type, Any, List

from spotipyio.logic.consts.typing_consts import AF, F
from spotipyio.logic.internal_tools.pool_executor import PoolExecutor


class DataChunksGenerator:
    def __init__(self, pool_executor: PoolExecutor = PoolExecutor()):
        self._pool_executor = pool_executor

    async def execute_by_chunk_in_parallel(
        self, lst: list, func: Union[F, AF], expected_type: Type[Any], chunk_size: int
    ) -> List[Any]:
        chunks = self.generate_data_chunks(lst=lst, chunk_size=chunk_size)
        return await self._pool_executor.run(iterable=list(chunks), func=func, expected_type=expected_type)

    @staticmethod
    def generate_data_chunks(lst: list, chunk_size: int) -> Generator[list, None, None]:
        for i in range(0, len(lst), chunk_size):
            yield lst[i : i + chunk_size]
