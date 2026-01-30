import json
import os
from typing import Optional

from requests import Response
from tqdm.auto import tqdm
from tqdm.utils import CallbackIOWrapper
from urllib3 import Retry

from frogml_storage.logging import logger
from frogml_storage.utils import join_url
from frogml_storage.constants import CHECKSUM_SHA2_HEADER
from frogml_storage.models.entity_manifest import Checksums, EntityManifest
from frogml_storage.models.frogml_entity_type_info import FrogMLEntityTypeInfo
from frogml_storage.http import HTTPClient
from frogml_storage.models import DownloadContext


class StartTransactionResponse:
    files_upload_path: str
    lead_upload_path: str
    dependencies_upload_path: str
    code_upload_path: str
    transaction_id: str

    def __init__(
        self,
        files_upload_path,
        lead_upload_path,
        dependencies_upload_path,
        code_upload_path,
        transaction_id,
    ):
        self.files_upload_path = files_upload_path
        self.lead_upload_path = lead_upload_path
        self.dependencies_upload_path = dependencies_upload_path
        self.code_upload_path = code_upload_path
        self.transaction_id = transaction_id


class ArtifactoryApi:
    def __init__(self, uri, auth=None, http_client=None):
        self.uri = uri
        if http_client is not None:
            self.http_client = http_client
        else:
            self.auth = auth
            self.http_client = HTTPClient(auth=auth)

    def start_transaction(
        self,
        entity_type_info: FrogMLEntityTypeInfo,
        repository: str,
        entity_name: str,
        version: Optional[str],
    ) -> StartTransactionResponse:
        """
        Initializes an upload. Returns transaction ID and upload path
        """
        if version is None:
            start_transaction_url = (
                f"{self.uri}/api/machinelearning/{repository}/"
                f"{entity_type_info.entity_type}/{entity_name}/start-transaction"
            )
        else:
            start_transaction_url = (
                f"{self.uri}/api/machinelearning/{repository}/{entity_type_info.entity_type}"
                f"/{entity_name}/start-transaction/{version}"
            )
        try:
            response = self.http_client.post(start_transaction_url)
            response.raise_for_status()
            files_upload_path = response.json()["filesUploadPath"]
            lead_upload_path = response.json()["leadUploadPath"]
            dependencies_upload_path = response.json()["dependenciesUploadPath"]
            code_upload_path = response.json()["codeUploadPath"]
            transaction_id = response.json()["transactionId"]
        except Exception as exception:
            err = (
                f"Error occurred while trying to start an upload transaction for "
                f"{entity_type_info.entity_type}: '{entity_name}'"
                f" Error: '{exception}'"
            )
            logger.error(err, exc_info=False)
            raise exception
        return StartTransactionResponse(
            files_upload_path=files_upload_path,
            lead_upload_path=lead_upload_path,
            dependencies_upload_path=dependencies_upload_path,
            code_upload_path=code_upload_path,
            transaction_id=transaction_id,
        )

    def end_transaction(
        self,
        entity_type: FrogMLEntityTypeInfo,
        repository: str,
        entity_name: str,
        entity_manifest: EntityManifest,
        transaction_id: str,
        version: str,
        properties: Optional[dict[str, str]],
    ) -> None:
        """
        Upload model-manifest.json | dataset-manifest.json file, makes the model | dataset available in the repository
        """
        filename = entity_type.metadata_file_name

        url = join_url(
            self.uri,
            "api",
            "machinelearning",
            repository,
            entity_type.entity_type,
            "entity-manifest",
            entity_name,
            version,
            transaction_id,
        )

        json_entity_manifest = entity_manifest.to_json()
        self.upload_entity_manifest(
            entity_type=entity_type,
            filename=filename,
            payload=json_entity_manifest,
            url=url,
            properties=properties,
        )

    def download_file(self, args: DownloadContext) -> None:
        filename = os.path.basename(args.target_path)
        try:
            url = f"{self.uri}/{args.repo_key}/{args.source_url}"
            with self.http_client.get(url=url, stream=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))
                with open(args.target_path, "wb") as file:
                    with self.__initialize_progress_bar(total_size, filename) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                file.write(chunk)
                                pbar.update(len(chunk))

        except Exception as exception:
            self.__handle_download_exception(exception, args.target_path, filename)

    def get_entity_manifest(
        self,
        entity_type_info: FrogMLEntityTypeInfo,
        repository: str,
        entity_name: str,
        namespace: Optional[str],
        version: Optional[str],
    ) -> dict:
        url = join_url(
            self.uri,
            "api",
            "machinelearning",
            repository,
            entity_type_info.entity_type,
            "entity-manifest",
            namespace,
            entity_name,
            version,
        )
        try:
            with self.http_client.get(url=url) as r:
                r.raise_for_status()
                return r.json()
        except Exception as exception:
            err = f"Error occurred while trying to get {entity_type_info.entity_type} info file. Error: '{exception}'"
            logger.error(err, exc_info=False)
            raise exception

    @staticmethod
    def __handle_download_exception(
        exception: Exception, target_path: str, filename: str
    ) -> None:
        if os.path.exists(target_path):
            os.remove(target_path)
        err = f"Error occurred while trying to download file: '{filename}' Error: '{exception}'"
        logger.error(err, exc_info=False)
        raise exception

    def get_artifact_checksum(self, download_context: DownloadContext) -> str:
        url = f"{self.uri}/{download_context.repo_key}/{download_context.source_url}"
        try:
            with self.http_client.head(url=url, stream=True) as response:
                response.raise_for_status()
                return response.headers.get(CHECKSUM_SHA2_HEADER)

        except Exception as exception:
            logger.error(exception.__cause__, exc_info=False)
            raise exception

    def upload_entity_manifest(
        self,
        entity_type: FrogMLEntityTypeInfo,
        filename: str,
        payload: str,
        url: str,
        properties: Optional[dict[str, str]],
        stream: bool = False,
    ) -> None:
        body_part_name = f"{entity_type.body_part_stream}"

        try:
            files = {
                f"{body_part_name}": (
                    f"{body_part_name}",
                    payload,
                    "application/octet-stream",
                ),  # Include the InputStream
                "additionalData": (
                    "additionalData",
                    json.dumps(properties),
                    "application/octet-stream",
                ),  # Include the object
            }
            with self.http_client.put(url=url, files=files, stream=stream) as response:
                response.raise_for_status()
        except Exception as exception:
            err = f"Error occurred while trying to upload file: '{filename}' Error: '{exception}'"
            logger.error(err, exc_info=False)
            raise exception

    def upload_file(self, file_path: str, url: str) -> None:
        wrapped_file = None
        try:
            file_size = os.stat(file_path).st_size
            with (
                self.__initialize_progress_bar(file_size, file_path) as pbar,
                open(file_path, "rb") as file,
            ):
                wrapped_file = CallbackIOWrapper(pbar.update, file, "read")
                with self.http_client.put(url=url, payload=wrapped_file) as response:
                    response.raise_for_status()
        except Exception as exception:
            err = f"Error occurred while trying to upload file: '{file_path}' Error: '{exception}'"
            logger.error(err, exc_info=False)
            raise type(exception)(f"{err} File: {file_path}") from exception
        finally:
            if wrapped_file is not None:
                wrapped_file.close()

    def checksum_deployment(
        self,
        checksum: Checksums,
        url: str,
        full_path: str,
        stream: bool = False,
    ) -> bool:
        response = self.http_client.put(
            url=url,
            headers={"X-Checksum-Sha256": checksum.sha2, "X-Checksum-Deploy": "true"},
            stream=stream,
        )
        if response.status_code != 200 and response.status_code != 201:
            return False
        else:
            file_size = os.path.getsize(full_path)
            pbar = self.__initialize_progress_bar(file_size, full_path)
            pbar.update(file_size)
            pbar.close()
            return True

    @staticmethod
    def __initialize_progress_bar(total_size: int, filename: str) -> tqdm:
        return tqdm(
            total=total_size, unit="B", unit_scale=True, desc=filename, initial=0
        )

    def encrypt_password(self) -> Response:
        """
        returns encrypted password as text
        """
        return self.http_client.get(
            url=join_url(self.uri, "/api/security/encryptedPassword")
        )

    def ping(self) -> Response:
        """
        Sends a ping to Artifactory to validate login status
        """
        url = join_url(self.uri, "api/system/ping")
        return self.http_client.get(url=url)

    def get_artifactory_version(self) -> Response:
        return self.http_client.get(url=join_url(self.uri, "/api/system/version"))

    def create_machinelearning_local_repo(self, repo_name: str) -> Response:
        data = {
            "rclass": "local",
            "packageType": "machinelearning",
        }
        return self.http_client.put(
            url=join_url(self.uri, "/api/repositories/" + repo_name), json=data
        )

    def delete_frogml_local_repo(self, repo_name: str) -> Response:
        return self.http_client.delete(
            url=join_url(self.uri, "/api/repositories/" + repo_name)
        )


class RetryWithLog(Retry):
    """
    Adding extra logs before making a retry request
    """

    def __init__(self, *args, **kwargs):
        history = kwargs.get("history")
        if history is not None:
            logger.debug(f"Error: ${history[-1].error}\nretrying...")
        super().__init__(*args, **kwargs)
