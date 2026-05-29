"""
CopyFromS3 — read one S3 object directly into a Pandas DataFrame.

No intermediate local file: the S3 ``StreamingBody`` is read fully into a
``BytesIO`` buffer and handed to ``CopyFromBase._parse()`` via
``_fetch_to_bytes()``.

Usage example:

.. code-block:: yaml

    CopyFromS3:
      credentials:
        use_credentials: false
        region_name: us-east-2
      bucket: my-bucket
      source_dir: reports/2026-05/
      file:
        filename: timeblock.xlsx
      mime: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
      file_engine: openpyxl
      sheet_name: Sheet1
"""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from io import BytesIO
from typing import Optional

from botocore.exceptions import ClientError

from ..exceptions import ComponentError, FileError, FileNotFound
from ..interfaces.Boto3Client import Boto3Client
from ..interfaces.copy_from_base import CopyFromBase


class CopyFromS3(Boto3Client, CopyFromBase):
    """Read one file from an S3 bucket directly into a Pandas DataFrame.

    Inherits from ``Boto3Client`` (left) and ``CopyFromBase`` (right), matching
    the MRO of ``DownloadFromS3(Boto3Client, DownloadFromBase)``.

    Properties (in addition to CopyFromBase read options):

    .. table::
        :widths: auto

        +-----------------+-----+--------------------------------------------------------------+
        | credentials     | Yes | AWS credentials dict (use_credentials / region / key /       |
        |                 |     | secret).                                                     |
        +-----------------+-----+--------------------------------------------------------------+
        | bucket          | Yes | S3 bucket name.                                              |
        +-----------------+-----+--------------------------------------------------------------+
        | source_dir      | No  | Key prefix within the bucket (e.g. "reports/2026-05/").      |
        |                 |     | Trailing "/" is added automatically.                         |
        +-----------------+-----+--------------------------------------------------------------+
        | file            | No  | Dict with ``{filename: <name>}`` for explicit key.           |
        +-----------------+-----+--------------------------------------------------------------+
        | source          | No  | Alias for ``file``.                                          |
        +-----------------+-----+--------------------------------------------------------------+

    Note:
        Single-file only in v1. For multi-file ingestion use
        ``DownloadFromS3 + OpenWithPandas``.
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop=None,
        job: Optional[Callable] = None,
        stat: Optional[Callable] = None,
        **kwargs,
    ) -> None:
        """Initialise, forwarding kwargs through the MRO chain.

        Args:
            loop: Unused; accepted for API parity.
            job: Optional job callable.
            stat: Optional stat callable.
            **kwargs: All component configuration, including ``credentials``,
                      ``bucket``, ``source_dir``, ``file``, and all
                      CopyFromBase read options (``mime``, ``separator``, etc.).
        """
        self.url: Optional[str] = None
        self.folder = None
        self.rename: Optional[str] = None
        self.context = None
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """Prepare the component, applying variable substitution to source_dir.

        Args:
            **kwargs: Forwarded to super().start().

        Returns:
            ``True`` on success.
        """
        await super().start(**kwargs)
        # Apply mask_replacement to source_dir when it contains {…} placeholders,
        # mirroring the pattern used by DownloadFromS3.start (lines 99-103).
        if (
            hasattr(self, "source_dir")
            and self.source_dir
            and isinstance(self.source_dir, str)
            and "{" in self.source_dir
        ):
            self.source_dir = self.mask_replacement(self.source_dir)
        if getattr(self, "source_dir", None) and not self.source_dir.endswith("/"):
            self.source_dir = self.source_dir + "/"
        return True

    def _resolve_key(self) -> str:
        """Build the S3 object key from source_dir and the file spec.

        Returns:
            The full S3 key string (e.g. ``"reports/2026-05/data.csv"``).

        Raises:
            ComponentError: When no ``file`` / ``source`` dict with a
                ``filename`` key is provided, or when the filename appears to
                be a list or glob pattern (multi-file not supported in v1).
        """
        spec = getattr(self, "file", None) or getattr(self, "source", None)
        if not spec or not isinstance(spec, dict) or "filename" not in spec:
            raise ComponentError(
                "CopyFromS3: provide `file: { filename: <name> }` "
                "(single file only in v1). For multi-file ingestion use "
                "DownloadFromS3 + OpenWithPandas."
            )
        filename = spec["filename"]
        if isinstance(filename, list) or (
            isinstance(filename, str) and any(c in filename for c in ("*", "?", "["))
        ):
            raise ComponentError(
                "CopyFromS3: glob patterns and lists are not supported (single file only in v1). "
                "For multi-file ingestion use DownloadFromS3 + OpenWithPandas."
            )
        name = self.mask_replacement(filename) if "{" in str(filename) else filename
        prefix = getattr(self, "source_dir", "") or ""
        return f"{prefix}{name}"

    async def _fetch_to_bytes(self) -> BytesIO:
        """Fetch the S3 object and return it as a BytesIO buffer.

        Returns:
            A ``BytesIO`` buffer at position 0, ready for parsing.

        Raises:
            FileNotFound: When the S3 key does not exist.
            FileError: On other S3 API errors.
            ComponentError: On unexpected errors.
        """
        if not self._connection:
            await self.open(credentials=self.credentials)
        key = self._resolve_key()

        # Run both get_object() and StreamingBody.read() inside the same
        # thread so the event loop is never blocked—even for large objects
        # over slow connections.
        connection = self._connection
        bucket = self.bucket

        def _get_and_read() -> bytes:
            obj = connection.get_object(Bucket=bucket, Key=key)
            status_code = int(obj["ResponseMetadata"]["HTTPStatusCode"])
            if status_code != 200:
                raise FileNotFound(
                    f"CopyFromS3: key not found s3://{bucket}/{key}"
                )
            return obj["Body"].read()

        try:
            data = await asyncio.to_thread(_get_and_read)
        except FileNotFound:
            raise
        except ClientError as err:
            error_code = err.response.get("Error", {}).get("Code", "")
            if error_code in ("NoSuchKey", "404"):
                raise FileNotFound(
                    f"CopyFromS3: key not found s3://{self.bucket}/{key}"
                ) from err
            raise FileError(
                f"CopyFromS3: error fetching s3://{self.bucket}/{key}: {err}"
            ) from err
        buf = BytesIO(data)
        buf.seek(0)
        return buf

    async def close(self) -> None:
        """Close the S3 connection gracefully.

        Wraps ``Boto3Client.close()`` and suppresses errors so that cleanup
        does not mask the primary exception from ``run()``.
        """
        try:
            await super().close()
        except Exception:
            self._logger.warning("CopyFromS3: error during close()", exc_info=True)
