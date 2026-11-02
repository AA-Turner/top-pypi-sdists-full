"""Private connection from a capability activity to its Session sandbox."""

from typing import Literal

from pydantic import BaseModel, Field, JsonValue, model_validator

from mistralai.vibe.harness.runtime.hosts.workflows import WorkflowSandboxResource
from mistralai.vibe_agents.sdk.authoring import contracts
from mistralai.vibe_agents.sdk.sandbox.koyeb import KoyebSandboxDefinition, KoyebSandboxDriver


class KoyebCapabilitySandbox(BaseModel):
    """Connection material for the sandbox already opened by the Workflow."""

    type: Literal["koyeb"] = "koyeb"
    definition: KoyebSandboxDefinition
    state: dict[str, JsonValue] = Field(repr=False)

    @model_validator(mode="after")
    def require_existing_sandbox(self) -> "KoyebCapabilitySandbox":
        if any(not isinstance(self.state.get(key), str) for key in ("sandbox_id", "app_id", "service_id")):
            raise ValueError("Koyeb capability access requires an existing session sandbox")
        return self


def from_workflow_sandbox(
    authored: contracts.Sandbox,
    resource: WorkflowSandboxResource,
) -> KoyebCapabilitySandbox | None:
    if not isinstance(authored, contracts.MistralSandbox):
        return None
    state = resource.continuation.provider_state
    if state is None:
        raise RuntimeError("MistralSandbox has no active connection state")
    return KoyebCapabilitySandbox(
        # The Workflow-owned driver renews proxy credentials before scheduling
        # this activity. Reconnecting here must not renew them a second time.
        definition=KoyebSandboxDefinition.from_authored(authored).model_copy(update={"proxy": None}),
        state=state,
    )


async def open_activity_sandbox(connection: KoyebCapabilitySandbox | None) -> contracts.HookSandbox:
    sandbox = contracts.HookSandbox()
    if connection is None:
        return sandbox
    driver = KoyebSandboxDriver(
        connection.definition,
        connection.state,
    )
    await driver.attach()
    sandbox.bind(driver)
    return sandbox


__all__ = ["KoyebCapabilitySandbox", "from_workflow_sandbox", "open_activity_sandbox"]
