"""
"""
import multiprocessing
import os
import signal
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from contextlib import nullcontext
from contextvars import copy_context
from datetime import timedelta
from functools import partial
from functools import wraps
from multiprocessing.synchronize import Event
from multiprocessing.context import ForkProcess
from pickle import PicklingError
from queue import Empty
from queue import Queue as ThreadQueue
from threading import Event as ThreadEvent
from threading import Thread
from typing import TYPE_CHECKING
from typing import Callable
from typing import Generator
from typing import Generic
from typing_extensions import assert_never

from ..config import Config
from ..utils import debug
from ..utils import drop_params
from ..utils import SimpleQueue as Queue
from . import client
from . import context
from . import torch
from .api import AllowToken
from .api import GPUSize
from .api import NvidiaIndex
from .api import NvidiaUUID
from .errors import ZeroGPUTaskAborted
from .errors import ZeroGPUTaskException
from .tqdm import remove_tqdm_multiprocessing_lock
from .tqdm import tqdm
from .utils import apply_cleanups
from .utils import get_process_connections
from .types import * # TODO: Please don't do that


GENERATOR_GLOBAL_TIMEOUT = 20 * 60

SPAWN_PROGRESS_CLEANUP = 0.1
SPAWN_PROGRESS_INIT = 0.1


multiprocessing_ctx = multiprocessing.get_context('fork')
Process = multiprocessing_ctx.Process
forked = False


class Worker(Generic[Res]):
    process: ForkProcess
    arg_queue: Queue[tuple[Params, Callable[[], None]]]
    res_queue: Queue[Res | None]
    _sentinel: Thread

    def __init__(
        self,
        target: Callable[[
            Queue[tuple[Params, Callable[[], None]]],
            Queue[Res | None],
            Event,
            AllowToken,
            NvidiaUUID,
            list[int],
        ], None],
        allow_token: str,
        nvidia_uuid: str,
        server_ports: set[int],
    ):
        self._sentinel = Thread(target=self._close_on_exit, daemon=True)
        self.arg_queue = Queue()
        self.res_queue = Queue()
        self.stop_event = Event(ctx=multiprocessing_ctx)
        debug(f"{self.arg_queue._writer.fileno()=}") # pyright: ignore [reportAttributeAccessIssue]
        debug(f"{self.res_queue._writer.fileno()=}") # pyright: ignore [reportAttributeAccessIssue]
        fds = [conn.fd for conn in get_process_connections() if conn.port in server_ports]
        args = self.arg_queue, self.res_queue, self.stop_event, allow_token, nvidia_uuid, fds
        if TYPE_CHECKING:
            target(*args)
        self.process = Process(
            target=target,
            args=args,
            daemon=True,
        )
        self.process.start()
        self._sentinel.start()

    def _close_on_exit(self):
        assert (pid := self.process.pid) is not None
        self.process.join()
        self.arg_queue.close()
        self.res_queue.wlock_release()
        apply_cleanups(pid)
        self.res_queue.put(None)


def worker_init(
    allow_token: str,
    nvidia_uuid: str,
    fds: list[int],
) -> None | ExceptionResult:
    # Immediately close file descriptors
    for fd in fds:
        try:
            os.close(fd)
        except Exception as e: # pragma: no cover
            if isinstance(e, OSError) and e.errno == 9:
                continue
            return exception_result(e)
    try:
        remove_tqdm_multiprocessing_lock()
    except Exception: # pragma: no cover
        print("Error while trying to remove tqdm mp_lock:")
        traceback.print_exc()
    progress = nullcontext()
    if tqdm is not None and Config.zero_gpu_v2:
        progress = tqdm(total=100, desc="ZeroGPU init", file=open(os.devnull, 'w'))
    try: # Unrecoverable init part
        with progress as progress:
            current_progress = 0 # Gradio does not support float progress updates
            def update(n: float):
                nonlocal current_progress
                current_progress += n
                if progress is not None:
                    progress.update(round(current_progress * 100) - progress.n)
            client.allow(allow_token)
            update(SPAWN_PROGRESS_CLEANUP)
            torch.unpatch()
            torch.init(nvidia_uuid)
            update(SPAWN_PROGRESS_INIT)
            callback = None
            if (transfer_size := torch.size()) > 0:
                remaining = 1 - (SPAWN_PROGRESS_CLEANUP + SPAWN_PROGRESS_INIT)
                callback = lambda n: update(n * remaining / transfer_size)
            torch.move(callback=callback)
    except Exception as e: # pragma: no cover
        return exception_result(e)


def process_duration(duration: Duration | None):
    if duration is None or isinstance(duration, timedelta):
        return duration
    return timedelta(seconds=duration)


def static_duration(duration: DynamicDuration[Param], *args: Param.args, **kwargs: Param.kwargs):
    if not callable(duration):
        return duration
    return duration(*args, **kwargs)


