# ruff: noqa: E402
# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# lance dataset distributed transform job checkpointing + UDF utils

import base64
import fcntl
import json
import logging
import os
import site
import tempfile
import threading
import warnings
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Suppress lance fork-safety warning - Geneva uses Ray which handles this properly
warnings.filterwarnings("ignore", message=".*lance is not fork-safe.*")
warnings.filterwarnings("ignore", message=".*lancedb fork support is experimental.*")

_LOG = logging.getLogger(__name__)

_extract_lock = threading.Lock()

DEFAULT_UPLOAD_DIR = "_geneva_uploads"


def _download_and_extract(args: dict) -> None:
    src_path, download_path, output_dir = (
        args["src_path"],
        args["download_path"],
        args["output_dir"],
    )
    namespace_info = args.get("namespace")

    parts = src_path.rsplit(f"/{DEFAULT_UPLOAD_DIR}/", 1)
    if len(parts) != 2:
        raise RuntimeError(
            "Workspace downloads require a _geneva_uploads path so they can use "
            "LanceFileSession."
        )

    table_base_path = parts[0]
    remote_filename = parts[1]
    remote_path = f"{DEFAULT_UPLOAD_DIR}/{remote_filename}"

    try:
        from lance.file import LanceFileSession
    except ImportError as e:
        raise RuntimeError(
            "could not import lance. pylance must be provided explicitly in the "
            "manifest via `pip=...`"
        ) from e

    session_kwargs = {}
    if namespace_info is not None:
        try:
            from lance_namespace import connect as namespace_connect
        except ImportError as e:
            raise RuntimeError(
                "could not import lance_namespace. lance_namespace must be provided "
                "explicitly in the manifest via `pip=...`"
            ) from e

        namespace_properties = dict(namespace_info["properties"])
        worker_uri = namespace_properties.pop("worker_uri", None)
        if worker_uri:
            namespace_properties["uri"] = worker_uri

        from geneva._namespace_client import with_geneva_user_agent

        namespace_properties = with_geneva_user_agent(
            namespace_info["impl"], namespace_properties
        )
        session_kwargs["namespace_client"] = namespace_connect(
            namespace_info["impl"],
            namespace_properties,
        )
        session_kwargs["table_id"] = namespace_info["table_id"]

    session = LanceFileSession(table_base_path, **session_kwargs)
    session.download_file(remote_path, download_path)

    with (
        zipfile.ZipFile(download_path) as z,
        _extract_lock,  # ensure only one thread extracts at a time
    ):
        z.extractall(output_dir)
        _LOG.info("extracted workspace to %s", output_dir)


# MAGIC: if GENEVA_ZIPS is set, we will extract the zips and add them as site-packages
# this is how we acheive "import geneva" == importing workspace from client
#
# NOTE: think of this like booting up a computer. At this point we do not have any
# dependencies installed, so this logic needs to have minimal dependency surface.
# We avoid importing anything from geneva and do everything in the stdlib
if "GENEVA_ZIPS" in os.environ:
    import fcntl

    with (
        open("/tmp/.geneva_zip_setup", "w") as file,  # noqa: S108
        ThreadPoolExecutor(max_workers=8) as executor,
    ):
        # use fcntl to lock the file so we don't have multiple processes
        # trying to extract at the same time and blow up the disk space
        fcntl.lockf(file, fcntl.LOCK_EX)

        payload = json.loads(base64.b64decode(os.environ["GENEVA_ZIPS"]))
        zips = payload.get("zips", [])
        namespace_info = payload.get("namespace")

        for parts in zips:
            if not len(parts):
                # got an empty list, skip
                continue

            _LOG.info("Setting up geneva workspace from zips %s", parts)
            file_name = parts[0].split("/")[-1]
            name = file_name.split(".")[0]
            output_dir = Path(tempfile.gettempdir()) / name
            if output_dir.exists():
                _LOG.info("workspace already extracted to %s", output_dir)
            else:
                # force collect to surface errors
                list(
                    executor.map(
                        _download_and_extract,
                        (
                            {
                                "src_path": z,
                                "download_path": Path(tempfile.gettempdir())
                                / z.split("/")[-1],
                                "output_dir": output_dir,
                                "namespace": namespace_info,
                            }
                            for z in parts
                        ),
                    )
                )

            site.addsitedir(output_dir.as_posix())
            _LOG.info("added %s to sys.path", output_dir)

        fcntl.lockf(file, fcntl.LOCK_UN)


from geneva import telemetry
from geneva._context import get_current_context
from geneva.apply import CheckpointingApplier, ReadTask, ScanTask
from geneva.checkpoint import (
    CheckpointStore,
    InMemoryCheckpointStore,
)
from geneva.db import NativeConnection, RemoteConnection, connect
from geneva.debug.error_store import (
    Fail,
    Retry,
    Skip,
    SkipThresholdExceededError,
    fail_fast,
    retry_all,
    retry_transient,
    skip_on_error,
)
from geneva.errors import (
    FatalWorkerCrashError,
    FatalWorkerError,
    FatalWorkerExitError,
    FatalWorkerOOMError,
    FatalWorkerTransientError,
)
from geneva.jobs.remote import RemoteJob
from geneva.jobs.types import (
    BackfillJobResult,
    Job,
    JobResult,
    RefreshJobResult,
)
from geneva.table import NativeTable
from geneva.transformer import (
    UDTF,
    Chunker,
    Columns,
    batch_udtf,
    chunker,
    udf,
    udtf,
)

# Ray worker bootstrap (set by geneva.runners.ray._mgr, like GENEVA_ZIPS):
# init telemetry before the worker's first I/O. Never raises.
if os.environ.get(telemetry.TELEMETRY_INIT_ON_IMPORT_ENV):
    telemetry.init()

__all__ = [
    "BackfillJobResult",
    "CheckpointingApplier",
    "CheckpointStore",
    "Columns",
    "connect",
    "Fail",
    "FatalWorkerCrashError",
    "FatalWorkerError",
    "FatalWorkerExitError",
    "FatalWorkerOOMError",
    "FatalWorkerTransientError",
    "fail_fast",
    "get_current_context",
    "InMemoryCheckpointStore",
    "Job",
    "JobResult",
    "NativeConnection",
    "NativeTable",
    "ReadTask",
    "RefreshJobResult",
    "RemoteConnection",
    "RemoteJob",
    "Retry",
    "retry_all",
    "retry_transient",
    "ScanTask",
    "Skip",
    "SkipThresholdExceededError",
    "skip_on_error",
    "batch_udtf",
    "chunker",
    "Chunker",
    "udf",
    "UDTF",
    "udtf",
]

version = "0.16.0"

__version__ = version
