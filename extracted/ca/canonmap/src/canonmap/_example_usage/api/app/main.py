from fastapi import FastAPI
from canonmap import make_console_handler

from app.context import lifespan
from app.routes.match_routes import router as match_router
from app.routes.database_routes import router as database_router
from app.routes.table_routes import router as table_router
from app.routes.field_routes import router as field_router

make_console_handler(set_root=True)

app = FastAPI(lifespan=lifespan)

app.include_router(match_router)
app.include_router(database_router)
app.include_router(table_router)
app.include_router(field_router)