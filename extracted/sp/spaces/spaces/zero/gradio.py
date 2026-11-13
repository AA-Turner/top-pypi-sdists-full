"""
"""
import inspect
import os
from contextlib import AbstractContextManager
from contextlib import contextmanager
from functools import wraps
from typing import Any
from typing import Callable
from typing import Literal
from typing import cast

import gradio as gr
from fastapi import FastAPI
from gradio import http_server
from gradio import routes
from gradio import utils
from gradio.context import LocalContext
from gradio.helpers import TrackedIterable
from gradio.queueing import Queue
from gradio.routes import App

from ..utils import create_thread_daemon
from ..utils import ShmFdQueue
from . import context
from .context import ZeroGPUContext
from .context import ZeroGPULog
from .errors import ZeroGPUException
from .errors import ZeroGPUError
from .errors import ZeroGPUTaskException
from .lifecycle import zerogpu_mode_enabled
from .lifecycle import zerogpu_startup
from .middleware import ASGIScope
from .middleware import get_server_ports
from .middleware import ZeroGPUMiddleware


orig_create_app = App.create_app
orig_mount_gradio_app = gr.mount_gradio_app
orig_start_server = http_server.start_server
orig_get_function_with_locals = utils.get_function_with_locals
orig_queue_start = Queue.start
orig_queue_methods: dict[str, Any] = {
    'set_progress': Queue.set_progress,
    'log_message': Queue.log_message,
}


try:
    Success = gr.Success # pyright: ignore[reportAttributeAccessIssue] (Gradio<5.10)
except AttributeError: # pragma: no cover
    Success = gr.Info


def info(title: str, message: str, level: Literal['success', 'info', 'warning'] = 'info'): # pragma: no cover
    params = inspect.signature(gr.Info).parameters
    kwargs: dict[str, Any] = {}
    if 'title' in params:
        kwargs = {**kwargs, 'title': title}
    match level:
        case 'info':
            return gr.Info(message, **kwargs)
        case 'success':
            return Success(message, **kwargs)
        case 'warning':
            return gr.Warning(message, **kwargs)


def error(title: str, message: str): # pragma: no cover
    params = inspect.signature(gr.Error).parameters
    kwargs: dict[str, Any] = {}
    if 'title' in params:
        kwargs = {**kwargs, 'title': title}
    if 'print_exception' in params:
        kwargs = {**kwargs, 'print_exception': False}
    return gr.Error(message, **kwargs)


def exception_mapper(detail: ZeroGPUError, exc: Exception | None, show_error: bool):
    if isinstance(exc, gr.Error):
        exc.print_exception = False
        return exc
    message = str(exc) if exc is not None and show_error else detail['message']
    return error(detail['title'], message)


def log_emitter(log: ZeroGPULog): # pragma: no cover
    return info(
        title=log['title'],
        message=log['message'],
        level=log['level'],
    )


def wrap_with_context(fn: Callable, context_factory: Callable[[], AbstractContextManager]):
    if inspect.isasyncgenfunction(fn):
        @wraps(fn)
        async def asyncgen_wrapper(*args, **kwargs):
            iterator = fn(*args, **kwargs)
            while True:
                try:
                    with context_factory():
                        response = await iterator.__anext__()
                except StopAsyncIteration:
                    break
                yield response
        return asyncgen_wrapper

    elif inspect.iscoroutinefunction(fn):
        @wraps(fn)
        async def async_wrapper(*args, **kwargs):
            with context_factory():
                return await fn(*args, **kwargs)
        return async_wrapper

    elif inspect.isgeneratorfunction(fn):
        @wraps(fn)
        def gen_wrapper(*args, **kwargs):
            iterator = fn(*args, **kwargs)
            while True:
                try:
                    with context_factory():
                        response = next(iterator)
                except StopIteration:
                    break
                yield response
        return gen_wrapper

    else:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            with context_factory():
                return fn(*args, **kwargs)
        return wrapper


class WorkerContextualizer:
    def __init__(self):
        self.event_id = LocalContext.event_id.get(None)
        self.in_event_listener = LocalContext.in_event_listener.get(False)
        self.progress = LocalContext.progress.get(None)
    def __call__(self):
        LocalContext.event_id.set(self.event_id)
        LocalContext.in_event_listener.set(self.in_event_listener)
        LocalContext.progress.set(self.progress)


