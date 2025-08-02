# arpakit

import asyncio
import logging
import multiprocessing
import threading
from abc import ABC
from datetime import timedelta
from random import randint
from typing import Any
from uuid import uuid4

from arpakitlib.ar_enumeration_util import Enumeration
from arpakitlib.ar_func_util import is_async_func, is_sync_func, is_coroutine
from arpakitlib.ar_sleep_util import sync_safe_sleep, async_safe_sleep

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class BaseWorker(ABC):
    def __init__(
            self,
            *,
            timeout_after_run: timedelta = timedelta(seconds=0.3),
            timeout_after_error_in_run: timedelta = timedelta(seconds=1),
            startup_funcs: list[Any] | None = None,
            worker_name: str | None = None,
            **kwargs
    ):
        self.timeout_after_run = timeout_after_run
        self.timeout_after_error_in_run = timeout_after_error_in_run

        if startup_funcs is None:
            startup_funcs = []
        self.startup_funcs = startup_funcs

        if worker_name is None:
            worker_name = self.__class__.__name__
        self.worker_name = worker_name
        self.worker_id = f"{str(uuid4()).replace('-', '')}_{randint(1000, 99999)}"

        self._logger = logging.getLogger(self.worker_fullname)

    @property
    def worker_fullname(self) -> str:
        return f"{self.worker_name}_{self.worker_id}"

    def sync_run_startup_funcs(self):
        self._logger.info("start")
        for startup_func in self.startup_funcs:
            if is_async_func(startup_func):
                asyncio.run(startup_func())
            elif is_coroutine(startup_func):
                async def __func():
                    await startup_func

                asyncio.run(__func())
            elif is_sync_func(startup_func):
                startup_func()
            else:
                raise TypeError("unknown startup_func type")
        self._logger.info("finish")

    def sync_on_startup(self):
        self.sync_run_startup_funcs()

    def sync_run(self):
        pass

    def sync_on_error(self, exception: Exception, **kwargs):
        pass

    def sync_safe_run(self):
        self._logger.info("start")
        try:
            self.sync_on_startup()
        except Exception as exception:
            self._logger.error("exception in sync_on_startup", exc_info=exception)
            raise
        while True:
            try:
                self.sync_run()
            except Exception as exception:
                self._logger.error("exception in sync_run", exc_info=exception)
                try:
                    self.sync_on_error(exception=exception)
                except Exception as exception_:
                    self._logger.error("exception in sync_on_error", exc_info=exception_)
                    raise
                sync_safe_sleep(self.timeout_after_error_in_run)
            sync_safe_sleep(self.timeout_after_run)

    async def async_run_startup_funcs(self):
        self._logger.info("start")
        for startup_func in self.startup_funcs:
            if is_async_func(startup_func):
                await startup_func()
            elif is_coroutine(startup_func):
                await startup_func
            elif is_sync_func(startup_func):
                startup_func()
            else:
                raise TypeError("unknown startup_func type")
        self._logger.info("finish")

    async def async_on_startup(self):
        await self.async_run_startup_funcs()

    async def async_run(self):
        pass

    async def async_on_error(self, exception: Exception, **kwargs):
        pass

    async def async_safe_run(self):
        self._logger.info("start async_safe_run")
        try:
            await self.async_on_startup()
        except Exception as exception:
            self._logger.error("exception in async_on_startup", exc_info=exception)
            raise
        while True:
            try:
                await self.async_run()
            except Exception as exception:
                self._logger.error("exception in async_run", exc_info=exception)
                try:
                    await self.async_on_error(exception=exception)
                except Exception as exception_:
                    self._logger.error("exception in async_on_error", exc_info=exception_)
                    raise
                await async_safe_sleep(self.timeout_after_error_in_run)
            await async_safe_sleep(self.timeout_after_run)


class SafeRunInBackgroundModes(Enumeration):
    async_task = "async_task"
    thread = "thread"
    process = "process"


def safe_run_worker_in_background(*, worker: BaseWorker, mode: str) -> (
        asyncio.Task | threading.Thread | multiprocessing.Process
):
    if mode == SafeRunInBackgroundModes.async_task:
        res: asyncio.Task = asyncio.create_task(worker.async_safe_run())
    elif mode == SafeRunInBackgroundModes.thread:
        res: threading.Thread = threading.Thread(
            target=worker.sync_safe_run,
            daemon=True
        )
        res.start()
    elif mode == SafeRunInBackgroundModes.process:
        res: multiprocessing.Process = multiprocessing.Process(
            target=worker.sync_safe_run,
            daemon=True
        )
        res.start()
    else:
        raise ValueError(f"unknown safe_run_mode={mode}")
    return res


def safe_run_workers_in_background(
        *, workers: list[BaseWorker], mode: str
) -> list[asyncio.Task] | list[threading.Thread] | list[multiprocessing.Process]:
    res = []
    for worker in workers:
        res.append(safe_run_worker_in_background(worker=worker, mode=mode))
    return res


async def a():
    print("1")


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
