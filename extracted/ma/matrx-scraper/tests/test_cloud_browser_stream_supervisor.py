from __future__ import annotations

import signal
import socket
import subprocess
from unittest.mock import MagicMock, Mock, patch

from matrx_scraper.cloud_browser.streaming.supervisor import SelkiesSupervisor


def test_selkies_supervisor_owns_and_stops_the_launcher_process_group() -> None:
    process = Mock(spec=subprocess.Popen)
    process.pid = 4242
    process.poll.return_value = None
    process.wait.return_value = 0

    with (
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.subprocess.Popen",
            return_value=process,
        ) as popen,
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.socket.create_connection",
            return_value=MagicMock(),
        ),
        patch("matrx_scraper.cloud_browser.streaming.supervisor.os.killpg") as killpg,
    ):
        supervisor = SelkiesSupervisor()
        supervisor.start()
        supervisor.stop()

    assert popen.call_args.kwargs["start_new_session"] is True
    killpg.assert_called_once_with(4242, signal.SIGTERM)
    process.wait.assert_called_once_with(timeout=0.75)


def test_selkies_supervisor_kills_the_group_after_graceful_timeout() -> None:
    process = Mock(spec=subprocess.Popen)
    process.pid = 4343
    process.poll.return_value = None
    process.wait.side_effect = [subprocess.TimeoutExpired("selkies", 0.75), 0]

    with (
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.subprocess.Popen",
            return_value=process,
        ),
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.socket.create_connection",
            return_value=MagicMock(),
        ),
        patch("matrx_scraper.cloud_browser.streaming.supervisor.os.killpg") as killpg,
    ):
        supervisor = SelkiesSupervisor()
        supervisor.start()
        supervisor.stop()

    assert killpg.call_args_list[0].args == (4343, signal.SIGTERM)
    assert killpg.call_args_list[1].args == (4343, signal.SIGKILL)


def test_selkies_supervisor_waits_for_listener_before_returning() -> None:
    process = Mock(spec=subprocess.Popen)
    process.pid = 4444
    process.poll.return_value = None
    connection = MagicMock()

    with (
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.subprocess.Popen",
            return_value=process,
        ),
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.socket.create_connection",
            side_effect=[ConnectionRefusedError(), connection],
        ) as connect,
        patch("matrx_scraper.cloud_browser.streaming.supervisor.time.sleep") as sleep,
    ):
        SelkiesSupervisor().start()

    assert connect.call_count == 2
    sleep.assert_called_once_with(0.05)


def test_selkies_supervisor_fails_closed_when_listener_never_starts() -> None:
    process = Mock(spec=subprocess.Popen)
    process.pid = 4545
    process.poll.return_value = None
    process.wait.return_value = 0

    with (
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.subprocess.Popen",
            return_value=process,
        ),
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.socket.create_connection",
            side_effect=socket.timeout,
        ),
        patch(
            "matrx_scraper.cloud_browser.streaming.supervisor.time.monotonic",
            side_effect=[0.0, 1.0, 9.0],
        ),
        patch("matrx_scraper.cloud_browser.streaming.supervisor.time.sleep"),
        patch("matrx_scraper.cloud_browser.streaming.supervisor.os.killpg") as killpg,
    ):
        try:
            SelkiesSupervisor().start()
        except RuntimeError as exc:
            assert str(exc) == "Selkies did not become ready during startup"
        else:
            raise AssertionError("startup unexpectedly succeeded")

    killpg.assert_called_once_with(4545, signal.SIGTERM)
