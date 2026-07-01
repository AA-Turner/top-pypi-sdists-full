#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import importlib
import tempfile
import threading
import zipfile
from pathlib import Path

from snowflake.snowpark import Session

_java_initialized_ = threading.Event()
_java_initialized_lock = threading.Lock()
JAVA_UDFS_JAR_NAME = "java_udfs-1.0-SNAPSHOT.jar"


def upload_java_udf_jar(session: Session) -> None:
    global _java_initialized_
    if _java_initialized_.is_set():
        return

    with _java_initialized_lock:
        if not _java_initialized_.is_set():
            stage = session.get_session_stage()
            try:
                jar_path = importlib.resources.files(
                    "snowflake.snowpark_connect.resources"
                ).joinpath(JAVA_UDFS_JAR_NAME)
            except NotADirectoryError:
                # importlib.resource doesn't work in Stage Package method
                zip_path = Path(__file__).parent.parent.parent.parent
                jar_path_in_zip = (
                    f"snowflake/snowpark_connect/resources/{JAVA_UDFS_JAR_NAME}"
                )
                temp_dir = tempfile.gettempdir()

                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    if jar_path_in_zip not in zip_ref.namelist():
                        raise FileNotFoundError(
                            f"[snowpark_connect::invalid_input] {jar_path_in_zip} not found"
                        )
                    zip_ref.extract(jar_path_in_zip, temp_dir)

                jar_path = f"{temp_dir}/{jar_path_in_zip}"

            from snowflake.snowpark_connect.resources_initializer import RESOURCE_PATH

            upload_result = session.file.put(
                str(jar_path), f"{stage}/{RESOURCE_PATH}", overwrite=True
            )

            if upload_result[0].status != "UPLOADED":
                raise RuntimeError(
                    f"[snowpark_connect::internal_error] Failed to upload JAR with UDF definitions to stage: {upload_result[0].message}"
                )
            _java_initialized_.set()
