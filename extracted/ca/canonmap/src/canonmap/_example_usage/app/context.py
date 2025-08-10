# app/context.py

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from canonmap.connectors.mysql_connector.config import MySQLConfig
from canonmap.connectors.mysql_connector.connector import MySQLConnector
from canonmap.mapping.mapping_pipeline import MappingPipeline

load_dotenv(override=True)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting lifespan")
    config = MySQLConfig(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )
    connector = MySQLConnector(config)
    connector.initialize_pool()
    app.state.connector = connector
    app.state.mapping_pipeline = MappingPipeline(connector)
    yield
    logger.info("Closing lifespan")
    try:
        connector.close_pool()
        logger.info("Pool closed successfully")
    except Exception as e:
        logger.error(f"Error closing pool: {e}")
    logger.info("Closed lifespan")
