# src/app/routes/table_routes.py

from fastapi import APIRouter, Request, HTTPException

from canonmap.connectors.mysql_connector.managers.table_manager.validators.requests import CreateTableRequest, DropTableRequest
from canonmap.connectors.mysql_connector.managers.table_manager.table_manager import TableManager
from canonmap.exceptions import TableManagerError

router = APIRouter(prefix="/table", tags=["table"])

@router.post("/create-table")
async def create_table(request: Request, create_table_request: CreateTableRequest):
    try:
        connector = request.app.state.mysql_connector
        table_manager = TableManager(connector)
        result = table_manager.create_table(create_table_request)
        
        if result["action"] == "created":
            if result["reason"] == "new_table_with_data":
                return {"message": f"Table {create_table_request.name} created successfully with {result.get('rows_inserted', 0)} rows"}
            else:
                return {"message": f"Table {create_table_request.name} created successfully"}
        elif result["action"] == "skipped":
            return {"message": f"Table {create_table_request.name} already exists (skipped due to {result['mode']} mode)"}
        elif result["action"] == "error":
            return {"message": f"Table {create_table_request.name} creation failed: {result['reason']}"}
        else:
            return {"message": f"Table {create_table_request.name} operation completed"}
    except TableManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-table")
async def drop_table(request: Request, drop_table_request: DropTableRequest):
    try:
        connector = request.app.state.mysql_connector
        table_manager = TableManager(connector)
        table_manager.drop_table(drop_table_request)
        return {"message": f"Table {drop_table_request.name} dropped"}
    except TableManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))
