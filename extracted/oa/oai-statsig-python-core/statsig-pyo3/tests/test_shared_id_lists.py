"""Shared ID lists with eight real SDKs constructed after fork on Linux."""

from contextlib import contextmanager
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
from time import monotonic, sleep

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
        lazy_load_id_lists=None,
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
            "lazy_load_id_lists": lazy_load_id_lists,
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
    values = {
        user: {"gate": value is True, "config": {} if value is None else {"member": value}}
        for user, value in expected.items()
    }
    deadline = monotonic() + 15
    while True:
        results = workers.command("evaluate", users=list(expected))
        if all(result["values"] == values for result in results.values()):
            return results
        assert monotonic() < deadline, results
        sleep(0.05)


def file_requests(server):
    return [
        request
        for request in server.state()["recent_requests"]
        if request["path"].startswith("/files/")
    ]


def assert_mapped_by_all_workers(workers, base):
    for index, result in workers.command("mapped_files").items():
        assert result["files"] == [str(base)], f"Worker {index} has no shared ID-list map"


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


@pytest.mark.parametrize(
    ("elias_fano", "lazy", "evaluation_cache"),
    [
        (False, False, False),
        (False, True, True),
        (None, False, True),
        (True, True, False),
    ],
    ids=["hash-eager", "hash-lazy", "ef-eager", "ef-lazy"],
)
def test_eight_workers_share_initial_base_and_refresh_independently(
    tmp_path, elias_fano, lazy, evaluation_cache
):
    directory = tmp_path / "shared"
    with IdListHTTPFixture() as server, SDKWorkers(
        server,
        directory,
        tmp_path / "workers.log",
        count=1,
        evaluation_cache=evaluation_cache,
        enable_id_list_elias_fano=elias_fano,
        lazy_load_id_lists=lazy,
        enable_logging=True,
    ) as workers:
        wait_for_membership(workers, {"alice": True, "steady": True, "bob": False})
        [base] = directory.rglob("*.ids")
        with base.open("rb") as image:
            image.seek(8)  # Skip the file magic.
            assert int.from_bytes(image.read(4), "little") == (2 if elias_fano is False else 3)

        joining = range(1, 8)
        workers.command("start_worker", workers=joining)
        if lazy:
            readers = workers.command("mapped_files", workers=joining)
            assert all(not reader["files"] for reader in readers.values())
        wait_for_membership(workers, {"alice": True, "steady": True, "bob": False})
        workers.command("evaluate", users=["alice", "bob"], hold_results=True)
        assert len(file_requests(server)) == 1
        assert_mapped_by_all_workers(workers, base)
        assert_events_delivered(workers, server, "initialized")

        initial_size = server.state()["manifest"]["members"]["size"]
        server.control({"op": "append", "add_users": ["bob"], "remove_users": ["alice"]})
        expected = {"alice": False, "steady": True, "bob": True}
        wait_for_membership(workers, expected)
        tails = file_requests(server)[1:]
        assert {request["worker"] for request in tails} == {
            f"shared-id-list-worker-{i}" for i in workers.active
        }
        assert all(request["start"] == initial_size for request in tails)
        assert_mapped_by_all_workers(workers, base)

        workers.command("kill", workers=[0])
        workers.command("shutdown", workers=[1])
        workers.command("drop", workers=[2])
        workers.command("start_worker", workers=[0])
        workers.command("restart", workers=[1, 2])
        wait_for_membership(workers, expected)
        assert all(request["start"] == initial_size for request in file_requests(server)[1:])
        assert_mapped_by_all_workers(workers, base)
        assert_events_delivered(workers, server, "restarted")

        server.control({"op": "replace", "users": ["carol"]})
        expected = {"alice": False, "steady": False, "bob": False, "carol": True}
        wait_for_membership(workers, expected)
        assert file_requests(server)[-1]["start"] == 0

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

        for result in workers.command("held_results", workers=range(3, 8)).values():
            assert result["values"] == [
                {"gate": True, "config": {"member": True}},
                {"gate": False, "config": {"member": False}},
            ]

        downloads_before_removal = len(file_requests(server))
        server.control({"op": "set_manifest", "names": []})
        # Lazy reports unknown membership. Eager uses the config default.
        wait_for_membership(workers, dict.fromkeys(expected, None if lazy else False))
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


