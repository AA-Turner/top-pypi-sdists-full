import os
import sys
import time
import subprocess
from io import BytesIO
from datetime import datetime, timezone

from metaflow.exception import MetaflowException


def kill_process_and_descendants(pid, termination_timeout=1, iterations=20, delay=0.5):
    for i in range(iterations):
        try:
            subprocess.check_call(["pkill", "-TERM", "-P", str(pid)])
            subprocess.check_call(["kill", "-TERM", str(pid)])

            time.sleep(termination_timeout)

            subprocess.check_call(["pkill", "-KILL", "-P", str(pid)])
            subprocess.check_call(["kill", "-KILL", str(pid)])
        except subprocess.CalledProcessError:
            pass

        # Don't delay after the last iteration
        if i < iterations - 1:
            time.sleep(delay)


class HeartbeatStore(object):
    def __init__(
        self,
        main_pid=None,
        storage_backend=None,
        emit_frequency=30,
        missed_heartbeat_timeout=60,
        monitor_frequency=15,
        max_missed_heartbeats=3,
    ) -> None:
        self.main_pid = main_pid
        self.storage_backend = storage_backend
        self.emit_frequency = emit_frequency
        self.monitor_frequency = monitor_frequency
        self.missed_heartbeat_timeout = missed_heartbeat_timeout
        self.max_missed_heartbeats = max_missed_heartbeats
        self.missed_heartbeats = 0

    def emit_heartbeat(self, heartbeat_prefix: str, folder_name=None):
        heartbeat_key = f"{heartbeat_prefix}/heartbeat"
        if folder_name:
            heartbeat_key = f"{folder_name}/{heartbeat_key}"

        while True:
            try:
                epoch_string = str(datetime.now(timezone.utc).timestamp()).encode(
                    "utf-8"
                )
                self.storage_backend.save_bytes(
                    [(heartbeat_key, BytesIO(bytes(epoch_string)))], overwrite=True
                )
            except Exception as e:
                print(f"Error writing heartbeat: {e}")
                sys.exit(1)

            time.sleep(self.emit_frequency)

    def emit_tombstone(self, tombstone_prefix: str, folder_name=None):
        tombstone_key = f"{tombstone_prefix}/tombstone"
        if folder_name:
            tombstone_key = f"{folder_name}/{tombstone_key}"

        tombstone_string = "tombstone".encode("utf-8")
        try:
            self.storage_backend.save_bytes(
                [(tombstone_key, BytesIO(bytes(tombstone_string)))], overwrite=True
            )
        except Exception as e:
            print(f"Error writing tombstone: {e}")
            sys.exit(1)

    def __handle_tombstone(self, path):
        if path is not None:
            with open(path) as f:
                contents = f.read()
                if "tombstone" in contents:
                    print("[Outerbounds] Tombstone detected. Terminating the task..")
                    kill_process_and_descendants(self.main_pid)
                    sys.exit(1)

    def __handle_heartbeat(self, path):
        if path is not None:
            with open(path) as f:
                contents = f.read()
                current_timestamp = datetime.now(timezone.utc).timestamp()
                if current_timestamp - float(contents) > self.missed_heartbeat_timeout:
                    self.missed_heartbeats += 1
                else:
                    self.missed_heartbeats = 0
        else:
            self.missed_heartbeats += 1

        if self.missed_heartbeats > self.max_missed_heartbeats:
            print(
                f"[Outerbounds] Missed {self.max_missed_heartbeats} consecutive heartbeats. Terminating the task.."
            )
            kill_process_and_descendants(self.main_pid)
            sys.exit(1)

    def is_main_process_running(self):
        try:
            # Check if the process is running
            os.kill(self.main_pid, 0)
        except ProcessLookupError:
            return False
        return True

    def monitor(self, heartbeat_prefix: str, tombstone_prefix: str, folder_name=None):
        heartbeat_key = f"{heartbeat_prefix}/heartbeat"
        if folder_name:
            heartbeat_key = f"{folder_name}/{heartbeat_key}"

        tombstone_key = f"{tombstone_prefix}/tombstone"
        if folder_name:
            tombstone_key = f"{folder_name}/{tombstone_key}"

        while self.is_main_process_running():
            with self.storage_backend.load_bytes(
                [heartbeat_key, tombstone_key]
            ) as results:
                for key, path, _ in results:
                    if key == tombstone_key:
                        self.__handle_tombstone(path)
                    elif key == heartbeat_key:
                        self.__handle_heartbeat(path)

            time.sleep(self.monitor_frequency)


if __name__ == "__main__":
    from metaflow.plugins import DATASTORES
    from metaflow.metaflow_config import NVIDIA_HEARTBEAT_THRESHOLD

    if len(sys.argv) != 4:
        print("Usage: heartbeat_store.py <main_pid> <datastore_type> <folder_name>")
        sys.exit(1)
    _, main_pid, datastore_type, folder_name = sys.argv

    if datastore_type not in ("azure", "gs", "s3"):
        print(f"Datastore unsupported for type: {datastore_type}")
        sys.exit(1)

    datastores = [d for d in DATASTORES if d.TYPE == datastore_type]
    datastore_sysroot = datastores[0].get_datastore_root_from_config(
        lambda *args, **kwargs: None
    )
    if datastore_sysroot is None:
        raise MetaflowException(
            msg="METAFLOW_DATASTORE_SYSROOT_{datastore_type} must be set!".format(
                datastore_type=datastore_type.upper()
            )
        )

    storage = datastores[0](datastore_sysroot)

    heartbeat_prefix = f"{os.getenv('MF_PATHSPEC')}/{os.getenv('MF_ATTEMPT')}"
    flow_name, run_id, _, _ = os.getenv("MF_PATHSPEC").split("/")
    tombstone_prefix = f"{flow_name}/{run_id}"

    store = HeartbeatStore(
        main_pid=int(main_pid),
        storage_backend=storage,
        max_missed_heartbeats=int(NVIDIA_HEARTBEAT_THRESHOLD),
    )

    store.monitor(
        heartbeat_prefix=heartbeat_prefix,
        tombstone_prefix=tombstone_prefix,
        folder_name=folder_name,
    )
