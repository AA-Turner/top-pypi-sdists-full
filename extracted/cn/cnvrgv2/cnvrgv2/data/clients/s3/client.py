from datetime import datetime
from time import time

import botocore
from boto3 import Session
from boto3.s3.transfer import TransferConfig
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from dateutil.tz import tzlocal

from cnvrgv2.data.clients.base_storage_client import BaseStorageClient
from cnvrgv2.utils.retry import retry
from cnvrgv2.utils.storage_utils import create_dir_if_not_exists

config = TransferConfig(max_concurrency=10, use_threads=True)


class S3Storage(BaseStorageClient):
    def __init__(self, refresh_function, storage_meta=None):
        """
        Inits a s3 client
        @param refresh_function: func. A function to retrieve storage credentials
        @param storage_meta: dict. Storage credentials. This is the output of the storage_function.
                We allow sending the first round of credentials to prevent double calls to the server at the initiation
        """
        if storage_meta is None:
            storage_meta = refresh_function()

        super().__init__(storage_meta)

        props = self._decrypt_dict(storage_meta, keys=["bucket", "region"])

        self.refresh_function = refresh_function
        self.bucket = props.get("bucket")
        self.region = props.get("region")
        self.client = self._get_client(storage_meta)

    @retry(log_error=True)
    def upload_single_file(self, local_path, object_path, progress_bar=None):
        try:
            self.client.upload_file(
                local_path,
                self.bucket,
                object_path,
                Config=config,
                Callback=self.progress_callback(progress_bar)
            )
        except Exception as e:
            print(e)
            raise e

    @retry(log_error=True)
    def download_single_file(self, local_path, object_path, progress_bar=None):
        try:
            create_dir_if_not_exists(local_path)
            if not object_path:
                return

            self.client.download_file(
                self.bucket,
                object_path,
                local_path,
                Config=config,
                Callback=self.progress_callback(progress_bar)
            )
        except Exception as e:
            raise e

    def _refresh(self, storage_meta=None):
        """
        Refreshes the credentials
        @param storage_meta: If sent, the refresh won't be called, the storage_meta will be assumed to be the server's
            response. This is to prevent double calling the server when starting the process
        @return:
        """
        props = self._decrypt_dict(
            storage_meta or self.refresh_function(),
            keys=["sts_a", "sts_s", "sts_st", "bucket", "region", "expiration"]
        )

        ttl = self._seconds_until_expiration(props.get("expiration"))

        credentials = {
            "access_key": props.get("sts_a"),
            "secret_key": props.get("sts_s"),
            "token": props.get("sts_st"),
            "expiry_time": datetime.fromtimestamp(time() + ttl, tz=tzlocal()).isoformat()
        }
        return credentials

    @staticmethod
    def _seconds_until_expiration(datetime_string, datetime_format="%Y-%m-%d %H:%M:%S %Z"):
        """
        Calculates the number of seconds until the given expiration time
        @param datetime_string: string. A datetime string
        @param datetime_format: string. Format of the given datetime_string. defaults to the format returned from
            cnvrg server
        @return: Seconds until the given datetime
        """
        if not datetime_string:
            # 36 hours, this is the default for ci-cd in the server.
            # Add here as a fallback for old server versions that doesn't return an expiration
            return 129600
        try:
            # In case the given string is an integer
            return int(datetime_string)
        except ValueError:
            # In case it's a string representing a datetime
            target_time = datetime.strptime(datetime_string, datetime_format)
            now = datetime.utcnow()
            time_delta = target_time - now
            return time_delta.total_seconds()

    def _get_client(self, storage_meta):
        """
        Generates a client fo the process using a RefreshableCredentials session.
        @param storage_meta: dict. Credentials to begin the process with
        @return: A boto3 client
        """
        session_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self._refresh(storage_meta=storage_meta),
            refresh_using=self._refresh,
            method="sts_assume_role"
        )
        session = get_session()
        session._credentials = session_credentials
        session.set_config_variable("region", self.region)
        autorefresh_session = Session(botocore_session=session)

        botocore_config = botocore.config.Config(max_pool_connections=50)
        return autorefresh_session.client('s3', config=botocore_config, verify=self.check_certificate)
