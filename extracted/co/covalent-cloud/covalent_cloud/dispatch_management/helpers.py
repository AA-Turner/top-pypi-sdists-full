# Copyright 2023 Agnostiq Inc.


"""Module for Covalent Cloud dispatching and related functionalities."""

import json
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, wait
from functools import wraps
from pathlib import Path
from typing import Callable, List, Union

import requests
from covalent._results_manager.result import Result
from covalent._serialize.result import merge_response_manifest, serialize_result, strip_local_uris
from covalent._shared_files import logger
from covalent._shared_files.defaults import parameter_prefix
from covalent._shared_files.schemas.asset import AssetSchema
from covalent._shared_files.schemas.result import ResultSchema
from covalent._workflow.lattice import Lattice
from rich.progress import BarColumn, MofNCompleteColumn, Progress, TaskID

from covalent_cloud.shared.schemas.volume import Volume

from ..shared.classes.api import APIClient, AssetAPIClient
from ..shared.classes.exceptions import (
    CovalentAPIKeyError,
    CovalentGenericAPIError,
    CovalentSDKError,
)
from ..shared.classes.settings import Settings, settings
from .dispatch_info import DispatchInfo

_dispatch_executor = ThreadPoolExecutor()

_VALID_EXECUTORS = {"cloud", "oci_cloud"}

dispatch_cache_dir = Path(settings.dispatch_cache_dir)
dispatch_cache_dir.mkdir(parents=True, exist_ok=True)

app_log = logger.app_log


class AssetUploadThreadFailure(CovalentSDKError):
    message: str = "One or more asset upload threads did not finish execution."
    code: str = "dispatch/asset-upload-thread/fail"

    def __init__(self) -> None:
        super().__init__(self.message, self.code)


class AssetUploadException(CovalentSDKError):
    message: str = "One or more asset upload raised exceptions."
    code: str = "dispatch/asset-upload/exception"

    def __init__(self, msg: str = ""):
        super().__init__(message=msg, code=self.code)


def validate_executors(lat: Lattice) -> bool:
    # Check lattice default executor and workflow_executor

    valid_lattice_executors = True
    valid_electron_executors = True

    if lat.metadata["executor"] not in _VALID_EXECUTORS:
        lat.set_metadata("executor", "cloud")
        lat.set_metadata("executor_data", {})

    if lat.metadata["workflow_executor"] not in _VALID_EXECUTORS:
        lat.set_metadata("workflow_executor", "cloud")
        lat.set_metadata("workflow_executor_data", {})

    tg = lat.transport_graph

    for i in tg._graph.nodes:
        name = tg.get_node_value(i, "name")

        if name.startswith(parameter_prefix):
            continue

        metadata = tg.get_node_value(i, "metadata")
        if metadata["executor"] not in _VALID_EXECUTORS:
            metadata["executor"] = "cloud"
            metadata["executor_data"] = {}
            tg.set_node_value(i, "metadata", metadata)

    return valid_lattice_executors and valid_electron_executors


def associate_volume_to_executors(lat: Lattice, volume: Volume) -> bool:

    lat.metadata["executor_data"]["attributes"]["volume_id"] = volume.id
    lat.metadata["workflow_executor_data"]["attributes"]["volume_id"] = volume.id

    tg = lat.transport_graph

    for i in tg._graph.nodes:
        name = tg.get_node_value(i, "name")

        if name.startswith(parameter_prefix):
            continue

        metadata = tg.get_node_value(i, "metadata")
        metadata["executor_data"]["attributes"]["volume_id"] = volume.id


# For multistage dispatches


def register(
    lattice: Lattice,
    volume: Union[Volume, None] = None,
    settings: Settings = settings,
) -> Callable:
    """
    Wrapping the dispatching functionality to allow input passing
    and server address specification.

    Afterwards, send the lattice to the dispatcher server and return
    the assigned dispatch id.

    Args:
        lattice: The lattice/workflow to send to the dispatcher server, its graph is built already.
        volume: [optional] Volume instance
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        Wrapper function which takes the inputs of the workflow as arguments
    """

    @wraps(lattice)
    def wrapper(*args, **kwargs) -> str:
        """
        Send the lattice to the dispatcher server and return
        the assigned dispatch id.

        Args:
            *args: The inputs of the workflow.
            **kwargs: The keyword arguments of the workflow.

        Returns:
            The dispatch id of the workflow.
        """

        try:

            if volume:
                associate_volume_to_executors(lattice, volume)

            with tempfile.TemporaryDirectory() as tmp_dir:
                if settings.redispatch.is_redispatch:
                    redispatch_id = settings.redispatch.id
                else:
                    redispatch_id = ""
                manifest = prepare_manifest(lattice, tmp_dir, redispatch_id)
                return_manifest = register_manifest(manifest, settings)
                new_dispatch_id = return_manifest.metadata.dispatch_id

                path = dispatch_cache_dir / f"{new_dispatch_id}"

                with open(path, "w") as f:
                    f.write(manifest.model_dump_json())

                upload_assets(manifest, settings)

                return new_dispatch_id

        except Exception as e:
            raise e

    return wrapper


