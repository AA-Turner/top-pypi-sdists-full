# app/routes/low_level_db_routes.py

import logging

from fastapi import Request, APIRouter

from canonmap.connectors.mysql_connector.models import QueryRequest, QueryResult
from canonmap.connectors.mysql_connector.db_client import DBClient
from fastapi.concurrency import run_in_threadpool
from fastapi.exceptions import HTTPException
from mysql.connector import Error as MySQLError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/db", tags=["db"])

@router.post("/read")
async def read(req: QueryRequest, request: Request):
    db = DBClient(request.app.state.connector)
    logger.info(f"Reading query: {req.query}")
    try:
        rows = await run_in_threadpool(db.execute_read, req.query, req.params)
        return QueryResult(rows=rows)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.post("/write")
async def write(req: QueryRequest, request: Request):
    db = DBClient(request.app.state.connector)
    logger.info(f"Writing query: {req.query}")
    try:
        result = await run_in_threadpool(db.execute_write, req.query, req.params)
        return QueryResult(affected_rows=result["affected_rows"])
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

