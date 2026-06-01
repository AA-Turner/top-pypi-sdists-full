"""
Example workflow demonstrating local activity execution.

Local activities run directly in the workflow worker process, bypassing
Temporal's task queue for faster execution of quick operations.

"""

import asyncio
from datetime import timedelta

from pydantic import BaseModel

import mistralai.workflows as workflows
from mistralai.workflows import run_activities_locally


class UserData(BaseModel):
    email: str
    name: str


class ValidationResult(BaseModel):
    is_valid: bool
    errors: list[str] = []


class EnrichedData(BaseModel):
    user_data: UserData
    domain: str
    initials: str


class SaveResult(BaseModel):
    status: str
    user_id: str


@workflows.activity(start_to_close_timeout=timedelta(seconds=2))
async def validate_user(data: UserData) -> ValidationResult:
    """Quick validation - perfect for local execution."""
    errors = []
    if "@" not in data.email:
        errors.append("Invalid email")
    if not data.name:
        errors.append("Name required")

    return ValidationResult(is_valid=len(errors) == 0, errors=errors)


@workflows.activity(start_to_close_timeout=timedelta(seconds=2))
async def enrich_user_data(data: UserData) -> EnrichedData:
    """Quick data enrichment - good for local execution."""
    return EnrichedData(
        user_data=data, domain=data.email.split("@")[1], initials="".join([n[0] for n in data.name.split()])
    )


@workflows.activity(start_to_close_timeout=timedelta(minutes=5), retry_policy_max_attempts=3)
async def save_to_database(data: EnrichedData) -> SaveResult:
    """External database call - needs retry isolation."""
    # Simulate slow database operation
    await asyncio.sleep(0.5)
    return SaveResult(status="saved", user_id=data.user_data.email)


@workflows.workflow.define(name="local-activity-demo")
class LocalActivityWorkflow:
    """
    Demonstrates mixing local and remote activity execution.

    Fast operations (validate, enrich) run locally for lower latency.
    Slow operations (database save) run remotely for better isolation.
    """

    @workflows.workflow.entrypoint
    async def run(self, user_data: UserData) -> SaveResult:
        # Fast operations run locally
        with run_activities_locally():
            validation = await validate_user(user_data)

            if not validation.is_valid:
                raise ValueError(f"Validation failed: {validation.errors}")

            enriched = await enrich_user_data(user_data)

        # Slow operation runs as regular activity
        result = await save_to_database(enriched)

        return result


async def main() -> None:
    from mistralai.workflows import run_worker

    await run_worker([LocalActivityWorkflow])


if __name__ == "__main__":
    asyncio.run(main())
