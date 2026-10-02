# Copyright 2023 Agnostiq Inc.


"""Helpers for result fetching."""


from __future__ import annotations

import enum
import os
from pathlib import Path
from typing import Any, Optional

import requests
from covalent._results_manager.result import Result
from covalent._results_manager.results_manager import SDK_LAT_META_KEYS, SDK_NODE_META_KEYS
from covalent._results_manager.wait import EXTREME
from covalent._serialize.common import load_asset
from covalent._serialize.electron import ASSET_FILENAME_MAP as ELECTRON_ASSET_FILENAMES
from covalent._serialize.electron import ASSET_TYPES as ELECTRON_ASSET_TYPES
from covalent._serialize.lattice import ASSET_FILENAME_MAP as LATTICE_ASSET_FILENAMES
from covalent._serialize.lattice import ASSET_TYPES as LATTICE_ASSET_TYPES
from covalent._serialize.result import ASSET_FILENAME_MAP as RESULT_ASSET_FILENAMES
from covalent._serialize.result import ASSET_TYPES as RESULT_ASSET_TYPES
from covalent._serialize.result import deserialize_result
from covalent._shared_files import logger
from covalent._shared_files.exceptions import MissingLatticeRecordError
from covalent._shared_files.schemas.asset import AssetSchema
from covalent._shared_files.schemas.result import ResultSchema
from covalent._workflow.transport import TransportableObject
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ..shared.classes.api import AssetAPIClient, AuthConfigManager
from ..shared.classes.settings import Settings, settings

app_log = logger.app_log
log_stack_info = logger.log_stack_info


# Multi-part


class AssetScope(enum.Enum):
    RESULT = "result"
    LATTICE = "lattice"
    NODE = "node"


# Utility function to decode TransportableObjects
def _decode(value: Any):
    if isinstance(value, TransportableObject):
        return value.get_deserialized()
    else:
        return value


class FutureVar:
    """A class that represents a variable that is not yet available.

    List of private attributes: _dispatch_id, _task_id, _name
    List of public and immutable attributes: value
    """

    def __init__(
        self,
        result_manager: ResultManager,
        scope: AssetScope,
        name: str,
        dispatch_id: str,
        task_id: Optional[int],
    ):
        self._scope = scope
        self._dispatch_id = dispatch_id
        self._task_id = task_id
        self._name = name
        self._value = None
        self._result_manager = result_manager
        self._downloaded = False

        if self._scope == AssetScope.RESULT:
            size = self._result_manager._manifest["assets"][name]["size"]

        if self._scope == AssetScope.LATTICE:
            size = self._result_manager._manifest["lattice"]["assets"][name]["size"]

        if self._scope == AssetScope.NODE:
            node = self._result_manager._manifest["lattice"]["transport_graph"]["nodes"][task_id]
            size = node["assets"][name]["size"]

        self._size = size

    @property
    def value(self):
        return self._value

    @property
    def size(self):
        return self._size

    # TODO - save artifacts to local storage first instead of loading
    # them entirely in memory.
    def load(self) -> Any:
        """Query Covalent Cloud to retrieve and populate 'value' attribute.'"""

        if self._scope == AssetScope.RESULT:
            if not self._downloaded:
                self._result_manager.download_result_asset(self._name)
                self._downloaded = True
            self._value = _decode(self._result_manager.load_result_asset(self._name))

        if self._scope == AssetScope.LATTICE:
            if not self._downloaded:
                self._result_manager.download_lattice_asset(self._name)
                self._downloaded = True
            self._value = _decode(self._result_manager.load_lattice_asset(self._name))

        if self._scope == AssetScope.NODE:
            if not self._downloaded:
                self._result_manager.download_node_asset(self._task_id, self._name)
                self._downloaded = True
            self._value = _decode(self._result_manager.load_node_asset(self._task_id, self._name))

        return self._value

    def __str__(self) -> str:
        if self._downloaded:
            return str(self.value)
        else:
            return "<FutureVar>"

    # infinite recursion
    def __deepcopy__(self, memo):
        """Make a deep copy.

        Detaches the result_manager attribute to avoid infinite
        recursion.

        """
        cls = type(self)
        fv = cls.__new__(cls)
        fv.__init__(None, self._scope, self._name, self._dispatch_id, self._task_id)
        return fv


