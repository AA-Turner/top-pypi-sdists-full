"""
threatwire.core.pipeline
=========================
ThreatPipeline — convenience class that wires PacketStreamer,
SignatureEngine, and ThreatEventBus into a single ready-to-run pipeline.

Usage::

    pipeline = ThreatPipeline(
        interface="eth0",
        bpf_filter="tcp or udp",
        enable_builtin_rules=True,
    )

    @pipeline.on_alert(severity="high")
    def handle(alert):
        print(alert.rule_name, alert.src_ip)

    pipeline.run()          # blocks; Ctrl-C to stop
    pipeline.run_async()    # returns immediately, runs in background thread
"""

from __future__ import annotations

import logging
import threading
from pathlib import Path
from typing import Callable

from threatwire.core.event_bus import HandlerFn, ThreatEventBus
from threatwire.core.models import AlertSeverity
from threatwire.core.signature_engine import SignatureEngine
from threatwire.core.streamer import PacketStreamer

logger = logging.getLogger(__name__)


class ThreatPipeline:
    """
    Full threatwire pipeline in one object.

    Internally creates and connects:
        PacketStreamer → SignatureEngine → ThreatEventBus

    Quick start::

        with ThreatPipeline(interface="eth0") as p:
            @p.on_alert(severity="critical")
            def handler(alert):
                print(alert)
            p.run()
    """

    def __init__(
        self,
        interface: str | None = None,
        pcap_file: str | Path | None = None,
        bpf_filter: str = "",
        enable_builtin_rules: bool = True,
        rule_path: str | Path | None = None,
        suricata_rules: str | Path | None = None,
        reconstruct_streams: bool = True,
        dedup_window: float = 30.0,
        min_alert_severity: AlertSeverity = AlertSeverity.LOW,
    ) -> None:
        self.streamer = PacketStreamer(
            interface=interface,
            pcap_file=pcap_file,
            bpf_filter=bpf_filter,
            reconstruct_streams=reconstruct_streams,
        )
        self.engine = SignatureEngine(
            rule_path=rule_path,
            suricata_rules=suricata_rules,
            enable_builtin=enable_builtin_rules,
            min_severity=min_alert_severity,
        )
        self.bus = ThreatEventBus(dedup_window=dedup_window)

        self._thread: threading.Thread | None = None

    # ------------------------------------------------------------------
    # Handler registration shortcut
    # ------------------------------------------------------------------

    def on_alert(
        self,
        severity: str | AlertSeverity = "info",
        rule_ids: list[str] | None = None,
        tactic_ids: list[str] | None = None,
    ) -> Callable[[HandlerFn], HandlerFn]:
        """Shortcut for bus.subscribe(...)."""
        return self.bus.subscribe(severity=severity, rule_ids=rule_ids, tactic_ids=tactic_ids)

    # ------------------------------------------------------------------
    # Run modes
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Run the pipeline in the current thread (blocking)."""
        self.bus.start()
        logger.info(
            "ThreatPipeline running — %d rules loaded",
            self.engine.rule_count(),
        )
        try:
            for packet in self.streamer.stream():
                alerts = self.engine.match_all([packet])
                self.bus.publish_many(alerts)
        except KeyboardInterrupt:
            logger.info("ThreatPipeline interrupted by user")
        finally:
            self.streamer.stop()
            self.bus.stop()

    def run_async(self) -> threading.Thread:
        """Run the pipeline in a background daemon thread. Returns the thread."""
        self._thread = threading.Thread(target=self.run, daemon=True, name="threatwire-pipeline")
        self._thread.start()
        return self._thread

    def stop(self) -> None:
        self.streamer.stop()
        self.bus.stop()

    def __enter__(self) -> ThreatPipeline:
        return self

    def __exit__(self, *_) -> None:
        self.stop()

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        return {
            "rules_loaded": self.engine.rule_count(),
            "active_flows": self.streamer.active_flows(),
            "bus": self.bus.stats(),
        }
