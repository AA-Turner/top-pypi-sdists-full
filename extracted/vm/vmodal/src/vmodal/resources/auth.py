from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal.models import HealthResponse, UserProfile
from vmodal.routes import ENDPOINTS, USERS_ENDPOINTS, full, users_full


class AuthResource:
    def __init__(self, http):
        self.http = http

    async def health(self) -> HealthResponse:
        body = await self.http.request("GET", full(ENDPOINTS.health))
        return HealthResponse.model_validate(body)

    async def auth_check(self, user_id: str = "") -> bool:
        old_user = self.http.cfg.user_id
        if str(user_id or "").strip():
            self.http.cfg.user_id = str(user_id).strip()
        try:
            await self.health()
            return True
        finally:
            self.http.cfg.user_id = old_user

    async def me(self) -> UserProfile:
        body = await self.http.request_users("GET", users_full(USERS_ENDPOINTS.auth_me))
        return UserProfile.model_validate(body)


if __name__ == "__main__":
    fire.Fire()
