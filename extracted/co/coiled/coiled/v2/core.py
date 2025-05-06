from __future__ import annotations

import asyncio
import datetime
import json
import logging
import time
import weakref
from collections import namedtuple
from typing import (
    Awaitable,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    NoReturn,
    Set,
    Tuple,
    Union,
    overload,
)

import dask.config
import dask.distributed
from aiohttp import ContentTypeError
from dask.utils import parse_timedelta
from distributed.utils import Log, Logs
from rich.progress import Progress
from typing_extensions import TypeAlias

from coiled.cli.setup.entry import do_setup_wizard
from coiled.context import track_context
from coiled.core import Async, IsAsynchronous, Sync, delete_docstring, list_docstring
from coiled.core import Cloud as OldCloud
from coiled.errors import ClusterCreationError, DoesNotExist, ServerError
from coiled.exceptions import PermissionsError
from coiled.types import (
    ArchitectureTypesEnum,
    AWSOptions,
    GCPOptions,
    PackageLevel,
    PackageSchema,
    ResolvedPackageInfo,
    SoftwareEnvironmentAlias,
)
from coiled.utils import (
    COILED_LOGGER_NAME,
    GatewaySecurity,
    get_grafana_url,
    validate_backend_options,
)

from .states import (
    InstanceStateEnum,
    ProcessStateEnum,
    flatten_log_states,
    get_process_instance_state,
    log_states,
)
from .widgets.util import simple_progress

logger = logging.getLogger(COILED_LOGGER_NAME)


def setup_logging(level=logging.INFO):
    # We want to be able to give info-level messages to users.
    # For users who haven't set up a log handler, this requires creating one (b/c the handler of "last resort,
    # logging.lastResort, has a level of "warning".
    #
    # Conservatively, we only do anything here if the user hasn't set up any log handlers on the root logger
    # or the Coiled logger. If they have any handler, we assume logging is configured how they want it.
    coiled_logger = logging.getLogger(COILED_LOGGER_NAME)
    root_logger = logging.getLogger()
    if coiled_logger.handlers == [] and root_logger.handlers == []:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(fmt="[%(asctime)s][%(levelname)-8s][%(name)s] %(message)s"))
        # Conservatively, only change the Coiled logger level there's no log level specified yet.
        if coiled_logger.level == 0:
            coiled_logger.setLevel(level)
            coiled_logger.addHandler(stream_handler)


async def handle_api_exception(response, exception_cls=ServerError) -> NoReturn:
    try:
        error_body = await response.json()
    except ContentTypeError:
        raise exception_cls(
            f"Unexpected status code ({response.status}) to {response.method}:{response.url}, contact support@coiled.io"
        ) from None
    if error_body.get("code") == PermissionsError.code:
        exception_cls = PermissionsError
    if "message" in error_body:
        raise exception_cls(error_body["message"])
    if "detail" in error_body:
        raise exception_cls(error_body["detail"])
    raise exception_cls(error_body)


CloudV2SyncAsync: TypeAlias = Union["CloudV2[Async]", "CloudV2[Sync]"]