class FutureResult(Result):
    """A class that represents a dispatch result that is not yet available.

    List of private attributes: _dispatch_id, _root_dispatch_id
    List of public and immutable attributes: dispatch_name, start_time, end_time, status, lattice, result, inputs, error
    """

    @property
    def result(self) -> Any:
        return self._result

    @property
    def inputs(self) -> Any:
        return super().inputs

    @property
    def error(self) -> str:
        return self._error

    @staticmethod
    def _from_result_object(res: Result):
        fr = FutureResult(res.lattice)
        fr.__dict__ = res.__dict__
        return fr

    def __str__(self):
        """String representation of the result object"""

        show_result_str = f"""
Lattice Result
==============
status: {self._status}
result: {self.result}
inputs: {self.inputs}
error: {self.error}

start_time: {self.start_time}
end_time: {self.end_time}

dispatch_id: {self.dispatch_id}

Node Outputs
------------
"""
        node_outputs = self.get_all_node_outputs()
        for k, v in node_outputs.items():
            show_result_str += f"{k}: {v}\n"

        return show_result_str


def _get_result_export_from_dispatcher(
    dispatch_id: str,
    wait: bool = False,
    status_only: bool = False,
    settings: Settings = settings,
) -> ResultSchema:
    """
    Internal function to get the results of a dispatch from the server without checking if it is ready to read.

    Args:
        dispatch_id: The dispatch id of the result.
        wait: Controls how long the method waits for the server to return a result. If False, the method will not wait and will return the current status of the workflow. If True, the method will wait for the result to finish and keep retrying for sys.maxsize.
        status_only: If true, only returns result status, not the full result object, default is False.
        dispatcher_addr: Dispatcher server address, defaults to the address set in covalent.config.

    Returns:
        The result object from the server.

    Raises:
        MissingLatticeRecordError: If the result is not found.
    """

    dispatcher_addr = settings.dispatcher_uri
    dispatcher_port = settings.dispatcher_port

    dispatcher_uri = dispatcher_addr

    if dispatcher_port is not None:
        dispatcher_uri += f":{dispatcher_port}"

    retries = int(EXTREME) if wait else 5

    adapter = HTTPAdapter(max_retries=Retry(total=retries, backoff_factor=1))
    http = requests.Session()
    http.mount("http://", adapter)
    http.mount("https://", adapter)
    url = dispatcher_uri + "/api/v1/export/" + dispatch_id

    headers = AuthConfigManager.get_auth_request_headers(settings)

    response = http.get(
        url,
        params={"wait": bool(int(wait)), "status_only": status_only},
        headers=headers,
    )
    if response.status_code == 404:
        raise MissingLatticeRecordError
    response.raise_for_status()
    export = response.json()
    return export


# Functions for computing local URIs
def get_node_asset_path(results_dir: str, node_id: int, key: str):
    filename = ELECTRON_ASSET_FILENAMES[key]
    return results_dir + f"/node_{node_id}/{filename}"


def get_lattice_asset_path(results_dir: str, key: str):
    filename = LATTICE_ASSET_FILENAMES[key]
    return results_dir + f"/{filename}"


def get_result_asset_path(results_dir: str, key: str):
    filename = RESULT_ASSET_FILENAMES[key]
    return results_dir + f"/{filename}"


# Asset transfers


def download_asset(
    remote_uri: str, local_path: str, chunk_size: int = 1024 * 1024, settings: Settings = settings
):
    """Download asset with intelligent authentication handling.

    For S3 presigned URLs, no authentication headers are added.
    For proxy URLs (e.g., /api/v2/assets/), authentication headers are included.

    Args:
        remote_uri: Remote URI to download from
        local_path: Local path to save the downloaded file
        chunk_size: Size of chunks to download in bytes
        settings: The settings object to use.

    Returns:
        Local file URI or None if asset is missing (404)
    """
    # Use AssetAPIClient for intelligent header management
    asset_client = AssetAPIClient(settings=settings)
    r = asset_client.download_asset(remote_uri)

    # Missing objects correspond to `None` attributes
    if r.status_code == 404:
        return None

    r.raise_for_status()

    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=chunk_size):
            f.write(chunk)
    return f"file://{local_path}"


