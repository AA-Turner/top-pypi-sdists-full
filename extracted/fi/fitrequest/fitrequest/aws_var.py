import logging
from enum import Enum
from functools import cached_property

import boto3
import botocore.exceptions
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AWSSecretTypeEnum(str, Enum):
    ssm = 'ssm'
    secretsmanager = 'secretsmanager'


class AWSRegionEnum(str, Enum):
    af_south_1 = 'af-south-1'
    ap_east_1 = 'ap-east-1'
    ap_northeast_1 = 'ap-northeast-1'
    ap_northeast_2 = 'ap-northeast-2'
    ap_northeast_3 = 'ap-northeast-3'
    ap_south_1 = 'ap-south-1'
    ap_south_2 = 'ap-south-2'
    ap_southeast_1 = 'ap-southeast-1'
    ap_southeast_2 = 'ap-southeast-2'
    ap_southeast_3 = 'ap-southeast-3'
    ap_southeast_4 = 'ap-southeast-4'
    ca_central_1 = 'ca-central-1'
    eu_central_1 = 'eu-central-1'
    eu_central_2 = 'eu-central-2'
    eu_north_1 = 'eu-north-1'
    eu_south_1 = 'eu-south-1'
    eu_south_2 = 'eu-south-2'
    eu_west_1 = 'eu-west-1'
    eu_west_2 = 'eu-west-2'
    eu_west_3 = 'eu-west-3'
    me_central_1 = 'me-central-1'
    me_south_1 = 'me-south-1'
    sa_east_1 = 'sa-east-1'
    us_east_1 = 'us-east-1'
    us_east_2 = 'us-east-2'
    us_west_1 = 'us-west-1'
    us_west_2 = 'us-west-2'


class AWSVar(BaseModel):
    path: str
    secret_type: AWSSecretTypeEnum
    region: AWSRegionEnum = AWSRegionEnum.eu_central_1

    @cached_property
    def session(self) -> boto3.Session:
        return boto3.Session(region_name=self.region.value)

    @staticmethod
    def ssm_value(session: boto3.Session, path: str) -> str | None:
        ssm_client = session.client('ssm')
        ssm_parameter = ssm_client.get_parameter(Name=path, WithDecryption=True)['Parameter']
        return ssm_parameter['Value']

    @staticmethod
    def secret_manager_value(session: boto3.Session, path: str) -> str | None:
        secrets_manager_client = session.client('secretsmanager')
        return secrets_manager_client.get_secret_value(SecretId=path)['SecretString']

    @cached_property
    def value(self) -> str | None:
        try:
            if self.secret_type == AWSSecretTypeEnum.ssm:
                return self.ssm_value(self.session, self.path)
            return self.secret_manager_value(self.session, self.path)
        except (
            botocore.exceptions.BotoCoreError,
            botocore.exceptions.ClientError,
            botocore.exceptions.UndefinedModelAttributeError,
        ) as err:
            logger.warning('Unable to retrieve AWS variable', extra=self.model_dump() | {'error': str(err)})
            return None