class CloudV2(OldCloud, Generic[IsAsynchronous]):
    _recent_sync: List[weakref.ReferenceType[CloudV2[Sync]]] = list()
    _recent_async: List[weakref.ReferenceType[CloudV2[Async]]] = list()

    # just overriding to get the right signature (CloudV2, not Cloud)
    def __enter__(self: CloudV2[Sync]) -> CloudV2[Sync]:
        return self

    def __exit__(self: CloudV2[Sync], typ, value, tb) -> None:
        self.close()

    async def __aenter__(self: CloudV2[Async]) -> CloudV2[Async]:
        return await self._start()

    async def __aexit__(self: CloudV2[Async], typ, value, tb) -> None:
        await self._close()

    # these overloads are necessary for the typechecker to know that we really have a CloudV2, not a Cloud
    # without them, CloudV2.current would be typed to return a Cloud
    #
    # https://www.python.org/dev/peps/pep-0673/ would remove the need for this.
    # That PEP also mentions a workaround with type vars, which doesn't work for us because type vars aren't
    # subscribtable
    @overload
    @classmethod
    def current(cls, asynchronous: Sync) -> CloudV2[Sync]: ...

    @overload
    @classmethod
    def current(cls, asynchronous: Async) -> CloudV2[Async]: ...

    @overload
    @classmethod
    def current(cls, asynchronous: bool) -> CloudV2: ...

    @classmethod
    def current(cls, asynchronous: bool) -> CloudV2:
        recent: List[weakref.ReferenceType[CloudV2]]
        if asynchronous:
            recent = cls._recent_async
        else:
            recent = cls._recent_sync
        try:
            cloud = recent[-1]()
            while cloud is None or cloud.status != "running":
                recent.pop()
                cloud = recent[-1]()
        except IndexError:
            if asynchronous:
                return cls(asynchronous=True)
            else:
                return cls(asynchronous=False)
        else:
            return cloud

    @track_context
    async def _get_default_instance_types(self, provider: str, gpu: bool = False, arch: str = "x86_64") -> List[str]:
        if arch not in ("arm64", "x86_64"):
            raise ValueError(f"arch '{arch}' is not supported for default instance types")
        if provider == "aws":
            if arch == "arm64":
                if gpu:
                    return ["g5g.xlarge"]  # has NVIDIA T4G
                else:
                    return ["m7g.xlarge", "m6g.xlarge"]
            if gpu:
                return ["g4dn.xlarge"]
            else:
                return ["m6i.xlarge", "m5.xlarge"]
        elif provider == "gcp":
            if arch != "x86_64":
                return ["t2a-standard-4"]
            if gpu:
                # n1-standard-8 with 30GB of memory might be best, but that's big for a default
                return ["n1-standard-4"]
            else:
                return ["e2-standard-4"]
        elif provider == "azure":
            if arch != "x86_64":
                raise ValueError(f"no default instance type for Azure with {arch} architecture")
            if gpu:
                raise ValueError("no default GPU instance type for Azure")
            return ["Standard_D4_v5"]
        else:
            raise ValueError(f"unexpected provider {provider}; cannot determine default instance types")

    async def _list_dask_scheduler_page(
        self,
        page: int,
        workspace: str | None = None,
        since: str | None = "7 days",
        user: str | None = None,
    ) -> Tuple[list, bool]:
        page_size = 100
        workspace = workspace or self.default_workspace
        kwargs = {}
        if since:
            kwargs["since"] = parse_timedelta(since)
        if user:
            kwargs["user"] = user
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/analytics/{workspace}/clusters/list",
            params={
                "limit": page_size,
                "offset": page_size * page,
                **kwargs,
            },
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @track_context
    async def _list_dask_scheduler(
        self,
        workspace: str | None = None,
        since: str | None = "7 days",
        user: str | None = None,
    ):
        return await self._depaginate_list(
            self._list_dask_scheduler_page,
            workspace=workspace,
            since=since,
            user=user,
        )

    @overload
    def list_dask_scheduler(
        self: Cloud[Sync],
        account: str | None = None,
        workspace: str | None = None,
        since: str | None = "7 days",
        user: str | None = None,
    ) -> list: ...

    @overload
    def list_dask_scheduler(
        self: Cloud[Async],
        account: str | None = None,
        workspace: str | None = None,
        since: str | None = "7 days",
        user: str | None = "",
    ) -> Awaitable[list]: ...

    def list_dask_scheduler(
        self,
        account: str | None = None,
        workspace: str | None = None,
        since: str | None = "7 days",
        user: str | None = "",
    ) -> Union[list, Awaitable[list]]:
        return self._sync(self._list_dask_scheduler, workspace or account, since=since, user=user)

    async def _list_computations(
        self, cluster_id: int | None = None, scheduler_id: int | None = None, workspace: str | None = None
    ):
        return await self._depaginate_list(
            self._list_computations_page, cluster_id=cluster_id, scheduler_id=scheduler_id, workspace=workspace
        )

    async def _list_computations_page(
        self,
        page: int,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        workspace: str | None = None,
    ) -> Tuple[list, bool]:
        page_size = 100
        workspace = workspace or self.default_workspace

        if not scheduler_id and not cluster_id:
            raise ValueError("either cluster_id or scheduler_id must be specified")

        api = (
            f"/api/v2/analytics/{workspace}/{scheduler_id}/computations/list"
            if scheduler_id
            else f"/api/v2/analytics/{workspace}/cluster/{cluster_id}/computations/list"
        )

        response = await self._do_request(
            "GET",
            self.server + api,
            params={"limit": page_size, "offset": page_size * page},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @overload
    def list_computations(
        self: Cloud[Sync],
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        workspace: str | None = None,
    ) -> list: ...

    @overload
    def list_computations(
        self: Cloud[Async],
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        workspace: str | None = None,
    ) -> Awaitable[list]: ...

    def list_computations(
        self,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        workspace: str | None = None,
    ) -> Union[list, Awaitable[list]]:
        return self._sync(
            self._list_computations, cluster_id=cluster_id, scheduler_id=scheduler_id, workspace=workspace or account
        )

    def list_exceptions(
        self,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        account: str | None = None,
        workspace: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ) -> Union[list, Awaitable[list]]:
        return self._sync(
            self._list_exceptions,
            cluster_id=cluster_id,
            scheduler_id=scheduler_id,
            workspace=workspace or account,
            since=since,
            user=user,
        )

    async def _list_exceptions(
        self,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        workspace: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ):
        return await self._depaginate_list(
            self._list_exceptions_page,
            cluster_id=cluster_id,
            scheduler_id=scheduler_id,
            workspace=workspace,
            since=since,
            user=user,
        )

    async def _list_exceptions_page(
        self,
        page: int,
        cluster_id: int | None = None,
        scheduler_id: int | None = None,
        workspace: str | None = None,
        since: str | None = None,
        user: str | None = None,
    ) -> Tuple[list, bool]:
        page_size = 100
        workspace = workspace or self.default_workspace
        kwargs = {}
        if since:
            kwargs["since"] = parse_timedelta(since)
        if user:
            kwargs["user"] = user
        if cluster_id:
            kwargs["cluster"] = cluster_id
        if scheduler_id:
            kwargs["scheduler"] = scheduler_id
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/analytics/{workspace}/exceptions/list",
            params={"limit": page_size, "offset": page_size * page, **kwargs},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    async def _list_events_page(
        self,
        page: int,
        cluster_id: int,
        workspace: str | None = None,
    ) -> Tuple[list, bool]:
        page_size = 100
        workspace = workspace or self.default_workspace
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/analytics/{workspace}/{cluster_id}/events/list",
            params={"limit": page_size, "offset": page_size * page},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    async def _list_events(self, cluster_id: int, workspace: str | None = None):
        return await self._depaginate_list(self._list_events_page, cluster_id=cluster_id, workspace=workspace)

    def list_events(
        self,
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
    ) -> Union[list, Awaitable[list]]:
        return self._sync(self._list_events, cluster_id, workspace or account)

    async def _send_state(self, cluster_id: int, desired_status: str, workspace: str | None = None):
        workspace = workspace or self.default_workspace
        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/analytics/{workspace}/{cluster_id}/desired-state",
            json={"desired_status": desired_status},
        )
        if response.status >= 400:
            await handle_api_exception(response)

    def send_state(
        self,
        cluster_id: int,
        desired_status: str,
        account: str | None = None,
        workspace: str | None = None,
    ) -> Union[None, Awaitable[None]]:
        return self._sync(self._send_state, cluster_id, desired_status, workspace or account)

    @track_context
    async def _list_clusters(self, workspace: str | None = None, max_pages: int | None = None, just_mine: bool = False):
        return await self._depaginate_list(
            self._list_clusters_page, workspace=workspace, max_pages=max_pages, just_mine=just_mine
        )

    @overload
    def list_clusters(
        self: Cloud[Sync],
        account: str | None = None,
        workspace: str | None = None,
        max_pages: int | None = None,
        just_mine: bool = False,
    ) -> list: ...

    @overload
    def list_clusters(
        self: Cloud[Async],
        account: str | None = None,
        workspace: str | None = None,
        max_pages: int | None = None,
        just_mine: bool = False,
    ) -> Awaitable[list]: ...

    @list_docstring
    def list_clusters(
        self,
        account: str | None = None,
        workspace: str | None = None,
        max_pages: int | None = None,
        just_mine: bool = False,
    ) -> Union[list, Awaitable[list]]:
        return self._sync(self._list_clusters, workspace=workspace or account, max_pages=max_pages, just_mine=just_mine)

    async def _list_clusters_page(
        self, page: int, workspace: str | None = None, just_mine: bool = False
    ) -> Tuple[list, bool]:
        page_size = 100
        workspace = workspace or self.default_workspace
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{workspace}/",
            params={"limit": page_size, "offset": page_size * page, "just_mine": "1" if just_mine else "0"},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @staticmethod
    async def _depaginate_list(
        func: Callable[..., Awaitable[Tuple[list, bool]]],
        max_pages: int | None = None,
        *args,
        **kwargs,
    ) -> list:
        results_all = []
        page = 0
        while True:
            kwargs["page"] = page
            results, next = await func(*args, **kwargs)
            results_all += results
            page += 1
            if (not results) or next is None:
                break
            # page is the number of pages we've already fetched (since 0-indexed)
            if max_pages and page >= max_pages:
                break
        return results_all

    @track_context
    async def _create_package_sync_env(
        self,
        packages: List[ResolvedPackageInfo],
        progress: Progress | None = None,
        workspace: str | None = None,
        gpu_enabled: bool = False,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        region_name: str | None = None,
        use_uv_installer: bool = True,
    ) -> SoftwareEnvironmentAlias:
        workspace = workspace or self.default_workspace
        prepared_packages: List[PackageSchema] = []
        for pkg in packages:
            if pkg["sdist"] and pkg["md5"]:
                with simple_progress(f"Uploading {pkg['name']}", progress=progress):
                    file_id = await self._create_senv_package(
                        pkg["sdist"],
                        contents_md5=pkg["md5"],
                        workspace=workspace,
                        region_name=region_name,
                    )
            else:
                file_id = None
            prepared_packages.append({
                "name": pkg["name"],
                "source": pkg["source"],
                "channel": pkg["channel"],
                "conda_name": pkg["conda_name"],
                "specifier": pkg["specifier"],
                "include": pkg["include"],
                "client_version": pkg["client_version"],
                "file": file_id,
            })
        with simple_progress("Requesting package sync build", progress=progress):
            result = await self._create_software_environment_v2(
                senv={
                    "packages": prepared_packages,
                    "raw_pip": None,
                    "raw_conda": None,
                },
                workspace=workspace,
                architecture=architecture,
                gpu_enabled=gpu_enabled,
                region_name=region_name,
                use_uv_installer=use_uv_installer,
            )
        return result

    @track_context
    async def _create_custom_certificate(self, subdomain: str, workspace: str | None = None):
        workspace = workspace or self.default_workspace
        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/clusters/account/{workspace}/https-certificate",
            json={"subdomain": subdomain},
        )
        if response.status >= 400:
            await handle_api_exception(response)

    async def _check_custom_certificate(self, subdomain: str, workspace: str | None = None):
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{workspace}/https-certificate/{subdomain}",
        )
        if response.status >= 400:
            await handle_api_exception(response)
        response_json = await response.json()
        cert_status = response_json.get("status")
        return cert_status

    @track_context
    async def _create_cluster(
        self,
        # todo: make name optional and pick one for them, like pre-declarative?
        # https://gitlab.com/coiled/cloud/-/issues/4305
        name: str,
        *,
        software_environment: str | None = None,
        senv_v2_id: int | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        workspace: str | None = None,
        workers: int = 0,
        environ: Dict | None = None,
        tags: Dict | None = None,
        dask_config: Dict | None = None,
        scheduler_vm_types: list | None = None,
        gcp_worker_gpu_type: str | None = None,
        gcp_worker_gpu_count: int | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: Union[AWSOptions, GCPOptions, dict] | None = None,
        use_scheduler_public_ip: bool | None = None,
        use_dashboard_https: bool | None = None,
        private_to_creator: bool | None = None,
        extra_worker_on_scheduler: bool | None = None,
        n_worker_specs_per_host: int | None = None,
        custom_subdomain: str | None = None,
        batch_job_ids: List[int] | None = None,
        extra_user_container: str | None = None,
        extra_user_container_ignore_entrypoint: bool | None = None,
        host_setup_script_content: str | None = None,
        pause_on_exit: bool | None = None,
    ) -> Tuple[int, bool]:
        # TODO (Declarative): support these args, or decide not to
        # https://gitlab.com/coiled/cloud/-/issues/4305

        workspace = workspace or self.default_workspace
        account, name = self._normalize_name(name, context_workspace=workspace, allow_uppercase=True)

        await self._verify_workspace(account)

        data = {
            "name": name,
            "workers": workers,
            "worker_instance_types": worker_vm_types,
            "scheduler_instance_types": scheduler_vm_types,
            "worker_options": worker_options,
            "worker_class": worker_class,
            "worker_disk_size": worker_disk_size,
            "worker_disk_throughput": worker_disk_throughput,
            "scheduler_disk_size": scheduler_disk_size,
            "scheduler_options": scheduler_options,
            "environ": environ,
            "tags": tags,
            "dask_config": dask_config,
            "private_to_creator": private_to_creator,
            "env_id": senv_v2_id,
            "env_name": software_environment,
            "extra_worker_on_scheduler": extra_worker_on_scheduler,
            "n_worker_specs_per_host": n_worker_specs_per_host,
            "use_aws_creds_endpoint": dask.config.get("coiled.use_aws_creds_endpoint", False),
            "custom_subdomain": custom_subdomain,
            "batch_job_ids": batch_job_ids,
            "extra_user_container": extra_user_container,
            "extra_user_container_ignore_entrypoint": extra_user_container_ignore_entrypoint,
            "host_setup_script": host_setup_script_content,
            "pause_on_exit": pause_on_exit,
        }

        backend_options = backend_options if backend_options else {}

        if gcp_worker_gpu_type is not None:
            # for backwards compatibility with v1 options
            backend_options = {
                **backend_options,
                "worker_accelerator_count": gcp_worker_gpu_count or 1,
                "worker_accelerator_type": gcp_worker_gpu_type,
            }
        elif gcp_worker_gpu_count:
            # not ideal but v1 only supported T4 and `worker_gpu=1` would give you one
            backend_options = {
                **backend_options,
                "worker_accelerator_count": gcp_worker_gpu_count,
                "worker_accelerator_type": "nvidia-tesla-t4",
            }

        if use_scheduler_public_ip is False:
            if "use_dashboard_public_ip" not in backend_options and not use_dashboard_https:
                backend_options["use_dashboard_public_ip"] = False

        if use_dashboard_https is False:
            if "use_dashboard_https" not in backend_options:
                backend_options["use_dashboard_https"] = False

        if backend_options:
            # for backwards compatibility with v1 options
            if "region" in backend_options and "region_name" not in backend_options:
                backend_options["region_name"] = backend_options["region"]  # type: ignore
                del backend_options["region"]  # type: ignore
            if "zone" in backend_options and "zone_name" not in backend_options:
                backend_options["zone_name"] = backend_options["zone"]  # type: ignore
                del backend_options["zone"]  # type: ignore
            # firewall just lets you specify a single CIDR block to open for ingress
            # we want to support a list of ingress CIDR blocks
            if "firewall" in backend_options:
                backend_options["ingress"] = [backend_options.pop("firewall")]  # type: ignore

            # convert the list of ingress rules to the FirewallSpec expected server-side
            if "ingress" in backend_options:
                fw_spec = {"ingress": backend_options.pop("ingress")}
                backend_options["firewall_spec"] = fw_spec  # type: ignore

            validate_backend_options(backend_options)
            data["options"] = backend_options

        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/clusters/account/{account}/",
            json=data,
        )

        response_json = await response.json()

        if response.status >= 400:
            from .widgets import EXECUTION_CONTEXT

            if response_json.get("code") == "NO_CLOUD_SETUP":
                server_error_message = response_json.get("message")
                error_message = f"{server_error_message} or by running `coiled setup`"

                if EXECUTION_CONTEXT == "terminal":
                    # maybe not interactive so just raise
                    raise ClusterCreationError(error_message)
                else:
                    # interactive session so let's try running the cloud setup wizard
                    if await do_setup_wizard():
                        # the user setup their cloud backend, so let's try creating cluster again!
                        response = await self._do_request(
                            "POST",
                            self.server + f"/api/v2/clusters/account/{account}/",
                            json=data,
                        )
                        if response.status >= 400:
                            await handle_api_exception(response)  # always raises exception, no return
                        response_json = await response.json()
                    else:
                        raise ClusterCreationError(error_message)
            else:
                error_class = PermissionsError if response_json.get("code") == PermissionsError.code else ServerError
                if "message" in response_json:
                    raise error_class(response_json["message"])
                if "detail" in response_json:
                    raise error_class(response_json["detail"])
                raise error_class(response_json)

        return response_json["id"], response_json["existing"]

    @overload
    def create_cluster(
        self: Cloud[Sync],
        name: str,
        *,
        software: str | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        account: str | None = None,
        workspace: str | None = None,
        workers: int = 0,
        environ: Dict | None = None,
        tags: Dict | None = None,
        dask_config: Dict | None = None,
        private_to_creator: bool | None = None,
        scheduler_vm_types: list | None = None,
        worker_gpu_type: str | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: Union[dict, AWSOptions, GCPOptions] | None = None,
    ) -> Tuple[int, bool]: ...

    @overload
    def create_cluster(
        self: Cloud[Async],
        name: str,
        *,
        software: str | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        account: str | None = None,
        workspace: str | None = None,
        workers: int = 0,
        environ: Dict | None = None,
        tags: Dict | None = None,
        dask_config: Dict | None = None,
        private_to_creator: bool | None = None,
        scheduler_vm_types: list | None = None,
        worker_gpu_type: str | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: Union[dict, AWSOptions, GCPOptions] | None = None,
    ) -> Awaitable[Tuple[int, bool]]: ...

    def create_cluster(
        self,
        name: str,
        *,
        software: str | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        scheduler_options: dict | None = None,
        account: str | None = None,
        workspace: str | None = None,
        workers: int = 0,
        environ: Dict | None = None,
        tags: Dict | None = None,
        private_to_creator: bool | None = None,
        dask_config: Dict | None = None,
        scheduler_vm_types: list | None = None,
        worker_gpu_type: str | None = None,
        worker_vm_types: list | None = None,
        worker_disk_size: int | None = None,
        worker_disk_throughput: int | None = None,
        scheduler_disk_size: int | None = None,
        backend_options: Union[dict, AWSOptions, GCPOptions] | None = None,
    ) -> Union[Tuple[int, bool], Awaitable[Tuple[int, bool]]]:
        return self._sync(
            self._create_cluster,
            name=name,
            software_environment=software,
            worker_class=worker_class,
            worker_options=worker_options,
            scheduler_options=scheduler_options,
            workspace=workspace or account,
            workers=workers,
            environ=environ,
            tags=tags,
            dask_config=dask_config,
            private_to_creator=private_to_creator,
            scheduler_vm_types=scheduler_vm_types,
            worker_vm_types=worker_vm_types,
            gcp_worker_gpu_type=worker_gpu_type,
            worker_disk_size=worker_disk_size,
            worker_disk_throughput=worker_disk_throughput,
            scheduler_disk_size=scheduler_disk_size,
            backend_options=backend_options,
        )

    @track_context
    async def _delete_cluster(
        self, cluster_id: int, workspace: str | None = None, reason: str | None = None, pause: bool = False
    ) -> None:
        workspace = workspace or self.default_workspace

        route = f"/api/v2/clusters/account/{workspace}/id/{cluster_id}"
        params = {}
        if reason:
            params["reason"] = reason[:6000]  # reason is sometimes long, we need to keep URL length under 8192 bytes
        if pause:
            params["pause"] = 1
        if not params:
            params = None
        response = await self._do_request_idempotent(
            "DELETE",
            self.server + route,
            params=params,
        )
        if response.status >= 400:
            await handle_api_exception(response)
        else:
            # multiple deletes sometimes fail if we don't await response here
            await response.json()
            logger.info(f"Cluster {cluster_id} deleted successfully.")

    @overload
    def delete_cluster(
        self: Cloud[Sync],
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        reason: str | None = None,
        pause: bool = False,
    ) -> None: ...

    @overload
    def delete_cluster(
        self: Cloud[Async],
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        reason: str | None = None,
        pause: bool = False,
    ) -> Awaitable[None]: ...

    @delete_docstring  # TODO: this docstring erroneously says "Name of cluster" when it really accepts an ID
    def delete_cluster(
        self,
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        reason: str | None = None,
        pause: bool = False,
    ) -> Awaitable[None] | None:
        return self._sync(
            self._delete_cluster, cluster_id=cluster_id, workspace=workspace or account, reason=reason, pause=pause
        )

    async def _get_cluster_state(self, cluster_id: int, workspace: str | None = None) -> dict:
        workspace = workspace or self.default_workspace
        # Make request directly instead of using `_do_request` because we don't want any retries.
        # Retry logic doesn't make sense because this is called by (frequent) period callback, so we'll just wait
        # for next periodic callback call, otherwise retries will overlap with the periodic callback and build up.
        session = self._ensure_session()
        response = await session.request(
            "GET", self.server + f"/api/v2/clusters/account/{workspace}/id/{cluster_id}/state"
        )
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    async def _get_cluster_details(self, cluster_id: int, workspace: str | None = None):
        workspace = workspace or self.default_workspace
        r = await self._do_request_idempotent(
            "GET", self.server + f"/api/v2/clusters/account/{workspace}/id/{cluster_id}"
        )
        if r.status >= 400:
            await handle_api_exception(r)
        return await r.json()

    def _get_cluster_details_synced(self, cluster_id: int, workspace: str | None = None):
        return self._sync(
            self._get_cluster_details,
            cluster_id=cluster_id,
            workspace=workspace,
        )

    def _cluster_grafana_url(self, cluster_id: int, workspace: str | None = None):
        """for internal Coiled use"""
        workspace = workspace or self.default_workspace
        details = self._sync(
            self._get_cluster_details,
            cluster_id=cluster_id,
            workspace=workspace,
        )

        return get_grafana_url(details, account=workspace, cluster_id=cluster_id)

    def cluster_details(self, cluster_id: int, account: str | None = None, workspace: str | None = None):
        details = self._sync(
            self._get_cluster_details,
            cluster_id=cluster_id,
            workspace=workspace or account,
        )
        state_keys = ["state", "reason", "updated"]

        def get_state(state: dict):
            return {k: v for k, v in state.items() if k in state_keys}

        def get_instance(instance):
            if instance is None:
                return None
            else:
                return {
                    "id": instance["id"],
                    "created": instance["created"],
                    "name": instance["name"],
                    "public_ip_address": instance["public_ip_address"],
                    "private_ip_address": instance["private_ip_address"],
                    "current_state": get_state(instance["current_state"]),
                }

        def get_process(process: dict):
            if process is None:
                return None
            else:
                return {
                    "created": process["created"],
                    "name": process["name"],
                    "current_state": get_state(process["current_state"]),
                    "instance": get_instance(process["instance"]),
                }

        return {
            "id": details["id"],
            "name": details["name"],
            "workers": [get_process(w) for w in details["workers"]],
            "scheduler": get_process(details["scheduler"]),
            "current_state": get_state(details["current_state"]),
            "created": details["created"],
        }

    async def _get_workers_page(self, cluster_id: int, page: int, workspace: str | None = None) -> Tuple[list, bool]:
        page_size = 100
        workspace = workspace or self.default_workspace

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/workers/account/{workspace}/cluster/{cluster_id}/",
            params={"limit": page_size, "offset": page_size * page},
        )
        if response.status >= 400:
            await handle_api_exception(response)

        results = await response.json()
        has_more_pages = len(results) > 0
        return results, has_more_pages

    @track_context
    async def _get_worker_names(
        self,
        workspace: str,
        cluster_id: int,
        statuses: List[ProcessStateEnum] | None = None,
    ) -> Set[str]:
        worker_infos = await self._depaginate_list(self._get_workers_page, cluster_id=cluster_id, workspace=workspace)
        logger.debug(f"workers: {worker_infos}")
        return {w["name"] for w in worker_infos if statuses is None or w["current_state"]["state"] in statuses}

    @track_context
    async def _security(self, cluster_id: int, workspace: str | None = None, client_wants_public_ip: bool = True):
        cluster_info = await self._get_cluster_details(cluster_id=cluster_id, workspace=workspace)
        if ProcessStateEnum(cluster_info["scheduler"]["current_state"]["state"]) != ProcessStateEnum.started:
            scheduler_state = cluster_info["scheduler"]["current_state"]["state"]
            raise RuntimeError(
                f"Cannot get security info for cluster {cluster_id}, scheduler state is {scheduler_state}"
            )

        public_ip = cluster_info["scheduler"]["instance"]["public_ip_address"]
        private_ip = cluster_info["scheduler"]["instance"]["private_ip_address"]
        tls_cert = cluster_info["cluster_options"]["tls_cert"]
        tls_key = cluster_info["cluster_options"]["tls_key"]
        scheduler_port = cluster_info["scheduler_port"]
        dashboard_address = cluster_info["scheduler"]["dashboard_address"]
        give_scheduler_public_ip = cluster_info["cluster_infra"]["give_scheduler_public_ip"]

        private_address = f"tls://{private_ip}:{scheduler_port}"
        public_address = f"tls://{public_ip}:{scheduler_port}"

        use_public_address = give_scheduler_public_ip and client_wants_public_ip
        if use_public_address:
            if not public_ip:
                raise RuntimeError(
                    "Your Coiled client is configured to use the public IP address, but the scheduler VM does not "
                    "have a public IP address.\n\n"
                    "If you're expecting to connect on private IP address, you can run\n"
                    "    coiled config set coiled.use_scheduler_public_ip False\n"
                    "to configure your local Client to use the private IP address, "
                    "or contact support@coiled.io if you'd like help."
                )
            address_to_use = public_address
        else:
            address_to_use = private_address
            logger.info(f"Connecting to scheduler on its internal address: {address_to_use}")

        # TODO (Declarative): pass extra_conn_args if we care about proxying through Coiled to the scheduler
        security = GatewaySecurity(tls_key, tls_cert)

        return security, {
            "address_to_use": address_to_use,
            "private_address": private_address,
            "public_address": public_address,
            "dashboard_address": dashboard_address,
        }

    @track_context
    async def _requested_workers(self, cluster_id: int, account: str | None = None) -> Set[str]:
        raise NotImplementedError("TODO")

    @overload
    def requested_workers(self: Cloud[Sync], cluster_id: int, account: str | None = None) -> Set[str]: ...

    @track_context
    async def _get_cluster_by_name(self, name: str, workspace: str | None = None, include_paused: bool = False) -> int:
        workspace, name = self._normalize_name(
            name, context_workspace=workspace, allow_uppercase=True, property_name="cluster name"
        )

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{workspace}/name/{name}",
            params={"include_paused": int(include_paused)},
        )
        if response.status == 404:
            raise DoesNotExist
        elif response.status >= 400:
            await handle_api_exception(response)

        cluster = await response.json()
        return cluster["id"]

    @overload
    def get_cluster_by_name(
        self: Cloud[Sync],
        name: str,
        account: str | None = None,
        workspace: str | None = None,
        include_paused: bool = False,
    ) -> int: ...

    @overload
    def get_cluster_by_name(
        self: Cloud[Async],
        name: str,
        account: str | None = None,
        workspace: str | None = None,
        include_paused: bool = False,
    ) -> Awaitable[int]: ...

    def get_cluster_by_name(
        self,
        name: str,
        account: str | None = None,
        workspace: str | None = None,
        include_paused: bool = False,
    ) -> Union[int, Awaitable[int]]:
        return self._sync(
            self._get_cluster_by_name,
            name=name,
            workspace=workspace or account,
            include_paused=include_paused,
        )

    @track_context
    async def _cluster_status(
        self,
        cluster_id: int,
        account: str | None = None,
        exclude_stopped: bool = True,
    ) -> dict:
        raise NotImplementedError("TODO?")

    @track_context
    async def _get_cluster_states_declarative(
        self,
        cluster_id: int,
        workspace: str | None = None,
        start_time: datetime.datetime | None = None,
    ) -> dict:
        workspace = workspace or self.default_workspace

        params = {"start_time": start_time.isoformat()} if start_time is not None else {}

        response = await self._do_request_idempotent(
            "GET",
            self.server + f"/api/v2/clusters/account/{workspace}/id/{cluster_id}/states",
            params=params,
        )

        # if we get 403 on this endpoint, most likely it's temporary,
        # unless we've never gotten 403 or it's been too long since we got a good response from the endpoint
        if (
            response.status == 403
            and time.monotonic() - getattr(self, "_get_cluster_states_declarative_last_good_response", 0) < 60
        ):
            return {}
        elif response.status >= 400:
            await handle_api_exception(response)

        self._get_cluster_states_declarative_last_good_response = time.monotonic()

        return await response.json()

    def get_cluster_states(
        self,
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        start_time: datetime.datetime | None = None,
    ) -> Union[dict, Awaitable[dict]]:
        return self._sync(
            self._get_cluster_states_declarative,
            cluster_id=cluster_id,
            workspace=workspace or account,
            start_time=start_time,
        )

    def get_clusters_by_name(
        self,
        name: str,
        account: str | None = None,
        workspace: str | None = None,
    ) -> List[dict]:
        """Get all clusters matching name."""
        return self._sync(
            self._get_clusters_by_name,
            name=name,
            workspace=workspace or account,
        )

    @track_context
    async def _get_clusters_by_name(self, name: str, workspace: str | None = None) -> List[dict]:
        workspace, name = self._normalize_name(name, context_workspace=workspace, allow_uppercase=True)

        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/clusters/account/{workspace}/",
            params={"name": name},
        )
        if response.status == 404:
            raise DoesNotExist
        elif response.status >= 400:
            await handle_api_exception(response)

        cluster = await response.json()
        return cluster

    @overload
    def cluster_logs(
        self: Cloud[Sync],
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Logs: ...

    @overload
    def cluster_logs(
        self: Cloud[Async],
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Awaitable[Logs]: ...

    @track_context
    async def _cluster_logs(
        self,
        cluster_id: int,
        workspace: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Logs:
        def is_errored(process):
            process_state, instance_state = get_process_instance_state(process)
            return process_state == ProcessStateEnum.error or instance_state == InstanceStateEnum.error

        workspace = workspace or self.default_workspace

        # hits endpoint in order to get scheduler and worker instance names
        cluster_info = await self._get_cluster_details(cluster_id=cluster_id, workspace=workspace)

        try:
            scheduler_name = cluster_info["scheduler"]["instance"]["name"]
        except (TypeError, KeyError):
            # no scheduler instance name in cluster info
            logger.warning("No scheduler found when attempting to retrieve cluster logs.")
            scheduler_name = None

        worker_names = [
            worker["instance"]["name"]
            for worker in cluster_info["workers"]
            if worker["instance"] and (not errors_only or is_errored(worker))
        ]

        LabeledInstance = namedtuple("LabeledInstance", ("name", "label"))

        instances = []
        if scheduler and scheduler_name and (not errors_only or is_errored(cluster_info["scheduler"])):
            instances.append(LabeledInstance(scheduler_name, "Scheduler"))
        if workers and worker_names:
            instances.extend([LabeledInstance(worker_name, worker_name) for worker_name in worker_names])

        async def instance_log_with_semaphor(semaphor, **kwargs):
            async with semaphor:
                return await self._instance_logs(**kwargs)

        # only get 100 logs at a time; the limit here is redundant since aiohttp session already limits concurrent
        # connections but let's be safe just in case
        semaphor = asyncio.Semaphore(value=100)
        results = await asyncio.gather(*[
            instance_log_with_semaphor(semaphor=semaphor, workspace=workspace, instance_name=inst.name)
            for inst in instances
        ])

        out = {
            instance_label: instance_log
            for (_, instance_label), instance_log in zip(instances, results)
            if len(instance_log)
        }

        return Logs(out)

    def cluster_logs(
        self,
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        scheduler: bool = True,
        workers: bool = True,
        errors_only: bool = False,
    ) -> Union[Logs, Awaitable[Logs]]:
        return self._sync(
            self._cluster_logs,
            cluster_id=cluster_id,
            workspace=workspace or account,
            scheduler=scheduler,
            workers=workers,
            errors_only=errors_only,
        )

    async def _instance_logs(self, workspace: str, instance_name: str, safe=True) -> Log:
        response = await self._do_request(
            "GET",
            self.server + "/api/v2/instances/{}/instance/{}/logs".format(workspace, instance_name),
        )
        if response.status >= 400:
            if safe:
                logger.warning(f"Error retrieving logs for {instance_name}")
                return Log()
            await handle_api_exception(response)

        data = await response.json()

        messages = "\n".join(logline.get("message", "") for logline in data)

        return Log(messages)

    @overload
    def requested_workers(
        self: Cloud[Async], cluster_id: int, account: str | None = None, workspace: str | None = None
    ) -> Awaitable[Set[str]]: ...

    def requested_workers(
        self, cluster_id: int, account: str | None = None, workspace: str | None = None
    ) -> Union[
        Set[str],
        Awaitable[Set[str]],
    ]:
        return self._sync(self._requested_workers, cluster_id, workspace or account)

    @overload
    def scale_up(
        self: Cloud[Sync], cluster_id: int, n: int, account: str | None = None, workspace: str | None = None
    ) -> Dict | None: ...

    @overload
    def scale_up(
        self: Cloud[Async], cluster_id: int, n: int, account: str | None = None, workspace: str | None = None
    ) -> Awaitable[Dict | None]: ...

    def scale_up(
        self, cluster_id: int, n: int, account: str | None = None, workspace: str | None = None
    ) -> Union[Dict | None, Awaitable[Dict | None]]:
        """Scale cluster to ``n`` workers

        Parameters
        ----------
        cluster_id
            Unique cluster identifier.
        n
            Number of workers to scale cluster size to.
        account
            **DEPRECATED**. Use ``workspace`` instead.
        workspace
            The Coiled workspace (previously "account") to use. If not specified,
            will check the ``coiled.workspace`` or ``coiled.account`` configuration values,
            or will use your default workspace if those aren't set.

        """
        return self._sync(self._scale_up, cluster_id, n, workspace or account)

    @overload
    def scale_down(
        self: Cloud[Sync],
        cluster_id: int,
        workers: Set[str],
        account: str | None = None,
        workspace: str | None = None,
    ) -> None: ...

    @overload
    def scale_down(
        self: Cloud[Async],
        cluster_id: int,
        workers: Set[str],
        account: str | None = None,
        workspace: str | None = None,
    ) -> Awaitable[None]: ...

    def scale_down(
        self,
        cluster_id: int,
        workers: Set[str],
        account: str | None = None,
        workspace: str | None = None,
    ) -> Awaitable[None] | None:
        """Scale cluster to ``n`` workers

        Parameters
        ----------
        cluster_id
            Unique cluster identifier.
        workers
            Set of workers to scale down to.
        account
            **DEPRECATED**. Use ``workspace`` instead.
        workspace
            The Coiled workspace (previously "account") to use. If not specified,
            will check the ``coiled.workspace`` or ``coiled.account`` configuration values,
            or will use your default workspace if those aren't set.

        """
        return self._sync(self._scale_down, cluster_id, workers, workspace or account)

    @track_context
    async def _better_cluster_logs(
        self,
        cluster_id: int,
        workspace: str | None = None,
        instance_ids: List[int] | None = None,
        dask: bool = False,
        system: bool = False,
        since_ms: int | None = None,
        until_ms: int | None = None,
        filter: str | None = None,
    ):
        workspace = workspace or self.default_workspace

        url_params = {}
        if dask:
            url_params["dask"] = "True"
        if system:
            url_params["system"] = "True"
        if since_ms:
            url_params["since_ms"] = f"{since_ms}"
        if until_ms:
            url_params["until_ms"] = f"{until_ms}"
        if filter:
            url_params["filter_pattern"] = f"{filter}"
        if instance_ids:
            url_params["instance_ids"] = ",".join(map(str, instance_ids))

        url_path = f"/api/v2/clusters/account/{workspace}/id/{cluster_id}/better-logs"

        response = await self._do_request(
            "GET",
            f"{self.server}{url_path}",
            params=url_params,
        )
        if response.status >= 400:
            await handle_api_exception(response)

        data = await response.json()

        return data

    def better_cluster_logs(
        self,
        cluster_id: int,
        account: str | None = None,
        workspace: str | None = None,
        instance_ids: List[int] | None = None,
        dask: bool = False,
        system: bool = False,
        since_ms: int | None = None,
        until_ms: int | None = None,
        filter: str | None = None,
    ) -> Logs:
        return self._sync(
            self._better_cluster_logs,
            cluster_id=cluster_id,
            workspace=workspace or account,
            instance_ids=instance_ids,
            dask=dask,
            system=system,
            since_ms=since_ms,
            until_ms=until_ms,
            filter=filter,
        )

    @track_context
    async def _scale_up(self, cluster_id: int, n: int, workspace: str | None = None, reason: str | None = None) -> Dict:
        """
        Increases the number of workers by ``n``.
        """
        workspace = workspace or self.default_workspace
        data = {"n_workers": n}
        if reason:
            # pyright is annoying
            data["reason"] = reason  # type: ignore
        response = await self._do_request(
            "POST", f"{self.server}/api/v2/workers/account/{workspace}/cluster/{cluster_id}/", json=data
        )
        if response.status >= 400:
            await handle_api_exception(response)

        workers_info = await response.json()

        return {"workers": {w["name"] for w in workers_info}}

    @track_context
    async def _scale_down(
        self, cluster_id: int, workers: Iterable[str], workspace: str | None = None, reason: str | None = None
    ) -> None:
        workspace = workspace or self.default_workspace
        workers = list(workers)  # yarl, used by aiohttp, expects list (not set) of strings

        reason_dict = {"reason": reason} if reason else {}
        response = await self._do_request(
            "DELETE",
            f"{self.server}/api/v2/workers/account/{workspace}/cluster/{cluster_id}/",
            params={"name": workers, **reason_dict},
        )
        if response.status >= 400:
            await handle_api_exception(response)

    @overload
    def security(
        self: Cloud[Sync], cluster_id: int, account: str | None = None, workspace: str | None = None
    ) -> Tuple[dask.distributed.Security, dict]: ...

    @overload
    def security(
        self: Cloud[Async], cluster_id: int, account: str | None = None, workspace: str | None = None
    ) -> Awaitable[Tuple[dask.distributed.Security, dict]]: ...

    def security(
        self, cluster_id: int, account: str | None = None, workspace: str | None = None
    ) -> Union[
        Tuple[dask.distributed.Security, dict],
        Awaitable[Tuple[dask.distributed.Security, dict]],
    ]:
        return self._sync(self._security, cluster_id, workspace or account)

    @track_context
    async def _fetch_package_levels(self, workspace: str | None = None) -> List[PackageLevel]:
        workspace = workspace or self.default_workspace
        response = await self._do_request("GET", f"{self.server}/api/v2/packages/", params={"account": workspace})
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    def get_ssh_key(
        self,
        cluster_id: int,
        workspace: str | None = None,
        worker: str | None = None,
    ) -> dict:
        workspace = workspace or self.default_workspace
        return self._sync(
            self._get_ssh_key,
            cluster_id=cluster_id,
            workspace=workspace,
            worker=worker,
        )

    @track_context
    async def _get_ssh_key(self, cluster_id: int, workspace: str, worker: str | None) -> dict:
        workspace = workspace or self.default_workspace

        route = f"/api/v2/clusters/account/{workspace}/id/{cluster_id}/ssh-key"
        url = f"{self.server}{route}"

        response = await self._do_request("GET", url, params={"worker": worker} if worker else None)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    def get_cluster_log_info(
        self,
        cluster_id: int,
        workspace: str | None = None,
    ) -> dict:
        workspace = workspace or self.default_workspace
        return self._sync(
            self._get_cluster_log_info,
            cluster_id=cluster_id,
            workspace=workspace,
        )

    @track_context
    async def _get_cluster_log_info(
        self,
        cluster_id: int,
        workspace: str,
    ) -> dict:
        workspace = workspace or self.default_workspace

        route = f"/api/v2/clusters/account/{workspace}/id/{cluster_id}/log-info"
        url = f"{self.server}{route}"

        response = await self._do_request("GET", url)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    @track_context
    async def _get_cluster_aggregated_metric(
        self,
        cluster_id: int,
        workspace: str | None,
        query: str,
        over_time: str,
        start_ts: int | None,
        end_ts: int | None,
    ):
        workspace = workspace or self.default_workspace
        route = f"/api/v2/metrics/account/{workspace}/cluster/{cluster_id}/value"
        url = f"{self.server}{route}"
        params = {"query": query, "over_time": over_time}
        if start_ts:
            params["start_ts"] = str(start_ts)
        if end_ts:
            params["end_ts"] = str(end_ts)

        response = await self._do_request("GET", url, params=params)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    @track_context
    async def _add_cluster_span(self, cluster_id: int, workspace: str | None, span_identifier: str, data: dict):
        workspace = workspace or self.default_workspace
        route = f"/api/v2/analytics/{workspace}/cluster/{cluster_id}/span/{span_identifier}"
        url = f"{self.server}{route}"

        response = await self._do_request("POST", url, json=data)
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    def _sync_request(self, route, method: str = "GET", json_result: bool = False, **kwargs):
        url = f"{self.server}{route}"
        response = self._sync(self._do_request, url=url, method=method, **kwargs)
        if response.status >= 400:
            raise ServerError(f"{url} returned {response.status}")

        async def get_result(r):
            return await (r.json() if json_result else r.text())

        return self._sync(
            get_result,
            response,
        )


Cloud = CloudV2


def cluster_logs(
    cluster_id: int,
    account: str | None = None,
    workspace: str | None = None,
    scheduler: bool = True,
    workers: bool = True,
    errors_only: bool = False,
):
    """
    Returns cluster logs as a dictionary, with a key for the scheduler and each worker.

    .. versionchanged:: 0.2.0
       ``cluster_name`` is no longer accepted, use ``cluster_id`` instead.
    """
    with CloudV2() as cloud:
        return cloud.cluster_logs(
            cluster_id=cluster_id,
            workspace=workspace or account,
            scheduler=scheduler,
            workers=workers,
            errors_only=errors_only,
        )


def better_cluster_logs(
    cluster_id: int,
    account: str | None = None,
    workspace: str | None = None,
    instance_ids: List[int] | None = None,
    dask: bool = False,
    system: bool = False,
    since_ms: int | None = None,
    until_ms: int | None = None,
    filter: str | None = None,
):
    """
    Pull logs for the cluster using better endpoint.

    Logs for recent clusters are split between system and container (dask), you can get
    either or both (or none).

    since_ms and until_ms are both inclusive (you'll get logs with timestamp matching those).
    """
    with Cloud() as cloud:
        return cloud.better_cluster_logs(
            cluster_id=cluster_id,
            workspace=workspace or account,
            instance_ids=instance_ids,
            dask=dask,
            system=system,
            since_ms=since_ms,
            until_ms=until_ms,
            filter=filter,
        )


def cluster_details(
    cluster_id: int,
    account: str | None = None,
    workspace: str | None = None,
) -> dict:
    """
    Get details of a cluster as a dictionary.
    """
    with CloudV2() as cloud:
        return cloud.cluster_details(
            cluster_id=cluster_id,
            workspace=workspace or account,
        )


def log_cluster_debug_info(
    cluster_id: int,
    account: str | None = None,
    workspace: str | None = None,
):
    with CloudV2() as cloud:
        details = cloud.cluster_details(cluster_id, workspace or account)
        logger.debug("Cluster details:")
        logger.debug(json.dumps(details, indent=2))

        states_by_type = cloud.get_cluster_states(cluster_id, workspace or account)

        logger.debug("cluster state history:")
        log_states(flatten_log_states(states_by_type), level=logging.DEBUG)


def create_cluster(
    name: str,
    *,
    software: str | None = None,
    worker_options: dict | None = None,
    scheduler_options: dict | None = None,
    account: str | None = None,
    workspace: str | None = None,
    workers: int = 0,
    environ: Dict | None = None,
    tags: Dict | None = None,
    dask_config: Dict | None = None,
    private_to_creator: bool | None = None,
    scheduler_vm_types: list | None = None,
    worker_vm_types: list | None = None,
    worker_disk_size: int | None = None,
    worker_disk_throughput: int | None = None,
    scheduler_disk_size: int | None = None,
    backend_options: Union[dict, AWSOptions, GCPOptions] | None = None,
) -> int:
    """Create a cluster

    Parameters
    ---------
    name
        Name of cluster.
    software
        Identifier of the software environment to use, in the format (<account>/)<name>. If the software environment
        is owned by the same account as that passed into "account", the (<account>/) prefix is optional.

        For example, suppose your account is "wondercorp", but your friends at "friendlycorp" have an environment
        named "xgboost" that you want to use; you can specify this with "friendlycorp/xgboost". If you simply
        entered "xgboost", this is shorthand for "wondercorp/xgboost".

        The "name" portion of (<account>/)<name> can only contain ASCII letters, hyphens and underscores.
    worker_options
        Mapping with keyword arguments to pass to ``worker_class``. Defaults to ``{}``.
    scheduler_options
        Mapping with keyword arguments to pass to the Scheduler ``__init__``. Defaults to ``{}``.
    account
        **DEPRECATED**. Use ``workspace`` instead.
    workspace
        The Coiled workspace (previously "account") to use. If not specified,
        will check the ``coiled.workspace`` or ``coiled.account`` configuration values,
        or will use your default workspace if those aren't set.
    workers
        Number of workers we to launch.
    environ
        Dictionary of environment variables.
    tags
        Dictionary of tags. Can also be set using the ``coiled.tags``
        Dask configuration option. Tags specified for cluster using keyword argument
        take precedence over those from Dask configuration.
    dask_config
        Dictionary of dask config to put on cluster

    See Also
    --------
    coiled.Cluster
    """
    with CloudV2(account=workspace or account) as cloud:
        cluster, _existing = cloud.create_cluster(
            name=name,
            software=software,
            worker_options=worker_options,
            scheduler_options=scheduler_options,
            workspace=workspace or account,
            workers=workers,
            environ=environ,
            tags=tags,
            dask_config=dask_config,
            private_to_creator=private_to_creator,
            backend_options=backend_options,
            worker_vm_types=worker_vm_types,
            worker_disk_size=worker_disk_size,
            worker_disk_throughput=worker_disk_throughput,
            scheduler_disk_size=scheduler_disk_size,
            scheduler_vm_types=scheduler_vm_types,
        )
        return cluster


@list_docstring
def list_clusters(account=None, workspace=None, max_pages: int | None = None, just_mine: bool = False):
    with CloudV2() as cloud:
        return cloud.list_clusters(workspace=workspace or account, max_pages=max_pages, just_mine=just_mine)


@delete_docstring
def delete_cluster(
    name: str | None = None,
    cluster_id: int | None = None,
    account: str | None = None,
    workspace: str | None = None,
    pause: bool = False,
):
    if name and cluster_id:
        raise ValueError("You specified both name and cluster_id, only one can be specified")
    if not name and not cluster_id:
        raise ValueError("You must specify either name or cluster_id")
    with CloudV2() as cloud:
        if not cluster_id:
            assert name  # too hard for pyright to figure out that name is str if cluster_id is falsy
            cluster_id = cloud.get_cluster_by_name(name=name, workspace=workspace or account)
        if cluster_id is not None:
            return cloud.delete_cluster(cluster_id=cluster_id, workspace=workspace or account, pause=pause)


def create_package_sync_software_env(
    workspace=None, gpu=False, arm=False, strict=False, force_rich_widget=False, **kwargs
):
    from coiled.capture_environment import scan_and_create

    with Cloud(workspace=workspace) as cloud:
        package_sync_env_alias = cloud._sync(
            scan_and_create,
            cloud=cloud,
            workspace=workspace,
            gpu_enabled=gpu,
            architecture=ArchitectureTypesEnum.ARM64 if arm else ArchitectureTypesEnum.X86_64,
            package_sync_strict=strict,
            force_rich_widget=force_rich_widget,
            **kwargs,
        )
        return package_sync_env_alias


def get_dask_client_from_batch_node():
    """
    Get Dask client for a Coiled Batch cluster.

    This function can be run on a node of a Coiled Batch cluster,
    and returns a dask.distributed.Client object connected to the Dask scheduler running
    on the scheduler node of the Batch cluster (which can also be a Dask cluster).
    """
    import os

    import dask.config
    from dask.distributed import Client

    scheduler_address = os.environ.get("COILED_INTERNAL_DASK_SCHEDULER_ADDRESS")

    if not scheduler_address:
        raise ValueError(
            "Unable to get scheduler address from COILED_INTERNAL_DASK_SCHEDULER_ADDRESS environment variable, "
            "this should automatically be set on Coiled Batch nodes."
        )

    security_config = {
        "scheduler-address": scheduler_address,
        "distributed.comm.tls.client.key": "/dask-tls/key",
        "distributed.comm.tls.client.cert": "/dask-tls/cert",
        "distributed.comm.tls.ca_file": "/dask-tls/cert",
        "distributed.comm.require-encryption": True,
    }

    with dask.config.set(security_config):
        return Client()
