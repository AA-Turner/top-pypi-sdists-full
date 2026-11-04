"""JSON-line driver for real SDK clients constructed after POSIX fork.

The driver itself never imports the SDK or starts HTTP threads. A separate
fixture server owns synthetic DCS/ID-list data. Tests and memory experiments
can therefore exercise the same child-process lifecycle without mocking SDKs.
"""

import gc
import json
import multiprocessing
import os
from pathlib import Path
import sys
import traceback


def _worker(connection, index, config):
    from statsig_python_core import (
        DynamicConfigEvaluationOptions,
        EvaluationCache,
        FeatureGateEvaluationOptions,
        Statsig,
        StatsigOptions,
        StatsigUser,
    )

    sdk = None
    running = False
    held_results = []
    gate_options = FeatureGateEvaluationOptions(disable_exposure_logging=True)
    config_options = DynamicConfigEvaluationOptions(disable_exposure_logging=True)

    def start():
        nonlocal sdk, running
        sdk = Statsig(
            config.get("sdk_key", "secret-local-shared-id-lists"),
            StatsigOptions(
                specs_url=config["specs_url"],
                id_lists_url=config["id_lists_url"],
                log_event_url=config["log_event_url"],
                shared_id_lists_dir=config.get("shared_id_lists_dir"),
                enable_id_list_elias_fano=config.get("enable_id_list_elias_fano"),
                enable_id_lists=config.get("enable_id_lists", True),
                disable_disk_access=config.get("disable_disk_access", False),
                specs_sync_interval_ms=60_000,
                id_lists_sync_interval_ms=config.get("sync_interval_ms", 1000),
                init_timeout_ms=config.get("init_timeout_ms", 10_000),
                sdk_runtime_thread_count=1,
                fallback_to_statsig_api=False,
                disable_all_logging=not config.get("enable_logging", False),
                output_log_level="none",
                service_name=f"shared-id-list-worker-{index}",
                evaluation_cache=(
                    EvaluationCache(max_bytes=1_048_576, max_entry_bytes=65_536)
                    if config.get("evaluation_cache")
                    else None
                ),
            ),
        )
        initialized = sdk.initialize().wait(20)
        running = True
        return {"pid": os.getpid(), "initialized": initialized, "active": True}

    try:
        connection.send(start())
        while True:
            command = connection.recv()
            operation = command["op"]
            if operation == "evaluate":
                values = {}
                for user_id in command["users"]:
                    user = StatsigUser(user_id)
                    gate = sdk.get_feature_gate(user, "membership", gate_options)
                    result = sdk.get_dynamic_config(user, "membership", config_options)
                    values[user_id] = {"gate": gate.value, "config": result.value}
                    if command.get("hold_results"):
                        held_results.append((gate, result))
                response = {"pid": os.getpid(), "values": values}
            elif operation == "held_results":
                response = {
                    "values": [
                        {"gate": gate.value, "config": result.value}
                        for gate, result in held_results
                    ]
                }
            elif operation == "mapped_files":
                response = {
                    "files": [
                        line.split(maxsplit=5)[-1]
                        for line in Path("/proc/self/maps").read_text().splitlines()
                        if ".ids" in line
                    ]
                }
            elif operation == "log_and_flush":
                sdk.log_event(StatsigUser(f"event-worker-{index}"), command["event_name"])
                response = {"flushed": sdk.flush_events().wait(10)}
            elif operation == "shutdown":
                response = {"pid": os.getpid(), "shutdown": sdk.shutdown().wait(10)}
                running = False
            elif operation == "drop":
                sdk = None
                running = False
                gc.collect()
                response = {"pid": os.getpid(), "active": False}
            elif operation == "restart":
                assert not running
                sdk = None
                gc.collect()
                response = start()
            elif operation == "exit":
                if running:
                    sdk.shutdown().wait(10)
                    running = False
                connection.send({"pid": os.getpid(), "exited": True})
                return
            else:
                raise ValueError(f"Unknown worker operation: {operation}")
            connection.send(response)
    except EOFError:
        pass
    except BaseException:
        connection.send({"error": traceback.format_exc(), "pid": os.getpid()})
    finally:
        if running:
            sdk.shutdown().wait(5)
        connection.close()


class WorkerGroup:
    def __init__(self, config):
        self.config = config
        self.context = multiprocessing.get_context("fork")
        self.workers = {}
        for index in range(config.get("workers", 8)):
            self.start_worker(index)

    def start_worker(self, index):
        parent, child = self.context.Pipe()
        process = self.context.Process(target=_worker, args=(child, index, self.config))
        process.start()
        child.close()
        self.workers[index] = (process, parent)

    def receive(self, index, timeout=30):
        process, connection = self.workers[index]
        if not connection.poll(timeout):
            raise TimeoutError(f"Worker {index} pid={process.pid} did not respond")
        response = connection.recv()
        if "error" in response:
            raise RuntimeError(response["error"])
        return response

    def command(self, command):
        operation = command["op"]
        indices = command.get("workers", list(self.workers))
        if operation == "ready":
            return {str(index): self.receive(index) for index in indices}
        if operation == "kill":
            responses = {}
            for index in indices:
                process, connection = self.workers.pop(index)
                process.kill()
                process.join(5)
                connection.close()
                responses[str(index)] = {"pid": process.pid, "exitcode": process.exitcode}
            return responses
        if operation == "start_worker":
            for index in indices:
                assert index not in self.workers
                self.start_worker(index)
            return {str(index): self.receive(index) for index in indices}
        for index in indices:
            self.workers[index][1].send(command)
        return {str(index): self.receive(index) for index in indices}

    def close(self):
        for process, connection in self.workers.values():
            if process.is_alive():
                try:
                    connection.send({"op": "exit"})
                except (BrokenPipeError, OSError):
                    pass
        for process, connection in self.workers.values():
            process.join(5)
            if process.is_alive():
                process.kill()
                process.join(5)
            connection.close()


def main():
    config = json.loads(sys.stdin.readline())
    group = WorkerGroup(config)
    try:
        print(json.dumps(group.command({"op": "ready"})), flush=True)
        for line in sys.stdin:
            command = json.loads(line)
            if command["op"] == "exit":
                break
            try:
                response = group.command(command)
            except BaseException:
                response = {"error": traceback.format_exc()}
            print(json.dumps(response), flush=True)
    finally:
        group.close()


if __name__ == "__main__":
    main()
