import concurrent.futures
import os
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Union

from frogml_storage.artifactory import ArtifactoryApi, StartTransactionResponse
from frogml_storage.authentication.models import AuthConfig
from frogml_storage.authentication.utils import get_credentials
from frogml_storage.base_storage import BaseStorage
from frogml_storage.constants import (
    DATASET,
    FROG_ML_DEFAULT_HTTP_THREADS_COUNT,
    FROG_ML_IGNORED_FILES,
    JFML_THREAD_COUNT,
    MODEL,
)
from frogml_storage.exceptions.checksum_verification_error import (
    ChecksumVerificationError,
)
from frogml_storage.exceptions.validation_error import FrogMLValidationError
from frogml_storage.logging import logger
from frogml_storage.logging.log_utils import (
    build_download_success_log,
    build_upload_success_log,
)
from frogml_storage.models import DownloadContext
from frogml_storage.models.dataset_manifest import DatasetManifest
from frogml_storage.models.entity_manifest import Artifact, Checksums, EntityManifest
from frogml_storage.models.frogml_dataset_version import FrogMLDatasetVersion
from frogml_storage.models.frogml_entity_type_info import FrogMLEntityTypeInfo
from frogml_storage.models.frogml_entity_version import FrogMLEntityVersion
from frogml_storage.models.frogml_model_version import FrogMLModelVersion
from frogml_storage.models.model_manifest import ModelManifest
from frogml_storage.models.serialization_metadata import SerializationMetadata
from frogml_storage.utils import (
    assemble_artifact_url,
    calculate_sha2,
    is_not_none,
    is_valid_thread_number,
    join_url,
    user_input_validation,
    validate_not_folder_paths,
    validate_path_exists,
)


class FileType(Enum):
    REGULAR = 1  # can represent either model or dataset file
    DEPENDENCY = 2
    ARCHIVE = 3


