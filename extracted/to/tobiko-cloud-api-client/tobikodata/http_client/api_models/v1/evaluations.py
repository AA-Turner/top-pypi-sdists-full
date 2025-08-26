import typing as t
from datetime import datetime
from functools import cached_property

from pydantic import HttpUrl

from tobikodata.http_client.api_models.v1.common import V1Status
from tobikodata.pydantic import ForwardCompatiblePydanticModel


class V1AuditEvaluation(ForwardCompatiblePydanticModel):
    name: str
    execution_time: t.Optional[datetime] = None
    interval_start: datetime
    interval_end: datetime
    status: t.Literal[V1Status.SUCCESS, V1Status.FAILED]
    link: HttpUrl
    log_link: HttpUrl
    log: t.Optional[str]


class V1EvaluationBase(ForwardCompatiblePydanticModel):
    evaluation_id: str
    node_name: str
    start_at: t.Optional[datetime]
    end_at: t.Optional[datetime]
    error_message: t.Optional[str]
    log: t.Optional[str]
    status: V1Status
    link: HttpUrl
    log_link: HttpUrl
    audits: t.List[V1AuditEvaluation] = []

    @property
    def complete(self) -> bool:
        return self.status.complete

    @cached_property
    def audits_by_name(self) -> t.Mapping[str, V1AuditEvaluation]:
        return {a.name: a for a in self.audits}


class V1PlanEvaluation(V1EvaluationBase):
    plan_id: str


class V1RunEvaluation(V1EvaluationBase):
    run_id: str


V1Evaluation = t.Union[V1PlanEvaluation, V1RunEvaluation]
