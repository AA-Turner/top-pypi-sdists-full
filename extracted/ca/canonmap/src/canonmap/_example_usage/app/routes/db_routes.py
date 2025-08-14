# app/routes/db_routes.py

from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from canonmap.connectors.mysql_connector import DBClient

from app.validation import (
  CreateTableBody,
  ImportTableBody,
  CreateFieldBody,
  CreateHelperFieldsBody,
  ExecuteQueryBody,
  AddPrimaryKeyBody,
  DropPrimaryKeyBody,
  AddForeignKeyBody,
  DropForeignKeyBody,
  CreateAutoIncrementPKBody,
  CreateDatabaseBody,
)

router = APIRouter(prefix="/db", tags=["db"])


########################################################
# Database management
########################################################

@router.post("/create-database")
async def create_database(request: Request, body: CreateDatabaseBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(
    db_client.create_database,
    body.database_name,
    if_not_exists=body.if_not_exists,
    charset=body.charset,
    collate=body.collate,
  )
  return {"status": "ok", "result": res}


########################################################
# Table management
########################################################

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


@router.post("/import-table-from-file")
async def import_table_from_file(request: Request, body: ImportTableBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  rows = await run_in_threadpool(
    db_client.import_table_from_file,
    body.file_path,
    body.table_name,
    if_table_exists=body.if_table_exists,
  )
  return {"status": "ok", "rows": rows}



########################################################
# Field management
########################################################

@router.post("/create-field")
async def create_field(request: Request, body: CreateFieldBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(
    db_client.create_field,
    body.table_name,
    body.field_name,
    body.field_ddl,
    if_field_exists=body.if_field_exists,
    first=body.first,
    after=body.after,
    sample_values=body.sample_values,
  )
  return {"status": "ok", "result": res}


@router.post("/create-helper-fields")
async def create_helper_fields(request: Request, body: CreateHelperFieldsBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  await run_in_threadpool(db_client.create_helper_fields, body.model_dump())
  return {"status": "ok"}



########################################################
# Execute queries
########################################################

@router.post("/execute-query")
async def execute_query(request: Request, body: ExecuteQueryBody):
  connector = request.app.state.connector
  result = await run_in_threadpool(
    connector.execute_query, body.query, body.params, body.allow_writes
  )
  return {"status": "ok", "result": result}



########################################################
# Constraint management
########################################################

@router.post("/add-primary-key")
async def add_primary_key(request: Request, body: AddPrimaryKeyBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(db_client.add_primary_key, body.table_name, body.columns, replace=body.replace)
  return {"status": "ok", "result": res}


@router.post("/drop-primary-key")
async def drop_primary_key(request: Request, body: DropPrimaryKeyBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(db_client.drop_primary_key, body.table_name)
  return {"status": "ok", "result": res}


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


@router.post("/drop-foreign-key")
async def drop_foreign_key(request: Request, body: DropForeignKeyBody):
  connector = request.app.state.connector
  db_client = DBClient(connector)
  res = await run_in_threadpool(db_client.drop_foreign_key, body.table_name, body.constraint_name)
  return {"status": "ok", "result": res}


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
