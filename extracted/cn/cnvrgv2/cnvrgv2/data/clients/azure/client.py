from azure.storage.blob import BlobServiceClient

from cnvrgv2.data.clients.base_storage_client import BaseStorageClient
from cnvrgv2.utils.converters import convert_bytes
from cnvrgv2.utils.retry import retry
from cnvrgv2.utils.storage_utils import create_dir_if_not_exists


class AzureStorage(BaseStorageClient):
    def __init__(self, storage_meta):
        super().__init__(storage_meta)

        self.chunk_size_bytes = 4*1024*1024  # default chunk size for upload/download is 4MB

        props = self._decrypt_dict(storage_meta, keys=[
            "container",
            "storage_access_key",
            "storage_account_name",
        ])
        account_name = props["storage_account_name"]
        account_key = props["storage_access_key"]
        container = props["container"]

        self.access_key = (
            "DefaultEndpointsProtocol=https;"
            "AccountName={};"
            "AccountKey={};"
            "EndpointSuffix=core.windows.net"
        ).format(
            account_name,
            account_key
        )
        self.container_name = container
        self.service = self._get_service()

    @retry(log_error=True)
    def upload_single_file(self, local_path, object_path, progress_bar=None):

        try:
            client = self.service.get_blob_client(container=self.container_name, blob=object_path)

            # Init the blob
            if client.exists():
                client.delete_blob()
            client.create_append_blob()

            with open(local_path, "rb") as local_file:
                while True:
                    read_data = local_file.read(self.chunk_size_bytes)
                    if not read_data:
                        break
                    client.append_block(read_data)
                    self.update_progress(progress_bar, len(read_data))
        except Exception as e:
            print(e)

    @retry(log_error=True)
    def download_single_file(self, local_path, object_path, progress_bar=None):
        try:
            create_dir_if_not_exists(local_path)
            if not object_path:
                return

            client = self.service.get_blob_client(container=self.container_name, blob=object_path)

            with open(local_path, "wb") as local_file:
                stream = client.download_blob(max_concurrency=1)
                for chunk in stream.chunks():
                    local_file.write(chunk)
                    self.update_progress(progress_bar, len(chunk))
        except Exception as e:
            print(e)

    def update_progress(self, progress_bar, chunk_length_bytes):
        if progress_bar and progress_bar.max > 0:
            converted_bytes, _ = convert_bytes(chunk_length_bytes, unit=progress_bar.unit)
            with progress_bar.mutex:
                progress_bar.throttled_next(converted_bytes)

    def _get_service(self):
        return BlobServiceClient.from_connection_string(
            self.access_key,
            max_chunk_get_size=self.chunk_size_bytes,
            max_single_get_size=self.chunk_size_bytes
        )
