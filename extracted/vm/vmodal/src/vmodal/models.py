from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator


class VBaseModel(BaseModel):
    model_config = ConfigDict(extra="allow")


class SearchRequest_frontui_In(VBaseModel):
    query_text: str = ""
    query_metadata: Optional[Dict[str, Any]] = None
    image_query: Optional[str] = None
    mode: str = "vid_file"
    group_name: str = "agroup"
    stream_name: str = "astream"
    search_sources: List[str] = Field(default_factory=lambda: ["ocr", "asr", "image"])
    search_combine_mode: str = "union"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    offset: int = 0
    limit: int = 50
    text_emb_score_min: float = 0.90
    image_emb_score_min: float = 1.5
    version_lancedb: Optional[int] = None

    @model_validator(mode="after")
    def check_query(self):
        text_ok = str(self.query_text or "").strip()
        image_ok = self.image_query not in (None, "", b"")
        if not text_ok and not image_ok:
            raise ValueError("query_text or image_query is required")
        return self


class SearchResultItem_frontui(VBaseModel):
    pass


class SearchResponse_frontui(VBaseModel):
    data: List[SearchResultItem_frontui] = Field(default_factory=list)
    cnt_actual: int = 0
    cnt_total: int = 0
    execution_time_ms: float = 0


class GroupItem(VBaseModel):
    pass


class GroupsResponse(VBaseModel):
    data: List[GroupItem] = Field(default_factory=list)
    total: int = 0
    execution_time_ms: float = 0


class ExternalUploadSignedUrlResponse(VBaseModel):
    user_id: str = ""
    expires_in: int = 0
    key: str = ""
    url: str = ""
    method: str = "PUT"


class MultipartPart(VBaseModel):
    part_number: int
    etag: str = ""
    size_bytes: int = 0


class MultipartSignedPart(VBaseModel):
    part_number: int
    url: str
    method: str = "PUT"
    headers: Dict[str, str] = Field(default_factory=dict)


class MultipartCreateResponse(VBaseModel):
    request_id: str
    upload_id: str
    key: str
    size_bytes: int
    part_size_bytes: int
    part_count: int
    status: str = "created"


class MultipartSignResponse(VBaseModel):
    parts: List[MultipartSignedPart] = Field(default_factory=list)
    expires_in: int = 0


class MultipartStatusResponse(VBaseModel):
    status: str = "uploading"
    parts: List[MultipartPart] = Field(default_factory=list)
    etag: str = ""
    size_bytes: int = 0


class MultipartCompleteResponse(VBaseModel):
    status: str = "completed"
    key: str
    etag: str = ""
    size_bytes: int
    already_completed: bool = False


class VideoUploadResponse(ExternalUploadSignedUrlResponse):
    filepath_local: str = ""
    filename: str = ""
    size_bytes: int = 0
    status_code: int = 0
    uploaded: bool = False
    upload_strategy: str = "single"
    upload_id: str = ""
    etag: str = ""
    part_size_bytes: int = 0
    part_count: int = 1
    parts_uploaded: int = 0
    resumed: bool = False
    attempt_count: int = 0
    upload_done: Dict[str, Any] = Field(default_factory=dict)
    dest_path: str = ""


class VideoUploadBulkResponse(VBaseModel):
    data: List[VideoUploadResponse] = Field(default_factory=list)
    total: int = 0


class FolderUploadItem(VBaseModel):
    pass


class FolderUploadResponse(VBaseModel):
    data: List[FolderUploadItem] = Field(default_factory=list)


class GoogleDriveFolderUploadResponse(VBaseModel):
    pass


class MetadataParquetUploadResponse(VBaseModel):
    pass


class CollectionDescriptionUpdateResponse(VBaseModel):
    pass


class DeleteCollectionRequest(VBaseModel):
    group_name: str
    mode: str
    scope: str = "all"
    dry_run: bool = False
    confirm: bool = False


class DeleteCollectionResponse(VBaseModel):
    pass


class CollectionAsset(VBaseModel):
    pass


class CollectionAddAssetsRequest(VBaseModel):
    collection_id: str
    mode: str
    group_name: str
    stream_name: str = "astream"
    asset_ids: List[str] = Field(default_factory=list)


class CollectionAddAssetsResponse(VBaseModel):
    pass


class IndexationJobItem(VBaseModel):
    pass


