from pydantic import BaseModel


class WorkerInfo(BaseModel):
    scheduler_url: str
    namespace: str
    tls: bool = False


class ExecutorIdentityResult(BaseModel):
    customer_id: str
    workspace_id: str
    user_id: str | None = None
    organization_id: str | None = None


class ExecutorIdentityTokenResult(BaseModel):
    token: str
