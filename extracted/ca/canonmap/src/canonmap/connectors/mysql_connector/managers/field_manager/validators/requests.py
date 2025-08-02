# canonmap/services/database/mysql/managers/field_manager/validators/requests.py

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from canonmap.connectors.mysql_connector.managers.field_manager.validators.models import (
    TableField,
    FieldTransformType,
)
from canonmap.connectors.mysql_connector.utils.mysql_data_types import MySQLDataType
from canonmap.connectors.mysql_connector.validators.models import IfExists


#### GENERAL FIELD MANAGEMENT ####
class CreateFieldRequest(BaseModel):
    field: TableField
    data_type: MySQLDataType = Field(default=MySQLDataType.VARCHAR)
    length: Optional[str] = None  # e.g. "(255)" or "(10,2)"
    nullable: bool = True
    default: Optional[str] = None
    auto_increment: bool = False
    primary_key: bool = False

    def ddl_sql(self) -> str:
        # Compose SQL fragment for this field
        length = self.length
        # Add default length if required and not set
        if MySQLDataType.needs_length_specification(self.data_type) and not length:
            length = MySQLDataType.get_default_length(self.data_type.value)
        type_part = f"{self.data_type.value}{length or ''}"
        nullable = "NULL" if self.nullable else "NOT NULL"
        default = f"DEFAULT {self.default}" if self.default is not None else ""
        auto_inc = "AUTO_INCREMENT" if self.auto_increment else ""
        pk = "PRIMARY KEY" if self.primary_key else ""
        return f"`{self.field.name}` {type_part} {nullable} {default} {auto_inc} {pk}".strip()

class CreateFieldsRequest(BaseModel):
    fields: List[TableField]
    data_type: MySQLDataType = MySQLDataType.VARCHAR
    length: Optional[str] = None
    nullable: bool = True
    default: Optional[str] = None
    auto_increment: bool = False
    primary_key: bool = False
    parallel: bool = False

class DropFieldRequest(BaseModel):
    field: TableField

class DropFieldsRequest(BaseModel):
    fields: List[TableField]
    parallel: bool = False



#### HELPER FIELD MANAGEMENT ####
ALLOWED_HELPER_EXISTS = {IfExists.REPLACE, IfExists.ERROR, IfExists.SKIP, IfExists.FILL_EMPTY}

class CreateHelperFieldRequest(BaseModel):
    field: TableField
    transform_type: FieldTransformType
    chunk_size: int = 10000
    if_helper_exists: IfExists = IfExists.ERROR

    @field_validator('if_helper_exists')
    def validate_helper_exists(cls, v):
        if v not in ALLOWED_HELPER_EXISTS:
            raise ValueError(f"if_helper_exists must be one of: {[e.value for e in ALLOWED_HELPER_EXISTS]}")
        return v

class CreateHelperFieldsRequest(BaseModel):
    fields: List[TableField]
    transform_type: FieldTransformType
    chunk_size: int = 10000
    parallel: bool = False
    if_helper_exists: IfExists = IfExists.ERROR

    @field_validator('if_helper_exists')
    def validate_helper_exists(cls, v):
        if v not in ALLOWED_HELPER_EXISTS:
            raise ValueError(f"if_helper_exists must be one of: {[e.value for e in ALLOWED_HELPER_EXISTS]}")
        return v

class CreateHelperFieldAllTransformsRequest(BaseModel):
    field: TableField
    chunk_size: int = 10000
    parallel: bool = False
    if_helper_exists: IfExists = IfExists.ERROR

    @field_validator('if_helper_exists')
    def validate_helper_exists(cls, v):
        if v not in ALLOWED_HELPER_EXISTS:
            raise ValueError(f"if_helper_exists must be one of: {[e.value for e in ALLOWED_HELPER_EXISTS]}")
        return v

class CreateHelperFieldsAllTransformsRequest(BaseModel):
    fields: List[TableField]
    chunk_size: int = 10000
    parallel: bool = False
    if_helper_exists: IfExists = IfExists.ERROR

    @field_validator('if_helper_exists')
    def validate_helper_exists(cls, v):
        if v not in ALLOWED_HELPER_EXISTS:
            raise ValueError(f"if_helper_exists must be one of: {[e.value for e in ALLOWED_HELPER_EXISTS]}")
        return v

class DropHelperFieldRequest(BaseModel):
    field: TableField
    field_transform_type: FieldTransformType

class DropHelperFieldsRequest(BaseModel):
    fields: List[TableField]
    field_transform_type: FieldTransformType
    parallel: bool = False

class DropHelperFieldAllTransformsRequest(BaseModel):
    field: TableField
    parallel: bool = False

class DropHelperFieldsAllTransformsRequest(BaseModel):
    fields: List[TableField]
    parallel: bool = False


#### INDEX FIELD MANAGEMENT ####
class CreateIndexFieldRequest(BaseModel):
    index_field: TableField
    index_name: Optional[str] = None
    index_type: str = "BTREE"
    unique: bool = False
    if_exists: IfExists = IfExists.ERROR

class CreateIndexFieldsRequest(BaseModel):
    index_fields: List[TableField]
    index_name: Optional[str] = None
    index_type: str = "BTREE"
    unique: bool = False
    if_exists: IfExists = IfExists.ERROR

class DropIndexFieldRequest(BaseModel):
    index_field: TableField
    index_name: Optional[str] = None
    if_exists: IfExists = IfExists.ERROR

class DropIndexFieldsRequest(BaseModel):
    index_fields: List[TableField]
    index_name: Optional[str] = None
    if_exists: IfExists = IfExists.ERROR
    parallel: bool = False


#### PRIMARY KEY MANAGEMENT ####
class AttachPrimaryKeyToFieldRequest(BaseModel):
    field: TableField

class DropPrimaryKeyFromFieldRequest(BaseModel):
    field: TableField
