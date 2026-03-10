import time
from typing import List, Dict, Any, Union
import re
import os
import uuid
import json
from tempfile import TemporaryDirectory
from subprocess import check_output, Popen
import subprocess
from datetime import datetime, timedelta
from collections import namedtuple

# Card plot styles
MEM_COLOR = "#0c64d6"
GPU_COLOR = "#ff69b4"

NVIDIA_TS_FORMAT = "%Y/%m/%d %H:%M:%S"


DRIVER_VER = re.compile(b"Driver Version: (.+?) ")
CUDA_VER = re.compile(b"CUDA Version:(.*) ")

MONITOR_FIELDS = [
    "timestamp",
    "gpu_utilization",
    "memory_used",
    "memory_total",
]

MONITOR = """nvidia-smi --query-gpu=pci.bus_id,timestamp,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits -l {interval};"""
ProcessUUID = namedtuple("ProcessUUID", ["uuid", "start_time", "end_time"])


def _get_uuid(time_duration=600):
    frmt_str = "%Y-%m-%d-%H-%M-%S"
    # Create a datetime range between the timerange values using current date as start date and time_duration as end date
    start_date = datetime.now()
    end_date = start_date + timedelta(seconds=time_duration)
    datetime_range = start_date = (
        datetime.now().strftime(frmt_str) + "_" + end_date.strftime(frmt_str)
    )
    uuid_str = uuid.uuid4().hex.replace("-", "") + "_" + datetime_range
    return ProcessUUID(uuid_str, start_date, end_date)


class AsyncProcessManager:
    """
    This class is responsible for managing the nvidia SMI subprocesses
    """

    processes: Dict[str, Dict] = {
        # "procid": {
        #     "proc": subprocess.Popen,
        #     "started": time.time()
        # }
    }

    @classmethod
    def _register_process(cls, procid, proc):
        cls.processes[procid] = {
            "proc": proc,
            "started": time.time(),
        }

    @classmethod
    def get(cls, procid):
        proc_dict = cls.processes.get(procid, None)
        if proc_dict is not None:
            return proc_dict["proc"], proc_dict["started"]
        return None, None

    @classmethod
    def spawn(cls, procid, cmd, file):
        proc = Popen(cmd, stdout=file)
        cls._register_process(procid, proc)

    @classmethod
    def remove(cls, procid, delete_item=True):
        if procid in cls.processes:
            if cls.processes[procid]["proc"].stdout is not None:
                cls.processes[procid]["proc"].stdout.close()
            cls.processes[procid]["proc"].terminate()
            cls.processes[procid]["proc"].wait()
            if delete_item:
                del cls.processes[procid]

    @classmethod
    def cleanup(cls):
        for procid in cls.processes:
            cls.remove(procid, delete_item=False)
        cls.processes.clear()

    @classmethod
    def is_running(cls, procid):
        if procid not in cls.processes:
            return False
        return cls.processes[procid]["proc"].poll() is None


def _parse_timestamp(timestamp):
    try:
        ts = timestamp.split(".")[0]
        return datetime.strptime(ts, NVIDIA_TS_FORMAT)
    except ValueError:
        return None