def regular_function_wrapper(
    task: Callable[Param, Res],
    duration: DynamicDuration[Param],
    gpu_size: GPUSize | None,
) -> Callable[Param, Res]:

    workers: dict[NvidiaIndex, Worker[RegularResQueueResult[Res] | None]] = {}
    task_id = id(task)

    @wraps(task)
    def gpu_executor(*args: Param.args, **kwargs: Param.kwargs) -> Res:

        if forked:
            return task(*args, **kwargs)

        ctx = context.get()
        duration_ = static_duration(duration, *args, **kwargs)
        duration_ = process_duration(duration_)
        schedule_response = client.schedule(task_id=task_id, duration=duration_, gpu_size=gpu_size)
        allow_token = schedule_response.allowToken
        nvidia_index = schedule_response.nvidiaIndex
        nvidia_uuid = schedule_response.nvidiaUUID
        release = partial(client.release, allow_token)

        try:
            worker = workers.pop(nvidia_index)
        except KeyError:
            worker = None

        if worker is not None and worker.process.is_alive() and schedule_response.idle:
            assert worker.arg_queue.empty()
            assert worker.res_queue.empty()
        else:
            worker = Worker(worker_loop, allow_token, nvidia_uuid, ctx.get_server_ports())

        worker_context_setup = ctx.worker_contextualizer()

        try:
            worker.arg_queue.put(((args, kwargs), worker_context_setup))
        except PicklingError: # TODO: detailed serialization diagnostic
            release(fail=True)
            raise

        duration_seconds = client.get_duration_seconds(duration_, gpu_size)
        res_event = ThreadEvent()
        def warn_duration():
            if not res_event.wait(duration_seconds):
                client.duration_warning()

        with ThreadPoolExecutor(1) as executor:
            executor.submit(copy_context().run, warn_duration)
            try:
                res = worker.res_queue.get()
                if res is None:
                    release(fail=True, allow_404=True)
                    raise ZeroGPUTaskAborted("GPU task aborted")
                if isinstance(res, ExceptionResult):
                    release(fail=True)
                    print(res.traceback)
                    raise ZeroGPUTaskException(
                        message=res.error_cls,
                        exception=res.exception,
                        traceback=res.traceback,
                    )
                if isinstance(res, OkResult):
                    workers[nvidia_index] = worker
                    release()
                    return res.value
                assert_never(res)
            finally:
                res_event.set()


    def worker_loop(
        arg_queue: Queue[tuple[Params, Callable[[], None]]],
        res_queue: Queue[RegularResQueueResult[Res] | None],
        _stop_event: Event,
        allow_token: str,
        nvidia_uuid: str,
        fds: list[int],
    ):
        global forked
        forked = True
        signal.signal(signal.SIGTERM, drop_params(arg_queue.close))
        initialized = False
        while True:
            try:
                (args, kwargs), worker_context_setup = arg_queue.get()
            except OSError:
                break
            if not initialized:
                if (res := worker_init(
                    allow_token=allow_token,
                    nvidia_uuid=nvidia_uuid,
                    fds=fds,
                )) is not None:
                    res_queue.put(res)
                    return
                initialized = True
            def run_task():
                try:
                    res = task(*args, **kwargs) # pyright: ignore [reportCallIssue]
                except Exception as e:
                    res = exception_result(e)
                else:
                    res = OkResult(res)
                try:
                    res_queue.put(res)
                except PicklingError as e:
                    res_queue.put(exception_result(e))
            worker_context_setup()
            context = copy_context()
            with ThreadPoolExecutor() as gpu_executor:
                future = gpu_executor.submit(context.run, run_task)
            future.result()

    # https://github.com/python/cpython/issues/91002
    if not hasattr(task, '__annotations__'):
        gpu_executor.__annotations__ = {}

    return gpu_executor


