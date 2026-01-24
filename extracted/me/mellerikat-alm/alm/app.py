import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from alm.model import settings
from alm.alo_llm_api import UpdateAPI
from alm.router.file import file_router
from alm.exceptions import AloErrors
from alm.orm import engine

settings.update()

def startup():
    print("app is started.")
    SQLModel.metadata.create_all(engine)
    if settings.experimental_plan.service_api.lifespan.startup:
        settings.experimental_plan.service_api.lifespan.startup()

def shutdown():
    print("app is stopped.")
    if settings.experimental_plan.service_api.lifespan.shutdown:
        settings.experimental_plan.service_api.lifespan.shutdown()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    workers 개수 만큼 반복 동직 작업 반복됨
    :param app:
    :return:
    """
    startup()
    yield
    shutdown()

# app = FastAPI()#(lifespan=lifespan)
aipack_name = os.getenv("AIPACK_NAME", "").strip()

if aipack_name and aipack_name != "/":
    app = FastAPI(
        docs_url=f"/{aipack_name}/docs/api/v1",  # Swagger UI 경로 설정
        openapi_url=f"/{aipack_name}/openapi.json"  # OpenAPI JSON 경로 설정
    )
else:
    app = FastAPI(
        docs_url="/docs/api/v1",  # Swagger UI 경로 설정
        openapi_url="/openapi.json"  # OpenAPI JSON 경로 설정
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def authorize(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)

    docs_path = f"/{aipack_name}/docs/api/v1" if aipack_name and aipack_name != "/" else "/docs/api/v1"
    openapi_path = f"/{aipack_name}/openapi.json" if aipack_name and aipack_name != "/" else "/openapi.json"

    if request.url.path in [docs_path, openapi_path, "/login"]:
        return await call_next(request)

    # 토큰 유효성 검사 로직
    auth = False
    if auth:
        return HTTPException(status_code=400, detail="Invalid authorization")

    request.state.token = {"user": {'id': 0, 'name': "llo"}}
    return await call_next(request)

# # 사전 등록된 API 등록
# app.include_router(file_router)

# system API 등록
update_api = UpdateAPI(settings=settings)
app.include_router(update_api.get_router())

if aipack_name and aipack_name != "/":
    router = APIRouter(prefix=f"/{aipack_name}")
else:
    router = APIRouter()

# router = APIRouter(prefix=f"/{aipack_name}")
if settings.experimental_plan.service_api.path:
    for rule, method_handler in settings.experimental_plan.service_api.path.items():
        for method, handler in method_handler.items():
            components = str(handler.handler).split('.')
            # 단어 리스트 중 'main' 또는 'llo'가 있는지 확인하고, 있으면 에러 발생
            if 'main' in components or 'alo-llm' in components:
                raise AloErrors['ALM-PIP-002']("Error 발생", doc = {"message": f'{handler.handler}는 허용되지 않습니다. "alo-llm"과 "main"은 사용하실 수 없습니다.'})
            else:
                pass
            router.add_api_route(rule, endpoint=handler.get_handler(), methods=[method])
    app.include_router(router)

# user yaml에 정의된 router 등록
for router in settings.experimental_plan.service_api.get_routers():
    app.include_router(router)
