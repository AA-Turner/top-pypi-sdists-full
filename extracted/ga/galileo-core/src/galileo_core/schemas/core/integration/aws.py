from enum import Enum
from typing import Dict

from pydantic import BaseModel


class AwsRegion(str, Enum):
    us_east_1 = "us-east-1"
    us_east_2 = "us-east-2"
    us_west_1 = "us-west-1"
    us_west_2 = "us-west-2"


class AwsCredentialType(str, Enum):
    assumed_role = "assumed_role"
    key_secret = "key_secret"


class AwsCredentials(BaseModel):
    credential_type: AwsCredentialType = AwsCredentialType.key_secret
    region: str = AwsRegion.us_west_2


class BaseAwsIntegrationCreate(AwsCredentials):
    token: Dict[str, str]
