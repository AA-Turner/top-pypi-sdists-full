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
    USE_LOCAL_CONFIGURATIONS: bool = Field(
        False,
        description="Whether to use local configurations"
    )
    CONFIGURATIONS_PATH: BaseTypes.OptionalString = Field(
        None,
        description="Configurations path"
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
        if self.USE_LOCAL_CONFIGURATIONS and self.CONFIGURATIONS_PATH is None:
            self.CONFIGURATIONS_PATH = (
                f"/configurations/{self.SERVICE_KEY}-configurations-{self.ENVIRONMENT}.yaml"
            )

        if self.USE_LOCAL_CONFIGURATIONS and self.CONFIGURATIONS_PATH is None:
            raise ValueError("Configurations path must exist if use local configurations is set to true")

        return self