from pydantic import BaseModel

import mistralai.workflows as workflows


@workflows.activity()
async def activity_with_optional_arg(name: str, id: int = 123) -> str:
    return f"Hello {name}, your ID is {id}"


class ModelArg(BaseModel):
    name: str


@workflows.activity()
async def activity_with_optional_arg_model(name: ModelArg, id: int = 123) -> str:
    return f"Hello {name.name}, your ID is {id}"


@workflows.workflow.define(name="activity-optional-arg-workflow")
class WorkflowCallingActivityWithOptionalArg:
    @workflows.workflow.entrypoint
    async def run(self, name: str) -> str:
        return await activity_with_optional_arg(name)


@workflows.workflow.define(name="activity-optional-arg-workflow-model")
class WorkflowCallingActivityWithOptionalArgModel:
    @workflows.workflow.entrypoint
    async def run(self, name: str) -> str:
        return await activity_with_optional_arg_model(ModelArg(name=name))


@workflows.workflow.define(name="optional-arg-workflow")
class WorkflowWithOptionalArg:
    @workflows.workflow.entrypoint
    async def run(self, name: str, id: int = 123) -> str:
        return f"Hello {name}, your ID is {id}"


@workflows.workflow.define(name="optional-arg-workflow-model")
class WorkflowWithOptionalArgModel:
    @workflows.workflow.entrypoint
    async def run(self, name: ModelArg, id: int = 123) -> str:
        return f"Hello {name.name}, your ID is {id}"
