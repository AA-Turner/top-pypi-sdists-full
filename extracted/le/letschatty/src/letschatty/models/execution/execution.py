from letschatty.models.utils.types import StrObjectId
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional, Union
from pydantic import BaseModel, Field
from bson import ObjectId
from .executor import Executor, ExecutorType
from letschatty.models.analytics.sources import Source
from letschatty.models.company.assets.users.user import User
from letschatty.models.channels.request_account import RequestAccount
from letschatty.models.whatsapp.account_context import AccountContext

class ExecutionContext(BaseModel):
    trace_id: StrObjectId = Field(default_factory=lambda: str(ObjectId()))
    start_time: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))
    metadata: dict = Field(default_factory=dict)
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    executor: Executor
    event_time: Optional[datetime] = None
    company_id: StrObjectId
    chain_of_thought_id: Optional[StrObjectId] = Field(default=None, description="If the execution is related to the decision of an ai agent, this will be the id of the chain of thought that was used to make the decision so we can use it to check if the decision is valid")
    workflow_id: Optional[str] = Field(default=None, description="If the execution is a copilot automation (workflow) sending a message/template, this is the originating workflow id, stamped onto the message context for attribution")
    wpp_apb_mode: bool = Field(default=False, description="If the execution is related to the wpp apb mode")
    account: Optional[Union[AccountContext, RequestAccount]] = Field(default=None, exclude=True, description="The account this request acts as (multi-account), of any channel: WhatsApp's is an `AccountContext` (ADR-011 §12, E3). A Union and not just the base: built from a dict, the account must still come out as an `AccountContext` (smart union picks the member that keeps every field). Set by the webhook entry (from the number the webhook arrived on) or by an endpoint that resolved it. Never serialized: it carries the account token")
    agents_can_see_unassigned_chats: bool = Field(default=True, description="Company-wide chat visibility rule for restricted users (plain agents), copied off `messaging_settings.agents_can_see_unassigned_chats` by the route layer. True (the default, and the historical behavior) means an agent sees their own chats plus every unassigned one; False means they only ever see the chats assigned to them. Defaults to True so any context built outside the request path keeps the old behavior instead of silently emptying a list.")

    resolved_accounts: dict = Field(default_factory=dict, exclude=True, repr=False, description="Per-request memo of the accounts already resolved for a chat ((company_id, account_id) -> (monotonic time, AccountContext)), so one send does not read the same account and WABA once per message. Owned by api-chatty's account resolution, which bounds its age. Never serialized: it carries account tokens")
    allowed_account_ids: Optional[list[Optional[str]]] = Field(default=None, exclude=True, description="Account floor of the person behind the request, stamped by the route layer from `users.account_ids` (see services/whatsapp_accounts/account_floor.py). None (the default) = every account: webhooks, lambdas, system, copilot, integrations and the Owner. A list = only the chats of those accounts; a None entry in the list means 'chats with no account', which belong to the default account. Never serialized: it is an authorization of this request, not data of the event.")

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