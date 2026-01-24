from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional, Annotated

from dotenv import find_dotenv

try:
    import uvicorn
    from fastapi import FastAPI, Header, HTTPException, Request, BackgroundTasks, Depends, Query, Response
    from fastapi.responses import RedirectResponse
    from sqlmodel import Session, SQLModel, create_engine, select
except ImportError:
    raise ImportError(
        "fastapi, uvicorn, and sqlmodel are required to run this script. "
        "Please install them with 'pip3 install ipfabric[webhook]."
    )

from ipfabric.models import WebhookEvent
from ipfabric.scripts.webhook import (
    calc_method,
    query_db,
    verify_signature,
    WebhookConfig,
    WebhookResponse,
    AnnotatedWebhookEvent,
)

find_dotenv(usecwd=True) or Path("~").expanduser().joinpath(".env")
SETTINGS = WebhookConfig()
ENGINE = create_engine(SETTINGS.database_url, connect_args={"check_same_thread": False})


def get_session():
    with Session(ENGINE) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(ENGINE)
    yield


app = FastAPI(title=SETTINGS.title, lifespan=lifespan)


@app.get("/", response_class=RedirectResponse)
async def redirect_root():
    """Redirect to API docs"""
    return "/docs"


@app.get("/healthcheck", response_model=str)
async def healthcheck():
    """Simple healthcheck endpoint"""
    return "Ok"


@app.get("/snapshots/")
def read_snapshots(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=1000)] = 100,
    snapshotId: Optional[str] = None,
) -> WebhookResponse:
    return WebhookResponse(**query_db(session, "snapshots", offset, limit, snapshotId))


@app.get("/intents/")
def read_intents(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=1000)] = 100,
    snapshotId: Optional[str] = None,
) -> WebhookResponse:
    return WebhookResponse(**query_db(session, "intents", offset, limit, snapshotId))


@app.get("/events/")
def read_events(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=1000)] = 100,
    snapshotId: Optional[str] = None,
) -> WebhookResponse:
    return WebhookResponse(**query_db(session, "events", offset, limit, snapshotId))


@app.get("/events/{dbId}")
def read_event(
    dbId: int,
    session: SessionDep,
) -> WebhookEvent:
    _ = session.exec(select(WebhookEvent).where(WebhookEvent.dbId == dbId)).first()
    return _ or Response(content="Not Found", status_code=404)


@app.post(SETTINGS.webhook_path)
async def webhook(
    event: AnnotatedWebhookEvent,
    request: Request,
    bg_tasks: BackgroundTasks,
    session: SessionDep,
    x_ipf_signature: str = Header(None),
):
    """IP Fabric Webhook Endpoint"""
    if not (_ := await verify_signature(request, x_ipf_signature, SETTINGS.ipf_secret))[0]:
        raise HTTPException(status_code=401, detail=_[1])

    return calc_method(event, bg_tasks, session, SETTINGS)


def main():
    uvicorn.run(
        "ipfabric.scripts.webhook_api:app",
        host=SETTINGS.uvicorn_ip,
        port=SETTINGS.uvicorn_port,
        reload=SETTINGS.uvicorn_reload,
    )


if __name__ == "__main__":
    main()
