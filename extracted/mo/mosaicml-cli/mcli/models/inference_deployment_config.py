""" Deployment Input """
from __future__ import annotations

import logging
import warnings
from dataclasses import asdict, dataclass, field
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import yaml
from typing_extensions import TypedDict

from mcli.api.exceptions import MAPIException, MCLIDeploymentConfigValidationError
from mcli.api.schema.generic_model import DeserializableModel
from mcli.utils.utils_config import (BaseSubmissionConfig, ComputeConfig, ComputeTranslation, EnvVarTranslation,
                                     IntegrationTranslation, Translation)
from mcli.utils.utils_string_functions import (camel_case_to_snake_case, clean_run_name, snake_case_to_camel_case,
                                               validate_image)

logger = logging.getLogger(__name__)


class ModelConfig(TypedDict, total=False):
    """Typed dictionary for model configs"""
    downloader: str
    download_parameters: Dict[str, str]
    model_handler: str
    model_parameters: Dict[str, str]
    backend: Optional[str]


class DefaultModelConfig(TypedDict, total=False):
    """Typed dictionary for default model configs"""
    model_type: str
    checkpoint_path: Dict[str, str]


class BatchingConfig(TypedDict, total=False):
    """Typed dictionary for model configs"""
    max_batch_size: int
    max_timeout_ms: int
    max_batch_size_in_bytes: int


