"""OmniDoc 开放 API 的同步客户端。

接口说明见 https://docs.omnidoc.top/ 。典型流程：

    client = OmniDocClient()                      # 读取环境变量 OMNIDOC_API_KEY
    paths = client.translate_file("report.docx", "en", output_dir="out")

Key 只发送给 API 地址；直传的 upload_url 不带 Key。
"""

from __future__ import annotations

import os
import random
import re
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import unquote

import requests

from .errors import JobFailedError, OmniDocError, error_from_response

DEFAULT_BASE_URL = "https://omnidoc.top/api/v1"
TERMINAL_JOB_STATUSES = frozenset({"completed", "failed"})
RETRYABLE_STATUSES = frozenset({429, 500, 502, 503, 504})
QUOTA_EXCEEDED_CODE = "AUTH_API_KEY_QUOTA_EXCEEDED"

PathLike = Union[str, os.PathLike]

_UTF8_FILENAME = re.compile(r"filename\*=UTF-8''([^;]+)", re.IGNORECASE)
_PLAIN_FILENAME = re.compile(r'filename="([^"]+)"', re.IGNORECASE)


def _filename_from_disposition(disposition: str, fallback: str) -> str:
    """从 Content-Disposition 取文件名，只保留最后一段，防止路径穿越。"""
    match = _UTF8_FILENAME.search(disposition)
    if match:
        name = unquote(match.group(1))
    else:
        match = _PLAIN_FILENAME.search(disposition)
        name = match.group(1) if match else fallback
    return Path(name).name or fallback


