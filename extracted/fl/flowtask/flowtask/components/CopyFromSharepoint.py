"""
CopyFromSharepoint — read one SharePoint file directly into a Pandas DataFrame.

Uses the existing ``SharepointClient`` interface (Microsoft Graph SDK) to
download the target file into a temporary directory, then delegates parsing
to ``CopyFromBase._parse()`` via the tempfile fallback path.  No permanent
local file is created; the base class deletes the tempfile unconditionally
after parsing.

Usage example:

.. code-block:: yaml

    CopyFromSharepoint:
      credentials:
        client_id: SHAREPOINT_APP_ID
        client_secret: SHAREPOINT_APP_SECRET
        tenant_id: SHAREPOINT_TENANT_ID
      tenant: symbits
      site: Navigator-Navigator-dev
      file:
        filename: Timeblock.xlsx
        directory: Stores
      mime: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
      file_engine: openpyxl
      sheet_name: Sheet1
"""
from __future__ import annotations

import shutil
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Optional

from ..exceptions import ComponentError, FileError, FileNotFound
from ..interfaces.Sharepoint import SharepointClient
from ..interfaces.copy_from_base import CopyFromBase


class CopyFromSharepoint(SharepointClient, CopyFromBase):
    """Read one file from Microsoft SharePoint directly into a Pandas DataFrame.

    Inherits from ``SharepointClient`` (left) and ``CopyFromBase`` (right),
    mirroring the inheritance order of
    ``DownloadFromSharepoint(SharepointClient, DownloadFromBase)``.

    The v1 implementation uses the tempfile fallback path:
    ``CopyFromBase.run()`` calls ``_fetch_to_tempfile()`` when
    ``_fetch_to_bytes()`` raises ``NotImplementedError`` (the default).

    Properties (in addition to CopyFromBase read options):

    .. table::
        :widths: auto

        +---------------+-----+-------------------------------------------------------+
        | credentials   | Yes | SharePoint credentials (app or user auth).            |
        +---------------+-----+-------------------------------------------------------+
        | tenant        | Yes | SharePoint tenant name (e.g. ``symbits``).            |
        +---------------+-----+-------------------------------------------------------+
        | site          | Yes | SharePoint site name (e.g. ``Navigator-Navigator-dev``|
        +---------------+-----+-------------------------------------------------------+
        | file          | Yes | Dict ``{ filename: <name>, directory: <path> }``      |
        |               |     | — single file only in v1.                             |
        +---------------+-----+-------------------------------------------------------+
        | mime          | Yes | MIME type of the file.                                |
        +---------------+-----+-------------------------------------------------------+

    Note:
        Single-file only in v1. For multi-file downloads use
        ``DownloadFromSharepoint``.
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
                      ``tenant``, ``site``, ``file``, and all CopyFromBase
                      read options (``mime``, ``separator``, etc.).
        """
        self.url: Optional[str] = None
        self.folder = None
        self.rename: Optional[str] = None
        self.context = None
        self._search_context: bool = False
        self._target_filename: Optional[str] = None
        self._target_directory: Optional[str] = None
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs) -> bool:
        """Prepare the component, resolving the single target file spec.

        Parses ``self.file`` exactly like ``DownloadFromSharepoint.start()``
        but enforces the v1 single-file constraint: lists and multi-file
        dicts raise ``ComponentError``.

        Args:
            **kwargs: Forwarded to super().start().

        Returns:
            ``True`` on success.

        Raises:
            ComponentError: When ``self.file`` is a list, missing ``filename``,
                or is not a dict.
        """
        await super().start(**kwargs)
        self._search_context = True

        spec = getattr(self, "file", None)
        if isinstance(spec, list):
            raise ComponentError(
                "CopyFromSharepoint: single file only in v1. "
                "Use DownloadFromSharepoint for multi-file downloads."
            )
        if not isinstance(spec, dict) or "filename" not in spec:
            raise ComponentError(
                "CopyFromSharepoint: provide "
                "`file: { filename: <name>, directory: <path> }` (single file only in v1)."
            )

        directory = spec.get("directory", "/") or "/"
        self._target_directory = self.mask_replacement(directory)
        filename = spec["filename"]
        self._target_filename = (
            self.mask_replacement(filename) if "{" in str(filename) else filename
        )

        # Populate _srcfiles so file_search() knows what to look for
        self._srcfiles = [
            {
                "filename": self._target_filename,
                "directory": self._target_directory,
            }
        ]
        return True

    async def _fetch_to_tempfile(self) -> Path:
        """Download the target file to a temporary directory and return its Path.

        Uses ``file_search()`` to resolve the item and ``download_found_files()``
        to write it to a uniquely-named temporary directory.  The base class
        deletes the file unconditionally after parsing — do NOT remove it here.

        Returns:
            Path to the downloaded file inside the temporary directory.

        Raises:
            FileNotFound: When the file is not found in SharePoint.
            FileError: On authentication or Graph API errors.
            ComponentError: When multiple files matched a single-file query.
        """
        async with self.connection():
            await self.verify_sharepoint_access()
            if not self.context:
                self.context = self.get_context(self.url)

            # Create a dedicated temp dir so download_found_files has a clean slate.
            tmpdir = Path(tempfile.mkdtemp(prefix="copyfrom-sharepoint-"))
            # SharepointClient.download_found_files writes to self.directory.
            self.directory = str(tmpdir)

            try:
                try:
                    found = await self.file_search()
                except (FileError, FileNotFound):
                    raise
                except Exception as err:
                    raise FileError(
                        f"CopyFromSharepoint: error searching for "
                        f"'{self._target_filename}' in '{self._target_directory}': {err}"
                    ) from err

                if not found:
                    raise FileNotFound(
                        f"CopyFromSharepoint: '{self._target_filename}' "
                        f"not found in '{self._target_directory}'"
                    )

                try:
                    await self.download_found_files(found)
                except (FileError, FileNotFound):
                    raise
                except Exception as err:
                    raise FileError(
                        f"CopyFromSharepoint: error downloading "
                        f"'{self._target_filename}': {err}"
                    ) from err

                candidates = [p for p in tmpdir.iterdir() if p.is_file()]
                if not candidates:
                    raise FileNotFound(
                        f"CopyFromSharepoint: '{self._target_filename}' "
                        f"not found in '{self._target_directory}' after download"
                    )
                if len(candidates) == 1:
                    return candidates[0]

                # More than one file: prefer an exact name match
                exact = [p for p in candidates if p.name == self._target_filename]
                if len(exact) == 1:
                    return exact[0]

                raise ComponentError(
                    f"CopyFromSharepoint: multiple files matched single-file query "
                    f"for '{self._target_filename}': {[p.name for p in candidates]}"
                )
            except Exception:
                shutil.rmtree(tmpdir, ignore_errors=True)
                raise

    async def close(self) -> None:
        """Close the SharePoint connection gracefully.

        Wraps ``SharepointClient.close()`` and suppresses errors so that
        cleanup does not mask the primary exception from ``run()``.
        """
        try:
            await super().close()
        except Exception:
            self._logger.warning(
                "CopyFromSharepoint: error during close()", exc_info=True
            )
