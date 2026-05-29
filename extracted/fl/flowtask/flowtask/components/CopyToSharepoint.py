"""
CopyToSharepoint — write a Pandas DataFrame directly to one SharePoint file.

Serializes the DataFrame to a temporary file (CSV / Excel / Parquet / JSON)
via ``CopyToFileBase.run()`` and then uploads it to SharePoint via the
existing ``SharepointClient.upload_files`` helper.  The temporary file is
deleted unconditionally by the base class after the upload completes or
fails.

Usage example:

.. code-block:: yaml

    CopyToSharepoint:
      credentials:
        client_id: SHAREPOINT_APP_ID
        client_secret: SHAREPOINT_APP_SECRET
        tenant_id: SHAREPOINT_TENANT_ID
      tenant: symbits
      site: Navigator-Navigator-dev
      destination:
        directory: Reports/2026-05/
        filename: monthly-report.xlsx
      format: xlsx
      sheet_name: Summary
"""
from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Optional

from ..exceptions import ComponentError, FileError
from ..interfaces.Sharepoint import SharepointClient
from ..interfaces.copy_to_file_base import CopyToFileBase


class CopyToSharepoint(SharepointClient, CopyToFileBase):
    """Upload a DataFrame to a single SharePoint file in CSV / Excel / Parquet / JSON format.

    Inherits from ``SharepointClient`` (left) and ``CopyToFileBase`` (right),
    mirroring the inheritance order of
    ``UploadToSharepoint(SharepointClient, UploadToBase)``.

    The v1 implementation uses the tempfile fallback path:
    ``CopyToFileBase.run()`` falls back to ``_put_from_tempfile()`` when
    ``_put_from_bytes()`` raises ``NotImplementedError`` (the default).

    Properties (in addition to CopyToFileBase write options):

    .. table::
        :widths: auto

        +------------------+-----+-------------------------------------------------------+
        | credentials      | Yes | SharePoint credentials (app or user auth).            |
        +------------------+-----+-------------------------------------------------------+
        | tenant           | Yes | SharePoint tenant name (e.g. ``symbits``).            |
        +------------------+-----+-------------------------------------------------------+
        | site             | Yes | SharePoint site name.                                 |
        +------------------+-----+-------------------------------------------------------+
        | destination      | Yes | Dict ``{ directory: <path>, filename: <name> }``      |
        |                  |     | — single file only in v1.                             |
        +------------------+-----+-------------------------------------------------------+
        | format           | No  | Output format: ``csv`` (default), ``xlsx``,           |
        |                  |     | ``parquet``, ``json``.                                |
        +------------------+-----+-------------------------------------------------------+

    Note:
        Single-file only in v1. For multi-file uploads use ``UploadToSharepoint``.
    """

    _version = "1.0.0"

    _credentials: dict = {
        "client_id": str,
        "client_secret": str,
        "tenant_id": str,
        "username": str,
        "password": str,
        "tenant": str,
        "site": str,
    }

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
                      ``tenant``, ``site``, ``destination``, ``format``,
                      and all CopyToFileBase write options.
        """
        self.url: Optional[str] = None
        self.context = None
        self.destination_dir: str = "Shared Documents/"
        self.destination_filename: Optional[str] = None
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """Prepare the component, resolving the destination path and filename.

        Args:
            **kwargs: Forwarded to super().start().

        Returns:
            ``True`` on success.

        Raises:
            ComponentError: When ``destination.filename`` is missing or a list.
        """
        await super().start(**kwargs)

        dest = getattr(self, "destination", None) or {}

        # Resolve directory prefix
        directory = dest.get("directory", "Shared Documents") or "Shared Documents"
        if "{" in directory:
            directory = self.mask_replacement(directory)
        if not directory.endswith("/"):
            directory += "/"
        self.destination_dir = directory

        # Resolve filename — single file only
        filename = dest.get("filename")
        if isinstance(filename, list):
            raise ComponentError(
                "CopyToSharepoint: single-file only in v1. "
                "Use UploadToSharepoint for multi-file uploads."
            )
        if not filename:
            raise ComponentError(
                "CopyToSharepoint: missing destination.filename. "
                "Provide `destination: { directory: <path>, filename: <name> }`."
            )
        if isinstance(filename, str) and "{" in filename:
            filename = self.mask_replacement(filename)
        self.destination_filename = filename
        return True

    async def _put_from_tempfile(self, path: Path) -> None:
        """Upload the serialised DataFrame tempfile to SharePoint.

        Called by ``CopyToFileBase.run()`` after writing the DataFrame to a
        temporary file.  The base class deletes the tempfile unconditionally
        after this method returns.

        Args:
            path: Path to the temporary file containing the serialised
                  DataFrame.

        Raises:
            FileError: When ``upload_files`` reports errors.
        """
        async with self.connection():
            await self.verify_sharepoint_access()
            if not self.context:
                self.context = self.get_context(self.url)
            result = await self.upload_files(
                filenames=[path],
                destination=self.destination_dir,
                destination_filenames=[self.destination_filename],
            )

        # Validate the result — upload_files may return a dict with an "errors" key
        if isinstance(result, dict) and result.get("errors"):
            raise FileError(
                f"CopyToSharepoint: upload errors for "
                f"'{self.destination_filename}' → '{self.destination_dir}': "
                f"{result['errors']}"
            )

        self.add_metric(
            "SHAREPOINT_UPLOADED",
            {self.destination_filename: self.destination_dir},
        )
        self._logger.info(
            "CopyToSharepoint: uploaded %s to %s",
            self.destination_filename,
            self.destination_dir,
        )

    async def close(self) -> None:
        """Close the SharePoint connection gracefully.

        Wraps ``SharepointClient.close()`` and suppresses errors so that
        cleanup does not mask the primary exception from ``run()``.
        """
        try:
            await super().close()
        except Exception:
            self._logger.warning(
                "CopyToSharepoint: error during close()", exc_info=True
            )
