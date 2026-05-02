""" Finetune config """
import logging
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

import yaml
from mcli.utils.utils_config import (BaseSubmissionConfig, ExperimentTrackerConfig, ExperimentTrackerTranslation,
                                     strip_nones)
from mcli.utils.utils_string_functions import camel_case_to_snake_case, snake_case_to_camel_case

from databricks.model_training.api.exceptions import DatabricksGenAIConfigError

logger = logging.getLogger(__name__)


class TrainTaskType(Enum):
    """ The Type of Finetune Task to run """
    INSTRUCTION_FINETUNE = 'INSTRUCTION_FINETUNE'
    CONTINUED_PRETRAIN = 'CONTINUED_PRETRAIN'
    CHAT_COMPLETION = 'CHAT_COMPLETION'


@dataclass
class TrainConfig(BaseSubmissionConfig):
    """Input for training run

    Args:
        model (str): Model to finetune (e.g. 'mosaicml/mpt-30b')
        task_type (str): Task type to finetune on
        train_data_path (str): HF dataset or remote path to training data
        save_folder (str): Folder to save checkpoints and HF checkpoints, currently must be an s3 or GCP path
        eval_data_path (Optional[str]): HF dataset or remote path to eval data
        eval_prompts (Optional[List[str]]): A list of prompt strings to generate from periodically during training
        custom_weights_path (Optional[str]): Remote location of custom weights to use for model training
        training_duration (str): Composer variable for the total number of epochs or tokens to train on
            (e.g. 2ep or 10000tok) [TO BE DEPRECATED]
        training_durations (Optional[List[str]]): List of epochs or tokens to train for
        experiment_tracker (Optional[ExperimentTrackerConfig]): Experiment tracker config
        learning_rate (Optional[float]): Learning rate to use [TO BE DEPRECATED]
        learning_rates (Optional[List[float]]): List of learning rates to use
        context_length (Optional[int]): Context length of the model. Override only works for MPT model families
        disable_credentials_check (Optional[bool]): Flag to disable checking credentials (S3, Databricks, etc.)
            on finetune submission
    """

    model: str
    train_data_path: str
    save_folder: str = 'dbfs:/databricks/mlflow-tracking/{mlflow_experiment_id}/{mlflow_run_id}/artifacts'
    task_type: Optional[str] = 'INSTRUCTION_FINETUNE'
    eval_data_path: Optional[str] = None
    eval_prompts: Optional[List[str]] = None
    custom_weights_path: Optional[str] = None
    training_duration: Optional[str] = None
    training_durations: Optional[List[str]] = None
    experiment_tracker: Optional[ExperimentTrackerConfig] = None
    learning_rate: Optional[float] = None
    learning_rates: Optional[List[float]] = None
    context_length: Optional[int] = None
    # The data prep config is an internal config passed to MAPI to define requirements for data transformation.
    # The SDK only minimally exposes the `data_prep_cluster_id` field to the user, which we will pack and unpack from
    # the `data_prep_config` automatically.
    data_prep_config: Optional[Dict] = None
    disable_credentials_check: Optional[bool] = None

    _required_properties = {'model', 'train_data_path', 'save_folder'}
    _finetune_properties = {
        'model', 'train_data_path', 'save_folder', 'eval_data_path', 'eval_prompts', 'custom_weights_path',
        'training_duration', 'training_durations', 'experiment_tracker', 'learning_rate', 'learning_rates',
        'context_length', 'task_type', 'data_prep_config', 'disable_credentials_check'
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def validate_dict(cls, dict_to_use: Dict, show_unused_warning: bool = True) -> Dict:
        """Load the config from the provided dictionary.
        """
        config_dict = strip_nones(dict_to_use)
        unused_keys = set(config_dict) - cls._finetune_properties
        for key in unused_keys:
            del config_dict[key]
        missing = cls._required_properties - set(dict_to_use)
        if missing:
            raise DatabricksGenAIConfigError(f'Missing required fields: {", ".join(missing)}',)
        if len(unused_keys) > 0 and show_unused_warning:
            raise DatabricksGenAIConfigError(
                f'Encountered unknown fields in training config: {", ".join(unused_keys)}.')
        return config_dict

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = True):
        """Load the config from the provided dictionary.
        """
        config_dict = cls.validate_dict(dict_to_use, show_unused_warning)
        return cls(**config_dict)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]):
        """Load the config from mapi response.
        """
        experiment_tracker_result = {}
        for key, value in response.items():
            if key == 'experimentTracker':
                experiment_tracker_result['experiment_tracker'] = ExperimentTrackerTranslation.from_mapi(value)
            else:
                experiment_tracker_result[camel_case_to_snake_case(key)] = value
        return cls.from_dict(experiment_tracker_result)

    def to_create_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Converts the TrainConfig object to Compute and Finetune that can be used to create a finetune run
        """
        finetune = {}
        config_dict = strip_nones(self.__dict__)
        for key, val in config_dict.items():
            if key == 'experiment_tracker':
                finetune['experimentTracker'] = ExperimentTrackerTranslation.to_mapi(val)
                continue
            translated_key = snake_case_to_camel_case(key)
            if key in self._finetune_properties:
                finetune[translated_key] = val

        return {'config': finetune}

    def to_yaml(self) -> str:
        """Converts the TrainConfig object to a yaml string with only used keys
        """
        filtered_config = {k: v for k, v in self.__dict__.items() if v}
        return yaml.safe_dump(filtered_config)

    def __post_init__(self):
        if self.task_type not in TrainTaskType.__members__:
            raise DatabricksGenAIConfigError(f'Invalid task_type: {self.task_type}, currently '
                                             f'supported options are: {", ".join([x.value for x in TrainTaskType])}')
