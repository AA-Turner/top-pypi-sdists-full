from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import asyncio
import json
import fire
from pydantic import ValidationError
from vmodal.config import SdkConfig, str_users_base_url
from vmodal.errors import ApiError, AuthError, ValidationFailed


class Http:
    def __init__(self, cfg: SdkConfig):
        self.cfg = cfg
        self._client = None

    async def _get_client(self):
        if self._client is not None:
            return self._client
        import httpx

        self._client = httpx.AsyncClient(base_url=self.cfg.base_url, timeout=self.cfg.timeout)
        return self._client

    def _headers(self, force_token: bool = False, require_user_id: bool = True) -> Dict[str, str]:
        user_id = str(self.cfg.user_id or "").strip()
        if require_user_id and not user_id:
            raise AuthError("user_id is required", status_code=401)
        out = {}
        if user_id:
            out["X-User-Id"] = user_id
        if self.cfg.tenant_id:
            out["X-Tenant-Id"] = self.cfg.tenant_id
        if self.cfg.email:
            out["X-User-Email"] = self.cfg.email
        if self.cfg.token and (force_token or str(self.cfg.mode or "").lower() != "direct"):
            out["Authorization"] = "Bearer " + str(self.cfg.token)
        return out

    def _users_api_url(self, path: str) -> str:
        path = str(path or "")
        if path.startswith("http://") or path.startswith("https://"):
            return path
        if not path.startswith("/"):
            path = "/" + path
        return str_users_base_url(self.cfg.base_url) + path

    def _decode_body(self, response) -> Any:
        ctype = str(response.headers.get("content-type", ""))
        if "application/json" in ctype:
            return response.json()
        try:
            return response.json()
        except Exception:
            return response.text

    def _raise_for_status(self, response) -> None:
        if 200 <= int(response.status_code) < 300:
            return
        body = self._decode_body(response)
        if int(response.status_code) == 401:
            raise AuthError("authentication failed", status_code=401, body=body)
        if int(response.status_code) == 422:
            details = body.get("detail") if isinstance(body, dict) else body
            raise ValidationFailed("validation failed", status_code=422, body=body, details=details)
        raise ApiError("api request failed", status_code=int(response.status_code), body=body)

    async def request(
        self,
        method: str,
        path: str,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        params: Any = None,
    ) -> Any:
        client = await self._get_client()
        headers = self._headers()
        attempts = max(1, self.cfg.max_retries + 1)
        last_exc = None
        for i in range(attempts):
            try:
                res = await client.request(
                    str(method).upper(),
                    path,
                    json=json,
                    data=data,
                    files=files,
                    params=params,
                    headers=headers,
                )
                if int(res.status_code) in (500, 502, 503, 504) and i + 1 < attempts:
                    await asyncio.sleep(0.05 * (i + 1))
                    continue
                self._raise_for_status(res)
                return self._decode_body(res)
            except AuthError:
                raise
            except ValidationFailed:
                raise
            except ApiError as exc:
                last_exc = exc
                if exc.status_code in (500, 502, 503, 504) and i + 1 < attempts:
                    await asyncio.sleep(0.05 * (i + 1))
                    continue
                raise
            except Exception as exc:
                last_exc = exc
                name = exc.__class__.__name__.lower()
                if "timeout" in name and i + 1 < attempts:
                    await asyncio.sleep(0.05 * (i + 1))
                    continue
                raise ApiError("transport error", body=str(exc)) from exc
        if isinstance(last_exc, Exception):
            raise last_exc
        raise ApiError("request failed")

    async def request_users(
        self,
        method: str,
        path: str,
        json: Any = None,
        params: Any = None,
    ) -> Any:
        if not str(self.cfg.token or "").strip():
            raise AuthError("token is required for users_api routes", status_code=401)
        client = await self._get_client()
        headers = self._headers(force_token=True, require_user_id=False)
        res = await client.request(
            str(method).upper(),
            self._users_api_url(path),
            json=json,
            params=params,
            headers=headers,
        )
        self._raise_for_status(res)
        return self._decode_body(res)

    async def request_bytes(
        self,
        method: str,
        path: str,
        json: Any = None,
        data: Any = None,
        files: Any = None,
        params: Any = None,
    ) -> bytes:
        client = await self._get_client()
        headers = self._headers()
        attempts = max(1, self.cfg.max_retries + 1)
        last_exc = None
        for i in range(attempts):
            try:
                res = await client.request(
                    str(method).upper(),
                    path,
                    json=json,
                    data=data,
                    files=files,
                    params=params,
                    headers=headers,
                )
                if int(res.status_code) in (500, 502, 503, 504) and i + 1 < attempts:
                    await asyncio.sleep(0.05 * (i + 1))
                    continue
                self._raise_for_status(res)
                return bytes(res.content or b"")
            except AuthError:
                raise
            except ValidationFailed:
                raise
            except ApiError as exc:
                last_exc = exc
                if exc.status_code in (500, 502, 503, 504) and i + 1 < attempts:
                    await asyncio.sleep(0.05 * (i + 1))
                    continue
                raise
            except Exception as exc:
                last_exc = exc
                name = exc.__class__.__name__.lower()
                if "timeout" in name and i + 1 < attempts:
                    await asyncio.sleep(0.05 * (i + 1))
                    continue
                raise ApiError("transport error", body=str(exc)) from exc
        if isinstance(last_exc, Exception):
            raise last_exc
        raise ApiError("request failed")

    async def aclose(self):
        client = self._client
        self._client = None
        if client is not None:
            await client.aclose()


if __name__ == "__main__":
    fire.Fire()
