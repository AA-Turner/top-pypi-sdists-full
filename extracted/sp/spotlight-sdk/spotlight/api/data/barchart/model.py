from pydantic import Field

from spotlight.core.common.base import Base
from spotlight.core.common.config import EnvironmentConfig

config = EnvironmentConfig()


class BarchartQuery(Base):
    apikey: str = Field(default=config.auth_config.barchart_api_token, init=False)
    symbol: str
    type: str
