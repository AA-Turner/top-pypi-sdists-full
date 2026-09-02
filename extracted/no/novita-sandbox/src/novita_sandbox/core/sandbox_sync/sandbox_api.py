import datetime
import json
from typing import Any, Dict, List, Optional, cast

from packaging.version import Version
from typing_extensions import Unpack

from novita_sandbox.core.api import SandboxCreateResponse, handle_api_exception
from novita_sandbox.core.api.client.api.sandboxes import (
    delete_sandboxes_sandbox_id,
    get_sandboxes_sandbox_id,
    post_sandboxes,
    post_sandboxes_sandbox_id_connect,
    post_sandboxes_sandbox_id_pause,
    post_sandboxes_sandbox_id_snapshots,
    post_sandboxes_sandbox_id_timeout,
)
from novita_sandbox.core.api.client.api.templates import delete_templates_template_id
from novita_sandbox.core.api.client.models import (
    ConnectSandbox,
    Error,
    NewSandbox,
    PostSandboxesSandboxIDSnapshotsBody,
    PostSandboxesSandboxIDTimeoutBody,
    Sandbox,
    SandboxAutoResumeConfig,
    SandboxNetworkConfig,
    SandboxVolumeMount as SandboxVolumeMountAPI,
)
from novita_sandbox.core.api.client.types import UNSET
from novita_sandbox.core.connection_config import ApiParams, ConnectionConfig
from novita_sandbox.core.compat import raise_if_legacy, should_use_legacy
from novita_sandbox.core.exceptions import (
    SandboxException,
    SandboxNotFoundException,
    TemplateException,
)
from novita_sandbox.core.sandbox.main import SandboxBase
from novita_sandbox.core.sandbox.sandbox_api import (
    SandboxLifecycle,
    get_auto_resume_enabled,
    McpServer,
    SandboxInfo,
    SandboxMetrics,
    SandboxNetworkOpts,
    SandboxQuery,
    SnapshotInfo,
    SandboxQuota,
    SandboxQuotaLimit,
    SandboxQuotaUsage,
    SandboxEventItem,
    SandboxEventsResult,
)
from novita_sandbox.core.sandbox_sync.paginator import SandboxPaginator, get_api_client
from novita_sandbox.core.legacy_api import (
    sandbox_create_response_from_dict,
    sandbox_from_dict,
    sandbox_info_from_dict,
)
from novita_sandbox.core.secret.validation import validate_secret_envs
from novita_sandbox.core.template.types import TemplateInfo


