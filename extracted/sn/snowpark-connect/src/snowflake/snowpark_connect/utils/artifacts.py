#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import gzip
import hashlib
import os
import pathlib
import tempfile
import zipfile
import zlib
from dataclasses import dataclass

from snowflake import snowpark


def check_checksum(data: bytes, crc: int) -> bool:
    return zlib.crc32(data) != crc


def artifact_base_dir(session_id: str, spark_session_id: str) -> pathlib.Path:
    """Return the per-session temp directory that all artifacts must live under."""
    if os.name != "nt":
        return pathlib.Path(f"/tmp/sas-{session_id}/{spark_session_id}")
    return pathlib.Path(
        f"{tempfile.gettempdir()}\\sas-{session_id}\\{spark_session_id}"
    )


def assert_artifact_name_is_safe(
    session_id: str, spark_session_id: str, name: str
) -> None:
    """Guard against path traversal in the client-provided artifact ``name``.

    ``name`` arrives from the Spark client and is joined onto the per-session
    temp directory before files are written or deleted. ``../`` segments could
    otherwise let those operations escape the intended directory, so resolve the
    final path and require it to stay within the base directory.
    """
    base_dir = artifact_base_dir(session_id, spark_session_id)
    resolved = (base_dir / name).resolve()
    if not resolved.is_relative_to(base_dir.resolve()):
        raise ValueError(f"Artifact name contains path traversal: {name}")


def write_artifact(
    session: snowpark.Session,
    spark_session_id: str,
    name: str,
    data: bytes,
    overwrite: bool = False,
) -> str:
    # When using the notebook we have greatly limited disk space (around 1GB), so the provided artifacts cannot be too large.
    # When name starts with "cache/" it indicates that the provided artifact should be compressed to save space on the disk.
    if name.startswith("cache/"):
        filename = name + ".gz"
    elif name.startswith("archives/"):
        filename = name + ".archive"
    else:
        filename = name
    return write_temporary_artifact(
        session, spark_session_id, filename, data, overwrite
    )


def write_temporary_artifact(
    session: snowpark.Session,
    spark_session_id: str,
    name: str,
    data: bytes,
    overwrite: bool,
) -> str:
    # We write to /tmp (or windows equivalent) to keep the data in memory.
    # This is designed to work in TCM as well.
    # `name` is client-controlled, so reject path traversal before building the
    # destination path (defense-in-depth, SNOW-3649289).
    assert_artifact_name_is_safe(session.session_id, spark_session_id, name)
    if os.name != "nt":
        filepath = f"/tmp/sas-{session.session_id}/{spark_session_id}/{name}"
    else:
        filepath = f"{tempfile.gettempdir()}\\sas-{session.session_id}\\{spark_session_id}\\{name}"
    # The name comes to us as a path (e.g. cache/<name>), so we need to create
    # the parent directory if it doesn't exist to avoid errors during writing.
    pathlib.Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    write_mode = "wb" if overwrite else "ab"
    open_file = gzip.open if name.startswith("cache/") else open
    with open_file(filepath, write_mode) as in_memory_file:
        in_memory_file.write(data)
    return filepath


def write_class_files_to_stage(
    session: snowpark.Session, spark_session_id: str, files: dict[str, str]
) -> str:
    jar_name = f'{hashlib.sha256(str(files).encode("utf-8")).hexdigest()[:10]}.jar'
    if os.name != "nt":
        filepath = f"/tmp/sas-{session.session_id}/{spark_session_id}"
        jar_path = f"{filepath}/{jar_name}"
    else:
        filepath = (
            f"{tempfile.gettempdir()}\\sas-{session.session_id}\\{spark_session_id}"
        )
        jar_path = f"{filepath}\\{jar_name}"
    with zipfile.ZipFile(jar_path, "w", zipfile.ZIP_DEFLATED) as jar:
        for name, path in files.items():
            jar.write(path, name)
    stage_path = f"{session.get_session_stage()}/class_jars/"
    session.file.put(
        jar_path,
        stage_path,
        auto_compress=False,
        overwrite=True,
    )
    return stage_path + jar_name


@dataclass(frozen=True)
class ArtifactKey:
    filename: str
    file_hash: tuple[str, ...]

    def append_chunk_hash(self, chunk_data: bytes) -> "ArtifactKey":
        content_hash = hashlib.sha256(chunk_data).hexdigest()
        return ArtifactKey(
            filename=self.filename,
            file_hash=self.file_hash + (content_hash,),
        )


def generate_artifact_key(filename: str, data: bytes) -> ArtifactKey:
    content_hash = hashlib.sha256(data).hexdigest()
    return ArtifactKey(filename=filename, file_hash=(content_hash,))
