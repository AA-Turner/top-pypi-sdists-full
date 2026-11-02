"""API client."""

import json
import math
import os
import platform
import re
import sys
import time
import uuid
from email.utils import parsedate_to_datetime
from typing import Any, Literal, Optional, Union
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit

import requests
from urllib3.util import Timeout as HTTPTimeout

from .config import Config, ConfigurationError, get_config, has_cluster_header
from .managed_ak import require_managed_ak_ack, validate_ak_id, validate_ak_selection

_DEFAULT_CONNECT_TIMEOUT = 300
_DEFAULT_READ_TIMEOUT = 86400

TimeoutType = Union[float, tuple[Optional[float], Optional[float]], None]


def _validate_credential_source_selection(
    *,
    account_pool: Optional[str],
    credential_type: Any,
    params: Optional[dict],
    params_list: Optional[list],
) -> None:
    """Reject ambiguous Account Pool and Template Credential submissions."""
    if not isinstance(account_pool, str) or not account_pool.strip():
        return
    candidates = [credential_type]
    if isinstance(params, dict):
        candidates.append(params.get("credential_type"))
    for item in params_list or []:
        if isinstance(item, dict):
            candidates.append(item.get("credential_type"))
    if any(value is not None and str(value).strip() for value in candidates):
        raise ValueError(
            "--account-pool and --credential-type cannot be used together; "
            "Account Pool account types are defined by the Bench Configuration"
        )


def _default_timeout() -> tuple[Optional[float], Optional[float]]:
    return (
        _timeout_env_or_default("AP_CONNECT_TIMEOUT", _DEFAULT_CONNECT_TIMEOUT),
        _timeout_env_or_default("AP_REQUEST_TIMEOUT", _DEFAULT_READ_TIMEOUT),
    )


def _timeout_env_or_default(name: str, default: float) -> Optional[float]:
    value = os.environ.get(name)
    if value is None or not value.strip():
        return default
    try:
        parsed = float(value)
    except ValueError as exc:
        raise ConfigurationError(f"{name} must be a number") from exc
    if parsed == 0:
        return None
    if parsed < 0 or not math.isfinite(parsed):
        raise ConfigurationError(f"{name} must be a finite number greater than or equal to 0")
    return parsed


def _merge_checkpoint_payload(
    checkpoint: Optional[dict],
    checkpoint_id: Optional[str],
    checkpoint_path: Optional[str],
) -> Optional[dict]:
    """Merge a raw checkpoint object with explicit id/path flags.

    Explicit ``id`` / ``path`` win over the same keys inside the raw object.
    Returns ``None`` (no checkpoint) when nothing non-empty is supplied.
    """
    payload = dict(checkpoint or {})
    if checkpoint_id is not None:
        payload["id"] = checkpoint_id
    if checkpoint_path is not None:
        payload["path"] = checkpoint_path
    return payload or None


def _normalize_explicit_timeout(timeout: TimeoutType) -> TimeoutType:
    if isinstance(timeout, (int, float)) and timeout == 0:
        return None
    if isinstance(timeout, tuple):
        return tuple(None if value == 0 else value for value in timeout)  # type: ignore[return-value]
    return timeout


_GROUP_ARTIFACTS_PAGE_SIZE = 500
_DATASET_PAGE_SIZE = 500
_DATASET_INSTANCES_PAGE_SIZE = 500
_VERBOSE_SAMPLE_KEYS = 5
_VERBOSE_SAMPLE_ITEMS = 3
_VERBOSE_VALUE_PREVIEW = 120
_RETRYABLE_METHODS = {"GET", "HEAD"}
_RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
# Retry only transient transport failures; local/config errors like bad URLs should fail fast.
_RETRYABLE_TRANSPORT_EXCEPTIONS = (
    requests.ConnectionError,
    requests.Timeout,
    requests.exceptions.ChunkedEncodingError,
)
_HTTP_RETRY_INITIAL_DELAY = 0.5
_HTTP_RETRY_MAX_DELAY = 2.0
_HTTP_RETRY_BACKOFF_FACTOR = 2.0

# Sentinel for distinguishing "not yet computed" from "computed and None"
# in cached lookups (e.g. self-user resolution).
_UNSET: Any = object()

# Operators supported by ``eval_config["extra_aggregations"]``. Mirrors the
# server's ``agent_platform.eval_aggregator.EXTRA_AGG_OPS``; kept client-side so
# a malformed/unsupported op surfaces at config time instead of failing silently
# when aggregation runs later.
EXTRA_AGG_OPS = ("avg", "sum")


def _merge_meta_tags(
    tags: Optional[list],
    *,
    meta_model: Optional[str] = None,
    meta_job_type: Optional[str] = None,
    meta_teacher_direction: Optional[str] = None,
    meta_train_stage: Optional[str] = None,
    upstream_platform: Optional[str] = None,
    upstream_job_id: Optional[str] = None,
) -> Optional[list]:
    """把 meta_* / upstream_* 参数转成 `key:value` tag 合并进 tags。

    meta 参数产出中划线 tag key（如 ``meta-model``，与 DLC 上游口径一致），
    upstream 维持下划线。与显式 tags 中的同 key 冲突时抛 ``ValueError``
    （服务端对同 key 多值是拒绝语义，提前在客户端报错）。
    任一参数为 None/空串即跳过。
    """

    provided = {
        "meta-model": meta_model,
        "meta-job-type": meta_job_type,
        "meta-teacher-direction": meta_teacher_direction,
        "meta-train-stage": meta_train_stage,
        "upstream_platform": upstream_platform,
        "upstream_job_id": upstream_job_id,
    }
    existing_keys = set()
    for t in tags or []:
        raw = str(t)
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        # 空值 tag（如 `meta-model:`）视为未声明，不参与冲突判定，
        # 与服务端 merge_meta_attrs_into_tags 的判定一致
        if value.strip():
            existing_keys.add(key.strip())
    conflicts = [k for k, v in provided.items() if v and str(v).strip() and k in existing_keys]
    if conflicts:
        raise ValueError(
            "tags already contains "
            + ", ".join(conflicts)
            + "; it conflicts with the meta parameter, keep only one"
        )
    extra = [
        f"{key}:{str(value).strip()}"
        for key, value in provided.items()
        if value and str(value).strip()
    ]
    merged = [*(tags or []), *extra]
    return merged or None


_META_TAG_TO_ATTR = {
    "meta-model": "meta_model",
    "meta-job-type": "meta_job_type",
    "meta-teacher-direction": "meta_teacher_direction",
    "meta-train-stage": "meta_train_stage",
}


def _lift_meta_tags_to_attrs(body: dict, tags) -> None:
    """把 tags 里的标准中划线 meta tag 同步为请求体独立属性（双写过渡期）。

    新服务端以独立属性为一等入口，tags 轨保留兼容老服务端；两者值一致，
    服务端幂等合并。支持 list[str]（key:value）与 dict 两种 tags 形态。
    """

    if not tags:
        return
    if isinstance(tags, dict):
        items = ((str(k).strip(), str(v).strip()) for k, v in tags.items())
    else:
        items = (
            (part[0].strip(), part[2].strip())
            for tag in tags
            for part in (str(tag).partition(":"),)
        )
    for key, value in items:
        attr = _META_TAG_TO_ATTR.get(key)
        if attr and value and attr not in body:
            body[attr] = value


def _validate_extra_aggregations(value: dict | None) -> None:
    """Structurally validate an ``eval_config["extra_aggregations"]`` mapping.

    Expected shape: ``{"<output_metric>": {"<op>": "<source_column>"}, ...}``.
    Mirrors the server's ``_parse_extra_aggregations`` checks so a bad spec is
    rejected here, before it is persisted. Raises ``ValueError`` on the first
    offending entry. ``None`` (and an empty mapping) is accepted and means
    "clear the key".
    """
    if not value:
        return
    if not isinstance(value, dict):
        raise ValueError(
            "extra_aggregations must be a mapping of {output_metric: {op: source_column}}"
        )
    for out_name, mapping in value.items():
        if not isinstance(mapping, dict) or len(mapping) != 1:
            raise ValueError(
                f"extra_aggregations['{out_name}'] must be a single-entry "
                f"{{op: source_column}} mapping, got {mapping!r}"
            )
        op, src = next(iter(mapping.items()))
        if op not in EXTRA_AGG_OPS:
            raise ValueError(
                f"extra_aggregations['{out_name}'] operator must be one of "
                f"{list(EXTRA_AGG_OPS)}, got {op!r}"
            )
        if not isinstance(src, str) or not src:
            raise ValueError(
                f"extra_aggregations['{out_name}']['{op}'] source column must "
                f"be a non-empty string, got {src!r}"
            )


class APIError(Exception):
    """Raised when an API request fails."""

    def __init__(
        self,
        status_code: Optional[int],
        detail: Any,
        request_id: str,
        response: Optional[requests.Response],
    ):
        self.status_code = status_code
        self.detail = detail
        self.request_id = request_id
        self.response = response
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        if self.status_code is None:
            return f"API Network Error: {self.detail} (request_id={self.request_id})"
        return f"API Error {self.status_code}: {self.detail} (request_id={self.request_id})"


class PaginationProtocolError(RuntimeError):
    """The server stopped honoring a pagination protocol already in use."""


def _ensure_next_token_honored(response: dict, *, next_token: Optional[str], endpoint: str) -> None:
    # An old server ignores the unknown next_token param and answers with its
    # default first page, so a `response.get("next_token")` loop would silently
    # repeat that page and drop the rest of the collection.
    if next_token and "next_token" not in response:
        raise PaginationProtocolError(
            f"server stopped returning next_token while paginating {endpoint}; upgrade the server"
        )


def _openapi_supports_instance_range(document: Any) -> bool:
    """Check the actual POST /jobs JSON request schema, failing closed on unknown shapes."""

    def resolve(node: Any) -> dict:
        seen = set()
        while isinstance(node, dict) and "$ref" in node:
            ref = node["$ref"]
            if not isinstance(ref, str) or not ref.startswith("#/") or ref in seen:
                return {}
            seen.add(ref)
            node = document
            for part in ref[2:].split("/"):
                if not isinstance(node, dict):
                    return {}
                node = node.get(part.replace("~1", "/").replace("~0", "~"))
        return node if isinstance(node, dict) else {}

    try:
        path = resolve(document["paths"]["/jobs"])
        body = resolve(path["post"]["requestBody"])
        schema = resolve(body["content"]["application/json"]["schema"])
        properties = schema["properties"]
    except (KeyError, TypeError):
        return False
    if not isinstance(properties, dict) or "instance_range" not in properties:
        return False
    field = resolve(properties["instance_range"])
    return bool(field) and field.get("readOnly") is not True


def _secret_ws_params(workspace_id: Optional[str]) -> Optional[dict]:
    """Build the ``?workspace_id=`` query for name-addressed secret endpoints.

    ``(name, workspace_id)`` is the secret's composite unique key, so every
    name-addressed call (get/update/delete/ACL) must carry the same WorkSpace the
    secret was created in. ``None`` sends no parameter and lets the apiserver fall
    back to the "default" WorkSpace, which keeps pre-WorkSpace callers working.
    """
    return {"workspace_id": workspace_id} if workspace_id else None


def _split_paged(payload: Any) -> tuple[list[dict], dict]:
    """Split a ``PagedSuccess`` envelope into ``(records, pagination)``.

    ``PagedSuccess`` is ``{code,message,data:[...],pagination:{total,page,page_size}}``.
    A bare list (or a null ``data``) yields an empty pagination dict so callers
    can render results without probing the response shape.
    """
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)], {}
    if not isinstance(payload, dict):
        return [], {}
    records = payload.get("data")
    pagination = payload.get("pagination")
    return (
        [item for item in (records or []) if isinstance(item, dict)],
        pagination if isinstance(pagination, dict) else {},
    )


# apiserver meta-tags 端点单页上限（handler.metaTagPaging 截断到 200；
# 缺省仅 20，目录查询必须显式带上并翻页）。
_META_TAG_PAGE_SIZE = 200


