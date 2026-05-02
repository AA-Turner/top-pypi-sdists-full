import os
import logging
import asyncio
from typing import List
from collections.abc import Callable
from pathlib import PosixPath, Path, PurePath
from zipfile import ZipFile, BadZipFile
from ..exceptions import FileError, ComponentError, FileNotFound
from .flow import FlowComponent
from ..interfaces.compress import CompressSupport


class Uncompress(CompressSupport, FlowComponent):
    """
    Uncompress

        Overview

            The Uncompress class is a component for decompressing files in various archive formats, including but not limited to:
            7z (.7z), ACE (.ace), ALZIP (.alz), AR (.a), ARC (.arc), ARJ (.arj), BZIP2 (.bz2), CAB (.cab), compress (.Z), 
            CPIO (.cpio), DEB (.deb), DMS (.dms), GZIP (.gz), LRZIP (.lrz), LZH (.lha, .lzh), LZIP (.lz), LZMA (.lzma), 
            LZOP (.lzo), RPM (.rpm), RAR (.rar), RZIP (.rz), TAR (.tar), XZ (.xz), ZIP (.zip, .jar), and ZOO (.zoo). 
            It extracts the specified compressed file into a target directory and can optionally delete the source file 
            upon successful extraction.

        :widths: auto

            | filename       |   Yes    | The path to the compressed file to be decompressed.                       |
            | directory      |   Yes    | The target directory where files will be extracted.                       |
            | delete_source  |   No     | Boolean indicating if the source file should be deleted post-extraction.  |
            | extract        |   No     | Dictionary specifying filenames to extract and/or output directory.       |
            | password       |   No     | Optional password for encrypted files in supported formats.               |

        Returns

            This component extracts files from the specified compressed archive into the designated directory and returns
            a list of paths to the extracted files. It tracks metrics for the output directory and compressed file name.
            If configured, the original compressed file is deleted after extraction. Errors related to file corruption 
            or extraction issues are logged and raised as exceptions.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Uncompress:
          filename: organizational_unit_ancestors_{yesterday}.zip
          masks:
          yesterday:
          - yesterday
          - mask: '%Y-%m-%d'
          directory: /home/ubuntu/symbits/polestar/files/organizational_unit_ancestors/
          extract:
          filenames:
          - OrganizationalUnitAncestors.csv
          directory: /home/ubuntu/symbits/polestar/files/organizational_unit_ancestors/
          delete_source: false
        ```
    """
    _version = "1.0.0"

    _namelist = []
    _directory = ""

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.filename: str = None
        self.directory: PurePath = None
        self._path: PurePath = None
        self._output: PurePath = None
        self._filenames: List = []
        self.delete_source: bool = False
        super(Uncompress, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if isinstance(self.directory, str):
            self.directory = PosixPath(self.directory).resolve()
            self._path = PosixPath(self.directory, self.filename)
        if self.filename is not None:
            if hasattr(self, "masks"):
                self.filename = self.mask_replacement(self.filename)
            self._path = PosixPath(self.directory, self.filename)
        elif self.previous:
            if isinstance(self.input, PosixPath):
                self.filename = self.input
            elif isinstance(self.input, list):
                self.filename = PosixPath(self.input[0])
            elif isinstance(self.input, str):
                self.filename = PosixPath(self.input)
            else:
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = PosixPath(filenames[0])
                    except IndexError as err:
                        raise FileError("File is empty or doesnt exists") from err
            self._variables["__FILEPATH__"] = self.filename
            self._variables["__FILENAME__"] = os.path.basename(self.filename)
            self._path = self.filename
        else:
            raise FileError("UnCompress: File is empty or doesn't exists")
        if hasattr(self, "extract"):
            for _, filename in enumerate(self.extract["filenames"]):
                filename = self.mask_replacement(filename)
                self._filenames.append(filename)
            if "directory" in self.extract:
                self._output = Path(self.extract["directory"]).resolve()
                # Create directory if not exists
                try:
                    self._output.mkdir(parents=True, exist_ok=True)
                except Exception as err:
                    logging.error(f"Error creating directory {self._output}: {err}")
                    raise ComponentError(
                        f"Error creating directory {self._output}: {err}"
                    ) from err
            else:
                # same directory:
                self._output = Path(self.directory)
        self.add_metric("OUTPUT_DIRECTORY", self._output)
        self.add_metric("ZIP_FILE", self.filename)
        return True

    async def close(self):
        pass

    async def run(self):
        # Check if File exists
        self._result = None
        if not self._path.exists() or not self._path.is_file():
            raise FileNotFound(
                f"Compressed File doesn't exists: {self._path}"
            )
        with ZipFile(self._path) as zfp:
            status = zfp.testzip()
            if not status:  # Si no hay status
                # If not exists namelist, extract all files
                members = self._filenames if self._filenames else None
                # If not exists password return None
                pwd = self.password if hasattr(self, "password") else None
                try:
                    zfp.extractall(path=self._output, members=members, pwd=pwd)
                    if self.delete_source is True:
                        self._path.unlink()
                except BadZipFile as err:
                    # The error raised for bad ZIP files.
                    raise ComponentError(f"Bad Zip File: {err}") from err
                except Exception as err:
                    # Undefined error
                    raise ComponentError(f"{self.__name__} ZIP Error: {err}") from err
                result = self._filenames if self._filenames else zfp.namelist()
                filenames = []
                for filename in result:
                    f = self._output.joinpath(filename)
                    filenames.append(f)
                self._result = filenames
            else:  # Si hay status devuelve el primer archivo corrupto
                raise ComponentError(f"Zip File {status} is corrupted")
        return self._result
