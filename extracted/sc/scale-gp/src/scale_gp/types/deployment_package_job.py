# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DeploymentPackageJob"]


class DeploymentPackageJob(BaseModel):
    deployment_package_job_id: str

    account_id: Optional[str] = None
