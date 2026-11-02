from typing import Dict, List, TypedDict

from pydantic import BaseModel, ConfigDict


class WireModel(BaseModel):
    model_config = ConfigDict(strict=True)


class ObjectExistsResponse(WireModel):
    exists: bool


class SignedUrlData(WireModel):
    url: str


class SignedUrlResponse(WireModel):
    data: SignedUrlData


class RecursiveSignedUrlData(WireModel):
    urls: Dict[str, str]


class RecursiveSignedUrlResponse(WireModel):
    data: RecursiveSignedUrlData


class ZeroPartStartUploadData(WireModel):
    version_id: str


class MultipartStartUploadData(WireModel):
    upload_id: str
    urls: List[str]


class ZeroPartStartUploadResponse(WireModel):
    data: ZeroPartStartUploadData


class MultipartStartUploadResponse(WireModel):
    data: MultipartStartUploadData


class CompletedUploadPart(TypedDict):
    ETag: str
    PartNumber: int


class EndUploadData(WireModel):
    version_id: str


class EndUploadResponse(WireModel):
    data: EndUploadData


class UploadResult(TypedDict):
    cache: str
