#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Session-local temp FILE FORMAT for the ``STAGE_FILE_READER`` / ``INFER_STAGE_FILE_SCHEMA``
TVF path.

``STAGE_FILE_READER`` takes a ``FILE_FORMAT`` by name; the FILE FORMAT is consumed by the
TVF (at compile) and the XP external scanner (at read) — **not** by the sandbox Spark
reader, which decodes from ``READER_OPTIONS``. So the format only needs the stage/scanner
concerns: the file *type* and ``COMPRESSION``. Decoding options (delimiters, mode,
timestamp formats, …) are intentionally omitted to avoid conflicting with the Spark
reader options (see plan Q4).

``COMPRESSION`` belongs on the format because the scanner splits files into byte chunks
*before* the sandbox sees them — a compressed stream cannot be decoded from an arbitrary
mid-file chunk, so the codec must be resolved at the scanner level. ``AUTO`` (the default)
detects the codec from the file extension, matching Spark's own read-side behavior.
"""

from snowflake import snowpark
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

_SF_FILE_TYPE = {"json": "JSON", "csv": "CSV"}


def _format_name(fmt: str, compression: str) -> str:
    """Deterministic temp-format name per (type, compression).

    ``AUTO`` keeps the base name (``SNOWPARK_CONNECT_NSS_JSON_FF``); an explicit codec gets
    its own object (``..._JSON_GZIP_FF``) so a cached ``AUTO`` format is never reused for a
    read that asked for a specific codec.
    """
    comp = compression.upper()
    suffix = "" if comp == "AUTO" else f"_{comp}"
    return f"SNOWPARK_CONNECT_NSS_{fmt.upper()}{suffix}_FF"


def ensure_nss_temp_file_format(
    session: snowpark.Session, fmt: str, compression: str = "AUTO"
) -> str:
    """Ensure a session-local temp FILE FORMAT for ``(fmt, compression)`` exists and return
    its name.

    The format is identical across reads with the same ``(type, compression)``, so it is
    created **once per session**: the name is cached on the session object and the
    ``CREATE`` (guarded by ``IF NOT EXISTS``) is issued only on first use, avoiding a DDL
    round-trip per read.

    Args:
        session: Active Snowpark session.
        fmt: ``"json"`` or ``"csv"``.
        compression: Snowflake ``COMPRESSION`` value (``AUTO`` by default; e.g. ``GZIP``,
            ``BZ2``, ``NONE``). ``AUTO`` detects the codec from the file extension.

    Returns:
        The temp FILE FORMAT name to pass as ``FILE_FORMAT``.
    """
    key = fmt.lower()
    sf_type = _SF_FILE_TYPE[key]
    comp = compression.upper()
    name = _format_name(key, comp)

    # The cache check-then-create below is not locked. Two concurrent requests on
    # the same session could both issue the CREATE for the same format name — benign,
    # since the DDL is guarded by ``IF NOT EXISTS`` (a race causes at most redundant,
    # never conflicting, DDL). A lock would add lifecycle concerns for no correctness
    # gain.
    created = getattr(session, "_nss_temp_file_formats", None)
    if created is None:
        created = set()
        session._nss_temp_file_formats = created
    if name in created:
        return name

    sql = (
        f"CREATE TEMP FILE FORMAT IF NOT EXISTS {name} "
        f"TYPE = {sf_type} COMPRESSION = {comp}"
    )
    # NSS read path: internal temp-FILE-FORMAT DDL. Keep the log, but keep the "NSS"
    # keyword out of the customer-visible message (reviewer request).
    logger.info(f"ensuring temp FILE FORMAT: {sql}")
    session.sql(sql).collect()
    created.add(name)
    return name
