from typing import List, Optional

from anyscale._private.sdk import sdk_command
from anyscale.llm.model._private.models_sdk import PrivateLLMModelsSDK
from anyscale.llm.model.models import DeletedFineTunedModel, FineTunedModel


_LLM_MODELS_SDK_SINGLETON_KEY = "llm_models_sdk"


_RETRIEVE_EXAMPLE = """
import anyscale

anyscale.llm.model.get(model_id="my-model-id")
anyscale.llm.model.get(job_ib="prodjob_123")
"""

_RETRIEVE_ARG_DOCSTRINGS = {
    "model_id": " ID of the finetuned model that is being retrieved.",
    "job_id": " ID of the Anyscale job corresponding to the fine-tuning run.",
}


_DELETE_EXAMPLE = """
import anyscale

anyscale.llm.model.delete(model_id="my-model-id")
"""

_DELETE_ARG_DOCSTRINGS = {"model_id": " ID of the finetuned model to delete."}

_LIST_EXAMPLE = """
import anyscale

anyscale.llm.model.list()
anyscale.llm.model.list(cloud_id="cld_123")
anyscale.llm.model.list(project_id="prj_123")
anyscale.llm.model.list(cloud_id="cld_123", project_id="prj_123")
anyscale.llm.model.list(project_id="prj_123", max_items=10)
"""

_LIST_ARG_DOCSTRINGS = {
    "cloud_id": "Cloud ID to filter by. If not specified, all models from all the clouds visible to the user (filtered optionally by `project_id`)  are listed.",
    "project_id": "Project ID to filter by. If not specified, all the models from all visible projects to the user (filtered optionally by `cloud_id`) are listed.",
    "max_items": "Maximum number of items to show in the list. By default, the 20 most recently created models are fetched.",
}


@sdk_command(
    _LLM_MODELS_SDK_SINGLETON_KEY,
    PrivateLLMModelsSDK,
    doc_py_example=_RETRIEVE_EXAMPLE,
    arg_docstrings=_RETRIEVE_ARG_DOCSTRINGS,
)
def get(
    *,
    model_id: Optional[str] = None,
    job_id: Optional[str] = None,
    _sdk: PrivateLLMModelsSDK,
) -> FineTunedModel:
    """Retrieves model card for a finetuned model."""
    return _sdk.get(model_id=model_id, job_id=job_id)


@sdk_command(
    _LLM_MODELS_SDK_SINGLETON_KEY,
    PrivateLLMModelsSDK,
    doc_py_example=_DELETE_EXAMPLE,
    arg_docstrings=_DELETE_ARG_DOCSTRINGS,
)
def delete(model_id: str, _sdk: PrivateLLMModelsSDK,) -> DeletedFineTunedModel:
    """Deletes a finetuned model. Requires owner permission for the corresponding Anyscale project."""
    return _sdk.delete(model_id)


@sdk_command(
    _LLM_MODELS_SDK_SINGLETON_KEY,
    PrivateLLMModelsSDK,
    doc_py_example=_LIST_EXAMPLE,
    arg_docstrings=_LIST_ARG_DOCSTRINGS,
)
def list(  # noqa: A001
    *,
    cloud_id: Optional[str] = None,
    project_id: Optional[str] = None,
    max_items: int = 20,
    _sdk: PrivateLLMModelsSDK,
) -> List[FineTunedModel]:
    """Lists fine-tuned models available to the user.

    By default, all models in all visible clouds under all visible projects to the user are listed. This is optionally filtered by `project_id` and/or `cloud_id`.
    """
    return _sdk.list(cloud_id=cloud_id, project_id=project_id, max_items=max_items)
