from datetime import datetime
from io import BytesIO
from pathlib import Path
import tempfile
from typing import Dict, List, Optional, Union

from benchling_api_client.v2.beta.api.data_frames import create_data_frame, get_data_frame, patch_data_frame
from benchling_api_client.v2.beta.models.data_frame import DataFrame
from benchling_api_client.v2.beta.models.data_frame_create import DataFrameCreate
from benchling_api_client.v2.beta.models.data_frame_create_manifest_manifest_item import (
    DataFrameCreateManifestManifestItem,
)
from benchling_api_client.v2.beta.models.data_frame_update import DataFrameUpdate
from benchling_api_client.v2.beta.models.data_frame_update_upload_status import DataFrameUpdateUploadStatus
from benchling_api_client.v2.beta.models.file_status_upload_status import FileStatusUploadStatus
from benchling_api_client.v2.types import Response
import httpx

from benchling_sdk.errors import DataFrameInProgressError, InvalidDataFrameError, raise_for_status
from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.helpers.task_helpers import TaskHelper
from benchling_sdk.services.v2.base_service import BaseService

_DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME: float = 60.0


class V2BetaDataFrameService(BaseService):
    """
    V2-Beta Data Frames.

    Data Frames are Benchling objects that represent tabular data with typed columns and rows of data.

    See https://benchling.com/api/v2-beta/reference#/Data%20Frames
    """

    @api_method
    def get_by_id(self, data_frame_id: str) -> DataFrame:
        """
        Get a data frame and URLs to download its data.

        See https://benchling.com/api/v2-beta/reference#/Data%20Frames/getDataFrame
        """
        response = get_data_frame.sync_detailed(client=self.client, data_frame_id=data_frame_id)
        return model_from_detailed(response)

    @api_method
    def create(self, data_frame: DataFrameCreate) -> DataFrame:
        """
        Create a data frame.

        See https://benchling.com/api/v2-beta/reference#/Data%20Frames/createDataFrame
        """
        response = create_data_frame.sync_detailed(client=self.client, json_body=data_frame)
        return model_from_detailed(response)

    @api_method
    def update(self, data_frame_id: str, data_frame: DataFrameUpdate) -> TaskHelper[DataFrame]:
        """
        Update a data frame.

        See https://benchling.com/api/v2-beta/reference#/Data%20Frames/patchDataFrame
        """
        response = patch_data_frame.sync_detailed(
            client=self.client, data_frame_id=data_frame_id, json_body=data_frame
        )
        return self._task_helper_from_response(response, DataFrame)

    def upload_bytes(
        self,
        url: str,
        input_bytes: Union[BytesIO, bytes],
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME,
    ) -> None:
        """
        Upload bytes to an existing data frame.

        :param url: The url provided by Benchling for uploading to the data frame
        :param input_bytes: Data to upload as bytes or BytesIO
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        """
        # Use a completely different client instead of our configured self.client.httpx_client
        # Amazon will reject clients sending other headers besides the ones it expects
        httpx_response = httpx.put(
            url, headers=_aws_url_headers(), content=input_bytes, timeout=timeout_seconds
        )
        response = _response_from_httpx(httpx_response)
        raise_for_status(response)

    def upload_file(
        self, url: str, file: Path, timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME
    ) -> None:
        """
        Upload a file to an existing data frame.

        :param url: The url provided by Benchling for uploading to the data frame
        :param file: A valid Path to an existing file containing the data to upload
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        """
        if file.is_dir():
            raise IsADirectoryError(
                f"Cannot write data frame from directory '{file}', specify a file instead"
            )
        # Use a completely different client instead of our configured self.client.httpx_client
        # Amazon will reject clients sending other headers besides the ones it expects
        files = {"file": open(file, "rb")}
        httpx_response = httpx.put(url, headers=_aws_url_headers(), files=files, timeout=timeout_seconds)
        response = _response_from_httpx(httpx_response)
        raise_for_status(response)

    @api_method
    def create_from_bytes(
        self,
        data_frame: DataFrameCreate,
        input_bytes: Union[BytesIO, bytes],
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME,
    ) -> TaskHelper[DataFrame]:
        """
        Create a data frame from bytes or BytesIO data.

        :param data_frame: The DataFrameCreate specification for the data. This must be provided, as it cannot be inferred from file names.
        :param input_bytes: Data to upload as bytes or BytesIO
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        :return: A TaskHelper that can be polled to know when the data frame has completed processing
        :rtype: TaskHelper[DataFrame]
        """
        # This is a current limit of the DataFrame API. We may need additional methods in the future
        # to allow multi upload
        if not data_frame.manifest:
            raise InvalidDataFrameError("The data frame manifest must contain exactly 1 item")
        elif len(data_frame.manifest) != 1:
            raise InvalidDataFrameError(
                f"The data frame manifest contains {len(data_frame.manifest)} items. It must contain exactly 1"
            )
        created_data_frame = self.create(data_frame)
        manifest_item = created_data_frame.manifest[0]

        # This would be unexpected and probably an error from the API return. Likely not a user error. This check appeases MyPy.
        if manifest_item.url is None:
            raise InvalidDataFrameError(
                f"The data frame manifest URL is None. The data frame {created_data_frame.id} is not available for data upload."
            )
        self.upload_bytes(url=manifest_item.url, input_bytes=input_bytes, timeout_seconds=timeout_seconds)
        data_frame_update = DataFrameUpdate(upload_status=DataFrameUpdateUploadStatus.IN_PROGRESS)
        return self.update(data_frame_id=created_data_frame.id, data_frame=data_frame_update)

    @api_method
    def create_from_file(
        self,
        file: Path,
        data_frame: Optional[DataFrameCreate] = None,
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME,
    ) -> TaskHelper[DataFrame]:
        """
        Create a data frame from file data.

        :param file: A valid Path to an existing file containing the data to upload
        :param data_frame: The DataFrameCreate specification for the data. If not provided, it will be inferred from the file name
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        :return: A TaskHelper that can be polled to know when the data frame has completed processing
        :rtype: TaskHelper[DataFrame]
        """
        if file.is_dir():
            raise IsADirectoryError(
                f"Cannot write data frame from directory '{file}', specify a file instead"
            )
        with open(file, "rb") as file_handle:
            input_bytes = file_handle.read()
        if not data_frame:
            data_frame = DataFrameCreate(
                name=f"{datetime.now()} {file.name}",
                manifest=[DataFrameCreateManifestManifestItem(file_name=file.name)],
            )
        return self.create_from_bytes(
            data_frame=data_frame, input_bytes=input_bytes, timeout_seconds=timeout_seconds
        )

    def download_data_frame_bytes(
        self, data_frame: DataFrame, timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME
    ) -> List[BytesIO]:
        """
        Download data frame data to bytes.

        :param data_frame: The data frame to download
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of BytesIO streams corresponding to a manifest item in the data frame
        :rtype: List[BytesIO]
        """
        if data_frame.upload_status != FileStatusUploadStatus.SUCCEEDED:
            raise DataFrameInProgressError(
                f"The data frame data cannot be downloaded until the status is {FileStatusUploadStatus.SUCCEEDED}. "
                f"The status of data frame {data_frame.id} is {data_frame.upload_status}"
            )
        data_frame_bytes = []
        for manifest_item in data_frame.manifest:
            # This should be present based on the status check above. Assertion satisfies MyPy
            assert (
                manifest_item.url is not None
            ), f"Unable to download data frame {data_frame.id}, URL was empty"
            with httpx.stream("GET", manifest_item.url, timeout=timeout_seconds) as download_stream:
                target_bytes = BytesIO()
                for chunk in download_stream.iter_bytes():
                    target_bytes.write(chunk)
                target_bytes.seek(0)
                data_frame_bytes.append(target_bytes)
        return data_frame_bytes

    def download_data_frame_files(
        self,
        data_frame: DataFrame,
        destination_path: Optional[Path] = None,
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME,
    ) -> List[Path]:
        """
        Download data frame data to files.

        :param data_frame: The data frame to download
        :param destination_path: A target directory to place the files. File names will be created based on the manifest item file names.
            If not specified, a temp directory will be created. The caller is responsible for deleting this directory.
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of downloaded file paths corresponding to a manifest item in the data frame
        :rtype: List[Path]
        """
        data_frame_files = []
        if not destination_path:
            destination_path = Path(tempfile.mkdtemp())
        elif destination_path.is_file():
            raise NotADirectoryError(
                f"The destination path '{destination_path}' is a file, specify a directory instead"
            )
        elif not destination_path.exists():
            raise NotADirectoryError(f"The destination path '{destination_path}' does not exist")
        if data_frame.upload_status != FileStatusUploadStatus.SUCCEEDED:
            raise DataFrameInProgressError(
                f"The data frame data cannot be downloaded until the status is {FileStatusUploadStatus.SUCCEEDED}. "
                f"The status of data frame {data_frame.id} is {data_frame.upload_status}"
            )
        for manifest_item in data_frame.manifest:
            target_path = destination_path / manifest_item.file_name
            data_frame_files.append(target_path)
            # This should be present based on the status check above. Assertion satisfies MyPy
            assert (
                manifest_item.url is not None
            ), f"Unable to download data frame {data_frame.id}, URL was empty"
            with open(target_path, "wb") as data_frame_handle:
                with httpx.stream("GET", manifest_item.url, timeout=timeout_seconds) as download_stream:
                    for chunk in download_stream.iter_bytes():
                        data_frame_handle.write(chunk)
        return data_frame_files

    @api_method
    def download_data_frame_bytes_by_id(
        self, data_frame_id: str, timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME
    ) -> List[BytesIO]:
        """
        Download data frame data to files by data_frame_id.

        Fetches the data frame first, then downloads the files.

        :param data_frame_id: The id of the data frame to download
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of BytesIO streams corresponding to a manifest item in the data frame
        :rtype: List[BytesIO]
        """
        data_frame = self.get_by_id(data_frame_id=data_frame_id)
        return self.download_data_frame_bytes(data_frame=data_frame, timeout_seconds=timeout_seconds)

    @api_method
    def download_data_frame_files_by_id(
        self,
        data_frame_id: str,
        destination_path: Optional[Path] = None,
        timeout_seconds: float = _DEFAULT_HTTP_TIMEOUT_UPLOAD_DATA_FRAME,
    ) -> List[Path]:
        """
        Download data frame data to files by data_frame_id.

        Fetches the data frame first, then downloads the files.

        :param data_frame_id: The id of the data frame to download
        :param destination_path: A target directory to place the files. File names will be created based on the manifest item file names.
            If not specified, a temp directory will be created. The caller is responsible for deleting this directory.
        :param timeout_seconds: Extends the normal HTTP timeout settings since DataFrame uploads can be large
            Use this to extend even further if streams are very large
        :return: An ordered list of downloaded file paths corresponding to a manifest item in the data frame
        :rtype: List[Path]
        """
        data_frame = self.get_by_id(data_frame_id=data_frame_id)
        return self.download_data_frame_files(
            data_frame=data_frame, destination_path=destination_path, timeout_seconds=timeout_seconds
        )


def _aws_url_headers() -> Dict[str, str]:
    return {"x-amz-server-side-encryption": "AES256"}


def _response_from_httpx(httpx_response: httpx.Response) -> Response:
    return Response(
        status_code=httpx_response.status_code,
        content=httpx_response.content,
        headers=httpx_response.headers,
        parsed=None,
    )
