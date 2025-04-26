from __future__ import annotations

import contextlib
import functools
import inspect
import os
import sys
import threading
import warnings
from collections.abc import Iterator
from typing import Dict, List, Union

import dask.config
import dask.distributed
import toolz
from dask.base import tokenize
from dask.system import CPU_COUNT
from dask.utils import parse_timedelta
from typing_extensions import Literal

import coiled
from coiled.spans import span
from coiled.utils import error_info_for_tracking

_clients = {}
_lock = threading.RLock()
_clusters = {}


@contextlib.contextmanager
def _set_local_environ(environ: Dict[str, str]):
    """Temporarily set local environment variables"""
    original_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original_environ)


class Function:
    """A function that you can run remotely"""

    def __init__(
        self,
        function,
        cluster_kwargs,
        keepalive,
        environ,
        local: bool = False,
        name: str | None = None,
    ):
        self.function = function
        self._cluster_kwargs = cluster_kwargs
        self.keepalive = parse_timedelta(keepalive)
        self._local = local
        self._environ = environ

        if isinstance(function, functools.partial):  # Special case partial functions
            _code = inspect.getsource(function.func)
        else:
            try:
                _code = inspect.getsource(function)
            except Exception:
                _code = ""

        # __code__ is for compatibility with prefect decorator
        # _code is for backward compatibility
        self.__code__ = self._code = _code

        if name is not None:
            self._name = name
        else:
            token = tokenize(
                sys.executable,
                local,
                environ,
                keepalive,
                # TODO: include something about the software environment
                **cluster_kwargs,
            )
            self._name = f"function-{token[:8]}"

    @property
    def __signature__(self):
        return inspect.signature(self.function)

    @property
    def cluster_status(self) -> dask.distributed.Status | None:
        if self._name in _clusters:
            return _clusters[self._name].status
        return None

    @property
    def client_status(self) -> str | None:
        if self._name in _clients:
            return _clients[self._name].status
        return None

    def _clear_terminal_cluster(self):
        # we can't use a cluster that's stopping or stopped, so check if we need to remake cluster
        if not self._local:
            # note that status will be `None` if there's no cluster
            if self.cluster_status in coiled.v2.cluster.TERMINATING_STATES or self.client_status in (
                "closing",
                "closed",
            ):
                _clusters.pop(self._name, None)
                _clients.pop(self._name, None)

    @property
    def cluster(self) -> Union[coiled.Cluster, dask.distributed.LocalCluster]:
        with _lock:
            self._clear_terminal_cluster()
            try:
                return _clusters[self._name]
            except KeyError:
                success = True
                exception = None
                info = {}
                info["keepalive"] = self.keepalive
                info["local"] = self._local
                try:
                    # Setting to use the local threaded scheduler avoids implicit tasks in tasks.
                    # This relies on `send_dask_config=True` (default value).
                    with dask.config.set({
                        "scheduler": "threads",
                        "distributed.worker.daemon": False,
                        "distributed.worker.memory.target": 0.9,
                        "distributed.worker.memory.spill": 0.9,
                        "distributed.worker.memory.pause": False,
                        "distributed.worker.memory.terminate": False,
                    }):
                        if self._local:
                            with _set_local_environ(self._environ or {}):
                                cluster = dask.distributed.LocalCluster(
                                    name=self._name,
                                    threads_per_worker=self._cluster_kwargs["worker_options"]["nthreads"],
                                )
                                if isinstance(self._cluster_kwargs["n_workers"], (list, tuple)):
                                    cluster.adapt(
                                        minimum=self._cluster_kwargs["n_workers"][0],
                                        maximum=self._cluster_kwargs["n_workers"][1],
                                    )
                        else:
                            cluster = coiled.Cluster(name=self._name, **self._cluster_kwargs)
                            info["account"] = cluster.account
                            info["cluster_id"] = cluster.cluster_id

                            if self._environ:
                                cluster.send_private_envs(self._environ)

                            # some env vars are set in dask config early in the dask loading process
                            # we set these to `""` since that's what we can do in the relevant dask config
                            # but some libraries don't accept empty string, so we'll unset them here.
                            # this won't affect things loaded by dask, but should affect user-code.
                            user_specified_env = {
                                **(self._environ or {}),
                                **(self._cluster_kwargs.get("environ") or {}),
                            }
                            single_thread_unsets = [
                                key
                                for key in coiled.utils.unset_single_thread_defaults().keys()
                                if not user_specified_env.get(key)
                            ]

                            cluster.unset_env_vars(single_thread_unsets)

                    _clusters[self._name] = cluster
                    return cluster
                except Exception as e:
                    success = False
                    exception = e
                    raise
                finally:
                    coiled.add_interaction(
                        "coiled-function",
                        success=success,
                        **info,
                        **error_info_for_tracking(exception),
                    )

    @property
    def client(self) -> dask.distributed.Client:
        with _lock:
            self._clear_terminal_cluster()
            try:
                return _clients[self._name]
            except KeyError:
                client = dask.distributed.Client(self.cluster, set_as_default=False)
                if self.cluster.shutdown_on_close and isinstance(self.cluster, coiled.Cluster):
                    self.cluster.set_keepalive(keepalive=self.keepalive)
                _clients[self._name] = client
                return client

    def __call__(self, *args, **kwargs):
        # If this is being called from on the desired cluster, then run locally.
        # This allows one Function (with same desired cluster specs) to call another without overhead.
        if os.environ.get("COILED_CLUSTER_NAME", None) == self._name:
            return self.local(*args, **kwargs)
        # Otherwise, submit to cluster.
        return self.submit(*args, **kwargs).result()

    @property
    def local(self):
        return Function(
            self.function,
            cluster_kwargs=self._cluster_kwargs,
            keepalive=self.keepalive,
            environ=self._environ,
            local=True,
        )

    def submit(self, *args, **kwargs) -> dask.distributed.Future:
        """Submit function call for asynchronous execution

        This immediately returns a Dask Future, allowing for the submission of
        many tasks in parallel.

        Example
        -------
        >>> @coiled.function()
        ... def f(x):
        ...    return x + 1

        >>> f(10)  # calling the function blocks until finished
        11
        >>> f.submit(10)  # immediately returns a future
        <Future: pending, key=f-1234>
        >>> f.submit(10).result()  # Call .result to get result
        11

        >>> futures = [f(i) for i in range(1000)]  # parallelize with a for loop
        >>> [future.result() for future in futures]
        ...

        Returns
        -------
        future: dask.distributed.Future

        See Also
        --------
        Function.map
        """
        with span(self.cluster, callstack=[{"code": self._code, "relative_line": 0}]):
            result = self.client.submit(self.function, *args, **kwargs)
        return result

    def map(self, *args, errors: Literal["raise", "skip"] = "raise", **kwargs) -> Iterator:
        """Map function across many inputs

        This runs your function many times in parallel across all of the items
        in an input list.  Coiled will auto-scale your cluster to meet demand.

        Parameters
        ----------
        errors
            Either 'raise' or 'skip' if we should raise if a function call has erred
            or include ``None`` in the output collection.

        Example
        -------
        >>> @coiled.function()
        ... def process(filename: str):
        ...     " Convert CSV file to Parquet "
        ...     df = pd.read_csv(filename)
        ...     outfile = filename[:-4] + ".parquet"
        ...     df.to_parquet(outfile)
        ...     return outfile

        >>> process("s3://my-bucket/data.csv")  # calling the function blocks until finished
        11
        >>> filenames = process.map(filenames)
        >>> print(list(filenames))  # print out all output filenames

        Returns
        -------
        results: Iterator

        See Also
        --------
        Function.submit
        """
        kwargs.setdefault("pure", False)

        if not hasattr(dask.distributed.client, "_MapLayer"):
            kwargs.setdefault("batch_size", 100)
        with span(self.cluster, callstack=[{"code": self._code, "relative_line": 0}]):
            futures = self.client.map(self.function, *args, **kwargs)  # type: ignore
        batchsize = max(int(len(futures) / 50), 1)  # type: ignore
        batches = toolz.partition_all(batchsize, futures)
        return (result for batch in batches for result in self.client.gather(batch, errors=errors))  # type: ignore


