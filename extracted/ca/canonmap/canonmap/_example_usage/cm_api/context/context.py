from contextlib import asynccontextmanager

from fastapi import FastAPI

from canonmap._example_usage.cm_api.context.context_helpers.get_canonmap_helper import get_canonmap
from canonmap._example_usage.cm_api.utils.api_logger import setup_logger

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.canonmap = get_canonmap()
    logger.success("🎉 Your custom API is ready to go!")
    yield

app = FastAPI(lifespan=lifespan)