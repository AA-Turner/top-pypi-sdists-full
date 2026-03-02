from pydantic import BaseModel

from .account import Account
from .organization import Organization


class Cloud(BaseModel):
    """
    The Cloud object contains information about a cloud account such as AWS Account
    ID, regions, etc.
    """

    provider: str # The unique name of the Cloud services provider, such as AWS, MS
                  # Azure, GCP, etc.

    # Recommended:
    region: str | None = None # The name of the cloud region, as defined by the cloud provider.

    # Optional:
    account: Account | None = None
    org: Organization | None = None
    project_uid: str | None = None
    zone: str | None = None # The availability zone in the cloud region, as defined by the cloud
                            # provider.