def function(
    *,
    software: str | None = None,
    container: str | None = None,
    vm_type: Union[str, list[str]] | None = None,
    cpu: Union[int, list[int]] | None = None,
    memory: Union[str, list[str]] | None = None,
    gpu: bool | None = None,
    account: str | None = None,
    workspace: str | None = None,
    region: str | None = None,
    arm: bool | None = None,
    disk_size: Union[str, int] | None = None,
    allow_ingress_from: str | None = None,
    shutdown_on_close: bool = True,
    spot_policy: str | None = None,
    idle_timeout: str = "6 hours",
    keepalive="30 seconds",
    package_sync_ignore: list[str] | None = None,
    environ: Dict[str, str] | None = None,
    threads_per_worker: Union[int, None] = 1,
    local: bool = False,
    name: str | None = None,
    tags: Dict[str, str] | None = None,
    n_workers: Union[int, List[int]] | None = None,
    extra_kwargs: dict | None = None,
):
    """
    Decorate a function to run on cloud infrastructure

    This creates a ``Function`` object that executes its code on a remote cluster
    with the hardware and software specified in the arguments to the decorator.
    It can run either as a normal function, or it can return Dask Futures for
    parallel computing.

    Parameters
    ----------
    software
        Name of the software environment to use; this allows you to use and re-use existing
        Coiled software environments, and should not be used with package sync or when specifying
        a container to use for this specific cluster.
    container
        Name or URI of container image to use; when using a pre-made container image with Coiled,
        this allows you to skip the step of explicitly creating a Coiled software environment
        from that image. Note that this should not be used with package sync or when specifying
        an existing Coiled software environment.
    vm_type
        Instance type, or list of instance types, that you would like to use.
        You can use ``coiled.list_instance_types()`` to see a list of allowed types.
    cpu
        Number, or range, of CPUs requested. Specify a range by
        using a list of two elements, for example: ``cpu=[2, 8]``.
    memory
        Amount of memory to request for each VM, Coiled will use a +/- 10% buffer
        from the memory that you specify. You may specify a range of memory by using a
        list of two elements, for example: ``memory=["2GiB", "4GiB"]``.
    disk_size
        Size of persistent disk attached to each VM instance, specified as string with units
        or integer for GiB.
    gpu
        Whether to attach a GPU; this would be a single NVIDIA T4.
    account
        **DEPRECATED**. Use ``workspace`` instead.
    workspace
        The Coiled workspace (previously "account") to use. If not specified,
        will check the ``coiled.workspace`` or ``coiled.account`` configuration values,
        or will use your default workspace if those aren't set.
    region
        The cloud provider region in which to run the cluster.
    arm
        Whether to use ARM instances for cluster; default is x86 (Intel) instances.
    keepalive
        Keep your cluster running for the specified time, even if your Python session closes.
        Default is "30 seconds".
    spot_policy
        Purchase option to use for workers in your cluster, options are "on-demand", "spot", and
        "spot_with_fallback"; by default this is "spot_with_fallback" for Coiled Functions.
        (Google Cloud refers to this as "provisioning model" for your instances.)
        Note that even with this option, the first VM is always on-demand. This only applies to any
        additional VMs when running Coiled Functions in parallel across multiple
        VMs with the ``.map()`` and ``.submit()`` methods. When running on a single VM, an on-demand
        instance will be used.

        Spot instances are much cheaper, but can have more limited availability and may be terminated
        while you're still using them if the cloud provider needs more capacity for other customers.
        On-demand instances have the best availability and are almost never
        terminated while still in use, but they're significantly more expensive than spot instances.
        For most workloads, "spot_with_fallback" is likely to be a good choice: Coiled will try to get as
        many spot instances as we can, and if we get less than you requested, we'll try to get the remaining
        instances as on-demand.
        For AWS, when we're notified that an active spot instance is going to be terminated,
        we'll attempt to get a replacement instance (spot if available, but could be on-demand if you've
        enabled "fallback"). Dask on the active instance will attempt a graceful shutdown before the
        instance is terminated so that computed results won't be lost.
    idle_timeout
        Shut down the cluster after this duration if no activity has occurred. Default is "6 hours".
    package_sync_ignore
        A list of package names to exclude from the cloud VM environment. This is useful when you have
        large libraries installed locally that aren't needed for the function being run.
        Note the packages listed here may still be installed by another package that depends on them.
    environ
        Dictionary of environment variables to securely pass to the cloud VM environment.
    threads_per_worker
        Number of threads to run concurrent tasks in for each VM. -1 can be used to run as many concurrent
        tasks as there are CPU cores. Default is 1.
    allow_ingress_from
        Control the CIDR from which cluster firewall allows ingress to scheduler; by default this is open
        to any source address (0.0.0.0/0). You can specify CIDR, or "me" for just your IP address.
    local
        Whether or not to run this function locally or on cloud VMs. If ``True``, this function will be
        run on your local machine, which can be useful for debugging or during development.
        Default is ``False``.
    name
        Name for the Coiled cluster on which this function will run. If not specified,
        VM specification parameters like ``vm_type``, ``disk_size``, etc. will be used to produce
        a unique, deterministic name. Note that ``name`` is used for sharing cloud VMs among
        Coiled Functions with the same hardware and software specification, so please use
        this parameter with care.  Default to ``None``.
    tags
        Dictionary of tags.
    n_workers
        Number of VMs to provision for parallel function execution. Can either be an integer for a
        static number of machines, or a list specifying the lower and upper bounds for adaptively
        scaling up/down machines depending on the amount of work submitted. Defaults to
        ``n_workers=[0, 500]`` which adaptively scales between 0 and 500 machines.
    extra_kwargs
        Dictionary of any additional keyword arguments to pass to ``coiled.Cluster()``. Note that any cluster
        arguments controlled by other ``@coiled.function`` keyword arguments will take precendence over the kwargs
        in this dictionary.


    See the :class:`coiled.Cluster` docstring for additional parameter descriptions.

    Examples
    --------
    >>> import coiled
    >>> @coiled.function()
    ... def f(x):
    ...    return x + 1

    >>> f(10)  # calling the function blocks until finished
    11
    >>> f.submit(10)  # immediately returns a future
    <Future: pending, key=f-1234>
    >>> f.submit(10).result()  # Call .result to get result
    11

    >>> futures = [f(i) for i in range(1000)]  # parallelize with a for loop
    >>> [future.result() for future in futures]
    ...
    """

    if workspace and account and workspace != account:
        raise ValueError(
            f"You specified both workspace='{workspace}' and account='{account}'. "
            "The `account` kwarg is being deprecated, use `workspace` instead."
        )
    if account and not workspace:
        warnings.warn("The `account` kwarg is deprecated, use `workspace` instead.", DeprecationWarning, stacklevel=2)
    account = account or workspace

    def decorator(func) -> Function:
        nonlocal cpu, threads_per_worker, environ, n_workers

        default_environ = {}
        if container and "rapidsai" in container:
            default_environ = {"DISABLE_JUPYTER": "true", **default_environ}  # needed for "stable" RAPIDS image
        if os.environ.get("COILED_REUSE_ENVIRON_KEYS"):
            keys = os.environ["COILED_REUSE_ENVIRON_KEYS"].split(",")
            default_environ.update({key: os.environ[key] for key in keys})

        if memory is None and cpu is None and not vm_type and not gpu:
            cpu = 2

        if threads_per_worker == -1:
            # Have `-1` mean the same as CPU count (Dask's default behavior)
            threads_per_worker = None

        if n_workers is None:
            if local:
                n_workers = [0, CPU_COUNT or 10]
            else:
                n_workers = [0, 500]

        cluster_kwargs = dict(
            account=account,
            n_workers=n_workers,
            scheduler_cpu=cpu,
            scheduler_memory=memory,
            worker_cpu=cpu,
            worker_memory=memory,
            software=software,
            container=container,
            idle_timeout=idle_timeout,
            scheduler_vm_types=vm_type,
            allow_ingress_from=allow_ingress_from,
            worker_vm_types=vm_type,
            allow_ssh_from="me",
            environ=default_environ,
            scheduler_gpu=gpu,
            worker_gpu=gpu,
            region=region,
            arm=arm,
            shutdown_on_close=shutdown_on_close,
            spot_policy="spot_with_fallback" if spot_policy is None else spot_policy,
            extra_worker_on_scheduler=True,
            tags={**(tags or {}), **{"coiled-cluster-type": "function"}},
            worker_options={"nthreads": threads_per_worker},
            scheduler_disk_size=disk_size,
            worker_disk_size=disk_size,
            package_sync_ignore=package_sync_ignore,
            unset_single_threading_variables=True,
        )

        # user args take precedence over defaults
        cluster_kwargs = {
            **cluster_kwargs,
            **(extra_kwargs or {}),
        }

        return functools.wraps(func)(  # type: ignore
            Function(func, cluster_kwargs, keepalive=keepalive, environ=environ, local=local, name=name)
        )

    return decorator


# Small backwards compatibility shim
def run(*args, **kwargs):
    warnings.warn(
        "coiled.run has been renamed to coiled.function. "
        "Please use coiled.function as coiled.run will be removed in a future release.",
        FutureWarning,
        stacklevel=2,
    )
    return function(*args, **kwargs)