class SandboxApi(SandboxBase):
    @staticmethod
    def list(
        query: Optional[SandboxQuery] = None,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> SandboxPaginator:
        """
        List all running sandboxes.

        :param query: Filter the list of sandboxes by metadata or state, e.g. `SandboxListQuery(metadata={"key": "value"})` or `SandboxListQuery(state=[SandboxState.RUNNING])`
        :param limit: Maximum number of sandboxes to return per page
        :param next_token: Token for pagination

        :return: List of running sandboxes
        """
        return SandboxPaginator(
            query=query,
            limit=limit,
            next_token=next_token,
            **opts,
        )

    @classmethod
    def _cls_get_info(
        cls,
        sandbox_id: str,
        **opts: Unpack[ApiParams],
    ) -> SandboxInfo:
        """
        Get the sandbox info.
        :param sandbox_id: Sandbox ID

        :return: Sandbox info
        """
        config = ConnectionConfig(**opts)

        if should_use_legacy(opts):
            api_client = get_api_client(config)
            res = api_client.get_httpx_client().get(f"/sandboxes/{sandbox_id}")
            if res.status_code == 404:
                raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")
            if res.status_code >= 300:
                raise handle_api_exception(res)
            return sandbox_info_from_dict(res.json())

        api_client = get_api_client(config)
        res = get_sandboxes_sandbox_id.sync_detailed(
            sandbox_id,
            client=api_client,
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

        if res.parsed is None:
            raise SandboxException("Body of the request is None")

        if isinstance(res.parsed, Error):
            raise SandboxException(f"{res.parsed.message}: Request failed")

        return SandboxInfo._from_sandbox_detail(res.parsed)

    @classmethod
    def _cls_kill(
        cls,
        sandbox_id: str,
        **opts: Unpack[ApiParams],
    ) -> bool:
        config = ConnectionConfig(**opts)

        if config.debug:
            # Skip killing the sandbox in debug mode
            return True

        api_client = get_api_client(config)
        res = delete_sandboxes_sandbox_id.sync_detailed(
            sandbox_id,
            client=api_client,
        )

        if res.status_code == 404:
            return False

        if res.status_code >= 300:
            raise handle_api_exception(res)

        return True

    @classmethod
    def _cls_set_timeout(
        cls,
        sandbox_id: str,
        timeout: int,
        **opts: Unpack[ApiParams],
    ) -> None:
        config = ConnectionConfig(**opts)

        if config.debug:
            # Skip setting timeout in debug mode
            return

        api_client = get_api_client(config)
        res = post_sandboxes_sandbox_id_timeout.sync_detailed(
            sandbox_id,
            client=api_client,
            body=PostSandboxesSandboxIDTimeoutBody(timeout=timeout),
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

    @classmethod
    def _cls_reset(
        cls,
        sandbox_id: str,
        resume: Optional[bool] = None,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> bool:
        config = ConnectionConfig(**opts)

        payload: Dict[str, object] = {
            "resume": True if resume is None else bool(resume),
        }
        if timeout is not None:
            payload["timeout"] = int(timeout)

        api_client = get_api_client(config)
        res = api_client.get_httpx_client().post(
            f"/sandboxes/{sandbox_id}/reset",
            json=payload,
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code == 409:
            return False

        if res.status_code >= 300:
            raise handle_api_exception(res)

        return True

    @classmethod
    def _cls_set_network(
        cls,
        sandbox_id: str,
        allow_out: Optional[List[str]] = None,
        deny_out: Optional[List[str]] = None,
        **opts: Unpack[ApiParams],
    ) -> None:
        raise_if_legacy(opts, "Sandbox.set_network")

        config = ConnectionConfig(**opts)
        body: Dict[str, Any] = {}
        if allow_out is not None:
            body["allowOut"] = allow_out
        if deny_out is not None:
            body["denyOut"] = deny_out

        api_client = get_api_client(config)
        res = api_client.get_httpx_client().put(
            f"/sandboxes/{sandbox_id}/network",
            json=body,
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

    @classmethod
    def _cls_clone_sandboxes(
        cls,
        sandbox_id: str,
        count: int = 1,
        node_id: Optional[str] = None,
        strict: bool = False,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> Dict[str, Any]:
        """
        Low-level clone API call. Returns minimal info needed to construct SDK instances.
        """
        config = ConnectionConfig(**opts)

        body: Dict[str, Any] = {
            "count": count,
            "strict": strict,
        }
        if node_id:
            body["nodeID"] = node_id
        if timeout is not None:
            body["timeout"] = timeout

        user_specified_timeout = (
            "request_timeout" in opts and opts.get("request_timeout") is not None
        )
        effective_timeout = config.request_timeout if user_specified_timeout else 300.0

        api_client = get_api_client(config)
        res = api_client.get_httpx_client().post(
            f"/sandboxes/{sandbox_id}/clone",
            json=body,
            timeout=effective_timeout,
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

        try:
            data = res.json() or {}
        except Exception as exc:
            raise SandboxException("Clone response data is invalid") from exc

        sandboxes = []
        for sb in data.get("sandboxes") or []:
            sandbox_id_full = sb.get("sandboxID")
            if config.is_legacy_domain and sb.get("clientID"):
                sandbox_id_full = f"{sandbox_id_full}-{sb.get('clientID')}"
            sandboxes.append(
                {
                    "sandbox_id": sandbox_id_full,
                    "envd_version": sb.get("envdVersion"),
                    "envd_access_token": sb.get("envdAccessToken"),
                    "traffic_access_token": sb.get("trafficAccessToken"),
                }
            )

        return {
            "sandboxes": sandboxes,
            "snapshot_template_id": data.get("snapshotTemplateId"),
        }

    @classmethod
    def _cls_hotplug_memory(
        cls,
        sandbox_id: str,
        requested_size_mib: int = 0,
        **opts: Unpack[ApiParams],
    ) -> None:
        raise_if_legacy(opts, "Sandbox.hotplug_memory")

        config = ConnectionConfig(**opts)
        api_client = get_api_client(config)
        res = api_client.get_httpx_client().post(
            f"/sandboxes/{sandbox_id}/hotplug-memory",
            json={"requested_size_mib": requested_size_mib},
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

    @classmethod
    def _cls_mount_volume(
        cls,
        sandbox_id: str,
        name: str,
        path: str,
        **opts: Unpack[ApiParams],
    ):
        raise_if_legacy(opts, "Sandbox.mount_volume")

        config = ConnectionConfig(**opts)
        api_client = get_api_client(config)
        res = api_client.get_httpx_client().post(
            f"/sandboxes/{sandbox_id}/volume-mounts",
            json={"name": name, "path": path},
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

        return res.json()

    @classmethod
    def _cls_unmount_volume(
        cls,
        sandbox_id: str,
        path: str,
        force: bool = False,
        **opts: Unpack[ApiParams],
    ):
        raise_if_legacy(opts, "Sandbox.unmount_volume")

        config = ConnectionConfig(**opts)
        api_client = get_api_client(config)
        params = {"path": path}
        if force:
            params["force"] = "true"
        res = api_client.get_httpx_client().delete(
            f"/sandboxes/{sandbox_id}/volume-mounts",
            params=params,
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

        return res.json()

    @classmethod
    def _create_sandbox(
        cls,
        template: str,
        timeout: int,
        auto_pause: Optional[bool],
        allow_internet_access: bool,
        metadata: Optional[Dict[str, str]],
        env_vars: Optional[Dict[str, str]],
        secure: bool,
        mcp: Optional[McpServer] = None,
        network: Optional[SandboxNetworkOpts] = None,
        secret_envs: Optional[Dict[str, str]] = None,
        lifecycle: Optional[SandboxLifecycle] = None,
        volume_mounts: Optional[List[SandboxVolumeMountAPI]] = None,
        node_id: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> SandboxCreateResponse:
        config = ConnectionConfig(**opts)

        if should_use_legacy(opts):
            if mcp is not None:
                raise_if_legacy(opts, "Sandbox.create mcp")
            if network is not None:
                raise_if_legacy(opts, "Sandbox.create network")
            if secret_envs:
                raise_if_legacy(opts, "Sandbox.create secret_envs")
            if volume_mounts:
                raise_if_legacy(opts, "Sandbox.create volume_mounts")

            body: Dict[str, Any] = {
                "templateID": template,
                "autoPause": bool(auto_pause),
                "metadata": metadata or {},
                "timeout": timeout,
                "envVars": env_vars or {},
                "secure": secure,
                "allowInternetAccess": allow_internet_access,
            }
            if node_id:
                body["nodeID"] = node_id

            api_client = get_api_client(config)
            res = api_client.get_httpx_client().post("/sandboxes", json=body)
            if res.status_code >= 300:
                raise handle_api_exception(res)

            data = res.json()
            if Version(data.get("envdVersion", "0")) < Version("0.1.0"):
                SandboxApi._cls_kill(data.get("sandboxID", ""), **opts)
                raise TemplateException(
                    "You need to update the template to use the new SDK. "
                    "You can do this by running `novita-sandbox-cli template build` in the directory with the template."
                )
            return sandbox_create_response_from_dict(data)

        should_auto_pause = (
            lifecycle["on_timeout"] == "pause" if lifecycle is not None else auto_pause
        )
        auto_resume_enabled = get_auto_resume_enabled(lifecycle)
        body = NewSandbox(
            template_id=template,
            auto_pause=(should_auto_pause if should_auto_pause is not None else UNSET),
            metadata=metadata or {},
            timeout=timeout,
            env_vars=env_vars or {},
            mcp=cast(Any, mcp) or UNSET,
            secure=secure,
            allow_internet_access=allow_internet_access,
            network=SandboxNetworkConfig(**network) if network else UNSET,
            volume_mounts=volume_mounts if volume_mounts else UNSET,
        )
        if auto_resume_enabled is not None:
            body.auto_resume = SandboxAutoResumeConfig(enabled=auto_resume_enabled)
        validated_secret_envs = validate_secret_envs(secret_envs, env_vars)
        if validated_secret_envs:
            body.additional_properties["secrets"] = validated_secret_envs
        if node_id:
            body.additional_properties["nodeID"] = node_id

        api_client = get_api_client(config)
        res = post_sandboxes.sync_detailed(
            body=body,
            client=api_client,
        )

        if res.status_code >= 300:
            raise handle_api_exception(res)

        if res.parsed is None:
            raise Exception("Body of the request is None")

        if isinstance(res.parsed, Error):
            raise SandboxException(f"{res.parsed.message}: Request failed")

        if Version(res.parsed.envd_version) < Version("0.1.0"):
            SandboxApi._cls_kill(res.parsed.sandbox_id)
            raise TemplateException(
                "You need to update the template to use the new SDK. "
                "You can do this by running `novita-sandbox-cli template build` in the directory with the template."
            )

        domain = res.parsed.domain if isinstance(res.parsed.domain, str) else None
        envd_token = (
            res.parsed.envd_access_token
            if isinstance(res.parsed.envd_access_token, str)
            else None
        )
        traffic_token = (
            res.parsed.traffic_access_token
            if isinstance(res.parsed.traffic_access_token, str)
            else None
        )

        return SandboxCreateResponse(
            sandbox_id=res.parsed.sandbox_id,
            sandbox_domain=domain,
            envd_version=res.parsed.envd_version,
            envd_access_token=envd_token,
            traffic_access_token=traffic_token,
        )

    @classmethod
    def _cls_get_metrics(
        cls,
        sandbox_id: str,
        start: Optional[datetime.datetime] = None,
        end: Optional[datetime.datetime] = None,
        **opts: Unpack[ApiParams],
    ) -> List[SandboxMetrics]:
        config = ConnectionConfig(**opts)

        if config.debug:
            # Skip getting the metrics in debug mode
            return []

        api_client = get_api_client(config)
        params = {}
        timestamp_multiplier = 1000 if should_use_legacy(opts) else 1
        if start:
            params["start"] = int(start.timestamp() * timestamp_multiplier)
        if end:
            params["end"] = int(end.timestamp() * timestamp_multiplier)
        res = api_client.get_httpx_client().get(
            f"/sandboxes/{sandbox_id}/metrics",
            params=params,
        )

        if res.status_code >= 300:
            raise handle_api_exception(res)

        data = res.json()
        if data is None:
            return []

        if should_use_legacy(opts):
            for metric in data:
                if "memTotalMiB" in metric:
                    mem_total_mib = metric["memTotalMiB"]
                    if isinstance(mem_total_mib, (int, float)):
                        metric["memTotal"] = mem_total_mib * 1024 * 1024
                if "memUsedMiB" in metric:
                    mem_used_mib = metric["memUsedMiB"]
                    if isinstance(mem_used_mib, (int, float)):
                        metric["memUsed"] = mem_used_mib * 1024 * 1024

        return [SandboxMetrics.from_dict(metric) for metric in data]

    @classmethod
    def _cls_connect(
        cls,
        sandbox_id: str,
        timeout: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> Sandbox:
        timeout = timeout or SandboxBase.default_sandbox_timeout

        config = ConnectionConfig(**opts)

        if should_use_legacy(opts):
            api_client = get_api_client(config)
            res = api_client.get_httpx_client().post(
                f"/sandboxes/{sandbox_id}/connect",
                json={"timeout": timeout, "autoPause": False},
            )
            if res.status_code == 404:
                raise SandboxNotFoundException(f"Paused sandbox {sandbox_id} not found")
            if res.status_code >= 300:
                raise handle_api_exception(res)
            return sandbox_from_dict(res.json())

        api_client = get_api_client(
            config,
            headers={
                "Novita-Sandbox-Id": sandbox_id,
                "Novita-Sandbox-Port": str(config.envd_port),
            },
        )
        res = post_sandboxes_sandbox_id_connect.sync_detailed(
            sandbox_id,
            client=api_client,
            body=ConnectSandbox(timeout=timeout),
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Paused sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

        if isinstance(res.parsed, Error):
            raise SandboxException(f"{res.parsed.message}: Request failed")

        if res.parsed is None:
            raise SandboxException("Body of the request is None")

        return res.parsed

    @classmethod
    def _cls_create_snapshot(
        cls,
        sandbox_id: str,
        **opts: Unpack[ApiParams],
    ) -> SnapshotInfo:
        raise_if_legacy(opts, "Sandbox.create_snapshot")

        config = ConnectionConfig(**opts)

        api_client = get_api_client(config)
        res = post_sandboxes_sandbox_id_snapshots.sync_detailed(
            sandbox_id,
            client=api_client,
            body=PostSandboxesSandboxIDSnapshotsBody(),
        )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res)

        if res.parsed is None:
            raise SandboxException("Body of the request is None")

        if isinstance(res.parsed, Error):
            raise SandboxException(f"{res.parsed.message}: Request failed")

        return SnapshotInfo(snapshot_id=res.parsed.snapshot_id)

    @classmethod
    def _cls_commit(
        cls,
        sandbox_id: str,
        alias: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ) -> TemplateInfo:
        config = ConnectionConfig(**opts)
        api_client = get_api_client(config)
        body = {"alias": alias} if alias else {}
        res = api_client.get_httpx_client().post(
            f"/sandboxes/{sandbox_id}/commit",
            json=body,
        )
        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")
        if res.status_code >= 300:
            raise handle_api_exception(res)
        return TemplateInfo.from_dict(res.json())

    @classmethod
    def _cls_delete_snapshot(
        cls,
        snapshot_id: str,
        **opts: Unpack[ApiParams],
    ) -> bool:
        config = ConnectionConfig(**opts)

        api_client = get_api_client(config)
        res = delete_templates_template_id.sync_detailed(
            snapshot_id,
            client=api_client,
        )

        if res.status_code == 404:
            return False

        if res.status_code >= 300:
            raise handle_api_exception(res)

        return True

    @classmethod
    def _cls_pause(
        cls,
        sandbox_id: str,
        sync: bool = False,
        **opts: Unpack[ApiParams],
    ) -> str:
        config = ConnectionConfig(**opts)

        api_client = get_api_client(config)
        if should_use_legacy(opts):
            res = api_client.get_httpx_client().post(
                f"/sandboxes/{sandbox_id}/pause",
                json={"sync": sync},
            )
        else:
            res = post_sandboxes_sandbox_id_pause.sync_detailed(
                sandbox_id,
                client=api_client,
            )

        if res.status_code == 404:
            raise SandboxNotFoundException(f"Sandbox {sandbox_id} not found")

        if res.status_code == 409:
            return sandbox_id

        if res.status_code >= 300:
            raise handle_api_exception(res)

        return sandbox_id

    @classmethod
    def _cls_get_quota(
        cls,
        **opts: Unpack[ApiParams],
    ) -> SandboxQuota:
        config = ConnectionConfig(**opts)
        api_client = get_api_client(config)
        res = api_client.get_httpx_client().get("/sandboxes/quota")

        if res.status_code >= 300:
            raise handle_api_exception(res)

        data = json.loads(res.content)
        limit_data = data.get("limit") or {}
        usage_data = data.get("usage") or {}
        return SandboxQuota(
            limit=SandboxQuotaLimit(
                concurrent_instances=limit_data.get("concurrentInstances", 0),
                concurrent_vcpu=limit_data.get("concurrentVcpu", 0),
                concurrent_ram_mb=limit_data.get("concurrentRamMb", 0),
                max_length_hours=limit_data.get("maxLengthHours", 0),
                disk_mb=limit_data.get("diskMb", 0),
                max_vcpu=limit_data.get("maxVcpu", 0),
                max_ram_mb=limit_data.get("maxRamMb", 0),
            ),
            usage=SandboxQuotaUsage(
                concurrent_instances=usage_data.get("concurrentInstances", 0),
                concurrent_vcpu=usage_data.get("concurrentVcpu", 0),
                concurrent_ram_mb=usage_data.get("concurrentRamMb", 0),
            ),
        )

    @classmethod
    def _cls_get_events(
        cls,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        sandbox_id: Optional[str] = None,
        template_id: Optional[str] = None,
        events: Optional[str] = None,
        state: Optional[str] = None,
        order_asc: Optional[bool] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        **opts: Unpack[ApiParams],
    ) -> SandboxEventsResult:
        config = ConnectionConfig(**opts)
        api_client = get_api_client(config)
        params: Dict[str, Any] = {}
        if start_time is not None:
            params["startTime"] = start_time
        if end_time is not None:
            params["endTime"] = end_time
        if sandbox_id is not None:
            params["sandboxID"] = sandbox_id
        if template_id is not None:
            params["templateID"] = template_id
        if events is not None:
            params["events"] = events
        if state is not None:
            params["state"] = state
        if order_asc is not None:
            params["orderAsc"] = order_asc
        if offset is not None:
            params["offset"] = offset
        if limit is not None:
            params["limit"] = limit

        res = api_client.get_httpx_client().get(
            "/sandboxes/events",
            params=params,
        )

        if res.status_code >= 300:
            raise handle_api_exception(res)

        data = json.loads(res.content)
        return SandboxEventsResult(
            items=[
                SandboxEventItem(
                    event_id=item.get("eventID", ""),
                    record_at=item.get("recordAt", 0),
                    template_id=item.get("templateID", ""),
                    template_name=item.get("templateName", ""),
                    sandbox_id=item.get("sandboxID", ""),
                    event_name=item.get("eventName", ""),
                    state=item.get("state", ""),
                    error_msg=item.get("errorMsg", ""),
                    status_code=item.get("statusCode", 0),
                )
                for item in data.get("items", [])
            ],
            total=data.get("total", 0),
            has_more=data.get("hasMore", False),
        )
