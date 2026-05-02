from connector_sdk_types import AnnotatedField, SemanticType
from pydantic import BaseModel


class AccioRequest(BaseModel):
    object_name: str


class AccioResponse(BaseModel):
    success: bool


class SampleRequest(BaseModel):
    account_id: str = AnnotatedField(title="Account ID", semantic_type=SemanticType.ACCOUNT_ID)


class SampleResponse(BaseModel):
    success: bool
