import os
import asyncio
import logging
from collections.abc import Callable
import aiofiles
from tqdm import tqdm
from ..exceptions import FileError
from .UploadTo import UploadToBase
from ..interfaces.Boto3Client import Boto3Client


class UploadToS3(Boto3Client, UploadToBase):
    """
    UploadToS3

    Overview

        The `UploadToS3` class is a specialized component that facilitates the uploading of files to an Amazon S3 bucket. 
        This class extends both the `Boto3Client` and `UploadToBase` classes, providing integration with AWS S3 for file 
        storage operations. The component supports the upload of individual files, multiple files, or entire directories.

    :widths: auto

        | bucket                  |   Yes    | The name of the S3 bucket to which files will be uploaded.                   |
        | directory               |   Yes    | The S3 directory path where files will be uploaded.                         |
        | source_dir              |   Yes    | The local directory containing the files to be uploaded.                    |
        | _filenames              |   Yes    | A list of filenames to be uploaded.                                         |
        | whole_dir               |   No     | A flag indicating whether to upload all files in the source directory.       |
        | ContentType             |   No     | The MIME type of the files to be uploaded. Defaults to "binary/octet-stream".|
        | credentials             |   Yes    | A dictionary containing the credentials necessary for AWS authentication.    |
        | generate_presigned_url  |   No     | Generate presigned URLs for uploaded files (default: False).                 |
        | url_column              |   No     | Column name to store presigned URLs (default: "s3_url").                     |
        | url_expiration          |   No     | Presigned URL expiration time in seconds (default: 3600).                    |
        | drop_bytesio_columns    |   No     | Drop BytesIO columns from DataFrame after upload (default: True).            |

    Return

        When receiving a DataFrame with BytesIO objects (from Zoom or Sassie):
        - Returns the same DataFrame enriched with columns:
          - `s3_key`: The S3 path/key where the file was uploaded (e.g., "zoom/recordings/2025-10-14/recording.mp3")
          - `upload_status`: "success" or "failed"
          - `upload_error`: Error message if upload failed (None if successful)
          - `s3_url`: Presigned URL for the uploaded file (if generate_presigned_url=True)

        When uploading from disk or without DataFrame input:
        - Returns a dictionary: {"files": {filename: s3_key}, "errors": {filename: error}}

    Example:

        Upload recordings from Zoom with presigned URLs:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          - UploadToS3:
          s3_config: zoom_s3
          directory: zoom/recordings/{today}/
          generate_presigned_url: true
          url_column: s3_url
          url_expiration: 86400  # 24 hours
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
        self.mdate = None
        self.local_name = None
        self.filename: str = ""
        self.whole_dir: bool = False
        self.preserve = True
        self.ContentType: str = "binary/octet-stream"

        # Handle s3_config like ThumbnailGenerator
        s3_config = kwargs.pop("s3_config", "default")
        self._config = s3_config
        
        # Handle directory parameter directly from YAML
        self.directory = kwargs.pop("directory", "/")

        # Presigned URL configuration
        self.generate_presigned_url = kwargs.pop("generate_presigned_url", False)
        self.url_column = kwargs.pop("url_column", "s3_url")
        self.url_expiration = kwargs.pop("url_expiration", 3600)

        # Drop BytesIO columns after upload (default: True to avoid DB errors)
        self.drop_bytesio_columns = kwargs.pop("drop_bytesio_columns", True)

        # Pass config to Boto3Client constructor
        kwargs['config'] = self._config

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """start Method."""
        await super(UploadToS3, self).start(**kwargs)
        
        # Process credentials first - similar to ThumbnailGenerator
        self.processing_credentials()

        if hasattr(self, "destination"):
            self.directory = self.destination["directory"]
            if not self.directory.endswith("/"):
                self.directory = self.directory + "/"
            self.directory = self.mask_replacement(self.destination["directory"])
        elif not hasattr(self, "directory") or self.directory is None:
            # Handle direct directory parameter from YAML
            self.directory = kwargs.get("directory", "/")

        # Ensure directory has trailing slash
        if self.directory and not self.directory.endswith("/"):
            self.directory += "/"
            
        if hasattr(self, "source"):
            self.whole_dir = (
                self.source["whole_dir"] if "whole_dir" in self.source else False
            )
            if self.whole_dir is True:
                # if whole dir, is all files in source directory
                logging.debug(f"Uploading all files on directory {self.source_dir}")
                p = self.source_dir.glob("**/*")
                self._filenames = [x for x in p if x.is_file()]
            else:
                if "filename" in self.source:
                    p = self.source_dir.glob(self.filename)
                    self._filenames = [x for x in p if x.is_file()]
        try:
            # Handle DataFrame input properly
            if self.previous and self.input is not None:
                # Check if input is a DataFrame
                if hasattr(self.input, 'empty'):
                    # It's a DataFrame
                    if not self.input.empty:
                        # Process DataFrame to extract file data for S3 upload
                        self._process_dataframe_input()
                else:
                    # It's a list or other iterable
                    self._filenames = self.input
            if hasattr(self, "file"):
                filenames = []
                for f in self._filenames:
                    p = self.source_dir.glob(f)
                    fp = [x for x in p if x.is_file()]
                    filenames = filenames + fp
                self._filenames = filenames
        except (NameError, KeyError):
            pass
        return self

    def _process_dataframe_input(self):
        """
        Process DataFrame input to extract file data for S3 upload.

        Supports DataFrames from:
        - Sassie component with download_photos (file_data, content_type, downloaded_filename/photo columns)
        - Zoom component with as_bytes=True (file_data, content_type, downloaded_filename columns)
        """
        import pandas as pd

        if not isinstance(self.input, pd.DataFrame):
            return

        # Check if DataFrame has file_data column (from Sassie download_photos or Zoom with as_bytes)
        if 'file_data' in self.input.columns:
            # We have BytesIO objects in memory - prepare for S3 upload
            self._filenames = []
            self._file_data_list = []
            self._content_types = []
            
            for index, row in self.input.iterrows():
                if row.get('file_data') is not None:
                    # Get filename from downloaded_filename or photo column
                    filename = row.get('downloaded_filename', row.get('photo', f'file_{index}'))
                    content_type = row.get('content_type', 'image/jpeg')
                    
                    self._filenames.append(filename)
                    self._file_data_list.append(row['file_data'])
                    self._content_types.append(content_type)
            
            # Set flag to indicate we're working with in-memory data
            self._use_memory_data = True
        else:
            # Fallback to original behavior
            self._filenames = self.input
            self._use_memory_data = False

    async def _generate_presigned_url(self, s3_key: str, expiration: int = None) -> str:
        """
        Generate a presigned URL for the S3 object.

        Args:
            s3_key: The S3 key for the uploaded file
            expiration: URL expiration time in seconds (uses self.url_expiration if not specified)

        Returns:
            Presigned URL as string
        """
        try:
            if expiration is None:
                expiration = self.url_expiration

            url = self._connection.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return url
        except Exception as e:
            self._logger.error(f"Error generating presigned URL for {s3_key}: {e}")
            return None

    async def run(self):
        """Running Upload file to S3."""
        self._result = None

        # Open S3 connection
        await self.open()

        errors = {}
        files = {}

        if hasattr(self, '_use_memory_data') and self._use_memory_data:
            # Upload from memory (BytesIO objects)
            import pandas as pd

            total_files = len(self._filenames)
            self._logger.info(f"📤 Starting upload of {total_files} files from memory to S3")

            # Add S3 columns to DataFrame
            if isinstance(self.input, pd.DataFrame):
                self.input['s3_key'] = None
                self.input['upload_status'] = None
                self.input['upload_error'] = None
                if self.generate_presigned_url:
                    self.input[self.url_column] = None

            with tqdm(total=total_files, desc="📤 Uploading to S3", unit="files", colour="blue") as pbar:
                for filename, file_data, content_type in zip(self._filenames, self._file_data_list, self._content_types):
                    s3_key = f"{self.directory}{filename}"

                    try:
                        # Reset BytesIO position to beginning
                        file_data.seek(0)
                        content = file_data.read()

                        response = self._connection.put_object(
                            Bucket=self.bucket,
                            Key=s3_key,
                            Body=content,
                            ContentType=content_type,
                        )
                        rsp = response["ResponseMetadata"]
                        status_code = int(rsp["HTTPStatusCode"])

                        if status_code == 200:
                            files[filename] = s3_key

                            # Generate presigned URL if enabled
                            presigned_url = None
                            if self.generate_presigned_url:
                                presigned_url = await self._generate_presigned_url(s3_key)

                            # Update DataFrame with success
                            if isinstance(self.input, pd.DataFrame):
                                # Find the row with this file_data
                                mask = self.input['downloaded_filename'] == filename
                                if mask.any():
                                    self.input.loc[mask, 's3_key'] = s3_key
                                    self.input.loc[mask, 'upload_status'] = 'success'
                                    if self.generate_presigned_url and presigned_url:
                                        self.input.loc[mask, self.url_column] = presigned_url
                        else:
                            error_msg = f"S3: Upload Error: {rsp!s}"
                            self._logger.error(f"❌ Upload failed for {filename}: {error_msg}")
                            errors[filename] = FileError(error_msg)

                            # Update DataFrame with error
                            if isinstance(self.input, pd.DataFrame):
                                mask = self.input['downloaded_filename'] == filename
                                if mask.any():
                                    self.input.loc[mask, 'upload_status'] = 'failed'
                                    self.input.loc[mask, 'upload_error'] = error_msg

                    except Exception as e:
                        error_msg = f"S3: Upload Error: {str(e)}"
                        self._logger.error(f"❌ CRITICAL ERROR uploading {filename}: {error_msg}")
                        errors[filename] = FileError(error_msg)

                        # Update DataFrame with error
                        if isinstance(self.input, pd.DataFrame):
                            mask = self.input['downloaded_filename'] == filename
                            if mask.any():
                                self.input.loc[mask, 'upload_status'] = 'failed'
                                self.input.loc[mask, 'upload_error'] = error_msg

                    pbar.update(1)
        else:
            # Original file-based upload logic
            total_files = len(self._filenames)
            self._logger.info(f"📤 Starting upload of {total_files} files from disk to S3")
            
            with tqdm(total=total_files, desc="📤 Uploading files to S3", unit="files", colour="blue") as pbar:
                for file in self._filenames:
                    key = os.path.basename(file)
                    filename = f"{self.directory}{key}"
                    
                    try:
                        async with aiofiles.open(file, mode="rb") as f:
                            content = await f.read()
                            response = self._connection.put_object(
                                Bucket=self.bucket,
                                Key=filename,
                                Body=content,
                                ContentType=self.ContentType,
                            )
                            rsp = response["ResponseMetadata"]
                            status_code = int(rsp["HTTPStatusCode"])
                            if status_code == 200:
                                files[file] = filename
                            else:
                                errors[file] = FileError(f"S3: Upload Error: {rsp!s}")
                    except Exception as e:
                        errors[file] = FileError(f"S3: Upload Error: {str(e)}")
                    
                    pbar.update(1)
        
        uploaded_count = len(files)
        total_count = len(self._filenames) if hasattr(self, '_filenames') else 0
        self._logger.info(f"📊 Upload completed: {uploaded_count}/{total_count} files uploaded successfully")

        if self.generate_presigned_url:
            self._logger.info(f"🔗 Presigned URLs generated with {self.url_expiration}s expiration")

        if errors:
            error_count = len(errors)
            self._logger.warning(f"⚠️ Upload errors: {error_count} files failed")

        # Add metrics
        self.add_metric("S3_UPLOADED", files)
        self.add_metric("S3_UPLOAD_COUNT", uploaded_count)
        self.add_metric("S3_ERROR_COUNT", len(errors))

        # Return DataFrame if we received one, otherwise return dict
        if hasattr(self, '_use_memory_data') and self._use_memory_data:
            import pandas as pd
            if isinstance(self.input, pd.DataFrame):
                # Drop BytesIO columns to avoid database serialization errors
                if self.drop_bytesio_columns:
                    bytesio_columns = ['file_data', 'transcript_data']
                    columns_to_drop = [col for col in bytesio_columns if col in self.input.columns]
                    if columns_to_drop:
                        self.input = self.input.drop(columns=columns_to_drop)
                        self._logger.info(f"🗑️  Dropped BytesIO columns: {columns_to_drop}")

                self._logger.info(f"✅ Returning enriched DataFrame with {len(self.input)} rows")
                self._result = self.input
                return self._result

        # Original behavior: return dict
        self._result = {"files": files, "errors": errors}
        return self._result
