from typing import Dict, List, Optional
import re
import boto3
from botocore.exceptions import ClientError
import aiofiles
from navconfig.logging import logging
from io import BytesIO
from ..conf import aws_region
try:
    from settings.settings import AWS_CREDENTIALS
except ImportError as e:
    logging.exception(
        f"AWS_CREDENTIALS not found. Please check your settings file: {e}"
    )
    from ..conf import AWS_CREDENTIALS
from .client import ClientInterface
from ..exceptions import FileNotFound, FileError, ComponentError


logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("s3transfer").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


class Boto3Client(ClientInterface):
    """
    Boto3 AWS Client.

        Overview

        Abstract class for interaction with Boto3 (AWS).

        .. table:: Properties
        :widths: auto

    +------------------------+----------+-----------+-------------------------------------------------------+
    | Name                   | Required | Summary                                                           |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |_credentials            |   Yes    | The function is loaded and then we define the necessary code to   |
    |                        |          | call the script                                                   |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  _init_                |   Yes    | Component for Data Integrator                                     |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  _host                 |   Yes    | The IPv4 or domain name of the server                             |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  get_client            |   Yes    | Gets the client access credentials, by which the user logs in to  |
    |                        |          | perform an action                                                 |
    +------------------------+----------+-----------+-------------------------------------------------------+
    |  print                 |   Yes    | Print message to display                                          |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | get_env_value          |   Yes    | Get env value  policies for setting virtual environment           |
    +------------------------+----------+-----------+-------------------------------------------------------+
    | processing_credentials |   Yes    | client credentials configured for used of the app                 |
    +------------------------+----------+-----------+-------------------------------------------------------+

            Return the list of arbitrary days


    """  # noqa

    _credentials: Dict = {
        "aws_key": str,
        "aws_secret": str,
        "client_id": str,
        "client_secret": str,
        "service": str,
        "region_name": str,
        "bucket": str,
    }

    def __init__(self, *args, **kwargs) -> None:
        self.region_name: str = kwargs.pop('region_name', None)
        self.service: str = kwargs.pop('service', 's3')
        self.bucket: Optional[str] = kwargs.pop('bucket', None)
        self.ContentType: str = kwargs.pop('ContentType', 'application/octet-stream')
        if 'config_section' in kwargs:
            self._config = kwargs.pop('config_section', 'default')
        else:
            self._config: str = kwargs.pop('config', 'default')
        super().__init__(*args, **kwargs)

    def define_host(self):
        return True

    async def open(
        self,
        host: str = None,
        port: int = None,
        credentials: dict = None,
        **kwargs
    ):
        use_credentials = credentials.pop('use_credentials', True) if credentials else True
        service = self.credentials.get('service', self.service)

        if use_credentials is False:
            self._logger.notice("Boto3: Using default credentials from environment")
            self._connection = boto3.client(
                service,
                region_name=self.credentials.get("region_name", self.region_name)
            )
        else:
            self._logger.notice("Boto3: Enter signed with explicit credentials")
            cred = {
                "aws_access_key_id": self.credentials["aws_key"],
                "aws_secret_access_key": self.credentials["aws_secret"],
                "region_name": self.credentials["region_name"],
            }
            self._connection = boto3.client(
                service,
                **cred
            )
        return self

    def processing_credentials(self):
        # getting credentials from self.credentials:
        if self.credentials:
            super().processing_credentials()
        else:
            # getting credentials from config
            self.credentials = AWS_CREDENTIALS.get(self._config)
        if not self.credentials:
            raise ValueError(
                f'Credentials not found for section {self._config}.'
            )
        ## getting Tenant and Site from credentials:
        self.region_name = self.credentials.get('region_name', aws_region)
        self.bucket = self.credentials.get('bucket_name', self.bucket)
        self.service = self.credentials.get('service', 's3')

    async def get_s3_object(self, bucket: str, filename: str):
        """
        Retrieve an object from an S3 bucket.

        Parameters
        ----------
        bucket: str
            The name of the S3 bucket.
        filename: str
            The name of the file (key) in the S3 bucket.

        Returns
        -------
        dict
            A dictionary containing the object data and metadata.

        Raises
        ------
        FileNotFound
            If the object is not found in the bucket.
        ComponentError
            If there is an issue with retrieving the object.
        """
        # Ensure connection is established
        if not self._connection:
            raise ComponentError(
                "S3 client is not connected. Call `open` first."
            )

        # Get the object from S3
        obj = self._connection.get_object(Bucket=bucket, Key=filename)
        # Validate the response
        status_code = int(obj["ResponseMetadata"]["HTTPStatusCode"])
        if status_code != 200:
            raise FileNotFound(
                f"File '{filename}' not found in bucket '{bucket}'."
            )
        return obj

    async def download_file(self, filename, obj):
        result = None
        ob_info = obj["ResponseMetadata"]["HTTPHeaders"]
        rsp = obj["ResponseMetadata"]
        status_code = int(rsp["HTTPStatusCode"])
        if status_code == 200:
            print('Content  ', ob_info["content-type"])
            filepath = self.directory.joinpath(filename)
            if ob_info["content-type"] == self.ContentType:
                contenttype = ob_info["content-type"]

                # Usar BytesIO solo cuando es un archivo individual
                if hasattr(self, '_srcfiles') and not self._srcfiles:
                    # Para múltiples archivos, usar streaming
                    async with aiofiles.open(filepath, mode="wb") as fp:
                        with obj["Body"] as stream:
                            chunk_size = 8192  # 8KB chunks
                            while True:
                                chunk = stream.read(chunk_size)
                                if not chunk:
                                    break
                                await fp.write(chunk)
                    result = {
                        "type": contenttype,
                        "file": filepath
                    }
                else:
                    # Para un archivo individual, mantener BytesIO
                    data = None
                    with obj["Body"] as stream:
                        data = stream.read()
                    output = BytesIO()
                    output.write(data)
                    output.seek(0)
                    result = {"type": contenttype, "data": output, "file": filepath}
                    # then save it into directory
                    await self.save_attachment(filepath, data)
            else:
                return FileError(
                    f'S3: Wrong File type: {ob_info["content-type"]!s}'
                )
        else:
            return FileNotFound(
                f"S3: File {filename} was not found: {rsp!s}"
            )
        return result

    async def save_attachment(self, filepath, content):
        try:
            self._logger.info(f"S3: Saving attachment file: {filepath}")
            if filepath.exists() is True:
                if (
                    "replace" in self.destination and self.destination["replace"] is True
                ):
                    # overwrite only if replace is True
                    async with aiofiles.open(filepath, mode="wb") as fp:
                        await fp.write(content)
                else:
                    self._logger.warning(
                        f"S3: File {filepath!s} was not saved, already exists."
                    )
            else:
                # saving file:
                async with aiofiles.open(filepath, mode="wb") as fp:
                    await fp.write(content)
        except Exception as err:
            raise FileError(f"File {filepath} was not saved: {err}") from err

    async def close(self, **kwargs):
        self._connection = None

    async def _list_objects_with_pagination(self, kwargs: dict) -> List:
        """Helper method to handle S3 pagination"""
        all_objects = []
        while True:
            response = self._connection.list_objects_v2(**kwargs)
            if response["KeyCount"] == 0:
                if not all_objects:  # Solo lanzar error si no hay objetos
                    raise FileNotFound(
                        f"S3 Bucket Error: Content not found on {self.bucket}"
                    )
                break

            all_objects.extend(response.get("Contents", []))

            if not response.get("IsTruncated"):  # No hay más resultados
                break

            kwargs["ContinuationToken"] = response["NextContinuationToken"]

        return all_objects

    async def s3_list(self, suffix: str = "") -> List:
        kwargs = {
            "Bucket": self.bucket,
            "Delimiter": "/",
            "Prefix": self.source_dir,
            "MaxKeys": 1000
        }
        prefix = self.source_dir
        files = []
        _patterns = []

        if not self._srcfiles:
            _patterns.append(re.compile(f"^{self.source_dir}.{suffix}+$"))
            # List objects in the S3 bucket with the specified prefix
            objects = await self._list_objects_with_pagination(kwargs)

            for obj in objects:
                key = obj["Key"]
                if obj["Size"] == 0:
                    # is a directory
                    continue
                if suffix is not None:
                    if key.startswith(prefix) and re.match(
                        prefix + suffix, key
                    ):
                        files.append(obj)
                else:
                    try:
                        for pat in _patterns:
                            mt = pat.match(key)
                            if mt:
                                files.append(obj)
                    except Exception as e:
                        self._logger.exception(e, stack_info=True)

        if self._srcfiles:
            for file in self._srcfiles:
                _patterns.append(re.compile(f"^{self.source_dir}.{file}+$"))
                objects = await self._list_objects_with_pagination(kwargs)

                for obj in objects:
                    key = obj["Key"]
                    if obj["Size"] == 0:
                        continue
                    try:
                        if hasattr(self, "source") and "filename" in self.source:
                            if self.source["filename"] == key:
                                files.append(obj)
                    except (KeyError, AttributeError):
                        pass
                    if suffix is not None:
                        if key.startswith(prefix) and re.match(
                            prefix + suffix, key
                        ):
                            files.append(obj)
                    else:
                        try:
                            for pat in _patterns:
                                mt = pat.match(key)
                                if mt:
                                    files.append(obj)
                        except Exception as e:
                            self._logger.exception(e, stack_info=True)

        return files
