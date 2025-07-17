from metaflow.user_configs.config_decorators import (
    MutableFlow,
    MutableStep,
    CustomFlowDecorator,
)
from .assume_role import OBP_ASSUME_ROLE_ARN_ENV_VAR


class assume_role(CustomFlowDecorator):
    """
    Flow-level decorator for assuming AWS IAM roles.

    When applied to a flow, all steps in the flow will automatically use the specified IAM role-arn
    as their source principal.

    Usage:
    ------
    @assume_role(role_arn="arn:aws:iam::123456789012:role/my-iam-role")
    class MyFlow(FlowSpec):
        @step
        def start(self):
            import boto3
            client = boto3.client("dynamodb")  # Automatically uses the role in the flow decorator
            self.next(self.end)

        @step
        def end(self):
            from metaflow import get_aws_client
            client = get_aws_client("dynamodb")  # Automatically uses the role in the flow decorator
    """

    def init(self, *args, **kwargs):
        self.role_arn = kwargs.get("role_arn", None)

        if self.role_arn is None:
            raise ValueError(
                "`role_arn` keyword argument is required for the assume_role decorator"
            )

        if not self.role_arn.startswith("arn:aws:iam::"):
            raise ValueError(
                "`role_arn` must be a valid AWS IAM role ARN starting with 'arn:aws:iam::'"
            )

    def evaluate(self, mutable_flow: MutableFlow) -> None:
        """
        This method is called by Metaflow to apply the decorator to the flow.
        It sets up environment variables that will be used by the AWS client
        to automatically assume the specified role.
        """
        # Import environment decorator at runtime to avoid circular imports
        from metaflow import environment

        # Set the role ARN as an environment variable that will be picked up
        # by the get_aws_client function
        def _setup_role_assumption(step: MutableStep) -> None:
            # We'll inject the role assumption by adding an environment decorator
            # The role will be available through an environment variable
            step.add_decorator(
                environment, vars={OBP_ASSUME_ROLE_ARN_ENV_VAR: self.role_arn}
            )

        # Apply the role assumption setup to all steps in the flow
        for _, step in mutable_flow.steps:
            _setup_role_assumption(step)
