from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal.models import AdminUserStatsResponse, CacheStats, UsageUserDetail
from vmodal.routes import ENDPOINTS, USERS_ENDPOINTS, full, users_full


class AdminResource:
    def __init__(self, http):
        self.http = http

    async def user_stats(self) -> AdminUserStatsResponse:
        body = await self.http.request("GET", full(ENDPOINTS.admin_user_stats))
        return AdminUserStatsResponse.model_validate(body)

    async def usage(self, date: str = "") -> UsageUserDetail:
        params = {}
        if str(date or "").strip():
            params["date"] = str(date).strip()
        body = await self.http.request_users("GET", users_full(USERS_ENDPOINTS.admin_usage), params=params or None)
        return UsageUserDetail.model_validate(body)

    async def cache_stats(self) -> CacheStats:
        body = await self.http.request_users("GET", users_full(USERS_ENDPOINTS.admin_cache_stats))
        return CacheStats.model_validate(body)

if __name__ == "__main__":
    fire.Fire()