class OmniDocClient:
    """OmniDoc API 客户端。

    Args:
        api_key: 以 ``sk_`` 开头的 API Key；缺省时读取环境变量 OMNIDOC_API_KEY。
        base_url: API 根地址，默认 https://omnidoc.top/api/v1。
        timeout: (连接超时, 读取超时) 秒数。
        max_retries: 遇到 429 与 5xx 时的最大重试次数（不含首次请求）。
        session: 可选的 requests.Session，便于测试或复用连接。
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: Tuple[float, float] = (10.0, 60.0),
        max_retries: int = 4,
        session: Optional[requests.Session] = None,
    ) -> None:
        key = api_key or os.environ.get("OMNIDOC_API_KEY")
        if not key:
            raise ValueError("需要 API Key：传入 api_key，或设置环境变量 OMNIDOC_API_KEY")
        self._api_key = key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._session = session or requests.Session()

    # ------------------------------------------------------------------ 底层请求

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        stream: bool = False,
    ) -> requests.Response:
        """发送请求，成功返回 Response，失败抛出 OmniDocError。

        429 与 5xx 按 Retry-After 或指数退避重试；AUTH_API_KEY_QUOTA_EXCEEDED 不重试。
        创建类请求重试时会沿用调用方传入的 Idempotency-Key，因此不会重复扣费。
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        attempt = 0
        while True:
            request_headers = {"X-API-Key": self._api_key, **(headers or {})}
            response = self._session.request(
                method,
                url,
                json=json,
                params=params,
                headers=request_headers,
                timeout=self.timeout,
                stream=stream,
            )
            if response.status_code < 400:
                return response

            error = error_from_response(response)
            retryable = response.status_code in RETRYABLE_STATUSES and error.code != QUOTA_EXCEEDED_CODE
            if not retryable or attempt >= self.max_retries:
                raise error

            time.sleep(_retry_delay(response, attempt))
            attempt += 1

    def get_json(self, path: str, **kwargs: Any) -> Any:
        """GET 并返回解析后的 JSON；可调用文档中任何尚未封装的接口。"""
        return self.request("GET", path, **kwargs).json()

    def post_json(self, path: str, json: Any = None, **kwargs: Any) -> Any:
        """POST 并返回解析后的 JSON。"""
        return self.request("POST", path, json=json, **kwargs).json()

    # ------------------------------------------------------------------ 上传

    def upload(self, path: PathLike, *, filename: Optional[str] = None) -> str:
        """上传本地文件并确认，返回文档 ID。

        流程：申请上传地址（presign）→ 直传到 upload_url → 确认（finalize）。
        """
        file_path = Path(path)
        size = file_path.stat().st_size
        ticket = self.post_json(
            "upload/presign",
            json={"filename": filename or file_path.name, "file_size": size},
        )

        put_headers = {**ticket["upload_headers"], "Content-Length": str(size)}
        with file_path.open("rb") as stream:
            # 直传地址不带 API Key，使用模块级 requests.put。
            uploaded = requests.put(
                ticket["upload_url"], headers=put_headers, data=stream, timeout=300
            )
        uploaded.raise_for_status()

        finalized = self.post_json(
            "upload/finalize", json={"finalize_token": ticket["finalize_token"]}
        )
        return finalized["document"]["id"]

    # ------------------------------------------------------------------ 翻译任务

    def create_job(
        self,
        document_id: str,
        target_lang: str,
        *,
        source_lang: Optional[str] = None,
        engine: Optional[str] = None,
        output_mode: Optional[str] = None,
        glossary_id: Optional[str] = None,
        include_images: Optional[bool] = None,
        context_translation: Optional[bool] = None,
        style_preset: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """创建文件翻译任务。

        output_mode 可选 ``single`` 或 ``bilingual``。重试同一次提交时请传入相同的
        idempotency_key；每次新的提交使用新的 UUID（缺省时自动生成）。
        """
        optional = {
            "source_lang": source_lang,
            "engine": engine,
            "output_mode": output_mode,
            "glossary_id": glossary_id,
            "include_images": include_images,
            "context_translation": context_translation,
            "style_preset": style_preset,
        }
        body: Dict[str, Any] = {"document_id": document_id, "target_lang": target_lang}
        body.update({k: v for k, v in optional.items() if v is not None})
        key = idempotency_key or str(uuid.uuid4())
        return self.request(
            "POST", "jobs", json=body, headers={"Idempotency-Key": key}
        ).json()

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """查询任务状态（不扣积分）。"""
        return self.request("GET", f"jobs/{job_id}").json()

    def cancel_job(self, job_id: str) -> Dict[str, Any]:
        """取消任务。取消的任务不会发送 Webhook。"""
        return self.request("POST", f"jobs/{job_id}/cancel").json()

    def wait_job(
        self,
        job_id: str,
        *,
        poll_interval: float = 3.0,
        timeout: float = 1800.0,
    ) -> Dict[str, Any]:
        """轮询直到任务 completed 或 failed，返回最终任务信息。

        生产环境建议改用 Webhook 或 SSE，不要长时间轮询。
        """
        deadline = time.monotonic() + timeout
        while True:
            job = self.get_job(job_id)
            if job.get("status") in TERMINAL_JOB_STATUSES:
                return job
            if time.monotonic() >= deadline:
                raise TimeoutError(f"任务 {job_id} 在 {timeout:.0f} 秒内没有结束")
            time.sleep(poll_interval)

    # ------------------------------------------------------------------ 产物

    def list_artifacts(self, job_id: str) -> List[Dict[str, Any]]:
        """列出任务的产物（不扣积分）。"""
        return self.request("GET", "artifacts", params={"job_id": job_id}).json()

    def download_artifact(
        self,
        artifact_id: str,
        output_dir: PathLike = ".",
        *,
        fallback_name: Optional[str] = None,
    ) -> Path:
        """下载产物到 output_dir，文件名取自响应头，取不到时用 fallback_name。"""
        response = self.request(
            "GET", f"artifacts/{artifact_id}/download", stream=True
        )
        fallback = fallback_name or artifact_id
        name = _filename_from_disposition(
            response.headers.get("Content-Disposition", ""), fallback
        )
        target = Path(output_dir) / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=64 * 1024):
                handle.write(chunk)
        return target

    # ------------------------------------------------------------------ 组合流程

    def translate_file(
        self,
        path: PathLike,
        target_lang: str,
        *,
        output_dir: PathLike = ".",
        poll_interval: float = 3.0,
        timeout: float = 1800.0,
        **options: Any,
    ) -> List[Path]:
        """上传、翻译、等待并下载全部产物，返回下载后的文件路径列表。

        options 会原样传给 create_job（如 output_mode、engine、glossary_id）。
        任务失败时抛出 JobFailedError。
        """
        document_id = self.upload(path)
        job = self.create_job(document_id, target_lang, **options)
        job = self.wait_job(job["id"], poll_interval=poll_interval, timeout=timeout)
        if job.get("status") == "failed":
            raise JobFailedError(job)

        files: List[Path] = []
        for artifact in self.list_artifacts(job["id"]):
            fallback = f"{artifact['id']}.{artifact.get('format') or 'bin'}"
            files.append(
                self.download_artifact(
                    artifact["id"], output_dir, fallback_name=fallback
                )
            )
        return files

    # ------------------------------------------------------------------ 账户与用量

    def credit_balance(self) -> Dict[str, Any]:
        """积分余额（不扣积分）。"""
        return self.get_json("billing/credits/balance")

    def credit_operations(self, **params: Any) -> Any:
        """积分流水，可按文档支持的查询参数过滤（不扣积分）。"""
        return self.get_json("billing/credits/operations", params=params or None)

    def usage_summary(self, **params: Any) -> Any:
        """用量汇总（不扣积分）。"""
        return self.get_json("usage/summary", params=params or None)


def _retry_delay(response: requests.Response, attempt: int) -> float:
    """优先使用 Retry-After；没有时指数退避并加入随机抖动。"""
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        try:
            return max(float(retry_after), 0.0)
        except ValueError:
            pass
    return min(2 ** attempt, 16) + random.random()
