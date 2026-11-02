"""artifacts.py — AP artifact HTTP 下载兼容入口。

调用方：普通用户 / UTS SDK，透传 apikey + job_id + cluster_id。
鉴权：由 AP 产物接口负责，SDK 不再读取 Job 详情预检查。
下载委托独立 irepo-artifact 包；旧 bucket/key 工具保留但不参与下载。
"""
from __future__ import annotations

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any

from .errors import Forbidden, InstanceRepoError
from . import _site_defaults

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# 常量（业务值一律经 _site_defaults 注入，源码里不硬编码，见 _site_defaults.py）
# ---------------------------------------------------------------------------

def _artifact_bucket_map() -> dict[str, str]:
    """解析 artifact bucket 映射：环境变量 > 站点默认 > 空。

    空则抛错并引导配置——业务桶名不进公网包源码（脱敏红线）。
    """
    raw = (os.environ.get("AP_ARTIFACT_BUCKET_MAP", "")
           or _site_defaults.ARTIFACT_BUCKET_MAP_JSON).strip()
    if not raw:
        raise InstanceRepoError(
            "artifact bucket map is not configured; set AP_ARTIFACT_BUCKET_MAP "
            "(JSON {\"<cluster>\": \"<bucket>\", ...}) or use an internal build "
            "with the map injected")
    try:
        data = json.loads(raw)
    except ValueError as exc:
        raise InstanceRepoError(
            f"AP_ARTIFACT_BUCKET_MAP must be valid JSON: {exc}") from exc
    if not isinstance(data, dict) or not all(
            isinstance(k, str) and isinstance(v, str) for k, v in data.items()):
        raise InstanceRepoError(
            "AP_ARTIFACT_BUCKET_MAP must be a JSON object of string pairs")
    return data


def _artifact_prefix_root() -> str:
    root = (os.environ.get("AP_ARTIFACT_PREFIX_ROOT", "")
            or _site_defaults.ARTIFACT_PREFIX_ROOT).strip()
    if not root:
        raise InstanceRepoError(
            "artifact prefix root is not configured; set AP_ARTIFACT_PREFIX_ROOT "
            "or use an internal build with the value injected")
    return root


def _ap_endpoint(ap_endpoint: str | None) -> str:
    endpoint = (ap_endpoint
                or os.environ.get("INSTANCE_REPO_AP_ENDPOINT")
                or _site_defaults.AP_ENDPOINT).strip()
    if not endpoint:
        raise InstanceRepoError(
            "AP endpoint is not configured; set INSTANCE_REPO_AP_ENDPOINT "
            "or use an internal build with the default injected")
    return endpoint.rstrip("/")

# 批量下载默认并发数
DEFAULT_MAX_CONCURRENT = 8

# OSS 限流退避参数
OSS_RETRY_INITIAL_WAIT = 1.0   # 秒
OSS_RETRY_MAX_WAIT = 30.0      # 秒
OSS_RETRY_MAX_ATTEMPTS = 5


# ---------------------------------------------------------------------------
# 异常
# ---------------------------------------------------------------------------

class ArtifactNotFoundError(InstanceRepoError):
    """job 不存在或无 artifact。"""


class ArtifactPermissionError(Forbidden):
    """用户无权访问该 job（workspace ACL 拒绝）。"""


# ---------------------------------------------------------------------------
# 内部辅助
# ---------------------------------------------------------------------------

def resolve_artifact_bucket(cluster: str) -> str:
    """根据数据面名查 artifact bucket（映射来自注入配置，非源码硬编码）。"""
    cluster = (cluster or "").strip()
    bucket_map = _artifact_bucket_map()
    bucket = bucket_map.get(cluster)
    if not bucket:
        raise InstanceRepoError(
            f"unknown cluster {cluster!r}; known clusters: "
            f"{sorted(bucket_map)}")
    return bucket


def artifact_prefix(job_id: str) -> str:
    """构造 artifact STS 前缀：{root}/{job_id}/"""
    return f"{_artifact_prefix_root()}/{job_id}/"


def artifact_key(job_id: str) -> str:
    """构造 artifact OSS 对象 key：{root}/{job_id}/result.tgz"""
    return f"{_artifact_prefix_root()}/{job_id}/result.tgz"


def fetch_job_info(api_key: str, job_id: str, cluster: str,
                   ap_endpoint: str | None = None) -> dict[str, Any]:
    """调 AP GET /api/jobs/{job_id}?include_params=true 获取 job 信息。

    AP 内部执行 workspace ACL 检查（enforce_workspace_action_req）。
    403 → ArtifactPermissionError；404 → ArtifactNotFoundError。
    """
    endpoint = _ap_endpoint(ap_endpoint)
    url = f"{endpoint}/api/jobs/{job_id}?include_params=true"
    headers = {
        "X-API-Key": api_key,
        "Accept": "application/json",
    }
    if cluster:
        headers["X-Cluster"] = cluster

    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise ArtifactPermissionError(
                f"workspace ACL denied access to job {job_id!r}"
            ) from e
        if e.code == 404:
            raise ArtifactNotFoundError(
                f"job {job_id!r} not found"
            ) from e
        raise InstanceRepoError(
            f"AP returned HTTP {e.code} for job {job_id!r}: {e.reason}"
        ) from e
    except urllib.error.URLError as e:
        raise InstanceRepoError(
            f"failed to reach AP at {endpoint}: {e.reason}"
        ) from e