def disconnect_detector(): # pragma: no cover
    blocks = LocalContext.blocks.get(None)
    event_id = LocalContext.event_id.get(None)
    if blocks is not None and event_id is not None:
        for job in blocks._queue.active_jobs:
            for event in job or []:
                if event._id == event_id:
                    return not event.alive
    return False


def setup_middleware(app: FastAPI, *, skip_zerogpu_startup: bool = False):
    mounted = any(middleware.cls is ZeroGPUMiddleware for middleware in app.user_middleware)
    if not mounted:
        app.add_middleware(ZeroGPUMiddleware, skip_zerogpu_startup=skip_zerogpu_startup)


def patch():
    @wraps(orig_create_app)
    def create_app(*args, **kwargs):
        app = orig_create_app(*args, **kwargs)
        setup_middleware(app, skip_zerogpu_startup=True)
        return app


    @wraps(orig_mount_gradio_app)
    def mount_gradio_app(*args, **kwargs):
        app = orig_mount_gradio_app(*args, **kwargs)
        setup_middleware(app)
        return app


    @wraps(orig_start_server)
    def start_server(*args, **kwargs):
        if zerogpu_mode_enabled():
            zerogpu_startup()
        return orig_start_server(*args, **kwargs)


    @wraps(orig_get_function_with_locals)
    def get_function_with_locals(
        fn: Callable,
        blocks: gr.Blocks,
        event_id: str | None,
        in_event_listener: bool,
        request: gr.Request | None,
        *args,
        **kwargs,
    ):
        wrapped = orig_get_function_with_locals(
            fn=fn,
            blocks=blocks,
            event_id=event_id,
            in_event_listener=in_event_listener,
            request=request,
            *args,
            **kwargs,
        )

        if not zerogpu_mode_enabled():
            return wrapped

        @contextmanager
        def execution_context():
            if request is not None and request.request is not None:
                server_ports = get_server_ports(cast(ASGIScope, request.request.scope))
            else:
                server_ports = context.get().get_server_ports()
            with context.set_context_var(ZeroGPUContext(
                log_emitter=log_emitter,
                worker_contextualizer=WorkerContextualizer,
                disconnect_detector=disconnect_detector,
                server_ports=server_ports,
                headers={key.lower(): value for key, value in dict(getattr(request, 'headers', {})).items()},
            )):
                try:
                    yield
                except ZeroGPUTaskException as exc:
                    raise exception_mapper(
                        detail=exc.detail,
                        exc=exc.exception,
                        show_error=blocks.show_error,
                    ) from exc
                except ZeroGPUException as exc:
                    raise exception_mapper(
                        detail=exc.detail,
                        exc=None,
                        show_error=blocks.show_error,
                    ) from exc

        return wrap_with_context(wrapped, execution_context)

    App.create_app = create_app
    gr.mount_gradio_app = mount_gradio_app
    routes.mount_gradio_app = mount_gradio_app
    http_server.start_server = start_server
    utils.get_function_with_locals = get_function_with_locals
    _patch_queue()


def _patch_queue():

    def queue_start(self: Queue):
        orig_queue_start(self)
        create_thread_daemon(start_rpc, self).start()

    def start_rpc(self: Queue):
        self._rpc_queue = ShmFdQueue() # pyright: ignore[reportAttributeAccessIssue]
        self._server_pid = os.getpid() # pyright: ignore[reportAttributeAccessIssue]
        while True:
            method_name, args, kwargs = self._rpc_queue.get() # pyright: ignore[reportAttributeAccessIssue]
            method = getattr(self, method_name, None)
            assert callable(method)
            method(*args, **kwargs)

    def rpc_method(method_name: str):
        def method(self: Queue, *args, **kwargs):
            rpc_queue = getattr(self, '_rpc_queue', None)
            server_pid = getattr(self, '_server_pid', None)
            if server_pid != os.getpid() and rpc_queue is not None:
                rpc_queue.put((method_name, args, kwargs))
            else:
                orig_queue_methods[method_name](self, *args, **kwargs)
        return method

    def tracked_iterable__getstate__(self):
        return {**self.__dict__, 'iterable': None, '_tqdm': None}

    Queue.start = queue_start
    setattr(TrackedIterable, '__getstate__', tracked_iterable__getstate__)
    for method_name, _method in orig_queue_methods.items():
        setattr(Queue, method_name, rpc_method(method_name))
