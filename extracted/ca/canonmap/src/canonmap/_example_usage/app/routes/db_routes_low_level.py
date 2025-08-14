# app/routes/db_routes_low_level.py

from typing import Any

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool

from app.validation import (
    TransactionBody,
    TransactionStatement,
)

router = APIRouter(prefix="/db", tags=["db"])

@router.post("/initialize-pool")
async def initialize_pool(request: Request):
  connector = request.app.state.connector
  await run_in_threadpool(connector.initialize_pool)
  return {"status": "ok"}


@router.post("/close-pool")
async def close_pool(request: Request):
  connector = request.app.state.connector
  await run_in_threadpool(connector.close_pool)
  return {"status": "ok"}


@router.post("/transaction")
async def transaction(request: Request, body: TransactionBody):
  connector = request.app.state.connector

  def _run(statements: list[TransactionStatement]):
    results: list[Any] = []
    with connector.transaction() as conn:
      cursor = conn.cursor(dictionary=True)
      try:
        for st in statements:
          cursor.execute(st.query, st.params or [])
          if cursor.with_rows:
            results.append(cursor.fetchall())
          else:
            results.append({"affected_rows": cursor.rowcount})
      finally:
        cursor.close()
    return results

  results = await run_in_threadpool(_run, body.statements)
  return {"status": "ok", "results": results}


