# app/routes/db_routes.py

from typing import Union, Literal
from pydantic import BaseModel, PositiveInt

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from canonmap.connectors.mysql_connector.mysql_db_client import DBClient

class TableFieldObj(BaseModel):
    table_name: str
    field_name: str

TableFieldIn = Union[str, TableFieldObj]

class CreateHelperFieldsBody(BaseModel):
    table_fields: list[TableFieldIn]
    all_transforms: bool = True
    transform_type: Literal["initialism","phonetic","soundex"] | None = None
    if_helper_exists: Literal["replace","append","error","skip","fill_empty"] = "error"
    chunk_size: PositiveInt = 10000
    parallel: bool = False

router = APIRouter(prefix="/db", tags=["db"])

@router.post("/create-helper-fields")
async def create_helper_fields(request: Request, body: CreateHelperFieldsBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  await run_in_threadpool(db_client.create_helper_fields, body.model_dump())
  return {"status": "ok"}
