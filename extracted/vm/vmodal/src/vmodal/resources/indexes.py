from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from pydantic import ValidationError
from vmodal.errors import ApiError, FeatureDisabled, ValidationFailed
from vmodal.models import (
    IndexationJobsListResponse,
    IndexationSubmitRequest,
    IndexationSubmitResponse,
    IndexationStatusResponse,
    IndexationDeleteRequest,
    IndexationDeleteResponse,
)
from vmodal.routes import ENDPOINTS, full


class IndexesResource:
    def __init__(self, http):
        self.http = http

    async def _index_status_from_jobs_list(self, job_id: str) -> Optional[IndexationStatusResponse]:
        res = await self.jobs_list(limit=1000)
        data = res.model_dump() if hasattr(res, "model_dump") else dict(getattr(res, "__dict__", {}) or {})
        rows = list(data.get("jobs") or []) + list(data.get("data") or [])
        for row in rows:
            item = row.model_dump() if hasattr(row, "model_dump") else dict(row or {})
            if str(item.get("job_id") or "").strip() == job_id:
                return IndexationStatusResponse.model_validate(item)
        return None

    async def jobs_list(self, status: Optional[str] = None, mode: Optional[str] = None, group_name: Optional[str] = None, limit: int = 200) -> IndexationJobsListResponse:
        if int(limit) < 1 or int(limit) > 1000:
            raise ValidationFailed("limit must be between 1 and 1000", status_code=422)
        params = {"limit": int(limit)}
        if status is not None:
            params["status"] = status
        if mode is not None:
            params["mode"] = mode
        if group_name is not None:
            params["group_name"] = group_name
        body = await self.http.request("GET", full(ENDPOINTS.indexation_jobs), params=params)
        return IndexationJobsListResponse.model_validate(body)

    async def create_index(
        self,
        mode: str = "",
        group_name: str = "",
        index_type: Optional[str] = None,
        modality: Optional[str] = None,
        stream_name: Optional[str] = None,
        insert_mode: str = "append",
        create_index: bool = True,
        version: str = "new_version",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        embedding_model: Optional[str] = None,
        re_process: bool = False,
        dry_run: bool = False,
        **kw,
    ) -> IndexationSubmitResponse:
        data = dict(kw)
        data.pop("user_id", None)
        data.update(
            {
                "mode": mode,
                "group_name": group_name,
                "index_type": index_type,
                "modality": modality,
                "stream_name": stream_name,
                "insert_mode": insert_mode,
                "create_index": create_index,
                "version": version,
                "start_date": start_date,
                "end_date": end_date,
                "embedding_model": embedding_model,
                "re_process": re_process,
                "dry_run": dry_run,
            }
        )
        try:
            req = IndexationSubmitRequest.model_validate(data)
        except ValidationError as exc:
            raise ValidationFailed("validation failed", status_code=422, details=exc.errors()) from exc
        body = await self.http.request("POST", full(ENDPOINTS.indexation_submit), json=req.model_dump(exclude_none=True))
        return IndexationSubmitResponse.model_validate(body)

    async def index_status(self, job_id: str = "") -> IndexationStatusResponse:
        job_id = str(job_id or "").strip()
        if not job_id:
            raise ValidationFailed("job_id is required", status_code=422)
        path = ENDPOINTS.indexation_status.format(job_id=job_id)
        try:
            body = await self.http.request("GET", full(path))
        except ApiError as exc:
            if int(getattr(exc, "status_code", 0) or 0) != 404:
                raise
            item = await self._index_status_from_jobs_list(job_id)
            if item is None:
                raise
            return item
        return IndexationStatusResponse.model_validate(body)

    async def delete_index(
        self,
        mode: str = "",
        group_name: str = "",
        version: str = "",
        modality: Optional[str] = None,
        dry_run: bool = False,
        confirm: bool = False,
        **kw,
    ) -> IndexationDeleteResponse:
        data = dict(kw)
        data.pop("user_id", None)
        data.update(
            {
                "mode": mode,
                "group_name": group_name,
                "version": version,
                "modality": modality,
                "dry_run": dry_run,
                "confirm": confirm,
            }
        )
        try:
            req = IndexationDeleteRequest.model_validate(data)
        except ValidationError as exc:
            raise ValidationFailed("validation failed", status_code=422, details=exc.errors()) from exc
        body = await self.http.request("DELETE", full(ENDPOINTS.indexation_delete), json=req.model_dump(exclude_none=True))
        return IndexationDeleteResponse.model_validate(body)

    async def embedding_models(self, **kw):
        raise FeatureDisabled("embedding models endpoint is disabled on server")


if __name__ == "__main__":
    fire.Fire()
