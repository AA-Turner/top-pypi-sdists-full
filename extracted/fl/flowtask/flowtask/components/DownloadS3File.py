from typing import Optional, Callable
import os
import mimetypes
import asyncio
from io import BytesIO
import aiofiles
from botocore.exceptions import ClientError
from urllib.parse import urlparse
from ..interfaces.Boto3Client import Boto3Client
from ..interfaces.dataframes.pandas import PandasDataframe
from .flow import FlowComponent
from ..exceptions import FileNotFound, ComponentError

_EXTENSION_MAP = {
    # fall‑backs when `mimetypes` lacks something you need
    'image/heic': '.heic',
    'image/webp': '.webp',
}

class DownloadS3File(Boto3Client, FlowComponent, PandasDataframe):
    """
    Download a file from an S3 bucket.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadS3File:
          # attributes here
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
        """
        Initialize the DownloadS3File component.

        Args:
            loop (asyncio.AbstractEventLoop): The event loop to use.
            job (Callable): The job to run.
            stat (Callable): The statistics to collect.
            **kwargs: Additional arguments.
        """
        self.path_column = kwargs.pop('path_column', 'file_path')
        self.content_type = kwargs.pop('content_type', 'application/octet-stream')
        self.filename_column: Optional[str] = kwargs.pop('filename_column', None)
        self.ignore_missing: bool = kwargs.pop('ignore_missing', False)
        self.download_dir: str = kwargs.pop('directory', '/tmp')
        self.as_bytes: bool = kwargs.pop('as_bytes', False)
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.task_parts: int = kwargs.get('task_parts', 10)
        self.extract_exif: bool = kwargs.pop('extract_exif', False)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.files_dict = {}  # Dictionary to store downloaded files

    async def start(self, **kwargs):
        """
        start.

            Initialize Task.
        """
        self.processing_credentials()
        await super().start(**kwargs)
        if self.previous:
            self.data = self.input
        # check if self.filename_column and self.path_column are in self.data dataframe:
        if self.filename_column not in self.data.columns:
            raise ValueError(f'Filename column {self.filename_column} not found in data.')
        if self.path_column not in self.data.columns:
            raise ValueError(f'Path column {self.path_column} not found in data.')
        if not self.bucket:
            self.bucket = self.credentials.get('bucket', None)
        # check if self.data is empty:
        if self.data.empty:
            raise ValueError('Dataframe is empty.')
        # evaluate the download_dir:
        if self.download_dir:
            self.download_dir = self.download_dir.strip()
            self.download_dir = self.mask_replacement(self.download_dir)
        return True

    def parse_s3_url(self, url: str) -> tuple:
        """
        Parse an S3 URL into bucket and key.

        Args:
            url (str): The S3 URL to parse.

        Returns:
            tuple: A tuple containing the bucket name and the key.
        """
        parsed_url = urlparse(url)
        if parsed_url.scheme == 's3':
            # s3://bucket-name/key
            bucket_name = parsed_url.netloc
            object_key = parsed_url.path.lstrip('/')
        elif parsed_url.netloc.endswith('.s3.amazonaws.com'):
            # https://bucket-name.s3.amazonaws.com/key
            bucket_name = parsed_url.netloc.split('.s3.amazonaws.com')[0]
            object_key = parsed_url.path.lstrip('/')
        elif '.s3.' in parsed_url.netloc:
            # https://s3.region.amazonaws.com/bucket-name/key or
            # https://bucket-name.s3.region.amazonaws.com/key
            if parsed_url.netloc.startswith('s3.'):
                # https://s3.region.amazonaws.com/bucket-name/key
                path_parts = parsed_url.path.lstrip('/').split('/', 1)
                bucket_name = path_parts[0]
                object_key = path_parts[1] if len(path_parts) > 1 else ''
            else:
                # https://bucket-name.s3.region.amazonaws.com/key
                bucket_name = parsed_url.netloc.split('.s3.')[0]
                object_key = parsed_url.path.lstrip('/')
        elif self.prefix:
            # Custom domain pointing to S3
            # Use provided bucket or extract from path
            bucket_name = self.bucket
            object_key = self.prefix + parsed_url.path.lstrip('/')
        else:
            # Custom domain pointing to S3
            # Use provided bucket or extract from path
            bucket_name = self.bucket
            object_key = parsed_url.path.lstrip('/')
        return bucket_name, object_key

    def _filename_from_key(
        self,
        object_key: str,
        content_type: str | None = None
    ) -> str:
        """
        Return a filename with an extension derived from either the key
        or the S3 object's Content‑Type.
        """
        # 1) basename from the key
        fname = os.path.basename(object_key)
        root, ext = os.path.splitext(fname)

        if ext:                         # key already has an extension
            return fname

        # 2) derive from Content‑Type
        if content_type:
            ext = mimetypes.guess_extension(content_type.split(';')[0].strip()) \
                or _EXTENSION_MAP.get(content_type)

        # 3) final fall‑back
        ext = ext or '.jpg'
        return f"{root}{ext}"

    async def download_file(self, row, idx, client, as_bytes: bool = False):
        path = row[self.path_column]
        filename = row[self.filename_column]
        if not path or not filename:
            raise ValueError(f'Path or filename is empty for row {idx}.')
        bucket_name, object_key = self.parse_s3_url(path)
        if bucket_name != self.bucket:
            raise ValueError(f'Bucket name {bucket_name} does not match {self.bucket}.')
        try:
            obj = await client.get_s3_object(
                bucket=bucket_name,
                filename=object_key,
            )
            content_type = obj.get("ContentType", self.content_type)
            filename = self._filename_from_key(object_key, content_type)

            self.data.at[idx, 'file_obj'] = obj
            file_data = None
            with obj["Body"] as stream:
                file_data = stream.read()
            if as_bytes:
                # Read the file into BytesIO
                output = BytesIO()
                output.write(file_data)
                output.seek(0)
                self.data.at[idx, 'file_data'] = output
            if self.download_dir:
                # save file in download_dir:
                output_path = f"{self.download_dir}/{filename}"
                async with aiofiles.open(output_path, 'wb') as f:
                    await f.write(file_data)
                self.data.at[idx, 'file_path'] = output_path
            return row
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise FileNotFound(
                    f"File '{object_key}' not found in bucket '{bucket_name}'."
                ) from e
            elif e.response['Error']['Code'] == 'NoSuchBucket':
                raise FileNotFound(
                    f"Bucket '{bucket_name}' does not exist."
                ) from e
            else:
                raise ComponentError(
                    f"Error downloading file from S3: {str(e)}"
                ) from e
        except Exception as e:
            self._logger.error(
                f'Error downloading file {filename}: {e}'
            )
            raise e

    async def run(self):
        """
        run.

            Download the file from S3.
        """
        async with await self.open() as client:
            if self.bucket is None:
                raise ValueError('Bucket name is required.')
            if self.filename_column is None:
                raise ValueError('Filename column is required.')
            if self.path_column is None:
                raise ValueError('Path column is required.')

            # Create the new columns:
            self.column_exists('file_obj')
            self.column_exists('file_path')
            self.column_exists('file_data')
            # generate tasks from dataframe:
            tasks = self._create_tasks(
                self.data,
                self.download_file,
                client=client,
                as_bytes=self.as_bytes
            )
            # process tasks:
            results = await self._processing_tasks(tasks, return_exceptions=True)
            # process results:
            for result in results:
                if isinstance(result, Exception):
                    if self.ignore_missing and isinstance(result, FileNotFound):
                        self._logger.warning(f'Ignoring missing file: {result}')
                        continue
                    raise result
        self._print_data_(self.data, ' DownloadS3File ')
        self._result = self.data
        return self._result
