from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from anyscale._private.models.model_base import ModelBase, ModelEnum


class FineTuningType(ModelEnum):
    LORA = "LORA"
    FULL_PARAM = "FULL_PARAM"

    __docstrings__ = {
        LORA: "Low-Rank Adaptation (LoRA) fine-tuning method.",
        FULL_PARAM: "Full parameter fine-tuning method.",
    }


@dataclass(frozen=True)
class FineTunedModel(ModelBase):
    """Represents a fine-tuned model with its associated metadata."""

    __doc_py_example__ = """\
import anyscale
from anyscale.llm.model.models import FineTunedModel
model: FineTunedModel = anyscale.llm.model.get(model_id="my-model-id")
"""

    __doc_cli_example__ = """\
$ anyscale llm model get --model-id my-model-id
id: my-model-id
base_model_id: meta-llama/Llama-3-8B-Instruct
cloud_id: cloud_abc123
created_at: 1725473924
job_id: prodjob_xyz789
ft_type: LORA
...
"""

    id: str = field(metadata={"docstring": "Unique ID/tag for the fine-tuned model."})

    def _validate_id(self, id: str):  # noqa: A002
        if not isinstance(id, str):
            raise TypeError("'id' must be a string.")

    base_model_id: str = field(
        metadata={"docstring": "Base model ID used for fine-tuning."}
    )

    def _validate_base_model_id(self, base_model_id: str):
        if not isinstance(base_model_id, str):
            raise TypeError("'base_model_id' must be a string.")

    cloud_id: str = field(
        metadata={
            "docstring": "ID for the Anyscale Cloud corresponding to the fine-tuning run."
        }
    )

    def _validate_cloud_id(self, cloud_id: str):
        if not isinstance(cloud_id, str):
            raise TypeError("'cloud_id' must be a string.")

    created_at: int = field(
        metadata={"docstring": "Time at which the fine-tuned model was created."}
    )

    def _validate_created_at(self, created_at: int):
        if not isinstance(created_at, int):
            raise TypeError("'created_at' must be an integer (Unix timestamp).")

        if created_at < 0:
            raise ValueError("'created_at' must be a positive integer")

    creator: Optional[str] = field(
        metadata={"docstring": "Email address for the user who created the model."}
    )

    def _validate_creator(self, creator: Optional[str]):
        if creator is not None and not isinstance(creator, str):
            raise TypeError("'creator' must be a string or None.")

    ft_type: FineTuningType = field(metadata={"docstring": "Fine-tuning type."})

    def _validate_ft_type(self, ft_type: FineTuningType) -> FineTuningType:
        return FineTuningType.validate(ft_type)

    generation_config: Optional[Dict[str, Any]] = field(
        metadata={
            "docstring": "Inference generation config with chat-templating parameters and stopping sequences."
        }
    )

    def _validate_generation_config(self, generation_config: Optional[Dict[str, Any]]):
        if generation_config is not None and not isinstance(generation_config, dict):
            raise TypeError("'generation_config' must be a dictionary or None.")

    job_id: Optional[str] = field(
        metadata={
            "docstring": "ID for the Anyscale job corresponding to the fine-tuning run, if applicable."
        }
    )

    def _validate_job_id(self, job_id: Optional[str]):
        if job_id is not None and not isinstance(job_id, str):
            raise TypeError("'job_id' must be a string or None.")

    project_id: Optional[str] = field(
        metadata={
            "docstring": "ID for the Anyscale Project corresponding to the fine-tuning run."
        }
    )

    def _validate_project_id(self, project_id: Optional[str]):
        if project_id is not None and not isinstance(project_id, str):
            raise TypeError("'project_id' must be a string.")

    storage_uri: str = field(
        metadata={
            "docstring": "URI at which the fine-tuned model checkpoint is stored."
        }
    )

    def _validate_storage_uri(self, storage_uri: str):
        if not isinstance(storage_uri, str):
            raise TypeError("'storage_uri' must be a string.")

    workspace_id: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "ID for the Anyscale Workspace in which the model was fine-tuned, if any."
        },
    )

    def _validate_workspace_id(self, workspace_id: Optional[str]):
        if workspace_id is not None and not isinstance(workspace_id, str):
            raise TypeError("'workspace_id' must be a string or None.")


@dataclass(frozen=True)
class DeletedFineTunedModel(ModelBase):
    """Represents a deleted fine-tuned model with its deletion metadata."""

    __doc_py_example__ = """\
import anyscale
from anyscale.llm.model.models import DeletedFineTunedModel
deleted_model: DeletedFineTunedModel = anyscale.llm.model.delete("my-model-id")
"""

    __doc_cli_example__ = """\
$ anyscale models get-deleted my-model-id
id: my-model-id
deleted_at: 1725473924
"""

    id: str = field(metadata={"docstring": "Unique ID/tag for the fine-tuned model."})

    def _validate_id(self, id: str):  # noqa: A002
        if not isinstance(id, str):
            raise TypeError("'id' must be a string.")

    deleted_at: int = field(
        metadata={
            "docstring": "Unix timestamp (in seconds) at which the fine-tuned model was deleted."
        }
    )

    def _validate_deleted_at(self, deleted_at: int):
        if not isinstance(deleted_at, int):
            raise TypeError("'deleted_at' must be an integer (Unix timestamp).")

        if deleted_at < 0:
            raise ValueError("'deleted_at' must be a positive integer (Unix timestamp)")