def _get_result_asset_uri(manifest: dict, key: str) -> str:
    return manifest["assets"][key]["remote_uri"]


def _download_result_asset(
    manifest: dict, results_dir: str, key: str, settings: Settings = settings
):
    remote_uri = manifest["assets"][key]["remote_uri"]
    local_path = get_result_asset_path(results_dir, key)
    manifest["assets"][key]["uri"] = download_asset(remote_uri, local_path, settings=settings)


def _get_lattice_asset_uri(manifest: dict, key: str) -> str:
    lattice_assets = manifest["lattice"]["assets"]
    return lattice_assets[key]["remote_uri"]


def _download_lattice_asset(
    manifest: dict, results_dir: str, key: str, settings: Settings = settings
):
    lattice_assets = manifest["lattice"]["assets"]
    remote_uri = lattice_assets[key]["remote_uri"]
    local_path = get_lattice_asset_path(results_dir, key)
    lattice_assets[key]["uri"] = download_asset(remote_uri, local_path, settings=settings)


def _get_node_asset_uri(manifest: dict, node_id: int, key: str):
    node = manifest["lattice"]["transport_graph"]["nodes"][node_id]
    node_assets = node["assets"]
    return node_assets[key]["remote_uri"]


def _download_node_asset(
    manifest: dict, results_dir: str, node_id: int, key: str, settings: Settings = settings
):
    node = manifest["lattice"]["transport_graph"]["nodes"][node_id]
    node_assets = node["assets"]
    remote_uri = node_assets[key]["remote_uri"]
    local_path = get_node_asset_path(results_dir, node_id, key)
    node_assets[key]["uri"] = download_asset(remote_uri, local_path, settings=settings)


def _load_result_asset(manifest: dict, key: str):
    asset_meta = AssetSchema(**manifest["assets"][key])
    return load_asset(asset_meta, RESULT_ASSET_TYPES[key])


def _load_lattice_asset(manifest: dict, key: str):
    asset_meta = AssetSchema(**manifest["lattice"]["assets"][key])
    return load_asset(asset_meta, LATTICE_ASSET_TYPES[key])


def _load_node_asset(manifest: dict, node_id: int, key: str):
    node = manifest["lattice"]["transport_graph"]["nodes"][node_id]
    asset_meta = AssetSchema(**node["assets"][key])
    return load_asset(asset_meta, ELECTRON_ASSET_TYPES[key])


