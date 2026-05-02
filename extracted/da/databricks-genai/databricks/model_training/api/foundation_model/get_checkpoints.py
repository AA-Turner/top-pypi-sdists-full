"""List multiple model checkpoint paths"""

import os
from typing import List

import mlflow

from databricks.model_training.api.exceptions import DatabricksGenAIResponseError
from databricks.model_training.types import TrainingRun

COMPOSER_CKPT_PREFIX = 'ep'


def get_checkpoints(training_run: TrainingRun) -> List[str]:
    """List MLflow checkpoint paths for the MosaicAI Model Training SDK

    Args:
        training_run (TrainingRun): The training run to get checkpoints for

    Returns:
        List[str]: A list of checkpoint paths for that training run
    """

    if training_run is None:
        raise DatabricksGenAIResponseError('Must provide training run object to retrieve checkpoints')

    try:
        mlflow_run_id = training_run.run_id
        artifact_path = f'{training_run.name}/checkpoints'
        artifacts = mlflow.artifacts.list_artifacts(run_id=mlflow_run_id, artifact_path=artifact_path)

    except Exception as e:
        raise DatabricksGenAIResponseError(f'Checkpoints could not be retrieved for {training_run}') from e

    # Convert FileInfo objects to a list of paths (Composer checkpoints only)
    paths = [f.path for f in artifacts if os.path.basename(f.path).startswith(COMPOSER_CKPT_PREFIX)]
    # Join relative paths with the save_folder path to get the full checkpoint paths
    # TODO: Once MCLOUD-4934 is addressed, the following line can be removed
    training_run.save_folder = (training_run.save_folder.format(mlflow_experiment_id=training_run.experiment_id,
                                                                mlflow_run_id=training_run.run_id))
    paths = [os.path.join(training_run.save_folder, path) for path in paths]

    if len(paths) == 0:
        print('No checkpoints created yet for this run. Please try again later.')

    return paths
