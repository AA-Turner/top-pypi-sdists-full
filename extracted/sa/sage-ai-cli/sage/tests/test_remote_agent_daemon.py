"""Tests for RemoteAgentDaemon — the OpenClaw-style unified bridge runner.

One daemon process subscribes to multiple messaging bridges
(iMessage/SMS, Telegram, Discord) and routes every incoming message
through ONE sage agent. The reply goes back via the same channel.

Result: users can text/DM sage from their phone (any platform) and sage
executes commands / runs the agent loop on their desktop — "run all the
apps on a computer from your mobile phone".

TDD: tests describe the multi-bridge orchestration contract.
Individual bridges (TelegramBridge, DiscordBridge) are already tested
in test_messaging_bridges.py; here we focus on the COORDINATION layer.
"""

from __future__ import annotations

from threading import Event
from unittest.mock import MagicMock

import pytest

from sage.core.remote_agent_daemon import (
    BridgeRunner,
    RemoteAgentDaemon,
)
from sage.core.messaging_bridges import BridgeMessage


# ── BridgeRunner contract ────────────────────────────────────────────────────


class TestBridgeRunner:
    """BridgeRunner wraps a bridge with a start/stop/poll lifecycle.
    Each bridge runs in its own thread so a wedged Telegram poll doesn't
    block iMessage delivery."""

    def test_runner_records_name(self):
        runner = BridgeRunner(
            name="test-bridge",
            poll_once=lambda: None,
        )
        assert runner.name == "test-bridge"

    def test_start_calls_poll_repeatedly_until_stop(self):
        poll_count = [0]
        def poll_once():
            poll_count[0] += 1

        runner = BridgeRunner(name="x", poll_once=poll_once, poll_interval=0.01)
        runner.start()
        # Let it tick a few times
        import time
        time.sleep(0.05)
        runner.stop()
        assert poll_count[0] >= 2

    def test_exception_in_poll_does_not_crash_runner(self):
        """Bridge-specific errors (network blips, malformed messages)
        must be isolated — one bridge's failure shouldn't take down
        the whole daemon."""
        poll_count = [0]
        def flaky_poll():
            poll_count[0] += 1
            if poll_count[0] == 1:
                raise ConnectionError("transient network blip")

        runner = BridgeRunner(name="x", poll_once=flaky_poll, poll_interval=0.01)
        runner.start()
        import time
        time.sleep(0.1)
        runner.stop()
        # Should have ticked multiple times despite the first failure
        assert poll_count[0] >= 2


# ── RemoteAgentDaemon ────────────────────────────────────────────────────────


class TestRemoteAgentDaemon:
    def test_daemon_starts_all_registered_bridges(self):
        b1_started = Event()
        b2_started = Event()
        b1 = BridgeRunner(name="b1", poll_once=lambda: b1_started.set(), poll_interval=0.01)
        b2 = BridgeRunner(name="b2", poll_once=lambda: b2_started.set(), poll_interval=0.01)

        daemon = RemoteAgentDaemon(
            agent=MagicMock(return_value="reply"),
            bridges=[b1, b2],
        )
        daemon.start()
        try:
            assert b1_started.wait(timeout=1.0)
            assert b2_started.wait(timeout=1.0)
        finally:
            daemon.stop()

    def test_daemon_stop_halts_all_bridges(self):
        ticked_after_stop = [False, False]
        def make_poll(i):
            def p():
                if not daemon.is_running:
                    ticked_after_stop[i] = True
            return p

        daemon = RemoteAgentDaemon(
            agent=MagicMock(return_value="reply"),
            bridges=[],
        )
        b1 = BridgeRunner(name="b1", poll_once=make_poll(0), poll_interval=0.01)
        b2 = BridgeRunner(name="b2", poll_once=make_poll(1), poll_interval=0.01)
        daemon._bridges = [b1, b2]

        daemon.start()
        import time
        time.sleep(0.05)
        daemon.stop()
        # Brief grace period for threads to notice the stop signal
        time.sleep(0.05)
        # The poll functions checked is_running and shouldn't have
        # observed a tick after stop. (Tolerant of one in-flight tick.)
        assert not all(ticked_after_stop)

    def test_handle_message_routes_through_agent_and_returns_reply(self):
        agent = MagicMock(return_value="agent answer")
        daemon = RemoteAgentDaemon(agent=agent, bridges=[])

        msg = BridgeMessage(
            platform="telegram", chat_id="c1", sender_id="u1",
            sender_name="alice", text="hello",
        )
        reply = daemon.handle_message(msg)
        agent.assert_called_once_with(msg)
        assert reply == "agent answer"

    def test_handle_message_serializes_agent_calls(self):
        """Multiple bridges may deliver messages concurrently. The agent
        loop is stateful (conversation context, file ops) — calling it
        from multiple threads simultaneously would corrupt state. The
        daemon serializes through a single lock."""
        import threading
        import time

        call_order: list[str] = []
        in_progress = [False]
        def slow_agent(msg):
            nonlocal in_progress
            if in_progress[0]:
                # If we got here while another call was active, that's a bug
                call_order.append(f"CONCURRENT_{msg.text}")
                return "concurrent-bug"
            in_progress[0] = True
            call_order.append(f"start_{msg.text}")
            time.sleep(0.01)
            call_order.append(f"end_{msg.text}")
            in_progress[0] = False
            return f"answered_{msg.text}"

        daemon = RemoteAgentDaemon(agent=slow_agent, bridges=[])
        threads = []
        for label in ("A", "B", "C"):
            msg = BridgeMessage(
                platform="t", chat_id="c", sender_id="u", sender_name="x", text=label,
            )
            t = threading.Thread(target=daemon.handle_message, args=(msg,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        # No CONCURRENT_* entries should appear
        assert not any(e.startswith("CONCURRENT_") for e in call_order), call_order
        # And every "start" should be followed immediately by its own "end"
        for i in range(0, len(call_order), 2):
            label = call_order[i].split("_")[1]
            assert call_order[i + 1] == f"end_{label}"

    def test_daemon_is_running_flag(self):
        daemon = RemoteAgentDaemon(
            agent=MagicMock(return_value="reply"),
            bridges=[],
        )
        assert not daemon.is_running
        daemon.start()
        try:
            assert daemon.is_running
        finally:
            daemon.stop()
        assert not daemon.is_running

    def test_daemon_status_reports_bridge_names(self):
        b1 = BridgeRunner(name="telegram", poll_once=lambda: None)
        b2 = BridgeRunner(name="discord", poll_once=lambda: None)
        b3 = BridgeRunner(name="imessage", poll_once=lambda: None)
        daemon = RemoteAgentDaemon(
            agent=MagicMock(return_value="reply"),
            bridges=[b1, b2, b3],
        )
        status = daemon.status()
        # Each bridge listed by name
        assert "telegram" in status["bridges"]
        assert "discord" in status["bridges"]
        assert "imessage" in status["bridges"]
        assert status["running"] is False  # not started yet
