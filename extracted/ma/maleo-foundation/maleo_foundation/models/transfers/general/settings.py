from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
from typing import Self
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes

class Settings(BaseSettings):
    ENVIRONMENT: BaseEnums.EnvironmentType = Field(..., description="Environment")
    SERVICE_KEY: str = Field(..., description="Service's key")
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

    @classmethod
    @model_validator(mode="before")
    def define_configurations_path(
        cls,
        values: BaseTypes.StringToAnyDict
    ) -> BaseTypes.StringToAnyDict:
        # Define and check environment
        environment: BaseTypes.OptionalString = values.get("ENVIRONMENT", None)
        if environment is None:
            raise ValueError("'ENVIRONMENT' variable not defined/found")

        # Define and check service key
        service_key: BaseTypes.OptionalString = values.get("SERVICE_KEY", None)
        if service_key is None:
            raise ValueError("'SERVICE_KEY' variable not defined/found")

        # Define and check use local static configurations
        use_local_static_configurations: BaseTypes.OptionalBoolean = values.get("USE_LOCAL_STATIC_CONFIGURATIONS", None)
        if use_local_static_configurations is None:
            raise ValueError("'USE_LOCAL_STATIC_CONFIGURATIONS' variable not defined/found")

        # Define static configurations path if necessary
        static_configurations_path: BaseTypes.OptionalString = values.get("STATIC_CONFIGURATIONS_PATH", None)
        if use_local_static_configurations and static_configurations_path is None:
            values["STATIC_CONFIGURATIONS_PATH"] = f"/configurations/maleo-static-configurations-{environment}"

        # Define and check use local runtime configurations
        use_local_runtime_configurations: BaseTypes.OptionalBoolean = values.get("USE_LOCAL_RUNTIME_CONFIGURATIONS", None)
        if use_local_runtime_configurations is None:
            raise ValueError("'USE_LOCAL_RUNTIME_CONFIGURATIONS' variable not defined/found")

        # Define runtime configurations path if necessary
        runtime_configurations_path: BaseTypes.OptionalString = values.get("RUNTIME_CONFIGURATIONS_PATH", None)
        if use_local_runtime_configurations and runtime_configurations_path is None:
            values["RUNTIME_CONFIGURATIONS_PATH"] = f"/configurations/{service_key}-runtime-configurations-{environment}"

        return values

    @model_validator(mode="after")
    def validate_configurations_path(self) -> Self:
        if self.USE_LOCAL_STATIC_CONFIGURATIONS and self.STATIC_CONFIGURATIONS_PATH is None:
            raise ValueError("Static configurations path must exist if use local static configurations is set to true")
        
        if self.USE_LOCAL_RUNTIME_CONFIGURATIONS and self.RUNTIME_CONFIGURATIONS_PATH is None:
            raise ValueError("Runtime configurations path must exist if use local runtime configurations is set to true")

        return self