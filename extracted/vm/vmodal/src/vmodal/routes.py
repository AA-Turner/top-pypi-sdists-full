from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire

PREFIX = "/api/external/v1"
USERS_API_PREFIX = "/api/v1"
_EXTERNAL_UPLOAD_GET_SIGNED_URL = "/collections/external_upload_get_signed_url"
_EXTERNAL_UPLOAD_DONE = "/collection/upload/done"
_EXTERNAL_UPLOAD_FINALIZE = _EXTERNAL_UPLOAD_DONE
_EXTERNAL_UPLOAD_MULTIPART_CREATE = "/collections/external_upload_multipart/create"
_EXTERNAL_UPLOAD_MULTIPART_SIGN_PARTS = "/collections/external_upload_multipart/sign_parts"
_EXTERNAL_UPLOAD_MULTIPART_STATUS = "/collections/external_upload_multipart/status"
_EXTERNAL_UPLOAD_MULTIPART_COMPLETE = "/collections/external_upload_multipart/complete"
_EXTERNAL_UPLOAD_MULTIPART_ABORT = "/collections/external_upload_multipart/abort"


@dataclass(frozen=True)
class apiEndpoints:
    health: str = "/health"
    search_client: str = "/search"
    groups: str = "/collection/groups"
    indexation_jobs: str = "/indexation/jobs"
    indexation_submit: str = "/indexation/job/create"
    indexation_status: str = "/indexation/job/{job_id}"
    indexation_delete: str = "/indexation/index/delete"
    upload: str = "/collection/upload"
    upload_folder: str = "/upload/folder"
    upload_google_drive_folder: str = "/collection/upload/google_drive"
    upload_metadata_jsonl: str = "/collection/upload/metadata"
    collection_description_update: str = "/collection/description/update"
    # Source of truth: vmx_avideo/infra/search_api_ui/routers/apionly_routes.py
    # The SDK/gateway surface is api/external + search_api_ui api/internal.
    # api/mobile is a different namespace and is not used by this SDK.
    upload_metadata_item_parquet_internal: str = "/api/internal/v1/collection/upload/metadata"
    collection_delete: str = "/collection/delete"
    collection_add_assets: str = "/collection/{collection_id}/assets/create"
    admin_user_stats: str = "/admin/user-stats"
    image_get_url: str = "/image/get_url"
    image_get_url_bulk: str = "/image/get_url_bulk"
    image_get_image: str = "/image/get_image"
    image_get_image_bulk: str = "/image/get_image_bulk"


ENDPOINTS = apiEndpoints()


@dataclass(frozen=True)
class apiUsersEndpoints:
    auth_me: str = "/auth/me"
    admin_usage: str = "/admin/usage"
    admin_cache_stats: str = "/admin/cache/stats"
    r2_credentials: str = "/get_r2_credentials/"
    r2_upload_file: str = "/upload_file/"
    r2_upload_folder_video: str = "/upload_folder_video/"


USERS_ENDPOINTS = apiUsersEndpoints()

ACTIVE_ENDPOINTS = {
    "auth.health": ("GET", ENDPOINTS.health),
    "auth.auth_check": ("GET", ENDPOINTS.health),
    "searches.search_video": ("POST", ENDPOINTS.search_client),
    "collections.list_groups": ("GET", ENDPOINTS.groups),
    "collections.upload_google_drive_folder": ("POST", ENDPOINTS.upload_google_drive_folder),
    "collections.upload_metadata_jsonl": ("POST", ENDPOINTS.upload_metadata_jsonl),
    "collections.update_description": ("POST", ENDPOINTS.collection_description_update),
    "collections.delete": ("DELETE", ENDPOINTS.collection_delete),
    "collections.add_assets": ("POST", ENDPOINTS.collection_add_assets),
    "indexes.jobs_list": ("GET", ENDPOINTS.indexation_jobs),
    "indexes.create_index": ("POST", ENDPOINTS.indexation_submit),
    "indexes.index_status": ("GET", ENDPOINTS.indexation_status),
    "indexes.delete_index": ("DELETE", ENDPOINTS.indexation_delete),
    "admin.user_stats": ("GET", ENDPOINTS.admin_user_stats),
    "images.get_url": ("POST", ENDPOINTS.image_get_url),
    "images.get_url_bulk": ("POST", ENDPOINTS.image_get_url_bulk),
    "images.get_image_from_url": ("POST", ENDPOINTS.image_get_image),
    "images.get_image_bulk_from_urls": ("POST", ENDPOINTS.image_get_image_bulk),
}

DISABLED_ENDPOINTS = {
    "collections.upload_folder": ("POST", "/upload/folder"),  # cannot scan remote PC/laptop folders
    "indexes.embedding_models": ("GET", "/indexes/embedding_models"),
    "collections.auto_index_get": ("GET", "/collection/auto_index"),
    "collections.auto_index_set": ("POST", "/collection/auto_index"),
    "collections.create": ("NONE", ""),
    "collections.edit": ("NONE", ""),
    "gdrive.private_auth_url": ("POST", "/gdrive/private/auth-url"),
    "gdrive.private_download": ("POST", "/gdrive/private/folder/download"),
    "sql.query": ("POST", "/sql/query"),
}


def full(path: str) -> str:
    path = str(path or "")
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{PREFIX}{path}"


def users_full(path: str) -> str:
    path = str(path or "")
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{USERS_API_PREFIX}{path}"


if __name__ == "__main__":
    fire.Fire({"full": full, "users_full": users_full, "active": ACTIVE_ENDPOINTS, "disabled": DISABLED_ENDPOINTS})
