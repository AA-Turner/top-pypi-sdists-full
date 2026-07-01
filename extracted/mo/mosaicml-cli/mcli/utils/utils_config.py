"""Utils for modifying MCLI Configs"""
import copy
import logging
import warnings
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

import yaml
from typing_extensions import TypedDict

from mcli.api.exceptions import ValidationError
from mcli.utils.utils_logging import str_presenter
from mcli.utils.utils_string_functions import camel_case_to_snake_case, snake_case_to_camel_case
from mcli.utils.utils_yaml import load_yaml

logger = logging.getLogger(__name__)


def strip_nones(d: Dict[str, Any]) -> Dict[str, Any]:
    """Remove all keys with None values from a dictionary"""
    return {k: v for k, v in d.items() if v is not None}


class SchedulingConfig(TypedDict, total=False):
    """Typed dictionary for nested scheduling configurations"""
    priority: Optional[str]
    resumable: Optional[bool]  # TODO: deprecate resumable
    preemptible: Optional[bool]
    retryOnSystemFailure: Optional[bool]
    max_retries: Optional[int]
    retry_on_system_failure: Optional[bool]
    max_duration: Optional[float]


class ComputeConfig(TypedDict, total=False):
    """Typed dictionary for nested compute requests"""
    cluster: Optional[str]
    instance: Optional[str]
    nodes: Optional[int]
    node_names: Optional[List[str]]
    gpu_type: Optional[str]
    gpus: Optional[int]
    cpus: Optional[int]


class MLflowConfig(TypedDict, total=False):
    """Typed dictionary for nested MLflow configs"""
    tracking_uri: Optional[str]
    experiment_path: str
    model_registry_path: Optional[str]


class WandbConfig(TypedDict, total=True):
    """Typed dictionary for nested W&B configs"""
    project: str
    entity: str


class ExperimentTrackerConfig(TypedDict, total=False):
    """Typed dictionary for nested experiment tracker configs"""
    mlflow: Optional[MLflowConfig]
    wandb: Optional[WandbConfig]


@dataclass
class BaseSubmissionConfig():
    """ Base class for config objects"""

    _required_display_properties = set()

    @classmethod
    def empty(cls):
        return cls()

    @classmethod
    def from_file(cls, path: Union[str, Path]):
        """Load the config from the provided YAML file.
        Args:
            path (Union[str, Path]): Path to YAML file
        Returns:
            BaseSubmissionConfig: The BaseSubmissionConfig object specified in the YAML file
        """
        config = load_yaml(path)
        return cls.from_dict(config, show_unused_warning=True)

    def to_file(self, path: Union[str, Path]):
        """Save the config to the provided YAML file.
        Args:
            path (Union[str, Path]): Path to YAML file
        """
        with open(path, 'w', encoding='utf8') as f:
            f.write(str(self))

    @classmethod
    def from_dict(cls, dict_to_use: Dict[str, Any], show_unused_warning: bool = False):
        """Load the config from the provided dictionary.
        Args:
            dict_to_use (Dict[str, Any]): The dictionary to populate the BaseSubmissionConfig with
        Returns:
            BaseSubmissionConfig: The BaseSubmissionConfig object specified in the dictionary
        """
        field_names = list(map(lambda x: x.name, fields(cls)))

        unused_keys = []
        constructor = {}

        for key, value in dict_to_use.items():
            if key in field_names:
                constructor[key] = value
            else:
                unused_keys.append(key)

        if len(unused_keys) > 0 and show_unused_warning:
            # pylint: disable=line-too-long
            warnings.warn(
                f'! Encountered unknown fields {", ".join(unused_keys)} which were not used in creating the request')

        return cls(**constructor)

    def __str__(self) -> str:
        filtered_dict = {}
        for k, v in asdict(self).items():
            # skip nested and direct empty values for optional properties
            if k not in self._required_display_properties:
                if isinstance(v, dict) and not any(v.values()):
                    continue
                if not v:
                    continue
            filtered_dict[k] = v
        # to use with safe_dump:
        yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

        return yaml.safe_dump(filtered_dict, default_flow_style=False, sort_keys=False).strip()


T = TypeVar('T')  # pylint: disable=invalid-name
U = TypeVar('U')


class Translation(ABC, Generic[T, U]):
    """ABC for MAPI/MCLI translations"""

    @classmethod
    @abstractmethod
    def to_mapi(cls, value: T) -> U:
        ...

    @classmethod
    @abstractmethod
    def from_mapi(cls, value: U) -> T:
        ...


class EnvVarTranslation:
    """Translate environment variable configs"""

    MAPI_KEY = 'envKey'
    MAPI_VALUE = 'envValue'

    @classmethod
    def to_mapi(cls, value: Dict[str, str]) -> List[Dict[str, str]]:
        return [{cls.MAPI_KEY: key, cls.MAPI_VALUE: val} for key, val in value.items()]

    @classmethod
    def from_mapi(cls, value: List[Dict[str, str]]) -> Dict[str, str]:
        env_vars = {}
        for env_var in value:
            try:
                key = env_var[cls.MAPI_KEY]
                val = env_var[cls.MAPI_VALUE]
            except KeyError:
                logger.warning(f'Received incompatible environment variable: {env_var}')
                continue
            env_vars[key] = val
        return env_vars


