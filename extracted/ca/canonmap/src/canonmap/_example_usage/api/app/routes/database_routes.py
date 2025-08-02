# app/routes/db_routes.py

from fastapi import APIRouter, Request, HTTPException
from canonmap.connectors.mysql_connector import DatabaseManager, CreateDatabaseRequest
from canonmap.connectors.mysql_connector.managers.database_manager.validators.requests import GenerateSchemaRequest
from canonmap.exceptions import DatabaseManagerError

router = APIRouter(prefix="/database", tags=["database"])

@router.post("/create-database")
async def create_database(request: Request, create_database_request: CreateDatabaseRequest):
    try:
        connector = request.app.state.mysql_connector
        db_manager = DatabaseManager(connector)
        result = db_manager.create_database(create_database_request)
        
        if result["action"] == "created":
            return {"message": f"Database {create_database_request.database_name} created successfully"}
        elif result["action"] == "skipped":
            return {"message": f"Database {create_database_request.database_name} already exists (skipped due to {result['mode']} mode)"}
        elif result["action"] == "cancelled":
            return {"message": f"Database {create_database_request.database_name} creation cancelled by user"}
        else:
            return {"message": f"Database {create_database_request.database_name} operation completed"}
    except DatabaseManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/get-databases")
async def get_databases(request: Request):
    try:
        connector = request.app.state.mysql_connector
        db_manager = DatabaseManager(connector)
        return db_manager.get_databases()
    except DatabaseManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/generate-schema")
async def generate_schema(request: Request, generate_schema_request: GenerateSchemaRequest):
    try:
        connector = request.app.state.mysql_connector
        db_manager = DatabaseManager(connector)
        schema_path = db_manager.generate_schema(generate_schema_request)
        return {
            "message": f"Schema generated successfully",
            "schema_path": schema_path,
            "schema_name": generate_schema_request.schema_name,
            "database_name": generate_schema_request.database.name
        }
    except DatabaseManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))