import asyncio
from typing import List

import pydantic

import mistralai.workflows as workflows
from mistralai.workflows import workflow
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.dependencies.dependency_injector import Depends
from mistralai.workflows.core.logging import setup_logging

with workflow.unsafe.imports_passed_through():
    import structlog

logger = structlog.getLogger(__name__)


# Use the real AppConfig from workflows.worker.config


class MockedDBConnection:
    def __init__(self) -> None:
        self.users = ["user1", "user2"]

    def add_user(self, user: str) -> None:
        self.users.append(user)

    def get_users(self) -> List[str]:
        return self.users


async def get_db_connection_async() -> MockedDBConnection:
    return MockedDBConnection()


class AllUsersResponse(pydantic.BaseModel):
    users: List[str] = pydantic.Field(description="List of users")


@workflows.activity()
async def get_all_users(db_conn: MockedDBConnection = Depends(dependency=get_db_connection_async)) -> AllUsersResponse:
    logger.info("activity: querying all users")
    await asyncio.sleep(1)  # fake work
    users = db_conn.get_users()
    return AllUsersResponse(users=users)


class AddUserParams(pydantic.BaseModel):
    user: str = pydantic.Field(description="User to add")


@workflows.activity()
async def add_user(
    params: AddUserParams, db_conn: MockedDBConnection = Depends(dependency=get_db_connection_async)
) -> None:
    logger.info(f"activity: adding user {params.user}")
    await asyncio.sleep(1)  # fake work
    db_conn.add_user(params.user)


class WorkflowParams(pydantic.BaseModel):
    user: str = pydantic.Field(description="User to add")


class WorkflowResult(pydantic.BaseModel):
    results: List[str] = pydantic.Field(description="List of results")


@workflows.workflow.define(name="example-dependency-injection-workflow", workflow_description="Example workflow")
class WorkflowWithDependencyInjection:
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> WorkflowResult:
        users = await get_all_users()
        logger.info(f"workflow: got users {users.users}")
        await add_user(AddUserParams(user=params.user))
        logger.info(f"workflow: added user {params.user}")
        users = await get_all_users()
        logger.info(f"workflow: got users {users.users}")
        return WorkflowResult(results=users.users)


if __name__ == "__main__":
    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )
    asyncio.run(workflows.run_worker([WorkflowWithDependencyInjection]))