class FrogMLStorage(BaseStorage):
    """
    Repository implementation to download or store model|dataset artifacts, and metrics in Artifactory repository.
    """

    def __init__(self, login_config: Optional[AuthConfig] = None):
        uri, auth = get_credentials(login_config)
        self.uri = assemble_artifact_url(uri)
        self.auth = auth
        self.artifactory_api = ArtifactoryApi(self.uri, self.auth)
        self.__initialize_executor()

    def __initialize_executor(self) -> None:
        thread_count = os.getenv(JFML_THREAD_COUNT)
        if thread_count is None or not is_valid_thread_number(thread_count):
            self.http_threads_count = FROG_ML_DEFAULT_HTTP_THREADS_COUNT
        else:
            self.http_threads_count = int(thread_count)

        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=self.http_threads_count
        )

    def upload_dataset_version(
        self,
        repository: str,
        dataset_name: str,
        dataset_path: str,
        namespace: Optional[str] = None,
        version: Optional[str] = None,
        properties: Optional[dict[str, str]] = None,
    ) -> FrogMLDatasetVersion:
        return FrogMLDatasetVersion.from_entity_version(
            self.__upload_entity_version(
                repository=repository,
                entity_name=dataset_name,
                source_path=dataset_path,
                entity_type=DATASET,
                namespace=namespace,
                version=version,
                properties=properties,
            )
        )

    def upload_model_version(
        self,
        repository: str,
        model_name: str,
        model_path: str,
        model_type: Union[SerializationMetadata, Dict],
        namespace: Optional[str] = None,
        version: Optional[str] = None,
        properties: Optional[dict[str, str]] = None,
        dependencies_files_paths: Optional[List[str]] = None,
        code_archive_file_path: Optional[str] = None,
    ) -> FrogMLModelVersion:

        is_not_none("model_type", model_type)
        if isinstance(model_type, Dict):
            logger.debug(
                "received dictionary model_type, converting to SerializationMetadata"
            )
            model_type = SerializationMetadata.from_json(model_type)
        validate_not_folder_paths(dependencies_files_paths)
        validate_not_folder_paths(code_archive_file_path)
        validate_path_exists(model_path)

        return FrogMLModelVersion.from_entity_version(
            self.__upload_entity_version(
                repository=repository,
                entity_name=model_name,
                source_path=model_path,
                entity_type=MODEL,
                model_type=model_type,
                namespace=namespace,
                version=version,
                properties=properties,
                dependencies_files_paths=dependencies_files_paths,
                code_archive_file_path=code_archive_file_path,
            )
        )

    def __upload_entity_version(
        self,
        repository: str,
        entity_name: str,
        source_path: str,
        entity_type: str = "model",
        model_type: Optional[SerializationMetadata] = None,
        namespace: Optional[str] = None,
        version: Optional[str] = None,
        properties: Optional[dict[str, str]] = None,
        dependencies_files_paths: Optional[List[str]] = None,
        code_archive_file_path: Optional[str] = None,
    ) -> FrogMLEntityVersion:
        try:
            self.__verify_upload_required_args_not_none(
                repository=repository, entity_name=entity_name, source_path=source_path
            )

            user_input_validation(
                entity_name=entity_name,
                namespace=namespace,
                version=version,
                properties=properties,
            )

            validate_path_exists(source_path)

            namespace_and_name = self.__union_entity_name_with_namespace(
                namespace, entity_name
            )

            entity_type_info = FrogMLEntityTypeInfo.from_string(entity_type)
            response: StartTransactionResponse = self.artifactory_api.start_transaction(
                entity_type_info=entity_type_info,
                repository=repository,
                entity_name=namespace_and_name,
                version=version,
            )

            if version is None:
                version = response.files_upload_path.replace(
                    f"{entity_type_info.folder_name}/{namespace_and_name}/tmp/",  # nosec B108
                    "",
                ).split("/")[0]
                logger.debug(
                    "Version was not specified. Setting version to {}".format(version)
                )

            transaction_date = self.__milliseconds_to_iso_instant(
                response.transaction_id
            )

            entity_manifest: Union[ModelManifest, DatasetManifest]
            if entity_type_info == FrogMLEntityTypeInfo.MODEL:
                if not isinstance(model_type, SerializationMetadata):
                    raise AssertionError(
                        f"model_type must be {SerializationMetadata.__name__}"
                    )

                entity_manifest = ModelManifest(
                    created_date=transaction_date,
                    artifacts=[],
                    model_format=model_type,
                )
                self.__upload_model(
                    source_path=source_path,
                    repository=repository,
                    files_upload_path=response.files_upload_path,
                    dependencies_upload_path=response.dependencies_upload_path,
                    code_upload_path=response.code_upload_path,
                    entity_name=entity_name,
                    version=version,
                    entity_type_info=entity_type_info,
                    model_manifest=entity_manifest,
                    dependency_files=dependencies_files_paths,
                    code_file=code_archive_file_path,
                )
            else:
                entity_manifest = DatasetManifest(
                    created_date=transaction_date,
                    artifacts=[],
                )
                self.__upload_dataset(
                    source_path=source_path,
                    repository=repository,
                    location_to_upload=response.files_upload_path,
                    entity_name=entity_name,
                    version=version,
                    entity_type_info=entity_type_info,
                    dataset_manifest=entity_manifest,
                )

            self.artifactory_api.end_transaction(
                entity_type=entity_type_info,
                repository=repository,
                entity_name=namespace_and_name,
                entity_manifest=entity_manifest,
                transaction_id=response.transaction_id,
                version=version,
                properties=properties,
            )

            return FrogMLEntityVersion(
                entity_name=entity_name,
                namespace=namespace,
                version=version,
                entity_manifest=entity_manifest,
            )

        except FrogMLValidationError as error:
            logger.error(error.args[0], exc_info=False)

        return FrogMLEntityVersion(
            entity_name="", namespace="", version="", entity_manifest=None
        )

    def download_dataset_version(
        self,
        repository: str,
        dataset_name: str,
        version: str,
        target_path: str,
        namespace: Optional[str] = None,
    ) -> None:
        return self.__download_entity_version(
            repository=repository,
            entity_name=dataset_name,
            version=version,
            target_path=target_path,
            entity_type=DATASET,
            namespace=namespace,
        )

    def download_model_version(
        self,
        repository: str,
        model_name: str,
        version: str,
        target_path: str,
        namespace: Optional[str] = None,
    ) -> None:
        return self.__download_entity_version(
            repository=repository,
            entity_name=model_name,
            version=version,
            target_path=target_path,
            entity_type=MODEL,
            namespace=namespace,
        )

    def __download_entity_version(
        self,
        repository: str,
        entity_name: str,
        version: str,
        target_path: str,
        entity_type: str,
        namespace: Optional[str] = None,
    ) -> None:
        try:
            self.__verify_download_required_args_not_none(
                repository=repository,
                entity_name=entity_name,
                version=version,
                target_path=target_path,
            )
            user_input_validation(
                entity_name=entity_name, version=version, namespace=namespace
            )

            entity_type_info = FrogMLEntityTypeInfo.from_string(entity_type)

            download_context_list = self._get_download_context_list(
                entity_type_info=entity_type_info,
                repository=repository,
                entity_name=entity_name,
                version=version,
                target_dir_path=target_path,
                namespace=namespace,
            )

            if len(download_context_list) == 0:
                logger.info(
                    f"No files to download for {entity_type_info.entity_type}: '{entity_name}' version: '{version}'"
                )
                return
            for download_context in download_context_list[:]:
                if download_context.exists_locally:
                    logger.info(
                        f"File '{download_context.target_path}' already exists locally, will not download it."
                    )
                    download_context_list.remove(download_context)
                elif not self.__is_checksum_valid(download_context):
                    raise ChecksumVerificationError(
                        os.path.basename(download_context.target_path)
                    )

            successfully_downloaded = self._execute_parallel_download(
                download_context_list
            )

            if successfully_downloaded:
                successful_log = build_download_success_log(
                    entity_type_info, entity_name, version
                )
                logger.info(successful_log)

        except FrogMLValidationError as error:
            logger.error(error.args[0], exc_info=False)
        except Exception as e:
            logger.error(
                f"An error occurred during download_entity_version: {e}", exc_info=False
            )
            raise e

    def __is_checksum_valid(self, download_arg: DownloadContext) -> bool:
        if not download_arg.artifact_checksum:
            return False
        return (
            download_arg.artifact_checksum.sha2
            == self.artifactory_api.get_artifact_checksum(download_arg)
        )

    def _get_download_context_list(
        self,
        entity_type_info: FrogMLEntityTypeInfo,
        repository: str,
        entity_name: str,
        version: str,
        target_dir_path: str,
        namespace: Optional[str] = None,
    ) -> List[DownloadContext]:
        download_context_list = []
        entity_manifest = self.artifactory_api.get_entity_manifest(
            entity_type_info,
            repository,
            entity_name,
            namespace,
            version,
        )
        search_under_repo = f"/{repository}/"

        for artifact in entity_manifest[
            (
                "model_artifacts"
                if entity_type_info == FrogMLEntityTypeInfo.MODEL
                else "dataset_artifacts"
            )
        ]:
            download_url = artifact["download_url"]
            artifact_path = artifact["artifact_path"]
            artifact_checksum = Checksums(**artifact["checksums"])
            target_path = os.path.join(target_dir_path, artifact_path)
            position_under_repo = download_url.find(search_under_repo)
            if position_under_repo != -1:
                repo_rel_path = download_url[
                    position_under_repo + len(search_under_repo) :
                ]

                args = DownloadContext(
                    repo_key=repository,
                    source_url=repo_rel_path,
                    target_path=target_path,
                    artifact_checksum=artifact_checksum,
                )

                if not os.path.exists(target_path):
                    self.__create_dirs_if_needed(target_dir_path, artifact_path)
                else:
                    args.exists_locally = True
                download_context_list.append(args)
        return download_context_list

    def _execute_parallel_download(
        self, download_context_list: List[DownloadContext]
    ) -> int:
        if len(download_context_list) == 0:
            logger.debug("No files to download.")
            return 0
        logger.debug(f"Fetching: {len(download_context_list)} files.")
        futures = []
        for download_arg in download_context_list:
            future = self.executor.submit(
                self.artifactory_api.download_file, download_arg
            )
            futures.append(future)
        return self.__submit_and_handle_futures(futures)

    def get_entity_manifest(
        self,
        entity_type: str,
        repository: str,
        namespace: Optional[str],
        entity_name: str,
        version: Optional[str],
    ) -> dict:
        entity_type_info = FrogMLEntityTypeInfo.from_string(entity_type)
        return self.artifactory_api.get_entity_manifest(
            entity_type_info=entity_type_info,
            repository=repository,
            entity_name=entity_name,
            namespace=namespace,
            version=version,
        )

    def __upload_by_source(
        self,
        source_path: str,
        repository: str,
        location_to_upload: str,
        file_type: FileType,
        entity_manifest: Optional[EntityManifest] = None,
    ) -> bool:
        if os.path.isfile(source_path):
            rel_path = os.path.basename(source_path)
            self.__upload_single_file(
                (
                    repository,
                    source_path,
                    rel_path,
                    location_to_upload,
                    file_type,
                    entity_manifest,
                )
            )
            return True

        else:
            futures = []
            for dir_path, dir_names, file_names in os.walk(source_path):
                for filename in file_names:
                    full_path = os.path.join(dir_path, filename)
                    rel_path = os.path.relpath(full_path, source_path)
                    future = self.executor.submit(
                        self.__upload_single_file,
                        (
                            repository,
                            full_path,
                            rel_path,
                            location_to_upload,
                            file_type,
                            entity_manifest,
                        ),
                    )
                    futures.append(future)

            successfully_uploaded = self.__submit_and_handle_futures(futures)

            if successfully_uploaded > 0:
                return True
            return False

    def __upload_model(
        self,
        source_path: str,
        repository: str,
        files_upload_path: str,
        dependencies_upload_path: str,
        code_upload_path: str,
        entity_name: str,
        version: str,
        entity_type_info: FrogMLEntityTypeInfo,
        model_manifest: ModelManifest,
        dependency_files: Optional[List[str]] = None,
        code_file: Optional[str] = None,
    ) -> None:
        logger.debug("Uploading model files...")
        is_successful_upload: bool = self.__upload_by_source(
            source_path,
            repository,
            files_upload_path,
            FileType.REGULAR,
            model_manifest,
        )
        logger.debug("Uploading model requirement files...")
        if dependency_files is not None:
            for dependency_file in dependency_files:
                is_successful_upload &= self.__upload_by_source(
                    dependency_file,
                    repository,
                    dependencies_upload_path,
                    FileType.DEPENDENCY,
                    model_manifest,
                )
        logger.debug("Uploading model code archive file...")
        if code_file is not None:
            is_successful_upload &= self.__upload_by_source(
                code_file,
                repository,
                code_upload_path,
                FileType.ARCHIVE,
                model_manifest,
            )
        if is_successful_upload:
            successful_log = build_upload_success_log(
                entity_type_info, entity_name, version
            )
            logger.info(successful_log)

    def __upload_dataset(
        self,
        source_path: str,
        repository: str,
        location_to_upload: str,
        entity_name: str,
        version: str,
        entity_type_info: FrogMLEntityTypeInfo,
        dataset_manifest: DatasetManifest,
    ) -> None:
        logger.debug("Uploading dataset files...")
        is_successful_upload: bool = self.__upload_by_source(
            source_path=source_path,
            repository=repository,
            location_to_upload=location_to_upload,
            file_type=FileType.REGULAR,
            entity_manifest=dataset_manifest,
        )
        if is_successful_upload:
            successful_log = build_upload_success_log(
                entity_type_info, entity_name, version
            )
            logger.info(successful_log)

    @staticmethod
    def __submit_and_handle_futures(futures: list) -> int:
        failed_futures = []
        for future in futures:
            try:
                future.result()
            except Exception as e:
                failed_futures.append(e.args)

        if len(failed_futures) > 0:
            for failed_future in failed_futures:
                logger.error(f"{failed_future}")

        return len(futures) - len(failed_futures)

    def __upload_single_file(self, args):
        (
            repository,
            full_path,
            rel_path,
            location_to_upload,
            file_type,
            entity_manifest,
        ) = args
        if not FrogMLStorage.__is_ignored_file(full_path=full_path):
            checksums = Checksums.calc_checksums(full_path)
            if entity_manifest is not None:
                if file_type == FileType.REGULAR:
                    entity_manifest.add_file(full_path, checksums, rel_path)
                elif file_type == FileType.DEPENDENCY:
                    entity_manifest.add_dependency_file(full_path, checksums, rel_path)
                elif file_type == FileType.ARCHIVE:
                    entity_manifest.code_artifacts = Artifact(
                        artifact_path=rel_path,
                        size=os.path.getsize(full_path),
                        checksums=checksums,
                    )
            url = join_url(self.uri, repository, location_to_upload, rel_path)
            is_checksum_deploy_success = self.artifactory_api.checksum_deployment(
                url=url, checksum=checksums, full_path=full_path, stream=True
            )
            if is_checksum_deploy_success is False:
                self.artifactory_api.upload_file(url=url, file_path=full_path)

    @staticmethod
    def __calculate_sha2_no_error(file_path: str) -> Optional[str]:
        # Used to calculate sha2 without raising an exception
        if os.path.exists(file_path) is False:
            logger.debug(f"File {file_path} does not exist, can't calculate sha256")
            return None
        try:
            return calculate_sha2(file_path)
        except Exception as e:
            logger.debug(f"Failed to calculate sha256 for file {file_path}. Error: {e}")
            return None

    @staticmethod
    def __verify_download_required_args_not_none(
        repository: str, entity_name: str, version: str, target_path: str
    ) -> bool:
        is_not_none("repository", repository)
        is_not_none("entity_name", entity_name)
        is_not_none("version", version)
        is_not_none("target_path", target_path)
        return True

    @staticmethod
    def __verify_upload_required_args_not_none(
        repository: str, entity_name: str, source_path: str
    ) -> bool:
        is_not_none("repository", repository)
        is_not_none("entity_name", entity_name)
        is_not_none("source_path", source_path)
        return True

    @staticmethod
    def __is_ignored_file(full_path: str) -> bool:
        normalized_path = os.path.normpath(full_path).lower()
        parts = normalized_path.split(os.sep)
        ignored_files_lower = [item.lower() for item in FROG_ML_IGNORED_FILES]

        for part in parts:
            if part in ignored_files_lower:
                return True
        return False

    @staticmethod
    def __union_entity_name_with_namespace(
        namespace: Optional[str], entity_name: str
    ) -> str:
        if namespace is None:
            return entity_name
        else:
            return namespace + "/" + entity_name

    @staticmethod
    def __create_dirs_if_needed(base_dir: str, file_uri: str) -> str:
        full_path = os.path.join(base_dir, file_uri.strip("/"))
        dest_path = os.path.dirname(full_path)
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        return dest_path

    @staticmethod
    def __milliseconds_to_iso_instant(milliseconds: str) -> str:
        instant: datetime = datetime.fromtimestamp(
            int(milliseconds) / 1000.0, tz=timezone.utc
        )
        x = instant.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]
        return x