class IndexationJobsListResponse(VBaseModel):
    data: List[IndexationJobItem] = Field(default_factory=list)
    total: int = 0


class IndexationSubmitRequest(VBaseModel):
    mode: str
    group_name: str
    stream_name: Optional[str] = None
    index_type: Optional[str] = None
    modality: Optional[str] = None
    insert_mode: str = "append"
    create_index: bool = True
    version: str = "new_version"
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    embedding_model: Optional[str] = None
    re_process: bool = False
    dry_run: bool = False


class IndexationSubmitResponse(VBaseModel):
    job_id: str = ""
    status: str = ""


class IndexationStatusResponse(VBaseModel):
    job_id: str = ""
    status: str = ""


class IndexationDeleteRequest(VBaseModel):
    mode: str
    group_name: str
    modality: Optional[str] = None
    version: str
    dry_run: bool = False
    confirm: bool = False


class IndexationDeleteResponse(VBaseModel):
    status: str = ""


class AdminUserStatItem(VBaseModel):
    pass


class AdminUserStatsResponse(VBaseModel):
    data: List[AdminUserStatItem] = Field(default_factory=list)
    total: int = 0


class UserProfile(VBaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    roles: List[Any] = Field(default_factory=list)
    tenant_id: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)
    type: str = "user"


class UsageUserDetail(VBaseModel):
    date: str = ""
    user_id: str = ""
    total: int = 0
    endpoints: Dict[str, int] = Field(default_factory=dict)


class CacheStats(VBaseModel):
    apikey_cache_size: int = 0
    rate_limiter_buckets: int = 0
    config: Dict[str, Any] = Field(default_factory=dict)


class R2CredentialsResponse(VBaseModel):
    user_id: str = ""
    access_key_id: str = ""
    secret_key: str = ""
    session_token: str = ""
    expiry_date: str = ""
    vmodal_r2_endpoint_url: str = ""
    vmodal_base_prefix: str = ""
    vmodal_bucket: str = ""
    CLI_USER_R2_BUCKET_DATA_UPLOAD: str = ""
    CLI_USER_PREFIX_DATA_UPLOAD: str = ""


class PresignedUploadResponse(VBaseModel):
    user_id: str = ""
    expires_in: int = 0
    key: str = ""
    url: str = ""
    method: str = "PUT"


class PresignedFolderItem(VBaseModel):
    filename: str = ""
    key: str = ""
    url: str = ""
    method: str = "PUT"


class PresignedFolderResponse(VBaseModel):
    user_id: str = ""
    expires_in: int = 0
    files: List[PresignedFolderItem] = Field(default_factory=list)


class ImageRecord(VBaseModel):
    mode: str = ""
    group_name: str = ""
    stream_name: str = "astream"
    filename: str = ""
    frame_id: str = ""
    userid: Optional[str] = None


class ImageResponse(VBaseModel):
    found: bool = False
    img_base64: str = ""
    mode: str = ""
    group_name: str = ""
    stream_name: str = ""
    filename: str = ""
    frame_id: str = ""


class FullPathImageResponse(VBaseModel):
    found: bool = False
    img_base64: str = ""
    fullpath: str = ""


class ImageBulkResponse(VBaseModel):
    records: List[Dict[str, Any]] = Field(default_factory=list)


class ImageUrlRecord(VBaseModel):
    mode: str = ""
    group_name: str = ""
    modality: str = ""
    stream_name: str = "astream"
    filename: str = ""
    ts_unix_13digits: Optional[str] = None


class ImageUrlResponse(VBaseModel):
    found: bool = False
    url_pre_signed: str = ""
    full_path: str = ""
    expire_sec: int = 72000
    mode: str = ""
    group_name: str = ""
    modality: str = ""
    stream_name: str = ""
    filename: str = ""
    ts_unix_13digits: str = ""
    error: str = ""


class ImageUrlBulkResponse(VBaseModel):
    records: List[Dict[str, Any]] = Field(default_factory=list)


class ImageGetBulkResponse(VBaseModel):
    records: List[Dict[str, Any]] = Field(default_factory=list)


class HealthResponse(VBaseModel):
    status: str = ""
    timestamp: Optional[str] = None
    version: Optional[str] = None
    python_version: Optional[str] = None
    dependencies: Any = None


if __name__ == "__main__":
    fire.Fire()
