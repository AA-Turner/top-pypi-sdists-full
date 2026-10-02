from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from pydantic import ValidationError
from vmodal.errors import ValidationFailed
from vmodal.models import SearchRequest_frontui_In, SearchResponse_frontui
from vmodal.routes import ENDPOINTS, full


class SearchesResource:
    def __init__(self, http):
        self.http = http

    async def search_video(
        self,
        query_text: str = "",
        query_metadata: Optional[Dict[str, Any]] = None,
        image_query: Optional[str] = None,
        mode: str = "vid_file",
        group_name: str = "agroup",
        stream_name: str = "astream",
        search_sources: Optional[List[str]] = None,
        search_combine_mode: str = "union",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        offset: int = 0,
        limit: int = 50,
        text_emb_score_min: float = 0.90,
        image_emb_score_min: float = 1.5,
        version_lancedb: Optional[int] = None,
        **kw,
    ) -> SearchResponse_frontui:
        data = dict(kw)
        data.pop("user_id", None)
        data.update(
            {
                "query_text": query_text,
                "query_metadata": query_metadata,
                "image_query": image_query,
                "mode": mode,
                "group_name": group_name,
                "stream_name": stream_name,
                "search_sources": search_sources or ["ocr", "asr", "image"],
                "search_combine_mode": search_combine_mode,
                "start_date": start_date,
                "end_date": end_date,
                "offset": offset,
                "limit": limit,
                "text_emb_score_min": text_emb_score_min,
                "image_emb_score_min": image_emb_score_min,
                "version_lancedb": version_lancedb,
            }
        )
        try:
            req = SearchRequest_frontui_In.model_validate(data)
        except ValidationError as exc:
            raise ValidationFailed("validation failed", status_code=422, details=exc.errors()) from exc
        body = await self.http.request("POST", full(ENDPOINTS.search_client), json=req.model_dump(exclude_none=True))
        return SearchResponse_frontui.model_validate(body)


if __name__ == "__main__":
    fire.Fire()