def test_truncated_base_is_downloaded_again_and_repaired(tmp_path):
    directory = tmp_path / "shared"
    with IdListHTTPFixture() as server:
        with SDKWorkers(server, directory, tmp_path / "seed.log", count=1) as seed:
            wait_for_membership(seed, {"alice": True, "bob": False})
        [base] = directory.rglob("*.ids")
        base.write_bytes(b"truncated")
        with SDKWorkers(server, directory, tmp_path / "repair.log", count=1) as workers:
            wait_for_membership(workers, {"alice": True, "bob": False})
            assert [request["start"] for request in file_requests(server)] == [0, 0]
            workers.command("start_worker", workers=[1])
            wait_for_membership(workers, {"alice": True, "bob": False})
            assert len(file_requests(server)) == 2


@contextmanager
def eager_sdk(
    server, *, partial_refresh=False, directory=None, sync_interval_ms=60_000
):
    from statsig_python_core import Statsig, StatsigOptions

    sdk = Statsig(
        "secret-local-partial-refresh",
        StatsigOptions(
            specs_url=server.url("/v2/download_config_specs"),
            id_lists_url=server.url("/v1/get_id_lists"),
            enable_id_lists=True,
            shared_id_lists_dir=str(directory) if directory is not None else None,
            experimental_flags={"partial_id_list_refresh"} if partial_refresh else None,
            id_lists_sync_interval_ms=sync_interval_ms,
            disable_all_logging=True,
            output_log_level="none",
        ),
    )
    try:
        yield sdk, sdk.initialize_with_details().result()
    finally:
        sdk.shutdown().wait(10)


@pytest.mark.parametrize(
    "flag,environment,expected",
    [(False, None, False), (True, None, True), (False, "true", True),
     (True, "false", False), (True, "", False), (True, "invalid", False)],
)
def test_failed_cold_refresh_keeps_eager_gate_semantics(monkeypatch, flag, environment, expected):
    from statsig_python_core import StatsigUser

    if environment is None:
        monkeypatch.delenv("STATSIG_PARTIAL_ID_LIST_REFRESH", raising=False)
    else:
        monkeypatch.setenv("STATSIG_PARTIAL_ID_LIST_REFRESH", environment)
    with IdListHTTPFixture({"a": ["member"], "b": ["member"]}) as server:
        server.control({"op": "set_failures", "file_status": {"b-initial": 403}})
        # The failed list is absent: its negative condition keeps the ordinary eager result.
        server.specs["condition_map"]["member-1"]["operator"] = "not_in_segment_list"
        with eager_sdk(server, partial_refresh=flag) as (sdk, details):
            assert details.is_config_spec_ready
            assert details.is_id_list_ready is False
            user = StatsigUser("member")
            assert sdk.check_gate(user, "a") is expected
            assert sdk.check_gate(user, "b")


@pytest.mark.parametrize("partial_refresh", [False, True], ids=["default", "partial"])
def test_eager_join_with_cached_base_and_failed_replacement(
    tmp_path, monkeypatch, partial_refresh
):
    from statsig_python_core import StatsigUser

    monkeypatch.delenv("STATSIG_PARTIAL_ID_LIST_REFRESH", raising=False)
    member = StatsigUser("member")
    with IdListHTTPFixture({"a": ["member"], "b": ["member"]}) as server:
        with eager_sdk(server, directory=tmp_path) as (_, details):
            assert details.is_id_list_ready

        server.control({"op": "reset_counters"})
        server.control(
            {"op": "replace", "list": "b", "file_id": "b-new", "users": ["new"]}
        )
        server.control({"op": "set_failures", "file_status": {"b-new": 403}})
        with eager_sdk(
            server,
            directory=tmp_path,
            partial_refresh=partial_refresh,
            sync_interval_ms=1000,
        ) as (sdk, details):
            assert details.is_config_spec_ready
            assert details.is_id_list_ready is False
            assert sdk.check_gate(member, "a") is partial_refresh
            assert not sdk.check_gate(member, "b")
            assert {r["status"] for r in file_requests(server)} == {403}

            server.control({"op": "set_failures"})
            deadline = monotonic() + 10
            while not sdk.check_gate(StatsigUser("new"), "b"):
                assert monotonic() < deadline, "B did not recover"
                sleep(0.05)
            assert sdk.check_gate(member, "a")
            assert {r["path"] for r in file_requests(server)} == {"/files/b-new"}
