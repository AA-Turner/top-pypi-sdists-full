from __future__ import annotations

from pydantic import BaseModel

from mistralai.workflows import Depends, activity, workflow
from mistralai.workflows.core.definition.workflow_definition import _on_behalf_of_by_name

REREG_OBO_TO_NON_OBO = "test-rereg-obo-to-non-obo"
REREG_NON_OBO_TO_OBO = "test-rereg-non-obo-to-obo"
REREG_OBO_CAN = "test-rereg-obo-continue-as-new"
REREG_NON_OBO_CAN = "test-rereg-non-obo-continue-as-new"


def _get_hooked_client():
    import httpx

    from mistralai.workflows.core.auth import StaticTokenProvider
    from mistralai.workflows.hooks.executor_credentials_hook import AsyncExecutorCredentialsHook

    hook = AsyncExecutorCredentialsHook(server_url="http://mint-server", token_provider=StaticTokenProvider("test-key"))
    return httpx.AsyncClient(
        event_hooks={"request": [hook]},
        transport=httpx.MockTransport(lambda req: httpx.Response(200, json={"ok": True})),
    )


class IterationInput(BaseModel):
    iteration: int = 0


@activity()
async def api_call_with_credentials(client=Depends(_get_hooked_client)) -> dict:
    response = await client.get("http://api/data")
    return response.json()


@workflow.define(name="test-can-jwt-propagation", on_behalf_of=True)
class JWTPropagationContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: IterationInput) -> dict:
        result = await api_call_with_credentials()
        if params.iteration < 1:
            workflow.continue_as_new(IterationInput(iteration=params.iteration + 1))
        return result


@activity()
async def set_obo_flag(workflow_name: str, value: bool) -> None:
    _on_behalf_of_by_name[workflow_name] = value


# enforce_determinism=False disables the Temporal sandbox, which otherwise
# re-imports this module on every execution and resets _on_behalf_of_by_name
# back to the decorator value, preventing the test from simulating a mid-flight re-registration.


@workflow.define(name=REREG_OBO_TO_NON_OBO, on_behalf_of=True, enforce_determinism=False)
class ReregOBOToNonOBOWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict:
        await set_obo_flag(REREG_OBO_TO_NON_OBO, False)
        return await api_call_with_credentials()


@workflow.define(name=REREG_NON_OBO_TO_OBO, on_behalf_of=False, enforce_determinism=False)
class ReregNonOBOToOBOWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict:
        await set_obo_flag(REREG_NON_OBO_TO_OBO, True)
        return await api_call_with_credentials()


@workflow.define(name=REREG_OBO_CAN, on_behalf_of=True, enforce_determinism=False)
class ReregOBOContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: IterationInput) -> dict:
        if params.iteration == 0:
            await set_obo_flag(REREG_OBO_CAN, False)
            workflow.continue_as_new(IterationInput(iteration=1))
        return await api_call_with_credentials()


@workflow.define(name=REREG_NON_OBO_CAN, on_behalf_of=False, enforce_determinism=False)
class ReregNonOBOContinueAsNewWorkflow:
    @workflow.entrypoint
    async def run(self, params: IterationInput) -> dict:
        if params.iteration == 0:
            await set_obo_flag(REREG_NON_OBO_CAN, True)
            workflow.continue_as_new(IterationInput(iteration=1))
        return await api_call_with_credentials()