class IntegrationTranslation(Translation[List[Dict[str, Any]], List[Dict[str, Any]]]):
    """Translate integration configs"""

    MAPI_TYPE = 'type'
    MAPI_PARAMS = 'params'

    MCLI_TYPE = 'integration_type'

    @classmethod
    def to_mapi(cls, value: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        value = copy.deepcopy(value)
        integrations_list = []
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise ValidationError(f'Integrations input must be a list of dictionary, received: {value}')
        for integration in value:
            if cls.MCLI_TYPE not in integration and cls.MAPI_TYPE not in integration:
                raise ValidationError(f'Integration missing required key: {cls.MCLI_TYPE}, received {integration}')
            elif cls.MAPI_TYPE in integration:
                integration_type = integration.pop(cls.MAPI_TYPE)
            else:
                integration_type = integration.pop(cls.MCLI_TYPE)
            translated_integration = {}
            for param, val in integration.items():
                # Translate keys to camel case for MAPI parameters
                translated_key = snake_case_to_camel_case(param)
                translated_integration[translated_key] = val

            integrations_dict = {cls.MAPI_TYPE: integration_type, cls.MAPI_PARAMS: translated_integration}
            integrations_list.append(integrations_dict)
        return integrations_list

    @classmethod
    def from_mapi(cls, value: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        integrations_list = []
        for integration in value:
            translated_integration = {cls.MCLI_TYPE: integration[cls.MAPI_TYPE]}
            params = integration.get(cls.MAPI_PARAMS, {})
            for param, val in params.items():
                # Translate keys to camel case for MAPI parameters
                translated_key = camel_case_to_snake_case(param)
                translated_integration[translated_key] = val

            integrations_list.append(translated_integration)
        return integrations_list


class ComputeTranslation(Translation[ComputeConfig, Dict[str, Any]]):
    """Translate compute configs to and from MAPI"""

    translations = {
        "gpuType": "gpu_type",
        "nodeNames": "node_names",
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> ComputeConfig:
        extracted = ComputeConfig(**{cls.translations.get(k, k): v for k, v in value.items()})
        return extracted

    @classmethod
    def to_mapi(cls, value: ComputeConfig) -> Dict[str, Any]:
        inv = {v: k for k, v in cls.translations.items()}
        processed = {inv.get(k, k): v for k, v in value.items() if v is not None}
        return processed


class SchedulingTranslation(Translation[SchedulingConfig, Dict[str, Any]]):
    """Translate scheduling configs to and from MAPI"""

    translations = {
        "maxRetries": "max_retries",
        "retryOnSystemFailure": "retry_on_system_failure",
        "maxDuration": "max_duration"
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> SchedulingConfig:
        extracted = SchedulingConfig(**{cls.translations.get(k, k): v for k, v in value.items() if k != "priorityInt"})
        return extracted

    @classmethod
    def to_mapi(cls, value: SchedulingConfig) -> Dict[str, Any]:
        inv = {v: k for k, v in cls.translations.items()}
        processed = {inv.get(k, k): v for k, v in value.items() if v is not None}
        return processed


class DependentDeploymentConfig(Translation, Generic[T]):
    """Basic translation for dependent deployment configs"""

    @classmethod
    def to_mapi(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        translated_config = {}
        for key, val in value.items():
            if key == 'env_variables':
                val = EnvVarTranslation.to_mapi(val)
            elif isinstance(val, dict):
                # This purposefully goes 2 levels deep and not further
                # due to how the inference server expects the config
                new_dict = {}
                for k, v in val.items():
                    new_dict[snake_case_to_camel_case(k)] = v
                val = new_dict
            mapi_key = snake_case_to_camel_case(key)
            translated_config[mapi_key] = val
        return translated_config

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> Dict[str, Any]:
        translated_config = {}
        for key, val in value.items():
            if key == 'envVariables':
                val = EnvVarTranslation.from_mapi(val)
            elif isinstance(val, dict):
                new_dict = {}
                for k, v in val.items():
                    new_dict[camel_case_to_snake_case(k)] = v
                val = new_dict
            mapi_key = camel_case_to_snake_case(key)
            translated_config[mapi_key] = val
        return translated_config


class ExperimentTrackerTranslation(Translation[ExperimentTrackerConfig, Dict[str, Any]]):
    """Translate scheduling configs to and from MAPI"""

    translations = {
        "mlflow": {
            'trackingUri': 'tracking_uri',
            'experimentPath': 'experiment_path',
            'modelRegistryPath': 'model_registry_path'
        },
        "wandb": {
            'project': 'project',
            'entity': 'entity'
        }
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> ExperimentTrackerConfig:
        extracted = ExperimentTrackerConfig()
        for tracker_name, tracker_config in value.items():
            extracted[tracker_name] = {
                cls.translations.get(tracker_name, {}).get(k, k): v for k, v in dict(tracker_config).items()
            }
        return extracted

    @classmethod
    def to_mapi(cls, value: ExperimentTrackerConfig) -> Dict[str, Any]:
        out = {}
        for tracker_name, tracker_config in value.items():
            inv = {v: k for k, v in cls.translations.get(tracker_name, {}).items()}
            assert isinstance(tracker_config, dict)
            out[tracker_name] = {inv.get(k, k): v for k, v in tracker_config.items() if v is not None}
        return out
