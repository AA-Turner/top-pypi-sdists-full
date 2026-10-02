from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal.models import R2CredentialsResponse, PresignedUploadResponse, PresignedFolderResponse
from vmodal.routes import USERS_ENDPOINTS, users_full


class R2Resource:
    def __init__(self, http):
        self.http = http

    async def get_credentials(self, dir_prefix: str = "") -> R2CredentialsResponse:
        params = {}
        if str(dir_prefix or "").strip():
            params["dir_prefix"] = str(dir_prefix).strip()
        body = await self.http.request_users("GET", users_full(USERS_ENDPOINTS.r2_credentials), params=params or None)
        return R2CredentialsResponse.model_validate(body)

    async def presign_upload_file(
        self,
        mode: str,
        group_name: str,
        stream_name: str,
        modality: str,
        filename: str,
        expires_in: int = 86400,
    ) -> PresignedUploadResponse:
        params = {
            "mode": mode,
            "group_name": group_name,
            "stream_name": stream_name,
            "modality": modality,
            "filename": filename,
            "expires_in": expires_in,
        }
        body = await self.http.request_users("GET", users_full(USERS_ENDPOINTS.r2_upload_file), params=params)
        return PresignedUploadResponse.model_validate(body)

    async def presign_upload_folder_video(
        self,
        mode: str,
        group_name: str,
        stream_name: str,
        filenames: List[str],
        expires_in: int = 86400,
    ) -> PresignedFolderResponse:
        data = {
            "mode": mode,
            "group_name": group_name,
            "stream_name": stream_name,
            "filenames": list(filenames or []),
            "expires_in": expires_in,
        }
        body = await self.http.request_users("POST", users_full(USERS_ENDPOINTS.r2_upload_folder_video), json=data)
        return PresignedFolderResponse.model_validate(body)


if __name__ == "__main__":
    fire.Fire()
