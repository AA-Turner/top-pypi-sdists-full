"""
Note that pyrightconfig.json is set to ignore this file. If our spark integration becomes more well supported,
we should undo that and fix the type errors.
"""

import asyncio
import multiprocessing
import os
import pathlib
import shlex
import subprocess
import sys
import time
import warnings
from typing import Optional

try:
    import pyspark  # type: ignore
except ImportError:
    raise ImportError(
        """pyspark and other libraries not installed

To use Spark with Coiled, you'll have to install some additional libraries.

For more information see https://docs.coiled.io/user_guide/spark.html#install
""".strip()
    ) from None
import rich
from dask.distributed import Client
from distributed.diagnostics.plugin import SchedulerPlugin, WorkerPlugin
from pyspark.errors.exceptions.connect import SparkConnectGrpcException
from pyspark.sql import SparkSession

from coiled import Cluster

SPARK_CONNECT_PORT = 15003  # this provides ssl termination with proxy in front of 15002
DEBUG_PORTS = [
    22,  # ssh
    7077,  # spark master <-> worker, so usually just internal to cluster
    # dashboards usually get proxied to 443 with auth
    8787,  # dash dashboard
    4040,  # spark connect
    8080,  # spark master
    15002,  # spark gRPC port directly exposed without ssl/bearer auth
]
SPARK_VERSION = pyspark.__version__
# sc._jvm.org.apache.hadoop.util.VersionInfo.getVersion()
HADOOP_AWS_VERSION = "3.3.4"
AWS_JAVA_SDK_BUNDLE_VERSION = "1.12.262"


class SparkMaster(SchedulerPlugin):
    name = "spark-master"
    cls = "org.apache.spark.deploy.master.Master"
    idempotent = True

    def start(self, scheduler):
        self.scheduler = scheduler
        self.scheduler.add_plugin(self)

        path = pathlib.Path(pyspark.__file__).absolute()
        module_loc = path.parent
        os.environ["SPARK_HOME"] = str(module_loc)
        os.environ["PYSPARK_PYTHON"] = sys.executable

        host = scheduler.address.split("//")[1].split(":")[0]
        cmd = f"spark-class {self.cls} --host {host} --port 7077 --webui-port 8080"
        print(f"Executing\n{cmd}")
        self.proc = subprocess.Popen(shlex.split(cmd))
        print("Launched Spark Master")

    def close(self):
        self.proc.terminate()
        self.proc.wait()
        return super().close()


class SparkConnect(SchedulerPlugin):
    name = "spark-connect"
    cls = "org.apache.spark.sql.connect.service.SparkConnectServer"
    idempotent = True

    def __init__(self, config=None, executor_memory_factor: float = 1.0):
        self.extra_spark_connect_config = config
        self.executor_memory_factor = executor_memory_factor

    async def start(self, scheduler):
        print("Starting SparkConnect")
        self.scheduler = scheduler
        self.scheduler.add_plugin(self)

        # We need a worker so we know how large to set executors
        while not self.scheduler.workers:
            print("Spark connect waiting for first worker to appear ...")
            await asyncio.sleep(1)

        ws = self.scheduler.workers.values()[0]

        path = pathlib.Path(pyspark.__file__).absolute()
        module_loc = path.parent
        os.environ["SPARK_HOME"] = str(module_loc)
        os.environ["PYSPARK_PYTHON"] = sys.executable

        host = scheduler.address.split("//")[1].split(":")[0]
        spark_master = f"{host}:7077"

        spark_config = {
            "spark.driver.host": f"{host}",
            "spark.executor.memory": f"{int(ws.memory_limit * self.executor_memory_factor) // 2**20}m",
            "spark.executor.cores": f"{ws.nthreads}",
            "spark.hadoop.fs.s3a.aws.credentials.provider": (
                "com.amazonaws.auth.EnvironmentVariableCredentialsProvider"
                ",org.apache.hadoop.fs.s3a.auth.IAMInstanceCredentialsProvider"
                ",com.amazonaws.auth.profile.ProfileCredentialsProvider "
            ),
            **(self.extra_spark_connect_config or {}),
        }

        spark_config_cmd = " ".join(f"--conf {key}={value}" for key, value in spark_config.items())

        cmd = (
            f"spark-submit --class {self.cls} "
            '--name "SparkConnectServer" '
            f"--packages org.apache.spark:spark-connect_2.12:{pyspark.__version__}"
            f",{','.join(PACKAGES)} "
            f"--master spark://{spark_master} "
            f"{spark_config_cmd}"
        )
        print(f"Executing\n{cmd}")
        self.proc = subprocess.Popen(shlex.split(cmd))

    def close(self):
        self.proc.terminate()
        self.proc.wait()
        return super().close()


