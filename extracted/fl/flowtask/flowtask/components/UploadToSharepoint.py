import os
from collections.abc import Callable
import asyncio
import logging
from pathlib import Path
from ..exceptions import (
    FileError,
    ConfigError
)
from .UploadTo import UploadToBase
from ..interfaces.Sharepoint import SharepointClient


class UploadToSharepoint(SharepointClient, UploadToBase):
    """
    UploadToSharepoint

        Overview

            The UploadToSharepoint class is a component for uploading files or entire directories to a SharePoint site.
            It supports various configuration options for selecting files by name, extension, or pattern, and includes
            functionality for recursive directory searches.

        :widths: auto

            | credentials    |   Yes    | A dictionary with SharePoint credentials: `username`, `password`,         |
            |                |          | `tenant`, and `site`.                                                     |
            | source         |   Yes    | A dictionary specifying the source directory, filename, and/or file       |
            |                |          | extension for selecting files to upload.                                  |
            | destination    |   Yes    | A dictionary defining the SharePoint destination directory.               |
            | whole_dir      |   No     | Boolean indicating if the entire source directory should be uploaded.     |
            | recursive      |   No     | Boolean specifying whether to search recursively within directories.      |

        Returns

            This component uploads files to a specified SharePoint directory and returns the upload result status.
            It logs the upload activity and records metrics for the number of files uploaded. If no files are found
            or the configuration is incomplete, it raises an error. The upload can handle both individual files and
            entire folders, depending on configuration.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          UploadToSharepoint:
          credentials:
          username: sharepoint_username
          password: sharepoint_password
          tenant: symbits
          site: trocstorage
          destination:
          directory: Shared Documents/Optimum Sales Files
          masks:
          '{today}':
          - today
          - mask: '%Y%m%d%H%M%S'
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
        self.mdate = None
        self.local_name = None
        self.filename: str = ""
        self.whole_dir: bool = False
        self.preserve = True
        self.ContentType: str = "binary/octet-stream"
        self.recursive: bool = kwargs.get('recursive', False)
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        self.define_host = None

    async def start(self, **kwargs):
        """start Method."""
        await super(UploadToSharepoint, self).start(**kwargs)
        if hasattr(self, "source"):
            self.source_dir = self.source.get('directory')
            if isinstance(self.source_dir, str):
                self.source_dir = Path(self.source_dir).resolve()
            self.filename = self.source.get("filename", None)
            self.whole_dir = (
                self.source["whole_dir"] if "whole_dir" in self.source else False
            )
            if self.whole_dir is True:
                # if whole dir, is all files in source directory
                logging.debug(
                    f"Uploading all files on directory {self.source_dir}"
                )
                p = self.source_dir.glob("**/*")
                self._filenames = [
                    x for x in p if x.is_file()
                ]
            else:
                if "filename" in self.source:
                    filename = self.source_dir.joinpath(self.source["filename"])
                    if filename.is_dir():
                        p = self.source_dir.glob(self.source["filename"])
                        self._filenames = [
                            x for x in p if x.is_file()
                        ]
                    else:
                        self._filenames = [filename]
                elif 'extension' in self.source:
                    extension = self.source["extension"]
                    pattern = self.source.get("pattern", None)
                    if pattern:
                        # TODO: fix recursive problem from Glob
                        if self.recursive is True:
                            p = self.source_dir.rglob(f"**/*{pattern}*{extension}")
                        else:
                            p = self.source_dir.glob(f"*{pattern}*{extension}")
                    else:
                        if self.recursive is True:
                            p = self.source_dir.rglob(f"**/*{extension}")
                        else:
                            p = self.source_dir.glob(f"*{extension}")
                    self._filenames = [
                        x for x in p if x.is_file()
                    ]
                else:
                    raise ConfigError(
                        "UploadToSharepoint: No filename or extension in source"
                    )
        if hasattr(self, "destination"):
            # Destination in Sharepoint:
            self._destination = []
            self.directory = self.destination.get("directory", "Shared Documents")
            self.directory = self.mask_replacement(self.directory)
            if not self.directory.endswith("/"):
                self.directory = str(self.directory) + "/"
            # Handle destination filename for renaming
            self.filename = self.destination.get('filename')
            if isinstance(self.filename, str):
                self.filename = self.mask_replacement(self.filename)
                self._destination.append(
                    self.filename
                )
            elif isinstance(self.filename, list):
                for fn in self.filename:
                    fn = self.mask_replacement(fn)
                    self._destination.append(fn)
            if self.filename and len(self._filenames) != len(self._destination):
                raise ConfigError(
                    "UploadToSharepoint: Number of source files and destination filenames do not match"
                )
        else:
            if self.previous and self.input:
                self._filenames = self.input
            if hasattr(self, "file"):
                filenames = []
                for f in self._filenames:
                    p = self.source_dir.glob(f)
                    fp = [x for x in p if x.is_file()]
                    filenames = filenames + fp
                self._filenames = filenames
            elif 'extension' in self.source:
                extension = self.source["extension"]
                pattern = self.source.get("pattern", None)
                # check if files in self._filenames ends with extension
                filenames = []
                for f in self._filenames:
                    if f.suffix == extension:
                        # check if pattern is in the filename
                        if pattern:
                            if pattern in f.name:
                                filenames.append(f)
                            continue
                        else:
                            filenames.append(f)
                self._filenames = filenames
        return self

    async def close(self):
        pass

    async def run(self):
        """Upload a File to Sharepoint"""
        self._result = None
        async with self.connection():
            await self.verify_sharepoint_access()
            if not self.context:
                self.context = self.get_context(self.url)
        if not self._filenames:
            raise FileError("No files to upload")
        if self.whole_dir is True:
            # Using Upload entire Folder:
            self._result = await self.upload_folder(
                local_folder=self.source_dir,
                destination=self.directory
            )
        else:
            self._result = await self.upload_files(
                filenames=self._filenames,
                destination=self.directory,
                destination_filenames=self._destination if self._destination else None
            )
        self.add_metric("SHAREPOINT_UPLOADED", self._result)
        return self._result
