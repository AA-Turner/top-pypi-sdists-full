"""Get model training runs"""

from typing import Union

from databricks.model_training.api.exceptions import DatabricksGenAIResponseError
from databricks.model_training.api.foundation_model.list import list as get_training_runs_paginated
from databricks.model_training.types import TrainingRun


def get(training_run: Union[str, TrainingRun]) -> TrainingRun:
    """Get a single training run by name or run object

    Args:
        training_run (Union[str, TrainingRun]): The training run to get.

    Returns:
        TrainingRun: The training run
    """
    training_runs = [training_run] if isinstance(training_run, str) else [training_run.name]
    run = get_training_runs_paginated(
        training_runs=training_runs,
        include_details=True,
    )

    if not run:
        name = training_run if isinstance(training_run, str) else training_run.name
        raise DatabricksGenAIResponseError(f'Finetuning run {name} not found')

    return run[0]
