from __future__ import annotations

import asyncio
import contextlib
import datetime
import json
import logging
import os
import re
import time
import traceback as tb
import uuid
import warnings
import weakref
from asyncio import wait_for
from contextlib import suppress
from copy import deepcopy
from inspect import isawaitable
from itertools import chain, islice
from types import TracebackType
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypedDict,
    TypeVar,
    Union,
    cast,
    overload,
)

import dask.config
import dask.distributed
import dask.utils
from distributed.core import Status
from distributed.deploy.adaptive import Adaptive
from distributed.deploy.cluster import Cluster as DistributedCluster
from distributed.objects import SchedulerInfo
from rich import print as rich_print
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn
from tornado.ioloop import PeriodicCallback
from typing_extensions import Literal, TypeAlias
from urllib3.util import parse_url

from coiled.capture_environment import scan_and_create
from coiled.cluster import CoiledAdaptive, CredentialsPreferred
from coiled.compatibility import DISTRIBUTED_VERSION, register_plugin
from coiled.context import track_context
from coiled.core import IsAsynchronous
from coiled.credentials.aws import get_aws_local_session_token
from coiled.credentials.google import get_gcp_local_session_token, send_application_default_credentials
from coiled.errors import ClusterCreationError, DoesNotExist
from coiled.exceptions import ArgumentCombinationError, InstanceTypeError, ParseIdentifierError, PermissionsError
from coiled.plugins import DaskSchedulerWriteFiles, DaskWorkerWriteFiles
from coiled.types import ArchitectureTypesEnum, AWSOptions, GCPOptions, PackageLevelEnum
from coiled.utils import (
    COILED_LOGGER_NAME,
    DASK_PRESPAWN_THREAD_VARS_UNSET,
    GCP_SCHEDULER_GPU,
    any_gpu_instance_type,
    cluster_firewall,
    error_info_for_tracking,
    get_details_url,
    get_grafana_url,
    get_instance_type_from_cpu_memory,
    is_arm_only_image,
    normalize_environ,
    parse_bytes_as_gib,
    parse_identifier,
    parse_wait_for_workers,
    short_random_string,
    truncate_traceback,
    unset_single_thread_defaults,
    validate_vm_typing,
)

from ..core import Async, AWSSessionCredentials, Sync
from .core import (
    CloudV2,
    CloudV2SyncAsync,
    log_cluster_debug_info,
    setup_logging,
)
from .cwi_log_link import cloudwatch_url
from .states import (
    ClusterStateEnum,
    InstanceStateEnum,
    ProcessStateEnum,
    flatten_log_states,
    group_worker_errors,
    log_states,
    summarize_status,
)
from .widgets import EXECUTION_CONTEXT, ClusterWidget
from .widgets.rich import CONSOLE_WIDTH, RichClusterWidget
from .widgets.util import use_rich_widget

logger = logging.getLogger(COILED_LOGGER_NAME)

_T = TypeVar("_T")

NO_CLIENT_DEFAULT = object()  # don't use `None` as the default so that `None` can be specified by user

TERMINATING_STATES = (
    Status.closing,
    Status.closed,
    Status.closing_gracefully,
    Status.failed,
)

BEHAVIOR_TO_LEVEL = {
    "critical-only": PackageLevelEnum.CRITICAL,
    "warning-or-higher": PackageLevelEnum.WARN,
    "any": PackageLevelEnum.NONE,
}

DEFAULT_ADAPTIVE_MIN = 4
DEFAULT_ADAPTIVE_MAX = 20

ClusterSyncAsync: TypeAlias = Union["Cluster[Async]", "Cluster[Sync]"]

_vm_type_cpu_memory_error_msg = (
    "Argument '{kind}_vm_types' can't be used together with '{kind}_cpu' or '{kind}_memory'. "
    "Please use either '{kind}_vm_types' or '{kind}_cpu'/'{kind}_memory' separately."
)


class ClusterKwargs(TypedDict, total=False):
    name: str | None
    software: str | None
    container: str | None
    n_workers: Union[int, List[int]] | None
    worker_class: str | None
    worker_options: dict | None
    worker_vm_types: list | None
    worker_cpu: Union[int, List[int]] | None
    worker_memory: Union[str, List[str]] | None
    worker_disk_size: Union[int, str] | None
    worker_disk_throughput: int | None
    worker_disk_config: dict | None
    worker_gpu: Union[int, bool] | None
    worker_gpu_type: str | None
    scheduler_options: dict | None
    scheduler_vm_types: list | None
    scheduler_cpu: Union[int, List[int]] | None
    scheduler_memory: Union[str, List[str]] | None
    scheduler_disk_size: int | None
    scheduler_disk_config: dict | None
    scheduler_gpu: bool | None
    asynchronous: bool
    cloud: CloudV2 | None
    account: str | None
    workspace: str | None
    shutdown_on_close: bool | None
    idle_timeout: str | None
    cluster_timeout: str | None
    no_client_timeout: str | None | object
    use_scheduler_public_ip: bool | None
    use_dashboard_https: bool | None
    dashboard_custom_subdomain: str | None
    credentials: str | None
    credentials_duration_seconds: int | None
    timeout: Union[int, float] | None
    environ: Dict[str, str] | None
    tags: Dict[str, str] | None
    send_dask_config: bool
    unset_single_threading_variables: bool | None
    backend_options: Union[AWSOptions, GCPOptions] | None
    show_widget: bool | None
    custom_widget: ClusterWidget | None
    configure_logging: bool | None
    wait_for_workers: Union[int, float, bool] | None
    package_sync: Union[bool, List[str]] | None
    package_sync_strict: bool
    package_sync_ignore: List[str] | None
    package_sync_only: List[str] | None
    package_sync_conda_extras: List[str] | None
    package_sync_fail_on: Literal["critical-only", "warning-or-higher", "any"]
    package_sync_use_uv_installer: bool
    private_to_creator: bool | None
    use_best_zone: bool | None
    allow_cross_zone: bool
    compute_purchase_option: Literal["on-demand", "spot", "spot_with_fallback"] | None
    spot_policy: Literal["on-demand", "spot", "spot_with_fallback"] | None
    extra_worker_on_scheduler: bool | None
    _n_worker_specs_per_host: int | None
    scheduler_port: int | None
    allow_ingress_from: str | None
    allow_ssh_from: str | None
    allow_ssh: bool | None
    allow_spark: bool | None
    open_extra_ports: List[int] | None
    jupyter: bool | None
    mount_bucket: Union[str, List[str]] | None
    host_setup_script: str | None
    region: str | None
    arm: bool | None
    batch_job_container: str | None
    pause_on_exit: bool | None


