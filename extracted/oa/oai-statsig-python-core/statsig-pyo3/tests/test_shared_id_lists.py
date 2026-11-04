"""Shared ID lists with eight real SDKs constructed after fork on Linux."""

import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
from time import monotonic, sleep, time

import pytest
from shared_id_lists_http_server import IdListHTTPFixture


pytestmark = pytest.mark.skipif(
    sys.platform != "linux", reason="Exercises Linux fork, process locks and mmap views"
)
RUNNER = Path(__file__).with_name("shared_id_lists_process_runner.py")


class SDKWorkers:
    def __init__(
        self,
        server,
        shared_dir,
        log_path,
        *,
        count=8,
        enabled=True,
        disk_access=True,
        enable_id_list_elias_fano=None,
        evaluation_cache=False,
        enable_logging=False,
    ):
        self.config = {
            "workers": count,
            "specs_url": server.url("/v2/download_config_specs"),
            "id_lists_url": server.url("/v1/get_id_lists"),
            "log_event_url": server.url("/v1/log_event"),
            "shared_id_lists_dir": str(shared_dir) if shared_dir is not None else None,
            "enable_id_lists": enabled,
            "enable_id_list_elias_fano": enable_id_list_elias_fano,
            "disable_disk_access": not disk_access,
            "evaluation_cache": evaluation_cache,
            "enable_logging": enable_logging,
        }
        self.active = set(range(count))
        self.log_path = log_path
        self.process = None
        self.log_file = None
        self.pids = {}

    def __enter__(self):
        self.log_file = self.log_path.open("w")
        self.process = subprocess.Popen(
            [sys.executable, str(RUNNER)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=self.log_file,
            text=True,
            bufsize=1,
            start_new_session=True,
        )
        try:
            self._send(self.config)
            ready = self._receive()
            assert all(value["initialized"] for value in ready.values()), ready
            self.pids = {int(index): value["pid"] for index, value in ready.items()}
            return self
        except BaseException:
            self.close()
            raise

    def _send(self, command):
        self.process.stdin.write(json.dumps(command) + "\n")
        self.process.stdin.flush()

    def _receive(self):
        readable, _, _ = select.select([self.process.stdout], [], [], 45)
        assert readable, f"SDK driver timed out; stderr: {self.log_path}"
        line = self.process.stdout.readline()
        assert line, f"SDK driver exited; stderr: {self.log_path}"
        response = json.loads(line)
        assert "error" not in response, response.get("error")
        return response

    def command(self, operation, *, workers=None, **kwargs):
        selected = sorted(self.active) if workers is None else list(workers)
        self._send({"op": operation, "workers": selected, **kwargs})
        response = self._receive()
        if operation in {"kill", "shutdown", "drop"}:
            self.active.difference_update(selected)
        elif operation in {"restart", "start_worker"}:
            self.active.update(selected)
            self.pids.update({int(index): value["pid"] for index, value in response.items()})
        return response

    def close(self):
        if self.process is not None:
            if self.process.poll() is None:
                try:
                    self._send({"op": "exit"})
                    self.process.communicate(timeout=15)
                except (BrokenPipeError, subprocess.TimeoutExpired):
                    os.killpg(self.process.pid, signal.SIGKILL)
                    self.process.communicate(timeout=5)
            if self.log_file is not None:
                self.log_file.close()

    def __exit__(self, *_):
        self.close()


def wait_for_membership(workers, expected):
    deadline = monotonic() + 15
    while True:
        results = workers.command("evaluate", users=list(expected))
        if all(
            result["values"][user] == {"gate": value, "config": {"member": value}}
            for result in results.values()
            for user, value in expected.items()
        ):
            return results
        assert monotonic() < deadline, results
        sleep(0.05)


def file_requests(server):
    return [
        request
        for request in server.state()["recent_requests"]
        if request["path"].startswith("/files/")
    ]


def current_downloader(server):
    request = file_requests(server)[-1]
    return int(request["worker"].removeprefix("shared-id-list-worker-"))


def shared_manifest(directory):
    manifests = list(directory.rglob("manifest.json"))
    assert len(manifests) == 1, manifests
    return manifests[0]


def assert_mapped_by_all_workers(workers, directory, expected_version):
    path = shared_manifest(directory)
    namespace_root = directory / "elias-fano-v1" if expected_version == 3 else directory
    assert path.parent.parent == namespace_root
    manifest = json.loads(path.read_text())
    data_file = path.parent / manifest["lists"]["members"]["data_file"]
    with data_file.open("rb") as snapshot:
        snapshot.seek(8)  # The data-file version follows its eight-byte magic.
        assert int.from_bytes(snapshot.read(4), "little") == expected_version
    for index, result in workers.command("mapped_files").items():
        assert str(data_file) in result["files"], f"Worker {index} has no shared ID-list map"


def assert_events_delivered(workers, server, phase):
    event_name = f"shared-id-list-{phase}"
    responses = workers.command("log_and_flush", event_name=event_name)
    assert all(response["flushed"] for response in responses.values())
    observed = {
        (request["worker"], event["user_id"])
        for request in server.state()["recent_requests"]
        for event in request.get("events", [])
        if event["name"] == event_name
    }
    assert observed == {
        (f"shared-id-list-worker-{index}", f"event-worker-{index}")
        for index in workers.active
    }


@pytest.mark.parametrize("evaluation_cache", [False, True])
@pytest.mark.parametrize(
    ("elias_fano", "expected_version"),
    [(None, 2), (False, 2), (True, 3)],
    ids=["default-v2", "false-v2", "ef-v3"],
)
def test_eight_workers_share_updates_and_leadership_handoffs(
    tmp_path, evaluation_cache, elias_fano, expected_version
):
    directory = tmp_path / "shared"
    with IdListHTTPFixture() as server, SDKWorkers(
        server,
        directory,
        tmp_path / "workers.log",
        evaluation_cache=evaluation_cache,
        enable_id_list_elias_fano=elias_fano,
        enable_logging=True,
    ) as workers:
        initial_pids = workers.pids.copy()
        wait_for_membership(workers, {"alice": True, "steady": True, "bob": False})
        workers.command("evaluate", users=["alice", "bob"], hold_results=True)
        assert len(file_requests(server)) == 1
        assert_mapped_by_all_workers(workers, directory, expected_version)
        assert_events_delivered(workers, server, "initialized")

        initial_size = server.state()["manifest"]["members"]["size"]
        server.control({"op": "append", "add_users": ["bob"], "remove_users": ["alice"]})
        wait_for_membership(workers, {"alice": False, "steady": True, "bob": True})
        assert file_requests(server)[-1]["start"] == initial_size

        server.control({"op": "replace", "users": ["carol"]})
        expected = {"alice": False, "steady": False, "bob": False, "carol": True}
        wait_for_membership(workers, expected)
        assert file_requests(server)[-1]["start"] == 0
        assert_mapped_by_all_workers(workers, directory, expected_version)

        metadata = server.state()["manifest"]["members"]
        server.control(
            {
                "op": "replace",
                "users": ["dana"],
                "file_id": metadata["fileID"],
                "creation_time": metadata["creationTime"] + 1,
            }
        )
        expected.update(carol=False, dana=True)
        wait_for_membership(workers, expected)
        assert file_requests(server)[-1]["start"] == 0

        for operation in ("kill", "shutdown", "drop"):
            leader = current_downloader(server)
            workers.command(operation, workers=[leader])
            server.control({"op": "reset_counters"})
            new_user = f"after-{operation}"
            server.control({"op": "append", "add_users": [new_user]})
            expected[new_user] = True
            wait_for_membership(workers, expected)
            assert current_downloader(server) != leader
            assert len({request["worker"] for request in file_requests(server)}) == 1
            restart = "start_worker" if operation == "kill" else "restart"
            workers.command(restart, workers=[leader])
            wait_for_membership(workers, expected)
            assert len(workers.active) == 8
            assert_mapped_by_all_workers(workers, directory, expected_version)
            assert_events_delivered(workers, server, operation)

        # Python results remain stable; native old-mmap snapshots are tested in Rust.
        held = workers.command("held_results")
        for index, result in held.items():
            if workers.pids[int(index)] == initial_pids[int(index)]:
                assert result["values"] == [
                    {"gate": True, "config": {"member": True}},
                    {"gate": False, "config": {"member": False}},
                ]

        downloads_before_removal = len(file_requests(server))
        server.control({"op": "set_manifest", "names": []})
        wait_for_membership(workers, dict.fromkeys(expected, False))
        assert len(file_requests(server)) == downloads_before_removal


@pytest.mark.parametrize("mode", ["unset", "unavailable", "disabled", "disk_disabled"])
def test_private_default_disabled_and_unavailable_directory(tmp_path, mode):
    directory = None if mode == "unset" else tmp_path / "shared"
    if mode == "unavailable":
        directory.write_text("a file cannot be a shared directory")
    with IdListHTTPFixture() as server, SDKWorkers(
        server,
        directory,
        tmp_path / "workers.log",
        enabled=mode != "disabled",
        disk_access=mode != "disk_disabled",
    ) as workers:
        wait_for_membership(workers, {"alice": mode != "disabled", "bob": False})
        requests = file_requests(server)
        if mode == "disabled":
            assert not requests
            assert not directory.exists()
        else:
            assert len({request["worker"] for request in requests}) == 8
            if mode == "disk_disabled":
                assert not directory.exists()


@pytest.mark.parametrize("failure", ["malformed_manifest", "malformed_file", "stale"])
def test_invalid_shared_snapshot_falls_back_to_current_http_data(tmp_path, failure):
    import fcntl

    directory = tmp_path / "shared"
    with IdListHTTPFixture() as server:
        with SDKWorkers(server, directory, tmp_path / "seed.log", count=1) as seed:
            wait_for_membership(seed, {"alice": True, "bob": False})
        path = shared_manifest(directory)
        manifest = json.loads(path.read_text())
        if failure == "malformed_manifest":
            path.write_text("not a valid shared manifest")
        elif failure == "malformed_file":
            data_file = path.parent / manifest["lists"]["members"]["data_file"]
            data_file.write_bytes(b"truncated")
        else:
            manifest["successful_refresh_ms"] = int(time() * 1000) - 600_000
            path.write_text(json.dumps(manifest))

        # Hold the real process lock so no SDK writer can repair the fixture.
        # All SDKs must use current HTTP data instead of the invalid/stale snapshot.
        with (path.parent / "leader.lock").open("a+") as lease:
            fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
            server.control({"op": "replace", "users": ["bob"]})
            server.control({"op": "reset_counters"})
            with SDKWorkers(server, directory, tmp_path / "fallback.log") as workers:
                wait_for_membership(workers, {"alice": False, "bob": True})
                assert len({request["worker"] for request in file_requests(server)}) == 8


@pytest.mark.parametrize(
    "flag,environment,expected",
    [(False, None, False), (True, None, True), (False, "true", True),
     (True, "false", False), (True, "", False), (True, "invalid", False)],
)
def test_failed_cold_refresh_keeps_eager_gate_semantics(monkeypatch, flag, environment, expected):
    from statsig_python_core import Statsig, StatsigOptions, StatsigUser

    if environment is None:
        monkeypatch.delenv("STATSIG_PARTIAL_ID_LIST_REFRESH", raising=False)
    else:
        monkeypatch.setenv("STATSIG_PARTIAL_ID_LIST_REFRESH", environment)
    with IdListHTTPFixture({"a": ["member"], "b": ["member"]}) as server:
        server.control({"op": "set_failures", "file_status": {"b-initial": 403}})
        # The failed list is absent: its negative condition keeps the ordinary eager result.
        server.specs["condition_map"]["member-1"]["operator"] = "not_in_segment_list"
        sdk = Statsig("secret-local-partial-refresh", StatsigOptions(
            specs_url=server.url("/v2/download_config_specs"),
            id_lists_url=server.url("/v1/get_id_lists"),
            enable_id_lists=True,
            experimental_flags={"partial_id_list_refresh"} if flag else None,
            id_lists_sync_interval_ms=60_000,
            disable_all_logging=True,
            output_log_level="none",
        ))
        try:
            details = sdk.initialize_with_details().result()
            assert details.is_config_spec_ready
            assert details.is_id_list_ready is False
            user = StatsigUser("member")
            assert sdk.check_gate(user, "a") is expected
            assert sdk.check_gate(user, "b")
        finally:
            sdk.shutdown().wait(10)
