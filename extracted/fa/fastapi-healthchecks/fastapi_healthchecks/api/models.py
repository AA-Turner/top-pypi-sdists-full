from pydantic import BaseModel

from fastapi_healthchecks.checks import CheckResult


class HealthcheckReport(BaseModel):
    healthy: bool
    checks: list[CheckResult]
