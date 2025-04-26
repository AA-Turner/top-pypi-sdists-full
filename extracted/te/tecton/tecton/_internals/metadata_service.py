import logging
import threading
from typing import Optional

from google.protobuf.empty_pb2 import Empty

import tecton
from tecton._internals.metadata_service_impl.auth_lib import InternalAuthProvider
from tecton._internals.metadata_service_impl.request_lib import InternalRequestProvider
from tecton._internals.metadata_service_impl.service_modules import GRPC_SERVICE_MODULES
from tecton_core import conf
from tecton_core.metadata_service_impl.base_stub import BaseStub
from tecton_core.metadata_service_impl.http_client import PureHTTPStub


_lock = threading.Lock()
_stub_instance: Optional[BaseStub] = None

logger = logging.getLogger(__name__)


def instance() -> BaseStub:
    if getattr(tecton, "__initializing__"):
        msg = "Tried to initialize MDS during module import"
        raise Exception(msg)
    global _stub_instance
    with _lock:
        if not _stub_instance:
            stub = PureHTTPStub(InternalRequestProvider(InternalAuthProvider()), GRPC_SERVICE_MODULES)
            conf._init_metadata_server_config(stub.GetConfigs(Empty()))

            # Only set the global at the end. Otherwise if GetConfigs() fails, we won't try to initialize the configs
            # again if the user retries
            _stub_instance = stub
        return _stub_instance


def close_instance():
    global _stub_instance
    with _lock:
        if _stub_instance:
            _stub_instance.close()
            _stub_instance = None