class ResultManager:
    def __init__(self, manifest: ResultSchema, results_dir: str, settings: Settings = settings):
        self.result_object = deserialize_result(manifest)
        self._manifest = manifest.dict()
        self._results_dir = results_dir
        self._settings = settings

    def save(self, path: Optional[str] = None):
        if not path:
            path = os.path.join(self._results_dir, "manifest.json")
        with open(path, "w") as f:
            f.write(ResultSchema.parse_obj(self._manifest).json())

    @staticmethod
    def load(path: str, results_dir: str) -> "ResultManager":
        with open(path, "r") as f:
            manifest_json = f.read()

        return ResultManager(ResultSchema.parse_raw(manifest_json), results_dir)

    def _populate_result_object(self):
        dispatch_id = self._manifest["metadata"]["dispatch_id"]

        # result assets
        for key in RESULT_ASSET_TYPES:
            remote_uri = _get_result_asset_uri(self._manifest, key)
            fv = FutureVar(self, AssetScope.RESULT, key, dispatch_id, None)
            self.result_object.__dict__[f"_{key}"] = fv

        # lattice assets
        for key in LATTICE_ASSET_TYPES:
            remote_uri = _get_lattice_asset_uri(self._manifest, key)
            fv = FutureVar(self, AssetScope.LATTICE, key, dispatch_id, None)
            if key in SDK_LAT_META_KEYS:
                self.result_object.lattice.metadata[key] = fv
            else:
                self.result_object.lattice.__dict__[key] = fv

        # transport graph node assets
        tg = self.result_object.lattice.transport_graph
        for node_id in tg._graph.nodes:
            for key in ELECTRON_ASSET_TYPES:
                remote_uri = _get_node_asset_uri(self._manifest, node_id, key)
                fv = FutureVar(self, AssetScope.NODE, key, dispatch_id, node_id)
                if key in SDK_NODE_META_KEYS:
                    node_meta = tg.get_node_value(node_id, "metadata")
                    node_meta[key] = fv
                else:
                    tg.set_node_value(node_id, key, fv)

    def download_result_asset(self, key: str):
        _download_result_asset(self._manifest, self._results_dir, key, self._settings)

    def download_lattice_asset(self, key: str):
        _download_lattice_asset(self._manifest, self._results_dir, key, self._settings)

    def download_node_asset(self, node_id: int, key: str):
        _download_node_asset(self._manifest, self._results_dir, node_id, key, self._settings)

    def load_result_asset(self, key: str) -> Any:
        return _load_result_asset(self._manifest, key)

    def load_lattice_asset(self, key: str) -> Any:
        return _load_lattice_asset(self._manifest, key)

    def load_node_asset(self, node_id: int, key: str) -> Any:
        return _load_node_asset(self._manifest, node_id, key)

    @staticmethod
    def from_dispatch_id(
        dispatch_id: str,
        results_dir: str,
        wait: bool = False,
        settings: Settings = settings,
    ) -> "ResultManager":
        export = _get_result_export_from_dispatcher(
            dispatch_id,
            wait,
            status_only=False,
            settings=settings,
        )

        manifest = ResultSchema.parse_obj(export["result_export"])

        new_electron_schemas = []
        for electron_schema in manifest.lattice.transport_graph.nodes:
            new_electron_schemas.append(electron_schema)

        manifest.lattice.transport_graph.nodes = new_electron_schemas

        # sort the nodes
        manifest.lattice.transport_graph.nodes.sort(key=lambda x: x.id)

        rm = ResultManager(manifest, results_dir, settings)
        result_object = rm.result_object
        result_object._results_dir = results_dir
        Path(results_dir).mkdir(parents=True, exist_ok=True)

        # Create node subdirectories
        for node_id in result_object.lattice.transport_graph._graph.nodes:
            node_dir = results_dir + f"/node_{node_id}"
            Path(node_dir).mkdir(exist_ok=True)

        return rm


def get_result_manager(dispatch_id, results_dir=None, wait=False, settings=settings):
    if not results_dir:
        results_dir = settings.results_dir + f"/{dispatch_id}"
    return ResultManager.from_dispatch_id(dispatch_id, results_dir, wait, settings)


def _get_result_multistage(
    dispatch_id: str,
    wait: bool = False,
    settings: Settings = settings,
    status_only: bool = False,
) -> Result:
    """
    Get the results of a dispatch from a file.

    Args:
        dispatch_id: The dispatch id of the result.
        wait: Controls how long the method waits for the server to return a result. If False, the method will not wait and will return the current status of the workflow. If True, the method will wait for the result to finish and keep retrying for sys.maxsize.

    Returns:
        The result from the file.

    """

    try:
        if status_only:
            return _get_result_export_from_dispatcher(
                dispatch_id=dispatch_id,
                wait=wait,
                status_only=status_only,
                settings=settings,
            )
        else:
            rm = get_result_manager(dispatch_id, None, wait, settings)
            rm._populate_result_object()

    except MissingLatticeRecordError as ex:
        app_log.warning(
            f"Dispatch ID {dispatch_id} was not found in the database. Incorrect dispatch id."
        )

        raise ex

    return rm.result_object


def get_result(
    dispatch_id: str,
    wait: bool = False,
    settings: Settings = settings,
    status_only: bool = False,
) -> Result:

    if not dispatch_id:
        return None

    res = _get_result_multistage(
        dispatch_id=dispatch_id,
        wait=wait,
        settings=settings,
        status_only=status_only,
    )
    if status_only:
        return res
    else:
        result_object = res

    # Populate sublattice results
    tg = result_object.lattice.transport_graph
    for node_id in tg._graph.nodes:
        sub_dispatch_id = tg.get_node_value(node_id, "sub_dispatch_id")
        sub_result_object = get_result(sub_dispatch_id, wait, settings, status_only)
        tg.set_node_value(node_id, "sublattice_result", sub_result_object)

    fr = FutureResult._from_result_object(result_object)

    return fr
