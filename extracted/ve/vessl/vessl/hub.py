

from typing import List

from openapi_client.models.response_hub_model_task_list_response import (
    ResponseHubModelTaskListResponse,
)
from openapi_client.models.v1_hub_model_task_spec import V1HubModelTaskSpec
from vessl import __version__, vessl_api


def list_hub_model_tasks(
    tag: str = "",
    _type: str = "",
    limit: int = 50,
    offset: int = 0,
)-> List[V1HubModelTaskSpec]:
    tasks: ResponseHubModelTaskListResponse = vessl_api.hub_model_task_list_api(
        tag_match=tag,
        type_match=_type,
        limit=limit,
        offset=offset,
    )

    return tasks.results
