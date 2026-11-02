from typing import Any, Literal, Self, TypedDict, Unpack, overload

from invoke.collection import Collection
from invoke.context import Context

from infrablocks.invoke_factory import Arguments, Parameter, ParameterList

from .configuration import (
    ApplyConfiguration,
    Configuration,
    ConfigureFunction,
    DestroyConfiguration,
    OutputConfiguration,
    PlanConfiguration,
    ValidateConfiguration,
)
from .factory import TerraformTaskFactory


class TerraformTaskCollectionParameters(TypedDict, total=False):
    configuration_name: str
    global_parameters: ParameterList
    global_configure_function: ConfigureFunction[Configuration]
    task_extra_parameters: dict[str, ParameterList]
    task_override_parameters: dict[str, ParameterList]
    task_extra_configure_function: dict[str, ConfigureFunction[Any]]
    task_override_configure_function: dict[
        str, ConfigureFunction[Configuration]
    ]


class TerraformTaskCollection:
    def __init__(
        self,
        configuration_name: str | None = None,
        global_parameters: ParameterList | None = None,
        global_configure_function: ConfigureFunction[Configuration]
        | None = None,
        task_extra_parameters: dict[str, ParameterList] | None = None,
        task_override_parameters: dict[str, ParameterList] | None = None,
        task_extra_configure_function: dict[str, ConfigureFunction[Any]]
        | None = None,
        task_override_configure_function: dict[str, ConfigureFunction[Any]]
        | None = None,
        task_factory: TerraformTaskFactory = TerraformTaskFactory(),
    ):
        self.configuration_name = configuration_name
        self.global_parameters: ParameterList = (
            global_parameters if global_parameters is not None else []
        )
        self.global_configure_function: ConfigureFunction[Configuration] = (
            global_configure_function
            if global_configure_function is not None
            else lambda context, arguments, configuration: None
        )
        self.task_extra_parameters: dict[str, ParameterList] = (
            task_extra_parameters if task_extra_parameters is not None else {}
        )
        self.task_override_parameters: dict[str, ParameterList] = (
            task_override_parameters
            if task_override_parameters is not None
            else {}
        )
        self.task_extra_configure_function: dict[
            str, ConfigureFunction[Any]
        ] = (
            task_extra_configure_function
            if task_extra_configure_function is not None
            else {}
        )
        self.task_override_configure_function: dict[
            str, ConfigureFunction[Any]
        ] = (
            task_override_configure_function
            if task_override_configure_function is not None
            else {}
        )
        self._task_factory = task_factory

    def _clone(
        self, **kwargs: Unpack[TerraformTaskCollectionParameters]
    ) -> Self:
        return self.__class__(
            configuration_name=kwargs.get(
                "configuration_name", self.configuration_name
            ),
            global_parameters=kwargs.get(
                "global_parameters", self.global_parameters
            ),
            global_configure_function=kwargs.get(
                "global_configure_function", self.global_configure_function
            ),
            task_extra_parameters=kwargs.get(
                "task_extra_parameters", self.task_extra_parameters
            ),
            task_override_parameters=kwargs.get(
                "task_override_parameters", self.task_override_parameters
            ),
            task_extra_configure_function=kwargs.get(
                "task_extra_configure_function",
                self.task_extra_configure_function,
            ),
            task_override_configure_function=kwargs.get(
                "task_override_configure_function",
                self.task_override_configure_function,
            ),
            task_factory=self._task_factory,
        )

    def for_configuration(self, configuration_name: str):
        return self._clone(configuration_name=configuration_name)

    def with_global_parameters(self, *global_parameters: Parameter) -> Self:
        return self._clone(global_parameters=global_parameters)

    def with_global_configure_function(
        self, global_configure_function: ConfigureFunction[Configuration]
    ) -> Self:
        return self._clone(global_configure_function=global_configure_function)

    def with_extra_task_parameters(
        self, task_name: str, *parameters: Parameter
    ) -> Self:
        return self._clone(
            task_extra_parameters={
                **self.task_extra_parameters,
                task_name: parameters,
            }
        )

    def with_overridden_task_parameters(
        self, task_name: str, *parameters: Parameter
    ) -> Self:
        return self._clone(
            task_override_parameters={
                **self.task_override_parameters,
                task_name: parameters,
            }
        )

    @overload
    def with_extra_task_configure_function(
        self,
        task_name: Literal["validate"],
        task_configure_function: ConfigureFunction[ValidateConfiguration],
    ) -> Self: ...

    @overload
    def with_extra_task_configure_function(
        self,
        task_name: Literal["plan"],
        task_configure_function: ConfigureFunction[PlanConfiguration],
    ) -> Self: ...

    @overload
    def with_extra_task_configure_function(
        self,
        task_name: Literal["apply"],
        task_configure_function: ConfigureFunction[ApplyConfiguration],
    ) -> Self: ...

    @overload
    def with_extra_task_configure_function(
        self,
        task_name: Literal["destroy"],
        task_configure_function: ConfigureFunction[DestroyConfiguration],
    ) -> Self: ...

    @overload
    def with_extra_task_configure_function(
        self,
        task_name: Literal["output"],
        task_configure_function: ConfigureFunction[OutputConfiguration],
    ) -> Self: ...

    def with_extra_task_configure_function(
        self, task_name: str, task_configure_function: ConfigureFunction[Any]
    ) -> Self:
        return self._clone(
            task_extra_configure_function={
                **self.task_extra_configure_function,
                task_name: task_configure_function,
            }
        )

    def with_overridden_task_configure_function(
        self,
        task_name: str,
        task_configure_function: ConfigureFunction[Configuration],
    ) -> Self:
        return self._clone(
            task_override_configure_function={
                **self.task_override_configure_function,
                task_name: task_configure_function,
            }
        )

    def _resolve_parameters(self, task_name: str) -> ParameterList:
        if task_name in self.task_override_parameters:
            return self.task_override_parameters[task_name]

        return [
            *self.global_parameters,
            *self.task_extra_parameters.get(task_name, []),
        ]

    def _resolve_configure_function(
        self,
        task_name: Literal["validate", "plan", "apply", "destroy", "output"],
    ) -> ConfigureFunction[Configuration]:
        if task_name in self.task_override_configure_function:
            return self.task_override_configure_function[task_name]

        global_configure_function = self.global_configure_function
        extra_configure_function = self.task_extra_configure_function.get(
            task_name, lambda context, arguments, configuration: None
        )

        specific_configuration_type: (
            type[ValidateConfiguration]
            | type[PlanConfiguration]
            | type[ApplyConfiguration]
            | type[DestroyConfiguration]
            | type[OutputConfiguration]
        )
        match task_name:
            case "validate":
                specific_configuration_type = PlanConfiguration
            case "plan":
                specific_configuration_type = PlanConfiguration
            case "apply":
                specific_configuration_type = ApplyConfiguration
            case "destroy":
                specific_configuration_type = ApplyConfiguration
            case "output":
                specific_configuration_type = OutputConfiguration
            case _:
                raise ValueError("Unsupported task name: " + task_name)

        def combined_configure_function(
            context: Context,
            arguments: Arguments,
            configuration: Configuration,
        ):
            global_configure_function(context, arguments, configuration)

            specific_configuration = specific_configuration_type(configuration)
            extra_configure_function(
                context, arguments, specific_configuration
            )

            configuration.apply_overrides(specific_configuration)

        return combined_configure_function

    def create(self) -> Collection:
        if self.configuration_name is None:
            raise ValueError("Configuration name must be set before creating.")

        collection = Collection(self.configuration_name)

        validate_task = self._task_factory.create_validate_task(
            self.configuration_name,
            self._resolve_configure_function("validate"),
            self._resolve_parameters("validate"),
        )
        plan_task = self._task_factory.create_plan_task(
            self.configuration_name,
            self._resolve_configure_function("plan"),
            self._resolve_parameters("plan"),
        )
        apply_task = self._task_factory.create_apply_task(
            self.configuration_name,
            self._resolve_configure_function("apply"),
            self._resolve_parameters("apply"),
        )
        destroy_task = self._task_factory.create_destroy_task(
            self.configuration_name,
            self._resolve_configure_function("destroy"),
            self._resolve_parameters("destroy"),
        )
        output_task = self._task_factory.create_output_task(
            self.configuration_name,
            self._resolve_configure_function("output"),
            self._resolve_parameters("output"),
        )

        collection.add_task(  # pyright: ignore[reportUnknownMemberType]
            validate_task
        )
        collection.add_task(  # pyright: ignore[reportUnknownMemberType]
            plan_task
        )
        collection.add_task(  # pyright: ignore[reportUnknownMemberType]
            apply_task
        )
        collection.add_task(  # pyright: ignore[reportUnknownMemberType]
            destroy_task
        )
        collection.add_task(  # pyright: ignore[reportUnknownMemberType]
            output_task
        )

        return collection
