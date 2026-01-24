from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class AuthType(str, Enum):
    USER = "user"
    SERVICE = "service"
    APPLICATION = "application"

    @property
    def path(self) -> str:
        return {
            AuthType.USER: "/user/v5",
            AuthType.SERVICE: "/service/v5",
            AuthType.APPLICATION: "/application/v5",
        }[self]


class GatewayEndpoint(str, Enum):
    STAGING = "https://api.app.stgn.grazie.aws.intellij.net"
    PRODUCTION = "https://api.app.prod.grazie.aws.intellij.net"


def format_decimal(decimal: Decimal) -> str:
    formatted = str(decimal)

    if "." not in formatted:
        formatted = f"{formatted}."
    return formatted


class Credit(BaseModel):
    amount: Decimal

    class Config:
        json_encoders = {
            Decimal: format_decimal,
        }


class QuotaId(BaseModel):
    quotaId: str
    userId: Optional[str] = None


class Quota(BaseModel):
    """
    Represents a Quota - a set of data that encapsulates current usage
    of user and total allowed usage in Credit.

    Attributes:
        license: The license id the quota is for.
        current: The current usage of user in Credit.
        maximum: The maximum usage of user in Credit. Note that
            it may differ from the tariff, if extensions has been applied.
        until: The time after which the quota is considered expired, equals to license expiration time.
        quotaID: Used to identify quota
    """

    license: str
    current: Credit
    maximum: Credit
    until: Optional[datetime]
    quotaID: Optional[QuotaId]


class GrazieHeaders(str, Enum):
    """
    Headers that are used in grazie platform.
    """

    AUTH_TOKEN = "Grazie-Authenticate-JWT"
    ORIGINAL_USER_TOKEN = "Grazie-Original-User-JWT"
    ORIGINAL_APPLICATION_TOKEN = "Grazie-Original-Application-JWT"
    APPLICATION_USER = "Grazie-Application-User-ID"
    ORIGINAL_SERVICE_TOKEN = "Grazie-Original-Service-JWT"
    ORIGINAL_USER_IP = "Grazie-Original-User-IP"
    AGENT = "Grazie-Agent"
    QUOTA_METADATA = "Grazie-Quota-Metadata"
    TRACE_ID = "Grazie-Trace-Id"
    DEPRECATION_INFO = "Grazie-Deprecated-Info"
    ORIGINAL_USER_COUNTRY = "Grazie-Original-User-Country"