class SparkWorker(WorkerPlugin):
    name = "spark-worker"
    cls = "org.apache.spark.deploy.worker.Worker"
    idempotent = True

    def __init__(self, worker_memory_factor: float = 1.0):
        self.worker_memory_factor = worker_memory_factor

    def setup(self, worker):
        self.worker = worker

        path = pathlib.Path(pyspark.__file__).absolute()
        module_loc = path.parent
        os.environ["SPARK_HOME"] = str(module_loc)
        os.environ["PYSPARK_PYTHON"] = sys.executable

        # Sometimes Dask super-saturates cores.  Don't do this for Spark.
        # not sure if this actually has any impact though ...
        cores = min(self.worker.state.nthreads, multiprocessing.cpu_count())

        host = worker.scheduler.address.split("//")[1].split(":")[0]
        spark_master = f"spark://{host}:7077"
        print(f"Launching Spark Worker connecting to {spark_master}")
        cmd = (
            f"spark-class {self.cls} {spark_master} "
            f"--cores {cores} "
            f"--memory {int(self.worker.memory_manager.memory_limit * self.worker_memory_factor) // 2**20}m "
        )
        self.proc = subprocess.Popen(shlex.split(cmd))
        print("Launched Spark Worker")

    def close(self):
        self.proc.terminate()
        self.proc.wait()
        return super().close()


PACKAGES = (
    f"org.apache.hadoop:hadoop-client:{HADOOP_AWS_VERSION}",
    f"org.apache.hadoop:hadoop-common:{HADOOP_AWS_VERSION}",
    f"org.apache.hadoop:hadoop-aws:{HADOOP_AWS_VERSION}",
    f"com.amazonaws:aws-java-sdk-bundle:{AWS_JAVA_SDK_BUNDLE_VERSION}",
)


def get_spark(
    client: Client,
    name="Coiled",
    connection_string=None,
    block_till_ready: bool = True,
    spark_connect_config: Optional[dict] = None,
    executor_memory_factor: Optional[float] = None,
    worker_memory_factor: Optional[float] = None,
) -> SparkSession:
    """Launch Spark on a Dask Client

    This returns a ``spark`` session instance connected via SparkConnect

    spark_connect_config:
        Optional dictionary of additional config options. For example, ``{"spark.foo": "123"}``
        would be equivalent to ``--config spark.foo=123`` when running ``spark-submit --class spark-connect``.
    """
    from coiled.spark import SparkConnect, SparkMaster, SparkWorker

    if not connection_string:
        host = client.scheduler.address.split("//")[1].split(":")[0]
        port = 15002
        connection_string = f"sc://{host}:{port}"
        # warn because it's unlikely that someone wants to be connecting insecurely
        warnings.warn(
            f"HTTPS is not enabled for this cluster. Attempting to connect to Spark at {connection_string} "
            "without encryption or authentication. This is not recommended and will only work if you've explicitly "
            f"opened {port} for ingress.",
            stacklevel=1,
        )

    spark_connect_kwargs = {"config": spark_connect_config}
    if executor_memory_factor is not None:
        spark_connect_kwargs["executor_memory_factor"] = executor_memory_factor

    worker_kwargs = {"worker_memory_factor": worker_memory_factor} if worker_memory_factor is not None else {}

    client.register_plugin(SparkMaster())
    client.register_plugin(SparkWorker(**worker_kwargs))
    client.register_plugin(SparkConnect(**spark_connect_kwargs))

    spark = SparkSession.builder.remote(connection_string).appName(name).getOrCreate()

    if block_till_ready:
        # wait up to 60s for spark to be ready
        n_times = 20
        for retry in range(n_times):
            try:
                v = spark.version  # do something that relies on connection
                rich.print(f"[bold]Spark connection established[/bold]. Spark version {v}.")
                break
            except SparkConnectGrpcException as e:
                if retry < n_times - 1:
                    time.sleep(5)
                    continue
                else:
                    rich.print(f"[red]Spark Connect is not (yet) accepting connections[/red]\n\n{e}")

    return spark


def get_spark_cluster(_open_debug_ports=False, *args, **kwargs):
    cluster = Cluster(
        *args,
        **kwargs,
        backend_options={
            "ingress": [
                {
                    "ports": [443, 8786, SPARK_CONNECT_PORT, *(DEBUG_PORTS if _open_debug_ports else [])],
                    "cidr": "0.0.0.0/0",
                },
            ],
        },
    )
    return cluster
