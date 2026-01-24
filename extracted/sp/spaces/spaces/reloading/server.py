"""
"""
import traceback
import threading
import warnings
from pathlib import Path
from queue import Queue
from typing import Any
from typing import Callable
from typing import NamedTuple
from typing_extensions import assert_type
from typing_extensions import Never
from uuid import uuid4

from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import HTTPException
from uvicorn import Config
from uvicorn import Server

with warnings.catch_warnings():
    warnings.filterwarnings('ignore', message='torch.distributed', category=FutureWarning)
    from .._vendor import codefind

from .._vendor.jurigged.codetools import CodeFile
from .._vendor.jurigged.codetools import CodeFileOperation
from .._vendor.jurigged.codetools import AddOperation
from .._vendor.jurigged.codetools import UpdateOperation
from .._vendor.jurigged.codetools import DeleteOperation
from .._vendor.jurigged.codetools import ExceptionOperation
from .._vendor.jurigged.codetools import Extent
from .._vendor.jurigged.codetools import LineDefinition
from .._vendor.jurigged.codetools import GroupDefinition
from .._vendor.jurigged.codetools import ModuleCode
from .._vendor.jurigged.codetools import ClassDefinition
from .._vendor.jurigged.codetools import FunctionDefinition
from .._vendor.jurigged.register import EventSource
from .._vendor.jurigged.register import Registry
from .._vendor.jurigged.utils import glob_filter
from .._vendor.sse_starlette import EventSourceResponse
from ..utils import create_thread

from .types import ApiCreateReloadRequest
from .types import ApiCreateReloadResponse
from .types import ApiCreateReloadResponseError
from .types import ApiCreateReloadResponseSuccess
from .types import ApiGetReloadRequest
from .types import ApiGetReloadEventSourceData
from .types import ApiGetStatusRequest
from .types import ApiGetStatusResponse
from .types import ApiFetchContentsRequest
from .types import ApiFetchContentsResponse
from .types import ApiFetchContentsResponseError
from .types import ApiFetchContentsResponseSuccess
from .types import ReloadRegion
from .types import ReloadOperationError
from .types import ReloadOperationException
from .types import ReloadOperationObject
from .types import ReloadOperationRun
from .types import ReloadOperationUI


class ReloadRun(NamedTuple):
    activity: EventSource
    thread: threading.Thread


