"""
A Databricks training run
"""

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin

import mlflow
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.utils.utils_string_functions import camel_case_to_snake_case

from databricks.model_training.api.engine.engine import MAPIException
from databricks.model_training.api.utils import _get_host_and_token_from_env, is_running_in_databricks_notebook
from databricks.model_training.types.run_status import RunStatus
from databricks.model_training.types.train_config import TrainConfig

PROGRESS = [
    '□□□□□□□□□□', '■□□□□□□□□□', '■■□□□□□□□□', '■■■□□□□□□□', '■■■■□□□□□□', '■■■■■□□□□□', '■■■■■■□□□□', '■■■■■■■□□□',
    '■■■■■■■■□□', '■■■■■■■■■□', '■■■■■■■■■■'
]

_MLFLOW_CLIENT = mlflow.MlflowClient(tracking_uri='databricks', registry_uri='databricks-uc')


def seconds_to_str(seconds: Union[int, float]) -> str:
    """Converts seconds to a human-readable string

    Args:
        seconds: Number of seconds

    Returns:
        Human-readable string
    """
    if seconds < 60:
        return f'{int(seconds)}s'
    elif seconds < 3600:
        return f'{int(seconds/60)}min'
    elif seconds < 24 * 3600:
        return f'{int(seconds/3600)}hr'
    else:
        return f'{int(seconds/3600/24)}d'


@dataclass()
class TrainingEvent(DeserializableModel):
    """ Finetuning Run Event """
    type: str
    time: datetime
    message: str

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> 'TrainingEvent':
        """Load the formatted run event from MAPI response.
        """
        args = {camel_case_to_snake_case(key): value for key, value in response.items()}
        return cls(
            type=args['event_type'],
            time=args['event_time'],
            message=args['event_message'],
        )

    def is_terminal_state(self):
        return self.type in ['COMPLETED', 'FAILED', 'STOPPED', 'CANCELED']


