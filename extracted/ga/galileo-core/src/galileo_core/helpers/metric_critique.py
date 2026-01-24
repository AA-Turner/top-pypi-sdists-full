from typing import List, Optional

from pydantic import UUID4

from galileo_core.constants.request_method import RequestMethod
from galileo_core.constants.routes import Routes
from galileo_core.helpers.logger import logger
from galileo_core.schemas.base_config import GalileoConfig
from galileo_core.schemas.core.metric_critique import (
    CreateMetricCritiquesRequest,
    MetricCritique,
    MetricCritiqueResponse,
)


def create_metric_critiques(
    project_id: UUID4,
    metric_name: str,
    critiques: List[MetricCritique],
    config: Optional[GalileoConfig] = None,
) -> List[MetricCritiqueResponse]:
    config = config or GalileoConfig.get()

    logger.debug(
        "Creating metric critiques.",
        extra=dict(project_id=project_id, metric_name=metric_name, n_critiques=len(critiques)),
    )

    request = CreateMetricCritiquesRequest.model_validate(
        dict(metric=metric_name, critiques=[critique.model_dump() for critique in critiques])
    )

    response_list = config.api_client.request(
        RequestMethod.POST,
        Routes.metric_critiques.format(project_id=project_id),
        json=request.model_dump(mode="json"),
    )

    return [MetricCritiqueResponse.model_validate(response_dict) for response_dict in response_list]
