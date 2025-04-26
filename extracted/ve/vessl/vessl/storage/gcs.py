import json
import os
from typing import Callable, List, Optional

import google.auth
from google.cloud import storage as gcslib
from google.cloud.exceptions import NotFound

from vessl.util.path import ensure_parent_dir_exists

from .abstract_volume import AbstractVolume
from .file import VolumeFile


class GCSVolume(AbstractVolume):
    def __init__(
        self,
        bucket_name: str,
        base_path: str,
        gcp_api_key_json: Optional[str] = "",
    ):
        self.gcp_api_key_json = gcp_api_key_json
        self.bucket_name = bucket_name
        self.base_path = base_path
        self._init_gcs()

    def _init_gcs(self):
        gcp_api_key_dict = json.loads(self.gcp_api_key_json)
        gcp_credentials, _ = google.auth.load_credentials_from_dict(gcp_api_key_dict)
        print("gcp_credentials", gcp_credentials)
        gcs_client = gcslib.Client(credentials=gcp_credentials)

        self.gcs_client = gcs_client
        self.bucket = gcs_client.bucket(bucket_name=self.bucket_name)

    def list(self, path: str) -> List[VolumeFile]:
        path_in_bucket = os.path.join(self.base_path, path)

        blobs = self.bucket.list_blobs(
            prefix=path_in_bucket,
        )

        files = []
        # Although a one-liner is also possible, we want to benefit from type check;
        # typing of list_blobs() is not very good.
        for blob in blobs:
            blob: gcslib.Blob = blob

            # Relative path to the volume root
            relative_path = os.path.relpath(blob.name, path_in_bucket)
            files.append(VolumeFile(path=relative_path, size=blob.size))

        return files

    def download_file(
        self,
        file: VolumeFile,
        destination: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ):
        path_in_bucket = os.path.join(self.base_path, file.path)

        ensure_parent_dir_exists(destination)

        self.gcs_client.download_blob_to_file(
            self.bucket.blob(blob_name=path_in_bucket),
            file_obj=open(destination, "wb"),
        )

    def download_directory(
        self,
        directory: str,
        destination: str,
        progress_callback: Optional[Callable[[int, int, int, int, int], None]] = None,
    ):
        self._download_directory_serially(directory, destination, progress_callback)

    def upload_file(
        self,
        local_file: str,
        destination: str,
        progress_callback: Optional[Callable[[int], None]] = None,
    ):
        dest_in_bucket = os.path.join(self.base_path, destination)
        self.bucket.blob(blob_name=dest_in_bucket).upload_from_filename(
            local_file,
        )

    def delete_file(self, path: str):
        blob = os.path.join(self.base_path, path)
        # Ignore NotFound errors to align with the behavior of other volumes (e.g., S3)
        try:
            self.bucket.delete_blob(blob_name=blob)
        except NotFound:
            pass

    def delete_directory(self, path: str):
        blob = os.path.join(self.base_path, path)
        files = [os.path.join(blob, v.path) for v in self.list(path)]
        # Ignore NotFound errors to align with the behavior of other volumes (e.g., S3)
        try:
            self.bucket.delete_blobs(blobs=files)
        except NotFound:
            pass
