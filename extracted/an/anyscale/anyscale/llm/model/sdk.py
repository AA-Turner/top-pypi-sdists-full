from typing import Any, Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import BaseSDK, Timer
from anyscale.cli_logger import BlockLogger
from anyscale.llm.model._private.models_sdk import PrivateLLMModelsSDK
from anyscale.llm.model.commands import (
    _DELETE_ARG_DOCSTRINGS,
    _DELETE_EXAMPLE,
    _LIST_ARG_DOCSTRINGS,
    _LIST_EXAMPLE,
    _RETRIEVE_ARG_DOCSTRINGS,
    _RETRIEVE_EXAMPLE,
)


class LLMModelsSDK(BaseSDK):
    def __init__(
        self,
        *,
        logger: Optional[BlockLogger] = None,
        client: Optional[AnyscaleClientInterface] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateLLMModelsSDK(
            logger=logger, client=client, timer=timer
        )

    @sdk_docs(
        doc_py_example=_RETRIEVE_EXAMPLE, arg_docstrings=_RETRIEVE_ARG_DOCSTRINGS,
    )
    def get(
        self, *, model_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> Any:
        """Retrives model card for a finetuned model."""
        return self._private_sdk.get(model_id=model_id, job_id=job_id)

    @sdk_docs(
        doc_py_example=_DELETE_EXAMPLE, arg_docstrings=_DELETE_ARG_DOCSTRINGS,
    )
    def delete(self, model_id: str) -> Any:
        """Deletes a finetuned model. Requires owner permission for the corresponding Anyscale project."""
        return self._private_sdk.delete(model_id)

    @sdk_docs(
        doc_py_example=_LIST_EXAMPLE, arg_docstrings=_LIST_ARG_DOCSTRINGS,
    )
    def list(
        self,
        *,
        cloud_id: Optional[str] = None,
        project_id: Optional[str] = None,
        max_items: int = 20,
    ) -> Any:
        """Lists fine-tuned models available to the user.

        By default, all models in all visible clouds under all visible projects to the user are listed. This is optionally filtered by `project_id` and/or `cloud_id`.
        """
        return self._private_sdk.list(
            cloud_id=cloud_id, project_id=project_id, max_items=max_items
        )
