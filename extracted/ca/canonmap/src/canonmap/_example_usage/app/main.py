# app/main.py

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from canonmap.logger import make_console_handler

from .context import lifespan
from .routes.entity_routes import router as entity_router
from .routes.db_routes import router as db_router

make_console_handler(set_root=True)
logger = logging.getLogger(__name__)

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(entity_router)
app.include_router(db_router)