def generator_function_wrapper(
    task: Callable[Param, Generator[Res, None, None]],
    duration: DynamicDuration[Param],
    gpu_size: GPUSize | None,
) -> Callable[Param, Generator[Res, None, None]]:

    workers: dict[NvidiaIndex, Worker[GeneratorResQueueResult[Res] | None]] = {}
    task_id = id(task)

    @wraps(task)
    def gpu_executor(*args: Param.args, **kwargs: Param.kwargs) -> Generator[Res, None, None]:

        if forked:
            yield from task(*args, **kwargs)
            return

        ctx = context.get()
        duration_ = static_duration(duration, *args, **kwargs)
        duration_ = process_duration(duration_)
        schedule_response = client.schedule(task_id=task_id, duration=duration_, gpu_size=gpu_size)
        allow_token = schedule_response.allowToken
        nvidia_index = schedule_response.nvidiaIndex
        nvidia_uuid = schedule_response.nvidiaUUID
        release = partial(client.release, allow_token)

        try:
            worker = workers.pop(nvidia_index)
        except KeyError:
            worker = None

        if worker is not None and worker.process.is_alive() and schedule_response.idle:
            assert worker.arg_queue.empty()
            assert worker.res_queue.empty()
        else:
            worker = Worker(worker_loop, allow_token, nvidia_uuid, ctx.get_server_ports())

        worker_context_setup = ctx.worker_contextualizer()

        try:
            worker.arg_queue.put(((args, kwargs), worker_context_setup))
        except PicklingError: # TODO: detailed serialization diagnostic
            release(fail=True)
            raise

        duration_seconds = client.get_duration_seconds(duration_, gpu_size)
        res_event = ThreadEvent()
        def warn_duration():
            if not res_event.wait(duration_seconds):
                client.duration_warning()

        yield_queue: ThreadQueue[YieldQueueResult[Res]] = ThreadQueue()
        def fill_yield_queue(worker: Worker[GeneratorResQueueResult[Res] | None]):
            torch.enter_mode() # TorchModes are thread-local and unpickling can trigger CUDA code
            while True:
                res = worker.res_queue.get()
                if res is None:
                    release(fail=True, allow_404=True)
                    yield_queue.put(AbortedResult())
                    return
                if isinstance(res, ExceptionResult):
                    release(fail=True)
                    yield_queue.put(res)
                    return
                if isinstance(res, EndResult):
                    workers[nvidia_index] = worker
                    release()
                    yield_queue.put(EndResult())
                    return
                if isinstance(res, OkResult):
                    yield_queue.put(OkResult(res.value))
                    continue
                assert_never(res)
        with ThreadPoolExecutor(2) as e:
            _ = e.submit(copy_context().run, warn_duration)
            f = e.submit(copy_context().run, fill_yield_queue, worker)
            f.add_done_callback(lambda _: res_event.set())
            f.add_done_callback(lambda _: debug("fill_yield_queue DONE"))
            while True:
                try:
                    res = yield_queue.get(timeout=GENERATOR_GLOBAL_TIMEOUT)
                except Empty: # pragma: no cover
                    debug(f"yield_queue TIMEOUT ({GENERATOR_GLOBAL_TIMEOUT=})")
                    raise
                if isinstance(res, AbortedResult):
                    raise ZeroGPUTaskAborted("GPU task aborted")
                if isinstance(res, ExceptionResult):
                    print(res.traceback)
                    raise ZeroGPUTaskException(
                        message=res.error_cls,
                        exception=res.exception,
                        traceback=res.traceback,
                    )
                if isinstance(res, EndResult):
                    break
                if isinstance(res, OkResult):
                    try:
                        yield res.value
                    except GeneratorExit:
                        worker.stop_event.set()
                        raise
                    continue
                debug(f"gpu_executor: assert_never({res=})")
                assert_never(res)


    def worker_loop(
        arg_queue: Queue[tuple[Params, Callable[[], None]]],
        res_queue: Queue[GeneratorResQueueResult[Res] | None],
        stop_event: Event,
        allow_token: str,
        nvidia_uuid: str,
        fds: list[int],
    ):
        global forked
        forked = True
        signal.signal(signal.SIGTERM, drop_params(arg_queue.close))
        initialized = False
        while True:
            try:
                (args, kwargs), worker_context_setup = arg_queue.get()
            except OSError:
                break
            stop_event.clear()
            if not initialized:
                if (res := worker_init(
                    allow_token=allow_token,
                    nvidia_uuid=nvidia_uuid,
                    fds=fds,
                )) is not None:
                    res_queue.put(res)
                    return
                initialized = True
            def iterate():
                gen = task(*args, **kwargs) # type: ignore
                while True:
                    try:
                        res = next(gen)
                    except StopIteration:
                        break
                    except Exception as e:
                        res_queue.put(exception_result(e))
                        break
                    if stop_event.is_set():
                        gen.close()
                        break
                    try:
                        res_queue.put(OkResult(res))
                    except PicklingError as e:
                        res_queue.put(exception_result(e))
                        break
                    else:
                        continue
            worker_context_setup()
            with ThreadPoolExecutor() as gpu_executor:
                gpu_executor.submit(copy_context().run, iterate)
            res_queue.put(EndResult())

    # https://github.com/python/cpython/issues/91002
    if not hasattr(task, '__annotations__'):
        gpu_executor.__annotations__ = {}

    return gpu_executor


def exception_result(exc: Exception) -> ExceptionResult:
    formatted = traceback.format_exception(type(exc), exc, exc.__traceback__)
    return ExceptionResult(
        traceback=''.join(formatted),
        error_cls=exc.__class__.__name__,
        exception=exc,
    )
