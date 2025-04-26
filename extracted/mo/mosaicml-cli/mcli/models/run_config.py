""" Run Input """
from __future__ import annotations

import difflib
import logging
import os
import warnings
from dataclasses import asdict, dataclass, field
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, get_type_hints

import yaml

from mcli.api.exceptions import MAPIException, MCLIRunConfigValidationError
from mcli.api.schema.generic_model import DeserializableModel
from mcli.utils.utils_config import (BaseSubmissionConfig, ComputeConfig, ComputeTranslation, DependentDeploymentConfig,
                                     EnvVarTranslation, IntegrationTranslation, SchedulingConfig, SchedulingTranslation,
                                     strip_nones)
from mcli.utils.utils_string_functions import clean_run_name, validate_image

logger = logging.getLogger(__name__)


@dataclass
class FinalRunConfig(DeserializableModel):
    """A finalized run configuration

    This configuration must be complete, with enough details to submit a new run to the
    MosaicML platform.
    """

    integrations: List[Dict[str, Any]]
    env_variables: Dict[str, str]
    parameters: Dict[str, Any]

    image: Optional[str] = None
    name: Optional[str] = None
    parent_name: Optional[str] = None

    cluster: str = ''  # deprecating, use compute['cluster']
    gpu_type: Optional[str] = None  # deprecating, use compute['gpu_type']
    gpu_num: Optional[int] = None  # deprecating, use compute['gpus']
    cpus: Optional[int] = None  # deprecating, use compute['cpus']

    command: str = ''

    # Scheduling parameters - optional for backwards-compatibility
    scheduling: SchedulingConfig = field(default_factory=SchedulingConfig)

    # Compute parameters - optional for backwards-compatibility
    compute: ComputeConfig = field(default_factory=ComputeConfig)

    # User defined metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    dependent_deployment: Dict[str, Any] = field(default_factory=dict)

    _property_translations = {
        'runName': 'name',
        'parentName': 'parent_name',
        'gpuType': 'gpu_type',
        'gpuNum': 'gpu_num',
        'cpus': 'cpus',
        'cluster': 'cluster',
        'image': 'image',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'scheduling': 'scheduling',
        'compute': 'compute',
        'metadata': 'metadata',
        'dependentDeployment': 'dependent_deployment',
    }

    _optional_properties = {
        'parentName',
        'scheduling',
        'compute',
        'metadata',
        'dependentDeployment',
    }

    def __str__(self) -> str:
        return yaml.safe_dump(asdict(self))

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FinalRunConfig:
        missing = set(cls._property_translations) - \
            set(response) - cls._optional_properties
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=
                f'Missing required key(s) in response to deserialize FinalRunConfig object: {", ".join(missing)}',
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
            elif v == 'scheduling':
                value = SchedulingTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeTranslation.from_mapi(value)
            data[v] = value

        return cls(**data)

    @classmethod
    def finalize_config(cls, run_config: RunConfig) -> FinalRunConfig:  # pylint: disable=too-many-statements
        """Create a :class:`~mcli.models.run_config.FinalRunConfig` from the provided
        :class:`~mcli.models.run_config.RunConfig`.

        If the :class:`~mcli.models.run_config.RunConfig` is not fully populated then
        this function fails with an error.

        Args:
            run_config (:class:`~mcli.models.run_config.RunConfig`): The RunConfig to finalize

        Returns:
            :class:`~mcli.models.run_config.FinalRunConfig`: The object created using values from the input

        Raises:
            :class:`~mcli.api.exceptions.MCLIConfigError`: If MCLI config is not present or is missing information
            :class:`~mcli.api.exceptions.MCLIRunConfigValidationError`: If run_config is not valid
        """
        if run_config.cpus is None:
            run_config.cpus = 0

        model_as_dict = asdict(run_config)
        model_as_dict = strip_nones(model_as_dict)

        # Fill in default initial values for FinalRunConfig
        if 'name' in model_as_dict:
            model_as_dict['name'] = clean_run_name(model_as_dict.get('name'))

        if isinstance(model_as_dict.get('gpu_type'), int):
            model_as_dict['gpu_type'] = str(model_as_dict['gpu_type'])

        if isinstance(model_as_dict.get('env_variables'), list):
            model_as_dict['env_variables'] = {var['key']: var['value'] for var in model_as_dict['env_variables']}
            warnings.warn('Support for passing env_variables as a list will soon be deprecated. ' +
                          f'Please use a dict instead, eg: {model_as_dict["env_variables"]}')

        image = model_as_dict.get('image')
        if not image:
            raise MCLIRunConfigValidationError('An image name must be provided using the keyword [bold]image[/]')
        elif not validate_image(image):
            raise MCLIRunConfigValidationError(f'The image name "{model_as_dict["image"]}" is not valid')

        return cls(**model_as_dict)

    def get_parent_name_from_env(self) -> Optional[str]:
        """Get the parent name from the environment

        Returns:
            Optional[str]: The parent name if it exists, otherwise None
        """
        inside_run = os.environ.get('MOSAICML_PLATFORM', 'false').lower() == 'true'
        if not inside_run:
            return None

        return os.environ.get('RUN_NAME')

    def to_create_run_api_input(self) -> Dict[str, Dict[str, Any]]:
        """Convert a run configuration to a proper JSON to pass to MAPI's createRun

        Returns:
            Dict[str, Dict[str, Any]]: The run configuration as a MAPI runInput JSON
        """
        translations = {v: k for k, v in self._property_translations.items()}

        translated_input = {}
        for field_name, value in asdict(self).items():
            if value is None:
                continue
            translated_name = translations.get(field_name, field_name)
            if field_name == 'env_variables':
                value = EnvVarTranslation.to_mapi(value)
            elif field_name == 'integrations':
                value = IntegrationTranslation.to_mapi(value)
            elif field_name == "scheduling":
                value = SchedulingTranslation.to_mapi(value)
            elif field_name == "compute":
                value = ComputeTranslation.to_mapi(value)
            elif field_name == "command":
                value = value.strip()
            elif field_name == "parameters":
                # parameters should be passed as-is, explicitly
                pass
            elif field_name == "dependent_deployment":
                value = DependentDeploymentConfig.to_mapi(value)
            elif field_name == "gpu_type" and not value:
                continue
            elif field_name == "cluster" and not value:
                continue
            elif isinstance(value, dict):
                value = strip_nones(value)

            translated_input[translated_name] = value

        # Automatically set the parentName if mcli is running inside a run
        if not translated_input.get('parentName'):
            translated_input['parentName'] = self.get_parent_name_from_env()

        return {
            'runInput': translated_input,
        }