@dataclass()
class TrainingRun(DeserializableModel):
    """A Databricks training run

    Args:
        name: The name of the training run
        created_by: The user email of who created the run
        model: The model to finetune
        train_data_path: The path to the training data
        register_to: The location to the registered model
        submitted_experiment_path: The submitted MLflow experiment path
        task_type: The type of training task to run
        eval_data_path: The path to the eval data
        eval_prompts: The list of prompts to use for eval
        custom_weights_path: The path to a custom model checkpoint to use for training
        training_duration: The total duration of the training run
        learning_rate: The peak learning rate to use for training
        context_length: The maximum sequence length to use
        data_prep_cluster_id: The id of the cluster used for data prep
        created_at: The time the run was created
        started_at: The time the run was started
        estimated_end_time: The estimated time the run will complete
        completed_at: The time the run was completed
        details: The current run event
    """

    name: str
    status: RunStatus
    created_by: str

    # User inputs
    model: Optional[str] = None
    save_folder: Optional[str] = None
    train_data_path: Optional[str] = None
    register_to: Optional[str] = None
    submitted_experiment_path: Optional[str] = None
    task_type: Optional[str] = 'INSTRUCTION_FINETUNE'
    eval_data_path: Optional[str] = None
    eval_prompts: Optional[List[str]] = None
    custom_weights_path: Optional[str] = None
    training_duration: Optional[str] = None
    learning_rate: Optional[float] = None
    context_length: Optional[int] = None
    # we do not include validate_inputs as this is not sent to MAPI nor stored anywhere
    data_prep_cluster_id: Optional[str] = None

    # holds the current run event
    details: Optional[str] = None

    # Lifecycle
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    estimated_end_time: Optional[datetime] = None
    formatted_eta: Optional[str] = None
    completed_at: Optional[datetime] = None

    # pylint: disable-next=import-outside-toplevel,cyclic-import
    from databricks.model_training.types.common import ObjectList

    # Details
    submitted_config: Optional[TrainConfig] = None
    events: Optional[ObjectList[TrainingEvent]] = None

    # MLflow
    experiment_id: Optional[str] = None
    run_id: Optional[str] = None

    _required_properties: Tuple[str, ...] = tuple([
        'id',
        'name',
        'status',
        'createdByEmail',
        'createdAt',
        'updatedAt',
    ])

    @property
    def run_progress(self) -> str:
        if self.status == RunStatus.RUNNING and self.started_at is not None and self.estimated_end_time is not None:
            total_time = (self.estimated_end_time - self.started_at).total_seconds()
            elapsed_time = (datetime.now(timezone.utc) - self.started_at).total_seconds()
            percentage = min(int((elapsed_time / total_time) * 100), 100)
            return f'{RunStatus.RUNNING} {PROGRESS[int(percentage / 10)]}({percentage}%)'
        return f'{self.status}'

    @property
    def formatted_events(self) -> str:
        return '' if self.events is None else '<br>'.join(
            ['<nobr>' + event.type + ' ' + str(event.time) + '</nobr>' for event in self.events])

    # hyperparameters: Hyperparameters ## todo

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> 'TrainingRun':
        """Load the training run from MAPI response.
        """
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message='Missing required key(s) in response to deserialize TrainingRun '
                f'object: {", ".join(missing)} ',
            )
        started_at = convert_datetime(response['startedAt']) if response.get('startedAt', None) else None
        completed_at = convert_datetime(response['completedAt']) if response.get('completedAt', None) else None
        estimated_end_time = convert_datetime(response['estimatedEndTime']) if response.get('estimatedEndTime',
                                                                                            None) else None

        args = {
            'name': response['name'],
            'created_at': convert_datetime(response['createdAt']),
            'started_at': started_at,
            'completed_at': completed_at,
            'status': RunStatus.from_string(response['status']),
            'details': response.get('reason', ''),
            'created_by': response['createdByEmail'],
            'estimated_end_time': estimated_end_time
        }

        if estimated_end_time is not None:
            args['estimated_end_time'] = estimated_end_time

        details = response.get('details', {})
        if len(details) > 0:
            args['model'] = details.get('model')
            args['save_folder'] = details.get('saveFolder')
            args['train_data_path'] = details.get('trainDataPath')
            args['eval_data_path'] = details.get('evalDataPath')
            args['eval_prompts'] = details.get('evalPrompts')
            args['custom_weights_path'] = details.get('customWeightsPath')
            args['training_duration'] = details.get('trainingDuration')
            args['learning_rate'] = details.get('learningRate')
            args['context_length'] = details.get('contextLength')
            experiment_tracker = details.get('experimentTracker')
            if experiment_tracker is None or experiment_tracker.get('mlflow') is None:
                raise MAPIException(
                    status=HTTPStatus.NOT_FOUND,
                    message=
                    'Missing MLflow experimentTracker, which is a required field to deserialize TrainingRun object',
                )
            mlflow_config = experiment_tracker.get('mlflow')
            args['register_to'] = mlflow_config.get('modelRegistryPath')
            args['submitted_experiment_path'] = mlflow_config.get('experimentPath')
            args['experiment_id'] = mlflow_config.get('mlflowExperimentId')
            args['run_id'] = mlflow_config.get('mlflowRunId')
            args['task_type'] = details.get('taskType')

            config_copy = deepcopy(details)
            # Remove events from details to keep only config properties
            if 'formattedFinetuningEvents' in config_copy:
                del config_copy['formattedFinetuningEvents']

            if 'dataPrepConfig' in config_copy:
                if 'clusterId' in config_copy['dataPrepConfig']:
                    args['data_prep_cluster_id'] = config_copy['dataPrepConfig']['clusterId']
                del config_copy['dataPrepConfig']
            args['submitted_config'] = TrainConfig.from_mapi_response(config_copy)

            formatted_training_events = sorted(
                [TrainingEvent.from_mapi_response(event) for event in details.get('formattedFinetuningEvents', [])],
                key=lambda x: x.time)

            # pylint: disable-next=import-outside-toplevel,cyclic-import
            from databricks.model_training.types.common import ObjectList, ObjectType

            # convert to ObjectList for better rendering when field referenced
            args['events'] = ObjectList(formatted_training_events, ObjectType.from_model_type(TrainingEvent))
            # Don't show ETA during checkpoint upload
            if args['estimated_end_time'] is not None:
                found = next((event for event in args['events'] if event.type == 'TRAIN_FINISHED'), None)
                if found is not None:
                    args['estimated_end_time'] = None

        if args['estimated_end_time'] is not None:
            time_left = (args['estimated_end_time'] - datetime.now(timezone.utc)).total_seconds()
            if time_left <= 0:
                args['estimated_end_time'] = None
            else:
                args['formatted_eta'] = seconds_to_str(time_left)

        return cls(**args)

    def refresh(self) -> 'TrainingRun':
        """Refetches the training run from the API

        Returns:
            TrainingRun: The updated training run
        """

        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from databricks.model_training.api.foundation_model.get import get
        return get(self)

    def cancel(self) -> int:
        """Cancel the training run

        Returns:
            int: Will return 1 if the run was cancelled, 0 if it was already cancelled
        """

        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from databricks.model_training.api.foundation_model.cancel import cancel
        return cancel(self)

    def get_events(self) -> ObjectList[TrainingEvent]:
        """Get events for the training run

        Returns:
            List[TrainingEvent]: A list of training run events. Each event has an event
                type, time, and message.
        """

        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from databricks.model_training.api.foundation_model.get_events import get_events
        return get_events(self)

    def _repr_html_(self) -> str:
        """Display the event as HTML.
        """

        keys = [
            'name', 'status', 'details', 'formatted_events', 'model', 'task_type', 'learning_rate', 'training_duration',
            'train_data_path', 'eval_data_path', 'register_to', 'experiment_id', 'eval_prompts', 'custom_weights_path',
            'data_prep_cluster_id'
        ]

        attr_to_label = {key: ' '.join([word.title() for word in key.split('_')]) for key in keys}
        # If the experiment_id or run_id isn't set, we can't display the full path to the MLflow run.
        # These experiment and path fields are mutable, so we can't rely on them to be the same as when
        # the run was created.
        if self.experiment_id is None or self.run_id is None:
            attr_to_label['submitted_experiment_path'] = 'MLflow Experiment'
        else:
            attr_to_label['_get_mlflow_path_html_with_link'] = 'MLflow Run'
        # override title for events
        attr_to_label['formatted_events'] = 'Events'

        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from databricks.model_training.types.common import generate_vertical_html_table
        return generate_vertical_html_table([self], attr_to_label)

    @property
    def experiment_path(self) -> str:
        """
        Get the experiment path for this run, not including run name (i.e. `/Users/username/experiment_name`).
        This uses the `experiment_id` attribute to get the latest experiment name, since experiment names
        are mutable.

        For runs created before 04/29/24, experiment id is not populated, so this returns the submitted experiment path.
        """
        if not self.experiment_id:
            if self.submitted_experiment_path is None:
                raise ValueError('Experiment ID and path are not set')
            return self.submitted_experiment_path
        return _MLFLOW_CLIENT.get_experiment(experiment_id=self.experiment_id).name

    # This is a property so that we can use `getattr`` with this in `generate_vertical_html_table`
    @property
    def _get_mlflow_path_html_with_link(self) -> str:
        """
        Get HTML for a link to the MLflow run page for this run.

        Only supported for TrainingRuns that have an experiment ID and run ID.
        """
        if not self.run_id or not self.experiment_id:
            raise ValueError('Run ID or Experiment ID is not set. ')
        run_name = _MLFLOW_CLIENT.get_run(run_id=self.run_id).info.run_name
        return self._get_mlflow_run_link_html(link_text=f'{self.experiment_path}/{run_name}')

    def _get_mlflow_message_html(self, num_runs: int = 1) -> str:
        """
        Get HTML for a message to display the MLflow run and experiment attributed to this run in the format:
        "Logged a run to an experiment in MLflow." with links to the run and experiment

        Also prints the experiment ID for easy cancellation/deletion.

        For older runs that do not have an experiment ID and run ID, this returns a message with the submitted
        experiment path and no links.
        """
        if self.experiment_id is None:
            raise ValueError('Experiment ID is not set')
        if not self.run_id or not self.experiment_id:
            return f'Logged to {self.submitted_experiment_path}'
        copyable_experiment_id = self._get_copyable_experiment_id_html(self.experiment_id)
        if num_runs > 1:
            return f'Logged {num_runs} runs to an {self._get_mlflow_experiment_link_html("experiment")} in MLflow. ' \
                f'Experiment ID: {copyable_experiment_id}'
        return f'Logged a {self._get_mlflow_run_link_html("run")} to an ' \
            f'{self._get_mlflow_experiment_link_html("experiment")} in MLflow. Experiment ID: {copyable_experiment_id}'

    def _get_mlflow_experiment_link_html(self, link_text: str = 'experiment') -> str:
        """
        Get a link for the MLflow experiment using the given link text.
        This link will open the MLflow experiment page in a new tab.

        Raises:
            ValueError: If the experiment ID is not set
        """
        if self.experiment_id is None:
            raise ValueError('Experiment ID is not set')
        if is_running_in_databricks_notebook():
            host = ''
        else:
            host, _ = _get_host_and_token_from_env()
        path = urljoin(host, f'/ml/experiments/{self.experiment_id}')
        return f"<a href={path} class target='_blank'>{link_text}</a>"

    def _get_mlflow_run_link_html(self, link_text: str = 'run') -> str:
        """
        Get a link for the MLflow run using the given link text. This link will open the MLflow run page in a new tab.

        Raises:
            ValueError: If the run ID or experiment ID is not set
        """
        if self.run_id is None or self.experiment_id is None:
            raise ValueError('Run ID or Experiment ID is not set')
        if is_running_in_databricks_notebook():
            host = ''
        else:
            host, _ = _get_host_and_token_from_env()
        path = urljoin(host, f'/ml/experiments/{self.experiment_id}/runs/{self.run_id}')
        return f"<a href={path} class target='_blank'>{link_text}</a>"

    def _get_copyable_experiment_id_html(self, experiment_id: str) -> str:
        """
        Generate HTML for a read-only input field that contains the experiment ID.
        This allows the experiment ID to be easily copied.
        """
        return f'<input type="text" value="{experiment_id}"' \
            'readonly="readonly" style="border:none;background:none;cursor:pointer;" onclick="this.select();">'
