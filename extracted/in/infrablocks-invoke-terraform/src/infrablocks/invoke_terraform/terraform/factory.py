from invoke.context import Context

from .invoke_executor import InvokeExecutor
from .terraform import Terraform


class TerraformFactory:
    def build(self, context: Context) -> Terraform:
        return Terraform(InvokeExecutor(context))
