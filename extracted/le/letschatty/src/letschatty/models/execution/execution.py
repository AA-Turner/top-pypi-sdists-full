from letschatty.models.utils.types import StrObjectId
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from .executor import Executor, ExecutorType
from letschatty.models.analytics.sources import Source
from letschatty.models.company.assets.users.user import User

class ExecutionContext(BaseModel):
    trace_id: StrObjectId = Field(default_factory=lambda: str(ObjectId()))
    start_time: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    metadata: dict = Field(default_factory=dict)
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    executor: Executor
    event_time: Optional[datetime] = None
    company_id: StrObjectId

    @staticmethod
    def chatty_company_id() -> StrObjectId:
        return "000000000000000000000000"

    @property
    def time(self) -> datetime:
        if not self.event_time:
            raise ValueError("Event time is not set")
        return self.event_time

    def add_metadata(self, key, value):
        self.metadata[key] = value

    def finish(self):
        self.end_time = datetime.now(ZoneInfo("UTC"))
        self.duration = (self.end_time - self.start_time).total_seconds()

    def set_event_time(self, timestamp: datetime):
        """Set the time to use for event timestamps"""
        if self.event_time is None:
            self.event_time = timestamp
        else:
            return

    @classmethod
    def for_continuous_conversation(cls, company_id: StrObjectId, creator_id: StrObjectId) -> "ExecutionContext":
        executor = Executor(id=creator_id, type=ExecutorType.SYSTEM, name="Continuous Conversation")
        return cls(executor=executor, company_id=company_id)

    @classmethod
    def default_for_automations(cls, source: Source) -> "ExecutionContext":
        executor = Executor.from_source(source)
        return cls(executor=executor, company_id=source.company_id)

    @classmethod
    def default_for_system(cls, company_id: StrObjectId) -> "ExecutionContext":
        executor = Executor.system()
        return cls(executor=executor, company_id=company_id)

    @classmethod
    def default_for_meta(cls, company_id: StrObjectId) -> "ExecutionContext":
        executor = Executor.from_meta()
        return cls(executor=executor, company_id=company_id)

    @classmethod
    def from_user(cls, user: User) -> "ExecutionContext":
        executor = Executor.from_user(user)
        return cls(executor=executor, company_id=user.company_id)

    @classmethod
    def from_copilot(cls, user_id: StrObjectId, company_id: StrObjectId) -> "ExecutionContext":
        executor = Executor(id=user_id, type=ExecutorType.COPILOT, name="Chatty Copilot")
        return cls(executor=executor, company_id=company_id)

    @classmethod
    def from_mega_admin(cls, user: User, company_id: StrObjectId) -> "ExecutionContext":
        executor = Executor(id=user.id, type=ExecutorType.MEGA_ADMIN, name=user.name)
        return cls(executor=executor, company_id=company_id)

    @classmethod
    def from_integration(cls, user: User, company_id: StrObjectId) -> "ExecutionContext":
        executor = Executor(id=user.id, type=ExecutorType.INTEGRATION, name=user.name)
        return cls(executor=executor, company_id=company_id)

    @property
    def is_mega_admin(self) -> bool:
        return self.executor.type == ExecutorType.MEGA_ADMIN

    @property
    def is_integration(self) -> bool:
        return self.executor.type == ExecutorType.INTEGRATION

    @property
    def is_copilot(self) -> bool:
        return self.executor.type == ExecutorType.COPILOT


    @property
    def user_id(self) -> StrObjectId:
        return self.executor.id