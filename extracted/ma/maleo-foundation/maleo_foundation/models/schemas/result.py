from pydantic import BaseModel, Field
from typing import Dict, Optional, Union, Any
from maleo_foundation.models.schemas.general import BaseGeneralSchemas
from maleo_foundation.types import BaseTypes

class FieldExpansionMetadata(BaseModel):
    success: bool = Field(..., description="Field expansion's success status")
    code: BaseTypes.OptionalString = Field(None, description="Optional result code")
    message: BaseTypes.OptionalString = Field(None, description="Optional message")
    description: BaseTypes.OptionalString = Field(None, description="Optional description")
    other: BaseTypes.OptionalAny = Field(None, description="Optional other information")

class ResultMetadata(BaseModel):
    field_expansion: Optional[Union[str, Dict[str, FieldExpansionMetadata]]] = Field(None, description="Field expansion metadata")

class BaseResultSchemas:
    class ExtendedPagination(BaseGeneralSchemas.SimplePagination):
        data_count: int = Field(..., description="Fetched data count")
        total_data: int = Field(..., description="Total data count")
        total_pages: int = Field(..., description="Total pages count")

    #* ----- ----- ----- Base ----- ----- ----- *#
    class Base(BaseModel):
        success: bool = Field(..., description="Success status")
        code: BaseTypes.OptionalString = Field(None, description="Optional result code")
        message: BaseTypes.OptionalString = Field(None, description="Optional message")
        description: BaseTypes.OptionalString = Field(None, description="Optional description")
        data: Any = Field(..., description="Data")
        metadata: Optional[ResultMetadata] = Field(None, description="Optional metadata")
        other: BaseTypes.OptionalAny = Field(None, description="Optional other information")

    #* ----- ----- ----- Intermediary ----- ----- ----- *#
    class Fail(Base):
        code: str = "MAL-FAI-001"
        message: str = "Fail result"
        description: str = "Operation failed."
        success: BaseTypes.LiteralFalse = Field(False, description="Success status")
        data: None = Field(None, description="No data")

    class Success(Base):
        success: BaseTypes.LiteralTrue = Field(True, description="Success status")
        code: str = "MAL-SCS-001"
        message: str = "Success result"
        description: str = "Operation succeeded."
        data: Any = Field(..., description="Data")

    #* ----- ----- ----- Derived ----- ----- ----- *#
    class NotFound(Fail):
        code: str = "MAL-NTF-001"
        message: str = "Resource not found"
        description: str = "The requested resource can not be found."
        data: None = Field(None, description="No data")

    class NoData(Success):
        code: str = "MAL-NDT-001"
        message: str = "No data found"
        description: str = "No data found in the requested resource."
        data: None = Field(None, description="No data")

    class SingleData(Success):
        code: str = "MAL-SGD-001"
        message: str = "Single data found"
        description: str = "Requested data found in database."
        data: Any = Field(..., description="Fetched single data")

    class UnpaginatedMultipleData(Success):
        code: str = "MAL-MTD-001"
        message: str = "Multiple unpaginated data found"
        description: str = "Requested unpaginated data found in database."
        data: BaseTypes.ListOfAny = Field(..., description="Unpaginated multiple data")

    class PaginatedMultipleData(
        UnpaginatedMultipleData,
        BaseGeneralSchemas.SimplePagination
    ):
        code: str = "MAL-MTD-002"
        message: str = "Multiple paginated data found"
        description: str = "Requested paginated data found in database."
        total_data: int = Field(..., ge=0, description="Total data count")
        pagination: "BaseResultSchemas.ExtendedPagination" = Field(..., description="Pagination metadata")

BaseResultSchemas.PaginatedMultipleData.model_rebuild()