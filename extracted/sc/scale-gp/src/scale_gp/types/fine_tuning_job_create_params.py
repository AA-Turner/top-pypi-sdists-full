# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

__all__ = [
    "FineTuningJobCreateParams",
    "VendorConfiguration",
    "VendorConfigurationLaunchFineTuningJobConfiguration",
    "VendorConfigurationLlmEngineFineTuningJobConfiguration",
    "VendorConfigurationOpenAIFineTuningJobConfiguration",
]


class FineTuningJobCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    training_dataset_id: Required[str]

    base_model_id: str

    fine_tuned_model_id: str

    validation_dataset_id: str

    vendor_configuration: VendorConfiguration


class VendorConfigurationLaunchFineTuningJobConfiguration(TypedDict, total=False):
    hyperparameters: Dict[str, object]

    output: str

    suffix: str

    vendor: Literal["LAUNCH"]

    wandb_config: Dict[str, object]


class VendorConfigurationLlmEngineFineTuningJobConfiguration(TypedDict, total=False):
    hyperparameters: Dict[str, object]

    output: str

    suffix: str

    vendor: Literal["LLMENGINE"]

    wandb_config: Dict[str, object]


class VendorConfigurationOpenAIFineTuningJobConfiguration(TypedDict, total=False):
    hyperparameters: Dict[str, object]

    suffix: str

    vendor: Literal["OPENAI"]


VendorConfiguration: TypeAlias = Union[
    VendorConfigurationLaunchFineTuningJobConfiguration,
    VendorConfigurationLlmEngineFineTuningJobConfiguration,
    VendorConfigurationOpenAIFineTuningJobConfiguration,
]