class Cluster(DistributedCluster, Generic[IsAsynchronous]):
    """Create a Dask cluster with Coiled

    Parameters
    ----------
    n_workers
        Number of workers in this cluster.
        Can either be an integer for a static number of workers,
        or a ``[min, max]`` list specifying the lower and upper bounds for adaptively
        scaling up/down workers depending on the amount of work submitted.
        For adaptive scaling, you can also specify an initial number of workers as ``[min, initial, max]``.
        Defaults to ``n_workers=[4, 20]`` which adaptively scales between
        4 and 20 workers, and initially starts with 4 workers.
    name
        Name to use for identifying this cluster. Defaults to ``None``.
    software
        Name of the software environment to use; this allows you to use and re-use existing
        Coiled software environments. Specifying this argument will disable package sync, and it
        cannot be combined with ``container``.
    container
        Name or URI of container image to use; when using a pre-made container image with Coiled,
        this allows you to skip the step of explicitly creating a Coiled software environment
        from that image. Specifying this argument will disable package sync, and it
        cannot be combined with ``software``.
    ignore_container_entrypoint
        Ignore entrypoint for specified Docker container (like ``docker run --entrypoint``);
        default is to use the entrypoint (if any) set on the image.
    worker_class
        Worker class to use. Defaults to :class:`distributed.nanny.Nanny`.
    worker_options
        Mapping with keyword arguments to pass to ``worker_class``. Defaults
        to ``{}``.
    worker_vm_types
        List of instance types that you would like workers to use, default instance type
        selected contains 4 cores. You can use the command ``coiled.list_instance_types()``
        to see a list of allowed types.
    worker_cpu
        Number, or range, of CPUs requested for each worker. Specify a range by
        using a list of two elements, for example: ``worker_cpu=[2, 8]``.
    worker_memory
        Amount of memory to request for each worker, Coiled will use a +/- 10% buffer
        from the memory that you specify. You may specify a range of memory by using a
        list of two elements, for example: ``worker_memory=["2GiB", "4GiB"]``.
    worker_disk_size
        Non-default size of persistent disk attached to each worker instance, specified as string with units
        or integer for GiB.
    worker_disk_throughput
        EXPERIMENTAL. For AWS, non-default throughput (in MB/s) for EBS gp3 volumes attached
        to workers.
    worker_disk_config
        Allows custom configuration of the disk attached to worker VMs.
        For AWS, this can be ``EbsBlockDevice`` dictionary that overrides our default EBS config.
    worker_gpu
        Number of GPUs to attach to each worker. Default is 0, ``True`` is interpreted as 1.
        Note that this is ignored if you're explicitly specifying an instance type which
        includes a fixed number of GPUs.
    worker_gpu_type
        For GCP, this lets you specify type of guest GPU for instances.
        Should match the way the cloud provider specifies the GPU, for example:
        ``worker_gpu_type="nvidia-tesla-t4"``.
        By default, Coiled will request NVIDIA T4 if GPU type isn't specified.
        For AWS, if you want GPU other than T4, you'll need to explicitly specify the VM
        instance type (e.g., ``g6.xlarge`` for instance with one NVIDIA L4 GPU).
    scheduler_options
        Mapping with keyword arguments to pass to the Scheduler ``__init__``. Defaults
        to ``{}``.
    scheduler_vm_types
        List of instance types that you would like the scheduler to use, default instances
        type selected contains 4 cores. You can use the command
        ``coiled.list_instance_types()`` to se a list of allowed types.
    scheduler_cpu
        Number, or range, of CPUs requested for the scheduler. Specify a range by
        using a list of two elements, for example: ``scheduler_cpu=[2, 8]``.
    scheduler_memory
        Amount of memory to request for the scheduler, Coiled will use a +/-10%
        buffer from the memory what you specify. You may specify a range of memory by using a
        list of two elements, for example: ``scheduler_memory=["2GiB", "4GiB"]``.
    scheduler_gpu
        Whether to attach GPU to scheduler; this would be a single NVIDIA T4.
        The best practice for Dask is to have a GPU on the scheduler if you are using GPUs on your
        workers, so if you don't explicitly specify, Coiled will follow this best practice and give
        you a scheduler GPU just in case you have ``worker_gpu`` set.
    scheduler_disk_config
        Allows custom configuration of the disk attached to scheduler VM.
        For AWS, this can be ``EbsBlockDevice`` dictionary that overrides our default EBS config.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    cloud
        Cloud object to use for interacting with Coiled. This object contains user/authentication/account
        information. If this is None (default), we look for a recently-cached Cloud object, and if none
        exists create one.
    account
        **DEPRECATED**. Use ``workspace`` instead.
    workspace
        The Coiled workspace (previously "account") to use. If not specified,
        will check the ``coiled.workspace`` or ``coiled.account`` configuration values,
        or will use your default workspace if those aren't set.
    shutdown_on_close
        Whether or not to shut down the cluster when it finishes.
        Defaults to True, unless name points to an existing cluster.
    idle_timeout
        Shut down the cluster after this duration if no activity has occurred. E.g. "30 minutes"
        Default: "20 minutes"
    cluster_timeout
        Shut down the cluster after this duration (even if active). E.g. "2 hours"
        Default: ``None``
    no_client_timeout
        Shut down the cluster after this duration after all clients have disconnected.
        When ``shutdown_on_close`` is ``False`` this is disabled,
        since ``shutdown_on_close=False`` usually means you want to keep cluster up
        after disconnecting so you can later connect a new client.
        Default: "2 minutes", or ``idle_timeout`` if there's a non-default idle timeout
    use_scheduler_public_ip
        Boolean value that determines if the Python client connects to the
        Dask scheduler using the scheduler machine's public IP address. The
        default behaviour when set to True is to connect to the scheduler
        using its public IP address, which means traffic will be routed over
        the public internet. When set to False, traffic will be routed over
        the local network the scheduler lives in, so make sure the scheduler
        private IP address is routable from where this function call is made
        when setting this to False.
    use_dashboard_https
        When public IP address is used for dashboard, we'll enable HTTPS + auth by default.
        You may want to disable this if using something that needs to connect directly to
        the scheduler dashboard without authentication, such as jupyter dask-labextension<=6.1.0.
    credentials
        Which credentials to use for Dask operations and forward to Dask
        clusters -- options are "local", or None. The default
        behavior is to use local credentials if available.
        NOTE: credential handling currently only works with AWS credentials.
    credentials_duration_seconds
        For "local" credentials shipped to cluster as STS token, set the duration of STS token.
        If not specified, the AWS default will be used.
    timeout
        Timeout in seconds to wait for a cluster to start, will use
        ``default_cluster_timeout`` set on parent Cloud by default.
    environ
        Dictionary of environment variables. Values will be transmitted to Coiled; for private environment variables
        (e.g., passwords or access keys you use for data access), :meth:`send_private_envs` is recommended.
    send_dask_config
        Whether to send a frozen copy of local ``dask.config`` to the cluster.
    unset_single_threading_variables
        By default, Dask sets environment variables such as ``OMP_NUM_THREADS`` and ``MKL_NUM_THREADS`` so that
        relevant libraries use a single thread per Dask worker (by default there are as many Dask workers as
        CPU cores). In some cases this is not what you want, so this option overrides the default Dask behavior.
    backend_options
        Dictionary of backend specific options.
    show_widget
        Whether to use the rich-based widget display.
        By default, the widget will show in IPython/Jupyter; specify ``show_widget=True`` to make widget show
        even when not in IPython/Jupyter (for example, when making cluster in code invoked via CLI).
        For use cases involving multiple Clusters at once, ``show_widget=False`` is recommended.
    custom_widget
        Use the rich-based widget display outside of IPython/Jupyter
        (Default: False)
    tags
        Dictionary of tags. Can also be set using the ``coiled.tags``
        Dask configuration option. Tags specified for cluster using keyword argument
        take precedence over those from Dask configuration.
    wait_for_workers
        Whether to wait for a number of workers before returning control
        of the prompt back to the user. Usually, computations will run better
        if you wait for most workers before submitting tasks to the cluster.
        You can wait for all workers by passing ``True``, or not wait for any
        by passing ``False``. You can pass a fraction of the total number of
        workers requested as a float(like 0.6), or a fixed number of workers
        as an int (like 13). If None, the value from ``coiled.wait-for-workers``
        in your Dask config will be used. Default: 0.3. If the requested number
        of workers don't launch within 10 minutes, the cluster will be shut
        down, then a TimeoutError is raised.
    package_sync
        DEPRECATED -- Always enabled when ``container`` and ``software`` are not given.
        Synchronize package versions between your local environment and the cluster.
        Cannot be used with the ``container`` or ``software`` options.
        Passing specific packages as a list of strings will attempt to synchronize only those packages,
        use with caution. (Deprecated: use ``package_sync_only`` instead.)
        We recommend reading the
        `additional documentation for this feature <https://docs.coiled.io/user_guide/package_sync.html>`_
    package_sync_conda_extras
        A list of conda package names (available on conda-forge) to include in the environment that
        are not in your local environment. Use with caution, as this can lead to dependency
        conflicts with local packages. Note, this will only work for conda package with
        platform-specific builds (i.e., not "noarch" packages).
    package_sync_ignore
        A list of package names to exclude from the environment. Note their dependencies may still be installed,
        or they may be installed by another package that depends on them!
    package_sync_only
        A list of package names to only include from the environment. Use with caution.
        We recommend reading the
        `additional documentation for this feature <https://docs.coiled.io/user_guide/package_sync.html>`_
    package_sync_strict
        Only allow exact packages matches, not recommended unless your client platform/architecture
        matches the cluster platform/architecture
    package_sync_use_uv_installer
        Use ``uv`` to install pip packages when building the software environment. This should only be
        disabled if you are experiencing issues with ``uv`` and need to use ``pip`` instead.
        (Default: True)
    private_to_creator
        Only allow the cluster creator, not other members of team account, to connect to this cluster.
    use_best_zone
        Allow the cloud provider to pick the zone (in your specified region) that has best availability
        for your requested instances. We'll keep the scheduler and workers all in a single zone in
        order to avoid any cross-zone network traffic (which would be billed).
    allow_cross_zone
        Allow the cluster to have VMs in distinct zones. There's a cost for cross-zone traffic
        (usually pennies per GB), so this is a bad choice for shuffle-heavy workloads, but can be a good
        choice for large embarrassingly parallel workloads.
    spot_policy
        Purchase option to use for workers in your cluster, options are "on-demand", "spot", and
        "spot_with_fallback"; by default this is "on-demand".
        (Google Cloud refers to this as "provisioning model" for your instances.)
        **Spot instances** are much cheaper, but can have more limited availability and may be terminated
        while you're still using them if the cloud provider needs more capacity for other customers.
        **On-demand instances** have the best availability and are almost never
        terminated while still in use, but they're significantly more expensive than spot instances.
        For most workloads, "spot_with_fallback" is likely to be a good choice: Coiled will try to get as
        many spot instances as we can, and if we get less than you requested, we'll try to get the remaining
        instances as on-demand.
        For AWS, when we're notified that an active spot instance is going to be terminated,
        we'll attempt to get a replacement instance (spot if available, but could be on-demand if you've
        enabled "fallback"). Dask on the active instance will attempt a graceful shutdown before the
        instance is terminated so that computed results won't be lost.
    scheduler_port
        Specify a port other than the default (443) for communication with Dask scheduler.
        Usually the default is the right choice; Coiled supports using 443 concurrently for scheduler comms
        and for scheduler dashboard.
    allow_ingress_from
        Control the CIDR from which cluster firewall allows ingress to scheduler; by default this is open
        to any source address (0.0.0.0/0). You can specify CIDR, or "me" for just your IP address.
    allow_ssh_from
        Allow connections to scheduler over port 22 (used for SSH) for a specified IP address or CIDR.
    allow_ssh
        Allow connections to scheduler over port 22, used for SSH.
    allow_spark
        Allow (secured) connections to scheduler on port 15003 used by Spark Connect. By default, this port is open.
    jupyter
        Start a Jupyter server in the same process as Dask scheduler. The Jupyter server will be behind HTTPS
        with authentication (unless you disable ``use_dashboard_https``, which we strongly recommend against).
        Note that ``jupyterlab`` will need to be installed in the software environment used on the cluster
        (or in your local environment if using package sync).
        Once the cluster is running, you can use ``jupyter_link`` to get link to access the Jupyter server.
    mount_bucket
        Optional name or list of names of buckets to mount. For example, ``"s3://my-s3-bucket"`` will mount the S3
        bucket ``my-s3-bucket``, using your forwarded AWS credentials, and ``"gs://my-gcs-bucket"`` will mount
        the GCS bucket ``my-gcs-bucket`` using your forwarded Google Application Default Credentials.
        Buckets are mounted to subdirectories in both ``/mount`` and ``./mount`` (relative to working directory
        for Dask), subdirectory name will be taken from bucket name. By default, mounting times out after 30 s.
        You can manually configure a different timeout using the ``coiled.mount-bucket.timeout`` configuration value.
    host_setup_script
        Script to run on the host VM during the setup process.
        You can either specify as text of the script to run, or as path to a local script file to copy and run.
    region
        The cloud provider region in which to run the cluster.
    arm
        Use ARM instances for cluster; default is x86 (Intel) instances.
    pause_on_exit
        Pause the cluster instead of shutting it down when exiting.
    """

    _instances = weakref.WeakSet()

    def __init__(
        self: ClusterSyncAsync,
        name: str | None = None,
        *,
        software: str | None = None,
        container: str | None = None,
        ignore_container_entrypoint: bool | None = None,
        n_workers: Union[int, List[int]] | None = None,
        worker_class: str | None = None,
        worker_options: dict | None = None,
        worker_vm_types: list | None = None,
        worker_cpu: Union[int, List[int]] | None = None,
        worker_memory: Union[str, List[str]] | None = None,
        worker_disk_size: Union[int, str] | None = None,
        worker_disk_throughput: int | None = None,
        worker_disk_config: dict | None = None,
        worker_gpu: Union[int, bool] | None = None,
        worker_gpu_type: str | None = None,
        scheduler_options: dict | None = None,
        scheduler_vm_types: list | None = None,
        scheduler_cpu: Union[int, List[int]] | None = None,
        scheduler_memory: Union[str, List[str]] | None = None,
        scheduler_disk_size: int | None = None,
        scheduler_disk_config: dict | None = None,
        scheduler_gpu: bool | None = None,
        asynchronous: bool = False,
        cloud: CloudV2 | None = None,
        account: str | None = None,
        workspace: str | None = None,
        shutdown_on_close: bool | None = None,
        idle_timeout: str | None = None,
        cluster_timeout: str | None = None,
        no_client_timeout: str | None | object = NO_CLIENT_DEFAULT,
        use_scheduler_public_ip: bool | None = None,
        use_dashboard_https: bool | None = None,
        dashboard_custom_subdomain: str | None = None,
        credentials: str | None = "local",
        credentials_duration_seconds: int | None = None,
        timeout: Union[int, float] | None = None,
        environ: Dict[str, str] | None = None,
        tags: Dict[str, str] | None = None,
        send_dask_config: bool = True,
        unset_single_threading_variables: bool | None = None,
        backend_options: Union[AWSOptions, GCPOptions] | None = None,  # intentionally not in the docstring yet
        show_widget: bool | None = None,
        custom_widget: ClusterWidget | None = None,
        configure_logging: bool | None = None,
        wait_for_workers: Union[int, float, bool] | None = None,
        package_sync: Union[bool, List[str]] | None = None,
        package_sync_strict: bool = False,
        package_sync_conda_extras: List[str] | None = None,
        package_sync_ignore: List[str] | None = None,
        package_sync_only: List[str] | None = None,
        package_sync_fail_on: Literal["critical-only", "warning-or-higher", "any"] = "critical-only",
        package_sync_use_uv_installer: bool = True,
        private_to_creator: bool | None = None,
        use_best_zone: bool | None = None,
        allow_cross_zone: bool = False,
        # "compute_purchase_option" is the old name for "spot_policy"
        # someday we should deprecate and then remove compute_purchase_option
        compute_purchase_option: Literal["on-demand", "spot", "spot_with_fallback"] | None = None,
        spot_policy: Literal["on-demand", "spot", "spot_with_fallback"] | None = None,
        extra_worker_on_scheduler: bool | None = None,
        _n_worker_specs_per_host: int | None = None,
        # easier network config
        scheduler_port: int | None = None,
        allow_ingress_from: str | None = None,
        allow_ssh_from: str | None = None,
        allow_ssh: bool | None = None,
        allow_spark: bool | None = None,
        open_extra_ports: List[int] | None = None,
        jupyter: bool | None = None,
        mount_bucket: Union[str, List[str]] | None = None,
        host_setup_script: str | None = None,
        region: str | None = None,
        arm: bool | None = None,
        batch_job_ids: List[int] | None = None,
        batch_job_container: str | None = None,
        pause_on_exit: bool | None = None,
    ):
        self.pause_on_exit = pause_on_exit
        self.init_time = datetime.datetime.now(tz=datetime.timezone.utc)
        type(self)._instances.add(self)

        # Determine consistent sync/async
        if cloud and asynchronous is not None and cloud.asynchronous != asynchronous:
            warnings.warn(
                f"Requested a Cluster with asynchronous={asynchronous}, but "
                f"cloud.asynchronous={cloud.asynchronous}, so the cluster will be"
                f"{cloud.asynchronous}",
                stacklevel=2,
            )

            asynchronous = cloud.asynchronous

        self.scheduler_comm: dask.distributed.rpc | None = None

        # It's annoying that the user must pass in `asynchronous=True` to get an async Cluster object
        # But I can't think of a good alternative right now.
        self.cloud: CloudV2SyncAsync = cloud or CloudV2.current(asynchronous=asynchronous)

        if configure_logging:
            setup_logging()

        if configure_logging is None:
            # setup logging only if we're not using the widget
            if not (custom_widget or use_rich_widget()):
                setup_logging()

        # we really need to call this first before any of the below code errors
        # out; otherwise because of the fact that this object inherits from
        # deploy.Cloud __del__ (and perhaps __repr__) will have AttributeErrors
        # because the gc will run and attributes like `.status` and
        # `.scheduler_comm` will not have been assigned to the object's instance
        # yet
        super().__init__(asynchronous=asynchronous, loop=self.cloud.loop)

        # control-plane can override dask config settings per user/workspace/org
        self.cloud.load_server_dask_config(workspace=account or workspace)

        self._cluster_event_queue = []

        # default range for adaptive (defining these here so pyright doesn't complain about ref before assignment)
        adaptive_min = DEFAULT_ADAPTIVE_MIN
        adaptive_max = DEFAULT_ADAPTIVE_MAX
        adaptive_init = None
        self._original_n_workers = n_workers
        if n_workers is None:
            # use adaptive if user didn't specify number of workers
            self.start_adaptive = True
        elif isinstance(n_workers, (list, tuple)):
            # user specified [min, max] or [min, initial, max] range which will be used for adaptive
            self.start_adaptive = True
            if len(n_workers) == 2:
                adaptive_min, adaptive_max = n_workers
            elif len(n_workers) == 3:
                adaptive_min, adaptive_init, adaptive_max = n_workers
            else:
                raise ValueError(
                    f"You specified `n_workers={n_workers}`. "
                    f"When specifying n_workers it must be single number of workers, "
                    f"or `[min, max]` or `[min, initial, max]` for adaptive scaling range."
                )
        else:
            self.start_adaptive = False

        # Use the adaptive min as the default initial number of workers to start, but also allow user to specify.
        if self.start_adaptive:
            n_workers = adaptive_min if adaptive_init is None else adaptive_init
            if n_workers < adaptive_min:
                raise ValueError(
                    f"Initial number of workers was specified as {n_workers}. "
                    f"This cannot be less than the minimum specified size for adaptive scaling ({adaptive_min})."
                )
            if n_workers > adaptive_max:
                raise ValueError(
                    f"Initial number of workers was specified as {n_workers}. "
                    f"This cannot be greater than the maximum specified size for adaptive scaling ({adaptive_max})."
                )

        # by this point n_workers will always be an int, but pyright isn't good at understanding this
        n_workers = cast(int, n_workers)

        # When there's an extra worker on scheduler, we'll request one fewer "worker" VM (non-scheduler VM)
        # because the scheduler VM will also be running a worker process.
        # Effectively this means that `n_workers` will be interpreted as number of VMs running a worker process.
        # Note that adaptive also interprets the min/max in this way, the extra worker is counted when determining
        # how much to scale up/down in order to get to adaptive target.
        if extra_worker_on_scheduler:
            n_workers -= 1 if n_workers else 0

        self.unset_single_threading_variables = bool(unset_single_threading_variables)

        # NOTE:
        # this attribute is only updated while we wait for cluster to come up
        self.errored_worker_count: int = 0

        senv_kwargs = {
            "package_sync": package_sync,
            "software": software,
            "container": container,
        }
        set_senv_kwargs = [name for name, value in senv_kwargs.items() if value]
        if len(set_senv_kwargs) > 1:
            raise ValueError(
                f"Multiple software environment parameters are set: {', '.join(set_senv_kwargs)}. "
                "You must use only one of these."
            )
        if not container and ignore_container_entrypoint is not None:
            raise ValueError(
                "`ignore_container_entrypoint` must be used together with the `container` keyword; "
                "it is not compatible with `package_sync` or `software`"
            )
        self._software_environment_name = ""
        self._package_sync_use_uv_installer = package_sync_use_uv_installer
        if package_sync is not None:
            warnings.warn(
                "`package_sync` is a deprecated kwarg for `Cluster` and will be removed in a future release. "
                "To only sync certain packages, use `package_sync_only`, and to disable package sync, pass the "
                "`container` or `software` kwargs instead.",
                category=FutureWarning,
                stacklevel=2,
            )
        self.package_sync = bool(package_sync)
        self.package_sync_ignore = package_sync_ignore
        self.package_sync_conda_extras = package_sync_conda_extras
        # We set this config option in `coiled hello` to reduce package sync build errors
        if not package_sync_only and dask.config.get("coiled._internal.package_sync_only", False):
            package_sync_only = dask.config.get("coiled._internal.package_sync_only")
        self.package_sync_only = set(package_sync_only) if package_sync_only else None
        if isinstance(package_sync, list):
            if self.package_sync_only:
                self.package_sync_only.update(set(package_sync))
            else:
                self.package_sync_only = set(package_sync)
        if self.package_sync_only is not None:
            # ensure critical packages are always included so cluster can start
            self.package_sync_only.update((
                "cloudpickle",
                "dask",
                "distributed",
                "msgpack-python",
                "msgpack",
                "pip",
                "python",
                "tornado",
            ))

        self.package_sync_strict = package_sync_strict
        self.package_sync_fail_on = BEHAVIOR_TO_LEVEL[package_sync_fail_on]
        self.show_widget = True if show_widget is None else show_widget
        self._force_rich_widget = True if show_widget else False
        self.custom_widget = custom_widget

        if arm is None and (batch_job_container or container) and not (scheduler_vm_types or worker_vm_types):
            # The user didn't explicitly ask for ARM or non-ARM, so if they provided a container,
            # see if we can match the required arch of that container.
            # We're using public Docker Hub endpoint, so this only works currently for public images there.
            image = batch_job_container or container or ""
            if is_arm_only_image(image):
                arm = True

        self.arch = ArchitectureTypesEnum.ARM64 if arm else ArchitectureTypesEnum.X86_64

        self._cluster_status_logs = []

        if region is not None:
            if backend_options is None:
                backend_options = {}
            # backend_options supports both `region` and `region_name` (for backwards compatibility
            # since we changed it at some point).
            # If either of those is specified along with kwarg `region=`, raise an exception.
            if "region_name" in backend_options:
                raise ValueError(
                    "You passed `region` as a kwarg to Cluster(...), and included region_name"
                    " in the backend_options dict. Only one of those should be specified."
                )
            if "region" in backend_options:
                raise ValueError(
                    "You passed `region` as a kwarg to Cluster(...), and included region"
                    " in the backend_options dict. Only one of those should be specified."
                )
            backend_options["region_name"] = region

        self.timeout = timeout if timeout is not None else self.cloud.default_cluster_timeout

        # Set cluster attributes from kwargs (first choice) or dask config

        self.private_to_creator = (
            dask.config.get("coiled.private-to-creator") if private_to_creator is None else private_to_creator
        )

        self.extra_worker_on_scheduler = extra_worker_on_scheduler
        self._worker_on_scheduler_name = None
        self.n_worker_specs_per_host = _n_worker_specs_per_host
        self.batch_job_ids = batch_job_ids

        # somewhat internal API since batch kwargs shouldn't be used directly by user but are for batch API:
        # "!" at end of container URI means "ignore entrypoint"
        if batch_job_container and batch_job_container[-1] == "!":
            self.extra_user_container = batch_job_container.rstrip("!")
            self.extra_user_container_ignore_entrypoint = True
        else:
            self.extra_user_container = batch_job_container
            self.extra_user_container_ignore_entrypoint = False

        self.software_environment = software or dask.config.get("coiled.software")
        self.software_container = container or dask.config.get("coiled.container", None)
        self.software_use_entrypoint = not ignore_container_entrypoint
        if not container and not self.software_environment and not package_sync:
            self.package_sync = True

        self.worker_class = worker_class or dask.config.get("coiled.worker.class")
        self.worker_cpu = worker_cpu or cast(Union[int, List[int]], dask.config.get("coiled.worker.cpu"))

        if isinstance(worker_cpu, int) and worker_cpu <= 1:
            if not arm:
                raise ValueError("`worker_cpu` should be at least 2 for x86 instance types.")
            elif worker_cpu < 1:
                raise ValueError("`worker_cpu` should be at least 1 for arm instance types.")

        self.worker_memory = worker_memory or dask.config.get("coiled.worker.memory")
        # FIXME get these from dask config
        self.worker_vm_types = worker_vm_types
        self.worker_disk_size = parse_bytes_as_gib(worker_disk_size)

        self.worker_disk_throughput = worker_disk_throughput
        self.worker_disk_config = worker_disk_config
        self.worker_gpu_count = int(worker_gpu) if worker_gpu is not None else None
        self.worker_gpu_type = worker_gpu_type
        self.worker_options = {
            **(cast(dict, dask.config.get("coiled.worker-options", {}))),
            **(worker_options or {}),
        }

        self.scheduler_vm_types = scheduler_vm_types
        self.scheduler_cpu = scheduler_cpu or cast(Union[int, List[int]], dask.config.get("coiled.scheduler.cpu"))
        self.scheduler_memory = scheduler_memory or cast(
            Union[int, List[int]], dask.config.get("coiled.scheduler.memory")
        )
        self.scheduler_disk_size = parse_bytes_as_gib(scheduler_disk_size)
        self.scheduler_disk_config = scheduler_disk_config
        self.scheduler_options = {
            **(cast(dict, dask.config.get("coiled.scheduler-options", {}))),
            **(scheduler_options or {}),
        }

        # use dask config if kwarg not specified for scheduler gpu
        scheduler_gpu = scheduler_gpu if scheduler_gpu is not None else dask.config.get("coiled.scheduler.gpu")

        self._is_gpu_cluster = (
            # explicitly specified GPU (needed for GCP guest GPU)
            bool(worker_gpu or worker_gpu_type or scheduler_gpu)
            # or GPU bundled with explicitly specified instance type
            or any_gpu_instance_type(worker_vm_types)
            or any_gpu_instance_type(scheduler_vm_types)
        )

        if scheduler_gpu is None:
            # when not specified by user (via kwarg or config), default to GPU on scheduler if workers have GPU
            scheduler_gpu = True if self._is_gpu_cluster else False
        else:
            scheduler_gpu = bool(scheduler_gpu)
        self.scheduler_gpu = scheduler_gpu

        # use best zone by default, unless user explicitly specified zone name
        self.use_best_zone = not ((backend_options or {}).get("zone_name")) if use_best_zone is None else use_best_zone
        self.allow_cross_zone = allow_cross_zone

        self.spot_policy = spot_policy
        if compute_purchase_option:
            if spot_policy:
                raise ValueError(
                    "You specified both compute_purchase_option and spot_policy, "
                    "which serve the same purpose. Please specify only spot_policy."
                )
            else:
                self.spot_policy = compute_purchase_option

        if workspace and account and workspace != account:
            raise ValueError(
                f"You specified both workspace='{workspace}' and account='{account}'. "
                "The `account` kwarg is being deprecated, use `workspace` instead."
            )
        if account and not workspace:
            warnings.warn(
                "The `account` kwarg is deprecated, use `workspace` instead.", DeprecationWarning, stacklevel=2
            )

        self.name = name or cast(Optional[str], dask.config.get("coiled.name"))
        self.workspace = workspace or account
        self._start_n_workers = n_workers
        self._lock = None
        self._asynchronous = asynchronous
        self._is_coiled_hosted = False
        self.shutdown_on_close = shutdown_on_close

        self.environ = normalize_environ(environ)
        aws_default_region = self._get_aws_default_region()
        if aws_default_region:
            self.environ["AWS_DEFAULT_REGION"] = aws_default_region

        # Cluster-specific kwarg tags take precedence over globally set config tags
        kwarg_tags = {k: str(v) for (k, v) in (tags or {}).items() if v}
        self.tags = {**dask.config.get("coiled.tags", {}), **kwarg_tags}
        self.frozen_dask_config = deepcopy(dask.config.config) if send_dask_config else {}
        self.credentials = CredentialsPreferred(credentials)
        self._credentials_duration_seconds = credentials_duration_seconds
        self._default_protocol = dask.config.get("coiled.protocol", "tls")
        self._wait_for_workers_arg = wait_for_workers
        self._last_logged_state_summary = None
        self._try_local_gcp_creds = True
        self._using_aws_creds_endpoint = False
        self._credentials_refresh_at = None
        self._credentials_refresh_handle = None

        if send_dask_config:
            if self.unset_single_threading_variables:
                dask.config.update(self.frozen_dask_config, DASK_PRESPAWN_THREAD_VARS_UNSET)

            try:
                json.dumps(self.frozen_dask_config)
            except TypeError as e:
                logger.warning(
                    f"Local dask config file is not JSON serializable because {e}, "
                    f"so we cannot forward dask config to cluster."
                )
                self.frozen_dask_config = None

            dask_log_config = dask.config.get("logging", {})
            if dask_log_config:
                # logging can be set in different ways in dask config, for example,
                # logging:
                #   distributed.worker: debug
                #   version: 1
                #   loggers:
                #     distributed.scheduler:
                #       level: DEBUG
                v0_debug_loggers = [
                    k for k, v in dask_log_config.items() if isinstance(v, str) and v.lower() == "debug"
                ]
                v1_debug_loggers = [
                    k
                    for k, v in dask_log_config.get("loggers", {}).items()
                    if isinstance(v, dict) and v.get("level") == "DEBUG"
                ]
                debug_loggers = [*v0_debug_loggers, *v1_debug_loggers]

                if debug_loggers:
                    if len(debug_loggers) > 1:
                        what_loggers = f"Dask loggers {debug_loggers} are"
                    else:
                        what_loggers = f"Dask logger {debug_loggers[0]!r} is"
                    logger.warning(
                        f"{what_loggers} configured to show DEBUG logs on your cluster.\n"
                        f"Debug logs can be very verbose, and there may be unexpected costs from your cloud provider "
                        f"for ingesting very large logs."
                    )

        # these are sets of names of workers, only including workers in states that might eventually reach
        # a "started" state
        # they're used in our implementation of scale up/down (mostly inherited from coiled.Cluster)
        # and their corresponding properties are used in adaptive scaling (at least once we
        # make adaptive work with Cluster).
        #
        # (Adaptive expects attributes `requested` and `plan`, which we implement as properties below.)
        #
        # Some good places to learn about adaptive:
        # https://github.com/dask/distributed/blob/39024291e429d983d7b73064c209701b68f41f71/distributed/deploy/adaptive_core.py#L31-L43
        # https://github.com/dask/distributed/issues/5080
        self._requested: Set[str] = set()
        self._plan: Set[str] = set()

        self.cluster_id: int | None = None
        self.use_scheduler_public_ip: bool = (
            dask.config.get("coiled.use_scheduler_public_ip", True)
            if use_scheduler_public_ip is None
            else use_scheduler_public_ip
        )
        self.use_dashboard_https: bool = (
            dask.config.get("coiled.use_dashboard_https", True) if use_dashboard_https is None else use_dashboard_https
        )
        self.dashboard_custom_subdomain = dashboard_custom_subdomain

        self.backend_options = backend_options

        scheduler_port = scheduler_port or dask.config.get("coiled.scheduler_port", None)

        custom_network_kwargs = {
            "allow_ingress_from": allow_ingress_from,
            "allow_ssh_from": allow_ssh_from,
            "allow_ssh": allow_ssh,
            "allow_spark": allow_spark,
            "scheduler_port": scheduler_port,
            "open_extra_ports": open_extra_ports,
        }
        used_network_kwargs = [name for name, val in custom_network_kwargs.items() if val is not None]
        if used_network_kwargs:
            if backend_options is not None and "ingress" in backend_options:
                friendly_list = " or ".join(f"`{kwarg}`" for kwarg in used_network_kwargs)
                raise ArgumentCombinationError(
                    f"You cannot use {friendly_list} when `ingress` is also specified in `backend_options`."
                )

            firewall_kwargs = {
                "target": allow_ingress_from or "everyone",
                "ssh": False if allow_ssh is None else allow_ssh,
                "ssh_target": allow_ssh_from,
                "spark": True if self.use_dashboard_https and allow_spark is None else bool(allow_spark),
                "extra_ports": open_extra_ports,
            }

            if scheduler_port is not None:
                firewall_kwargs["scheduler"] = scheduler_port
                self.scheduler_options["port"] = scheduler_port

            self.backend_options = self.backend_options or {}
            self.backend_options["ingress"] = cluster_firewall(**firewall_kwargs)["ingress"]  # type: ignore

        if jupyter:
            self.scheduler_options["jupyter"] = True

        if host_setup_script and os.path.exists(host_setup_script):
            with open(host_setup_script) as f:
                self.host_setup_script_content = f.read()
        else:
            self.host_setup_script_content = host_setup_script

        idle_timeout = idle_timeout or dask.config.get("distributed.scheduler.idle-timeout", None)
        if idle_timeout:
            dask.utils.parse_timedelta(idle_timeout)  # fail fast if dask can't parse this timedelta
            self.scheduler_options["idle_timeout"] = idle_timeout

        cluster_timeout = cluster_timeout or dask.config.get("coiled.cluster-timeout", None)
        self.cluster_timeout_seconds = int(dask.utils.parse_timedelta(cluster_timeout)) if cluster_timeout else None

        self.no_client_timeout = (
            no_client_timeout if no_client_timeout != NO_CLIENT_DEFAULT else (idle_timeout or "2 minutes")
        )

        if not self.asynchronous:
            # If we don't close the cluster, the user's ipython session gets spammed with
            # messages from distributed.
            #
            # Note that this doesn't solve all such spammy dead clusters (which is probably still
            # a problem), just spam created by clusters who failed initial creation.
            error = None
            try:
                self.sync(self._start)
                if self._is_coiled_hosted:
                    coiled_hosted_message = (
                        "[bold]Note[/]: You're currently using [bold][blue]Coiled-hosted[/blue][/bold], "
                        "a sandbox for running computations on our cloud infrastructure.\n"
                        "When you're ready to use Coiled in your own cloud provider account "
                        "(AWS, Azure, or Google Cloud), "
                        "you can run [green]coiled setup[/green] or visit "
                        f"[link]{self.cloud.server}/settings/setup[/link]"
                        "\n"
                    )
                    try:
                        self.custom_widget.console.print(f"\n{coiled_hosted_message}\n")  # type: ignore
                    except AttributeError:
                        rich_print(coiled_hosted_message)
            except (ClusterCreationError, InstanceTypeError, PermissionsError) as e:
                error = e
                self.close(reason=f"Failed to start cluster due to an exception: {tb.format_exc()}")
                if self.cluster_id:
                    log_cluster_debug_info(self.cluster_id, self.workspace)
                raise e.with_traceback(None)  # noqa: B904
            except KeyboardInterrupt as e:
                error = e
                if self.cluster_id is not None and self.shutdown_on_close in (
                    True,
                    None,
                ):
                    logger.warning(f"Received KeyboardInterrupt, deleting cluster {self.cluster_id}")
                    self.cloud.delete_cluster(
                        self.cluster_id,
                        workspace=self.workspace,
                        reason="User keyboard interrupt",
                    )
                raise
            except Exception as e:
                error = e
                self.close(reason=f"Failed to start cluster due to an exception: {tb.format_exc()}")
                raise e.with_traceback(truncate_traceback(e.__traceback__))  # noqa: B904
            finally:
                if error:
                    self.sync(
                        self.cloud.add_interaction,
                        "cluster-create",
                        success=False,
                        additional_data={
                            **error_info_for_tracking(error),
                            **self._as_json_compatible(),
                        },
                    )
                else:
                    self.sync(
                        self.cloud.add_interaction,
                        "cluster-create",
                        success=True,
                        additional_data={
                            **self._as_json_compatible(),
                        },
                    )
            if not error:
                if self.start_adaptive:
                    self.adapt(minimum=adaptive_min, maximum=adaptive_max)
                if mount_bucket:
                    self.mount_bucket(bucket=mount_bucket)

    @property
    def account(self):
        return self.workspace

    @property
    def details_url(self):
        """URL for cluster on the web UI at cloud.coiled.io."""
        return get_details_url(self.cloud.server, self.workspace, self.cluster_id)

    @property
    def _grafana_url(self) -> str | None:
        """for internal Coiled use"""
        if not self.cluster_id:
            return None

        details = self.cloud._get_cluster_details_synced(cluster_id=self.cluster_id, workspace=self.workspace)
        return get_grafana_url(details, account=self.workspace, cluster_id=self.cluster_id)

    def _ipython_display_(self: ClusterSyncAsync):
        widget = None
        from IPython.display import display

        if use_rich_widget():
            widget = RichClusterWidget(server=self.cloud.server, workspace=self.workspace)

        if widget and self.cluster_id:
            # TODO: These synchronous calls may be too slow. They can be done concurrently
            cluster_details = self.cloud._get_cluster_details_synced(
                cluster_id=self.cluster_id, workspace=self.workspace
            )
            if cluster_details.get("coiled_hosted"):
                self._is_coiled_hosted = True
            self.sync(self._update_cluster_status_logs, asynchronous=False)
            widget.update(cluster_details, self._cluster_status_logs)
            display(widget)

    def _repr_mimebundle_(self: ClusterSyncAsync, include: Iterable[str], exclude: Iterable[str], **kwargs):
        # In IPython 7.x This is called in an ipython terminal instead of
        # _ipython_display_ : https://github.com/ipython/ipython/pull/10249
        # In 8.x _ipython_display has been re-enabled in the terminal to
        # allow for rich outputs: https://github.com/ipython/ipython/pull/12315/files
        # So this function *should* only be calle  when in an ipython context using
        # IPython 7.x.
        cloud = self.cloud
        if use_rich_widget() and self.cluster_id:
            rich_widget = RichClusterWidget(server=self.cloud.server, workspace=self.workspace)
            cluster_details = cloud._get_cluster_details_synced(cluster_id=self.cluster_id, workspace=self.workspace)
            if cluster_details.get("coiled_hosted"):
                self._is_coiled_hosted = True
            self.sync(self._update_cluster_status_logs, asynchronous=False)
            rich_widget.update(cluster_details, self._cluster_status_logs)
            return rich_widget._repr_mimebundle_(include, exclude, **kwargs)
        else:
            return {"text/plain": repr(self)}

    @track_context
    async def _get_cluster_vm_types_to_use(self):
        cloud = self.cloud
        if (self.worker_cpu or self.worker_memory) and not self.worker_vm_types:
            # match worker types by cpu and/or memory
            worker_vm_types_to_use = get_instance_type_from_cpu_memory(
                self.worker_cpu,
                self.worker_memory,
                gpus=self.worker_gpu_count,
                backend=await self._get_account_cloud_provider_name(),
                arch=self.arch.vm_arch,
                recommended=True,
            )
        elif (self.worker_cpu or self.worker_memory) and self.worker_vm_types:
            raise ArgumentCombinationError(_vm_type_cpu_memory_error_msg.format(kind="worker"))
        else:
            # get default types from dask config
            if self.worker_vm_types is None:
                self.worker_vm_types = dask.config.get("coiled.worker.vm-types")
            # accept string or list of strings
            if isinstance(self.worker_vm_types, str):
                self.worker_vm_types = [self.worker_vm_types]
            validate_vm_typing(self.worker_vm_types)
            worker_vm_types_to_use = self.worker_vm_types

        if (self.scheduler_cpu or self.scheduler_memory) and not self.scheduler_vm_types:
            # match scheduler types by cpu and/or memory
            scheduler_vm_types_to_use = get_instance_type_from_cpu_memory(
                self.scheduler_cpu,
                self.scheduler_memory,
                gpus=1 if self.scheduler_gpu else 0,
                backend=await self._get_account_cloud_provider_name(),
                arch=self.arch.vm_arch,
                recommended=True,
            )
        elif (self.scheduler_cpu or self.scheduler_memory) and self.scheduler_vm_types:
            raise ArgumentCombinationError(_vm_type_cpu_memory_error_msg.format(kind="scheduler"))
        else:
            # get default types from dask config
            if self.scheduler_vm_types is None:
                self.scheduler_vm_types = dask.config.get("coiled.scheduler.vm_types")
            # accept string or list of strings
            if isinstance(self.scheduler_vm_types, str):
                self.scheduler_vm_types = [self.scheduler_vm_types]
            validate_vm_typing(self.scheduler_vm_types)
            scheduler_vm_types_to_use = self.scheduler_vm_types

        # If we still don't have instance types, use the defaults
        if not scheduler_vm_types_to_use or not worker_vm_types_to_use:
            provider = await self._get_account_cloud_provider_name()

            if not self.scheduler_gpu and not self.worker_gpu_count:
                # When no GPUs, use same default for scheduler and workers
                default_vm_types = await cloud._get_default_instance_types(
                    provider=provider,
                    gpu=False,
                    arch=self.arch.vm_arch,
                )
                scheduler_vm_types_to_use = scheduler_vm_types_to_use or default_vm_types
                worker_vm_types_to_use = worker_vm_types_to_use or default_vm_types
            else:
                # GPUs so there might be different defaults for scheduler/workers
                if not scheduler_vm_types_to_use:
                    scheduler_vm_types_to_use = get_instance_type_from_cpu_memory(
                        gpus=1 if self.scheduler_gpu else 0,
                        backend=await self._get_account_cloud_provider_name(),
                        arch=self.arch.vm_arch,
                        recommended=True,
                    )
                if not worker_vm_types_to_use:
                    worker_vm_types_to_use = get_instance_type_from_cpu_memory(
                        gpus=self.worker_gpu_count,
                        arch=self.arch.vm_arch,
                        recommended=True,
                    )
        return scheduler_vm_types_to_use, worker_vm_types_to_use

    @property
    def workspace_cloud_provider_name(self: ClusterSyncAsync):
        return self.sync(self._get_account_cloud_provider_name)

    @track_context
    async def _get_account_cloud_provider_name(self) -> str:
        if not hasattr(self, "_cached_account_cloud_provider_name"):
            self._cached_account_cloud_provider_name = await self.cloud.get_account_provider_name(
                account=self.workspace
            )

        return self._cached_account_cloud_provider_name

    @track_context
    async def _check_create_or_reuse(self):
        cloud = self.cloud
        if self.name:
            try:
                self.cluster_id = await cloud._get_cluster_by_name(
                    name=self.name,
                    workspace=self.workspace,
                )
            except DoesNotExist:
                should_create = True
            else:
                logger.info(f"Using existing cluster: '{self.name} (id: {self.cluster_id})'")
                should_create = False
        else:
            should_create = True
            self.name = self.name or (self.workspace or cloud.default_workspace) + "-" + short_random_string()
        return should_create

    async def _wait_for_custom_certificate(
        self,
        subdomain: str,
        started_at: datetime.datetime | None,
        workspace: str | None = None,
    ):
        # wait at most 2 minutes for cert to be ready
        started_at = started_at or datetime.datetime.now(tz=datetime.timezone.utc)
        timeout_at = started_at + datetime.timedelta(minutes=2)

        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
        )
        if self.show_widget and (self._force_rich_widget or use_rich_widget()):
            live = Live(Panel(progress, title="[green]Custom Dashboard Certificate", width=CONSOLE_WIDTH))
        else:
            live = contextlib.nullcontext()

        with live:
            initial_seconds_remaining = (timeout_at - datetime.datetime.now(tz=datetime.timezone.utc)).total_seconds()
            task = progress.add_task("Requesting certificate", total=initial_seconds_remaining)

            while True:
                seconds_remaining = (timeout_at - datetime.datetime.now(tz=datetime.timezone.utc)).total_seconds()
                progress.update(task, completed=initial_seconds_remaining - seconds_remaining)
                cert_status = await self.cloud._check_custom_certificate(subdomain=subdomain, workspace=workspace)

                if cert_status in ("ready", "continue"):
                    # "continue" is not currently used, but could be used if control-plane is changed
                    # so that it's not necessary to block while requesting certificate
                    progress.update(task, completed=initial_seconds_remaining)
                    return True

                if cert_status in ("in use", "error"):
                    raise ClusterCreationError(
                        f"Unable to provision the custom subdomain {subdomain!r}, status={cert_status}"
                    )

                for _ in range(6):
                    seconds_remaining = (timeout_at - datetime.datetime.now(tz=datetime.timezone.utc)).total_seconds()
                    if seconds_remaining <= 0:
                        raise ClusterCreationError(f"Timed out waiting for custom subdomain {subdomain!r}")
                    progress.update(task, completed=initial_seconds_remaining - seconds_remaining)
                    await asyncio.sleep(0.5)

    @track_context
    async def _package_sync_scan_and_create(
        self,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        gpu_enabled: bool = False,
    ) -> Tuple[int | None, str | None]:
        senv_name = None
        # For package sync, this is where we scrape local environment, determine
        # what to install on cluster, and build/upload wheels as needed.
        if self.package_sync:
            async with self._time_cluster_event("package sync", "scan and create") as package_sync_event:
                await self._get_account_cloud_provider_name()
                package_sync_env_alias = await scan_and_create(
                    cloud=self.cloud,
                    cluster=self,
                    region_name=self.backend_options.get("region_name") if self.backend_options else None,
                    architecture=architecture,
                    gpu_enabled=gpu_enabled,
                    workspace=self.workspace,
                    show_widget=self.show_widget,
                    package_sync_strict=self.package_sync_strict,
                    package_sync_only=self.package_sync_only,
                    package_sync_ignore=self.package_sync_ignore,
                    package_sync_conda_extras=self.package_sync_conda_extras,
                    package_sync_fail_on=self.package_sync_fail_on,
                    use_uv_installer=self._package_sync_use_uv_installer,
                    force_rich_widget=self._force_rich_widget,
                )
                package_sync_env = package_sync_env_alias["id"]
                senv_name = package_sync_env_alias["name"]
                package_sync_event["senv_id"] = package_sync_env
                package_sync_event["senv_name"] = senv_name

                logger.debug(f"Environment capture complete, {package_sync_env}")
        else:
            package_sync_env = None

        return package_sync_env, senv_name

    @track_context
    async def _attach_to_cluster(self, is_new_cluster: bool):
        assert self.cluster_id

        # this is what waits for the cluster to be "ready"
        await self._wait_until_ready(is_new_cluster)

        results = await asyncio.gather(*[
            self._set_plan_requested(),
            self.cloud._security(
                cluster_id=self.cluster_id,
                workspace=self.workspace,
                client_wants_public_ip=self.use_scheduler_public_ip,
            ),
        ])
        self.security, security_info = results[1]

        self._proxy = bool(self.security.extra_conn_args)
        self._dashboard_address = security_info["dashboard_address"]
        rpc_address = security_info["address_to_use"]

        try:
            self.scheduler_comm = dask.distributed.rpc(
                rpc_address,
                connection_args=self.security.get_connection_args("client"),
            )
            await self._send_credentials()
            if self.unset_single_threading_variables:
                await self._unset_env_vars(list(unset_single_thread_defaults().keys()))
            if self.shutdown_on_close and self.no_client_timeout:
                await self._set_keepalive(self.no_client_timeout)
        except OSError as e:
            if "Timed out" in str(e):
                raise RuntimeError(
                    "Unable to connect to Dask cluster. This may be due "
                    "to different versions of `dask` and `distributed` "
                    "locally and remotely.\n\n"
                    f"You are using distributed={DISTRIBUTED_VERSION} locally.\n\n"
                    "With pip, you can upgrade to the latest with:\n\n"
                    "\tpip install --upgrade dask distributed"
                ) from None
            raise

    @track_context
    async def _start(self):
        did_error = False
        cluster_created = False

        await self.cloud
        try:
            cloud = self.cloud
            self.workspace = self.workspace or self.cloud.default_workspace

            # check_create_or_reuse has the side effect of creating a name
            # if none is assigned
            should_try_create = await self._check_create_or_reuse()
            self.name = self.name or (self.workspace or cloud.default_workspace) + "-" + short_random_string()
            assert self.name

            if not should_try_create and self.batch_job_ids:
                raise RuntimeError(
                    f"Unable to add batch jobs to existing cluster {self.name!r}, "
                    f"please specify a cluster name that doesn't match currently running clusters."
                )

            # Set shutdown_on_close here instead of in __init__ to make sure
            # the dask config default isn't used when we are reusing a cluster
            if self.shutdown_on_close is None:
                self.shutdown_on_close = should_try_create and dask.config.get("coiled.shutdown-on-close")

            if should_try_create:
                (
                    scheduler_vm_types_to_use,
                    worker_vm_types_to_use,
                ) = await self._get_cluster_vm_types_to_use()

                user_provider = await self._get_account_cloud_provider_name()

                # Update backend options for cluster based on the friendlier kwargs
                if self.scheduler_gpu:
                    if user_provider == "gcp":
                        self.backend_options = {
                            **GCP_SCHEDULER_GPU,
                            **(self.backend_options or {}),
                        }
                if self.use_best_zone:
                    self.backend_options = {
                        **(self.backend_options or {}),
                        "multizone": True,
                    }
                if self.allow_cross_zone:
                    self.backend_options = {
                        **(self.backend_options or {}),
                        "multizone": True,
                        "multizone_allow_cross_zone": True,
                    }
                if self.spot_policy:
                    purchase_configs = {
                        "on-demand": {"spot": False},
                        "spot": {
                            "spot": True,
                            "spot_on_demand_fallback": False,
                        },
                        "spot_with_fallback": {
                            "spot": True,
                            "spot_on_demand_fallback": True,
                        },
                    }

                    if self.spot_policy not in purchase_configs:
                        valid_options = ", ".join(purchase_configs.keys())
                        raise ValueError(
                            f"{self.spot_policy} is not a valid spot_policy; valid options are: {valid_options}"
                        )

                    self.backend_options = {
                        **(self.backend_options or {}),
                        **purchase_configs[self.spot_policy],
                    }

                # Elsewhere (in _wait_until_ready) we actually decide how many workers to wait for,
                # in a way that's unified/correct for both the "should_create" case and the case
                # where a cluster already exists.
                #
                # However, we should check here to make sure _wait_for_workers_arg is valid to
                # avoid creating the cluster if it's not valid.
                #
                # (We can't do this check earlier because we don't know until now if we're
                # creating a cluster, and if we're not then "_start_n_workers" may be the wrong
                # number of workers...)
                parse_wait_for_workers(self._start_n_workers, self._wait_for_workers_arg)

                # Determine software environment (legacy or package sync)
                architecture = (
                    ArchitectureTypesEnum.ARM64
                    if (
                        (
                            user_provider == "aws"
                            and all(
                                re.search(r"^\w+\d.*g.*", vm_type.split(".")[0], flags=re.IGNORECASE)
                                for vm_type in chain(scheduler_vm_types_to_use, worker_vm_types_to_use)
                            )
                        )
                        or (
                            user_provider == "gcp"
                            and all(
                                vm_type.split("-")[0].lower() in ("t2a", "c4a")
                                for vm_type in chain(scheduler_vm_types_to_use, worker_vm_types_to_use)
                            )
                        )
                    )
                    else ArchitectureTypesEnum.X86_64
                )

                # `architecture` is set to ARM64 iff *all* instances are ARM,
                # so when architecture is X86_64 that could mean all instances are x86
                # or it could mean that there's a mix (which we want to reject).
                if architecture == ArchitectureTypesEnum.ARM64:
                    self.arch = ArchitectureTypesEnum.ARM64

                # This check ensures that if the user asked for ARM cluster (using the `arm` kwarg),
                # then they didn't also explicitly specify x86 instance type.
                # (It also catches if our code to pick ARM instances types returns an x86 instance type.)
                if architecture != self.arch:
                    # TODO (future PR) more specific error about which instance type doesn't match
                    raise RuntimeError(
                        f"Requested cluster architecture ({self.arch.vm_arch}) does not match "
                        f"architecture of some instance types ({scheduler_vm_types_to_use}, {worker_vm_types_to_use})."
                    )

                if self.arch.vm_arch != dask.config.get("coiled.software_requires_vm_arch", self.arch.vm_arch):
                    # specified senv with specified arch comes from `coiled run`
                    # we don't want to re-use senv if it was for a different arch than cluster we're now starting
                    self.package_sync = True
                    self.software_environment = ""

                reusing_existing_package_sync_env = self.software_environment == dask.config.get(
                    "coiled.software", None
                ) and (dask.config.get("coiled.software") or "").startswith("package-sync-")
                gpu_discrepancy = self._is_gpu_cluster != dask.config.get(
                    "coiled.software_is_gpu_cluster", self._is_gpu_cluster
                )
                if reusing_existing_package_sync_env and gpu_discrepancy:
                    # We reuse software environments from `coiled run` and `coiled batch run` when possible.
                    # We want to avoid reusing package sync envs when there's a GPU / CPU mismatch.
                    # We go in this `if`-block when:
                    #     1. No manual software environment was specified by the user (i.e. `software=`)
                    #     2. This cluster is being created from within an existing package sync env
                    #     3. There's a GPU/no-GPU mismatch between the existing package sync env and the
                    #        package sync environment being created here.
                    self.package_sync = True
                    self.software_environment = ""

                # create an ad hoc software environment if container was specified
                if self.software_container:
                    # make a valid software env name unique for this container
                    image_and_tag = self.software_container.split("/")[-1]
                    uri_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, self.software_container))
                    container_senv_name = re.sub(
                        r"[^A-Za-z0-9-_]", "_", f"{image_and_tag}-{self.arch}-{uri_uuid}"
                    ).lower()

                    await cloud._create_software_environment(
                        name=container_senv_name,
                        container=self.software_container,
                        workspace=self.workspace,
                        architecture=self.arch,
                        region_name=self.backend_options.get("region_name") if self.backend_options else None,
                        use_entrypoint=self.software_use_entrypoint,
                    )
                    self.software_environment = container_senv_name

                # Validate software environment name, setting `can_have_revision` to False since
                # we don't seem to be using this yet.
                if not self.package_sync:
                    try:
                        parse_identifier(
                            self.software_environment,
                            property_name="software_environment",
                            can_have_revision=False,
                        )
                    except ParseIdentifierError as e:
                        # one likely reason for invalid name format is if this looks like an image URL
                        # match on <foo>.<bar>/<name> to see if this looks vaguely like a URL
                        if re.search(r"\..*/", self.software_environment):
                            message = (
                                f"{e.message}\n\n"
                                f"If you meant to specify a container image, you should use "
                                f"`container={self.software_container!r}` instead of `software=...`"
                                f"to specify the image."
                            )
                            raise ParseIdentifierError(message) from None
                        raise

                custom_subdomain_t0 = None
                if self.dashboard_custom_subdomain:
                    # start process to provision custom certificate before we start package sync scan/create
                    custom_subdomain_t0 = datetime.datetime.now(tz=datetime.timezone.utc)
                    await cloud._create_custom_certificate(
                        workspace=self.workspace, subdomain=self.dashboard_custom_subdomain
                    )

                package_sync_senv_id, package_sync_senv_name = await self._package_sync_scan_and_create(
                    architecture=architecture, gpu_enabled=self._is_gpu_cluster
                )
                self._software_environment_name = package_sync_senv_name or self.software_environment

                if self.dashboard_custom_subdomain:
                    await self._wait_for_custom_certificate(
                        workspace=self.workspace,
                        subdomain=self.dashboard_custom_subdomain,
                        started_at=custom_subdomain_t0,
                    )

                self.cluster_id, cluster_existed = await cloud._create_cluster(
                    workspace=self.workspace,
                    name=self.name,
                    workers=self._start_n_workers,
                    software_environment=self.software_environment,
                    worker_class=self.worker_class,
                    worker_options=self.worker_options,
                    worker_disk_size=self.worker_disk_size,
                    worker_disk_throughput=self.worker_disk_throughput,
                    worker_disk_config=self.worker_disk_config,
                    gcp_worker_gpu_type=self.worker_gpu_type,
                    gcp_worker_gpu_count=self.worker_gpu_count,
                    scheduler_disk_size=self.scheduler_disk_size,
                    scheduler_disk_config=self.scheduler_disk_config,
                    scheduler_options=self.scheduler_options,
                    environ=self.environ,
                    tags=self.tags,
                    dask_config=self.frozen_dask_config,
                    scheduler_vm_types=scheduler_vm_types_to_use,
                    worker_vm_types=worker_vm_types_to_use,
                    backend_options=self.backend_options,
                    use_scheduler_public_ip=self.use_scheduler_public_ip,
                    use_dashboard_https=self.use_dashboard_https,
                    senv_v2_id=package_sync_senv_id,
                    private_to_creator=self.private_to_creator,
                    extra_worker_on_scheduler=self.extra_worker_on_scheduler,
                    n_worker_specs_per_host=self.n_worker_specs_per_host,
                    custom_subdomain=self.dashboard_custom_subdomain,
                    batch_job_ids=self.batch_job_ids,
                    extra_user_container=self.extra_user_container,
                    extra_user_container_ignore_entrypoint=self.extra_user_container_ignore_entrypoint,
                    host_setup_script_content=self.host_setup_script_content,
                    pause_on_exit=self.pause_on_exit,
                    cluster_timeout_seconds=self.cluster_timeout_seconds,
                )
                cluster_created = not cluster_existed

            if not self.cluster_id:
                raise RuntimeError(f"Failed to find/create cluster {self.name}")

            if cluster_created:
                if self.start_adaptive and self._original_n_workers is None:
                    logger.warning(
                        "Using adaptive scaling with default range of "
                        f"`[{DEFAULT_ADAPTIVE_MIN}, {DEFAULT_ADAPTIVE_MAX}]`. "
                        "To manually control the size of your cluster, use n_workers=.\n"
                    )
                logger.info(
                    f"Creating Cluster (name: {self.name}, {self.details_url} ). This usually takes 1-2 minutes..."
                )
            else:
                logger.info(f"Attaching to existing cluster (name: {self.name}, {self.details_url} )")

            # while cluster is "running", check state according to Coiled every 1s
            self._state_check_failed = 0
            self.periodic_callbacks["check_coiled_state"] = PeriodicCallback(
                self._check_status,
                dask.utils.parse_timedelta(dask.config.get("coiled.cluster-state-check-interval")) * 1000,  # type: ignore
            )

            # slightly hacky way to make cluster creation not block if this is a batch job cluster
            if self.batch_job_ids:
                cluster_details = await cloud._get_cluster_details(cluster_id=self.cluster_id, workspace=self.workspace)
                if cluster_details.get("coiled_hosted"):
                    self._is_coiled_hosted = True
            else:
                await self._attach_to_cluster(is_new_cluster=cluster_created)
                await super()._start()

        except Exception as e:
            if self._asynchronous:
                did_error = True
                asyncio.create_task(
                    self.cloud.add_interaction(
                        "cluster-create",
                        success=False,
                        additional_data={
                            **error_info_for_tracking(e),
                            **self._as_json_compatible(),
                        },
                    )
                )
            raise
        finally:
            if self._asynchronous and not did_error:
                asyncio.create_task(
                    self.cloud.add_interaction(
                        "cluster-create",
                        success=True,
                        additional_data={
                            **self._as_json_compatible(),
                        },
                    )
                )

    def _as_json_compatible(self):
        # the typecasting here is to avoid accidentally
        # submitting something passed in that is not json serializable
        # (user error may cause this)
        return {
            "name": str(self.name),
            "software_environment": str(self.software_environment),
            "show_widget": bool(self.show_widget),
            "async": bool(self._asynchronous),
            "worker_class": str(self.worker_class),
            "worker_cpu": str(self.worker_cpu),
            "worker_memory": str(self.worker_memory),
            "worker_vm_types": str(self.worker_vm_types),
            "worker_gpu_count": str(self.worker_gpu_count),
            "worker_gpu_type": str(self.worker_gpu_type),
            "scheduler_memory": str(self.scheduler_memory),
            "scheduler_vm_types": str(self.scheduler_vm_types),
            "n_workers": int(self._start_n_workers),
            "shutdown_on_close": bool(self.shutdown_on_close),
            "use_scheduler_public_ip": bool(self.use_scheduler_public_ip),
            "use_dashboard_https": bool(self.use_dashboard_https),
            "package_sync": bool(self.package_sync),
            "package_sync_fail_on": bool(self.package_sync_fail_on),
            "package_sync_ignore": str(self.package_sync_ignore) if self.package_sync_ignore else False,
            "execution_context": EXECUTION_CONTEXT,
            "account": self.workspace,
            "timeout": self.timeout,
            "wait_for_workers": self._wait_for_workers_arg,
            "cluster_id": self.cluster_id,
            "backend_options": self.backend_options,
            "scheduler_gpu": self.scheduler_gpu,
            "use_best_zone": self.use_best_zone,
            "spot_policy": self.spot_policy,
            "start_adaptive": self.start_adaptive,
            "errored_worker_count": self.errored_worker_count,
            # NOTE: this is not a measure of the CLUSTER life time
            # just a measure of how long this object has been around
            "cluster_object_life": str(datetime.datetime.now(tz=datetime.timezone.utc) - self.init_time),
        }

    def _maybe_log_summary(self, cluster_details):
        now = time.time()
        if self._last_logged_state_summary is None or now > self._last_logged_state_summary + 5:
            logger.debug(summarize_status(cluster_details))
            self._last_logged_state_summary = now

    @track_context
    async def _wait_until_ready(self, is_new_cluster: bool) -> None:
        cloud = self.cloud
        cluster_id = self._assert_cluster_id()
        await self._flush_cluster_events()
        timeout_at = (
            datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=self.timeout)
            if self.timeout is not None
            else None
        )
        self._latest_dt_seen = None

        if self.custom_widget:
            widget = self.custom_widget
            ctx = contextlib.nullcontext()
        elif self.show_widget and (self._force_rich_widget or use_rich_widget()):
            widget = RichClusterWidget(
                n_workers=self._start_n_workers,
                server=self.cloud.server,
                workspace=self.workspace,
            )
            ctx = widget
        else:
            widget = None
            ctx = contextlib.nullcontext()

        num_workers_to_wait_for = None
        with ctx:
            while True:
                cluster_details = await cloud._get_cluster_details(cluster_id=cluster_id, workspace=self.workspace)

                if cluster_details.get("coiled_hosted"):
                    self._is_coiled_hosted = True

                # Computing num_workers_to_wait_for inside the while loop is kinda goofy, but I don't want to add an
                # extra _get_cluster_details call right now since that endpoint can be very slow for big clusters.
                # Let's optimize it, and then move this code up outside the loop.
                if num_workers_to_wait_for is None:
                    cluster_desired_workers = cluster_details["desired_workers"]
                    num_workers_to_wait_for = parse_wait_for_workers(
                        cluster_desired_workers, self._wait_for_workers_arg
                    )
                    if not is_new_cluster:
                        if self.start_adaptive:
                            # When re-attaching to existing cluster without specifying n_workers,
                            # we don't want to start adaptive (which we'd do otherwise when n_workers isn't specified)
                            # and we also don't want to show message that we're ignoring n_workers (since in this case
                            # it was set as default because n_workers was unspecified).
                            self.start_adaptive = False
                        elif self._start_n_workers != cluster_desired_workers:
                            logger.warning(
                                f"Ignoring your request for {self._start_n_workers} workers since you are "
                                f"connecting to a cluster that had been requested with {cluster_desired_workers} "
                                "workers"
                            )

                await self._update_cluster_status_logs()
                self._maybe_log_summary(cluster_details)

                if widget:
                    widget.update(
                        cluster_details,
                        self._cluster_status_logs,
                    )

                cluster_state = ClusterStateEnum(cluster_details["current_state"]["state"])
                reason = cluster_details["current_state"]["reason"]

                scheduler_current_state = cluster_details["scheduler"]["current_state"]
                scheduler_state = ProcessStateEnum(scheduler_current_state["state"])
                if cluster_details["scheduler"].get("instance"):
                    scheduler_instance_state = InstanceStateEnum(
                        cluster_details["scheduler"]["instance"]["current_state"]["state"]
                    )
                else:
                    scheduler_instance_state = InstanceStateEnum.queued
                worker_current_states = [w["current_state"] for w in cluster_details["workers"]]
                ready_worker_current = [
                    current
                    for current in worker_current_states
                    if ProcessStateEnum(current["state"]) == ProcessStateEnum.started
                ]
                self.errored_worker_count = sum([
                    1
                    for current in worker_current_states
                    if ProcessStateEnum(current["state"]) == ProcessStateEnum.error
                ])
                starting_workers = sum([
                    1
                    for current in worker_current_states
                    if ProcessStateEnum(current["state"])
                    in [
                        ProcessStateEnum.starting,
                        ProcessStateEnum.pending,
                    ]
                ])

                if scheduler_state == ProcessStateEnum.started and scheduler_instance_state in [
                    InstanceStateEnum.ready,
                    InstanceStateEnum.started,
                ]:
                    scheduler_ready = True
                    scheduler_reason_not_ready = ""
                else:
                    scheduler_ready = False
                    scheduler_reason_not_ready = "Scheduler not ready."

                n_workers_ready = len(ready_worker_current)

                final_update = None
                if n_workers_ready >= num_workers_to_wait_for:
                    if n_workers_ready == self._start_n_workers:
                        final_update = "All workers ready."
                    else:
                        final_update = "Most of your workers have arrived. Cluster ready for use."

                    enough_workers_ready = True
                    workers_reason_not_ready = ""
                else:
                    enough_workers_ready = False
                    workers_reason_not_ready = (
                        f"Only {len(ready_worker_current)} workers ready "
                        f"(was waiting for at least {num_workers_to_wait_for}). "
                    )

                # Check if cluster is ready to return to user in a good state
                if scheduler_ready and enough_workers_ready:
                    assert final_update is not None
                    if widget:
                        widget.update(
                            cluster_details,
                            self._cluster_status_logs,
                            final_update=final_update,
                        )
                    logger.debug(summarize_status(cluster_details))
                    return
                else:
                    reason_not_ready = scheduler_reason_not_ready if not scheduler_ready else workers_reason_not_ready
                    if cluster_state in (
                        ClusterStateEnum.error,
                        ClusterStateEnum.paused,
                        ClusterStateEnum.pausing,
                        ClusterStateEnum.stopped,
                        ClusterStateEnum.stopping,
                    ):
                        # this cluster will never become ready; raise an exception
                        error = f"Cluster status is {cluster_state.value} (reason: {reason})"
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=error,
                            )
                        logger.debug(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            error,
                            cluster_id=self.cluster_id,
                        )
                    elif cluster_state == ClusterStateEnum.ready:
                        # (cluster state "ready" means all worked either started or errored, so
                        # this cluster will never have all the workers we want)
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=reason_not_ready,
                            )
                        logger.debug(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            reason_not_ready,
                            cluster_id=self.cluster_id,
                        )
                    elif (starting_workers + n_workers_ready) < num_workers_to_wait_for:
                        # including workers that are starting, cluster cannot get to the number
                        # of desired ready workers (because some workers have already errored),
                        logger.debug(summarize_status(cluster_details))

                        message = (
                            f"Cluster was waiting for {num_workers_to_wait_for} workers but "
                            f"{self.errored_worker_count} (of {self._start_n_workers}) workers have already failed. "
                            "You could try requesting fewer workers or adjust `wait_for_workers` if fewer workers "
                            "would be acceptable."
                        )
                        errors = group_worker_errors(cluster_details)
                        if errors:
                            header = "Failure Reasons\n---------------"
                            message = f"{message}\n\n{header}"
                            # show error that affected the most workers first
                            for error in sorted(errors, key=lambda k: -errors[k]):
                                n_affected = errors[error]
                                plural = "" if n_affected == 1 else "s"
                                error_message = f"{error}\n\t(error affected {n_affected} worker{plural})"
                                message = f"{message}\n\n{error_message}"

                        raise ClusterCreationError(
                            message,
                            cluster_id=self.cluster_id,
                        )
                    elif timeout_at is not None and datetime.datetime.now(tz=datetime.timezone.utc) > timeout_at:
                        error = "User-specified timeout expired: " + reason_not_ready
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=error,
                            )
                        logger.debug(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            error,
                            cluster_id=self.cluster_id,
                        )

                    else:
                        await asyncio.sleep(1.0)

    async def _update_cluster_status_logs(self):
        cluster_id = self._assert_cluster_id()
        states_by_type = await self.cloud._get_cluster_states_declarative(
            cluster_id, self.workspace, start_time=self._latest_dt_seen
        )
        states = flatten_log_states(states_by_type)
        if states:
            if not self.custom_widget and (not self.show_widget or EXECUTION_CONTEXT == "terminal"):
                log_states(states)
            self._latest_dt_seen = states[-1].updated
            self._cluster_status_logs.extend(states)

    def _assert_cluster_id(self) -> int:
        if self.cluster_id is None:
            raise RuntimeError("'cluster_id' is not set, perhaps the cluster hasn't been created yet")
        return self.cluster_id

    def cwi_logs_url(self):
        if self.cluster_id is None:
            raise ValueError("cluster_id is None. Cannot get CloudWatch link without a cluster")

        # kinda hacky, probably something as important as region ought to be an attribute on the
        # cluster itself already and not require an API call
        cluster_details = self.cloud._get_cluster_details_synced(cluster_id=self.cluster_id, workspace=self.workspace)
        if cluster_details["backend_type"] != "vm_aws":
            raise ValueError("Sorry, the cwi_logs_url only works for AWS clusters.")
        region = cluster_details["cluster_options"]["region_name"]

        return cloudwatch_url(self.workspace, self.name, region)

    def details(self):
        if self.cluster_id is None:
            raise ValueError("cluster_id is None. Cannot get details without a cluster")
        return self.cloud.cluster_details(cluster_id=self.cluster_id, workspace=self.workspace)

    async def _set_plan_requested(self):
        eventually_maybe_good_statuses = [
            ProcessStateEnum.starting,
            ProcessStateEnum.pending,
            ProcessStateEnum.started,
        ]
        assert self.workspace
        assert self.cluster_id
        eventually_maybe_good_workers = await self.cloud._get_worker_names(
            workspace=self.workspace,
            cluster_id=self.cluster_id,
            statuses=eventually_maybe_good_statuses,
        )

        # scale (including adaptive) relies on `plan` and `requested` and these (on Coiled)
        # are set based on the control-plane's view of what workers there are, so if we have
        # extra worker on the scheduler (which isn't tracked separately by control-plane)
        # we need to include that here.
        if self.extra_worker_on_scheduler:
            # get the actual name of worker on scheduler if we haven't gotten it yet
            if not self._worker_on_scheduler_name:
                worker_on_scheduler = [worker for worker in self.observed if "scheduler" in worker]
                if worker_on_scheduler:
                    self._worker_on_scheduler_name = worker_on_scheduler[0]
            # if we have actual name, use it, otherwise use fake name for now
            if self._worker_on_scheduler_name:
                eventually_maybe_good_workers.add(self._worker_on_scheduler_name)
            else:
                eventually_maybe_good_workers.add("extra-worker-on-scheduler")

        self._plan = eventually_maybe_good_workers
        self._requested = eventually_maybe_good_workers

    @track_context
    async def _scale(self, n: int, force_stop: bool = True) -> None:
        if not self.cluster_id:
            raise ValueError("No cluster available to scale!")

        await self._submit_cluster_event(
            "scaling",
            f"scale to {n} workers requested",
            extra_data={
                "force_stop": force_stop,
                "n_workers": n,
            },
            level=logging.INFO,
        )

        # Adaptive directly calls `scale_up` and `scale_down`, so if `scale(n)` is called, it means this came from user;
        # when user explicitly specified cluster size, it makes sense to turn off adaptive scaling.
        if getattr(self, "_adaptive", None) is not None:
            assert self._adaptive  # for pyright
            if self._adaptive.periodic_callback:
                logger.warning(
                    f"Turning off adaptive scaling because `scale(n={n})` was explicitly called.\n"
                    f"To resume adaptive scaling, you can use the `adapt(minimum=..., maximum=...)` method."
                )
                await self._submit_cluster_event("adaptive", "disabled", level=logging.INFO)
            self._adaptive.stop()

        await self._set_plan_requested()  # need to update our understanding of current workers before scaling
        logger.debug(f"current _plan: {self._plan}")

        recommendations = await self.recommendations(n)
        logger.debug(f"scale recommendations: {recommendations}")

        return await self._apply_scaling_recommendations(recommendations, force_stop=force_stop)

    @track_context
    async def scale_up(self, n: int, reason: str | None = None) -> None:
        """
        Scales up *to* a target number of ``n`` workers

        It's documented that scale_up should scale up to a certain target, not scale up BY a certain amount:

        https://github.com/dask/distributed/blob/main/distributed/deploy/adaptive_core.py#L60
        """
        if not self.cluster_id:
            raise ValueError("No cluster available to scale! Check cluster was not closed by another process.")
        n_to_add = n - len(self.plan)

        await self._submit_cluster_event(
            "scaling",
            f"scale up to {n} workers requested",
            extra_data={
                "target": n,
                "n_to_add": n_to_add,
                "reason": reason,
            },
        )

        response = await self.cloud._scale_up(
            workspace=self.workspace,
            cluster_id=self.cluster_id,
            n=n_to_add,
            reason=reason,
        )
        if response:
            self._plan.update(set(response.get("workers", [])))
            self._requested.update(set(response.get("workers", [])))

    @track_context
    async def _close(self, force_shutdown: bool = False, reason: str | None = None) -> None:
        # My small changes to _close probably make sense for legacy Cluster too, but I don't want to carefully
        # test them, so copying this method over.

        await self._flush_cluster_events()

        with suppress(AttributeError):
            self._adaptive.stop()  # type: ignore

        # Stop here because otherwise we get intermittent `OSError: Timed out` when
        # deleting cluster takes a while and callback tries to poll cluster status.
        for pc in self.periodic_callbacks.values():
            pc.stop()

        if hasattr(self, "cluster_id") and self.cluster_id:
            # If the initial create call failed, we don't have a cluster ID.
            # But the rest of this method (at least calling distributed.deploy.Cluster.close)
            # is important.
            if force_shutdown or self.shutdown_on_close in (True, None):
                await self.cloud._delete_cluster(
                    workspace=self.workspace,
                    cluster_id=self.cluster_id,
                    reason=reason,
                )
        await super()._close()

    @property
    def requested(self):
        return self._requested

    @property
    def plan(self):
        return self._plan

    @overload
    def sync(
        self: Cluster[Sync],
        func: Callable[..., Awaitable[_T]],
        *args,
        asynchronous: Union[Sync, Literal[None]] = None,
        callback_timeout=None,
        **kwargs,
    ) -> _T: ...

    @overload
    def sync(
        self: Cluster[Async],
        func: Callable[..., Awaitable[_T]],
        *args,
        asynchronous: Union[bool, Literal[None]] = None,
        callback_timeout=None,
        **kwargs,
    ) -> Coroutine[Any, Any, _T]: ...

    def sync(
        self,
        func: Callable[..., Awaitable[_T]],
        *args,
        asynchronous: bool | None = None,
        callback_timeout=None,
        **kwargs,
    ) -> Union[_T, Coroutine[Any, Any, _T]]:
        return cast(
            Union[_T, Coroutine[Any, Any, _T]],
            super().sync(
                func,
                *args,
                asynchronous=asynchronous,
                callback_timeout=callback_timeout,
                **kwargs,
            ),
        )

    def _ensure_scheduler_comm(self) -> dask.distributed.rpc:
        """
        Guard to make sure that the scheduler comm exists before trying to use it.
        """
        if not self.scheduler_comm:
            raise RuntimeError("Scheduler comm is not set, have you been disconnected from Coiled?")
        return self.scheduler_comm

    @track_context
    async def _wait_for_workers(
        self,
        n_workers,
        timeout=None,
        err_msg=None,
    ) -> None:
        # `distributed.Client.wait_for_workers` uses `wait_for_workers` method on cluster if there is one
        # so this is the code that gets used
        def running_workers(info):
            return len([ws for ws in info["workers"].values() if ws["status"] == Status.running.name])

        if timeout is None:
            deadline = None
        else:
            timeout = dask.utils.parse_timedelta(timeout, "s")
            deadline = time.time() + timeout if timeout else None

        scheduler_comm = self._ensure_scheduler_comm()

        self.scheduler_info = cast(SchedulerInfo, await scheduler_comm.identity())
        while n_workers and running_workers(self.scheduler_info) < n_workers:
            if deadline and time.time() > deadline:
                err_msg = err_msg or f"Timed out after {timeout} seconds waiting for {n_workers} workers to arrive"
                raise TimeoutError(err_msg)
            await asyncio.sleep(1)
            self.scheduler_info = cast(SchedulerInfo, await scheduler_comm.identity())

    @staticmethod
    def _get_aws_default_region() -> str | None:
        try:
            from boto3.session import Session

            region_name = Session().region_name
            return str(region_name) if region_name else None
        except Exception:
            pass
        return None

    async def _get_aws_local_session_token(
        self,
        duration_seconds: int | None = None,
    ) -> AWSSessionCredentials:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, get_aws_local_session_token, duration_seconds)

    def _has_gcp_auth_installed(self) -> bool:
        try:
            import google.auth  # type: ignore # noqa F401
            from google.auth.transport.requests import Request  # type: ignore # noqa F401

            return True
        except ImportError:
            self._try_local_gcp_creds = False
            return False

    def set_keepalive(self: ClusterSyncAsync, keepalive):
        """
        Set how long to keep cluster running if all the clients have disconnected.

        This is a way to shut down no-longer-used cluster, in additional to dask idle timeout.
        With no keepalive set, cluster will not shut down on account of clients going away.

        Arguments:
            keepalive: duration string like "30s" or "5m"
        """
        return self.sync(self._set_keepalive, keepalive)

    async def _set_keepalive(self, keepalive, retries=5):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await scheduler_comm.coiled_set_keepalive(keepalive=keepalive)
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # using the scheduler comm sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._set_keepalive(keepalive=keepalive, retries=retries - 1)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error setting keepalive on cluster: {e}")

    def _call_scheduler_comm(self: ClusterSyncAsync, function: str, **kwargs):
        return self.sync(self._call_scheduler_comm_async, function, **kwargs)

    async def _call_scheduler_comm_async(self, function: str, retries=5, **kwargs):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await getattr(scheduler_comm, function)(**kwargs)
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # sending credentials sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._call_scheduler_comm_async(function=function, retries=retries - 1, **kwargs)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error calling {function} on scheduler comm: {e}")

    def send_private_envs(self: ClusterSyncAsync, env: dict):
        """
        Send potentially private environment variables to be set on scheduler and all workers.

        You can use this to send secrets (passwords, auth tokens) that you can use in code running on cluster.
        Unlike environment variables set with ``coiled.Cluster(environ=...)``, the values will be transmitted
        directly to your cluster without being transmitted to Coiled, logged, or written to disk.

        The Dask scheduler will ensure that these environment variables are set on any new workers you add to the
        cluster.
        """
        return self.sync(self._send_env_vars, env)

    async def _send_env_vars(self, env: dict, retries=5):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await scheduler_comm.coiled_update_env_vars(env=env)
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # sending credentials sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._send_env_vars(env, retries=retries - 1)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error sending environment variables to cluster: {e}")

    def unset_env_vars(self: ClusterSyncAsync, unset: Iterable[str]):
        return self.sync(self._unset_env_vars, list(unset))

    async def _unset_env_vars(self, unset: Iterable[str], retries=5):
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            await scheduler_comm.coiled_unset_env_vars(unset=list(unset))
        except Exception as e:
            if self.status not in TERMINATING_STATES:
                # sending credentials sometimes fails on a poor internet connection
                # so try a few times before giving up and showing warning
                if retries > 0:
                    await self._unset_env_vars(unset, retries=retries - 1)
                else:
                    # no more retries!
                    # warn, but don't crash
                    logger.warning(f"error unsetting environment variables on cluster: {e}")

    def send_credentials(self: ClusterSyncAsync, automatic_refresh: bool = False):
        """
        Manually trigger sending STS token to cluster.

        Usually STS token is automatically sent and refreshed by default, this allows
        you to manually force a refresh in case that's needed for any reason.
        """
        return self.sync(self._send_credentials, schedule_callback=automatic_refresh)

    def _schedule_cred_update(self, expiration: datetime.datetime | None, label: str, extra_warning: str = ""):
        """Schedule callback for updating credentials before they expire"""
        if self.status in TERMINATING_STATES:
            return

        # default to updating every 45 minutes
        delay = 45 * 60

        if expiration:
            diff = expiration - datetime.datetime.now(tz=datetime.timezone.utc)
            delay = int((diff * 0.5).total_seconds())

            if diff < datetime.timedelta(minutes=5):
                # usually the existing STS token will be from a role assumption and
                # will expire in ~1 hour, but just in case the local session has a very
                # short lived token, let the user know
                # TODO give user information about what to do in this case
                logger.warning(f"Locally generated {label} expires in less than 5 minutes ({diff}).{extra_warning}")

            # don't try to update sooner than in 1 minute
            delay = max(60, delay)

        elif self._credentials_duration_seconds and self._credentials_duration_seconds < 900:
            # 15 minutes is min duration for STS token, but if shorter duration explicitly
            # requested, then we'll update as if that were the duration (with lower bound of 5s).
            delay = max(5, int(self._credentials_duration_seconds * 0.5))

        # should never be None but distributed baseclass claims it can be
        if self.loop:
            now = self.loop.time()
            at = now + delay
            if (
                self._credentials_refresh_at is not None
                and self._credentials_refresh_at > now
                and self._credentials_refresh_at < at
            ):
                return
            handle = self.loop.call_at(when=at, callback=self._send_credentials)
            if self._credentials_refresh_handle is not None:
                self.loop.remove_timeout(self._credentials_refresh_handle)
            self._credentials_refresh_handle = handle
            self._credentials_refresh_at = at
            self._queue_cluster_event("credentials", f"refresh scheduled in {delay} seconds")
            logger.debug(f"{label} from local credentials shipped to cluster, planning to refresh in {delay} seconds")

    async def _send_aws_credentials(self, schedule_callback: bool):
        # AWS STS token
        token_creds = await self._get_aws_local_session_token(duration_seconds=self._credentials_duration_seconds)

        if not token_creds:
            await self._submit_cluster_event(
                "credential", "not forwarding AWS credentials, could not retrieve local credentials", level=logging.INFO
            )
        elif not token_creds.get("SessionToken"):
            await self._submit_cluster_event(
                "credentials", "not forwarding AWS credentials, no local session token", level=logging.INFO
            )

        if token_creds and token_creds.get("SessionToken"):
            scheduler_comm = self._ensure_scheduler_comm()

            keys = [
                "AccessKeyId",
                "SecretAccessKey",
                "SessionToken",
                "DefaultRegion",
            ]

            # creds endpoint will be used iff expiration is sent to plugin
            # so this is a way to (for now) feature flag using creds endpoint (vs. env vars)
            if dask.config.get("coiled.use_aws_creds_endpoint", False):
                keys.append("Expiration")

            def _format_vals(k: str) -> str | None:
                if k == "Expiration" and isinstance(token_creds.get("Expiration"), datetime.datetime):
                    # use assert to make pyright happy since it doesn't understand that the above conditional
                    # already ensures that token_creds["Expiration"] is not None
                    assert token_creds["Expiration"] is not None
                    # Format of datetime from the IMDS endpoint is `2024-03-10T05:24:34Z`, so match that.
                    # Python SDK is more flexible about what it accepts (e.g., it accepts isoformat)
                    # but some other code is stricter in parsing datetime string.
                    return token_creds["Expiration"].astimezone(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                # values should be str | None; make sure we don't use "None"
                return str(token_creds.get(k)) if token_creds.get(k) is not None else None

            creds_to_send = {k: _format_vals(k) for k in keys}
            await self._submit_cluster_event(
                "credentials",
                "forwarding AWS credentials",
                extra_data={"expiration": str(token_creds.get("Expiration"))},
            )
            await scheduler_comm.aws_update_credentials(credentials=creds_to_send)

            if creds_to_send.get("Expiration"):
                self._using_aws_creds_endpoint = True

            if schedule_callback:
                self._schedule_cred_update(
                    expiration=token_creds.get("Expiration"),
                    label="AWS STS token",
                    extra_warning=(
                        " Code running on your cluster may be unable to access other AWS services "
                        "(e.g, S3) when this token expires."
                    ),
                )
            else:
                logger.debug("AWS STS token from local credentials shipped to cluster, no scheduled refresh")
        elif dask.config.get("coiled.use_aws_creds_endpoint", False):
            # since we aren't shipping local creds, remove creds endpoint in credential chain
            await self._unset_env_vars(["AWS_CONTAINER_CREDENTIALS_FULL_URI"])

    async def _send_gcp_credentials(self, schedule_callback: bool):
        # Google Cloud OAuth2 token
        has_gcp_auth_installed = self._has_gcp_auth_installed()

        if self._try_local_gcp_creds and not has_gcp_auth_installed:
            await self._submit_cluster_event(
                "credentials",
                "not forwarding Google credentials, Google Python libraries not found",
            )

        if self._try_local_gcp_creds and has_gcp_auth_installed:
            gcp_token = get_gcp_local_session_token(set_local_token_env=True)

            if gcp_token.get("token"):
                await self._submit_cluster_event(
                    "credentials",
                    "forwarding Google credentials",
                    extra_data={"expiration": str(gcp_token.get("expiry"))},
                )

                # ship token to cluster
                await self._send_env_vars({"CLOUDSDK_AUTH_ACCESS_TOKEN": gcp_token["token"]})

                if gcp_token.get("expiry") and schedule_callback:
                    self._schedule_cred_update(expiration=gcp_token.get("expiry"), label="Google Cloud OAuth2 token")
                else:
                    logger.debug(
                        "Google Cloud OAuth2 token from local credentials shipped to cluster, no scheduled refresh"
                    )
            else:
                await self._submit_cluster_event(
                    "credentials", "not forwarding Google credentials, unable to get local token", level=logging.INFO
                )
                self._try_local_gcp_creds = False

    async def _send_credentials(self, schedule_callback: bool = True, retries=5):
        """
        Get credentials and pass them to the scheduler.
        """
        if self.credentials is CredentialsPreferred.NONE and dask.config.get("coiled.use_aws_creds_endpoint", False):
            await self._unset_env_vars(["AWS_CONTAINER_CREDENTIALS_FULL_URI"])

        if self.credentials is CredentialsPreferred.NONE:
            await self._submit_cluster_event(
                "credentials", "forwarding disabled by `credentials` kwarg", level=logging.INFO
            )

        if self.credentials is not CredentialsPreferred.NONE:
            try:
                if self.credentials is CredentialsPreferred.ACCOUNT:
                    # cloud.get_aws_credentials doesn't return credentials for currently implemented backends
                    # aws_creds = await cloud.get_aws_credentials(self.workspace)
                    logger.warning(
                        "Using account backend AWS credentials is not currently supported, "
                        "local AWS credentials (if present) will be used."
                    )

                # Concurrently handle AWS and GCP creds
                await asyncio.gather(*[
                    self._send_aws_credentials(schedule_callback),
                    self._send_gcp_credentials(schedule_callback),
                ])

            except Exception as e:
                if self.status not in TERMINATING_STATES:
                    # sending credentials sometimes fails on a poor internet connection
                    # so try a few times before giving up and showing warning
                    if retries > 0:
                        await self._send_credentials(schedule_callback, retries=retries - 1)
                    else:
                        # no more retries!
                        # warn, but don't crash
                        logger.warning(f"error sending local AWS or Google Cloud credentials to cluster: {e}")
                        await self._submit_cluster_event(
                            "credentials", f"error sending local credentials to cluster: {e}", level=logging.ERROR
                        )

    def __await__(self: Cluster[Async]):
        async def _():
            if self._lock is None:
                self._lock = asyncio.Lock()
            async with self._lock:
                if self.status == Status.created:
                    await wait_for(self._start(), self.timeout)
                assert self.status == Status.running
            return self

        return _().__await__()

    def _queue_cluster_event(
        self, topic, message, *, level: int = logging.DEBUG, extra_data=None, duration: float | None = None
    ):
        payload = {
            "topic": topic,
            "message": message,
            "timestamp": datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
            "extra_data": {**extra_data} if extra_data else None,
            "duration": duration,
            "level": level,
        }
        self._cluster_event_queue.append(payload)

    async def _flush_cluster_events(self):
        # any events prior to cluster having an ID get queued and sent once there's an event when cluster has ID
        if self.cluster_id and dask.config.get("coiled.send_client_events", True):
            url = f"{self.cloud.server}/api/v2/clusters/id/{self.cluster_id}/event"
            while self._cluster_event_queue:
                payload = self._cluster_event_queue.pop(0)
                try:
                    await self.cloud._do_request("POST", url, json=payload)
                except Exception as e:
                    logger.debug("Failed to send client event to control-plane", exc_info=e)

    async def _submit_cluster_event(
        self, topic, message, *, level: int = logging.DEBUG, extra_data=None, duration: float | None = None
    ):
        self._queue_cluster_event(topic, message, level=level, extra_data=extra_data, duration=duration)
        await self._flush_cluster_events()

    @contextlib.asynccontextmanager
    async def _time_cluster_event(self, topic, action, *, extra_data=None):
        extra_data = {**(extra_data or {})}
        await self._submit_cluster_event(topic, f"{action} started")
        t0 = time.monotonic()
        yield extra_data
        t1 = time.monotonic()

        await self._submit_cluster_event(topic, f"{action} finished", extra_data=extra_data, duration=t1 - t0)

    async def _check_status(self):
        if self.cluster_id and self.status in (Status.running, Status.closing):
            try:
                state = (await self.cloud._get_cluster_state(cluster_id=self.cluster_id, workspace=self.workspace)).get(
                    "state"
                )
                if state == "stopping":
                    self.status = Status.closing
                elif state in ("stopped", "error"):
                    self.status = Status.closed
                self._state_check_failed = 0
            except Exception as e:
                self._state_check_failed += 1
                logger.debug(f"Failed to fetch cluster state (failure {self._state_check_failed}/3): {e}")
                if self._state_check_failed >= 3:
                    # we've failed 3 times in a row, so stop periodic callback
                    # this is a fail-safe in case there's some reason this endpoint isn't responding
                    self.periodic_callbacks["check_coiled_state"].stop()
                elif "rate limit" in str(e).lower():
                    # every time we get rate limit, reduce rate at which we check cluster state
                    check_interval = (
                        dask.utils.parse_timedelta(dask.config.get("coiled.cluster-state-check-interval"))
                        * 1000
                        * self._state_check_failed
                    )
                    self.periodic_callbacks["check_coiled_state"].callback_time = check_interval

    @overload
    def close(self: Cluster[Sync], force_shutdown: bool = False, reason: str | None = None) -> None: ...

    @overload
    def close(self: Cluster[Async], force_shutdown: bool = False, reason: str | None = None) -> Awaitable[None]: ...

    def close(
        self: ClusterSyncAsync, force_shutdown: bool = False, reason: str | None = None
    ) -> Union[None, Awaitable[None]]:
        """
        Close the cluster.
        """
        return self.sync(self._close, force_shutdown=force_shutdown, reason=reason)

    @overload
    def shutdown(self: Cluster[Sync]) -> None: ...

    @overload
    def shutdown(self: Cluster[Async]) -> Awaitable[None]: ...

    def shutdown(self: ClusterSyncAsync) -> Union[None, Awaitable[None]]:
        """
        Shutdown the cluster; useful when shutdown_on_close is False.
        """
        return self.sync(self._close, force_shutdown=True)

    @overload
    def scale(self: Cluster[Sync], n: int, force_stop: bool = True) -> None: ...

    @overload
    def scale(self: Cluster[Async], n: int, force_stop: bool = True) -> Awaitable[None]: ...

    def scale(self: ClusterSyncAsync, n: int, force_stop: bool = True) -> Awaitable[None] | None:
        """Scale cluster to ``n`` workers

        Parameters
        ----------
        n
            Number of workers to scale cluster size to.
        force_stop
            Stop the VM even if scheduler did not retire the worker; for example, if worker has unique data
            that could not be moved to another worker.
        """
        return self.sync(self._scale, n=n, force_stop=force_stop)

    @track_context
    async def scale_down(self, workers: Iterable[str], reason: str | None = None, force_stop: bool = True) -> None:
        """
        Remove specified workers from the cluster.

        Parameters
        ----------
        workers
            Iterable of worker names
        reason
            Optional reason for why these workers are being removed (e.g., adaptive scaling)
        force_stop
            Stop the VM even if scheduler did not retire the worker; for example, if worker has unique data
            that could not be moved to another worker.
        """
        if not self.cluster_id:
            raise ValueError("No cluster available to scale!")
        cloud = cast(CloudV2[Async], self.cloud)

        await self._submit_cluster_event(
            "scaling",
            "scale down",
            extra_data={
                "workers": list(workers),
                "reason": reason,
                "force_stop": force_stop,
                "n_workers": len(list(workers)),
            },
        )

        scheduler_workers_retired = None
        try:
            scheduler_comm = self._ensure_scheduler_comm()
            scheduler_workers_retired = await scheduler_comm.retire_workers(
                names=workers,
                remove=True,
                close_workers=True,
            )
        except Exception as e:
            logger.warning(f"error retiring workers {e}. Trying more forcefully")

        # close workers more forcefully
        if scheduler_workers_retired is not None:
            scheduler_workers_retired = cast(dict, scheduler_workers_retired)
            # We got a response from scheduler about which of the requested workers are successfully being retired.
            # We'll assume that if a worker got removed from the list by the scheduler, there was a good reason
            # (e.g., unique data could not be moved to any other worker), so we won't forcibly stop the VM.
            scheduler_retired_names = {w.get("name") for w in scheduler_workers_retired.values()}

            not_retired_by_scheduler = [w for w in workers if w not in scheduler_retired_names]
            if not_retired_by_scheduler:
                logger.debug(
                    "There are some workers that the scheduler chose not to retire:\n"
                    f"  {', '.join(not_retired_by_scheduler)}\n"
                    "Scheduler logs may have more information about why worker(s) were not retired."
                )
                await self._submit_cluster_event(
                    "scaling",
                    "cluster scale down called with workers that scheduler did not retire",
                    extra_data={
                        "workers_not_retired": list(not_retired_by_scheduler),
                        "n_not_retired": len(not_retired_by_scheduler),
                        "force_stop": force_stop,
                    },
                )
                if force_stop:
                    logger.debug(
                        "Coiled will stop the VMs for these worker(s) as requested, "
                        "although this may result in lost work."
                    )
                else:
                    workers = [w for w in workers if w in scheduler_retired_names]

        # Because there's a limit on URL length and worker names are passed in DELETE as url params,
        # 1. remove the non-unique part of name (worker name is "<cluster name>-worker-<unique id>"), and
        # 2. limit worker in DELETE request to batch of at most 500.
        worker_name_identifiers = [w.replace(f"{self.name}-worker", "") for w in workers]
        batch_size = 200
        for batch_start in range(0, len(worker_name_identifiers), batch_size):
            worker_name_batch = worker_name_identifiers[batch_start : batch_start + batch_size]
            await cloud._scale_down(
                workspace=self.workspace,
                cluster_id=self.cluster_id,
                workers=worker_name_batch,
                reason=reason,
            )
        self._plan.difference_update(workers)
        self._requested.difference_update(workers)

    async def recommendations(self, target: int) -> dict:
        """
        Make scale up/down recommendations based on current state and target.

        Return a recommendation of the form
        - {"status": "same"}
        - {"status": "up", "n": <desired number of total workers>}
        - {"status": "down", "workers": <list of workers to close>}
        """
        # note that `Adaptive` has a `recommendations()` method, but (as far as I can tell) it doesn't
        # appear that adaptive ever calls `cluster.recommendations()`, so this appears to only be used
        # from `cluster.scale()`
        plan = self.plan
        requested = self.requested
        observed = self.observed

        n_current_or_expected = len(plan)

        if target == n_current_or_expected:
            return {"status": "same"}

        if target > n_current_or_expected:
            return {"status": "up", "n": target}

        # when scaling down, prefer workers that haven't yet connected to scheduler
        # for this to work, the worker name known by scheduler needs to match worker name in database
        not_yet_arrived = requested - observed
        to_close = set()
        if not_yet_arrived:
            to_close.update(islice(not_yet_arrived, n_current_or_expected - target))

        if target < n_current_or_expected - len(to_close):
            worker_list = await self.workers_to_close(target=target)
            to_close.update(worker_list)
        return {"status": "down", "workers": list(to_close)}

    async def _apply_scaling_recommendations(self, recommendations: dict, force_stop: bool = True):
        # structure of `recommendations` matches output of `self.recommendations()`
        status = recommendations.pop("status")
        if status == "same":
            return
        if status == "up":
            return await self.scale_up(**recommendations)
        if status == "down":
            return await self.scale_down(**recommendations, force_stop=force_stop)

    async def workers_to_close(self, target: int) -> List[str]:
        """
        Determine which, if any, workers should potentially be removed from
        the cluster.

        Notes
        -----
        ``Cluster.workers_to_close`` dispatches to Scheduler.workers_to_close(),
        but may be overridden in subclasses.

        Returns
        -------
        List of worker addresses to close, if any

        See Also
        --------
        Scheduler.workers_to_close
        """
        scheduler_comm = self._ensure_scheduler_comm()

        target_offset = 0
        if self.extra_worker_on_scheduler and target:
            # ask for an extra worker we can remove, so that if worker-on-scheduler is in the list
            # we can keep it alive and still get to target number of workers
            target_offset = 1
            target -= target_offset

        workers = await scheduler_comm.workers_to_close(
            target=target,
            attribute="name",
        )

        if self.extra_worker_on_scheduler and workers:
            # Never include the extra worker-on-scheduler in list of workers to kill.
            # Because we requested an extra possible worker (so we'd still get desired number if
            # worker-on-scheduler was in the list), we need only return the desired number (in case
            # extra worker-on-scheduler was *not* in the list of workers to kill).
            desired_workers = len(workers) - target_offset
            workers = list(filter(lambda name: "scheduler" not in name, workers))[:desired_workers]

        return workers  # type: ignore

    def adapt(
        self,
        Adaptive=CoiledAdaptive,
        *,
        minimum=1,
        maximum=200,
        target_duration="3m",
        wait_count=24,
        interval="5s",
        **kwargs,
    ) -> Adaptive:
        """Dynamically scale the number of workers in the cluster
        based on scaling heuristics.

        Parameters
        ----------
        minimum : int
            Minimum number of workers that the cluster should have while
            on low load, defaults to 1.
        maximum : int
            Maximum numbers of workers that the cluster should have while
            on high load.
        wait_count : int
            Number of consecutive times that a worker should be suggested
            for removal before the cluster removes it.
        interval : timedelta or str
            Milliseconds between checks, defaults to 5000 ms.
        target_duration : timedelta or str
            Amount of time we want a computation to take. This affects how
            aggressively the cluster scales up.

        """
        self._queue_cluster_event(
            "adaptive",
            "configured",
            extra_data={
                "minimum": minimum,
                "maximum": maximum,
                "target_duration": target_duration,
                "wait_count": wait_count,
                "interval": interval,
            },
        )
        return super().adapt(
            Adaptive=Adaptive,
            minimum=minimum,
            maximum=maximum,
            target_duration=target_duration,
            wait_count=wait_count,
            interval=interval,
            **kwargs,
        )

    def __enter__(self: Cluster[Sync]) -> Cluster[Sync]:
        return self.sync(self.__aenter__)

    def __exit__(
        self: Cluster[Sync],
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return self.sync(self.__aexit__, exc_type, exc_value, traceback)

    async def __aenter__(self: Cluster):
        await self
        return self

    async def __aexit__(
        self: ClusterSyncAsync,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: "TracebackType | None",
    ):
        if exc_type is not None:
            exit_reason = f"Shutdown due to an exception: {tb.format_exception(exc_type, exc_value, traceback)}"
        else:
            exit_reason = None
        f = self.close(reason=exit_reason)
        if isawaitable(f):
            await f

    @overload
    def get_logs(self: Cluster[Sync], scheduler: bool, workers: bool = True) -> dict: ...

    @overload
    def get_logs(self: Cluster[Async], scheduler: bool, workers: bool = True) -> Awaitable[dict]: ...

    def get_logs(self: ClusterSyncAsync, scheduler: bool = True, workers: bool = True) -> Union[dict, Awaitable[dict]]:
        """Return logs for the scheduler and workers
        Parameters
        ----------
        scheduler : boolean
            Whether or not to collect logs for the scheduler
        workers : boolean
            Whether or not to collect logs for the workers
        Returns
        -------
        logs: Dict[str]
            A dictionary of logs, with one item for the scheduler and one for
            the workers
        """
        return self.sync(self._get_logs, scheduler=scheduler, workers=workers)

    @track_context
    async def _get_logs(self, scheduler: bool = True, workers: bool = True) -> dict:
        if not self.cluster_id:
            raise ValueError("No cluster available for logs!")
        cloud = cast(CloudV2[Async], self.cloud)
        return await cloud.cluster_logs(
            cluster_id=self.cluster_id,
            workspace=self.workspace,
            scheduler=scheduler,
            workers=workers,
        )

    @overload
    def get_aggregated_metric(
        self: Cluster[Sync], query: str, over_time: str, start_ts: int | None = None, end_ts: int | None = None
    ) -> dict: ...

    @overload
    def get_aggregated_metric(
        self: Cluster[Async], query: str, over_time: str, start_ts: int | None = None, end_ts: int | None = None
    ) -> Awaitable[dict]: ...

    def get_aggregated_metric(
        self: ClusterSyncAsync, query: str, over_time: str, start_ts: int | None = None, end_ts: int | None = None
    ) -> Union[dict, Awaitable[dict]]:
        return self.sync(
            self._get_aggregated_metric, query=query, over_time=over_time, start_ts=start_ts, end_ts=end_ts
        )

    @track_context
    async def _get_aggregated_metric(
        self, query: str, over_time: str, start_ts: int | None = None, end_ts: int | None = None
    ) -> dict:
        if not self.cluster_id:
            raise ValueError("No cluster available for metrics!")
        cloud = cast(CloudV2[Async], self.cloud)
        return await cloud._get_cluster_aggregated_metric(
            cluster_id=self.cluster_id,
            workspace=self.workspace,
            query=query,
            over_time=over_time,
            start_ts=start_ts,
            end_ts=end_ts,
        )

    @overload
    def add_span(self: Cluster[Sync], span_identifier: str, data: dict): ...

    @overload
    def add_span(self: Cluster[Async], span_identifier: str, data: dict): ...

    def add_span(self: ClusterSyncAsync, span_identifier: str, data: dict):
        self.sync(
            self._add_span,
            span_identifier=span_identifier,
            data=data,
        )

    @track_context
    async def _add_span(self, span_identifier: str, data: dict):
        if not self.cluster_id:
            raise ValueError("No cluster available")
        cloud = cast(CloudV2[Async], self.cloud)
        await cloud._add_cluster_span(
            cluster_id=self.cluster_id,
            workspace=self.workspace,
            span_identifier=span_identifier,
            data=data,
        )

    @property
    def dashboard_link(self):
        if EXECUTION_CONTEXT == "notebook":
            # dask-labextension has trouble following the token in query, so we'll give it the token
            # in the url path, which our dashboard auth also accepts.
            parsed = parse_url(self._dashboard_address)
            if parsed.query and parsed.query.startswith("token="):
                token = parsed.query[6:]
                path_with_token = f"/{token}/status" if not parsed.path else f"/{token}{parsed.path}"
                return parsed._replace(path=path_with_token)._replace(query=None).url

        return self._dashboard_address

    @property
    def jupyter_link(self):
        if not self.scheduler_options.get("jupyter"):
            logger.warning(
                "Jupyter was not enabled on the cluster scheduler. Use `scheduler_options={'jupyter': True}` to enable."
            )
        return parse_url(self._dashboard_address)._replace(path="/jupyter/lab").url

    def write_files_for_dask(self, files: Dict[str, str], symlink_dirs: Dict | None = None):
        """
        Use Dask to write files to scheduler and all workers.

        files:
            Dictionary of files to write, for example, ``{"/path/to/file": "text to write"}``.
        """
        with dask.distributed.Client(self, name="non-user-write-files-via-dask") as client:
            register_plugin(client, DaskSchedulerWriteFiles(files=files, symlink_dirs=symlink_dirs))
            register_plugin(client, DaskWorkerWriteFiles(files=files, symlink_dirs=symlink_dirs))

    def mount_bucket(self: ClusterSyncAsync, bucket: Union[str, List[str]]):
        request_files = {}
        send_adc = False

        buckets: List[str] = [bucket] if isinstance(bucket, str) else bucket
        self._queue_cluster_event("mount", "Attempting to mount buckets", extra_data={"buckets": buckets})

        for single_bucket in buckets:
            service = None

            if single_bucket.startswith("gs://"):
                service = "gcs"
            elif single_bucket.startswith("s3://"):
                service = "s3"
            # don't block other schemes here and pass URI through so they can be handled by code doing the mount;
            # for example, we might add backend support for "r2://" and don't want to block this in client code.

            # if s3 or gcs is not explicitly specified, default to storage service for workspace cloud provider
            if not service and "://" not in single_bucket:
                if self.workspace_cloud_provider_name == "aws":
                    service = "s3"
                if self.workspace_cloud_provider_name == "gcp":
                    service = "gcs"

            if service == "gcs":
                # mount for Google Cloud Storage bucket relies on Application Default Credentials
                send_adc = True
            elif service == "s3":
                # mount for S3 bucket relies on the renewable credential endpoint
                if not self._using_aws_creds_endpoint:
                    logger.warning(
                        f"Mounting bucket '{bucket}' requires forwarding of refreshable AWS credentials, "
                        f"which is not currently working as needed."
                    )

            mount_kwargs = {"bucket": single_bucket}
            if service:
                mount_kwargs["service"] = service

            # agent on host VM watches /mount/.requests for info about buckets to mount
            request_files[f"/mount/.requests/todo/{short_random_string()}"] = json.dumps(mount_kwargs)

        if send_adc:
            send_application_default_credentials(self)
        # map /mount to a subdirectory in whatever the cwd for the container is
        self.write_files_for_dask(files=request_files, symlink_dirs={"/mount": "./mount"})

    def get_spark(
        self,
        block_till_ready: bool = True,
        spark_connect_config: dict | None = None,
        executor_memory_factor: float | None = None,
        worker_memory_factor: float | None = None,
    ):
        """
        Get a spark client. Experimental and subject to change without notice.

        To use this, start the cluster with ``coiled.spark.get_spark_cluster``.

        spark_connect_config:
            Optional dictionary of additional config options. For example, ``{"spark.foo": "123"}``
            would be equivalent to ``--config spark.foo=123`` when running ``spark-submit --class spark-connect``.
        executor_memory_factor:
            Determines ``spark.executor.memory`` based on the available memory, can be any value between 1 and 0.
            Default is 1.0, giving all available memory to the executor.
        worker_memory_factor:
            Determines ``--memory`` for org.apache.spark.deploy.worker.Worker, can be any value between 1 and 0.
            Default is 1.0.
        """
        from coiled.spark import SPARK_CONNECT_PORT, get_spark

        self._spark_dashboard = parse_url(self._dashboard_address)._replace(path="/spark").url
        self._spark_master = parse_url(self._dashboard_address)._replace(path="/spark-master").url
        dashboards = (
            "\n"
            f"[bold green]Spark UI:[/]     [link={self._spark_dashboard}]{self._spark_dashboard}[/link]"
            "\n\n"
            f"[bold green]Spark Master:[/] [link={self._spark_master}]{self._spark_master}[/link]"
            "\n"
        )

        if self.use_dashboard_https:
            host = parse_url(self._dashboard_address).host
            token = parse_url(self._dashboard_address).query
            remote_address = f"sc://{host}:{SPARK_CONNECT_PORT}/;use_ssl=true;{token}"
        else:
            remote_address = None

        with self.get_client() as client:
            spark_session = get_spark(
                client,
                connection_string=remote_address,
                block_till_ready=block_till_ready,
                spark_connect_config=spark_connect_config,
                executor_memory_factor=executor_memory_factor,
                worker_memory_factor=worker_memory_factor,
            )
            if self._spark_dashboard.startswith("https"):
                rich_print(Panel(dashboards, title="[bold green]Spark Dashboards[/]", width=CONSOLE_WIDTH))
            return spark_session


def __getattr__(name):
    if name == "ClusterBeta":
        warnings.warn(
            "`ClusterBeta` is deprecated and will be removed in a future release. Use `Cluster` instead.",
            category=FutureWarning,
            stacklevel=2,
        )
        return Cluster
    else:
        raise AttributeError(f"module {__name__} has no attribute {name}")