@dataclass
class RunConfig(BaseSubmissionConfig):
    """A run configuration for the MosaicML platform

    Values in here are not yet validated and some required values may be missing.
    On attempting to create the run, a bad config will raise a MapiException with a 400 status code.

    Required args:
        - name (`str`): User-defined name of the run
        - image (`str`): Docker image (e.g. `mosaicml/composer`)
        - command (`str`): Command to use when a run starts
        - compute (:class:`~mcli.ComputeConfig` or `Dict[str, Any]`): Compute configuration. Typically
            a subset of the following fields will be required:

            - `cluster` (`str`): Name of cluster to use
            - `instance` (`str`): Name of instance to use
            - `gpu_type` (`str`): Name of gpu type to use
            - `gpus` (`int`): Number of GPUs to use
            - `cpus` (`int`): Number of CPUs to use
            - `nodes` (`int`): Number of nodes to use

            See `mcli get clusters` for a list of available clusters and instances

    Optional args:
        - parameters (`Dict[str, Any]`): Parameters to mount into the environment
        - scheduling (:class:`~mcli.SchedulingConfig` or `Dict[str, Any]`): Scheduling configuration
            - `priority` (`str`): Priority of the run (default `auto` with options `low` and lowest`)
            - `preemptible` (`bool`): Whether the run is preemptible (default False)
            - `retry_on_system_failure` (`bool`): Whether the run should be retried on system failure (default False)
            - `max_retries` (`int`): Maximum number of retries (default 0)
            - `max_duration` (`float`): Maximum duration of the run in hours (default None)
                Run will be automatically stopped after this duration has elapsed.
        - integrations (`List[Dict[str, Any]]`): List of integrations. See integration documentation for more details:
            https://docs.mosaicml.com/projects/mcli/en/latest/resources/integrations/index.html
        - env_variables (`Dict[str, str]`): Dictionary of environment variables to set in the run
            - key (`str`): Name of the environment variable
            - value (`str`): Value of the environment variable
        - metadata (`Dict[str, Any]`): Arbitrary metadata to attach to the run
    """
    name: Optional[str] = None
    parent_name: Optional[str] = None
    image: Optional[str] = None
    gpu_type: Optional[str] = None
    gpu_num: Optional[int] = None
    cpus: Optional[int] = None
    cluster: Optional[str] = None
    scheduling: SchedulingConfig = field(default_factory=SchedulingConfig)
    compute: ComputeConfig = field(default_factory=ComputeConfig)
    parameters: Dict[str, Any] = field(default_factory=dict)
    scheduling: SchedulingConfig = field(default_factory=SchedulingConfig)
    integrations: List[Dict[str, Any]] = field(default_factory=list)
    env_variables: Union[Dict[str, str], List[Dict[str, str]]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    command: str = ''
    parameters: Dict[str, Any] = field(default_factory=dict)
    dependent_deployment: Dict[str, Any] = field(default_factory=dict)

    _suppress_deprecation_warnings: Optional[bool] = False

    _property_translations = {
        'runName': 'name',
        'parentName': 'parent_name',
        'gpuNum': 'gpu_num',
        'gpuType': 'gpu_type',
        'cpus': 'cpus',
        'cluster': 'cluster',
        'image': 'image',
        'integrations': 'integrations',
        'envVariables': 'env_variables',
        'parameters': 'parameters',
        'command': 'command',
        'compute': 'compute',
        'scheduling': 'scheduling',
        'metadata': 'metadata',
        'dependentDeployment': 'dependent_deployment',
    }

    _required_display_properties = {'name', 'image', 'command', 'compute'}

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> RunConfig:
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
            elif v == 'scheduling':
                value = SchedulingTranslation.from_mapi(value)
            elif v == 'compute':
                value = ComputeTranslation.from_mapi(value)
            elif v == 'dependent_deployment':
                value = DependentDeploymentConfig.from_mapi(value)
            data[v] = value

        # Convert deprecated fields to new format
        compute = data.get('compute', {})
        if data.get('gpu_type') is not None and 'gpu_type' not in compute:
            compute['gpu_type'] = data['gpu_type']
            data['gpu_type'] = None
        if data.get('gpu_num') is not None and 'gpus' not in compute:
            compute['gpus'] = data['gpu_num']
            data['gpu_num'] = None
        if data.get('cpus') and 'cpus' not in compute:
            compute['cpus'] = data['cpus']
            data['cpus'] = None
        if data.get('cluster') is not None and 'cluster' not in compute:
            compute['cluster'] = data['cluster']
            data['cluster'] = None
        data['compute'] = compute

        # Always suppress warnings when deserializing from MAPI response
        data['_suppress_deprecation_warnings'] = True
        return cls(**data)

    def __post_init__(self):
        if isinstance(self.env_variables, list):
            self.env_variables = {var['key']: var['value'] for var in self.env_variables}
            if not self._suppress_deprecation_warnings:
                warnings.warn('Support for passing env_variables as a list will soon be deprecated. ' +
                              f'Please use a dict instead, eg: {self.env_variables}')

        if self.cluster is not None and self._suppress_deprecation_warnings is False:
            warnings.warn('Field "cluster" is deprecated. Please use "compute.cluster" instead.')

        if self.gpu_type is not None and self._suppress_deprecation_warnings is False:
            warnings.warn('Field "gpu_type" is deprecated. Please use "compute.gpu_type" instead.')

        if self.gpu_num is not None and self._suppress_deprecation_warnings is False:
            warnings.warn('Field "gpu_num" is deprecated. Please use "compute.gpus" instead.')

        if self.cpus is not None and self._suppress_deprecation_warnings is False:
            warnings.warn('Field "cpus" is deprecated. Please use "compute.cpus" instead.')

        # Verify types in the compute and scheduling configs and warn for any unknown fields.
        # Soft-warn to maintain backwards compatibility with existing run configs.
        if self._suppress_deprecation_warnings is False:
            unknown_fields_msg = 'Encountered unknown fields in run configuration:\n'
            has_unknown_fields = False

            if self.scheduling is not None:
                expected_scheduling_keys = set(get_type_hints(SchedulingConfig).keys())

                # TODO(MCLOUD-2742): We deprecated `retryOnSystemFailure` in MAPI in favor of `watchdogEnabled` but it
                # is not yet deprecated in MCLI. We should remove this once we deprecate `retryOnSystemFailure` in MCLI
                # and add `watchdog_enabled` to SchedulingConfig.
                expected_scheduling_keys.add('watchdogEnabled')

                unknown_scheduling_keys = set(self.scheduling.keys()) - expected_scheduling_keys
                if len(unknown_scheduling_keys) > 0:
                    has_unknown_fields = True
                    for key in unknown_scheduling_keys:
                        unknown_fields_msg += f'  - \'scheduling.{key}\''

                        match_candidate = difflib.get_close_matches(key, expected_scheduling_keys, n=1, cutoff=0.5)
                        if len(match_candidate) > 0:
                            unknown_fields_msg += f' (did you mean \'{match_candidate[0]}\'?)'

                        unknown_fields_msg += '\n'

            if self.compute is not None:
                expected_compute_keys = get_type_hints(ComputeConfig).keys()
                unknown_compute_keys = set(self.compute.keys()) - expected_compute_keys
                if len(unknown_compute_keys) > 0:
                    has_unknown_fields = True
                    for key in unknown_compute_keys:
                        unknown_fields_msg += f'  - \'compute.{key}\''

                        match_candidate = difflib.get_close_matches(key, expected_compute_keys, n=1, cutoff=0.5)
                        if len(match_candidate) > 0:
                            unknown_fields_msg += f' (did you mean \'{match_candidate[0]}\'?)'

                        unknown_fields_msg += '\n'

            if has_unknown_fields:
                warnings.warn(f'{unknown_fields_msg.strip()}')

        self._suppress_deprecation_warnings = None  # so it won't be printed