class GPUMonitor:
    """
    The `GPUMonitor` class is designed to monitor GPU usage.

    When an instance of `GPUMonitor` is created, it initializes with a specified `interval` and `duration`.
    The `duration` is the timeperiod it will run the NVIDIA SMI command for and the `interval` is the timeperiod between each reading.
    The class exposes a `_monitor_update_thread` method which runs as a background thread that continuously updates the GPU usage readings.
    It will keep running unitl the `_finished` flag is set to `True`.

    The class will statefully manage the the spawned NVIDI-SMI processes.
    It will start a new NVIDI-SMI process after the current one has ran for the specified `duration`.
    At a time this class will only maintain readings for the `_current_process` and will have all the aggregated
    readings for the past processes stored in the `_past_readings` dictionary.
    When a process finishes completion, the readings are appended to the `_past_readings` dictionary and a new process is started.

    If the caller of this class wishes to read the GPU usage, they can call the `read` method which will return the readings in a dictionary format.
    The `read` method will aggregate the readings from the `_current_readings` and `_past_readings`.
    """

    _started_processes: List[ProcessUUID] = []

    _current_process: Union[ProcessUUID, None] = None

    _current_readings: Dict[str, Any] = {}

    _past_readings: Dict[str, Any] = {}

    # Approximate bytes per sample per GPU (4 Python str objects + list pointers).
    BYTES_PER_SAMPLE = 258

    def __init__(self, interval=1, duration=300, max_samples_per_gpu=None) -> None:
        self._tempdir = TemporaryDirectory(prefix="gpu_card_monitor", dir="./")
        self._interval = interval
        self._duration = duration
        self._finished = False
        self._max_samples = max_samples_per_gpu

    @property
    def _current_file(self):
        if self._current_process is None:
            return None
        return os.path.join(self._tempdir.name, self._current_process.uuid + ".csv")

    def get_file_name(self, uuid):
        return os.path.join(self._tempdir.name, uuid + ".csv")

    def create_new_monitor(self):
        uuid = _get_uuid(self._duration)
        file = open(self.get_file_name(uuid.uuid), "w")
        cmd = MONITOR.format(interval=self._interval, time_duration=self._duration)
        AsyncProcessManager.spawn(uuid.uuid, ["bash", "-c", cmd], file)
        self._started_processes.append(uuid)
        self._current_process = uuid
        return uuid

    def clear_current_monitor(self):
        if self._current_process is None:
            return
        AsyncProcessManager.remove(self._current_process.uuid)
        self._current_process = None

    def current_process_has_ended(self):
        if self._current_process is None:
            return True
        return datetime.now() > self._current_process.end_time

    def current_process_is_running(self):
        if self._current_process is None:
            return False
        return AsyncProcessManager.is_running(self._current_process.uuid)

    def _read_monitor(self):
        """
        Reads the monitor file and returns the readings in a dictionary format
        """
        all_readings = []
        if self._current_file is None:
            return None

        if not os.path.exists(self._current_file):
            return None
        # Extract everything from the CVS File and store it in a list of dictionaries
        all_fields = ["gpu_id"] + MONITOR_FIELDS
        with open(self._current_file, "r") as _monitor_out:
            for line in _monitor_out.readlines():
                data = {}
                fields = [f.strip() for f in line.split(",")]
                if len(fields) == len(all_fields):
                    # strip subsecond resolution from timestamps that doesn't align across devices
                    for idx, _f in enumerate(all_fields):
                        data[_f] = fields[idx]
                    all_readings.append(data)
                else:
                    # expect that the last line may be truncated
                    break

        # Convert to dictionary format
        devdata = {}
        for reading in all_readings:
            gpu_id = reading["gpu_id"]
            if "timestamp" not in reading:
                continue
            if _parse_timestamp(reading["timestamp"]) is None:
                continue
            reading["timestamp"] = reading["timestamp"].split(".")[0]
            if gpu_id not in devdata:
                devdata[gpu_id] = {}

            for i, field in enumerate(MONITOR_FIELDS):
                if field not in devdata[gpu_id]:
                    devdata[gpu_id][field] = []
                devdata[gpu_id][field].append(reading[field])
        return devdata

    def _update_readings(self):
        """
        Core update function that checks if the current process has ended and if so, it will create a new monitor
        otherwise sets the current readings to the readings from the monitor file
        """
        if self.current_process_has_ended() or not self.current_process_is_running():
            self._update_past_readings()
            self.clear_current_monitor()
            self.create_new_monitor()
            # Sleep for 1 seconds to allow the new process to start and we can make a reading
            time.sleep(1)

        readings = self._read_monitor()
        if readings is None:
            return
        self._current_readings = readings

    @staticmethod
    def _make_full_reading(current, past):
        if current is None:
            return past
        for gpu_id in current:
            if gpu_id not in past:
                past[gpu_id] = {}
            for field in MONITOR_FIELDS:
                if field not in past[gpu_id]:
                    past[gpu_id][field] = []
                past[gpu_id][field].extend(current[gpu_id][field])
        return past

    @staticmethod
    def _downsample(readings, max_points):
        """
        Stride-sample each GPU's field arrays to at most `max_points` entries.
        Preserves the first and last point so time range is accurate.
        """
        for gpu_id in readings:
            n = len(readings[gpu_id].get("timestamp", []))
            if n <= max_points:
                continue
            stride = max(1, (n - 1) // (max_points - 1))
            indices = list(range(0, n, stride))
            if indices[-1] != n - 1:
                indices.append(n - 1)
            for field in MONITOR_FIELDS:
                if field in readings[gpu_id]:
                    readings[gpu_id][field] = [
                        readings[gpu_id][field][i] for i in indices
                    ]
        return readings

    def read(self, max_points=None):
        full = self._make_full_reading(
            self._current_readings, json.loads(json.dumps(self._past_readings))
        )
        if max_points is not None and max_points > 0:
            return self._downsample(full, max_points)
        return full

    def _update_past_readings(self):
        if self._current_readings is None:
            return
        self._past_readings = self._make_full_reading(
            self._current_readings, json.loads(json.dumps(self._past_readings))
        )
        self._current_readings = None
        if self._max_samples is not None:
            self._trim_past_readings()

    def _trim_past_readings(self):
        """Ring-buffer trim: keep only the last _max_samples entries per GPU."""
        for gpu_id in self._past_readings:
            n = len(self._past_readings[gpu_id].get("timestamp", []))
            if n <= self._max_samples:
                continue
            for field in MONITOR_FIELDS:
                if field in self._past_readings[gpu_id]:
                    self._past_readings[gpu_id][field] = self._past_readings[gpu_id][
                        field
                    ][-self._max_samples :]

    def cleanup(self):
        self._finished = True
        AsyncProcessManager.cleanup()
        self._tempdir.cleanup()

    def _monitor_update_thread(self):
        while not self._finished:
            self._update_readings()
            time.sleep(self._interval)


# This code is adapted from: https://github.com/outerbounds/monitorbench
class GPUProfiler:
    @staticmethod
    def _read_versions():
        def parse(r, s):
            return r.search(s).group(1).strip().decode("utf-8")

        try:
            result = subprocess.run(
                ["nvidia-smi"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            out = result.stdout
            return parse(DRIVER_VER, out), parse(CUDA_VER, out), None
        except FileNotFoundError:
            return None, None, "nvidia-smi not found"
        except AttributeError:
            return None, None, "nvidia-smi output is unexpected"
        except subprocess.CalledProcessError as e:
            _error_message = "nvidia-smi error (CalledProcessError calling nvidia-smi)"
            if e.stderr is not None:
                _error_message = (
                    "nvidia-smi error (CalledProcessError stderr) \n %s \n %s"
                    % (e.stderr.decode("utf-8"), e.stdout.decode("utf-8"))
                )
            return None, None, _error_message
        except Exception as e:
            return None, None, "nvidia-smi error (unknown error) \n%s" % str(e)

    @staticmethod
    def _read_devices():
        out = check_output(
            [
                "nvidia-smi",
                "--query-gpu=name,pci.bus_id,memory.total",
                "--format=csv,noheader",
            ]
        )
        return [
            dict(
                zip(("name", "device_id", "memory"), (x.strip() for x in l.split(",")))
            )
            for l in out.decode("utf-8").splitlines()
        ]

    @staticmethod
    def _read_multi_gpu_interconnect():
        """
        parse output of `nvidia-smi tomo -m`, such as this sample:

            GPU0    GPU1    CPU Affinity    NUMA Affinity
            GPU0     X      NV2     0-23            N/A
            GPU1    NV2      X      0-23            N/A

        returns two dictionaries describing multi-GPU topology:
            data: {index: [GPU0, GPU1, ...], GPU0: [X, NV2, ...], GPU1: [NV2, X, ...], ...}
            legend_items: {X: 'Same PCI', NV2: 'NVLink 2', ...}
        """
        try:
            import re

            ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")

            out = check_output(["nvidia-smi", "topo", "-m"])
            rows = out.decode("utf-8").split("\n")

            header = ansi_escape.sub("", rows[0]).split("\t")[1:]
            data = {}
            data["index"] = []
            data |= {k: [] for k in header}

            for i, row in enumerate(rows[1:]):
                row = ansi_escape.sub("", row).split()
                if len(row) == 0:
                    continue
                if row[0].startswith("GPU"):
                    data["index"].append(row[0])
                    for key, val in zip(header, row[1:]):
                        data[key].append(val)
                elif row[0].startswith("Legend"):
                    break

            legend_items = {}
            for legend_row in rows[i:]:
                if legend_row == "" or legend_row.startswith("Legend"):
                    continue
                res = legend_row.strip().split(" = ")
                legend_items[res[0].strip()] = res[1].strip()

            return data, legend_items

        except:
            return None, None

    @staticmethod
    def read_gpu_info():
        """
        Query nvidia-smi for driver info, device list, and interconnect topology.

        Returns a dict with keys:
            driver_version, cuda_version, error, devices, interconnect
        """
        driver_ver, cuda_ver, error = GPUProfiler._read_versions()
        if error:
            return {
                "driver_version": None,
                "cuda_version": None,
                "error": error,
                "devices": [],
                "interconnect": None,
            }
        devices = GPUProfiler._read_devices()
        ic_data, ic_legend = GPUProfiler._read_multi_gpu_interconnect()
        interconnect = None
        if ic_data and ic_legend:
            interconnect = {"data": ic_data, "legend": ic_legend}
        return {
            "driver_version": driver_ver,
            "cuda_version": cuda_ver,
            "error": None,
            "devices": devices,
            "interconnect": interconnect,
        }
