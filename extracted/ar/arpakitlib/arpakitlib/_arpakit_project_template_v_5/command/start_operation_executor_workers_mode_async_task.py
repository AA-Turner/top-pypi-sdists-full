import asyncio

from arpakitlib.ar_base_worker_util import safe_run_workers_in_background, SafeRunInBackgroundModes
from project.core.setup_logging import setup_logging
from project.operation_execution.operation_executor_worker import OperationExecutorWorker
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db


async def __async_command():
    setup_logging()
    workers = []
    for i in range(int(input("amount of workers: "))):
        workers.append(OperationExecutorWorker(
            sqlalchemy_db=get_cached_sqlalchemy_db(),
        ))
    async_tasks = safe_run_workers_in_background(
        workers=workers,
        mode=SafeRunInBackgroundModes.async_task
    )
    await asyncio.gather(*async_tasks)


if __name__ == '__main__':
    asyncio.run(__async_command())
