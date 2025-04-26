import base64
import fnmatch
import json
import os
from typing import List, Tuple

import boto3
import botocore.client
from boto3.s3.transfer import S3Transfer
from botocore.credentials import Credentials, RefreshableCredentials
from botocore.session import Session as BotocoreSession
from google.cloud import storage
from google.oauth2.service_account import Credentials as GoogleServiceAccountCredentials

from vessl import vessl_api
from vessl.util.fmt import sizeof_fmt
from vessl.util.common import remove_prefix, safe_cast
from vessl.util.constant import VESSL_IGNORE_FILE_PATH
from vessl.util.downloader import Downloader
from vessl.util.exception import InvalidParamsError, InvalidVolumeFileError
from vessl.util.google_storage_uploader import GoogleStorageUploader


class FileTransmission:
    def __init__(self, source_path, source_abs_path, dest_abs_path, size):
        self.source_path = source_path
        self.source_abs_path = source_abs_path
        self.dest_abs_path = dest_abs_path
        self.size = size


class VolumeFileTransfer:
    def __init__(self, volume_id: int):
        self.volume = vessl_api.volume_read_api(volume_id=volume_id)
        self.provider = None
        self.region_name = None
        self.bucket_name = None
        self.prefix = None
        self.endpoint = None
        self.s3_client = None
        self.gs_client = None
        self._update_federation_credentials()

    def download(self, source_path, dest_path):
        if self.provider == "gs":
            result = vessl_api.volume_file_list_api(
                volume_id=self.volume.id,
                recursive=True,
                path=source_path,
                need_download_url=True,
            ).results
            files = sorted(result, key=lambda x: x.path)
            Downloader.download(source_path, dest_path, *files, quiet=True)
            return

        (
            file_transmissions,
            total_size,
        ) = self._get_download_file_transmissions_and_total_size(source_path, dest_path)
        total_file_count = len(file_transmissions)
        if total_file_count == 0:
            print("No files to download.")
            return

        formatted_total_size = sizeof_fmt(total_size)
        print(f"Downloading {total_file_count} file(s) ({formatted_total_size})...")

        succeeded_count = 0
        succeeded_size = 0
        for file_transmission in file_transmissions:
            dirname = os.path.dirname(file_transmission.dest_abs_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            try:
                self._get_s3_client().download_file(
                    self.bucket_name,
                    file_transmission.source_abs_path,
                    file_transmission.dest_abs_path,
                    Callback=self._create_callback(succeeded_size, total_size),
                )
                succeeded_count += 1
                succeeded_size += file_transmission.size
            except BaseException as e:
                print(f"Failed to download {file_transmission.source_path}.")
                raise e

        print(f"Total {succeeded_count} file(s) downloaded.")

    def upload(self, source_path, dest_path):
        if self.volume.is_read_only:
            print("Cannot upload to read-only volume.")
            return

        ignores = []
        if os.path.exists(VESSL_IGNORE_FILE_PATH):
            with open(VESSL_IGNORE_FILE_PATH, "r") as f:
                ignores = [line.strip() for line in f.readlines()]

        if self.provider == "gs":
            client = self._get_gs_client()
            GoogleStorageUploader.upload(
                client, source_path, self.bucket_name, self.prefix, ignores
            )
            return

        s3_client = self._get_s3_client()
        (
            file_transmissions,
            total_size,
        ) = self._get_upload_file_transmissions_and_total_size(source_path, dest_path, ignores)
        total_file_count = len(file_transmissions)
        if total_file_count == 0:
            print("No files to upload.")
            return

        formatted_total_size = sizeof_fmt(total_size)
        print(f"Uploading {total_file_count} file(s) ({formatted_total_size})...")

        succeeded_count = 0
        succeeded_size = 0
        succeeded_files = []
        for file_transmission in file_transmissions:
            try:
                s3_client.upload_file(
                    file_transmission.source_abs_path,
                    self.bucket_name,
                    file_transmission.dest_abs_path,
                    Callback=self._create_callback(succeeded_size, total_size),
                )
                succeeded_count += 1
                succeeded_size += file_transmission.size
                succeeded_files.append({"path": os.path.basename(file_transmission.dest_abs_path)})
            except BaseException as e:
                print(f"Failed to upload {file_transmission.source_path}.")
                raise e

        print(f"Total {succeeded_count} file(s) uploaded.")
        return succeeded_files

    def copy(self, source_path, dest_path):
        # TODO
        return

    def remove(self, path):
        # TODO
        return

    def _create_callback(self, current_size, total_size):
        if total_size < 100 * 1024 * 1024:
            return None

        total_transmitted = current_size
        last_percent = int(total_transmitted / total_size * 100)
        formatted_size = sizeof_fmt(total_size)
        interval = max(int(31 * 1024 * 1024 / total_size * 100), 3)

        def callback(transmitted_bytes):
            nonlocal total_transmitted, last_percent
            total_transmitted += transmitted_bytes
            percent = int(total_transmitted / total_size * 100)
            if percent - last_percent >= interval or percent == 100:
                print(f"{sizeof_fmt(total_transmitted)}/{formatted_size} ({percent}%) completed.")
                last_percent = percent

        return callback

    def _update_federation_credentials(self):
        federation_credentials = vessl_api.volume_federate_api(volume_id=self.volume.id)
        self.region_name = federation_credentials.region
        self.bucket_name = federation_credentials.bucket
        self.prefix = federation_credentials.prefix
        self.provider = federation_credentials.token.provider
        self.endpoint = federation_credentials.endpoint

    def _get_gs_client(self):
        if self.provider != "gs":
            raise InvalidVolumeFileError("This volume is not a Google Cloud Storage volume.")
        if self.gs_client:
            return self.gs_client

        self.gs_client = storage.Client(credentials=self.__get_gs_downscoped_credentials())
        return self.gs_client

    def __get_s3_api_endpoint_url(self):
        return os.environ.get("VESSL_VOLUME_S3_API_ENDPOINT_URL", self.endpoint)

    def __get_s3_api_verify_ssl(self):
        insecure_skip_tls_verify = safe_cast(os.environ.get('VESSL_INSECURE_SKIP_TLS_VERIFY'), bool, False)
        verify_tls = not insecure_skip_tls_verify
        if verify_tls:
            return True

        if os.environ.get("VESSL_VOLUME_S3_API_VERIFY_SSL") == "false":
            return False
        return None

    def _get_s3_client(self) -> S3Transfer:
        if self.s3_client:
            return self.s3_client

        no_refresh = os.environ.get("VESSL_VOLUME_CREDENTIAL_NO_REFRESH") == "true"
        if no_refresh:
            return self._get_s3_client_from_static_credentials()

        botocore_session = BotocoreSession()
        botocore_session.set_config_variable("region", self.region_name)

        creds = self.__get_s3_session_credentials()
        if creds is not None:
            refreshable_credentials = RefreshableCredentials.create_from_metadata(
                metadata=creds,
                refresh_using=self.__get_s3_session_credentials,
                method="sts-assume-role",
            )
            botocore_session._credentials = refreshable_credentials

        session = boto3.session.Session(botocore_session=botocore_session)
        config = botocore.client.Config(connect_timeout=120, read_timeout=120)
        self.s3_client = session.client(
            "s3",
            config=config,
            endpoint_url=self.__get_s3_api_endpoint_url(),
            verify=self.__get_s3_api_verify_ssl(),
        )
        return self.s3_client

    def _get_s3_client_from_static_credentials(self) -> S3Transfer:
        if self.s3_client:
            return self.s3_client

        metadata = self.__get_s3_session_credentials()
        credential = Credentials(
            access_key=metadata["access_key"], secret_key=metadata["secret_key"]
        )
        botocore_session = BotocoreSession()
        botocore_session._credentials = credential
        botocore_session.set_config_variable("region", self.region_name)
        session = boto3.session.Session(botocore_session=botocore_session)
        config = botocore.client.Config(connect_timeout=120, read_timeout=120)
        self.s3_client = session.client(
            "s3",
            config=config,
            endpoint_url=self.__get_s3_api_endpoint_url(),
            verify=self.__get_s3_api_verify_ssl(),
        )
        return self.s3_client

    def __get_all_s3_objects(self, **base_kwargs):
        continuation_token = None
        while True:
            list_kwargs = dict(MaxKeys=1000, **base_kwargs)
            if continuation_token:
                list_kwargs["ContinuationToken"] = continuation_token

            response = self._get_s3_client().list_objects_v2(**list_kwargs)
            yield from filter(
                lambda x: not x["Key"].endswith("/") or x["Size"] > 0, response.get("Contents", [])
            )

            if not response.get("IsTruncated"):
                break

            continuation_token = response.get("NextContinuationToken")

    def _get_download_file_transmissions_and_total_size(
        self, source_path: str, dest_path: str
    ) -> Tuple[List[FileTransmission], int]:
        source_path = source_path.strip("/")
        contents_only = source_path == "." or source_path.endswith("/.")
        if contents_only:
            source_path = source_path[:-2] if source_path.endswith("/.") else ""
        is_root = source_path == ""
        source_abs_path = (
            os.path.join(self.prefix, source_path).replace(os.sep, "/").rstrip("/")
            if self.prefix
            else source_path
        )
        dest_abs_path = os.path.abspath(dest_path)

        objects = list(self.__get_all_s3_objects(Bucket=self.bucket_name, Prefix=source_abs_path))
        if len(objects) == 0:
            return [], 0

        if len(objects) > 1 and os.path.exists(dest_abs_path) and not os.path.isdir(dest_abs_path):
            raise InvalidParamsError(f"{dest_abs_path} is not a directory.")

        if len(objects) == 1 and source_path == remove_prefix(objects[0]["Key"], self.prefix + "/"):
            file_transmission = FileTransmission(
                source_path=source_path,
                source_abs_path=objects[0]["Key"],
                dest_abs_path=dest_abs_path,
                size=objects[0]["Size"],
            )
            if os.path.isdir(dest_abs_path):
                file_transmission.dest_abs_path = os.path.join(
                    dest_abs_path, source_path.split("/")[-1]
                )

            return [file_transmission], file_transmission.size

        prefix = source_abs_path if contents_only else source_abs_path.rsplit("/", 1)[0]
        total_size = 0
        file_transmissions = []
        for obj in objects:
            total_size += obj["Size"]
            if is_root:
                source_rel_path = remove_prefix(obj["Key"], self.prefix + "/")
            else:
                source_rel_path = remove_prefix(obj["Key"], prefix + "/")

            file_transmissions.append(
                FileTransmission(
                    source_path=source_rel_path,
                    source_abs_path=obj["Key"],
                    dest_abs_path=os.path.join(dest_abs_path, source_rel_path),
                    size=obj["Size"],
                )
            )

        return file_transmissions, total_size

    def _get_upload_file_transmissions_and_total_size(
        self, source_path: str, dest_path: str, ignores: List[str] = []
    ) -> Tuple[List[FileTransmission], int]:
        contents_only = source_path.endswith("/.")
        source_path = os.path.relpath(source_path)
        if not os.path.exists(source_path):
            raise InvalidParamsError(f"{source_path} does not exist.")

        dest_path = dest_path.strip("/")
        dest_abs_path = (
            os.path.join(self.prefix, dest_path).replace(os.sep, "/").rstrip("/")
            if self.prefix
            else dest_path
        )

        s3_client = self._get_s3_client()
        exist = True
        is_root = dest_path == ""
        is_dir = is_root
        try:
            s3_client.head_object(Bucket=self.bucket_name, Key=dest_abs_path)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                response = s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=dest_abs_path)
                if response["KeyCount"] == 0:
                    exist = False
                else:
                    is_dir = True
            else:
                raise

        source_file_name = os.path.basename(source_path)
        source_abs_path = os.path.abspath(source_path)
        if os.path.isfile(source_path):
            if len(ignores) > 0 and any(
                fnmatch.fnmatch(source_file_name, ignore) for ignore in ignores
            ):
                return [], 0
            if not exist or not is_dir:
                file_transmission = FileTransmission(
                    source_path=source_path,
                    source_abs_path=source_abs_path,
                    dest_abs_path=dest_abs_path,
                    size=os.path.getsize(source_abs_path),
                )
                return [file_transmission], file_transmission.size
            else:
                file_transmission = FileTransmission(
                    source_path=source_path,
                    source_abs_path=source_abs_path,
                    dest_abs_path=os.path.join(dest_abs_path, source_file_name).replace(
                        os.sep, "/"
                    ),
                    size=os.path.getsize(source_abs_path),
                )
                return [file_transmission], file_transmission.size

        elif not exist or is_dir:
            total_size = 0
            file_transmissions = []
            for root_path, dirs, file_names in os.walk(source_path, topdown=True):
                # Remove ignored directories
                dirs[:] = [
                    d for d in dirs if not any(fnmatch.fnmatch(d, ignore) for ignore in ignores)
                ]
                for file_name in file_names:
                    if any(fnmatch.fnmatch(file_name, ignore) for ignore in ignores):
                        continue
                    source_file_path = os.path.join(root_path, file_name)
                    source_file_abs_path = os.path.abspath(source_file_path)
                    prefix = source_abs_path if contents_only else source_abs_path.rsplit("/", 1)[0]
                    source_rel_path = remove_prefix(source_file_abs_path, prefix + "/")

                    file_size = os.path.getsize(source_abs_path)
                    file_transmissions.append(
                        FileTransmission(
                            source_file_path,
                            source_file_abs_path,
                            os.path.join(dest_abs_path, source_rel_path).replace(os.sep, "/"),
                            file_size,
                        )
                    )
                    total_size += file_size

            return file_transmissions, total_size
        else:
            raise InvalidParamsError(f"{dest_path} is not a directory.")

    def __get_s3_session_credentials(self):
        federation_credentials = vessl_api.volume_federate_api(volume_id=self.volume.id)
        if federation_credentials.token.s3 is None:
            return None

        creds = federation_credentials.token.s3
        return {
            "access_key": creds.access_key_id,
            "secret_key": creds.secret_access_key,
            "token": creds.session_token,
            "expiry_time": creds.expiration.isoformat(),
        }

    def __get_gs_downscoped_credentials(self):
        federation_credentials = vessl_api.volume_federate_api(volume_id=self.volume.id)
        json_key_bytes = base64.b64decode(federation_credentials.token.gs.base64_credentials)
        json_key = json.loads(json_key_bytes)
        return GoogleServiceAccountCredentials.from_service_account_info(json_key)
