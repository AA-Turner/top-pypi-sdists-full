import asyncio

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.logging import Env, LogFormat, LogLevel, setup_logging

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


class AppConfig(pydantic.BaseModel):
    env: Env = Env.DEV
    temporal_server_url: str = "localhost:7233"
    temporal_namespace: str = "default"
    log_format: str = "console"
    log_level: str = "DEBUG"
    app_version: str = "local_test"


class Address(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")
    street: str
    city: str


class UserProfile(pydantic.BaseModel):
    name: str
    address: Address


@workflows.workflow.define(
    name="example-nested-input-workflow",
    workflow_description="A workflow for testing nested input validation.",
)
class NestedInputWorkflow:
    def __init__(self) -> None:
        self._profile: UserProfile | None = None
        self._continue = True
        self._action_occurred = False

    @workflows.workflow.entrypoint
    async def run(self) -> UserProfile | None:
        while self._continue:
            await workflows.workflow.wait_condition(lambda: self._action_occurred)
            self._action_occurred = False
        return self._profile

    @workflows.workflow.signal(name="update_profile", description="Updates the user profile.")
    async def update_profile_signal(self, profile: UserProfile) -> None:
        self._profile = profile
        self._action_occurred = True

    @workflows.workflow.query(name="get_profile", description="Gets the current user profile.")
    def get_profile_query(self) -> UserProfile | None:
        return self._profile

    @workflows.workflow.update(name="set_profile", description="Sets the user profile and returns it.")
    async def set_profile_update(self, profile: UserProfile) -> UserProfile:
        self._profile = profile
        self._action_occurred = True
        return self._profile

    @workflows.workflow.signal(name="stop", description="Stops the workflow.")
    async def stop_signal(self) -> None:
        self._continue = False
        self._action_occurred = True


if __name__ == "__main__":
    app_cfg = AppConfig()
    setup_logging(
        log_format=LogFormat(app_cfg.log_format),
        log_level=LogLevel(app_cfg.log_level),
        app_version=app_cfg.app_version,
    )
    asyncio.run(workflows.run_worker(workflows=[NestedInputWorkflow]))
