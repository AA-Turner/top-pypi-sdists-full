import asyncio
from collections.abc import Callable
from pathlib import Path
from navconfig.logging import logging
from ..exceptions import FileNotFound, FileError
from ..interfaces.download_from import DownloadFromBase
from ..interfaces.Sharepoint import SharepointClient
from ..utils import SafeDict


class DownloadFromSharepoint(SharepointClient, DownloadFromBase):
    """
    DownloadFromSharepoint.

    **Overview**

        This SharePoint component downloads files from Microsoft SharePoint using Microsoft Graph SDK

    **Properties** (inherited from DownloadFromBase and SharepointClient)

        :widths: auto

        | credentials        |   Yes    | Credentials to establish connection with SharePoint site:                        |
        |                    |          | - client_id, client_secret, tenant_id (for app authentication)                   |
        |                    |          | - username, password (for user authentication)                                   |
        | site               |   Yes    | The SharePoint site name.                                                       |
        | tenant             |   Yes    | The SharePoint tenant name.                                                     |
        | file               |   Yes    | File configuration with filename and directory                                   |
        | destination        |   Yes    | Local destination directory and optional filename                                |
        | create_destination |   No     | Boolean flag indicating whether to create the destination directory if it       |
        |                    |          | doesn't exist (default: True).                                                   |

    Save the downloaded files on the new destination.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromSharepoint:
          credentials:
          client_id: "SHAREPOINT_APP_ID"
          client_secret: "SHAREPOINT_APP_SECRET"
          tenant_id: "SHAREPOINT_TENANT_ID"
          tenant: symbits
          site: Navigator-Navigator-dev
          file:
          filename: "Timeblock-08222025.csv"
          directory: "Stores"
          destination:
          directory: "/home/ubuntu/test/downloads/"
          filename: "Downloaded-Timeblock.csv"
        ```
    """
    _version = "1.0.0"

    # dict of expected credentials
    _credentials: dict = {
        "client_id": str,
        "client_secret": str,
        "tenant_id": str,
        "username": str,
        "password": str,
        "tenant": str,
        "site": str
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.url: str = None
        self.folder = None
        self.rename: str = None
        self.context = None
        self._search_context: bool = False
        self._debug_structure: bool = kwargs.pop("debug_structure", False)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Call the start method from the base classes
        await super(DownloadFromSharepoint, self).start(**kwargs)
        self._started = True
        # In case of DownloadFromSharepoint, source is Sharepoint URL a Destination is local path:
        if hasattr(self, "file"):
            self._srcfiles = []
            self._search_context = True
            if isinstance(self.file, list):
                # is a list of files:
                for file in self.file:
                    self._srcfiles.append({
                        'filename': file,
                        'directory': '/'
                    })
            elif isinstance(self.file, dict):
                self.source_dir = self.mask_replacement(self.file.get('directory', '/'))
                if 'extension' in self.file or 'pattern' in self.file:
                    self._srcfiles.append(
                        {
                            "extension": self.file.get('extension', None),
                            "pattern": self.file.get('pattern', None),
                            "directory": self.source_dir,
                            "recursive": self.file.get("recursive", True)
                        }
                    )
                else:
                    filename = self.file.get('filename')
                    if not filename:
                        raise FileError(
                            "File 'filename' is required in DownloadFromSharepoint component"
                        )
                    self._srcfiles.append({
                        'filename': self.mask_replacement(filename),
                        'directory': self.source_dir
                    })
        elif hasattr(self, "source"):
            # using the destination filosophy.
            source_dir = self.source.get('directory', '/')
            self.source_dir = self.mask_replacement(source_dir)
            self._srcfiles = []
            filenames = self.source.get('filename')
            if isinstance(filenames, list):
                if filenames:
                    for filename in filenames:
                        self._srcfiles.append({
                            'filename': self.mask_replacement(filename),
                            'directory': self.source_dir
                        })
            elif isinstance(filenames, dict):
                self._srcfiles.append(filenames)
            else:
                self._srcfiles.append({
                    'filename': self.mask_replacement(filenames),
                    'directory': self.source_dir
                })
        if hasattr(self, "destination"):
            self._filenames = []
            _dir = self.destination.get('directory')
            _direc = _dir.format_map(SafeDict(**self._variables))
            _dir = self.mask_replacement(_direc)
            self.directory = Path(_dir)
            self.filename = self.destination.get('filename', None)
            if isinstance(self.filename, list):
                for fname in self.filename:
                    self._filenames.append(
                        self.mask_replacement(fname)
                    )
            else:
                if self.filename:
                    self._filenames.append(
                        self.mask_replacement(self.filename)
                    )
        return True

    async def close(self):
        pass

    async def run(self):
        async with self.connection():
            await self.verify_sharepoint_access()
            if self._debug_structure:
                await self.debug_root_structure()
            if not self.context:
                self.context = self.get_context(self.url)
            try:
                if self._search_context:  # search-like context
                    found = await self.file_search()
                else:
                    found = await self.file_lookup()
                if not found:
                    raise FileNotFound("No files found to download")
                self._result = await self.download_found_files(found)
                self.add_metric(
                    "SHAREPOINT_FILES",
                    self._result
                )
                return self._result
            except (FileError, FileNotFound):
                raise
            except Exception as err:
                logging.error(f"Error downloading File: {err}")
                raise FileError(
                    f"Error downloading File: {err}"
                ) from err
