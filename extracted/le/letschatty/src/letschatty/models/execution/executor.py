from letschatty.models.utils.types import ExecutorType
from letschatty.models.company.assets.users.user import User
from letschatty.models.utils.types import StrObjectId
from typing import Optional
from pydantic import BaseModel
from letschatty.models.analytics.sources import Source
from letschatty.models.company.assets.flow import FlowPreview

class Executor(BaseModel):
    id: StrObjectId
    type: ExecutorType
    name: str

    @classmethod
    def system(cls) -> 'Executor':
        return cls(id="000000000000000000000000", type=ExecutorType.SYSTEM, name="Chatty")

    @classmethod
    def from_user(cls, user: User) -> 'Executor':
        return cls(id=user.id, type=ExecutorType.AGENT, name=user.name)

    @classmethod
    def from_workflow(cls, workflow : FlowPreview) -> 'Executor':
        return cls(id=workflow.id, type=ExecutorType.WORKFLOW, name=workflow.title)

    @classmethod
    def from_source(cls, source: Source) -> 'Executor':
        return cls(id=source.id, type=ExecutorType.SOURCE_AUTOMATION, name=source.name)

    @classmethod
    def from_meta(cls) -> 'Executor':
        return cls(id="000000000000000000000001", type=ExecutorType.META, name="Meta")
