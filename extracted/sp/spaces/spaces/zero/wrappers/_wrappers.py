"""
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from contextvars import copy_context
from datetime import timedelta
from functools import partial
from functools import update_wrapper
from functools import wraps
from threading import Event
from types import FunctionType
from types import MethodType
from typing import Callable
from typing import Generator
from typing import Generic
from typing_extensions import assert_never
from weakref import finalize

from .. import client
from .. import context
from .. import torch
from ..api import GPUSize
from ..api import NvidiaIndex
from ..errors import ZeroGPUArgsPicklingError
from ..errors import ZeroGPUOutputUnpicklingError
from ..errors import ZeroGPUSerializationError
from ..errors import ZeroGPUTaskAborted
from ..errors import ZeroGPUTaskException
from ..types import Duration
from ..types import DynamicDuration
from ..types import Param
from . import _channel as channel
from . import _protocol as protocol
from ._protocol import Returned
from ._protocol import Sent
from ._protocol import Yielded
from ._worker import Worker


def process_duration(duration: Duration | None):
    if duration is None or isinstance(duration, timedelta):
        return duration
    return timedelta(seconds=duration)


def static_duration(duration: DynamicDuration[Param], *args: Param.args, **kwargs: Param.kwargs):
    if not callable(duration):
        return duration
    return duration(*args, **kwargs)


class GeneratorFunction(Generic[Param, Yielded, Sent, Returned]):
    """
    Function-like object that `inspect` (thus Gradio and friends) sees as a generator function
    Unlike an actual one, calling it runs `call` right away rather than at first `next`
    """
    __code__ = (lambda: (yield)).__code__
    __defaults__ = None
    __kwdefaults__ = None

    def __init__(self, task: Callable[..., object], call: Callable[Param, Generator[Yielded, Sent, Returned]]):
        self.__name__ = 'gpu_executor'
        update_wrapper(self, task)
        self.call = call

    def __call__(self, *args: Param.args, **kwargs: Param.kwargs):
        return self.call(*args, **kwargs)

    def __get__(self, instance: object, owner: type | None = None):
        return self if instance is None else MethodType(self, instance)

    def __reduce__(self):
        return self.__qualname__

    @property
    def __class__(self): # pyright: ignore[reportIncompatibleMethodOverride]
        return FunctionType


def generator_function_wrapper(
    task: Callable[Param, Generator[Yielded, Sent, Returned]],
    duration: DynamicDuration[Param],
    gpu_size: GPUSize | None,
) -> Callable[Param, Generator[Yielded, Sent, Returned]]:

    idle_workers: dict[NvidiaIndex, Worker[Yielded, Sent, Returned]] = {}
    task_id = id(task)

    # TODO: auto release after duration (release: stop|raise|None = raise, release_margin: duration = 0)

    @contextmanager
    def duration_warning(duration_seconds: float):
        done = Event()
        def warn_duration():
            if not done.wait(duration_seconds):
                client.duration_warning()
        with ThreadPoolExecutor(1) as executor:
            executor.submit(copy_context().run, warn_duration)
            try:
                yield
            finally:
                done.set()

    def gpu_executor(*args: Param.args, **kwargs: Param.kwargs):

        if Worker.forked:
            return task(*args, **kwargs)

        ctx = context.get()
        duration_ = static_duration(duration, *args, **kwargs)
        duration_ = process_duration(duration_)
        schedule_response = client.schedule(task_id=task_id, duration=duration_, gpu_size=gpu_size)
        allow_token = schedule_response.allowToken
        nvidia_index = schedule_response.nvidiaIndex
        nvidia_uuid = schedule_response.nvidiaUUID
        release = partial(client.release, allow_token)

        worker = idle_workers.pop(nvidia_index, None)
        if worker is not None and not (worker.process.is_alive() and schedule_response.idle):
            worker.shutdown()
            worker = None
        if worker is None:
            worker = Worker(task, allow_token, nvidia_uuid, ctx.get_server_ports())

        def done():
            idle_workers[nvidia_index] = worker
            release()

        def failed(aborted: bool = False):
            worker.shutdown()
            release(fail=True, allow_404=aborted)

        # Safeguard: a response left by a previous task would be taken for one of this task
        if worker.steps.pending():
            failed()
            raise AssertionError("Unexpected pending worker on re-use")

        started = False

        def discard(): # A generator that never started runs nothing, not even on `close`
            if not started:
                worker.shutdown()
                release()

        def forward() -> Generator[Yielded, Sent, Returned]:

            nonlocal started
            started = True

            match worker.tasks.send(((args, kwargs), ctx.worker_contextualizer())):
                case None:
                    pass
                case channel.PicklingFailure(cause) as failure:
                    failed()
                    raise ZeroGPUArgsPicklingError(worker.task_name, failure.traceback) from cause
                case channel.Closed():
                    failed(aborted=True)
                    raise ZeroGPUTaskAborted(f"GPU task aborted while sending arguments for `{worker.task_name}` task")

            with duration_warning(client.get_duration_seconds(duration_, gpu_size)):
                while True:

                    # TorchModes are thread-local and unpickling can trigger CUDA code
                    with ThreadPoolExecutor(1, initializer=torch.enter_mode) as executor:
                        received = executor.submit(worker.steps.recv).result()

                    match received:
                        case channel.Received(response):
                            pass
                        case channel.UnpicklingFailure(cause) as failure:
                            failed()
                            raise ZeroGPUOutputUnpicklingError(worker.task_name, failure.traceback) from cause
                        case channel.Closed():
                            failed(aborted=True)
                            raise ZeroGPUTaskAborted(f"GPU task aborted while waiting for `{worker.task_name}` task")

                    match response:
                        case protocol.Yield(value):
                            try:
                                sent = yield value
                            except (Exception, GeneratorExit) as e: # `close()` is nothing more than a GeneratorExit
                                request = protocol.Throw(e)
                            else:
                                request = protocol.Send(sent)
                        case protocol.Return(value):
                            done()
                            return value
                        case protocol.Raise(ZeroGPUSerializationError() as error, traceback):
                            failed()
                            print(traceback)
                            raise error
                        case protocol.Raise(Exception() as exception, traceback):
                            failed()
                            print(traceback)
                            raise ZeroGPUTaskException(
                                message=type(exception).__name__,
                                exception=exception,
                                traceback=traceback,
                            )
                        case protocol.Raise(generator_exit):
                            done()
                            raise generator_exit

                    match worker.steps.send(request):
                        case None:
                            pass
                        case channel.PicklingFailure(cause) as failure:
                            failed()
                            raise request.pickling_error(worker.task_name, failure.traceback) from cause
                        case channel.Closed():
                            failed(aborted=True)
                            raise ZeroGPUTaskAborted(f"GPU task aborted while resuming `{worker.task_name}` task")

        generator = forward()
        finalize(generator, discard)
        return generator

    return GeneratorFunction(task, gpu_executor)


def regular_function_wrapper(
    task: Callable[Param, Returned],
    duration: DynamicDuration[Param],
    gpu_size: GPUSize | None,
) -> Callable[Param, Returned]:

    @wraps(task)
    def generator_task(*args: Param.args, **kwargs: Param.kwargs):
        return task(*args, **kwargs)
        yield

    generator_executor = generator_function_wrapper(generator_task, duration, gpu_size)

    @wraps(task)
    def gpu_executor(*args: Param.args, **kwargs: Param.kwargs) -> Returned:
        try:
            assert_never(next(generator_executor(*args, **kwargs)))
        except StopIteration as stop:
            return stop.value

    # https://github.com/python/cpython/issues/91002
    if not hasattr(task, '__annotations__'):
        gpu_executor.__annotations__ = {}

    return gpu_executor