@dataclass
class FinalInferenceDeploymentConfig(DeserializableModel):
    """A finalized deployment configuration
    This configuration must be complete, with enough details to submit a new deployment to the
    MosaicML Cloud.
    """

    name: str
    replicas: int
    env_variables: Dict[str, str] = field(default_factory=dict)
    integrations: List[Dict[str, Any]] = field(default_factory=list)

    metadata: Dict[str, Any] = field(default_factory=dict)

    batching: BatchingConfig = field(default_factory=BatchingConfig)
    compute: ComputeConfig = field(default_factory=ComputeConfig)
    rate_limit: Optional[int] = None

    # Model config - optional for backwards-compatibility
    model: Optional[ModelConfig] = None
    default_model: Optional[DefaultModelConfig] = None

    gpu_num: Optional[int] = None
    gpu_type: Optional[str] = None
    image: str = ''
    command: str = ''

    cluster: str = ''

    _property_translations = {
        'deploymentName': 'name',
        'gpuType': 'gpu_type',
        'gpuNum': 'gpu_num',
        'cluster': 'cluster',
        'image': 'image',
        'command': 'command',
        'replicas': 'replicas',
        'metadata': 'metadata',
        'envVariables': 'env_variables',
        'integrations': 'integrations',
        'model': 'model',
        'defaultModel': 'default_model',
        'batching': 'batching',
        'compute': 'compute',
        'rateLimit': 'rate_limit'
    }

    # Backwards Compatibility
    _optional_properties = {
        'metadata', 'envVariables', 'integrations', 'model', 'defaultModel', 'compute', 'batching', 'rateLimit'
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FinalInferenceDeploymentConfig:
        missing = set(cls._property_translations) - set(response) - cls._optional_properties
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=('Missing required key(s) in response to deserialize '
                         f'FinalDeploymentConfig object: {", ".join(missing)}'),
            )
        data = {}
        for k, v in cls._property_translations.items():
            if k not in response:
                # This must be an optional property, so skip
                continue
            value = response[k]
            if v == 'env_variables':
                value = EnvVarTranslation.from_mapi(value)
            elif v == 'integrations':
                value = IntegrationTranslation.from_mapi(value)
            elif value and v == 'model':
                value = InferenceModelTranslation.from_mapi(value)
            elif value and v == 'default_model':
                value = InferenceDefaultModelTranslation.from_mapi(value)
            elif v == 'batching':
                value = BatchingConfigTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeTranslation.from_mapi(value)
            data[v] = value

        return cls(**data)

    @classmethod
    def finalize_config(cls, deployment_config: InferenceDeploymentConfig) -> FinalInferenceDeploymentConfig:
        """Create a :class:`~mcli.models.deployment_config.FinalDeploymentConfig` from the provided
        :class:`~mcli.models.deployment_config.DeploymentConfig`.
        If the :class:`~mcli.models.deployment_config.DeploymentConfig` is not fully populated then
        this function fails with an error.
        Args:
            deployment_config (:class:`~mcli.models.deployment_config.DeploymentConfig`): The DeploymentConfig
            to finalize
        Returns:
            :class:`~mcli.models.deployment_config.FinalDeploymentConfig`:The object created using values from the input
        Raises:
            :class:`~mcli.api.exceptions.MCLIConfigError`: If MCLI config is not present or is missing information
            :class:`~mcli.api.exceptions.MCLIDeploymentConfigValidationError`: If deployment_config is not valid
        """

        model_as_dict = asdict(deployment_config)

        missing_fields = [field for field, value in model_as_dict.items() if value is None]
        for missing in missing_fields:
            model_as_dict.pop(missing, None)

        # required for FinalDeploymentConfig, even though not required for mcloud

        if not model_as_dict.get("replicas"):
            model_as_dict["replicas"] = 1

        if not model_as_dict.get("metadata"):
            model_as_dict["metadata"] = {}

        # Fill in default initial values for FinalDeploymentConfig
        model_as_dict['name'] = clean_run_name(model_as_dict.get('name'))

        if isinstance(model_as_dict.get('gpu_type'), int):
            model_as_dict['gpu_type'] = str(model_as_dict['gpu_type'])

        if isinstance(model_as_dict.get('env_variables'), list):
            model_as_dict['env_variables'] = {var['key']: var['value'] for var in model_as_dict['env_variables']}
            warnings.warn('Support for passing env_variables as a list will soon be deprecated. ' +
                          f'Please use a dict instead, eg: {model_as_dict["env_variables"]}')

        image = model_as_dict.get('image')
        if image and not validate_image(image):
            raise MCLIDeploymentConfigValidationError(f'The image name "{model_as_dict["image"]}" is not valid')

        return cls(**model_as_dict)

    def to_create_deployment_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Convert a deployment configuration to a proper JSON to pass to MAPI's createDeployment
        Returns:
            Dict[str, Dict[str, Any]]: The deployment configuration as a MAPI deploymentInput JSON
        """
        translations = {v: k for k, v in self._property_translations.items()}

        translated_input = {}
        for field_name, value in asdict(self).items():
            translated_name = translations.get(field_name, field_name)
            if value is None:
                continue
            if field_name == 'env_variables':
                value = EnvVarTranslation.to_mapi(value)
            elif field_name == 'integrations':
                value = IntegrationTranslation.to_mapi(value)
            elif field_name == 'model':
                value = InferenceModelTranslation.to_mapi(value)
            elif field_name == 'default_model':
                value = InferenceDefaultModelTranslation.to_mapi(value)
            elif field_name == "compute":
                value = ComputeTranslation.to_mapi(value)
            elif field_name == "batching":
                value = BatchingConfigTranslation.to_mapi(value)
            elif field_name in ("image", "gpu_type", "cluster") and not value:
                continue  # optional field
            translated_input[translated_name] = value
        return {
            'inferenceDeploymentInput': translated_input,
        }


@dataclass
class InferenceDeploymentConfig(BaseSubmissionConfig):
    """A deployment configuration for the MosaicML Cloud

    Values in here are not yet validated and some required values may be missing.

    Args:
        name (`Optional[str]`): User-defined name of the deployment
        gpu_type (`Optional[str]`): GPU type (optional if only one gpu type for your cluster)
        gpu_num (`Optional[int]`): Number of GPUs
        image (`Optional[str]`): Docker image (e.g. `mosaicml/composer`)
        command (`str`): Command to use when a deployment starts
        env_variables (`Dict[str, str]`): Dict of environment variables
        integrations (`List[Dict[str, Any]]`): List of integrations
        compute (`ComputeConfig`): The compute to use for the inference deployment.
        replicas (`Optional[int]`): Number of replicas to create
        batching (`BatchingConfig`): The dynamic batching configuration.
        cluster (`Optional[str]`): Deprecated. Cluster to use (optional if you only have one)
    """
    name: Optional[str] = None
    gpu_type: Optional[str] = None
    gpu_num: Optional[int] = None
    cluster: Optional[str] = None
    image: Optional[str] = None
    replicas: Optional[int] = None
    command: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    env_variables: Union[Dict[str, str], List[Dict[str, str]]] = field(default_factory=dict)
    integrations: List[Dict[str, Any]] = field(default_factory=list)
    model: Optional[ModelConfig] = None
    default_model: Optional[DefaultModelConfig] = None
    batching: BatchingConfig = field(default_factory=BatchingConfig)
    compute: ComputeConfig = field(default_factory=ComputeConfig)
    rate_limit: Optional[int] = None

    _property_translations = {
        'deploymentName': 'name',
        'gpuNum': 'gpu_num',
        'cluster': 'cluster',
        'image': 'image',
        'command': 'command',
        'replicas': 'replicas',
        'metadata': 'metadata',
        'envVariables': 'env_variables',
        'integrations': 'integrations',
        'model': 'model',
        'defaultModel': 'default_model',
        'batching': 'batching',
        'compute': 'compute',
        'rateLimit': 'rate_limit',
    }

    _required_display_properties = {'name', 'image', 'command', 'replicas'}

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> InferenceDeploymentConfig:
        data = {}
        for k, v in cls._property_translations.items():
            if k not in response:
                # This must be an optional property, so skip
                continue
            value = response[k]
            if v == 'env_variables':
                value = EnvVarTranslation.from_mapi(value)
            elif v == 'integrations':
                value = IntegrationTranslation.from_mapi(value)
            elif value and v == 'model':
                value = InferenceModelTranslation.from_mapi(value)
            elif value and v == 'default_model':
                value = InferenceDefaultModelTranslation.from_mapi(value)
            elif v == 'batching':
                value = BatchingConfigTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeConfig(**value)
            data[v] = value

        return_val = cls(**data)
        return return_val

    def __post_init__(self):
        if isinstance(self.env_variables, list):
            self.env_variables = {var['key']: var['value'] for var in self.env_variables}
            warnings.warn('Support for passing env_variables as a list will soon be deprecated. ' +
                          f'Please use a dict instead, eg: {self.env_variables}')


class InferenceModelTranslation(Translation[ModelConfig, Dict[str, Any]]):
    """Translate model configs to and from MAPI"""

    _property_translations = {
        'downloader': 'downloader',
        'download_parameters': 'downloadParameters',
        'model_handler': 'modelHandler',
        'model_parameters': 'modelParameters',
        'backend': 'backend',
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> ModelConfig:
        translated_config = {}
        for mcli_key, mapi_key in cls._property_translations.items():
            translated_config[mcli_key] = value.get(mapi_key)

        return ModelConfig(**translated_config)

    @classmethod
    def to_mapi(cls, value: ModelConfig) -> Dict[str, Any]:
        translated_config = {}
        for mcli_key, val in value.items():
            mapi_key = cls._property_translations.get(mcli_key)
            translated_config[mapi_key] = val

        return translated_config


class InferenceDefaultModelTranslation(Translation[DefaultModelConfig, Dict[str, Any]]):
    """Translate default model configs to and from MAPI"""

    _property_translations = {
        'model_type': 'modelType',
        'checkpoint_path': 'checkpointPath',
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> DefaultModelConfig:
        translated_config = {}
        for mcli_key, mapi_key in cls._property_translations.items():
            val = value.get(mapi_key)
            if isinstance(val, dict):
                val = {camel_case_to_snake_case(k): v for k, v in val.items()}
            translated_config[mcli_key] = val

        return DefaultModelConfig(**translated_config)

    @classmethod
    def to_mapi(cls, value: DefaultModelConfig) -> Dict[str, Any]:
        translated_config = {}
        for mcli_key, val in value.items():
            if isinstance(val, dict):
                val = {snake_case_to_camel_case(k): v for k, v in val.items()}
            mapi_key = cls._property_translations.get(mcli_key)
            translated_config[mapi_key] = val

        return translated_config


class BatchingConfigTranslation(Translation[BatchingConfig, Dict[str, Any]]):
    """Translate batching configs to and from MAPI"""

    _property_translations = {
        'max_batch_size': 'maxBatchSize',
        'max_timeout_ms': 'maxTimeoutMs',
        'max_batch_size_in_bytes': 'maxBatchSizeInBytes',
        'max_queue_size': 'maxQueueSize'
    }

    @classmethod
    def from_mapi(cls, value: Dict[str, Any]) -> BatchingConfig:
        translated_config = {}
        for mcli_key, mapi_key in cls._property_translations.items():
            translated_config[mcli_key] = value.get(mapi_key)

        return BatchingConfig(**translated_config)

    @classmethod
    def to_mapi(cls, value: BatchingConfig) -> Dict[str, Any]:
        translated_config = {}
        for mcli_key, val in value.items():
            mapi_key = cls._property_translations.get(mcli_key)
            translated_config[mapi_key] = val

        return translated_config