def start(
    dispatch_id: str,
    settings: Settings = settings,
) -> str:
    """
    Wrapping the dispatching functionality to allow input passing
    and server address specification.

    Afterwards, send the lattice to the dispatcher server and return
    the assigned dispatch id.

    Args:
        orig_lattice: The lattice/workflow to send to the dispatcher server.
        dispatcher_addr: The address of the dispatcher server.  If None then then defaults to the address set in Covalent's config.

    Returns:
        str - The dispatch id of the workflow.
    """

    dispatcher_addr = settings.dispatcher_uri
    dispatcher_port = settings.dispatcher_port

    client = APIClient(host_uri=dispatcher_addr, settings=settings, port=dispatcher_port)
    endpoint = f"/api/v1/dispatchv2/start/{dispatch_id}"

    try:
        r = client.put(endpoint)
    except requests.exceptions.HTTPError as e:
        print(e.response.text, file=sys.stderr)
        raise e
    return r.content.decode("utf-8").strip().replace('"', "")


def prepare_manifest(lattice, storage_path, dispatch_id: str = "") -> ResultSchema:
    """Prepare a built-out lattice for submission"""

    result_object = Result(lattice, dispatch_id=dispatch_id)
    return serialize_result(result_object, storage_path)


def register_manifest(
    manifest: ResultSchema,
    settings: Settings = settings,
    parent_dispatch_id: Union[str, None] = None,
    push_assets: bool = True,
) -> ResultSchema:
    """Submits a manifest for registration.

    Returns:
        Dictionary representation of manifest with asset remote_uris filled in

    Side effect:
        If push_assets is False, the server will
        automatically pull the task assets from the submitted asset URIs.

    Raises:
        CovalentAPIKeyError: If the API key is invalid.

    """
    dispatcher_addr = settings.dispatcher_uri
    dispatcher_port = settings.dispatcher_port

    stripped = strip_local_uris(manifest) if push_assets else manifest
    client = APIClient(
        host_uri=dispatcher_addr,
        settings=settings,
        port=dispatcher_port,
        headers={"Content-Type": "application/json"},
    )
    endpoint = "/api/v2/lattices"

    if parent_dispatch_id:
        endpoint = f"{endpoint}/{parent_dispatch_id}"

    try:
        r = client.post(endpoint, request_options={"data": stripped.model_dump_json()})
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401 and e.response.json()["code"] == "auth/unauthorized":
            raise CovalentAPIKeyError(
                message="A valid API key is required to register a dispatch.",
                code=e.response.json()["code"],
            ) from e
        else:
            raise CovalentGenericAPIError(error=e)

    parsed_resp = ResultSchema.model_validate(r.json())

    return merge_response_manifest(manifest, parsed_resp)


def upload_assets(manifest: ResultSchema, settings: Settings = settings):
    assets = _extract_assets(manifest)
    _upload(assets, settings)


def _extract_assets(manifest: ResultSchema) -> List[AssetSchema]:
    # workflow-level assets
    dispatch_assets = manifest.assets
    assets = [asset for key, asset in dispatch_assets]
    lattice = manifest.lattice
    lattice_assets = lattice.assets
    assets.extend(asset for key, asset in lattice_assets)
    # Node assets
    tg = lattice.transport_graph
    nodes = tg.nodes
    for node in nodes:
        node_assets = node.assets
        assets.extend(asset for key, asset in node_assets)
    return assets


def _upload(assets: List[AssetSchema], settings: Settings = settings) -> None:
    """Upload assets to remote storage.

    Args:
        assets: List of AssetSchema objects to upload.

    Raises:
        RuntimeError: If any of the assets fail to upload.

    """
    total_assets = len(assets)
    _upload_futures = []

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>4.1f}%",
        MofNCompleteColumn(),
        disable=(os.environ.get("COVALENT_CLOUD_DISABLE_RICH") == "1"),
    ) as progress:
        task = progress.add_task("[green]Uploading assets...", total=total_assets)

        for asset in assets:

            if asset.size == 0:
                progress.advance(task, advance=1)
                progress.refresh()
                total_assets -= 1
                continue

            # Unset attributes won't be saved to the staging dir during
            # prepare_manifest.
            if not asset.uri:
                continue
            fut = _dispatch_executor.submit(
                _upload_asset, asset.uri, asset.remote_uri, task, progress, settings
            )
            _upload_futures.append(fut)

        done, _ = wait(_upload_futures)

        if len(done) < total_assets:
            raise AssetUploadThreadFailure

        _exceptions = []
        for fut in done:
            if ex := fut.exception(timeout=0.1):
                _exceptions.append(ex)

        if _exceptions:
            msg = f"Attempted and failed to upload {len(_exceptions)} out of {total_assets} due to raised exceptions."
            print(msg, file=sys.stderr)
            app_log.debug(_exceptions)
            raise AssetUploadException(msg)


