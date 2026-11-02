"""Read-only API adapter for Job and Group share tokens."""

from __future__ import annotations

from dataclasses import replace
from typing import Any
from urllib.parse import quote, quote_plus

import requests

from .api import APIClient, APIError, PaginationProtocolError, TimeoutType


class ShareAPIClient(APIClient):
    """Use existing export/CLI readers against the token-scoped share routes."""

    is_share = True

    def __init__(self, config, token: str, *, group_id: str | None = None):
        if not token or not token.strip():
            raise ValueError("--share-token must not be empty")
        # The share token is the only credential for these public routes.
        headers = {
            key: value
            for key, value in config.headers.items()
            if key.lower()
            not in {
                "authorization",
                "x-api-key",
                "cookie",
                "proxy-authorization",
                "x-access-token",
                "x-apiserver-token",
            }
        }
        safe_config = replace(config, headers=headers, token_key=None, verbose_redaction=True)
        super().__init__(safe_config)
        self.share_token = token.strip()
        self.share_group_id = group_id

    @classmethod
    def from_client(cls, client: APIClient, token: str, *, group_id: str | None = None):
        return cls(client.config, token, group_id=group_id)

    def _group_path(self, group_id: str, suffix: str = "") -> str:
        if self.share_group_id != group_id:
            raise ValueError("Group share token requires its matching group ID")
        return f"/share/view/groups/{quote(group_id, safe='')}{suffix}"

    def _job_path(self, job_id: str, suffix: str = "") -> str:
        encoded_job = quote(job_id, safe="")
        return f"/share/view/jobs/{encoded_job}{suffix}"

    def _share_get(self, path: str, *, timeout: TimeoutType = None, **params: Any) -> Any:
        kwargs = {"timeout": timeout} if timeout is not None else {}
        return self._get(path, params={"token": self.share_token, **params}, **kwargs)

    def _token_spellings(self) -> set[str]:
        return {
            self.share_token,
            quote(self.share_token, safe=""),
            quote_plus(self.share_token),
        }

    def _redact_token(self, value: Any) -> str:
        result = str(value)
        for secret in self._token_spellings():
            if secret:
                result = result.replace(secret, "<redacted>")
        return result

    def _redacted_response(self, response: requests.Response | None) -> requests.Response | None:
        if response is None:
            return None
        safe = requests.Response()
        safe.status_code = response.status_code
        safe.headers.update(
            {key: self._redact_token(value) for key, value in response.headers.items()}
        )
        safe.url = self._redact_token(response.url or "")
        safe.reason = self._redact_token(response.reason or "")
        content = response.content
        for secret in self._token_spellings():
            if secret:
                content = content.replace(secret.encode("utf-8"), b"<redacted>")
        safe._content = content
        return safe

    def _request(self, *args, **kwargs):
        try:
            return super()._request(*args, **kwargs)
        except APIError as exc:
            # requests errors and server error bodies can echo the query string.
            raise APIError(
                exc.status_code,
                self._redact_token(exc.detail),
                exc.request_id,
                self._redacted_response(exc.response),
            ) from None

    def _log_request(self, method, url, request_id, headers, params, body, **kwargs) -> None:
        # The generic verbose redactor does not classify a plain `token` key.
        safe_params = dict(params or {})
        if params and "token" in params:
            safe_params["token"] = "<redacted>"
        super()._log_request(method, url, request_id, headers, safe_params, body, **kwargs)

    def _log_exception(self, method, url, request_id, duration_ms, exc) -> None:
        super()._log_exception(
            method,
            url,
            request_id,
            duration_ms,
            exc,
            error_detail=self._redact_token(exc),
        )

    def _log_retry(
        self, method, url, request_id, attempt, max_attempts, delay, *, status=None, error=None
    ) -> None:
        super()._log_retry(
            method,
            url,
            request_id,
            attempt,
            max_attempts,
            delay,
            status=status,
            error=self._redact_token(error) if error is not None else None,
        )

    def _summarize_response(self, resp, raw) -> str:
        return self._redact_token(super()._summarize_response(resp, raw))

    def get_group(self, group_id: str, timeout: TimeoutType = None) -> dict:
        return self._share_get(self._group_path(group_id), timeout=timeout)

    def get_group_stats(self, group_id: str, timeout: TimeoutType = None) -> dict:
        return self.get_group(group_id, timeout=timeout)

    def list_jobs(
        self, *, group_id: str | None = None, skip: int = 0, limit: int = 100, **kwargs
    ) -> dict:
        if group_id is None:
            raise ValueError("Group share token requires --group-id to list jobs")
        return self._share_get(self._group_path(group_id, "/jobs"), skip=skip, limit=limit)

    def get_group_eval_summary(self, group_id: str) -> dict:
        return self._share_get(self._group_path(group_id, "/eval_summary"))

    def get_group_eval(self, group_id: str) -> dict:
        result = self.get_group_eval_summary(group_id)
        tasks: list[dict] = []
        while True:
            page = self._share_get(
                self._group_path(group_id, "/eval_tasks"), skip=len(tasks), limit=500
            )
            batch = page.get("tasks")
            total = page.get("total")
            if not isinstance(batch, list) or not isinstance(total, int) or total < 0:
                raise PaginationProtocolError("invalid share eval task page")
            tasks.extend(batch)
            if len(tasks) >= total:
                break
            if not batch:
                raise PaginationProtocolError("share eval tasks ended before total")
        return {**result, "per_task": tasks}

    def get_job(
        self,
        job_id: str,
        *,
        include_params: bool = False,
        include_spec: bool = False,
        spec_format: str = "json",
        timeout: TimeoutType = None,
    ) -> dict:
        result = self._share_get(self._job_path(job_id), timeout=timeout)
        # Share responses include these payloads unconditionally; preserve the
        # existing CLI opt-in presentation contract.
        result = dict(result)
        if not include_params:
            result.pop("params", None)
        if not include_spec:
            result.pop("job_spec_data", None)
        elif spec_format == "yaml" and isinstance(result.get("job_spec_data"), dict):
            import yaml

            spec_data = dict(result["job_spec_data"])
            if "spec" in spec_data:
                spec_data["spec_yaml"] = yaml.safe_dump(
                    spec_data["spec"], allow_unicode=True, sort_keys=False
                )
            result["job_spec_data"] = spec_data
        return result

    def get_job_metrics(self, job_id: str) -> dict:
        return self._share_get(self._job_path(job_id, "/metrics"))

    def get_job_events(self, job_id: str, container: str | None = None) -> dict:
        params = {"container": container} if container else {}
        return self._share_get(self._job_path(job_id, "/events"), **params)

    def get_job_containers(self, job_id: str) -> dict:
        return self._share_get(self._job_path(job_id, "/containers"))

    def get_job_logs(
        self,
        job_id: str,
        container: str | None = None,
        offset: int | None = 0,
        limit: int | None = 500,
    ) -> dict:
        params: dict[str, Any] = {}
        if container:
            params["container"] = container
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        return self._share_get(self._job_path(job_id, "/logs"), **params)

    def get_job_artifacts(self, job_ids: list[str], *, download_mode=None) -> list:
        if download_mode is not None:
            raise ValueError("share artifact endpoint does not accept download_mode")
        items: list = []
        for job_id in job_ids:
            items.extend(self._share_get(self._job_path(job_id, "/artifacts")))
        return items
