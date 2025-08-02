import logging
from fastapi import APIRouter, Request, HTTPException

from canonmap.connectors.mysql_connector.managers.field_manager.validators.requests import (
    CreateFieldRequest,
    CreateFieldsRequest,
    DropFieldRequest,
    DropFieldsRequest,
    CreateHelperFieldRequest,
    CreateHelperFieldsRequest,
    CreateHelperFieldAllTransformsRequest,
    CreateHelperFieldsAllTransformsRequest,
    DropHelperFieldRequest,
    DropHelperFieldsRequest,
    DropHelperFieldAllTransformsRequest,
    DropHelperFieldsAllTransformsRequest,
    CreateIndexFieldRequest,
    CreateIndexFieldsRequest,
    DropIndexFieldRequest,
    DropIndexFieldsRequest,
    AttachPrimaryKeyToFieldRequest,
    DropPrimaryKeyFromFieldRequest
)
from canonmap.connectors.mysql_connector.managers.field_manager.field_manager import FieldManager
from canonmap.exceptions import FieldManagerError

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/field", tags=["field"])

#### GENERAL FIELD MANAGEMENT ####
@router.post("/create-field")
async def create_field(request: Request, create_field_request: CreateFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.create_field(create_field_request)
        return {"message": f"Field created"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-fields")
async def create_fields(request: Request, create_fields_request: CreateFieldsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.create_fields(create_fields_request)
        return {"message": f"Fields created"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-field")
async def drop_field(request: Request, drop_field_request: DropFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.drop_field(drop_field_request)
        return {"message": f"Field dropped"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-fields")
async def drop_fields(request: Request, drop_fields_request: DropFieldsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.drop_fields(drop_fields_request)
        return {"message": f"Fields dropped"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))



#### HELPER FIELD MANAGEMENT ####
@router.post("/create-helper-field")
async def create_helper_field(request: Request, create_helper_field_request: CreateHelperFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.create_helper_field(create_helper_field_request)
        return {"message": f"Helper field created"}
    except FieldManagerError as e:
        logger.error(f"FieldManagerError in create_helper_field: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-helper-fields")
async def create_helper_fields(request: Request, create_helper_fields_request: CreateHelperFieldsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.create_helper_fields(create_helper_fields_request)
        return {"message": f"Helper fields created"}
    except FieldManagerError as e:
        logger.error(f"FieldManagerError in create_helper_fields: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-helper-field-all-transforms")
async def create_helper_field_all_transforms(request: Request, create_helper_field_all_transforms_request: CreateHelperFieldAllTransformsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.create_helper_field_all_transforms(create_helper_field_all_transforms_request)
        return {"message": f"Helper field all transforms created"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-helper-fields-all-transforms")
async def create_helper_fields_all_transforms(request: Request, create_helper_fields_all_transforms_request: CreateHelperFieldsAllTransformsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.create_helper_fields_all_transforms(create_helper_fields_all_transforms_request)
        return {"message": f"Helper fields all transforms created"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-helper-field")
async def drop_helper_field(request: Request, drop_helper_field_request: DropHelperFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.drop_helper_field(drop_helper_field_request)
        return {"message": f"Helper field dropped"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-helper-fields")
async def drop_helper_fields(request: Request, drop_helper_fields_request: DropHelperFieldsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.drop_helper_fields(drop_helper_fields_request)
        return {"message": f"Helper fields dropped"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-helper-field-all-transforms")
async def drop_helper_field_all_transforms(request: Request, drop_helper_field_all_transforms_request: DropHelperFieldAllTransformsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.drop_helper_field_all_transforms(drop_helper_field_all_transforms_request)
        return {"message": f"Helper field all transforms dropped"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-helper-fields-all-transforms")
async def drop_helper_fields_all_transforms(request: Request, drop_helper_fields_all_transforms_request: DropHelperFieldsAllTransformsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.drop_helper_fields_all_transforms(drop_helper_fields_all_transforms_request)
        return {"message": f"Helper fields all transforms dropped"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))



#### INDEX FIELD MANAGEMENT ####
@router.post("/create-index-field")
async def create_index_field(request: Request, create_index_field_request: CreateIndexFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        index_name = field_manager.create_index_field(create_index_field_request)
        return {"message": f"Index created", "index_name": index_name}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/create-index-fields")
async def create_index_fields(request: Request, create_index_fields_request: CreateIndexFieldsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        index_names = field_manager.create_index_fields(create_index_fields_request)
        return {"message": f"Indexes created", "index_names": index_names}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-index-field")
async def drop_index_field(request: Request, drop_index_field_request: DropIndexFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        index_name = field_manager.drop_index_field(drop_index_field_request)
        return {"message": f"Index dropped", "index_name": index_name}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-index-fields")
async def drop_index_fields(request: Request, drop_index_fields_request: DropIndexFieldsRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        index_names = field_manager.drop_index_fields(drop_index_fields_request)
        return {"message": f"Indexes dropped", "index_names": index_names}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))



#### CONSTRAINT MANAGEMENT ####
@router.post("/attach-primary-key")
async def attach_primary_key(request: Request, attach_primary_key_request: AttachPrimaryKeyToFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.attach_primary_key_to_field(attach_primary_key_request)
        return {"message": f"Primary key attached"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/drop-primary-key")
async def drop_primary_key(request: Request, drop_primary_key_request: DropPrimaryKeyFromFieldRequest):
    try:
        connector = request.app.state.mysql_connector
        field_manager = FieldManager(connector)
        field_manager.drop_primary_key_from_field(drop_primary_key_request)
        return {"message": f"Primary key dropped"}
    except FieldManagerError as e:
        raise HTTPException(status_code=400, detail=str(e))