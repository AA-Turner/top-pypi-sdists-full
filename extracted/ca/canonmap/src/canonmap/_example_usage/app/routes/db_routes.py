# app/routes/db_routes.py

from typing import Union, Literal, Any
from pydantic import BaseModel, PositiveInt

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from canonmap.connectors.mysql_connector.db_client import DBClient

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


class ImportTableBody(BaseModel):
  file_path: str
  table_name: str | None = None
  if_exists: Literal["append","replace","fail"] = "append"


@router.post("/import-table-from-file")
async def import_table_from_file(request: Request, body: ImportTableBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  rows = await run_in_threadpool(
    db_client.import_table_from_file,
    body.file_path,
    body.table_name,
    if_exists=body.if_exists,
  )
  return {"status": "ok", "rows": rows}


# Low-level endpoints mapping to connector.py methods

class ExecuteQueryBody(BaseModel):
  query: str
  params: list[Any] | None = None
  allow_writes: bool = False


@router.post("/execute-query")
async def execute_query(request: Request, body: ExecuteQueryBody):
  connector = request.app.state.connector
  result = await run_in_threadpool(
    connector.execute_query, body.query, body.params, body.allow_writes
  )
  return {"status": "ok", "result": result}


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


class TransactionStatement(BaseModel):
  query: str
  params: list[Any] | None = None


class TransactionBody(BaseModel):
  statements: list[TransactionStatement]


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


class AddPrimaryKeyBody(BaseModel):
  table_name: str
  columns: list[str]
  replace: bool = False


@router.post("/add-primary-key")
async def add_primary_key(request: Request, body: AddPrimaryKeyBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(db_client.add_primary_key, body.table_name, body.columns, replace=body.replace)
  return {"status": "ok", "result": res}


class DropPrimaryKeyBody(BaseModel):
  table_name: str


@router.post("/drop-primary-key")
async def drop_primary_key(request: Request, body: DropPrimaryKeyBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(db_client.drop_primary_key, body.table_name)
  return {"status": "ok", "result": res}


class AddForeignKeyBody(BaseModel):
  table_name: str
  columns: list[str]
  ref_table: str
  ref_columns: list[str]
  constraint_name: str | None = None
  on_delete: Literal["CASCADE","SET NULL","RESTRICT","NO ACTION"] | None = None
  on_update: Literal["CASCADE","SET NULL","RESTRICT","NO ACTION"] | None = None
  replace: bool = False


@router.post("/add-foreign-key")
async def add_foreign_key(request: Request, body: AddForeignKeyBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(
    db_client.add_foreign_key,
    body.table_name,
    body.columns,
    body.ref_table,
    body.ref_columns,
    constraint_name=body.constraint_name,
    on_delete=body.on_delete,
    on_update=body.on_update,
    replace=body.replace,
  )
  return {"status": "ok", "result": res}


# High-level endpoints mapping to DBClient methods not yet covered

class CreateTableBody(BaseModel):
  table_name: str
  fields_ddl: str
  if_not_exists: bool = True
  temporary: bool = False
  table_options: str | None = None


@router.post("/create-table")
async def create_table(request: Request, body: CreateTableBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(
    db_client.create_table,
    body.table_name,
    body.fields_ddl,
    if_not_exists=body.if_not_exists,
    temporary=body.temporary,
    table_options=body.table_options,
  )
  return {"status": "ok", "result": res}


class CreateFieldBody(BaseModel):
  table_name: str
  field_name: str
  field_ddl: str | None = None
  if_exists: Literal["error","skip","replace"] = "error"
  first: bool = False
  after: str | None = None
  sample_values: list[Any] | None = None


@router.post("/create-field")
async def create_field(request: Request, body: CreateFieldBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(
    db_client.create_field,
    body.table_name,
    body.field_name,
    body.field_ddl,
    if_exists=body.if_exists,
    first=body.first,
    after=body.after,
    sample_values=body.sample_values,
  )
  return {"status": "ok", "result": res}


class CreateAutoIncrementPKBody(BaseModel):
  table_name: str
  field_name: str = "id"
  replace: bool = False
  unsigned: bool = True
  start_with: int | None = None


@router.post("/create-auto-increment-pk")
async def create_auto_increment_pk(request: Request, body: CreateAutoIncrementPKBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(
    db_client.create_auto_increment_pk,
    body.table_name,
    body.field_name,
    replace=body.replace,
    unsigned=body.unsigned,
    start_with=body.start_with,
  )
  return {"status": "ok", "result": res}


class DropForeignKeyBody(BaseModel):
  table_name: str
  constraint_name: str


@router.post("/drop-foreign-key")
async def drop_foreign_key(request: Request, body: DropForeignKeyBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(db_client.drop_foreign_key, body.table_name, body.constraint_name)
  return {"status": "ok", "result": res}