class ReloadServer:
    def __init__(
        self,
        prerun: Callable[[], Any],
        postrun: Callable[[], bool],
        stop_event: threading.Event,
    ):
        self.prerun = prerun
        self.postrun = postrun
        self.stop_event = stop_event
        self.create_lock = threading.Lock()
        self.reload_runs: dict[str, ReloadRun] = {}
        self.active_reload_id: str | None = None
        self.router = APIRouter()
        self.router.add_api_route('/healthz', lambda: {}, methods=['GET'])
        self.router.add_api_route('/get-status', self.get_status, methods=['POST'])
        self.router.add_api_route('/fetch-contents', self.fetch_contents, methods=['POST'])
        self.router.add_api_route('/create-reload', self.create_reload, methods=['POST'])
        self.router.add_api_route('/get-reload', self.get_reload, methods=['POST'])
        self.registry = Registry()
        self.registry.auto_register(filter=glob_filter('./*.py'))


    def get_status(self, req: ApiGetStatusRequest) -> ApiGetStatusResponse:
        """
        POST /get-status
        """
        raise NotImplementedError # pragma: no cover


    def fetch_contents(self, req: ApiFetchContentsRequest) -> ApiFetchContentsResponse:
        """
        POST /fetch-contents
        """

        filepath = (Path.cwd() / req.filepath).resolve()
        if not filepath.is_relative_to(Path.cwd()) or not (file := Path(req.filepath)).is_file():
            res = ApiFetchContentsResponseError(status='fileNotFound')
            return  ApiFetchContentsResponse(res=res)

        res = ApiFetchContentsResponseSuccess(status='ok', contents=file.read_text())
        return ApiFetchContentsResponse(res=res)


    def _create_reload(self, req: ApiCreateReloadRequest):

        if self.active_reload_id is not None:
            return  ApiCreateReloadResponseError(status='alreadyReloading')

        filepath = (Path.cwd() / req.filepath).resolve()
        if not filepath.is_relative_to(Path.cwd()) or (code_file := self.registry.get(str(filepath))) is None:
            return  ApiCreateReloadResponseError(status='fileNotFound')

        Path(req.filepath).write_text(req.contents)
        activity = EventSource(save_history=True) # TODO: Generic EventSource[ApiGetReloadEventSourceMessage]
        code_file.activity = activity

        thread = create_thread(self.run_reload, code_file)
        reload_id = str(uuid4()) if req.reloadId is None else req.reloadId
        self.reload_runs[reload_id] = ReloadRun(activity, thread)
        self.active_reload_id = reload_id
        thread.start()

        return ApiCreateReloadResponseSuccess(status='created', reloadId=reload_id)


    def create_reload(self, req: ApiCreateReloadRequest) -> ApiCreateReloadResponse:
        """
        POST /create-reload
        """

        with self.create_lock:
            res = self._create_reload(req)

        return ApiCreateReloadResponse(res=res)


    def get_reload(self, req: ApiGetReloadRequest):
        """
        POST /get-reload
        """

        reload_id = req.reloadId
        if (run := self.reload_runs.get(reload_id, None)) is None:
            raise HTTPException(404, f"{reload_id=} not found")

        queue = Queue()
        run.activity.register(queue.put, apply_history=True)

        def activity_stream(queue: Queue):
            while (item := queue.get()) is not None:
                if isinstance(item, ApiGetReloadEventSourceData):
                    yield item
                elif isinstance(item, CodeFileOperation):
                    if (op := serialize_code_operation(item)) is not None:
                        yield ApiGetReloadEventSourceData(data=op)

        def event_source_stream():
            for data in activity_stream(queue):
                yield data.model_dump_json()

        return EventSourceResponse(event_source_stream())


    def run_reload(self, code_file: CodeFile):
        updated = False
        try:
            self.prerun()
            code_file.refresh()
            updated = self.postrun()
        except Exception as exc:
            tb = format_traceback(exc)
            op = ReloadOperationError(kind='error', traceback=tb)
            data = ApiGetReloadEventSourceData(data=op)
            code_file.activity.emit(data)
        op = ReloadOperationUI(kind='ui', updated=updated)
        data = ApiGetReloadEventSourceData(data=op)
        code_file.activity.emit(data)
        code_file.activity.emit(None)
        self.active_reload_id = None


    def run(self, port: int):
        app = FastAPI()
        app.include_router(self.router)
        server = Server(Config(app, host='0.0.0.0', port=port, log_level='warning'))
        server_thread = create_thread(server.run)
        server_thread.start()
        self.stop_event.wait()
        server.should_exit = True


def serialize_code_operation(cf_operation: CodeFileOperation):
    assert isinstance(defn := cf_operation.defn, (LineDefinition, GroupDefinition))
    region = serialize_extent(defn.stashed)
    if isinstance(cf_operation, ExceptionOperation):
        if (exc := cf_operation.exc) is None: # pragma: no cover
            exc = Exception("Unable to retrieve reload exception")
        tb = format_traceback(exc)
        return ReloadOperationException(kind='exception', region=region, traceback=tb)
    if isinstance(defn, GroupDefinition):
        otype = get_object_type(defn)
        oname = defn.dotpath()
        if isinstance(cf_operation, AddOperation):
            kind = 'add'
        elif isinstance(cf_operation, UpdateOperation):
            if not isinstance(defn, FunctionDefinition):
                return None
            kind = 'update'
        else:
            kind = 'delete'
        return ReloadOperationObject(kind=kind, region=region, objectType=otype, objectName=oname)
    if isinstance(defn, LineDefinition):
        if isinstance(cf_operation, DeleteOperation):
            return None
        return ReloadOperationRun(kind='run', region=region, codeLines=defn.text)
    assert_type(defn, Never) # pragma: no cover


def get_object_type(defn: GroupDefinition):
    if isinstance(defn, ClassDefinition):
        return 'class'
    if isinstance(defn, ModuleCode):
        return 'module'
    if isinstance(defn, FunctionDefinition):
        return 'function'
    return 'unknown' # pragma: no cover


def serialize_extent(extent: Extent):
    return ReloadRegion(
        startLine=extent.lineno,
        startCol=extent.col_offset,
        endLine=extent.end_lineno,
        endCol=extent.end_col_offset,
    )


def format_traceback(exc: Exception):
    traces = traceback.format_exception(type(exc), exc, exc.__traceback__)
    return "".join(traces)
