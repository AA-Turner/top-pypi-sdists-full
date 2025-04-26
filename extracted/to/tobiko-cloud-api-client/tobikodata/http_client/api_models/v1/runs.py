import typing as t
from datetime import datetime

from pydantic import HttpUrl

from tobikodata.http_client.api_models.v1.common import V1Status
from tobikodata.pydantic import ForwardCompatiblePydanticModel


class V1Run(ForwardCompatiblePydanticModel):
    environment: str
    run_id: str
    start_at: t.Optional[datetime]
    end_at: t.Optional[datetime]
    error_message: t.Optional[str]
    status: V1Status
    link: HttpUrl

    @property
    def complete(self) -> bool:
        return self.status.complete
