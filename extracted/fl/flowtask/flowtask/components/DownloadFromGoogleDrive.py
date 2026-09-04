import asyncio
from collections.abc import Callable
from pathlib import Path
from typing import Any, Dict, List, Optional
from ..exceptions import FileError, FileNotFound
from ..interfaces.GoogleDrive import GoogleDriveClient
from ..interfaces.download_from import DownloadFromBase
from ..utils import SafeDict


class DownloadFromGoogleDrive(GoogleDriveClient, DownloadFromBase):
    """
    DownloadFromGoogleDrive.

    **Overview**

        Downloads (or, for native Google Docs/Sheets/Slides/Drawings,
        exports) files from Google Drive using a service account. Supports
        lookup by Drive ``file_id``, exact ``filename``, or
        ``pattern``/``extension`` search scoped to a ``directory`` (folder
        path, resolved by segment — Drive has no literal paths). When no
        ``filename``/``pattern`` is given, matches every file directly under
        ``directory``; with ``recursive: true``, descends into subfolders
        too.

    **Properties** (inherited from ``DownloadFromBase`` and ``GoogleClient``)

        | Name          | Required | Summary                                                            |
        |---------------|----------|---------------------------------------------------------------------|
        | credentials   | No       | Service account credentials override (path, JSON string, or dict). |
        |               |          | Defaults to ``GOOGLE_CREDENTIALS_FILE`` when omitted.               |
        | file          | Yes*     | Search spec dict (or list of dicts): ``file_id`` \\| ``filename`` \\| |
        |               |          | ``pattern``/``extension`` + ``directory`` + ``recursive``.          |
        | source        | Yes*     | Alternate spelling of ``file`` (destination-style tasks).          |
        | destination   | Yes      | ``directory`` (required), optional ``filename``/``export_format``. |

        \\* Exactly one of ``file`` or ``source`` must be provided.

        Example:

        ```yaml
        DownloadFromGoogleDrive:
          file:
            file_id: "1t8W6lNVTH1Z0DDG0IHpCgAu7ALtHMJNQz8YpaVz2J1o"
          destination:
            directory: "/home/ubuntu/symbits/pharmabox/files/"
            filename: "MasterProductList.xlsx"
            export_format: "xlsx"
        ```

        ```yaml
        DownloadFromGoogleDrive:
          file:
            pattern: "*MPL*"
            extension: "xlsx"
            directory: "Pharmabox/Reports"
          destination:
            directory: "/home/ubuntu/symbits/pharmabox/files/"
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.export_format: Optional[str] = None
        self._srcfiles: List[Dict[str, Any]] = []
        self._filenames: List[str] = []
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    def processing_credentials(self):
        """No-op override.

        ``GoogleClient.__init__`` already fully resolves credentials into
        ``credentials_file``/``credentials_dict``/``credentials_str`` from
        the ``credentials`` constructor kwarg. There is no per-field
        env-var substitution step to run the way
        ``CredentialsInterface.processing_credentials()`` does for
        username/password-style dict credentials, so this is intentionally
        a no-op — it exists only so ``DownloadFromBase.start()`` (which
        calls ``self.processing_credentials()`` unconditionally) has
        something to call, since ``GoogleClient`` doesn't provide one.
        """
        return None

    async def start(self, **kwargs):
        await super(DownloadFromGoogleDrive, self).start(**kwargs)
        self._started = True

        self._srcfiles = []
        if hasattr(self, "file"):
            spec_source = self.file
        elif hasattr(self, "source"):
            spec_source = self.source
        else:
            raise FileError(
                "DownloadFromGoogleDrive: either 'file' or 'source' must be provided"
            )

        if isinstance(spec_source, list):
            for entry in spec_source:
                if isinstance(entry, dict):
                    self._srcfiles.append(dict(entry))
                else:
                    self._srcfiles.append({"filename": entry})
        elif isinstance(spec_source, dict):
            self._srcfiles.append(dict(spec_source))
        else:
            raise FileError(
                "DownloadFromGoogleDrive: 'file'/'source' must be a dict or a list of dicts"
            )

        self.export_format = None
        self._filenames = []
        if hasattr(self, "destination"):
            _dir = self.destination.get("directory", ".")
            _direc = _dir.format_map(SafeDict(**self._variables))
            _dir = self.mask_replacement(_direc)
            self.directory = Path(_dir)
            self.export_format = self.destination.get("export_format")

            filename = self.destination.get("filename")
            if isinstance(filename, list):
                self._filenames = [self.mask_replacement(f) for f in filename]
            elif filename:
                self._filenames = [self.mask_replacement(filename)]
        else:
            self.directory = Path(".")

        return True

    async def close(self):
        pass

    async def run(self):
        # GoogleClient never initializes self.credentials in __init__, so
        # get_service()'s lazy `if not self.credentials: self.connection()`
        # check would raise AttributeError on first use. Connect eagerly
        # here instead of relying on that lazy path.
        self.connection()

        found = await self.search_files(self._srcfiles)
        if not found:
            raise FileNotFound("No files found to download")

        self._result = await self.download_found_files(
            found, self.directory, self._filenames, self.export_format
        )
        self.add_metric("GOOGLEDRIVE_FILES", self._result)
        return self._result
