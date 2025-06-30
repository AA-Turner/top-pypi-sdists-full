from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
from typing import Self
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class Settings(BaseSettings):
    ENVIRONMENT: BaseEnums.EnvironmentType = Field(..., description="Environment")
    SERVICE_KEY: str = Field(..., description="Service's key")
    ROOT_PATH: str = Field("", description="Application's root path")
    GOOGLE_CREDENTIALS_PATH: str = Field(
        "/credentials/maleo-google-service-account.json",
        description="Internal credential's file path"
    )
    USE_LOCAL_STATIC_CONFIGURATIONS: bool = Field(
        False,
        description="Whether to use local static configurations"
    )
    STATIC_CONFIGURATIONS_PATH: BaseTypes.OptionalString = Field(
        None,
        description="Maleo's static configurations path"
    )
    USE_LOCAL_RUNTIME_CONFIGURATIONS: bool = Field(
        False,
        description="Whether to use local runtime configurations"
    )
    RUNTIME_CONFIGURATIONS_PATH: BaseTypes.OptionalString = Field(
        None,
        description="Service's runtime configurations path"
    )
    KEY_PASSWORD: BaseTypes.OptionalString = Field(
        None,
        description="Key's password"
    )
    PRIVATE_KEY: BaseTypes.OptionalString = Field(
        None,
        description="Private key"
    )
    PUBLIC_KEY: BaseTypes.OptionalString = Field(
        None,
        description="Public key"
    )

    @model_validator(mode="after")
    def validate_configurations_path(self) -> Self:
        if self.USE_LOCAL_STATIC_CONFIGURATIONS and self.STATIC_CONFIGURATIONS_PATH is None:
            self.STATIC_CONFIGURATIONS_PATH = (
                f"/static-configurations/maleo-static-configurations-{self.ENVIRONMENT}.yaml"
            )

        if self.USE_LOCAL_STATIC_CONFIGURATIONS and self.STATIC_CONFIGURATIONS_PATH is None:
            raise ValueError("Static configurations path must exist if use local static configurations is set to true")

        if self.USE_LOCAL_RUNTIME_CONFIGURATIONS and self.RUNTIME_CONFIGURATIONS_PATH is None:
            self.RUNTIME_CONFIGURATIONS_PATH = (
                f"/runtime-configurations/{self.SERVICE_KEY}-runtime-configurations-{self.ENVIRONMENT}.yaml"
            )

        if self.USE_LOCAL_RUNTIME_CONFIGURATIONS and self.RUNTIME_CONFIGURATIONS_PATH is None:
            raise ValueError("Runtime configurations path must exist if use local runtime configurations is set to true")

        return self