def _upload_asset(
    local_uri: str,
    remote_uri: str,
    task: TaskID,
    progress: Progress,
    settings: Settings = settings,
) -> None:
    """Upload a single asset to remote storage with automatic retries.

    Args:
        local_uri: Local URI of the asset to upload.
        remote_uri: Remote URI to upload the asset to.
        task: Task ID of the progress bar task.
        progress: Progress bar object.

    Raises:
        requests.exceptions.HTTPError: If the upload fails.

    """
    scheme_prefix = "file://"
    if local_uri.startswith(scheme_prefix):
        local_path = local_uri[len(scheme_prefix) :]
    else:
        local_path = local_uri

    # Use AssetAPIClient for intelligent header management
    asset_client = AssetAPIClient(settings=settings)

    try:
        if os.path.getsize(local_path) == 0:
            # Handle empty files with Content-Length header
            r = asset_client.upload_asset(
                remote_uri, b"", additional_headers={"Content-Length": "0"}
            )
        else:
            with open(local_path, "rb") as f:
                data = f.read()
                r = asset_client.upload_asset(remote_uri, data)
    except Exception:
        raise

    if r.status_code == requests.codes.ok:
        progress.advance(task, advance=1)
        progress.refresh()


def fast_redispatch(
    dispatch_id: str,
    input_args: list,
    input_kwargs: dict,
    settings: Settings = settings,
) -> Callable:
    """
    Redispatches a Covalent workflow to the Covalent Cloud and returns the assigned dispatch ID.

    Args:
        dispatch_id: The dispatch ID of the workflow to re-dispatch.
        input_args: The positional arguments of the workflow.
        input_kwargs: The keyword arguments of the workflow.
        settings: The settings object to use. If None, the default settings will be used.

    Returns:
        The dispatch ID of the re-dispatched workflow.

    """

    dispatcher_addr = settings.dispatcher_uri
    dispatcher_port = settings.dispatcher_port

    client = APIClient(host_uri=dispatcher_addr, settings=settings, port=dispatcher_port)
    endpoint = f"/api/v2/dispatch/{dispatch_id}/redispatch"
    payload = {
        "api_key": settings.auth.api_key,  # TODO: remove this from payload after cloud-server is updated
        "dispatch_id": dispatch_id,
        "input_args": input_args,
        "input_kwargs": input_kwargs,
    }

    try:
        r = client.post(endpoint, request_options={"data": json.dumps(payload)})
    except requests.exceptions.HTTPError as e:
        print(e.response.text, file=sys.stderr)
        raise e
    return r.json()["dispatch_id"]


def track_redispatch(
    dispatch_id: str,
    original_dispatch_id: str,
    settings: Settings = settings,
) -> Callable:

    dispatcher_addr = settings.dispatcher_uri
    dispatcher_port = settings.dispatcher_port

    client = APIClient(host_uri=dispatcher_addr, settings=settings, port=dispatcher_port)
    endpoint = f"/api/v2/lattices/{dispatch_id}"

    payload = {
        "original_dispatch_id": original_dispatch_id,
    }

    try:
        r = client.put(endpoint, request_options={"data": json.dumps(payload)})
        r_json = r.json()
        update_response = {
            "dispatch_id": r_json["dispatch_id"],
            "original_dispatch_id": r_json["original_dispatch_id"],
        }
    except requests.exceptions.HTTPError as e:
        print(e.response.text, file=sys.stderr)
        raise e

    return update_response


def add_dispatch_info(
    dispatch_id: str,
    dispatch_info: DispatchInfo,
    settings: Settings = settings,
) -> Callable:

    dispatcher_addr = settings.dispatcher_uri
    dispatcher_port = settings.dispatcher_port

    client = APIClient(host_uri=dispatcher_addr, settings=settings, port=dispatcher_port)
    endpoint = f"/api/v2/lattices/{dispatch_id}/dispatch-info"

    try:
        client.post(endpoint, request_options={"json": dispatch_info.model_dump()})
    except requests.exceptions.HTTPError as e:
        print(e.response.text, file=sys.stderr)
        raise e
