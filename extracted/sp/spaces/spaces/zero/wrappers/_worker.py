"""
"""
from __future__ import annotations

import multiprocessing
import os
import signal
import socket
import traceback
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from contextlib import nullcontext
from contextvars import copy_context
from functools import partial
from typing import Callable
from typing import ClassVar
from typing import Generator
from typing import Generic
from typing_extensions import Never

from ...config import Config
from ...utils import create_thread_daemon
from ...utils import drop_params
from .. import client
from .. import torch
from ..errors import ZeroGPUArgsUnpicklingError
from ..errors import ZeroGPUInputUnpicklingError
from ..errors import ZeroGPUSerializationError
from ..tqdm import remove_tqdm_multiprocessing_lock
from ..tqdm import tqdm
from ..utils import apply_cleanups
from ..utils import get_process_connections
from . import _channel as channel
from . import _protocol as protocol
from ._channel import Channel
from ._protocol import Returned
from ._protocol import Sent
from ._protocol import Yielded


SPAWN_PROGRESS_CLEANUP = 0.1
SPAWN_PROGRESS_INIT = 0.1


Process = multiprocessing.get_context('fork').Process


class Worker(Generic[Yielded, Sent, Returned]):
    """
    Process running `task` each time it is asked to. Both sides are linked by two channels:

    - `tasks`: tasks to run, one at a time
    - `steps`: generator forwarding protocol of the current task

    Main process side is `__init__`, `shutdown` and the `tasks` and `steps` attributes
    Worker process side is `run` (and what it calls), with its own `tasks` and `steps` ends

    Main process ends are inherited by the workers forked afterwards and worker ends can be
    inherited by worker subprocesses, so closing an end is not reliably seen by the other one
    Channels are thus shut down instead: by `shutdown` and when the worker process exits
    """

    forked: ClassVar = False # Whether current process is a worker one

    def __init__(
        self,
        task: Callable[..., Generator[Yielded, Sent, Returned]],
        allow_token: str,
        nvidia_uuid: str,
        server_ports: set[int],
    ):
        self.task = task
        self.task_name: str = getattr(task, '__name__', repr(task))
        self.allow_token = allow_token
        self.nvidia_uuid = nvidia_uuid
        self.fds = [conn.fd for conn in get_process_connections() if conn.port in server_ports]
        self.tasks, tasks = Channel[protocol.Task, Never].pair()
        self.steps, steps = Channel[protocol.Request[Sent], protocol.Response[Yielded, Returned]].pair()
        self.process = Process(
            target=self.run,
            args=(tasks, steps),
            daemon=True,
        )
        self.process.start()
        tasks.close()
        steps.close()
        create_thread_daemon(self.watch).start()

    def watch(self):
        assert (pid := self.process.pid) is not None
        self.process.join()
        apply_cleanups(pid)
        self.shutdown()

    def shutdown(self):
        """
        Worker process exits as soon as its current step (if any) is done
        """
        self.tasks.shutdown()
        self.steps.shutdown()

    def run(
        self,
        tasks: Channel[Never, protocol.Task],
        steps: Channel[protocol.Response[Yielded, Returned], protocol.Request[Sent]],
    ):
        Worker.forked = True
        # Main process ends have been inherited
        self.tasks.close()
        self.steps.close()
        def terminate():
            # No more incoming task or request: worker exits once its current step (if any) is done
            tasks.shutdown(socket.SHUT_RD)
            steps.shutdown(socket.SHUT_RD)
        signal.signal(signal.SIGTERM, drop_params(terminate))
        initialized = False
        while True:
            match tasks.recv():
                case channel.Received((params, worker_context_setup)):
                    pass
                case channel.UnpicklingFailure() as failure:
                    return self.report(steps, ZeroGPUArgsUnpicklingError, failure)
                case channel.Closed(): # Main process is done with this worker or SIGTERM
                    return
            if not initialized:
                if (error := self.initialize()) is not None:
                    steps.send(error)
                    return
                initialized = True
            worker_context_setup()
            with ThreadPoolExecutor() as executor:
                executor.submit(copy_context().run, self.serve, steps, params).result()

    def serve(
        self,
        steps: Channel[protocol.Response[Yielded, Returned], protocol.Request[Sent]],
        params: protocol.Params,
    ):
        """
        Runs one task: drives its generator according to the requests and reports each outcome
        """
        args, kwargs = params
        try:
            generator = self.task(*args, **kwargs)
        except Exception as e:
            steps.send(protocol.Raise.of(e))
            return
        advance = partial(next, generator)
        with closing(generator):
            while True:

                try:
                    response = protocol.Yield(advance())
                except StopIteration as stop:
                    response = protocol.Return(stop.value)
                except (Exception, GeneratorExit) as e:
                    response = protocol.Raise.of(e)

                match steps.send(response):
                    case None:
                        pass
                    case channel.PicklingFailure() as failure:
                        return self.report(steps, response.pickling_error, failure)
                    case channel.Closed(): # pragma: no cover
                        return # Main process only gives up on its turn. Not expected to happen

                match response:
                    case protocol.Yield():
                        pass
                    case protocol.Return() | protocol.Raise():
                        return

                match steps.recv():
                    case channel.Received(request):
                        pass
                    case channel.UnpicklingFailure() as failure:
                        return self.report(steps, ZeroGPUInputUnpicklingError, failure)
                    case channel.Closed(): # Task has been given up by the main process or SIGTERM
                        return

                match request:
                    case protocol.Send(value):
                        advance = partial(generator.send, value)
                    case protocol.Throw(exception):
                        advance = partial(generator.throw, exception)

    def report(
        self,
        steps: Channel[protocol.Response[Yielded, Returned], protocol.Request[Sent]],
        error_type: type[ZeroGPUSerializationError],
        failure: channel.Failure,
    ):
        error = error_type(self.task_name, failure.traceback)
        steps.send(protocol.Raise(error, error.traceback))

    def initialize(self):
        # Immediately close file descriptors
        for fd in self.fds:
            try:
                os.close(fd)
            except Exception as e: # pragma: no cover
                if isinstance(e, OSError) and e.errno == 9:
                    continue
                return protocol.Raise.of(e)
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
                client.allow(self.allow_token)
                update(SPAWN_PROGRESS_CLEANUP)
                torch.unpatch()
                torch.init(self.nvidia_uuid)
                update(SPAWN_PROGRESS_INIT)
                callback = None
                if (transfer_size := torch.size()) > 0:
                    remaining = 1 - (SPAWN_PROGRESS_CLEANUP + SPAWN_PROGRESS_INIT)
                    callback = lambda n: update(n * remaining / transfer_size)
                torch.move(callback=callback)
        except Exception as e: # pragma: no cover
            return protocol.Raise.of(e)
