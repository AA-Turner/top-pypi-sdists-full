"""List multiple model training runs"""

from datetime import datetime
from typing import List, Optional, Union

from databricks.model_training.api.engine import get_return_response, run_paginated_mapi_request
from databricks.model_training.api.validation import parse_datetime
from databricks.model_training.types import TrainingRun
from databricks.model_training.types.common import ObjectList
from databricks.model_training.types.run_status import RunStatus

DEFAULT_LIMIT = 100

QUERY_FUNCTION = 'getFinetunesPaginated'
VARIABLE_DATA_NAME = 'getFinetunesPaginatedData'

QUERY = f"""
query GetFinetunesPaginated(${VARIABLE_DATA_NAME}: GetFinetunesPaginatedInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    cursor
    hasNextPage
    finetunes {{
        id
        name
        status
        createdById
        createdByEmail
        createdAt
        updatedAt
        startedAt
        completedAt
        reason
        estimatedEndTime
        isDeleted
    }}
  }}
}}"""

QUERY_WITH_DETAILS_DB = f"""
query GetFinetunesPaginated(${VARIABLE_DATA_NAME}: GetFinetunesPaginatedInput!) {{
  {QUERY_FUNCTION}({VARIABLE_DATA_NAME}: ${VARIABLE_DATA_NAME}) {{
    cursor
    hasNextPage
    finetunes {{
        id
        name
        status
        createdById
        createdByEmail
        createdAt
        updatedAt
        startedAt
        completedAt
        reason
        estimatedEndTime
        isDeleted
        details {{
            model
            taskType
            trainDataPath
            saveFolder
            evalDataPath
            evalPrompts
            trainingDuration
            learningRate
            contextLength
            experimentTracker
            customWeightsPath
            dataPrepConfig
            formattedFinetuningEvents {{
                eventType
                eventTime
                eventMessage
            }}
        }}
    }}
  }}
}}"""


def list(  # pylint: disable=redefined-builtin
    training_runs: Optional[Union[List[str], List[TrainingRun], ObjectList[TrainingRun]]] = None,
    experiment_id: Optional[str] = None,
    *,
    statuses: Optional[Union[List[str], List[RunStatus]]] = None,
    user_emails: Optional[List[str]] = None,
    before: Optional[Union[str, datetime]] = None,
    after: Optional[Union[str, datetime]] = None,
    include_details: bool = True,
    limit: Optional[int] = DEFAULT_LIMIT,
) -> ObjectList[TrainingRun]:
    """List training runs

    Args:
        training_runs (Optional[Union[List[str], List[TrainingRun], ObjectList[TrainingRun]]], optional):
        The training runs to list. Defaults to None.
        experiment_id (Optional[str], optional): The MLflow experiment ID to filter by. Defaults to None.
        statuses (Optional[Union[List[str], List[RunStatus]], optional): The statuses to filter by. Defaults to None.
        user_emails (Optional[List[str]], optional): The user emails to filter by. Defaults to None.
        include_details (bool, optional): Whether to include details in the response. Defaults to True.
        before (Optional[Union[str, datetime]], optional): The date to filter before. Defaults to None.
        after (Optional[Union[str, datetime]], optional): The date to filter after. Defaults to None.
        limit (Optional[int], optional): The maximum number of runs to return. Defaults to the 100 most recent.

    Returns:
        ObjectList[TrainingRun]: A list of training runs
    """
    filters = {}
    if training_runs:
        filters['name'] = {'in': [r.name if isinstance(r, TrainingRun) else r for r in training_runs]}
    if experiment_id:
        filters['mlflowExperimentId'] = {'equals': experiment_id}
    if statuses:
        filters['status'] = {'in': [s.value if isinstance(s, RunStatus) else s for s in statuses]}
    if before or after:
        date_filters = {}
        if before:
            date_filters['lt'] = before.astimezone().isoformat() if isinstance(before,
                                                                               datetime) else parse_datetime(before)
        if after:
            date_filters['gte'] = after.astimezone().isoformat() if isinstance(after,
                                                                               datetime) else parse_datetime(after)
        filters['createdAt'] = date_filters

    variables = {
        VARIABLE_DATA_NAME: {
            'filters': filters,
            'includeDeleted': False,
            'limit': limit,
        },
    }

    if user_emails:
        if variables[VARIABLE_DATA_NAME].get('entity'):
            variables[VARIABLE_DATA_NAME]['entity']['emails'] = user_emails
        else:
            variables[VARIABLE_DATA_NAME]['entity'] = {'emails': user_emails}

    response = run_paginated_mapi_request(
        query=QUERY_WITH_DETAILS_DB if include_details else QUERY,
        query_function=QUERY_FUNCTION,
        return_model_type=TrainingRun,
        variables=variables,
    )
    return get_return_response(response)
