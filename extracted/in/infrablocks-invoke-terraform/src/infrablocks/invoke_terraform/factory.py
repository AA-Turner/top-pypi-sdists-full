from invoke.context import Context
from invoke.tasks import Task

from infrablocks.invoke_factory import (
    Arguments,
    BodyCallable,
    ParameterList,
    create_task,
)
from infrablocks.invoke_terraform.terraform import (
    StreamNames,
    Terraform,
    TerraformFactory,
)

from .configuration import Configuration, ConfigureFunction


class TerraformTaskFactory:
    def __init__(
        self, terraform_factory: TerraformFactory = TerraformFactory()
    ):
        self._terraform_factory = terraform_factory

    def create_plan_task(
        self,
        configuration_name: str,
        configure_function: ConfigureFunction[Configuration],
        parameters: ParameterList,
    ) -> Task[BodyCallable[None]]:
        def plan(context: Context, arguments: Arguments):
            (terraform, configuration) = self._setup_configuration(
                configure_function, context, arguments
            )
            terraform.plan(
                chdir=configuration.source_directory,
                vars=configuration.variables,
                environment=configuration.environment,
            )

        plan.__doc__ = (
            f"Plan the {configuration_name} Terraform configuration."
        )

        return create_task(plan, parameters)

    def create_apply_task(
        self,
        configuration_name: str,
        configure_function: ConfigureFunction[Configuration],
        parameters: ParameterList,
    ) -> Task[BodyCallable[None]]:
        def apply(context: Context, arguments: Arguments):
            (terraform, configuration) = self._setup_configuration(
                configure_function, context, arguments
            )
            terraform.apply(
                chdir=configuration.source_directory,
                vars=configuration.variables,
                autoapprove=configuration.auto_approve,
                environment=configuration.environment,
            )

        apply.__doc__ = (
            f"Apply the {configuration_name} Terraform configuration."
        )

        return create_task(apply, parameters)

    def create_destroy_task(
        self,
        configuration_name: str,
        configure_function: ConfigureFunction[Configuration],
        parameters: ParameterList,
    ) -> Task[BodyCallable[None]]:
        def destroy(context: Context, arguments: Arguments):
            (terraform, configuration) = self._setup_configuration(
                configure_function, context, arguments
            )
            terraform.destroy(
                chdir=configuration.source_directory,
                vars=configuration.variables,
                autoapprove=configuration.auto_approve,
                environment=configuration.environment,
            )

        destroy.__doc__ = (
            f"Destroy the {configuration_name} Terraform configuration."
        )

        return create_task(destroy, parameters)

    def create_validate_task(
        self,
        configuration_name: str,
        configure_function: ConfigureFunction[Configuration],
        parameters: ParameterList,
    ) -> Task[BodyCallable[None]]:
        def validate(context: Context, arguments: Arguments):
            (terraform, configuration) = self._setup_configuration(
                configure_function, context, arguments
            )
            terraform.validate(
                chdir=configuration.source_directory,
                json=configuration.validate.json,
                environment=configuration.environment,
            )

        validate.__doc__ = (
            f"Validate the {configuration_name} Terraform configuration."
        )

        return create_task(validate, parameters)

    def create_output_task(
        self,
        configuration_name: str,
        configure_function: ConfigureFunction[Configuration],
        parameters: ParameterList,
    ) -> Task[BodyCallable[str | None]]:
        def output(context: Context, arguments: Arguments) -> str | None:
            (terraform, configuration) = self._setup_configuration(
                configure_function, context, arguments
            )

            capture: StreamNames | None = None
            if configuration.output.capture_stdout:
                capture = {"stdout"}

            result = terraform.output(
                chdir=configuration.source_directory,
                capture=capture,
                json=configuration.output.json,
                environment=configuration.environment,
            )

            if (
                configuration.output.capture_stdout
                and result.stdout is not None
            ):
                output = result.stdout.read()
                return output.strip()

            return None

        output.__doc__ = (
            f"Output from the {configuration_name} Terraform configuration."
        )

        return create_task(output, parameters)

    def _setup_configuration(
        self,
        configure_function: ConfigureFunction[Configuration],
        context: Context,
        arguments: Arguments,
    ) -> tuple[Terraform, Configuration]:
        configuration = Configuration.create_empty()
        configure_function(
            context,
            arguments,
            configuration,
        )
        terraform = self._terraform_factory.build(context)
        terraform.init(
            chdir=configuration.source_directory,
            backend_config=configuration.init.backend_config,
            reconfigure=configuration.init.reconfigure,
            environment=configuration.environment,
        )

        if configuration.workspace is not None:
            terraform.select_workspace(
                configuration.workspace,
                chdir=configuration.source_directory,
                or_create=True,
                environment=configuration.environment,
            )

        return terraform, configuration
