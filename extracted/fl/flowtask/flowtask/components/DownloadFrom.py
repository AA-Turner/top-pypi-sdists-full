import asyncio
import random
import ssl
from abc import abstractmethod
from functools import partial
from typing import Dict, List
from collections.abc import Callable
from pathlib import Path, PurePath, PosixPath
from tqdm import tqdm
import aiohttp
from ..exceptions import ComponentError, FileNotFound
from ..utils.encoders import DefaultEncoder
from ..utils import SafeDict
from .flow import FlowComponent
from ..interfaces.dataframes import PandasDataframe
from ..interfaces.http import ua


class DownloadFromBase(PandasDataframe, FlowComponent):
    """
    DownloadFromBase

    Abstract base class for downloading files from various sources.

    Inherits from `FlowComponent` and `PandasDataframe` to provide common functionalities
    for component management and data handling.

    This class utilizes `aiohttp` for asynchronous HTTP requests and offers support
    for authentication, SSL connections, and basic file management.

    .. note::
    This class is intended to be subclassed for specific download implementations.

    :widths: auto

        | credentials          |    Yes   | Dictionary containing expected username and password for authentication             |
        |                      |          | (default: {"username": str, "password": str}).                                      |
        | no_host              |    No    | Boolean flag indicating whether to skip defining host and port (default: False).    |
        | overwrite            |    No    | Boolean flag indicating whether to overwrite existing files (default: True).        |
        | overwrite            |    No    | Boolean flag indicating whether to overwrite existing files (default: True).        |
        | create_destination   |    No    | Boolean flag indicating whether to create the destination directory                 |
        |                      |          | if it doesn't exist (default: True).                                               |
        | rename               |    No    | String defining a new filename for the downloaded file.                             |
        | file                 |   Yes    | Access the file download through a url, with the required user credentials and      |
        |                      |          | password                                                                            |
        | download             |   Yes    | File destination and directory                                                      |
        | source               |   Yes    | Origin of the file to download and location where the file is located.              |
        | destination          |   Yes    | Destination where the file will be save.                                            |
        | ssl                  |    No    | Boolean flag indicating whether to use SSL connection (default: False).             |
        | ssl_cafile           |    No    | Path to the CA certificate file for SSL verification.                               |
        | ssl_certs            |    No    | List of certificate chains for SSL verification.                                    |
        | host                 |    No    | Hostname for the download source (default: "localhost").                            |
        | port                 |    No    | Port number for the download source (default: 22).                                  |
        | timeout              |    No    | Timeout value in seconds for HTTP requests (default: 30).                           |
        | url                  |    No    | URL of the download source (populated within the class).                            |
        | headers              |   Yes    | Dictionary containing HTTP headers for the request.                                 |

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromBase:
          # attributes here
        ```
    """
    _version = "1.0.0"
    _credentials: dict = {"username": str, "password": str}

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.no_host: bool = kwargs.pop("no_host", False)
        self.accept: str = "text/plain"
        self.overwrite: bool = True
        self.create_destination: bool = kwargs.pop("create_destination", False)
        self.rename: str = None
        # source:
        self.source_file: str = None
        self.source_dir: str = None
        # destination:
        self.filename: str = None
        self._srcfiles: List = []
        self._filenames: Dict = {}
        self._connection: Callable = None
        self.ssl: bool = False
        self.ssl_cafile: str = None
        self.ssl_certs: list = []
        self.timeout: int = kwargs.pop("timeout", 30)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        if not hasattr(self, "url"):
            self.url: str = None
        if not hasattr(self, "headers"):
            self.headers = {}
        self._encoder = DefaultEncoder()
        self._valid_response_status: tuple = (200, 201, 202)
        # SSL Context:
        if self.ssl:
            # TODO: add CAFile and cert-chain
            self.ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS, cafile=self.ssl_cafile)
            self.ssl_ctx.minimum_version = ssl.TLSVersion.TLSv1_2
            self.ssl_ctx.options &= ~ssl.OP_NO_SSLv3
            self.ssl_ctx.verify_mode = ssl.CERT_NONE
            if self.ssl_certs:
                self.ssl_ctx.load_cert_chain(*self.ssl_certs)
        else:
            self.ssl_ctx = None

    def build_headers(self):
        self.headers = {
            "Accept": self.accept,
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": random.choice(ua),
            **self.headers,
        }

    async def start(self, **kwargs):
        """Start.

        Processing variables and credentials.
        """
        try:
            if getattr(self, 'define_host', None) is not None:
                self.define_host()
            self.processing_credentials()
        except Exception as err:
            self._logger.error(err)
            raise
        if hasattr(self, "directory") and self.directory:
            self.directory = Path(self.directory)
            try:
                if hasattr(self, "masks"):
                    p = self.mask_replacement(self.directory)
                else:
                    p = self.directory
                if not p.exists():
                    if self.create_destination is True:
                        try:
                            PosixPath(p).mkdir(parents=True, exist_ok=True)
                        except (Exception, OSError) as err:
                            raise ComponentError(
                                f"Error creating directory {self.directory}: {err}"
                            ) from err
                    else:
                        self._logger.error(
                            f"DownloadFrom: Path doesn't exists: {p}"
                        )
                        raise FileNotFound(
                            f"DownloadFrom: Path doesn't exists: {p}"
                        )
            except Exception as err:
                self._logger.error(err)
                raise ComponentError(f"{err!s}") from err
            self._logger.debug(f"Destination Directory: {self.directory}")
        if hasattr(self, "file"):
            if isinstance(self.file, list):
                # is a list of files:
                for file in self.file:
                    filename = file
                    if hasattr(self, "masks"):
                        filename = self.mask_replacement(file)
                    self._logger.debug(f"Filename > {filename}")
                    self._srcfiles.append(filename)
            else:
                try:
                    filename = self.process_pattern("file")
                    directory = self.file.get('directory', None)
                    if hasattr(self, "masks"):
                        if isinstance(filename, dict):
                            for key, value in filename.items():
                                filename[key] = self.mask_replacement(value)
                        elif isinstance(filename, str):
                            filename = self.mask_replacement(filename)
                    # path for file
                    self._logger.debug(
                        f"Filename > {filename}"
                    )
                    self.filename = filename
                    # for some exception, directory is on file:
                    if directory:
                        self.source_dir = directory
                        if hasattr(self, "masks"):
                            self.source_dir = self.mask_replacement(directory)
                    self._logger.debug(f"Source Directory: {self.source_dir}")
                    # IN CASE of DownloadFromSharepoint, filename is a dict
                    if 'extension' in self.file or 'pattern' in self.file:
                        self._srcfiles.append(
                            {
                                "extension": self.file.get('extension', None),
                                "pattern": self.file.get('pattern', None),
                                "filename": filename,
                                "directory": directory
                            }
                        )
                    else:
                        self._srcfiles.append(filename)
                except Exception as err:
                    raise ComponentError(f"{err!s}") from err
        elif hasattr(self, "source"):  # using the destination filosophy
            source_dir = self.source.get('directory', '/')
            if hasattr(self, "masks"):
                self.source_dir = self.mask_replacement(source_dir)
            else:
                self.source_dir = source_dir
            # filename:
            if "file" in self.source:
                self.source_file = self.process_pattern(
                    "file",
                    parent=self.source
                )
                self._srcfiles.append(self.source_file)
            else:
                filenames = self.source.get('filename')
                try:
                    if isinstance(filenames, list):
                        for file in filenames:
                            filename = self.mask_replacement(file)
                            self._srcfiles.append(
                                {
                                    "filename": file,
                                    "directory": self.source_dir
                                }
                            )
                    elif isinstance(filenames, dict):
                        self._srcfiles.append(filenames)
                    else:
                        self.source_file = {
                            "filename": self.mask_replacement(
                                filenames
                            ),
                            "directory": self.source_dir
                        }
                        self._srcfiles.append(self.source_file)
                except KeyError:
                    self.source_file = None
        if hasattr(self, "destination"):
            if "filename" in self.destination:
                # Rename the file to be downloaded
                self.filename = self.destination.get('filename', None)
            elif isinstance(self.filename, dict) and 'filename' in self.filename:
                self.filename = self.filename["filename"]
            else:
                # Preserving Filename from Source
                self.filename = None
            if self.filename:
                self._logger.debug(
                    f"Raw Destination Filename: {self.filename}\n"
                )
                if hasattr(self, "masks") or "{" in self.filename:
                    self.filename = self.mask_replacement(self.filename)
            try:
                _dir = self.destination.get('directory')
                _direc = _dir.format_map(SafeDict(**self._variables))
                _dir = self.mask_replacement(_direc)
                self.directory = Path(_dir)
            except KeyError:
                # Maybe Filename contains directory?
                if self.destination["filename"]:
                    self.directory = Path(
                        self.destination["filename"]).parent
                    self.filename = Path(
                        self.destination["filename"]).name
            try:
                if self.create_destination is True:
                    self.directory.mkdir(parents=True, exist_ok=True)
            except OSError as err:
                raise ComponentError(
                    f"DownloadFrom: Error creating directory {self.directory}: {err}"
                ) from err
            except Exception as err:
                self._logger.error(f"Error creating directory {self.directory}: {err}")
                raise ComponentError(
                    f"Error creating directory {self.directory}: {err}"
                ) from err
            if "filename" in self.destination:
                if not isinstance(self.filename, PurePath):
                    self.filename = self.directory.joinpath(self.filename)
                self._logger.debug(
                    f":: Destination File: {self.filename}"
                )
        await super(DownloadFromBase, self).start(**kwargs)
        if self.url:
            self.build_headers()
        return True

    async def http_response(self, response):
        return response

    async def http_session(
        self,
        url: str = None,
        method: str = "get",
        data: dict = None,
        data_format: str = "json",
    ):
        """
        session.
            connect to an http source using aiohttp
        """
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        if url is not None:
            self.url = url
        # TODO: Auth, Data, etc
        auth = {}
        params = {}
        _data = {"data": None}
        if self.credentials:
            if "username" in self.credentials:  # basic Authentication
                auth = aiohttp.BasicAuth(
                    self.credentials["username"], self.credentials["password"]
                )
                params = {"auth": auth}
            elif "token" in self.credentials:
                self.headers["Authorization"] = "{scheme} {token}".format(
                    scheme=self.credentials["scheme"], token=self.credentials["token"]
                )
        if data_format == "json":
            params["json_serialize"] = self._encoder.dumps
            _data["json"] = data
        else:
            _data["data"] = data
        async with aiohttp.ClientSession(**params) as session:
            meth = getattr(session, method)
            if self.ssl:
                ssl = {"ssl": self.ssl_ctx, "verify_ssl": True}
            else:
                ssl = {}
            fn = partial(
                meth,
                self.url,
                headers=self.headers,
                timeout=timeout,
                allow_redirects=True,
                **ssl,
                **_data,
            )
            try:
                async with fn() as response:
                    if response.status in self._valid_response_status:
                        return await self.http_response(response)
                    else:
                        print("ERROR RESPONSE >> ", response)
                        raise ComponentError(
                            f"DownloadFrom: Error getting data from URL {response}"
                        )
            except Exception as err:
                raise ComponentError(
                    f"DownloadFrom: Error Making an SSL Connection to ({self.url}): {err}"
                ) from err
            except aiohttp.exceptions.HTTPError as err:
                raise ComponentError(
                    f"DownloadFrom: SSL Certificate Error: {err}"
                ) from err

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def run(self):
        pass

    def start_pbar(self, total: int = 1):
        return tqdm(total=total)
