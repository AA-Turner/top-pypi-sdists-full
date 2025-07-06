import os
from typing import Optional
import boto3
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from botocore.config import Config

from cnvrgv2.config import routes, error_messages
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.datasource.datasource_operations import format_credentials, get_refreshable_credentials_function,\
    handle_dir_exist
from cnvrgv2.modules.datasource.datasource_operations_interface import DatasourceOperationsInterface
from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.utils.url_utils import urljoin
from cnvrgv2.modules.datasource.bucket_downloader import BucketDownloader
from enum import Enum
import logging


# Storage types ENUM
class StorageTypes(Enum):
    S3 = "s3"
    MINIO = "minio"


class Datasource(DatasourceOperationsInterface):
    available_attributes = {
        "slug": str,
        "storage_type": str,
        "bucket_name": str,
        "name": str,
        "admin": str,
        "path": str,
        "endpoint": str,
        "region": str,
        "public": str,
        "description": str,
        "collaborators": str,
        "collaborators_info": str,
        "access_point": str
    }

    def __init__(self, context: Optional[dict] = None, slug: Optional[str] = None,
                 attributes: Optional[dict] = None) -> None:
        """Initialize the Datasource object.

        @param context: The context for the data source.
        @param slug: The slug identifier for the data source.
        @param attributes: Additional attributes for the data source.
        """
        super().__init__()
        self._context = Context(context=context)
        if slug:
            self._context.set_scope(SCOPE.DATASOURCE, slug)
        self.scope = self._context.get_scope(SCOPE.DATASOURCE)
        self._proxy = Proxy(context=self._context)
        self._route = routes.DATASOURCE_BASE.format(self.scope["organization"], self.scope["datasource"])
        self._attributes = attributes or {}
        self.slug = self.scope["datasource"]
        if self.path is None:
            self.path = ""
        elif self.path and not self.path.endswith("/"):
            # if path is not an empty string
            self.path = f"{self.path}/"

        self._client = None

    @property
    def client(self) -> boto3.client:
        """
        Lazy initialization of the S3 client.

        @return: The S3 client.
        """
        if self._client is None:
            self._client = self.get_s3_client()
        return self._client

    def _get_credentials(self) -> dict:
        """Fetch the credentials for the data source.

        @return: The credentials as a dictionary.
        """
        route = urljoin(self._route, "get_credentials")
        response = self._proxy.call_api(
            route=route,
            http_method=HTTP.GET
        )
        return response.attributes["config"]

    def get_refreshable_credentials(self) -> dict:
        """Get the refreshable credentials for the data source.

        @return: The refreshable credentials.
        """
        creds = self._get_credentials()
        return format_credentials(creds)

    def get_s3_client(self) -> boto3.client:
        """Get the S3 client with refreshable credentials.

        @return: The S3 client.
        """
        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self.get_refreshable_credentials(),
            refresh_using=get_refreshable_credentials_function(self),
            method="get_refreshable_credentials_function"
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.region)
        auto_refresh_session = boto3.Session(botocore_session=session)
        config = Config(max_pool_connections=50)
        return auto_refresh_session.client('s3', endpoint_url=self.endpoint if self.endpoint else None, config=config)

    def add_collaborator(self, collaborator_email: str) -> dict:
        """Add a collaborator to the data source.

        @param collaborator_email: The email of the user to add.
        @return: The response from the API.
        """
        route = urljoin(self._route, "add_collaborator")
        data = {
            "user_email": collaborator_email
        }
        response = self._proxy.call_api(
            route=route,
            http_method=HTTP.POST,
            payload=data
        )
        return response

    def remove_collaborator(self, collaborator_email: str) -> dict:
        """Remove a collaborator from the data source.

        @param collaborator_email: The email of the user to remove.
        @return: The response from the API.
        """
        route = urljoin(self._route, "remove_collaborator")
        data = {
            "user_email": collaborator_email
        }
        response = self._proxy.call_api(
            route=route,
            http_method=HTTP.POST,
            payload=data
        )
        return response

    def list_objects(self, page_size=100):
        """
        List the objects in the S3 bucket.

        @param page_size: The number of objects to fetch in each page when listing the bucket.
        @type page_size: int
        @return: An iterable paginator of the file names in the bucket path.
        """
        paginator = self.client.get_paginator('list_objects_v2')
        pagination_config = {'PageSize': page_size}
        list_iter = paginator.paginate(Bucket=self.bucket_name, Prefix=self.path, PaginationConfig=pagination_config)

        for page in list_iter:
            relative_paths = []
            for obj in page.get('Contents', []):
                relative_path = obj['Key']
                # Removes datasource.path from the results.
                # (this is because datasource.path represents the "root" path)
                if self.path and relative_path.startswith(self.path):
                    # in the sdk we add a trailing '/' to the path in order for boto3 to list files correctly.
                    # So when removing the datasource_path it will actually remove datasource_path/.
                    # e.g. for key = 'datasource_path/path1/path2', it will return 'path1/path2'
                    # (In s3 folders are saved in the following way : "path1/" "path2/")
                    path_to_remove = self.path
                    if not path_to_remove.endswith("/"):
                        # in this case 'datasource_path/path1/path2', it should return 'path1/path
                        # otherwise it would return '/path1/path2' which would be treated as an absolute path & cause errors
                        path_to_remove = f"{path_to_remove}/"
                    relative_path = relative_path.replace(path_to_remove, "", 1)
                if relative_path:  # don't add empty strings
                    # (this would be for instance if obj = datasource.path, then relative_path would be an empty string
                    relative_paths.append(relative_path)
            yield relative_paths

    def download_file(self, file_path: str, destination_path: str):
        """
        Download a file from the S3 bucket.

        @param file_path: The path of the file in the S3 bucket.
        @type file_path: str
        @param destination_path: The local file path to download the file to.
        @type destination_path: str
        """
        # Key will be datasource.path + file_path
        file_name_normalized = self._normalize_file_path(file_path)
        self.client.download_file(Bucket=self.bucket_name, Key=file_name_normalized,
                                  Filename=destination_path)

        return destination_path

    def get_files_downloader(self, destination_folder: str = None, page_size: int = 100,
                             max_workers: Optional[int] = None) -> BucketDownloader:
        """Get a downloader for downloading multiple files from the S3 bucket.
        @param destination_folder: The file path to download to.
        @param page_size: The number of files to fetch in each page.
        @param max_workers: The maximum number of parallel workers to use for downloading.
        @return: A BucketDownloader instance
        """
        if destination_folder is None:
            destination_folder = os.curdir

        return BucketDownloader(
            datasource=self,
            destination_folder=destination_folder,
            page_size=page_size,
            max_workers=max_workers
        )

    def clone(self, page_size: int = 100, max_workers: Optional[int] = None, skip_if_exists: bool = False,
              force: bool = False) -> None:
        """Clone the contents of the S3 bucket to a local directory.

        @param page_size: The number of files to fetch in each page.
        @param max_workers: The maximum number of parallel workers to use for downloading.
        @param skip_if_exists: If True, skip the cloning if the directory already exists.
        @param force: If True, forcefully delete the existing directory.
        """
        # Destination folder for clone: /datasource_slug
        destination_folder = self.slug

        # Handle existing datasource_slug folder:
        # 1. By default, if the folder already exists, raise an error and return.
        # 2. Force: delete the existing folder and download all. (This is useful when we want to make sure we
        # are aligned with the latest version of the datasource.)
        # 3. skip if exists: if the folder already exists, return without raising an error. (This is useful when running
        # jobs, if the user knows no changes have been made since last clone)
        if os.path.isdir(destination_folder):
            if skip_if_exists:
                if force:
                    raise CnvrgArgumentsError(error_messages.DATASOURCE_BAD_FORCE_ARGUMENTS)
                return
            else:
                handle_dir_exist(force, destination_folder)

        downloader = self.get_files_downloader(page_size=page_size,
                                               max_workers=max_workers,
                                               destination_folder=destination_folder)

        for page in downloader.page_iterator:
            downloader.download_objects(page)

    def upload_file(self, file_path: str, destination_path: Optional[str] = None) -> None:
        """Upload a file to the S3 bucket.
         @param file_path: The local file to upload.
         @param destination_path: The destination file path in the bucket.
         @return response: S3 response
        """
        if not destination_path:
            destination_path = file_path
        file_name_normalized = self._normalize_file_path(destination_path)
        response = self.client.upload_file(Bucket=self.bucket_name, Filename=file_path, Key=file_name_normalized)
        return response

    def remove_file(self, file_path: str) -> None:
        """Remove a file from the S3 bucket.
        @param file_path: The path of the file to remove.
        """
        file = self._normalize_file_path(file_path)
        response = self.client.delete_objects(Bucket=self.bucket_name, Delete={'Objects': [{'Key': file}]})
        if 'Errors' in response:
            error_message = ", ".join([error['Message'] for error in response['Errors']])
            raise Exception(f"Failed to delete file '{file_path}']: {error_message}")

    def _normalize_file_path(self, file_path: str) -> str:
        """Normalize the file name to include the path.
        @param file_path: The file name to normalize.
        @return: The file name normalized with datasource path.
        """
        if not self.path:
            return file_path
        else:
            relative_path = file_path.lstrip('/')  # if file_path is an absolute path, join will ignore self.path
            return os.path.join(self.path, relative_path)

    def delete(self) -> None:
        """Delete the data source."""
        logging.info("Deleting the datasource may affect running jobs that use it")
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE)