def fetch_group_job_ids(api_key: str, group_id: str, cluster: str,
                        ap_endpoint: str | None = None) -> list[str]:
    """调 AP GET /api/groups/{group_id}/jobs 分页收集全部 job_id。

    endpoint 解析与 fetch_job_info 完全一致（复用 _ap_endpoint），
    且 URL 必须带 /api 前缀：AP 网关的裸 /groups/{id}/jobs 路径返回
    控制台 HTML 页（HTTP 200），json 解析会报错（真机实测）。
    """
    endpoint = _ap_endpoint(ap_endpoint)
    job_ids: list[str] = []
    skip = 0
    limit = 500

    while True:
        url = (f"{endpoint}/api/groups/{group_id}/jobs"
               f"?skip={skip}&limit={limit}&include_post_process=false")
        headers = {
            "X-API-Key": api_key,
            "Accept": "application/json",
        }
        if cluster:
            headers["X-Cluster"] = cluster

        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 403:
                raise ArtifactPermissionError(
                    f"workspace ACL denied access to group {group_id!r}"
                ) from e
            if e.code == 404:
                raise ArtifactNotFoundError(
                    f"group {group_id!r} not found"
                ) from e
            raise InstanceRepoError(
                f"AP returned HTTP {e.code} for group {group_id!r}"
            ) from e
        except urllib.error.URLError as e:
            raise InstanceRepoError(
                f"failed to reach AP at {endpoint}: {e.reason}"
            ) from e

        jobs = data.get("jobs", [])
        if not jobs:
            break
        for j in jobs:
            jid = j.get("job_id")
            if jid:
                job_ids.append(jid)
        if len(jobs) < limit:
            break
        skip += limit

    return job_ids


def _client(api_key: str, cluster: str, ap_endpoint: str | None):
    from irepo_artifact import ArtifactClient
    return ArtifactClient(ap_endpoint=_ap_endpoint(ap_endpoint), api_key=api_key, cluster=cluster)


def _legacy_error(error):
    from irepo_artifact import AccessDenied, ArtifactNotFound, NoMatchingFiles
    if isinstance(error, AccessDenied):
        mapped = ArtifactPermissionError(str(error), cause=error)
    elif isinstance(error, (ArtifactNotFound, NoMatchingFiles)):
        mapped = ArtifactNotFoundError(str(error), cause=error)
    else:
        mapped = InstanceRepoError(f"{type(error).__name__}: {error}", cause=error)
    mapped.artifact_error = error
    mapped.error_type = type(error).__name__
    mapped.status = getattr(error, 'status', None)
    return mapped


def _result_path(result):
    return str(result.files_dir if result.files_dir is not None else result.archive_path)


def download_artifact(transport, api_key: str, job_id: str,
                      cluster: str, output_dir: str = ".",
                      ap_endpoint: str | None = None, *,
                      include_files: list[str] | None = None,
                      exclude_files: list[str] | None = None,
                      extract: bool = False) -> str:
    """Download through AP-issued HTTP links; transport retained for compatibility.

    output_dir is the Job directory. AP artifact endpoints enforce access;
    no Job precheck, STS or object-storage SDK is used.
    """
    from irepo_artifact import ArtifactError
    try:
        result = _client(api_key, cluster, ap_endpoint).download(
            job_id, output_dir, include_files=include_files,
            exclude_files=exclude_files, extract=extract, overwrite=True)
        return _result_path(result)
    except ArtifactError as exc:
        raise _legacy_error(exc) from exc


def download_artifacts(transport, api_key: str, job_ids: list[str],
                       cluster: str, output_dir: str = ".",
                       max_concurrent: int = DEFAULT_MAX_CONCURRENT,
                       ap_endpoint: str | None = None, *,
                       include_files: list[str] | None = None,
                       exclude_files: list[str] | None = None,
                       extract: bool = False) -> dict[str, str | Exception]:
    """Download into output_dir/jobs/<job_id>; retain per-Job path/error results."""
    from irepo_artifact import ArtifactError
    try:
        results = _client(api_key, cluster, ap_endpoint).download_many(
            job_ids, output_dir, max_concurrent=max_concurrent,
            include_files=include_files, exclude_files=exclude_files,
            extract=extract, overwrite=True)
    except ArtifactError as exc:
        raise _legacy_error(exc) from exc
    return {jid: (_legacy_error(result.error) if result.error is not None
                  else _result_path(result)) for jid, result in results.items()}
