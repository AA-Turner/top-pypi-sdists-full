from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from frogml_storage.models.frogml_dataset_version import FrogMLDatasetVersion
from frogml_storage.models.frogml_model_version import FrogMLModelVersion
from frogml_storage.models.serialization_metadata import SerializationMetadata


class BaseStorage(ABC):
    """
    Repository storage to download or store model | dataset artifacts,
    metrics and relation between these in an Artifactory repository.
    """

    @abstractmethod
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
        """Upload model to a repository in Artifactory. Uploaded models should be stored with the following layout:
        ├── REPO
            ├── models
                ├── ${NAMESPACE}
                    ├── ${MODEL_NAME}
                        ├── ${MODEL_VERSION}
                            ├── model-manifest.json
                            ├── model
                                ├── model.pkl
                                ├── evidence.json
                                ├── ...
                            ├── code
                                ├── code.zip
                                ├── requirements.txt
        :param repository: the repository to upload the model to
        :param model_name: the name of the model
        :param model_path: the source path of the model
        :param model_type: the type of the model (PyTorch, HuggingFace, Catboost)
        :param namespace: the namespace to upload the model to
        :param version: the version of the model
        :param properties: tags to associate with the model
        :param dependencies_files_paths: the list of dependencies files paths
        :param code_archive_file_path: the path to the code archive file
        """
        pass

    @abstractmethod
    def download_model_version(
        self,
        repository: str,
        model_name: str,
        version: str,
        target_path: str,
        namespace: Optional[str] = None,
    ) -> None:
        """Downloads a model from an Artifactory repository
        :param repository: the repository to download the model from
        :param model_name: the name of the model to download
        :param version: the version of the model to download
        :param target_path: the target local path to store the model in
        :param namespace: the namespace of the model to download

        """
        pass

    def download_model_single_artifact(
        self,
        repository: str,
        model_name: str,
        version: str,
        target_path: str,
        source_artifact_path: str,
        namespace: Optional[str] = None,
    ) -> None:
        """Downloads an artifact from an Artifactory repository
        :param repository: the repository to download the artifact from
        :param model_name: the model to download artifact from
        :param version: the model's version to download artifact from
        :param target_path: the target local path to store the artifact in
        :param source_artifact_path: the path of the artifact under the model's version directory
        :param namespace: the namespace of the artifact
        """
        pass

    @abstractmethod
    def upload_dataset_version(
        self,
        repository: str,
        dataset_name: str,
        source_path: str,
        namespace: Optional[str] = None,
        version: Optional[str] = None,
        tags: Optional[dict[str, str]] = None,
    ) -> FrogMLDatasetVersion:
        """Uploads a dataset to a repository in Artifactory. Uploaded datasets should be stored with
         the following layout:
        ├── REPO
            ├── datasets
                ├── ${NAMESPACE}
                    ├── ${DATASET_NAME}
                        ├── ${DATASET_VERSION}
                            ├── dataset-manifest.json
                            ├── dataset
                                ├── cli_docs_1.csv
                                ├── cli_docs_2.csv
                                ├── ...
        :param repository: the repository to upload the dataset to
        :param dataset_name: the name of the dataset
        :param source_path: the source path of the dataset
        :param namespace: the namespace to upload the dataset to
        :param version: the version of the dataset
        :param tags: tags to associate with the dataset
        """
        pass

    @abstractmethod
    def download_dataset_version(
        self,
        repository: str,
        dataset_name: str,
        version: str,
        target_path: str,
        namespace: Optional[str] = None,
    ) -> None:
        """Downloads a dataset from an Artifactory repository
        :param repository: the repository to download the dataset from
        :param dataset_name: the name of the dataset to download
        :param version: the version of the dataset to download
        :param target_path: the target local path to store the dataset in
        :param namespace: the namespace of the dataset to download

        """
        pass
