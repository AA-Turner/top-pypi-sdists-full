from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from anyscale._private.models.model_base import ModelBase
from anyscale.client.openapi_client.models import Dataset as InternalDataset
from anyscale.commands import command_examples
from anyscale.llm.dataset._private import docs


@dataclass(frozen=True)
class Dataset(ModelBase):
    """
    Metadata about a dataset, which is a file uploaded by a user to their Anyscale cloud.
    """

    __ignore_validation__ = True

    __doc_py_example__ = docs.GET_PY_EXAMPLE
    __doc_cli_example__ = command_examples.LLM_DATASET_GET_EXAMPLE

    id: str = field(metadata={"docstring": "The ID of the dataset."})
    name: str = field(metadata={"docstring": "The name of the dataset."})
    filename: str = field(
        metadata={"docstring": "The file name of the uploaded dataset."}
    )
    storage_uri: str = field(
        metadata={
            "docstring": "The URI at which the dataset is stored (eg. `s3://bucket/path/to/test.jsonl`)."
        }
    )
    version: int = field(metadata={"docstring": "The version of the dataset."})
    num_versions: int = field(
        metadata={"docstring": "Number of versions of the dataset."}
    )
    created_at: datetime = field(
        metadata={"docstring": "The time at which the dataset was uploaded."}
    )
    creator_id: str = field(
        metadata={"docstring": "The ID of the Anyscale user who uploaded the dataset."}
    )
    project_id: str = field(
        metadata={
            "docstring": "The ID of the Anyscale project that the dataset belongs to."
        }
    )
    cloud_id: str = field(
        metadata={
            "docstring": "The ID of the Anyscale cloud that the dataset belongs to."
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={"docstring": "The description of the current dataset version."},
    )

    @classmethod
    def parse_from_internal_model(cls, internal_model: InternalDataset) -> "Dataset":
        return Dataset(
            id=internal_model.id,
            name=internal_model.name,
            filename=internal_model.filename,
            storage_uri=internal_model.storage_uri,
            version=internal_model.version,
            num_versions=internal_model.num_versions,
            created_at=internal_model.created_at,
            creator_id=internal_model.creator_id,
            project_id=internal_model.project_id,
            cloud_id=internal_model.cloud_id,
            description=internal_model.description,
        )
