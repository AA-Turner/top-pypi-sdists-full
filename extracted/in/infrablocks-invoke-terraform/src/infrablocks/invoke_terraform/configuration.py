from collections.abc import Callable
from dataclasses import dataclass
from typing import overload

from invoke.context import Context

from infrablocks.invoke_factory import (
    Arguments,
)
from infrablocks.invoke_terraform.terraform import (
    BackendConfig,
    Environment,
    Variables,
)


@dataclass
class InitSpecificConfiguration:
    backend_config: BackendConfig
    reconfigure: bool


@dataclass
class OutputSpecificConfiguration:
    json: bool
    capture_stdout: bool


@dataclass
class ValidateSpecificConfiguration:
    json: bool


@dataclass
class PlanConfiguration:
    init: InitSpecificConfiguration

    variables: Variables
    workspace: str | None

    environment: Environment | None = None

    def __init__(self, configuration: "Configuration | None" = None):
        if configuration is not None:
            self.init = configuration.init
            self.variables = configuration.variables
            self.workspace = configuration.workspace
            self.environment = configuration.environment or {}


@dataclass
class ValidateConfiguration:
    init: InitSpecificConfiguration

    workspace: str | None
    json: bool

    environment: Environment | None = None

    def __init__(self, configuration: "Configuration | None" = None):
        if configuration is not None:
            self.init = configuration.init
            self.workspace = configuration.workspace
            self.json = configuration.validate.json
            self.environment = configuration.environment or {}


@dataclass
class ApplyConfiguration:
    init: InitSpecificConfiguration

    variables: Variables
    workspace: str | None
    auto_approve: bool = True

    environment: Environment | None = None

    def __init__(self, configuration: "Configuration | None" = None):
        if configuration is not None:
            self.init = configuration.init
            self.variables = configuration.variables
            self.workspace = configuration.workspace
            self.auto_approve = configuration.auto_approve
            self.environment = configuration.environment or {}


@dataclass
class DestroyConfiguration:
    init: InitSpecificConfiguration

    variables: Variables
    workspace: str | None
    auto_approve: bool = True

    environment: Environment | None = None

    def __init__(self, configuration: "Configuration | None" = None):
        if configuration is not None:
            self.init = configuration.init
            self.variables = configuration.variables
            self.workspace = configuration.workspace
            self.auto_approve = configuration.auto_approve
            self.environment = configuration.environment or {}


@dataclass
class OutputConfiguration:
    init: InitSpecificConfiguration

    workspace: str | None
    json: bool

    capture_stdout: bool
    environment: Environment | None = None

    def __init__(self, configuration: "Configuration | None" = None):
        if configuration is not None:
            self.init = configuration.init
            self.workspace = configuration.workspace
            self.json = configuration.output.json
            self.capture_stdout = configuration.output.capture_stdout
            self.environment = configuration.environment or {}


@dataclass
class Configuration:
    init: InitSpecificConfiguration
    validate: ValidateSpecificConfiguration
    output: OutputSpecificConfiguration

    source_directory: str
    variables: Variables
    workspace: str | None
    auto_approve: bool = True

    environment: Environment | None = None

    @staticmethod
    def create_empty():
        return Configuration(
            init=InitSpecificConfiguration(
                backend_config={}, reconfigure=False
            ),
            output=OutputSpecificConfiguration(
                json=False, capture_stdout=False
            ),
            validate=ValidateSpecificConfiguration(json=False),
            source_directory="",
            variables={},
            workspace=None,
            environment={},
        )

    @overload
    def apply_overrides(self, configuration: PlanConfiguration) -> None: ...

    @overload
    def apply_overrides(self, configuration: ApplyConfiguration) -> None: ...

    @overload
    def apply_overrides(self, configuration: OutputConfiguration) -> None: ...

    def apply_overrides(
        self,
        configuration: (
            ValidateConfiguration
            | PlanConfiguration
            | ApplyConfiguration
            | DestroyConfiguration
            | OutputConfiguration
        ),
    ) -> None:
        self.init = configuration.init
        self.workspace = configuration.workspace
        self.environment = configuration.environment

        match configuration:
            case ValidateConfiguration():
                self.validate.json = configuration.json
            case PlanConfiguration():
                self.variables = configuration.variables
            case ApplyConfiguration():
                self.variables = configuration.variables
                self.auto_approve = configuration.auto_approve
            case DestroyConfiguration():
                self.variables = configuration.variables
                self.auto_approve = configuration.auto_approve
            case OutputConfiguration():
                self.output.json = configuration.json
                self.output.capture_stdout = configuration.capture_stdout
            case _:
                raise ValueError(
                    "Unsupported configuration type: "
                    + type(configuration).__name__
                )


type ConfigureFunction[C] = Callable[[Context, Arguments, C], None]
