import json
from typing import Any, Dict, Optional

from rich import print as rprint

from anyscale.api_utils.common_utils import (
    get_current_workspace_id,
    source_cloud_id_and_project_id,
)
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client import FinetunedmodelListResponse
from anyscale.client.openapi_client.models import FineTunedModel as APIFineTunedModel
from anyscale.controllers.base_controller import BaseController
from anyscale.llm.model.models import DeletedFineTunedModel, FineTunedModel


LIST_ENDPOINT_COUNT = 20


class ModelsController(BaseController):
    def __init__(
        self, log: Optional[BlockLogger] = None, initialize_auth_api_client: bool = True
    ):
        if log is None:
            log = BlockLogger()

        super().__init__(initialize_auth_api_client=initialize_auth_api_client)

        self.log = log
        self.log.open_block("Output")

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

    def _truncate(self, val: str, limit=50):
        return val[:limit] + "..." if len(val) > limit else val

    def _format_as_dict(
        self, model: FineTunedModel, truncate: bool = False
    ) -> Dict[str, Any]:
        output_map = {
            "id": model.id,
            "base_model_id": model.base_model_id,
            "storage_uri": self._truncate(model.storage_uri)
            if truncate
            else model.storage_uri,
            "ft_type": str(model.ft_type),
            "cloud_id": model.cloud_id,
            "project_id": model.project_id if model.project_id else "N/A",
            "created_at": model.created_at,
            "creator": model.creator if model.creator else "N/A",
            "job_id": model.job_id if model.job_id else "N/A",
            "workspace_id": model.workspace_id if model.workspace_id else "N/A",
            "generation_config": self._truncate(json.dumps(model.generation_config))
            if truncate
            else model.generation_config,
        }
        return output_map

    def get_model(self, model_id: Optional[str], job_id: Optional[str]):
        """Retrieves model information given model id"""
        if model_id:
            model = self.api_client.get_model_api_v2_llm_models_model_id_get(
                model_id
            ).result
        elif job_id:
            model = self.api_client.get_model_by_job_id_api_v2_llm_models_get_by_job_id_job_id_get(
                job_id
            ).result
        else:
            raise ValueError("Atleast one of `model-id` or `job-id` should be provided")

        model = self._parse_response_model_get(model)
        formatted_model = self._format_as_dict(model)
        rprint(formatted_model)
        return

    def delete_model(self, model_id: str):
        deleted_model = self.api_client.delete_model_api_v2_llm_models_model_id_delete(
            model_id
        ).result
        deleted_model_dict = deleted_model.to_dict()
        deleted_model_dict["deleted_at"] = int(
            deleted_model_dict["deleted_at"].timestamp()
        )
        deleted_model = DeletedFineTunedModel.from_dict(deleted_model_dict)
        rprint(deleted_model.to_dict())
        return

    def list_models(
        self, *, cloud_id: Optional[str], project_id: Optional[str], max_items: int
    ):
        """Lists fine-tuned models optionally filtered by `cloud_id` and `project_id`"""
        if get_current_workspace_id() is not None:
            # Resolve `cloud_id` and `project_id`. If not provided and if this is being run in a workspace,
            # we use the `cloud_id` and `project_id` of the workspace
            cloud_id, project_id = source_cloud_id_and_project_id(
                internal_api=self.api_client,
                external_api=self.anyscale_api_client,
                cloud_id=cloud_id,
                project_id=project_id,
            )
        paging_token = None
        results = []
        while True:
            count = min(LIST_ENDPOINT_COUNT, max_items)
            resp: FinetunedmodelListResponse = self.api_client.list_models_api_v2_llm_models_get(
                cloud_id=cloud_id,
                project_id=project_id,
                paging_token=paging_token,
                count=count,
            )
            models = resp.results
            results.extend(models)
            if not len(models) or not resp.metadata.next_paging_token:
                break

            if max_items and len(results) >= max_items:
                break
            paging_token = resp.metadata.next_paging_token

        results = results[:max_items] if max_items else results
        parsed_results = [self._parse_response_model_get(result) for result in results]
        # get formatted dict with truncated strings for a nicer print
        models_as_dicts = [
            self._format_as_dict(model, truncate=True) for model in parsed_results
        ]
        print("MODELS:")
        rprint(models_as_dicts)
        return
