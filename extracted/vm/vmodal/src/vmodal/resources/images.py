from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal.models import (
    ImageUrlResponse,
    ImageUrlBulkResponse,
    ImageGetBulkResponse,
)
from vmodal.routes import ENDPOINTS, full


class ImagesResource:
    """Image-serving endpoints. Identity: explicit `userid` wins, else
    the SDK's configured user_id (sent as X-User-Id). Fail-closed server-side."""

    def __init__(self, http):
        self.http = http

    async def get_url(
        self,
        mode: str,
        group_name: str,
        modality: str,
        filename: str,
        stream_name: str = "astream",
        ts_unix_13digits: Optional[Union[str, int]] = None,
        userid: Optional[str] = None,
    ) -> ImageUrlResponse:
        data = {
            "mode": mode,
            "group_name": group_name,
            "modality": modality,
            "stream_name": stream_name,
            "filename": filename,
        }
        if ts_unix_13digits is not None:
            data["ts_unix_13digits"] = str(ts_unix_13digits)
        if userid:
            data["userid"] = userid
        body = await self.http.request("POST", full(ENDPOINTS.image_get_url), json=data)
        return ImageUrlResponse.model_validate(body)

    async def get_url_bulk(
        self,
        records: List[Dict[str, Any]],
        userid: Optional[str] = None,
    ) -> ImageUrlBulkResponse:
        data = {"records": list(records or [])}
        if userid:
            data["userid"] = userid
        body = await self.http.request("POST", full(ENDPOINTS.image_get_url_bulk), json=data)
        return ImageUrlBulkResponse.model_validate(body)

    async def get_image_from_url(
        self,
        url_pre_signed: str,
        userid: Optional[str] = None,
    ) -> bytes:
        data = {"url_pre_signed": url_pre_signed}
        if userid:
            data["userid"] = userid
        return await self.http.request_bytes("POST", full(ENDPOINTS.image_get_image), json=data)

    async def get_image_bulk_from_urls(
        self,
        urls: List[str],
        userid: Optional[str] = None,
    ) -> ImageGetBulkResponse:
        data = {"urls": list(urls or [])}
        if userid:
            data["userid"] = userid
        body = await self.http.request("POST", full(ENDPOINTS.image_get_image_bulk), json=data)
        return ImageGetBulkResponse.model_validate(body)


if __name__ == "__main__":
    fire.Fire()