class APIClient:
    """Agent Platform API client."""

    def __init__(self, config: Config):
        self.config = config
        self.session = requests.Session()
        headers = dict(config.headers)
        user_agent = _build_user_agent(headers.get("User-Agent"))
        headers["User-Agent"] = user_agent

        # 认证 header: resolved CLI API key -> X-API-Key
        if config.token_key:
            headers["X-API-Key"] = config.token_key

        self.session.headers.update(
            {
                "Content-Type": "application/json",
                **headers,
            }
        )

    def _url(self, path: str) -> str:
        """Build the full URL.

        For paths starting with /apis/ (apiserver native routes), skip the /api prefix.
        """
        if path.startswith("/apis/"):
            return f"{self.config.base_url}{path}"
        if (
            path.startswith("/")
            and "/api" not in self.config.base_url
            and "nlb-" not in self.config.base_url
            and "localhost" not in self.config.base_url
        ):
            return f"{self.config.base_url}/api{path}"
        return f"{self.config.base_url}{path}"

    def _url_central(self, path: str) -> str:
        """Build the full URL for the central AP (agent-platform-apiserver).

        The central AP uses /apis/v1 prefix and does not require X-Cluster header.
        """
        return f"{self.config.base_url}/apis/v1{path}"

    def preview_request_headers(self) -> dict:
        """Return redacted headers that would be sent with a request."""
        headers = dict(self.session.headers)
        headers["X-Request-ID"] = "<generated per HTTP request>"
        return _redact_headers(headers, self.config.verbose_redaction)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict] = None,
        json_body: Any = None,
        timeout: TimeoutType = None,
        deadline: Optional[float] = None,
        _return_response: bool = False,
    ) -> Any:
        """Send an HTTP request with X-Request-ID and optional verbose logging."""
        self._require_cluster_config()
        if timeout is None:
            timeout = _default_timeout()
        else:
            timeout = _normalize_explicit_timeout(timeout)
        url = self._url(path)
        verbose = self.config.verbose
        max_attempts = self._max_attempts_for(method)
        for attempt in range(1, max_attempts + 1):
            attempt_timeout = _deadline_timeout(timeout, deadline)
            request_id = str(uuid.uuid4())
            headers = {"X-Request-ID": request_id}
            if verbose:
                request_headers = dict(self.session.headers)
                request_headers.update(headers)
                self._log_request(
                    method,
                    url,
                    request_id,
                    request_headers,
                    params,
                    json_body,
                    attempt=attempt,
                    max_attempts=max_attempts,
                )
            start = time.perf_counter()
            try:
                resp = self.session.request(
                    method,
                    url,
                    params=params,
                    json=json_body,
                    headers=headers,
                    timeout=attempt_timeout,
                )
            except requests.RequestException as exc:
                if deadline is not None:
                    _manifest_budget_remaining(deadline)
                duration_ms = (time.perf_counter() - start) * 1000
                if verbose:
                    self._log_exception(method, url, request_id, duration_ms, exc)
                if attempt < max_attempts and _is_retryable_exception(exc):
                    delay = _retry_delay(attempt)
                    if verbose:
                        self._log_retry(
                            method,
                            url,
                            request_id,
                            attempt,
                            max_attempts,
                            delay,
                            error=f"{type(exc).__name__}: {exc}",
                        )
                    _deadline_sleep(delay, deadline)
                    continue
                raise APIError(None, str(exc), request_id, None) from exc
            duration_ms = (time.perf_counter() - start) * 1000
            if deadline is not None:
                _manifest_budget_remaining(deadline)
            if verbose:
                self._log_response(method, url, request_id, resp, duration_ms)
            if not resp.ok:
                if attempt < max_attempts and _is_retryable_status(resp.status_code):
                    delay = _retry_delay(attempt, resp)
                    if verbose:
                        self._log_retry(
                            method,
                            url,
                            request_id,
                            attempt,
                            max_attempts,
                            delay,
                            status=resp.status_code,
                        )
                    _deadline_sleep(delay, deadline)
                    continue
                detail = _response_error_detail(resp)
                raise APIError(resp.status_code, detail, request_id, resp)
            if _return_response:
                return resp, request_id
            if not resp.content:
                return None
            try:
                return resp.json()
            except ValueError as exc:
                detail = _unexpected_non_json_response_detail(resp)
                raise APIError(resp.status_code, detail, request_id, resp) from exc
        raise RuntimeError("unreachable retry state")

    def _max_attempts_for(self, method: str) -> int:
        if method.upper() not in _RETRYABLE_METHODS:
            return 1
        return max(1, self.config.http_max_attempts)

    def _require_cluster_config(self) -> None:
        if has_cluster_header(self.config.headers):
            return
        raise ConfigurationError(
            "Missing cluster configuration. Set AP_CLUSTER (e.g. export AP_CLUSTER=test) "
            "or include a non-empty X-Cluster in AP_HEADERS (e.g. export AP_HEADERS='X-Cluster: test')."
        )

    def _get(
        self,
        path: str,
        params: Optional[dict] = None,
        timeout: TimeoutType = None,
    ) -> Any:
        """Send a GET request."""
        return self._request("GET", path, params=params, timeout=timeout)

    def ensure_profile_range_supported(self, timeout: TimeoutType = None) -> None:
        """Check the target cluster before sending a profile range request.

        Do not cache this across submissions: the server may have been rolled back.
        Use the normal authenticated, cluster-scoped request path.
        """
        try:
            document = self._get(
                "/openapi.json", timeout=timeout if timeout is not None else (10, 30)
            )
        except APIError as exc:
            raise ValueError(
                "Cannot verify server support for --profile --range via /openapi.json; "
                f"no jobs were submitted. Check AP_BASE_URL, AP_CLUSTER and server access. {exc}"
            ) from exc
        if not _openapi_supports_instance_range(document):
            raise ValueError(
                "Cannot confirm server support for --profile --range: /openapi.json must "
                "declare instance_range in the POST /jobs JSON request schema. "
                "No jobs were submitted. Upgrade the target server before using --range."
            )

    def _post(self, path: str, data: Any, timeout: TimeoutType = None) -> Any:
        """Send a POST request."""
        from .managed_ak import parameter_ak_usage, require_parameter_ak_ack

        references, selectors = parameter_ak_usage(data) if path == "/jobs" else (set(), set())
        result = self._request("POST", path, json_body=data, timeout=timeout)
        require_parameter_ak_ack(result, references, selectors)
        return result

    def _delete(self, path: str, *, params: Optional[dict] = None) -> Any:
        """Send a DELETE request."""
        return self._request("DELETE", path, params=params)

    def _put(self, path: str, data: Any, timeout: TimeoutType = None) -> Any:
        """Send a PUT request."""
        return self._request("PUT", path, json_body=data, timeout=timeout)

    # ==================== Central AP (apiserver) requests ====================

    def _request_central(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict] = None,
        json_body: Any = None,
        timeout: TimeoutType = None,
    ) -> Any:
        """Send an HTTP request to the central AP (agent-platform-apiserver).

        Unlike _request, this does NOT require X-Cluster config because
        the central AP is cluster-agnostic (data syncs to all clusters).
        Uses /apis/v1 prefix instead of /api.
        """
        if timeout is None:
            timeout = _default_timeout()
        else:
            timeout = _normalize_explicit_timeout(timeout)
        url = self._url_central(path)
        request_id = str(uuid.uuid4())
        headers = {"X-Request-ID": request_id}
        verbose = self.config.verbose
        if verbose:
            request_headers = dict(self.session.headers)
            request_headers.update(headers)
            self._log_request(method, url, request_id, request_headers, params, json_body)
        start = time.perf_counter()
        try:
            resp = self.session.request(
                method,
                url,
                params=params,
                json=json_body,
                headers=headers,
                timeout=timeout,
            )
        except requests.RequestException as exc:
            if verbose:
                duration_ms = (time.perf_counter() - start) * 1000
                self._log_exception(method, url, request_id, duration_ms, exc)
            raise APIError(None, str(exc), request_id, None) from exc
        duration_ms = (time.perf_counter() - start) * 1000
        if verbose:
            self._log_response(method, url, request_id, resp, duration_ms)
        if not resp.ok:
            detail = _response_error_detail(resp)
            raise APIError(resp.status_code, detail, request_id, resp)
        if not resp.content:
            return None
        try:
            return resp.json()
        except ValueError as exc:
            detail = _unexpected_non_json_response_detail(resp)
            raise APIError(resp.status_code, detail, request_id, resp) from exc

    def _get_central(
        self, path: str, params: Optional[dict] = None, timeout: TimeoutType = None
    ) -> Any:
        """Send a GET request to the central AP."""
        return self._request_central("GET", path, params=params, timeout=timeout)

    def _post_central(
        self,
        path: str,
        data: Any,
        params: Optional[dict] = None,
        timeout: TimeoutType = None,
    ) -> Any:
        """Send a POST request to the central AP."""
        return self._request_central("POST", path, params=params, json_body=data, timeout=timeout)

    def _put_central(
        self,
        path: str,
        data: Any,
        params: Optional[dict] = None,
        timeout: TimeoutType = None,
    ) -> Any:
        """Send a PUT request to the central AP."""
        return self._request_central("PUT", path, params=params, json_body=data, timeout=timeout)

    def _delete_central(
        self, path: str, params: Optional[dict] = None, timeout: TimeoutType = None
    ) -> Any:
        """Send a DELETE request to the central AP."""
        return self._request_central("DELETE", path, params=params, timeout=timeout)

    # ==================== Verbose logging ====================

    def _log_request(
        self,
        method: str,
        url: str,
        request_id: str,
        headers: dict,
        params: Optional[dict],
        body: Any,
        *,
        attempt: int = 1,
        max_attempts: int = 1,
    ) -> None:
        lines = [
            f">> Request {method} {url}",
            f"   request_id={request_id}",
        ]
        if max_attempts > 1:
            lines.append(f"   attempt={attempt}/{max_attempts}")
        lines.append(
            f"   headers={_safe_json(_redact_headers(headers, self.config.verbose_redaction))}"
        )
        if params:
            log_params = _redact_sensitive_data(params, self.config.verbose_redaction)
            lines.append(f"   params={_safe_json(log_params)}")
        if body is not None:
            encoded = _safe_json(body).encode("utf-8", errors="replace")
            log_body = _redact_sensitive_data(body, self.config.verbose_redaction)
            log_encoded = _safe_json(log_body).encode("utf-8", errors="replace")
            lines.append(f"   body_size={len(encoded)}")
            preview = self._summarize_body(log_body, encoded, log_encoded)
            if preview:
                lines.append(f"   body={preview}")
        _write_stderr(lines)

    def _log_response(
        self,
        method: str,
        url: str,
        request_id: str,
        resp: requests.Response,
        duration_ms: float,
    ) -> None:
        raw = resp.content or b""
        lines = [
            f"<< Response {method} {url}",
            f"   request_id={request_id}",
            f"   status={resp.status_code}",
            f"   duration_ms={duration_ms:.1f}",
            f"   headers={_safe_json(_redact_headers(dict(resp.headers), self.config.verbose_redaction))}",
            f"   body_size={len(raw)}",
        ]
        preview = self._summarize_response(resp, raw)
        if preview:
            lines.append(f"   body={preview}")
        _write_stderr(lines)

    def _log_exception(
        self,
        method: str,
        url: str,
        request_id: str,
        duration_ms: float,
        exc: Exception,
        *,
        error_detail: str | None = None,
    ) -> None:
        detail = str(exc) if error_detail is None else error_detail
        _write_stderr(
            [
                f"!! Error {method} {url}",
                f"   request_id={request_id}",
                f"   duration_ms={duration_ms:.1f}",
                f"   error={type(exc).__name__}: {detail}",
            ]
        )

    def _log_retry(
        self,
        method: str,
        url: str,
        request_id: str,
        attempt: int,
        max_attempts: int,
        delay: float,
        *,
        status: int | None = None,
        error: str | None = None,
    ) -> None:
        lines = [
            f"!! Retry {method} {url}",
            f"   request_id={request_id}",
            f"   attempt={attempt}/{max_attempts}",
            f"   retry_in={delay:.1f}s",
        ]
        if status is not None:
            lines.append(f"   status={status}")
        if error is not None:
            lines.append(f"   error={error}")
        _write_stderr(lines)

    def _summarize_body(self, body: Any, encoded: bytes, log_encoded: bytes | None = None) -> str:
        preview_encoded = log_encoded if log_encoded is not None else encoded
        if self.config.verbose_full_body:
            return preview_encoded.decode("utf-8", errors="replace")
        limit = self.config.verbose_body_limit
        if len(encoded) <= limit:
            return preview_encoded.decode("utf-8", errors="replace")
        return _summarize_json_value(body, limit)

    def _summarize_response(self, resp: requests.Response, raw: bytes) -> str:
        if not raw:
            return ""
        content_type = (resp.headers.get("Content-Type") or "").lower()
        if self.config.verbose_full_body:
            if self.config.verbose_redaction and "json" in content_type:
                try:
                    return _safe_json(_redact_sensitive_data(resp.json(), True))
                except Exception:
                    pass
            return _safe_decode(raw)
        limit = self.config.verbose_body_limit
        if "json" in content_type:
            try:
                data = resp.json()
            except Exception:
                return _truncate_text(_safe_decode(raw), limit)
            data = _redact_sensitive_data(data, self.config.verbose_redaction)
            encoded = _safe_json(data)
            if len(encoded.encode("utf-8", errors="replace")) <= limit:
                return encoded
            return _summarize_json_value(data, limit)
        return _truncate_text(_safe_decode(raw), limit)

    # ==================== Template operations ====================

    def list_templates(self) -> list:
        """List all templates."""
        params = {}
        if self.config.agenthub_ref:
            params["agenthub_revision"] = self.config.agenthub_ref
        return self._get("/templates", params=params)

    def get_template(self, name: str) -> dict:
        """Get template details."""
        params = {}
        if self.config.agenthub_ref:
            params["agenthub_revision"] = self.config.agenthub_ref
        return self._get(f"/templates/{quote(name)}", params=params)

    def list_benchmarks(self) -> list:
        """List all benchmarks from the central registry, preserving legacy IDs."""
        benchmarks = []
        page = 1
        page_size = 200
        # 与 CLI dataset list 的自动翻页同口径:100 页上限,防分页异常导致死循环。
        max_pages = 100
        while page <= max_pages:
            payload = self._get(
                "/apis/v1/benchmarks", params={"page": page, "page_size": page_size}
            )
            records, pagination = _split_paged(payload)
            for record in records:
                item = dict(record)
                if "source_id" in item:
                    item.setdefault("id", item["source_id"])
                benchmarks.append(item)
            if not records or not pagination:
                break
            try:
                total = int(pagination.get("total"))
            except (TypeError, ValueError):
                total = None
            if total is not None:
                if len(benchmarks) >= total:
                    break
            elif len(records) < page_size:
                break
            page += 1
        return benchmarks

    def get_benchmark(self, name: str) -> dict:
        """Get a single benchmark by exact name."""
        return self._get(f"/benchmarks/{quote(name, safe='')}")

    # ==================== Checkpoint operations ====================

    def list_checkpoints(
        self,
        *,
        name: Optional[str] = None,
        model_id: Optional[str] = None,
        status: Optional[str] = None,
        uuid: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> dict:
        """List active checkpoints from the local checkpoint registry."""
        params = {"skip": skip, "limit": limit}
        if name:
            params["name"] = name
        if model_id:
            params["model_id"] = model_id
        if status:
            params["status"] = status
        if uuid:
            params["uuid"] = uuid
        return self._get("/checkpoints", params=params)

    def get_checkpoint(self, name: str) -> dict:
        """Get a single checkpoint by exact name."""
        return self._get(f"/checkpoints/{quote(name, safe='')}")

    # ==================== Dataset operations ====================

    def list_datasets_page(
        self,
        *,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = _DATASET_PAGE_SIZE,
    ) -> dict:
        """Get one page of datasets."""
        params: dict = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        return self._get("/datasets", params=params)

    def list_datasets(self, search: Optional[str] = None) -> dict:
        """List datasets."""
        params: dict = {"limit": _DATASET_PAGE_SIZE}
        if search:
            params["search"] = search
        return self._get("/datasets", params=params)

    def list_all_datasets(self, search: Optional[str] = None) -> dict:
        """List all datasets (auto-paginated)."""
        skip = 0
        all_datasets: list[dict] = []
        last_page: dict | None = None

        while True:
            page = self.list_datasets_page(
                search=search,
                skip=skip,
                limit=_DATASET_PAGE_SIZE,
            )
            last_page = page
            page_datasets = page.get("datasets") or []
            all_datasets.extend(page_datasets)

            total = page.get("total")
            if total is not None and len(all_datasets) >= total:
                break
            if len(page_datasets) < _DATASET_PAGE_SIZE:
                break

            skip += len(page_datasets)

        return {
            **last_page,
            "datasets": all_datasets,
        }

    def list_dataset_versions(self, dataset: str) -> list:
        """List dataset versions."""
        return self._get(f"/datasets/{quote(dataset)}/versions")

    def list_dataset_instances_page(
        self,
        dataset_version: str,
        *,
        skip: int = 0,
        limit: int = _DATASET_INSTANCES_PAGE_SIZE,
    ) -> dict:
        """Get one page of dataset instances."""
        return self._get(
            f"/datasets/{quote(dataset_version)}/instances",
            params={"skip": skip, "limit": limit},
        )

    def list_dataset_instances(self, dataset_version: str, limit: int = 500) -> dict:
        """List dataset instances."""
        return self._get(f"/datasets/{quote(dataset_version)}/instances", params={"limit": limit})

    def list_all_dataset_instances(self, dataset_version: str) -> dict:
        """List all dataset instances (auto-paginated)."""
        skip = 0
        all_instance_ids: list[str] = []
        last_page: dict | None = None

        while True:
            page = self.list_dataset_instances_page(
                dataset_version,
                skip=skip,
                limit=_DATASET_INSTANCES_PAGE_SIZE,
            )
            last_page = page
            page_ids = page.get("instance_ids") or []
            all_instance_ids.extend(page_ids)

            total = page.get("total")
            if total is not None and len(all_instance_ids) >= total:
                break
            if len(page_ids) < _DATASET_INSTANCES_PAGE_SIZE:
                break

            skip += len(page_ids)

        return {
            **last_page,
            "instance_ids": all_instance_ids,
        }

    # ==================== Dataset series (apiserver dataset domain) ====================
    #
    # 这一节对接 Go apiserver 的 dataset 领域(/apis/v1/datasets/...),与上面
    # ossdata 目录的 /api/datasets 路由完全无关。
    #
    # **dataset 领域的控制面读写全部在 InstanceRepo SDK 上**(见
    # docs/ap-cli-dataset-refactor-design.md §9.5):迁移期加进这里的 registry 方法、
    # 以及最后三条"push 前检查 + publish-status"的旧读,都已随迁移删除。
    # 本文件现在只服务旧 ossdata 路径(`dataset list --legacy`、弃用的
    # `dataset versions/instances`、`job create --dataset`)。

    def list_meta_models(self) -> dict:
        """从 meta-model 标签目录获取可用模型，保留 list 的 items 响应形状。"""
        items = self.get_meta_tags("meta-model").get("items") or []
        return {
            "items": [
                {**item, "name": item["value"]}
                for item in items
                if item.get("value") and item.get("is_enabled", True)
            ]
        }

    def get_meta_model(self, name: str) -> dict:
        """从启用的 meta-model 标签值中按 value 或 source_id 查找。"""
        result = self.list_meta_models()
        for item in result.get("items") or []:
            if item.get("name") == name or item.get("source_id") == name:
                return item
        raise APIError(404, f"meta model {name!r} not found", "client-filter", None)

    def _get_meta_tag_catalog(
        self, path: str, params: Optional[dict] = None
    ) -> tuple[list[dict], dict]:
        """按 benchmarks 同口径自动翻页取全量目录记录，返回 ``(records, pagination)``。

        apiserver ``meta-tags`` 端点分页参数为 ``page`` / ``page_size``（缺省
        20、上限 200，见 handler.metaTagPaging）；单页取用会把值目录静默截断
        （``meta-job-type`` 漏掉 ``Eval-Eval`` 时 ``default`` 会被算成空串），
        故显式传上限并翻页。
        """
        records: list[dict] = []
        pagination: dict = {}
        page = 1
        # 与 list_benchmarks 同口径的 100 页上限，防分页异常导致死循环
        max_pages = 100
        while page <= max_pages:
            query = dict(params or {})
            query["page"] = page
            query["page_size"] = _META_TAG_PAGE_SIZE
            page_records, pagination = _split_paged(self._get_central(path, params=query))
            records.extend(page_records)
            if not page_records or not pagination:
                break
            try:
                total = int(pagination.get("total"))
            except (TypeError, ValueError):
                total = None
            if total is not None:
                if len(records) >= total:
                    break
            elif len(page_records) < _META_TAG_PAGE_SIZE:
                break
            page += 1
        return records, pagination

    def list_meta_tags(self) -> dict:
        """meta 标签键目录（apiserver GET /apis/v1/meta-tags/keys，返回 {items:[...]}）。

        apiserver 用 PagedSuccess envelope（{code,data,pagination}）返回，
        按基准 benchmarks 客户端同口径经 _split_paged 拆包并自动翻页；
        裸列表等旧形态兜底为空分页。
        """
        records, pagination = self._get_meta_tag_catalog("/meta-tags/keys")
        result = {"items": records}
        if pagination:
            result["pagination"] = pagination
        return result

    def get_meta_tags(self, key: str) -> dict:
        """单个 meta 键的值目录（GET /apis/v1/meta-tags?key=，返回 {items:[...]}）。

        与 ``list_meta_tags`` 同样自动翻页，避免值目录被单页默认大小截断。
        """
        records, pagination = self._get_meta_tag_catalog("/meta-tags", {"key": key})
        result = {"items": records}
        if pagination:
            result["pagination"] = pagination
        return result

    def list_meta_job_types(self) -> dict:
        """从 meta-job-type 标签目录获取启用的任务类型，不补本地展示值。"""
        items = self.get_meta_tags("meta-job-type").get("items") or []
        return {
            "meta_job_type": {
                "options": [
                    item for item in items if item.get("value") and item.get("is_enabled", True)
                ],
            }
        }

    # ==================== Account Pool operations ====================

    def get_akpool_rpm(
        self,
        *,
        model: str,
        ak_id: Optional[str] = None,
        masked_ak: Optional[str] = None,
        time_range: Optional[str] = None,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        timeout: TimeoutType = None,
    ) -> dict:
        """查询托管 AK 在指定模型上的当前 RPM 用量与上限（GET /apis/v1/model-api-keys/rpm-usage）。

        ``ak_id``(uak-xxx) 与 ``masked_ak``(掩码后 6 位) 二选一，都缺或都给
        服务端返回 400；``from_time``/``to_time``(RFC3339) 显式指定时覆盖
        ``time_range``(Go duration，如 5m/1h，服务端默认 5m)。
        响应为嵌套结构：``usage.current_rpm``/``usage.sampled_at``、
        ``rpm.limit``/``rpm.limit_state``/``rpm.synced_at``、``usage_status``；
        查未托管 AK 时 ``ak_id`` 为 null。
        """
        validate_ak_id(ak_id)
        params: dict = {"model": model}
        if ak_id is not None:
            params["ak_id"] = ak_id
        if masked_ak is not None:
            params["masked_ak"] = masked_ak
        if time_range is not None:
            params["time_range"] = time_range
        if from_time is not None:
            params["from"] = from_time
        if to_time is not None:
            params["to"] = to_time
        return self._get_central("/model-api-keys/rpm-usage", params=params, timeout=timeout)

    # ==================== Job operations ====================

    def create_group(
        self,
        name: Optional[str] = None,
        template: Optional[str] = None,
        agenthub_revision: Optional[str] = None,
        queue_id: Optional[str] = None,
        # ``queue`` 是老参数名 (向后兼容),两者都传时 queue_id 优先。
        queue: Optional[str] = None,
        max_concurrency: Optional[int] = None,
        eval_config: Optional[dict] = None,
        model_base_url_collection: Optional[list] = None,
        group_post_process: Optional[dict] = None,
        dataset: Optional[str] = None,
        model: Optional[str] = None,
        scaffold: Optional[str] = None,
        agent: Optional[dict] = None,
        tags: Optional[list[str]] = None,
        meta_model: Optional[str] = None,
        meta_job_type: Optional[str] = None,
        upstream_platform: Optional[str] = None,
        upstream_job_id: Optional[str] = None,
        # ─── Benchmark+ckpt reporting metadata (Group-level) ──────────
        checkpoint_id: Optional[str] = None,
        checkpoint_path: Optional[str] = None,
        checkpoint: Optional[dict] = None,
        benchmark: Optional[str] = None,
        experiment: Optional[str] = None,
        ak_ids: Optional[list[str]] = None,
        priority: Optional[str] = None,
        priority_weight: Optional[int] = None,
        transparency: Optional[Literal["whitebox", "blackbox"]] = None,
        idempotency_key: Optional[str] = None,
    ) -> dict:
        """Create a group with optional scheduling defaults for its Jobs.

        Omitted priority fields use the server defaults: medium and weight 0.
        """
        if priority is not None and priority not in {"high", "medium"}:
            raise ValueError("priority must be one of high/medium")
        if transparency is not None and transparency not in {"whitebox", "blackbox"}:
            raise ValueError("transparency must be whitebox or blackbox")
        if transparency == "blackbox" and not idempotency_key:
            raise ValueError("blackbox Group creation requires a reusable idempotency_key (UUID4)")
        if ak_ids is not None and not isinstance(ak_ids, list):
            raise ValueError("ak_ids must be a list")
        references = list(ak_ids or [])
        for reference in references:
            if validate_ak_id(reference) is None:
                raise ValueError("ak_ids entries must be nonempty strings")
        references = list(dict.fromkeys(references))
        body: dict = {}
        if transparency is not None:
            body["transparency"] = transparency
        if idempotency_key is not None:
            body["idempotency_key"] = idempotency_key
        if references:
            body["ak_ids"] = references
        if name:
            body["name"] = name
        effective_tags = _merge_meta_tags(
            tags,
            meta_model=meta_model,
            meta_job_type=meta_job_type,
            upstream_platform=upstream_platform,
            upstream_job_id=upstream_job_id,
        )
        if effective_tags:
            body["tags"] = effective_tags
            _lift_meta_tags_to_attrs(body, effective_tags)
        if template is not None:
            body["template"] = template
        effective_agenthub_revision = (
            agenthub_revision if agenthub_revision is not None else self.config.agenthub_ref
        )
        if effective_agenthub_revision is not None and (
            template is not None or group_post_process is not None
        ):
            body["agenthub_revision"] = effective_agenthub_revision
        # body 标准字段是 queue_id;queue 是向后兼容入参,仅在 queue_id 缺失时 fallback。
        effective_queue_id = queue_id if queue_id is not None else queue
        if effective_queue_id is not None:
            body["queue_id"] = effective_queue_id
        if max_concurrency is not None:
            body["max_concurrency"] = max_concurrency
        if priority is not None:
            body["priority"] = priority
        if priority_weight is not None:
            body["priority_weight"] = priority_weight
        if eval_config is not None:
            body["eval_config"] = eval_config
        if model_base_url_collection is not None:
            body["model_base_url_collection"] = model_base_url_collection
        if group_post_process is not None:
            body["group_post_process"] = group_post_process
        if dataset is not None:
            body["dataset"] = dataset
        if model is not None:
            body["model"] = model
        if scaffold is not None:
            body["scaffold"] = scaffold
        if agent is not None:
            body["agent"] = agent
        # Benchmark+ckpt reporting metadata — same wire shape as create_job:
        # checkpoint travels as a single JSON object with optional id/path
        # plus any additional attributes from the raw ``checkpoint`` object.
        checkpoint_payload = _merge_checkpoint_payload(checkpoint, checkpoint_id, checkpoint_path)
        if checkpoint_payload:
            body["checkpoint"] = checkpoint_payload
        if benchmark is not None:
            body["benchmark"] = benchmark
        if experiment is not None:
            body["experiment"] = experiment
        result = self._post("/groups", body)
        for reference in references:
            require_managed_ak_ack(result, reference)
        return result

    def create_job(
        self,
        template: Optional[str] = None,
        params: Optional[dict] = None,
        params_list: Optional[list] = None,
        suite_name: Optional[str] = None,
        tags: Optional[list] = None,
        overrides: Optional[dict] = None,
        max_concurrency: Optional[int] = None,
        group_id: Optional[str] = None,
        queue_id: Optional[str] = None,
        quota_id: Optional[str] = None,
        # Concurrency-policy admission key (request-level, shared across batch).
        policy_id: Optional[str] = None,
        # ``queue`` 是老参数名 (向后兼容),功能等同 queue_id。两者都传时 queue_id 优先。
        # 新调用方一律传 queue_id;后续 deprecation cycle 走完后移除 queue。
        queue: Optional[str] = None,
        model_base_url_collection: Optional[list] = None,
        group_post_process: Optional[dict] = None,
        datasources: Optional[list] = None,
        enable_otel_tracing: Optional[bool] = None,
        runner: Optional[str] = None,
        runner_options: Optional[dict] = None,
        idempotency_key: Optional[str] = None,
        max_failure_retries: int = 0,
        # ─── Scheduling hints ─────────────────────────────────────────
        priority: Optional[str] = None,
        priority_weight: Optional[int] = None,
        resource_mode: Optional[str] = None,
        disable_loongcollector: bool = False,
        timeout: TimeoutType = None,
        # ─── Credential assignment ────────────────────────────────────
        credential_type: Optional[str] = None,
        account_pool: Optional[str] = None,
        # ─── Eval config ──────────────────────────────────────────────
        eval_config: Optional[dict] = None,
        # ─── Profile mode fields ───────────────────────────────────────
        profile_id: Optional[str] = None,
        profile_version: Optional[int] = None,
        instances: Optional[list] = None,
        dataset: Optional[str] = None,
        batch_size: Optional[int] = None,
        trials: Optional[int] = None,
        resource_profile_id: Optional[str] = None,
        # ─── Meta tags（任务看清）──────────────────────────────────────
        meta_model: Optional[str] = None,
        meta_job_type: Optional[str] = None,
        upstream_platform: Optional[str] = None,
        upstream_job_id: Optional[str] = None,
        # ─── Benchmark+ckpt reporting metadata (Group-level) ──────────
        checkpoint_id: Optional[str] = None,
        checkpoint_path: Optional[str] = None,
        checkpoint: Optional[dict] = None,
        benchmark: Optional[str] = None,
        experiment: Optional[str] = None,
        ak_id: Optional[str] = None,
        ak_mode: str = "auto",
        instance_range: Optional[str] = None,
        profile: Optional[str] = None,
        transparency: Optional[Literal["whitebox", "blackbox"]] = None,
    ) -> dict:
        """Create a job."""
        body = self.build_create_job_body(
            transparency=transparency,
            template=template,
            params=params,
            params_list=params_list,
            suite_name=suite_name,
            tags=tags,
            overrides=overrides,
            max_concurrency=max_concurrency,
            group_id=group_id,
            queue_id=queue_id,
            quota_id=quota_id,
            policy_id=policy_id,
            queue=queue,
            model_base_url_collection=model_base_url_collection,
            group_post_process=group_post_process,
            datasources=datasources,
            enable_otel_tracing=enable_otel_tracing,
            runner=runner,
            runner_options=runner_options,
            idempotency_key=idempotency_key,
            max_failure_retries=max_failure_retries,
            priority=priority,
            priority_weight=priority_weight,
            resource_mode=resource_mode,
            disable_loongcollector=disable_loongcollector,
            credential_type=credential_type,
            account_pool=account_pool,
            eval_config=eval_config,
            profile=profile,
            profile_id=profile_id,
            profile_version=profile_version,
            instances=instances,
            dataset=dataset,
            batch_size=batch_size,
            trials=trials,
            resource_profile_id=resource_profile_id,
            instance_range=instance_range,
            meta_model=meta_model,
            meta_job_type=meta_job_type,
            upstream_platform=upstream_platform,
            upstream_job_id=upstream_job_id,
            checkpoint_id=checkpoint_id,
            checkpoint_path=checkpoint_path,
            checkpoint=checkpoint,
            benchmark=benchmark,
            experiment=experiment,
            ak_id=ak_id,
            ak_mode=ak_mode,
        )

        result = self._post("/jobs", body, timeout=timeout)
        require_managed_ak_ack(result, ak_id)
        return result

    def build_create_job_body(
        self,
        template: Optional[str] = None,
        params: Optional[dict] = None,
        params_list: Optional[list] = None,
        suite_name: Optional[str] = None,
        tags: Optional[list] = None,
        overrides: Optional[dict] = None,
        max_concurrency: Optional[int] = None,
        group_id: Optional[str] = None,
        queue_id: Optional[str] = None,
        quota_id: Optional[str] = None,
        # Concurrency-policy admission key (request-level, shared across batch).
        policy_id: Optional[str] = None,
        # ``queue`` 是老参数名 (向后兼容),两者都传时 queue_id 优先。
        queue: Optional[str] = None,
        model_base_url_collection: Optional[list] = None,
        group_post_process: Optional[dict] = None,
        datasources: Optional[list] = None,
        enable_otel_tracing: Optional[bool] = None,
        runner: Optional[str] = None,
        runner_options: Optional[dict] = None,
        idempotency_key: Optional[str] = None,
        max_failure_retries: int = 0,
        # ─── Scheduling hints ─────────────────────────────────────────
        priority: Optional[str] = None,
        priority_weight: Optional[int] = None,
        resource_mode: Optional[str] = None,
        disable_loongcollector: bool = False,
        # ─── Credential assignment ────────────────────────────────────
        credential_type: Optional[str] = None,
        account_pool: Optional[str] = None,
        # ─── Eval config ──────────────────────────────────────────────
        eval_config: Optional[dict] = None,
        # ─── Profile mode fields ───────────────────────────────────────
        profile_id: Optional[str] = None,
        profile_version: Optional[int] = None,
        instances: Optional[list] = None,
        dataset: Optional[str] = None,
        batch_size: Optional[int] = None,
        trials: Optional[int] = None,
        dry_run: bool = False,
        resource_profile_id: Optional[str] = None,
        # ─── Meta tags（任务看清）──────────────────────────────────────
        meta_model: Optional[str] = None,
        meta_job_type: Optional[str] = None,
        upstream_platform: Optional[str] = None,
        upstream_job_id: Optional[str] = None,
        # ─── Benchmark+ckpt reporting metadata (Group-level) ──────────
        checkpoint_id: Optional[str] = None,
        checkpoint_path: Optional[str] = None,
        checkpoint: Optional[dict] = None,
        benchmark: Optional[str] = None,
        experiment: Optional[str] = None,
        ak_id: Optional[str] = None,
        ak_mode: str = "auto",
        instance_range: Optional[str] = None,
        profile: Optional[str] = None,
        transparency: Optional[Literal["whitebox", "blackbox"]] = None,
    ) -> dict:
        """Build the /jobs request body for job creation."""
        if transparency is not None and transparency not in {"whitebox", "blackbox"}:
            raise ValueError("transparency must be whitebox or blackbox")
        if profile is not None and (profile_id is not None or profile_version is not None):
            raise ValueError("profile cannot be combined with profile_id or profile_version")
        _validate_credential_source_selection(
            account_pool=account_pool,
            credential_type=credential_type,
            params=params,
            params_list=params_list,
        )
        if not template and not profile_id and profile is None:
            raise ValueError("Either template, profile or profile_id is required")
        validate_ak_selection(ak_id, params, params_list, overrides)
        if ak_mode not in {"auto", "manual", "synced"}:
            raise ValueError("ak_mode must be auto, manual or synced")
        body: dict = {}
        if template is not None:
            body["template"] = template
        if ak_id is not None:
            body["ak_id"] = ak_id
        if ak_mode != "auto":
            body["ak_mode"] = ak_mode

        if params is not None:
            body["params"] = params
        if params_list is not None:
            body["params_list"] = params_list
        if suite_name:
            body["suite_name"] = suite_name
        if self.config.agenthub_ref:
            body["agenthub_revision"] = self.config.agenthub_ref
        effective_tags = _merge_meta_tags(
            tags,
            meta_model=meta_model,
            meta_job_type=meta_job_type,
            upstream_platform=upstream_platform,
            upstream_job_id=upstream_job_id,
        )
        if effective_tags:
            body["tags"] = effective_tags
            _lift_meta_tags_to_attrs(body, effective_tags)
        if overrides:
            body["overrides"] = overrides
        if max_concurrency is not None:
            body["max_concurrency"] = max_concurrency
        if group_id is not None:
            body["group_id"] = group_id
        # body 标准字段是 queue_id;queue 是向后兼容入参,仅在 queue_id 缺失时 fallback。
        effective_queue_id = queue_id if queue_id is not None else queue
        if effective_queue_id is not None:
            body["queue_id"] = effective_queue_id
        if quota_id is not None:
            body["quota_id"] = quota_id
        if policy_id is not None:
            body["policy_id"] = policy_id
        if model_base_url_collection is not None:
            body["model_base_url_collection"] = model_base_url_collection
        if group_post_process is not None:
            body["group_post_process"] = group_post_process
        if datasources is not None:
            body["datasources"] = datasources
        if enable_otel_tracing is not None:
            body["enable_otel_tracing"] = enable_otel_tracing
        if runner is not None:
            body["runner"] = runner
        if runner_options is not None:
            body["runner_options"] = runner_options
        if idempotency_key is not None:
            body["idempotency_key"] = idempotency_key
        if max_failure_retries:
            body["max_failure_retries"] = max_failure_retries

        # Scheduling hints
        if priority is not None:
            body["priority"] = priority
        if priority_weight is not None:
            body["priority_weight"] = priority_weight
        if resource_mode is not None:
            body["resource_mode"] = resource_mode
        if disable_loongcollector:
            body["disable_loongcollector"] = True

        # Credential assignment
        if credential_type is not None:
            body["credential_type"] = credential_type
        if account_pool is not None:
            body["account_pool"] = account_pool

        # Eval config
        if eval_config is not None:
            body["eval_config"] = eval_config

        # Profile mode fields
        if profile is not None:
            body["profile"] = profile
        if profile_id is not None:
            body["profile_id"] = profile_id
        if profile_version is not None:
            body["profile_version"] = profile_version
        if instances is not None:
            body["instances"] = instances
        if instance_range is not None:
            body["instance_range"] = instance_range
        if dataset is not None:
            body["dataset"] = dataset
        if batch_size is not None:
            body["batch_size"] = batch_size
        if trials is not None:
            body["trials"] = trials
        if resource_profile_id is not None:
            body["resource_profile_id"] = resource_profile_id
        if dry_run:
            body["dry_run"] = True

        # Benchmark+ckpt reporting metadata (Group-level; the server persists
        # them on the Group at creation time). The checkpoint travels as a
        # single JSON object with optional id/path plus any additional
        # attributes from the raw ``checkpoint`` object.
        checkpoint_payload = _merge_checkpoint_payload(checkpoint, checkpoint_id, checkpoint_path)
        if checkpoint_payload:
            body["checkpoint"] = checkpoint_payload
        if benchmark is not None:
            body["benchmark"] = benchmark
        if experiment is not None:
            body["experiment"] = experiment

        if transparency is not None:
            body["transparency"] = transparency
        return body

    def get_job_access_contact(self, job_id: str) -> dict:
        """Discover the owner and grant contact without reading protected details."""
        result = self._get(f"/jobs/{quote(job_id, safe='')}", params={"access_contact": True})
        if (
            not isinstance(result, dict)
            or result.get("resource_type") != "job"
            or "authorization_contact" not in result
        ):
            raise ConfigurationError(
                "Server does not support access contact queries; upgrade Agent-Platform first"
            )
        return result

    def get_job(
        self,
        job_id: str,
        *,
        include_params: bool = False,
        include_spec: bool = False,
        spec_format: str = "json",
        timeout: TimeoutType = None,
    ) -> dict:
        """Get job details."""
        params: dict[str, Any] = {}
        if include_params:
            params["include_params"] = True
        if include_spec:
            params["include_spec"] = True
            params["spec_format"] = spec_format
        return self._get(f"/jobs/{quote(job_id)}", params=params or None, timeout=timeout)

    def list_jobs(
        self,
        template: Optional[str] = None,
        group_id: Optional[str] = None,
        status: Optional[str] = None,
        job_id: Optional[str] = None,
        instance_id: Optional[str] = None,
        user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        queue_id: Optional[str] = None,
        concurrency_policy_id: Optional[str] = None,
        active_only: bool = False,
        finished_after: Optional[str] = None,
        finished_before: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        prefix_match: bool = False,
        tag: Optional[list[str]] = None,
        tag_pattern: Optional[str] = None,
        tag_logic: Optional[str] = None,
        duration_sort: Optional[bool] = None,
        created_at_sort: Optional[bool] = None,
        finished_at_sort: Optional[bool] = None,
        skip: int = 0,
        limit: int = 100,
        meta_teacher_direction: Optional[str] = None,
        meta_train_stage: Optional[str] = None,
        meta_model: Optional[str] = None,
        meta_job_type: Optional[str] = None,
        upstream_platform: Optional[str] = None,
        upstream_job_id: Optional[str] = None,
        next_token: Optional[str] = None,
        pagination: Optional[str] = None,
        include_total: bool = True,
        ak_id: Optional[str] = None,
    ) -> dict:
        """List jobs."""
        validate_ak_id(ak_id)
        params = {"skip": skip, "limit": limit}
        if ak_id is not None:
            params["ak_id"] = ak_id
        if template:
            params["template"] = template
        if group_id:
            params["group_id"] = group_id
        if status:
            params["status"] = status
        if job_id:
            params["job_id"] = job_id
        if instance_id:
            params["instance_id"] = instance_id
        if user_id:
            params["user_id"] = user_id
        if user_name:
            params["user_name"] = user_name
        if queue_id:
            params["queue_id"] = queue_id
        if concurrency_policy_id:
            params["concurrency_policy_id"] = concurrency_policy_id
        if active_only:
            params["active_only"] = True
        if finished_after:
            params["finished_after"] = finished_after
        if finished_before:
            params["finished_before"] = finished_before
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        if prefix_match:
            params["prefix_match"] = True
        if tag:
            params["tag"] = tag
        if tag_pattern:
            params["tag_pattern"] = tag_pattern
        if tag_logic:
            params["tag_logic"] = tag_logic
        if meta_teacher_direction is not None:
            params["meta_teacher_direction"] = meta_teacher_direction
        if meta_train_stage is not None:
            params["meta_train_stage"] = meta_train_stage
        if meta_model is not None:
            params["meta_model"] = meta_model
        if meta_job_type is not None:
            params["meta_job_type"] = meta_job_type
        if upstream_platform is not None:
            params["upstream_platform"] = upstream_platform
        if upstream_job_id is not None:
            params["upstream_job_id"] = upstream_job_id
        if duration_sort is not None:
            params["duration_sort"] = duration_sort
        if created_at_sort is not None:
            params["created_at_sort"] = created_at_sort
        if finished_at_sort is not None:
            params["finished_at_sort"] = finished_at_sort
        if next_token:
            params["next_token"] = next_token
        if pagination:
            params["pagination"] = pagination
        if not include_total:
            params["include_total"] = False
        response = self._get("/jobs", params=params)
        _ensure_next_token_honored(response, next_token=next_token, endpoint="/jobs")
        return response

    # ==================== Group operations ====================

    def get_group_access_contact(self, group_id: str) -> dict:
        """Discover the owner and grant contact without reading protected details."""
        result = self._get(f"/groups/{quote(group_id, safe='')}", params={"access_contact": True})
        if (
            not isinstance(result, dict)
            or result.get("resource_type") != "group"
            or "authorization_contact" not in result
        ):
            raise ConfigurationError(
                "Server does not support access contact queries; upgrade Agent-Platform first"
            )
        return result

    def get_group(self, group_id: str, timeout: TimeoutType = None) -> dict:
        """Get group details."""
        return self._get(f"/groups/{quote(group_id)}", timeout=timeout)

    @staticmethod
    def _unified_group_clone_body(
        *,
        source_cluster: Optional[str] = None,
        source_mode: str = "terminal_only",
        start_paused: Optional[bool] = None,
        trials: Optional[int] = None,
        target_group: Optional[dict] = None,
        job_patch: Optional[dict] = None,
        resource_mappings: Optional[dict] = None,
        idempotency_key: Optional[str] = None,
    ) -> dict:
        body: dict[str, Any] = {
            "source_mode": source_mode,
            "target_group": target_group or {},
            "job_patch": job_patch or {},
        }
        if source_cluster is not None:
            body["source_cluster"] = source_cluster
        if start_paused is not None:
            body["start_paused"] = start_paused
        if trials is not None:
            body["trials"] = trials
        if resource_mappings is not None:
            body["resource_mappings"] = resource_mappings
        if idempotency_key is not None:
            body["idempotency_key"] = idempotency_key
        return body

    def preview_group_clone(
        self,
        source_group_id: str,
        **kwargs: Any,
    ) -> dict:
        """Preview a local clone, or a cross-cluster clone with source_cluster."""

        body = self._unified_group_clone_body(**kwargs)
        return self._post(f"/groups/{quote(source_group_id)}/clone/preview", body)

    def clone_group(
        self,
        source_group_id: str,
        **kwargs: Any,
    ) -> dict:
        """Clone locally, or cross-cluster when source_cluster is supplied."""

        body = self._unified_group_clone_body(**kwargs)
        return self._post(f"/groups/{quote(source_group_id)}/clone", body)

    @staticmethod
    def _cross_cluster_clone_body(
        source_cluster: str,
        source_group_id: str,
        *,
        source_mode: str = "terminal_only",
        start_paused: bool = True,
        trials: Optional[int] = None,
        target_group: Optional[dict] = None,
        job_patch: Optional[dict] = None,
        resource_mappings: Optional[dict] = None,
        idempotency_key: Optional[str] = None,
    ) -> dict:
        body = {
            "source_cluster": source_cluster,
            "source_group_id": source_group_id,
            "source_mode": source_mode,
            "start_paused": start_paused,
            "target_group": target_group or {},
            "job_patch": job_patch or {},
            "resource_mappings": resource_mappings or {},
        }
        if trials is not None:
            body["trials"] = trials
        if idempotency_key is not None:
            body["idempotency_key"] = idempotency_key
        return body

    def preview_cross_cluster_group_clone(
        self,
        source_cluster: str,
        source_group_id: str,
        **kwargs: Any,
    ) -> dict:
        """Preview a cross-cluster Group Clone on this client's target cluster."""

        body = self._cross_cluster_clone_body(source_cluster, source_group_id, **kwargs)
        return self._post("/group-clones/cross-cluster/preview", body)

    def clone_group_cross_cluster(
        self,
        source_cluster: str,
        source_group_id: str,
        **kwargs: Any,
    ) -> dict:
        """Execute a cross-cluster Group Clone on this client's target cluster."""

        body = self._cross_cluster_clone_body(source_cluster, source_group_id, **kwargs)
        return self._post("/group-clones/cross-cluster", body)

    def list_groups(
        self,
        skip: int = 0,
        limit: int = 100,
        profile: Optional[str] = None,
        name: Optional[str] = None,
        group_id: Optional[str] = None,
        user_id: Optional[str] = None,
        user_name: Optional[str] = None,
        dataset: Optional[str] = None,
        model: Optional[str] = None,
        scaffold: Optional[str] = None,
        queue_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        prefix_match: bool = False,
        tag: Optional[list[str]] = None,
        tag_logic: Optional[str] = None,
        meta_teacher_direction: Optional[str] = None,
        meta_train_stage: Optional[str] = None,
        meta_model: Optional[str] = None,
        meta_job_type: Optional[str] = None,
        upstream_platform: Optional[str] = None,
        upstream_job_id: Optional[str] = None,
        ak_id: Optional[str] = None,
    ) -> dict:
        """List groups."""
        validate_ak_id(ak_id)
        params: dict = {"skip": skip, "limit": limit}
        if ak_id is not None:
            params["ak_id"] = ak_id
        if name is not None:
            params["name"] = name
        if group_id is not None:
            params["group_id"] = group_id
        if user_id is not None:
            params["user_id"] = user_id
        if user_name is not None:
            params["user_name"] = user_name
        if profile is not None:
            params["profile"] = profile
        if dataset is not None:
            params["dataset"] = dataset
        if model is not None:
            params["model"] = model
        if scaffold is not None:
            params["scaffold"] = scaffold
        if queue_id is not None:
            params["queue_id"] = queue_id
        if tag:
            params["tag"] = tag
        if tag_logic:
            params["tag_logic"] = tag_logic
        if meta_teacher_direction is not None:
            params["meta_teacher_direction"] = meta_teacher_direction
        if meta_train_stage is not None:
            params["meta_train_stage"] = meta_train_stage
        if meta_model is not None:
            params["meta_model"] = meta_model
        if meta_job_type is not None:
            params["meta_job_type"] = meta_job_type
        if upstream_platform is not None:
            params["upstream_platform"] = upstream_platform
        if upstream_job_id is not None:
            params["upstream_job_id"] = upstream_job_id
        if created_after is not None:
            params["created_after"] = created_after
        if created_before is not None:
            params["created_before"] = created_before
        if prefix_match:
            params["prefix_match"] = True
        return self._get("/groups", params=params)

    def list_group_jobs(
        self,
        group_id: str,
        tag: Optional[list[str]] = None,
        include_post_process: bool = False,
        skip: int = 0,
        limit: int = 100,
        tag_pattern: Optional[str] = None,
        tag_logic: Optional[str] = None,
        meta_teacher_direction: Optional[str] = None,
        meta_train_stage: Optional[str] = None,
        meta_model: Optional[str] = None,
        meta_job_type: Optional[str] = None,
        upstream_platform: Optional[str] = None,
        upstream_job_id: Optional[str] = None,
        next_token: Optional[str] = None,
        pagination: Optional[str] = None,
        include_total: bool = True,
    ) -> dict:
        """List jobs in a group."""
        params: dict = {"skip": skip, "limit": limit}
        if tag:
            params["tag"] = tag
        if tag_pattern:
            params["tag_pattern"] = tag_pattern
        if tag_logic:
            params["tag_logic"] = tag_logic
        if meta_teacher_direction is not None:
            params["meta_teacher_direction"] = meta_teacher_direction
        if meta_train_stage is not None:
            params["meta_train_stage"] = meta_train_stage
        if meta_model is not None:
            params["meta_model"] = meta_model
        if meta_job_type is not None:
            params["meta_job_type"] = meta_job_type
        if upstream_platform is not None:
            params["upstream_platform"] = upstream_platform
        if upstream_job_id is not None:
            params["upstream_job_id"] = upstream_job_id
        if include_post_process:
            params["include_post_process"] = True
        if next_token:
            params["next_token"] = next_token
        if pagination:
            params["pagination"] = pagination
        if not include_total:
            params["include_total"] = False
        endpoint = f"/groups/{quote(group_id)}/jobs"
        response = self._get(endpoint, params=params)
        _ensure_next_token_honored(response, next_token=next_token, endpoint=endpoint)
        return response

    def get_group_post_process_job_id(
        self, group_id: str, timeout: TimeoutType = None
    ) -> Optional[str]:
        """Return the post-process job id for a group, if configured."""
        group = self.get_group(group_id, timeout=timeout)
        return group.get("group_post_process_job_id")

    def get_group_post_process_job(
        self, group_id: str, timeout: TimeoutType = None
    ) -> Optional[dict]:
        """Return the post-process job for a group, if configured."""
        job_id = self.get_group_post_process_job_id(group_id, timeout=timeout)
        if not job_id:
            return None
        return self.get_job(job_id, timeout=timeout)

    def get_group_stats(self, group_id: str, timeout: TimeoutType = None) -> dict:
        """Get group progress."""
        return self._get(f"/groups/{quote(group_id)}/stats", timeout=timeout)

    def update_group(
        self,
        group_id: str,
        max_concurrency: Optional[int] = None,
        eval_config: Optional[dict] = None,
        model_base_url_collection: Optional[list] = None,
        dataset: Optional[str] = None,
        model: Optional[str] = None,
        scaffold: Optional[str] = None,
        tags: Optional[list] = None,
        meta_model: Optional[str] = None,
        meta_job_type: Optional[str] = None,
        meta_teacher_direction: Optional[str] = None,
        meta_train_stage: Optional[str] = None,
        benchmark: Optional[str] = None,
        priority: Optional[str] = None,
        priority_weight: Optional[int] = None,
        priority_update_mode: Optional[str] = None,
    ) -> dict:
        """Update group properties.

        ``benchmark`` is omitted when None; pass an empty string to clear it.

        ``tags``（`key:value` 数组）在客户端先与 Group 现有 tags 合并，再以
        全量替换语义提交（服务端 PATCH 是整体替换）；同名 key 覆盖，未提及
        的 key 保留。服务端会从 tags 同步 meta_* 等派生字段。

        ``meta_*`` 独立属性为部分更新（传了才改，不支持清除）；新服务端
        优先读属性，老服务端忽略属性——因此过渡期内同时也会将属性合并进
        tags 轨（双写）。

        Priority changes update the Group defaults. The default existing mode
        also updates all current Jobs, including PostProcess; incremental mode
        changes only the defaults for future Jobs. Updating priority alone uses
        weight 0; updating only weight preserves the current priority tier.
        """
        if priority is not None and priority not in {"high", "medium"}:
            raise ValueError("priority must be one of high/medium")
        if priority_update_mode is not None:
            if priority_update_mode not in {"existing", "incremental"}:
                raise ValueError("priority_update_mode must be one of existing/incremental")
            if priority is None and priority_weight is None:
                raise ValueError("priority_update_mode requires priority or priority_weight")
        body: dict = {}

        if max_concurrency is not None:
            body["max_concurrency"] = max_concurrency
        if eval_config is not None:
            body["eval_config"] = eval_config
        if model_base_url_collection is not None:
            body["model_base_url_collection"] = model_base_url_collection
        if dataset is not None:
            body["dataset"] = dataset
        if model is not None:
            body["model"] = model
        if scaffold is not None:
            body["scaffold"] = scaffold
        if benchmark is not None:
            body["benchmark"] = benchmark
        if priority is not None:
            body["priority"] = priority
        if priority_weight is not None:
            body["priority_weight"] = priority_weight
        if priority_update_mode is not None:
            body["priority_update_mode"] = priority_update_mode
        meta_attr_tags = _merge_meta_tags(
            None,
            meta_model=meta_model,
            meta_job_type=meta_job_type,
            meta_teacher_direction=meta_teacher_direction,
            meta_train_stage=meta_train_stage,
        )
        effective_tags = [*(tags or []), *(meta_attr_tags or [])] or None
        if effective_tags is not None:
            current = self.get_group(group_id)
            merged = dict(current.get("tags") or {})
            for raw in effective_tags:
                key, _, value = str(raw).partition(":")
                key = key.strip()
                if key:
                    merged[key] = value.strip()
            body["tags"] = merged
        _lift_meta_tags_to_attrs(body, body.get("tags"))

        return self._request("PATCH", f"/groups/{quote(group_id)}", json_body=body)

    def set_group_extra_aggregations(
        self,
        group_id: str,
        extra_aggregations: dict | None,
    ) -> dict:
        """Set ``eval_config["extra_aggregations"]`` for a group.

        The server's ``PATCH /groups/{group_id}`` replaces the *whole*
        ``eval_config`` dict, so this helper fetches the current group, merges
        the ``extra_aggregations`` key into the existing ``eval_config``, and
        writes the merged config back — leaving sibling keys (``group_by``,
        ``score_field``, ``aggregations``, ``category_field``,
        ``difficulty_field``, …) untouched.

        Pass ``None`` or an empty mapping to clear the key.

        Raises:
            ValueError: if ``extra_aggregations`` is structurally invalid
                (mirrors the server's aggregation-time validation, but raised
                here at config time so misconfiguration surfaces immediately).
        """
        _validate_extra_aggregations(extra_aggregations)
        group = self.get_group(group_id)
        eval_config = dict(group.get("eval_config") or {})
        if extra_aggregations:
            eval_config["extra_aggregations"] = extra_aggregations
        else:
            eval_config.pop("extra_aggregations", None)
        return self.update_group(group_id, eval_config=eval_config)

    def pause_group(self, group_id: str) -> dict:
        """Pause scheduling for a group."""
        return self._post(f"/groups/{quote(group_id)}/pause", {})

    def resume_group(self, group_id: str) -> dict:
        """Resume scheduling for a group."""
        return self._post(f"/groups/{quote(group_id)}/resume", {})

    def get_group_eval(self, group_id: str) -> dict:
        """Get aggregated evaluation results for a group."""
        return self._get(f"/groups/{quote(group_id)}/eval")

    def get_group_eval_summary(self, group_id: str) -> dict:
        """Get aggregated evaluation summary for a group, without per-task results."""
        return self._get(f"/groups/{quote(group_id)}/eval_summary")

    # ==================== DataSources ====================
    def create_datasource(
        self,
        name: str,
        type: str,
        uri: str,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        endpoint: Optional[str] = None,
        access_mode: Optional[str] = None,
        mount_path: Optional[str] = None,
        extras: Optional[dict] = None,
        timeout: TimeoutType = None,
    ) -> dict:
        """Create a data source. type must be 'oss', 'nas' or 'cpfs'."""
        body: dict = {"name": name, "type": type, "uri": uri}
        if access_key_id is not None:
            body["access_key_id"] = access_key_id
        if access_key_secret is not None:
            body["access_key_secret"] = access_key_secret
        if endpoint is not None:
            body["endpoint"] = endpoint
        if access_mode is not None:
            body["access_mode"] = access_mode
        if mount_path is not None:
            body["mount_path"] = mount_path
        if extras is not None:
            body["extras"] = extras
        return self._post("/datasources", body, timeout=timeout)

    def list_datasources(
        self,
        type: Optional[str] = None,
        name: Optional[str] = None,
        all_users: bool = False,
        skip: int = 0,
        limit: int = 200,
    ) -> dict:
        """List datasources visible to the caller."""
        params: dict = {"skip": skip, "limit": limit}
        if type is not None:
            params["type"] = type
        if name is not None:
            params["name"] = name
        if all_users:
            params["all_users"] = "true"
        return self._get("/datasources", params=params)

    def get_datasource(self, identifier: str) -> dict:
        """Get a data source by ObjectId, datasource_id, or name."""
        return self._get(f"/datasources/{quote(identifier)}")

    def update_datasource(
        self,
        identifier: str,
        name: Optional[str] = None,
        type: Optional[str] = None,
        uri: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        endpoint: Optional[str] = None,
        access_mode: Optional[str] = None,
        mount_path: Optional[str] = None,
        extras: Optional[dict] = None,
    ) -> dict:
        """Update mutable fields on a data source."""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if type is not None:
            body["type"] = type
        if uri is not None:
            body["uri"] = uri
        if access_key_id is not None:
            body["access_key_id"] = access_key_id
        if access_key_secret is not None:
            body["access_key_secret"] = access_key_secret
        if endpoint is not None:
            body["endpoint"] = endpoint
        if access_mode is not None:
            body["access_mode"] = access_mode
        if mount_path is not None:
            body["mount_path"] = mount_path
        if extras is not None:
            body["extras"] = extras
        return self._request("PUT", f"/datasources/{quote(identifier)}", json_body=body)

    def delete_datasource(self, identifier: str) -> dict:
        """Delete a data source by identifier."""
        return self._delete(f"/datasources/{quote(identifier)}")

    # ==================== Concurrency Policies ====================
    def create_concurrency_policy(
        self,
        name: str,
        capacity: int,
        queue_id: str,
        scope: str = "cluster",
        label: Optional[dict] = None,
        enabled: bool = True,
        timeout: TimeoutType = None,
    ) -> dict:
        """Create a concurrency policy (server-generated ``cp-<uuid>`` policy_id).

        ``queue_id`` is required — every resource is owned by a queue, and only
        queue members with write access may manage it (same-queue visible &
        modifiable). ``policy_id`` is always generated by the server; the
        create endpoint does not accept a client-supplied id.
        """
        body: dict = {"name": name, "capacity": capacity, "enabled": enabled, "queue_id": queue_id}
        body["scope"] = scope
        if label:
            body["label"] = label
        return self._post("/concurrency-policies", body, timeout=timeout)

    def list_concurrency_policies(
        self,
        queue_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 200,
    ) -> dict:
        """List concurrency policies (visible to your associated queues)."""
        params: dict = {"skip": skip, "limit": limit}
        if queue_id is not None:
            params["queue_id"] = queue_id
        return self._get("/concurrency-policies", params=params)

    def get_concurrency_policy(self, policy_id: str) -> dict:
        """Get a single concurrency policy by policy_id."""
        return self._get(f"/concurrency-policies/{quote(policy_id)}")

    def update_concurrency_policy(
        self,
        policy_id: str,
        name: Optional[str] = None,
        scope: Optional[str] = None,
        queue_id: Optional[str] = None,
        label: Optional[dict] = None,
        capacity: Optional[int] = None,
        enabled: Optional[bool] = None,
        reason: Optional[str] = None,
    ) -> dict:
        """Partially update a concurrency policy (upsert: creates if absent)."""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if scope is not None:
            body["scope"] = scope
        if queue_id is not None:
            body["queue_id"] = queue_id
        if label is not None:
            body["label"] = label
        if capacity is not None:
            body["capacity"] = capacity
        if enabled is not None:
            body["enabled"] = enabled
        if reason is not None:
            body["reason"] = reason
        return self._request("PATCH", f"/concurrency-policies/{quote(policy_id)}", json_body=body)

    def delete_concurrency_policy(self, policy_id: str) -> dict:
        """Delete a concurrency policy by policy_id (requires write access on the owning queue)."""
        return self._delete(f"/concurrency-policies/{quote(policy_id)}")

    # ==================== Logs and artifacts ====================
    def preview_group_cancel(self, group_id: str) -> dict:
        """Preview the current Group cancel scope and obtain confirmation if required."""
        return self._post(f"/groups/{quote(group_id)}/cancel-preview", {})

    def cancel_group(self, group_id: str, confirmation_token: Optional[str] = None) -> dict:
        """Cancel all unfinished jobs in a group."""
        body = {"confirmation_token": confirmation_token} if confirmation_token else {}
        return self._post(f"/groups/{quote(group_id)}/cancel", body)

    def get_job_logs(
        self,
        job_id: str,
        container: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 500,
    ) -> dict:
        """获取任务日志

        Args:
            job_id: 任务ID
            container: 容器名称，如果为None则返回所有容器日志
            offset: 分页偏移量，用于获取后续日志页
            limit: 分页大小，默认为500
        """
        params = {}
        if container:
            params["container"] = container
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit
        return self._get(f"/jobs/{quote(job_id)}/logs", params=params or None)

    def get_job_logs_complete(self, job_id: str, container: str) -> dict:
        """获取完整日志（自动处理分页）

        一直调用接口直到返回的next_offset为空，标识日志获取完成

        Args:
            job_id: 任务ID
            container: 容器名称

        Returns:
            dict: 所有日志
        """
        all_logs = []
        offset = 0

        while True:
            result = self.get_job_logs(job_id=job_id, container=container, offset=offset, limit=500)

            # 提取日志数据
            if "logs" in result and isinstance(result["logs"], list):
                all_logs.extend(result["logs"])

            # 检查是否还有更多日志
            next_offset = result.get("next_offset")
            if next_offset is None:
                break

            offset = next_offset

        return {"logs": all_logs, "container": container, "job_id": job_id}

    def get_job_events(self, job_id: str, container: Optional[str] = None) -> dict:
        """Get job events."""
        params = {}
        if container:
            params["container"] = container
        return self._get(f"/jobs/{quote(job_id)}/events", params=params or None)

    def get_job_containers(self, job_id: str) -> dict:
        """Get all container names for a job.

        Args:
            job_id: The job ID to get containers for
        """
        return self._get(f"/jobs/{quote(job_id)}/containers")

    def get_ws_terminal_info(
        self,
        job_id: str,
        container: str = "main",
        command: list = None,
        tty: bool = True,
        cols: int = 0,
        rows: int = 0,
    ) -> tuple[str, dict]:
        """构建 WebSocket 终端连接的 URI 和认证 headers。

        将 base_url 的 http:// → ws://、https:// → wss://，
        复用 _url() 的逻辑确定是否需要 /api 前缀。

        Args:
            job_id: 任务 ID
            container: 容器名称，默认 "main"
            command: 执行命令列表，默认 None
            tty: 是否启用 TTY，默认 True
            cols: 终端列数，0 表示不指定
            rows: 终端行数，0 表示不指定

        Returns:
            (ws_uri, extra_headers) 元组
        """
        # 协议转换: http → ws, https → wss
        base_url = self.config.base_url
        if base_url.startswith("https://"):
            ws_base = "wss://" + base_url[len("https://") :]
        elif base_url.startswith("http://"):
            ws_base = "ws://" + base_url[len("http://") :]
        else:
            # 非标准协议地址，直接使用
            ws_base = base_url

        # 复用 _url() 逻辑确定路径前缀
        path = f"/ws/jobs/{quote(job_id)}/terminal"
        if (
            path.startswith("/")
            and "/api" not in base_url
            and "nlb-" not in base_url
            and "localhost" not in base_url
        ):
            path = f"/api{path}"

        # 构建查询参数
        query_params = f"container={quote(container)}"
        if command:
            import json as _json

            query_params += f"&command={quote(_json.dumps(command))}"
        if not tty:
            query_params += "&tty=false"
        if cols > 0:
            query_params += f"&cols={cols}"
        if rows > 0:
            query_params += f"&rows={rows}"

        # 兼容网关两种路由方式: 如果 headers 中有 X-Cluster，也添加到 query 参数
        cluster = self.session.headers.get("X-Cluster")
        if cluster:
            query_params += f"&cluster={quote(cluster)}"

        ws_uri = f"{ws_base}{path}?{query_params}"

        # 提取 session headers，去掉 WebSocket 不兼容的 header
        # - Content-Type: WebSocket 不需要
        # - Connection: requests 默认 "keep-alive"，会覆盖 websockets 自动设置的
        #   "Connection: Upgrade"，导致服务端拒绝 WebSocket 握手返回 404
        _skip = {"content-type", "connection"}
        extra_headers = {k: v for k, v in self.session.headers.items() if k.lower() not in _skip}

        return (ws_uri, extra_headers)

    def get_job_metrics(self, job_id: str) -> dict:
        """Get job metrics."""
        return self._get(f"/metrics/{quote(job_id)}")

    def cancel_job(self, job_id: str) -> dict:
        """Cancel a job."""
        return self._delete(f"/jobs/{quote(job_id)}")

    def retry_job(
        self,
        job_id: str,
        params: Optional[dict] = None,
        delete_params: Optional[list[str]] = None,
        timeout: TimeoutType = None,
    ) -> dict:
        """Retry a terminal job."""
        body = None
        if params is not None or delete_params:
            body = {}
            if params is not None:
                body["params"] = params
            if delete_params:
                body["delete_params"] = delete_params
        return self._request(
            "POST",
            f"/jobs/{quote(job_id)}/retry",
            json_body=body,
            timeout=timeout,
        )

    def get_group_artifacts_page(
        self,
        group_id: str,
        *,
        skip: int = 0,
        limit: int = _GROUP_ARTIFACTS_PAGE_SIZE,
        include_post_process: bool = False,
        next_token: Optional[str] = None,
        pagination: Optional[str] = None,
        include_total: bool = True,
        download_mode: Optional[Literal["oss", "proxy", "both"]] = None,
    ) -> dict:
        """Get one page of archive links.

        Omit download_mode for the server default and legacy response. Explicit
        oss/proxy/both modes add a downloads mapping to each artifact; both can
        return only one successful provider. This method does not download files.
        """
        params: dict[str, object] = {"skip": skip, "limit": limit}
        if include_post_process:
            params["include_post_process"] = True
        if next_token:
            params["next_token"] = next_token
        if pagination:
            params["pagination"] = pagination
        if not include_total:
            params["include_total"] = False
        if download_mode is not None:
            params["download_mode"] = download_mode
        endpoint = f"/groups/{quote(group_id)}/artifacts"
        response = self._get(endpoint, params=params)
        _ensure_next_token_honored(response, next_token=next_token, endpoint=endpoint)
        return response

    def get_group_artifacts(
        self,
        group_id: str,
        include_post_process: bool = False,
        *,
        download_mode: Optional[Literal["oss", "proxy", "both"]] = None,
    ) -> dict:
        """Collect all archive-link pages, preserving download_mode on every page."""
        next_token: str | None = None
        skip = 0
        mode: str | None = None
        artifacts: list[dict] = []
        last_page: dict | None = None

        download_options = {"download_mode": download_mode} if download_mode is not None else {}
        while True:
            page = self.get_group_artifacts_page(
                group_id,
                skip=skip,
                limit=_GROUP_ARTIFACTS_PAGE_SIZE,
                include_post_process=include_post_process,
                next_token=next_token,
                pagination="cursor" if mode in {None, "cursor"} else None,
                include_total=False,
                **download_options,
            )
            last_page = page
            page_artifacts = page.get("artifacts") or []
            artifacts.extend(page_artifacts)
            has_token_field = "next_token" in page

            if mode is None:
                mode = "cursor" if has_token_field else "offset"

            if mode == "cursor":
                next_token = page.get("next_token")
                if not next_token:
                    break
            else:
                skip += len(page_artifacts)
                total = page.get("total")
                if not page_artifacts or len(page_artifacts) < _GROUP_ARTIFACTS_PAGE_SIZE:
                    break
                if total is not None and skip >= total:
                    break

        result = dict(last_page or {})
        result.pop("next_token", None)
        result.update(
            {
                "total": len(artifacts),
                "skip": 0,
                "limit": len(artifacts),
                "artifacts": artifacts,
            }
        )
        return result

    def get_job_artifacts(
        self,
        job_ids: list,
        *,
        download_mode: Optional[Literal["oss", "proxy", "both"]] = None,
    ) -> list:
        """Get archive links; explicit modes also return typed ``downloads`` entries."""
        body = {"job_ids": job_ids}
        if download_mode is not None:
            body["download_mode"] = download_mode
        return self._post("/jobs/artifacts", body)

    def get_job_artifacts_manifest(
        self,
        job_id: str,
        *,
        require_file_download: bool = False,
    ) -> dict:
        """Get the file manifest for one job's artifacts."""
        params = {"require_file_download": "true"} if require_file_download else None
        return self._get(
            f"/jobs/{quote(job_id, safe='')}/artifacts-manifest",
            params=params,
        )

    def wait_for_job_artifacts_manifest(self, job_id: str) -> dict:
        """Poll the new API within one per-Job budget; HTTP failures keep normal retries."""
        budget = self.config.artifact_manifest_wait_timeout
        if not math.isfinite(budget) or budget <= 0:
            raise ConfigurationError(
                "AP_ARTIFACT_MANIFEST_WAIT_TIMEOUT must be a finite positive number"
            )
        deadline = time.monotonic() + budget
        while True:
            response, request_id = self._request(
                "GET",
                f"/jobs/{quote(job_id, safe='')}/artifacts/manifest",
                deadline=deadline,
                _return_response=True,
            )
            try:
                payload = response.json()
            except ValueError as exc:
                raise APIError(
                    response.status_code, "Invalid artifact manifest response", request_id, response
                ) from exc
            if not isinstance(payload, dict) or payload.get("job_id") != job_id:
                raise APIError(
                    response.status_code, "Invalid artifact manifest response", request_id, response
                )
            if response.status_code == 200:
                if "manifest" not in payload or (
                    payload["manifest"] is not None and not isinstance(payload["manifest"], list)
                ):
                    raise APIError(200, "Invalid artifact manifest response", request_id, response)
                return payload
            if response.status_code != 202 or payload.get("status") != "preparing":
                raise APIError(
                    response.status_code,
                    "Invalid artifact preparation response",
                    request_id,
                    response,
                )
            try:
                delay = float(response.headers.get("Retry-After", "2"))
            except ValueError:
                delay = 2.0
            if not math.isfinite(delay) or delay <= 0:
                delay = 2.0
            _deadline_sleep(delay, deadline)

    def get_artifact_file_download_urls(self, job_id: str, paths: list[str]) -> dict:
        """Get download URLs for multiple artifact files."""
        endpoint = f"/jobs/{quote(job_id, safe='')}/artifacts/files/download"
        return self._post(endpoint, {"paths": paths})

    def render_template(self, name: str, params: dict) -> dict:
        """Preview the rendered template output."""
        query_params = {}
        if self.config.agenthub_ref:
            query_params["agenthub_revision"] = self.config.agenthub_ref
        return self._request(
            "POST",
            f"/templates/{quote(name)}/render",
            params=query_params,
            json_body={"params": params},
        )

    def fetch_repo(self) -> dict:
        """Trigger a repo fetch and return the resolved ref + commit."""
        query_params = {}
        if self.config.agenthub_ref:
            query_params["agenthub_revision"] = self.config.agenthub_ref
        return self._request("POST", "/admin/repo/fetch", params=query_params)

    # ==================== Eval Plan operations ====================

    def create_eval_plan(
        self,
        name: str,
        job_spec: dict,
        cron_expression: str,
        valid_from: str,
        valid_until: str,
        description: Optional[str] = None,
    ) -> dict:
        """Create an eval plan."""
        body: dict = {
            "name": name,
            "job_spec": job_spec,
            "cron_expression": cron_expression,
            "valid_from": valid_from,
            "valid_until": valid_until,
        }
        if description is not None:
            body["description"] = description
        return self._post("/eval-plans", body)

    def list_eval_plans(
        self,
        status: Optional[str] = None,
        user_id: Optional[str] = None,
        created_after: Optional[str] = None,
        created_before: Optional[str] = None,
        skip: int = 0,
        limit: int = -1,
    ) -> dict:
        """List eval plans with optional filters."""
        params: dict = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if user_id:
            params["user_id"] = user_id
        if created_after:
            params["created_after"] = created_after
        if created_before:
            params["created_before"] = created_before
        return self._get("/eval-plans", params=params)

    def get_eval_plan(self, plan_id: str) -> dict:
        """Get eval plan detail."""
        return self._get(f"/eval-plans/{quote(plan_id)}")

    def update_eval_plan(
        self,
        plan_id: str,
        name: Optional[str] = None,
        job_spec: Optional[dict] = None,
        cron_expression: Optional[str] = None,
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
    ) -> dict:
        """Update an eval plan.

        All fields except *plan_id* are optional — only provided fields
        are included in the PATCH request body.
        """
        body: dict = {}
        if name is not None:
            body["name"] = name
        if job_spec is not None:
            body["job_spec"] = job_spec
        if cron_expression is not None:
            body["cron_expression"] = cron_expression
        if valid_from is not None:
            body["valid_from"] = valid_from
        if valid_until is not None:
            body["valid_until"] = valid_until
        if description is not None:
            body["description"] = description
        if status is not None:
            body["status"] = status
        return self._request("PATCH", f"/eval-plans/{quote(plan_id)}", json_body=body)

    def delete_eval_plan(self, plan_id: str) -> dict:
        """Permanently delete an eval plan from MongoDB."""
        return self._delete(f"/eval-plans/{quote(plan_id)}")

    def trigger_eval_plan(self, plan_id: str) -> dict:
        """Manual trigger — creates Group + Jobs."""
        return self._post(f"/eval-plans/{quote(plan_id)}/trigger", {})

    def list_eval_plan_runs(
        self,
        plan_id: str,
        skip: int = 0,
        limit: int = -1,
    ) -> dict:
        """List historical runs for an eval plan."""
        return self._get(
            f"/eval-plans/{quote(plan_id)}/runs", params={"skip": skip, "limit": limit}
        )

    # ==================== Template Credentials ====================

    def create_template_credential(
        self,
        credential_name: str,
        template: str,
        content: dict,
        credential_type: str = "",
    ) -> dict:
        """Create a new template credential."""
        body = {
            "credential_name": credential_name,
            "template": template,
            "credential_type": credential_type,
            "content": content,
        }
        return self._post("/template_credentials", body)

    def list_template_credentials(
        self,
        template: Optional[str] = None,
        credential_name: Optional[str] = None,
        credential_type: Optional[str] = None,
    ) -> list:
        """List template credentials with optional filters."""
        params: dict = {}
        if template is not None:
            params["template"] = template
        if credential_name is not None:
            params["credential_name"] = credential_name
        if credential_type is not None:
            params["credential_type"] = credential_type
        return self._get("/template_credentials", params=params if params else None)

    def get_template_credential(self, identifier: str) -> dict:
        """Get a template credential by ID or credential_name."""
        return self._get(f"/template_credentials/{quote(identifier)}")

    def update_template_credential(
        self,
        identifier: str,
        content: dict | None = None,
        credential_type: str | None = None,
    ) -> dict:
        """Update a template credential's content and/or credential_type."""
        body: dict = {}
        if content is not None:
            body["content"] = content
        if credential_type is not None:
            body["credential_type"] = credential_type
        return self._request("PUT", f"/template_credentials/{quote(identifier)}", json_body=body)

    def delete_template_credential(self, identifier: str) -> dict:
        """Delete a template credential by ID or credential_name."""
        return self._delete(f"/template_credentials/{quote(identifier)}")

    # ==================== Secret operations (Central AP) ====================

    def create_secret(
        self,
        name: str,
        data: dict,
        description: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> dict:
        """Create a platform secret in the central AP.

        The created_by field is automatically extracted from the JWT token
        on the server side — the client does not need to pass it.

        Args:
            name: Secret name (unique within ``workspace_id``).
            data: Secret data dict. String values are env vars,
                  {content, filename} objects are file credentials.
            description: Optional description.
            workspace_id: Owning WorkSpace. Names are unique per WorkSpace, so this
                is part of the secret's identity — pass the same value to the
                name-addressed get/update/delete/ACL calls. Server defaults to
                nothing (workspace_id is required); the CLI defaults to "default".
        """
        body: dict = {"name": name, "data": data}
        if workspace_id is not None:
            body["workspace_id"] = workspace_id
        if description is not None:
            body["description"] = description
        return self._post_central("/secrets", body)

    def list_secrets(
        self,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """List secrets accessible to the current user (from the central AP).

        Returns paginated results with masked values. Includes:
        - Secrets owned by the current user (role="owner", with masked data)
        - Secrets shared to the current user via ACL (role="use", metadata only, no data)
        """
        return self._get_central("/secrets", params={"page": page, "page_size": page_size})

    def get_secret(self, name: str, workspace_id: Optional[str] = None) -> dict:
        """Get a secret by name (masked values) from the central AP.

        ``(name, workspace_id)`` is the composite unique key, so ``workspace_id``
        is the locating dimension — omit it and the server falls back to the
        "default" WorkSpace. The caller must have owner or use access.

        For cross-user access use get_secret_by_id(secret_id): a grantee that also
        owns a same-named secret cannot reach the granted one by name.
        """
        return self._get_central(f"/secrets/{quote(name)}", params=_secret_ws_params(workspace_id))

    def get_secret_by_id(self, secret_id: str) -> dict:
        """Get a secret by its globally unique secret_id (masked values).

        Unlike get_secret(name), this method needs no ``workspace_id`` and is
        unambiguous even when the same name exists in several WorkSpaces.

        The caller must have owner or use access to the secret. Non-owners
        receive metadata only (no data field).

        Args:
            secret_id: The globally unique secret ID (e.g. "secret-uf600987gapsl25fwm7s").
        """
        return self._get_central(f"/secrets/id/{quote(secret_id)}")

    def update_secret(
        self,
        name: str,
        data: Optional[dict] = None,
        description: Optional[str] = None,
        workspace_id: Optional[str] = None,
    ) -> dict:
        """Update a secret in the central AP.

        Only the secret owner (or a superuser) can update it. ``name`` and
        ``workspace_id`` are part of the composite unique key and cannot be changed;
        ``workspace_id`` here only locates the secret.
        """
        body: dict = {}
        if data is not None:
            body["data"] = data
        if description is not None:
            body["description"] = description
        return self._put_central(
            f"/secrets/{quote(name)}", body, params=_secret_ws_params(workspace_id)
        )

    def delete_secret(self, name: str, workspace_id: Optional[str] = None) -> dict:
        """Delete a secret by name from the central AP.

        Only the secret owner (or a superuser) can delete it. ``workspace_id``
        locates the secret within its WorkSpace.
        """
        return self._delete_central(
            f"/secrets/{quote(name)}", params=_secret_ws_params(workspace_id)
        )

    def grant_secret_acl(
        self,
        name: str,
        principal_type: str,
        principal_id: str,
        permission: str = "use",
        workspace_id: Optional[str] = None,
    ) -> dict:
        """Grant ACL access to a secret (owner-only operation).

        Server-side this becomes a scope=resource role_binding
        (role_id=built-in:secret-user) — see the apiserver RBAC design.

        Args:
            name: Secret name.
            principal_type: "user" or "user_group".
            principal_id: User ID or user group ID to grant access to.
            permission: Permission to grant (currently only "use" supported).
            workspace_id: WorkSpace locating the secret (defaults to "default").
        """
        body = {
            "principal_type": principal_type,
            "principal_id": principal_id,
            "permission": permission,
        }
        return self._post_central(
            f"/secrets/{quote(name)}/acl", body, params=_secret_ws_params(workspace_id)
        )

    def revoke_secret_acl(
        self,
        name: str,
        principal_type: str,
        principal_id: str,
        workspace_id: Optional[str] = None,
    ) -> dict:
        """Revoke ACL access from a secret (owner-only operation).

        Args:
            name: Secret name.
            principal_type: "user" or "user_group".
            principal_id: User ID or user group ID to revoke access from.
            workspace_id: WorkSpace locating the secret (defaults to "default").
        """
        return self._delete_central(
            f"/secrets/{quote(name)}/acl/{quote(principal_type)}/{quote(principal_id)}",
            params=_secret_ws_params(workspace_id),
        )

    def list_secret_acl(self, name: str, workspace_id: Optional[str] = None) -> dict:
        """List ACL entries for a secret (owner-only operation).

        Entries are projected from the secret's scope=resource role_bindings.

        Args:
            name: Secret name.
            workspace_id: WorkSpace locating the secret (defaults to "default").
        """
        return self._get_central(
            f"/secrets/{quote(name)}/acl", params=_secret_ws_params(workspace_id)
        )

    # ==================== Cluster operations ====================

    def list_clusters(self, timeout: TimeoutType = None) -> dict:
        """List platform-supported clusters from the central AP.

        Returns ``{"clusters": [...]}`` where each entry carries
        ``name`` / ``cluster_id`` / ``region`` / ``url_cluster`` (the slug
        accepted by ``--cluster`` and ``AP_CLUSTER``) plus optional
        ``group`` / ``description`` / ``hidden`` / ``default`` / ``quota``.
        Does not require X-Cluster to be configured.
        """
        return self._get_central("/clusters", timeout=timeout)

    # ==================== Profile operations ====================

    _PROFILES_BASE = "/apis/v1/profiles"

    def _resolve_self_user_id(self) -> Optional[str]:
        """Resolve the current caller's user_id via the configured API key.

        The API server's ``GET /apis/v1/users/<id>`` endpoint accepts both
        a user_id and a raw API key as the path parameter. We use the API
        key form to look up the caller's identity, then cache the result
        on the client instance to avoid an extra round-trip per request.

        Returns None when no API key is configured or the lookup fails.
        """
        if not self.config.token_key:
            return None
        cached = getattr(self, "_cached_self_user_id", _UNSET)
        if cached is not _UNSET:
            return cached
        try:
            user = self._get(f"/apis/v1/users/{quote(self.config.token_key, safe='')}")
            user_id = user.get("user_id") if isinstance(user, dict) else None
        except APIError as exc:
            # 404 / 401 / 403 → key genuinely invalid or unauthorized;
            # cache None so we don't retry on every call.
            if exc.status_code in (401, 403, 404):
                user_id = None
            else:
                # 5xx, network, non-JSON, etc. → transient; don't cache,
                # let the caller see the real error.
                raise
        self._cached_self_user_id = user_id or None
        return self._cached_self_user_id

    def create_profile(
        self,
        name: str,
        spec: dict,
        description: str = "",
        account_pool: Optional[str] = None,
        metadata: Optional[dict] = None,
        tags: Optional[list[str]] = None,
    ) -> dict:
        """Create a new submission profile."""
        body: dict = {"name": name, "spec": spec}
        if description:
            body["description"] = description
        if account_pool is not None:
            body["account_pool"] = account_pool
        if metadata is not None:
            body["metadata"] = metadata
        if tags is not None:
            body["tags"] = tags
        return self._post(self._PROFILES_BASE, body)

    def list_profiles(
        self,
        *,
        keyword: Optional[str] = None,
        template: Optional[str] = None,
        dataset: Optional[str] = None,
        scaffold: Optional[str] = None,
        owner: Optional[str] = None,
        profile_ids: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
        show_all: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """List submission profiles.

        Args:
            keyword: Filter by name keyword.
            template: Filter by template name.
            dataset: Filter by metadata dataset using a case-insensitive substring match.
            scaffold: Filter by metadata scaffold using a case-insensitive substring match.
            owner: Filter by an explicit owner ID instead of the current caller.
            profile_ids: Filter by profile IDs (maximum 100; mutually exclusive
                with ``keyword``).
            tags: Filter by profile tags using AND semantics (maximum 10).
            show_all: If False (default), return only profiles owned by the
                current caller — the owner filter is resolved client-side
                via the configured API key, mirroring how the web console
                appends ``owner=<user_id>`` to its requests. If True, omit
                the owner filter and return all visible profiles.
            page: Page number (1-based).
            page_size: Number of items per page.

        Raises:
            ConfigurationError: When the default Mine view needs an API key
                but none is configured, or the key cannot be resolved.
            ValueError: When mutually exclusive filters are combined.
        """
        if keyword and profile_ids:
            raise ValueError("profile_ids and keyword are mutually exclusive")
        if owner and show_all:
            raise ValueError("owner and show_all are mutually exclusive")
        if profile_ids and len(profile_ids) > 100:
            raise ValueError("profile_ids accepts at most 100 values")
        if tags and len(tags) > 10:
            raise ValueError("tags accepts at most 10 values")

        params: dict = {"page": page, "page_size": page_size}
        if keyword:
            params["keyword"] = keyword
        if template:
            params["template"] = template
        if dataset:
            params["dataset"] = dataset
        if scaffold:
            params["scaffold"] = scaffold
        if profile_ids:
            params["profile_ids"] = ",".join(profile_ids)
        if tags:
            params["tags"] = ",".join(tags)
        if owner:
            params["owner"] = owner
        elif not show_all:
            if not self.config.token_key:
                raise ConfigurationError(
                    "Cannot list own profiles without authentication. "
                    "Set AP_API_KEY environment variable or use --all."
                )
            try:
                owner_id = self._resolve_self_user_id()
            except APIError as exc:
                raise ConfigurationError(
                    f"Failed to resolve user identity for owner filter "
                    f"(upstream {exc.status_code}). Please retry or use --all."
                ) from exc
            if not owner_id:
                raise ConfigurationError(
                    "Failed to resolve current user via AP_API_KEY. "
                    "Please verify the API key is valid."
                )
            params["owner"] = owner_id
        return self._get(self._PROFILES_BASE, params=params)

    def list_profile_tags(
        self,
        *,
        query: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """List distinct tags for SDK consumers building tag selectors or completion UIs."""
        params: dict = {}
        if query:
            params["q"] = query
        if limit is not None:
            params["limit"] = limit
        return self._get(f"{self._PROFILES_BASE}/tags", params=params)

    def replace_profile_tags(self, profile_id: str, tags: list[str]) -> dict:
        """Replace all tags on a submission profile; an empty list clears them."""
        return self._put(
            f"{self._PROFILES_BASE}/{quote(profile_id)}/tags",
            {"tags": tags},
        )

    def get_profile(self, id_or_name: str, *, version: Optional[int] = None) -> dict:
        """Get a submission profile by ID or name.

        If version is specified, returns that specific version.
        """
        if version is not None:
            return self._get(f"{self._PROFILES_BASE}/{quote(id_or_name)}/versions/{version}")
        return self._get(f"{self._PROFILES_BASE}/{quote(id_or_name)}")

    def update_profile_job_meta(self, profile_id: str, patch: dict) -> dict:
        """Patch live Job defaults without changing the Profile version.

        Omitted fields stay unchanged. Set benchmark to None to clear it.
        Tags use {"append": [...], "remove": [...]} and are applied atomically.
        """
        return self._request_central(
            "PATCH", f"/profiles/{quote(profile_id, safe='')}/job-meta", json_body=patch
        )

    def replace_profile_job_meta(self, profile_id: str, job_meta: dict) -> dict:
        """Replace all live Job defaults; {} clears benchmark and tags.

        This does not change spec, Profile tags, version, verification or release.
        """
        return self._put_central(f"/profiles/{quote(profile_id, safe='')}/job-meta", job_meta)

    def update_profile(
        self,
        profile_id: str,
        name: str,
        spec: dict,
        description: str = "",
        account_pool: Optional[str] = None,
        metadata: Optional[dict] = None,
        reason: Optional[str] = None,
    ) -> dict:
        """Update a submission profile, preserving an omitted default Pool.

        reason describes this update; omission never reuses a previous reason.
        The server validates whether it is required and its 500-character limit.
        """
        body: dict = {"name": name, "spec": spec}
        if description:
            body["description"] = description
        if account_pool is not None:
            body["account_pool"] = account_pool
        if metadata is not None:
            body["metadata"] = metadata
        if reason is not None:
            body["reason"] = reason
        return self._put(f"{self._PROFILES_BASE}/{quote(profile_id)}", body)

    def delete_profile(self, profile_id: str) -> dict:
        """Delete a submission profile."""
        return self._delete(f"{self._PROFILES_BASE}/{quote(profile_id)}")

    # ---- RBAC v2 实例级委托：job/group 单实例访问授权（scope=resource） ----

    _ROLE_BINDINGS_BASE = "/apis/v1/role-bindings"

    def grant_resource_access(
        self,
        *,
        resource_type: str,
        resource_id: str,
        workspace_id: str,
        role_id: str,
        principal_id: str,
        principal_type: str = "user",
    ) -> dict:
        """把某个 job/group 实例的访问权授予某 user/user_group（scope=resource 绑定）。

        workspace_id = 该实例所属 queue_id；Job/Group Owner、Group Admin 或所属
        WorkSpace 的管理员/创建者及平台管理员可授权。鉴权走当前 API Key 解析出的调用者身份。
        """
        body = {
            "scope": "resource",
            "resource_type": resource_type,
            "resource_id": resource_id,
            "workspace_id": workspace_id,
            "role_id": role_id,
            "principal_type": principal_type,
            "principal_id": principal_id,
        }
        return self._post(self._ROLE_BINDINGS_BASE, body)

    def revoke_resource_access(
        self,
        *,
        resource_type: str,
        resource_id: str,
        role_id: str,
        principal_id: str,
        principal_type: str = "user",
    ) -> Any:
        """撤销某 job/group 实例的实例级委托绑定（无需 workspace_id：apiserver 按存量落库值门控）。"""
        params = {
            "scope": "resource",
            "resource_type": resource_type,
            "resource_id": resource_id,
            "role_id": role_id,
            "principal_type": principal_type,
            "principal_id": principal_id,
        }
        return self._delete(self._ROLE_BINDINGS_BASE, params=params)

    def list_resource_access(self, *, resource_type: str, resource_id: str) -> Any:
        """列出某 job/group 实例上的全部实例级委托绑定（谁能访问这个实例）。"""
        params = {
            "scope": "resource",
            "resource_type": resource_type,
            "resource_id": resource_id,
        }
        return self._get(self._ROLE_BINDINGS_BASE, params=params)

    def list_profile_versions(
        self,
        profile_id: str,
        *,
        page: int = 1,
        page_size: int = 20,
    ) -> dict:
        """List all versions of a submission profile."""
        params: dict = {"page": page, "page_size": page_size}
        return self._get(f"{self._PROFILES_BASE}/{quote(profile_id)}/versions", params=params)

    def verify_profile_version(
        self,
        profile_id: str,
        version: int,
        group_id: str,
    ) -> dict:
        """Verify a specific version of a submission profile."""
        body: dict = {"group_id": group_id}
        return self._post(
            f"{self._PROFILES_BASE}/{quote(profile_id)}/versions/{version}/verification",
            body,
        )

    def revoke_profile_verification(
        self,
        profile_id: str,
        version: int,
    ) -> dict:
        """Revoke verification for a specific version of a submission profile."""
        return self._delete(
            f"{self._PROFILES_BASE}/{quote(profile_id)}/versions/{version}/verification"
        )


_verbose_override: Optional[bool] = None
_cluster_override: Optional[str] = None


def set_verbose_override(value: Optional[bool]) -> None:
    """Set a process-wide verbose override consulted by get_client()."""
    global _verbose_override
    _verbose_override = value


def set_cluster_override(value: Optional[str]) -> None:
    """Set a process-wide cluster override consulted by get_client()."""
    global _cluster_override
    _cluster_override = value


def get_client(
    agenthub_ref: Optional[str] = None,
    cluster: Optional[str] = None,
) -> APIClient:
    """Get an API client."""
    return APIClient(
        get_config(
            verbose=_verbose_override,
            agenthub_ref=agenthub_ref,
            cluster=cluster if cluster is not None else _cluster_override,
        )
    )


def _build_user_agent(existing: Optional[str] = None) -> str:
    """Build client User-Agent string."""
    client_ua = (
        f"ap-client/{_client_version()} "
        f"python/{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} "
        f"{platform.system().lower()}/{platform.machine().lower()}"
    )
    if existing:
        return f"{existing} {client_ua}"
    return client_ua


def _client_version() -> str:
    from . import __version__

    return __version__


def _write_stderr(lines: list[str]) -> None:
    sys.stderr.write("\n".join(lines) + "\n")
    sys.stderr.flush()


def _safe_json(value: Any) -> str:
    try:
        return json.dumps(value, ensure_ascii=False, default=str)
    except Exception:
        return str(value)


_SENSITIVE_SUBSTRINGS = (
    "authorization",
    "api-key",
    "api_key",
    "apikey",
    "api-secret",
    "api_secret",
    "secret_key",
    "secret-key",
    "access_key",
    "access-key",
    "accesskey",
    "secretkey",
    "cookie",
    "secret",
    "password",
    "passwd",
)
_SENSITIVE_SEGMENT_RE = re.compile(r"(?:^|[_-])(?:ak|sk)(?:[_-]|$)", re.IGNORECASE)
_SENSITIVE_URL_QUERY_KEYS = frozenset(
    {
        "credential",
        "ossaccesskeyid",
        "security-token",
        "signature",
        "token",
        "x-amz-credential",
        "x-amz-security-token",
        "x-amz-signature",
        "x-oss-security-token",
        "x-oss-signature",
    }
)


def _redact_headers(headers: dict, enabled: bool = True) -> dict:
    if not enabled:
        return dict(headers)
    return {
        key: _mask_sensitive_value(value) if _is_sensitive_key(str(key)) else value
        for key, value in headers.items()
    }


def _redact_sensitive_data(value: Any, enabled: bool = True) -> Any:
    if not enabled:
        return value
    if isinstance(value, dict):
        return {
            key: _redact_sensitive_field(str(key), field_value)
            for key, field_value in value.items()
        }
    if isinstance(value, list):
        return [_redact_sensitive_data(item, enabled=True) for item in value]
    if isinstance(value, str):
        return _redact_url_query_secrets(value)
    return value


def _redact_sensitive_field(key: str, value: Any) -> Any:
    if key == "request_json" and isinstance(value, str):
        return "<redacted>"
    if _is_sensitive_key(key):
        return _mask_sensitive_value(value)
    return _redact_sensitive_data(value, enabled=True)


def _is_sensitive_key(key: str) -> bool:
    lower_key = key.lower()
    if any(pattern in lower_key for pattern in _SENSITIVE_SUBSTRINGS):
        return True
    return bool(_SENSITIVE_SEGMENT_RE.search(lower_key))


def _mask_sensitive_value(value: Any) -> Any:
    if isinstance(value, str) and value:
        return _mask_middle(value)
    return value


def _mask_middle(value: str) -> str:
    if len(value) == 1:
        return "*"
    if len(value) <= 8:
        return value[:1] + "..." + value[-1:]
    if value.lower().startswith("bearer "):
        return "Bearer " + _mask_middle(value[7:])
    if len(value) <= 16:
        return value[:4] + "..." + value[-4:]
    return value[:8] + "..." + value[-4:]


def _redact_url_query_secrets(value: str) -> str:
    if "?" not in value:
        return value
    try:
        parsed = urlsplit(value)
    except ValueError:
        return value
    if not parsed.query:
        return value

    changed = False
    query = []
    for key, item_value in parse_qsl(parsed.query, keep_blank_values=True):
        if (_is_sensitive_key(key) or key.lower() in _SENSITIVE_URL_QUERY_KEYS) and item_value:
            query.append((key, _mask_middle(item_value)))
            changed = True
        else:
            query.append((key, item_value))
    if not changed:
        return value
    return urlunsplit(
        (
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            urlencode(query),
            parsed.fragment,
        )
    )


def _response_error_detail(resp: requests.Response) -> Any:
    try:
        err_data = resp.json()
    except Exception:
        return resp.text
    if isinstance(err_data, dict):
        return err_data.get("detail", err_data.get("message", resp.text))
    return err_data


def _unexpected_non_json_response_detail(resp: requests.Response) -> str:
    return "Unexpected non-JSON response from API endpoint"


def _is_retryable_exception(exc: requests.RequestException) -> bool:
    return isinstance(exc, _RETRYABLE_TRANSPORT_EXCEPTIONS)


def _is_retryable_status(status_code: int) -> bool:
    return status_code in _RETRYABLE_STATUS_CODES


def _retry_delay(attempt: int, resp: requests.Response | None = None) -> float:
    delay = _HTTP_RETRY_INITIAL_DELAY * (_HTTP_RETRY_BACKOFF_FACTOR ** max(0, attempt - 1))
    delay = min(delay, _HTTP_RETRY_MAX_DELAY)
    if resp is not None:
        retry_after = _retry_after_delay(resp)
        if retry_after is not None:
            return max(retry_after, delay)
    return delay


def _retry_after_delay(resp: requests.Response) -> float | None:
    value = resp.headers.get("Retry-After")
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, retry_at.timestamp() - time.time())


def _safe_decode(raw: bytes) -> str:
    try:
        return raw.decode("utf-8", errors="replace")
    except Exception:
        return f"<{len(raw)} bytes binary>"


def _truncate_text(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"...<truncated {len(text) - limit} chars>"


def _shorten_value(value: Any) -> Any:
    if isinstance(value, str):
        if len(value) > _VERBOSE_VALUE_PREVIEW:
            return value[:_VERBOSE_VALUE_PREVIEW] + "..."
        return value
    if isinstance(value, dict):
        return f"<dict {len(value)} keys>"
    if isinstance(value, list):
        return f"<list {len(value)} items>"
    return value


def _summarize_json_value(data: Any, limit: int) -> str:
    if isinstance(data, dict):
        keys = list(data.keys())
        sample = {k: _shorten_value(data[k]) for k in keys[:_VERBOSE_SAMPLE_KEYS]}
        summary = {"_keys": keys, "_sample": sample}
        if len(keys) > _VERBOSE_SAMPLE_KEYS:
            summary["_truncated_keys"] = len(keys) - _VERBOSE_SAMPLE_KEYS
        return _truncate_text(_safe_json(summary), limit)
    if isinstance(data, list):
        sample = [_shorten_value(item) for item in data[:_VERBOSE_SAMPLE_ITEMS]]
        summary = {"_count": len(data), "_sample": sample}
        return _truncate_text(_safe_json(summary), limit)
    return _truncate_text(_safe_json(data), limit)


def _manifest_budget_remaining(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise APIError(None, "Artifact manifest wait timed out", None, None)
    return remaining


def _deadline_timeout(
    timeout: TimeoutType, deadline: Optional[float]
) -> Union[TimeoutType, HTTPTimeout]:
    if deadline is None:
        return timeout
    remaining = _manifest_budget_remaining(deadline)

    def bounded(value):
        return min(value, remaining) if value is not None else remaining

    if isinstance(timeout, tuple):
        connect, read = (bounded(value) for value in timeout)
    else:
        connect = read = bounded(timeout)
    # The connect phase must consume the same remaining budget as the read.
    return HTTPTimeout(total=remaining, connect=connect, read=read)


def _deadline_sleep(delay: float, deadline: Optional[float]) -> None:
    if deadline is not None:
        delay = min(delay, _manifest_budget_remaining(deadline))
    time.sleep(delay)
