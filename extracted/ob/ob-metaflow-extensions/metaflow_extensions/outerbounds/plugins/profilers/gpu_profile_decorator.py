"""
gpu_profile_decorator.py — @gpu_profile via StepMutator + isolated subprocess.

Injects @card(type='blank', id='gpu_profile') + a @user_step_decorator wrapper
that spawns an isolated subprocess for live GPU monitoring.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime

from metaflow import StepMutator, user_step_decorator

_DEBUG = os.environ.get("METAFLOW_GPU_PROFILE_DEBUG", "") != ""


def _debug(msg):
    if _DEBUG:
        print("[gpu_profile] %s" % msg, file=sys.stderr, flush=True)


from ...profilers.gpu import GPUProfiler
from ...profilers.gpu_card_writer import (
    _build_gpu_spec,
    _build_max_util_table,
    _build_mem_spec,
    _build_ts_range,
)
from ...profilers.gpu_card_utils import build_subprocess_config


_CARD_PROCESS_SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.pardir,
    os.pardir,
    "profilers",
    "gpu_card_process.py",
)


def _safe_id(device_id):
    return re.sub(r"[^a-zA-Z0-9]", "_", device_id)


def _build_comp_ids(devices):
    comp_ids = {"max_util_table": "max_util_table", "devices": {}}
    for d in devices:
        did = d["device_id"]
        safe = _safe_id(did)
        comp_ids["devices"][did] = {
            "charts_table": "charts_table_%s" % safe,
            "ts_range": "ts_%s" % safe,
        }
    return comp_ids


def _placeholder_spec():
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Waiting for GPU readings...",
        "data": {"values": []},
        "width": 600,
        "height": 400,
        "mark": "line",
        "encoding": {
            "x": {"field": "tstamps", "type": "temporal"},
            "y": {"field": "vals", "type": "quantitative"},
        },
    }


def _setup_card(
    card,
    pathspec,
    started_at,
    attempt,
    devices,
    driver_ver,
    cuda_ver,
    comp_ids,
    artifact_prefix,
    interconnect=None,
):
    from metaflow.cards import Markdown, Table, VegaChart

    refs = {}

    card.append(Markdown("# GPU profile for `%s`" % pathspec))
    card.append(Markdown("_Started at: %s_" % started_at))
    card.append(Markdown("_Attempt: %d_" % attempt))

    card.append(Markdown("## Drivers"))
    card.append(
        Table(
            [[driver_ver, cuda_ver]],
            headers=["NVidia driver version", "CUDA version"],
        )
    )

    card.append(Markdown("## Devices"))
    if devices:
        rows = [[d["device_id"], d["name"], d["memory"]] for d in devices]
        card.append(Table(rows, headers=["Device ID", "Device type", "GPU memory"]))
    else:
        card.append(Markdown("_No GPU devices found._"))

    if interconnect:
        card.append(Markdown("## Interconnect"))
        ic_data = interconnect["data"]
        rows = list(ic_data.values())
        rows = [list(transpose_row) for transpose_row in list(zip(*rows))]
        card.append(Table(rows, headers=list(ic_data.keys())))
        card.append(Markdown("#### Legend"))
        card.append(
            Table(
                [list(interconnect["legend"].values())],
                headers=list(interconnect["legend"].keys()),
            )
        )

    card.append(Markdown("## Maximum utilization"))
    max_util_md = Markdown("_Waiting for first reading..._")
    card.append(max_util_md, id=comp_ids["max_util_table"])
    card.append(
        Markdown("_Detailed data saved in artifact `%sdata`_" % artifact_prefix)
    )
    refs["__max_util__"] = max_util_md

    card.append(Markdown("## GPU utilization and memory usage over time"))

    for d in devices:
        did = d["device_id"]
        cids = comp_ids["devices"][did]

        card.append(Markdown("### GPU Utilization for device : %s" % did))

        ts_md = Markdown("*No readings available*")
        card.append(ts_md, id=cids["ts_range"])

        gpu_vc = VegaChart(_placeholder_spec())
        mem_vc = VegaChart(_placeholder_spec())
        chart_table = Table(
            data=[
                [Markdown("GPU Utilization"), gpu_vc],
                [Markdown("Memory usage"), mem_vc],
            ]
        )
        card.append(chart_table, id=cids["charts_table"])

        refs[did] = {"gpu": gpu_vc, "mem": mem_vc, "ts": ts_md}

    return refs


@user_step_decorator
def _gpu_profile_wrapper(step_name, flow, inputs=None, attr=None):
    from metaflow import current

    attr = attr or {}
    interval = attr.get("interval", 1)
    card_interval = attr.get("card_interval", 5)
    max_memory_mb = attr.get("max_memory_mb", 100)
    include_artifacts = attr.get("include_artifacts", True)
    artifact_prefix = attr.get("artifact_prefix", "gpu_profile_")

    try:
        gpu_info = GPUProfiler.read_gpu_info()
        error = gpu_info["error"]
        devices = gpu_info["devices"]
        driver_ver = gpu_info["driver_version"] or "unknown"
        cuda_ver = gpu_info["cuda_version"] or "unknown"
        interconnect = gpu_info["interconnect"]
    except Exception as e:
        error, devices, driver_ver, cuda_ver, interconnect = (
            None,
            [],
            "unknown",
            "unknown",
            None,
        )
        _debug("device read failed: %s" % e)

    comp_ids = _build_comp_ids(devices)
    started_at = datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S %z")

    num_gpus = max(len(devices), 1)
    max_samples_per_gpu = (max_memory_mb * 1024 * 1024) // (258 * num_gpus)
    # Debug override: force a tiny buffer to test the shedding codepath.
    _samples_override = os.environ.get("METAFLOW_GPU_PROFILE_MAX_SAMPLES", "")
    if _samples_override:
        max_samples_per_gpu = int(_samples_override)
        _debug("max_samples OVERRIDDEN to %d via env var" % max_samples_per_gpu)
    window_hrs = (max_samples_per_gpu * interval) / 3600.0
    _debug(
        "memory cap: %dMB, %d GPUs, %d samples/GPU, window: %.1f hrs"
        % (max_memory_mb, num_gpus, max_samples_per_gpu, window_hrs)
    )

    card = current.card["gpu_profile"]
    attempt = getattr(current, "retry_count", 0)
    refs = _setup_card(
        card,
        current.pathspec,
        started_at,
        attempt,
        devices,
        driver_ver,
        cuda_ver,
        comp_ids,
        artifact_prefix,
        interconnect,
    )

    card.refresh(force=True)

    readings_path = tempfile.mktemp(suffix=".json", prefix="gpu_readings_")

    config = build_subprocess_config(
        card_id="gpu_profile",
        comp_ids=comp_ids,
        interval=interval,
        card_interval=card_interval,
        devices=devices,
        readings_path=readings_path,
        max_samples_per_gpu=max_samples_per_gpu,
    )

    cmd = [sys.executable, _CARD_PROCESS_SCRIPT, "--config", json.dumps(config)]
    _debug("launching subprocess")

    _subprocess_log = tempfile.NamedTemporaryFile(
        mode="w", suffix=".log", prefix="gpu_card_proc_", delete=False
    )
    _subprocess_log_path = _subprocess_log.name

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=_subprocess_log,
        env={**os.environ, "METAFLOW_PROFILE": os.environ.get("METAFLOW_PROFILE", "")},
    )

    import time as _time

    _time.sleep(3)
    if proc.poll() is not None:
        _subprocess_log.flush()
        with open(_subprocess_log_path, "r") as f:
            err = f.read().strip()
        print(
            "[gpu_profile] subprocess died immediately (exit %d):\n%s"
            % (proc.returncode, err),
            file=sys.stderr,
            flush=True,
        )
    else:
        _debug("subprocess alive (pid=%d)" % proc.pid)

    _final_readings = {}

    try:
        yield  # user's step code runs here

    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()

        _subprocess_log.close()
        try:
            with open(_subprocess_log_path, "r") as f:
                stderr_out = f.read().strip()
        except Exception:
            stderr_out = ""
        if stderr_out:
            _debug("subprocess log:\n" + stderr_out)
        try:
            os.remove(_subprocess_log_path)
        except OSError:
            pass

        try:
            with open(readings_path, "r") as f:
                _final_readings = json.loads(f.read())
        except Exception as e:
            _debug("could not read final readings from %s: %s" % (readings_path, e))
        finally:
            try:
                os.remove(readings_path)
            except OSError:
                pass

        if _final_readings:
            ut = _build_max_util_table(_final_readings, comp_ids["max_util_table"])
            refs["__max_util__"].update(text=ut["source"])

            for did, cids in comp_ids["devices"].items():
                dev_data = _final_readings.get(did, {})
                dev_refs = refs[did]
                gpu_spec = _build_gpu_spec(dev_data)
                mem_spec = _build_mem_spec(dev_data)
                ts_c = _build_ts_range(dev_data, cids["ts_range"])
                if gpu_spec:
                    dev_refs["gpu"].update(spec=gpu_spec)
                if mem_spec:
                    dev_refs["mem"].update(spec=mem_spec)
                dev_refs["ts"].update(text=ts_c["source"])

        if include_artifacts:
            setattr(flow, artifact_prefix + "num_gpus", len(devices))
            setattr(
                flow,
                artifact_prefix + "data",
                {
                    "error": error,
                    "cuda_version": cuda_ver,
                    "driver_version": driver_ver,
                    "devices": devices,
                    "profile": _final_readings,
                    "interconnect": interconnect,
                },
            )


_DEFAULT_CARD_INTERVAL = 5
_DEFAULT_MAX_MEMORY_MB = 100


class gpu_profile(StepMutator):
    """
    Monitors GPU utilization and memory usage during a step.

    Produces a live-updating Metaflow card with:

    - Driver and CUDA version info
    - Device summary (ID, type, memory)
    - Multi-GPU interconnect topology (when multiple GPUs are present)
    - Peak utilization table
    - Per-device time-series charts for GPU utilization and memory

    Profiling runs with negligible overhead on your training loop.

    Readings are stored up to the ``max_memory_mb`` limit. When full,
    the oldest readings are dropped automatically. At the defaults
    (100 MB, 1-second interval), coverage is approximately:

    - **1 GPU:** ~4.5 days
    - **4 GPUs:** ~1.1 days
    - **8 GPUs:** ~13.5 hours

    Increase ``max_memory_mb`` for longer runs; decrease it on large
    multi-GPU nodes to save memory.

    The full set of retained readings is saved as an artifact at step
    end, so the artifact size is proportional to ``max_memory_mb``.

    Artifacts (when ``include_artifacts=True``):

    - ``{artifact_prefix}num_gpus``: number of GPUs detected.
    - ``{artifact_prefix}data``: dict with per-GPU time series,
      driver/CUDA versions, device metadata, and interconnect topology.

    Parameters
    ----------
    interval : int, default 1
        How often to sample GPU metrics, in seconds.
    max_memory_mb : int, default 100
        Memory budget in MB for storing GPU readings. Controls how
        far back readings extend before the oldest are dropped.
    include_artifacts : bool, default True
        Whether to save profiling data as Metaflow artifacts.
    artifact_prefix : str, default ``"gpu_profile_"``
        Prefix for artifact names.
    """

    def init(self, **kwargs):
        self.interval = int(kwargs.get("interval", 1))
        self.max_memory_mb = int(kwargs.get("max_memory_mb", _DEFAULT_MAX_MEMORY_MB))
        self.include_artifacts = kwargs.get("include_artifacts", True)
        self.artifact_prefix = kwargs.get("artifact_prefix", "gpu_profile_")

    def mutate(self, mutable_step):
        card_interval = max(_DEFAULT_CARD_INTERVAL, self.interval)
        mutable_step.add_decorator(
            "card",
            deco_kwargs={
                "type": "blank",
                "id": "gpu_profile",
                "refresh_interval": card_interval,
            },
            duplicates=mutable_step.IGNORE,
        )
        mutable_step.add_decorator(
            _gpu_profile_wrapper,
            deco_kwargs={
                "interval": self.interval,
                "card_interval": card_interval,
                "max_memory_mb": self.max_memory_mb,
                "include_artifacts": self.include_artifacts,
                "artifact_prefix": self.artifact_prefix,
            },
            duplicates=mutable_step.IGNORE,
        )
