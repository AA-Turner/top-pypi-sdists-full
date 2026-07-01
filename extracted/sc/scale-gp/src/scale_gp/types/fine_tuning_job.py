# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "FineTuningJob",
    "VendorConfiguration",
    "VendorConfigurationLaunchFineTuningJobConfiguration",
    "VendorConfigurationLlmEngineFineTuningJobConfiguration",
    "VendorConfigurationOpenAIFineTuningJobConfiguration",
]


class VendorConfigurationLaunchFineTuningJobConfiguration(BaseModel):
    hyperparameters: Optional[Dict[str, object]] = None

    output: Optional[str] = None

    suffix: Optional[str] = None

    vendor: Optional[Literal["LAUNCH"]] = None

    wandb_config: Optional[Dict[str, object]] = None


class VendorConfigurationLlmEngineFineTuningJobConfiguration(BaseModel):
    hyperparameters: Optional[Dict[str, object]] = None

    output: Optional[str] = None

    suffix: Optional[str] = None

    vendor: Optional[Literal["LLMENGINE"]] = None

    wandb_config: Optional[Dict[str, object]] = None


class VendorConfigurationOpenAIFineTuningJobConfiguration(BaseModel):
    hyperparameters: Optional[Dict[str, object]] = None

    suffix: Optional[str] = None

    vendor: Optional[Literal["OPENAI"]] = None


VendorConfiguration: TypeAlias = Annotated[
    Union[
        VendorConfigurationLaunchFineTuningJobConfiguration,
        VendorConfigurationLlmEngineFineTuningJobConfiguration,
        VendorConfigurationOpenAIFineTuningJobConfiguration,
    ],
    PropertyInfo(discriminator="vendor"),
]


class FineTuningJob(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    status: Literal["PENDING", "COMPLETED", "FAILED", "RUNNING", "CANCELED"]

    training_dataset_id: str

    base_model_id: Optional[str] = None

    fine_tuned_model_id: Optional[str] = None

    validation_dataset_id: Optional[str] = None

    vendor_configuration: Optional[VendorConfiguration] = None
