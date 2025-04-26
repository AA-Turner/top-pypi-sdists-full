from typing import Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale._private.sdk.timer import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import FineTunedModel as APIFineTunedModel
from anyscale.llm.model.models import DeletedFineTunedModel, FineTunedModel


class PrivateLLMModelsSDK(BaseSDK):
    def __init__(
        self,
        *,
        logger: Optional[BlockLogger] = None,
        client: Optional[AnyscaleClientInterface] = None,
        timer: Optional[Timer] = None,
    ):
        super().__init__(logger=logger, client=client, timer=timer)

    def _parse_response_model_get(self, model: APIFineTunedModel) -> FineTunedModel:
        return FineTunedModel(
            id=model.id,
            base_model_id=model.base_model_id,
            cloud_id=model.cloud_id,
            # model.created_at is a datetime object, convert to unix timestamp
            created_at=int(model.created_at.timestamp()),
            # `creator` is a MiniUser object, just retrieve email
            creator=model.creator.email if model.creator is not None else None,
            ft_type=model.ft_type,
            generation_config=model.generation_config,
            job_id=model.job_id,
            project_id=model.project_id,
            storage_uri=model.storage_uri,
            workspace_id=model.workspace_id,
        )

    def list(
        self,
        *,
        cloud_id: Optional[str] = None,
        project_id: Optional[str] = None,
        max_items: int = 20,
    ):
        finetuned_models = self.client.list_finetuned_models(
            cloud_id, project_id, max_items
        )
        parsed_models = [
            self._parse_response_model_get(model) for model in finetuned_models
        ]
        return parsed_models

    def get(
        self, *, model_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> FineTunedModel:
        model = self.client.get_finetuned_model(model_id, job_id)
        return self._parse_response_model_get(model)

    def delete(self, model_id) -> DeletedFineTunedModel:
        deleted_model = self.client.delete_finetuned_model(model_id).to_dict()
        deleted_model["deleted_at"] = int(deleted_model["deleted_at"].timestamp())
        return DeletedFineTunedModel(**deleted_model)
