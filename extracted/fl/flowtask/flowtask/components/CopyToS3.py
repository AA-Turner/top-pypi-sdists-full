"""
CopyToS3 — write a Pandas DataFrame directly to one S3 object.

No intermediate local file: the DataFrame is serialized into a ``BytesIO``
buffer by ``CopyToFileBase.run()`` and then handed to
``CopyToS3._put_from_bytes()`` which calls ``put_object(Body=...)``.

Usage example:

.. code-block:: yaml

    CopyToS3:
      credentials:
        use_credentials: false
        region_name: us-east-2
      bucket: my-bucket
      destination:
        directory: exports/2026-05/
        filename: report.parquet
      format: parquet
      compression: snappy
"""
from __future__ import annotations

import asyncio
from collections.abc import Callable
from io import BytesIO
from typing import Optional

from botocore.exceptions import ClientError

from ..exceptions import ComponentError, FileError
from ..interfaces.Boto3Client import Boto3Client
from ..interfaces.copy_to_file_base import CopyToFileBase

_FORMAT_CONTENT_TYPE: dict[str, str] = {
    "csv": "text/csv",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "parquet": "application/parquet",
    "json": "application/json",
}


class CopyToS3(Boto3Client, CopyToFileBase):
    """Write a DataFrame to a single S3 object in CSV / Excel / Parquet / JSON format.

    Inherits from ``Boto3Client`` (left) and ``CopyToFileBase`` (right), mirroring
    the MRO of ``UploadToS3(Boto3Client, UploadToBase)``.

    Properties (in addition to CopyToFileBase write options):

    .. table::
        :widths: auto

        +-------------------+-----+---------------------------------------------------------------+
        | credentials       | Yes | AWS credentials dict (use_credentials / region / key /        |
        |                   |     | secret).                                                      |
        +-------------------+-----+---------------------------------------------------------------+
        | bucket            | Yes | S3 bucket name.                                               |
        +-------------------+-----+---------------------------------------------------------------+
        | destination       | Yes | Dict with ``directory`` (prefix) and ``filename`` (object     |
        |                   |     | name). Both values accept ``{…}`` placeholders.               |
        +-------------------+-----+---------------------------------------------------------------+
        | format            | No  | Output format: ``csv`` (default), ``xlsx``, ``parquet``,      |
        |                   |     | ``json``.                                                     |
        +-------------------+-----+---------------------------------------------------------------+
        | ContentType       | No  | Override the MIME type sent to S3.                            |
        +-------------------+-----+---------------------------------------------------------------+

    Note:
        Single-file only in v1. For multi-file uploads use ``UploadToS3``.
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
                      ``bucket``, ``destination``, ``format``, ``ContentType``,
                      and all CopyToFileBase write options.
        """
        self.directory: str = ""
        self.filename: str = ""
        self._content_type: str = "application/octet-stream"
        # Stash any explicit ContentType override BEFORE super().__init__() runs
        # because Boto3Client.__init__ also pops this key and defaults to
        # "application/octet-stream".  We use a private name to avoid the clash.
        self._user_content_type: Optional[str] = kwargs.pop("ContentType", None)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """Prepare the component, resolving destination key and content type.

        Applies ``mask_replacement`` to ``destination.directory`` and
        ``destination.filename`` when they contain ``{…}`` placeholders.

        Args:
            **kwargs: Forwarded to super().start().

        Returns:
            ``True`` on success.

        Raises:
            ComponentError: When ``destination.filename`` is missing or is a list.
        """
        await super().start(**kwargs)

        dest = getattr(self, "destination", None) or {}

        # Resolve directory prefix
        directory = dest.get("directory", "") or ""
        if directory and "{" in directory:
            directory = self.mask_replacement(directory)
        if directory and not directory.endswith("/"):
            directory += "/"
        self.directory = directory

        # Resolve filename — single file only
        filename = dest.get("filename")
        if isinstance(filename, list):
            raise ComponentError(
                "CopyToS3: single-file only in v1. "
                "Use UploadToS3 for multi-file uploads."
            )
        if not filename:
            raise ComponentError(
                "CopyToS3: missing destination.filename. "
                "Provide `destination: { directory: <prefix>, filename: <name> }`."
            )
        if isinstance(filename, str) and "{" in filename:
            filename = self.mask_replacement(filename)
        self.filename = filename

        # Content-type: honour explicit override first, then derive from format
        self._content_type = self._user_content_type or _FORMAT_CONTENT_TYPE.get(
            self.format, "application/octet-stream"
        )
        return True

    async def _put_from_bytes(self, buf: BytesIO) -> None:
        """Upload the serialised DataFrame to S3 via ``put_object``.

        Args:
            buf: A ``BytesIO`` at position 0, ready for reading.

        Raises:
            FileError: On boto3 ``ClientError`` or when S3 returns a non-200
                HTTP status code.
        """
        if not self._connection:
            await self.open(credentials=self.credentials)
        key = f"{self.directory}{self.filename}"
        try:
            response = await asyncio.to_thread(
                self._connection.put_object,
                Bucket=self.bucket,
                Key=key,
                Body=buf.getvalue(),
                ContentType=self._content_type,
            )
        except ClientError as err:
            raise FileError(
                f"CopyToS3: put_object failed for s3://{self.bucket}/{key}: {err}"
            ) from err

        status = int(response["ResponseMetadata"]["HTTPStatusCode"])
        if status != 200:
            raise FileError(
                f"CopyToS3: put_object returned HTTP {status} "
                f"for s3://{self.bucket}/{key}: {response['ResponseMetadata']!s}"
            )

        self.add_metric("S3_UPLOADED", {self.filename: key})
        self._logger.info(
            "CopyToS3: uploaded s3://%s/%s",
            self.bucket,
            key,
        )

    async def close(self) -> None:
        """Close the S3 connection gracefully.

        Wraps ``Boto3Client.close()`` and suppresses errors so that cleanup
        does not mask the primary exception from ``run()``.
        """
        try:
            await super().close()
        except Exception:
            self._logger.warning("CopyToS3: error during close()", exc_info=True)
