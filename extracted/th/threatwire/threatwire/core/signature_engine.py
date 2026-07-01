"""
threatwire.core.signature_engine
=================================
SignatureEngine — matches packet payloads and flow metadata against a rule
library using Aho-Corasick multi-pattern matching for high throughput.

Ships with 1,200+ built-in rules covering:
  - Common exploit kits
  - C2 beaconing intervals and URI patterns
  - Protocol abuse patterns
  - DNS tunneling indicators

Supports Suricata rule syntax for external rule imports.

Attack scenario addressed:
    Emotet beacons via HTTP POST with randomised User-Agent strings but a
    predictable 300-second interval and fixed URI structure buried in junk.
    SignatureEngine matches the URI structure AND beaconing interval
    simultaneously — something a pure payload or pure frequency detector
    misses independently.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from threatwire.core.models import AlertSeverity, Packet, ThreatAlert
from threatwire.rules.loader import RuleLoader
from threatwire.rules.suricata import SuricataParser
from threatwire.utils.exceptions import RuleLoadError

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Rule model
# ---------------------------------------------------------------------------

@dataclass
class Rule:
    """A single detection rule in threatwire's internal format."""
    rule_id: str
    name: str
    severity: AlertSeverity
    description: str

    # MITRE ATT&CK
    technique_id: str = ""
    tactic_id: str = ""
    tactic_name: str = ""

    # Matching criteria (all present criteria must match — implicit AND)
    payload_patterns: list[bytes] = field(default_factory=list)   # raw byte patterns
    regex_patterns: list[str] = field(default_factory=list)       # regex on payload
    dst_ports: list[int] = field(default_factory=list)
    src_ports: list[int] = field(default_factory=list)
    protocols: list[str] = field(default_factory=list)

    # Temporal / flow matching
    beacon_interval_s: float | None = None                      # C2 beacon interval check
    beacon_tolerance_s: float = 30.0
    min_payload_len: int = 0
    max_payload_len: int = 0                                       # 0 = no limit

    # Confidence for this rule's matches
    base_confidence: float = 0.8

    def matches(self, packet: Packet, flow_intervals: list[float] | None = None) -> bool:
        """
        Returns True if this rule matches the given packet.
        All defined criteria must match (AND semantics).
        """
        # Protocol filter
        if self.protocols and packet.protocol.value not in self.protocols:
            return False

        # Port filters
        if self.dst_ports and packet.dst_port not in self.dst_ports:
            return False
        if self.src_ports and packet.src_port not in self.src_ports:
            return False

        # Payload length
        if self.min_payload_len and packet.payload_len < self.min_payload_len:
            return False
        if self.max_payload_len and packet.payload_len > self.max_payload_len:
            return False

        # Byte pattern matching
        for pattern in self.payload_patterns:
            if pattern not in packet.payload:
                return False

        # Regex matching (on decoded utf-8 lossy)
        payload_str = packet.payload.decode("utf-8", errors="replace")
        for rx in self.regex_patterns:
            if not re.search(rx, payload_str, re.IGNORECASE | re.DOTALL):
                return False

        # Beacon interval check (requires flow_intervals from engine)
        if self.beacon_interval_s is not None:
            if not flow_intervals or not self._check_beacon(flow_intervals):
                return False

        return True

    def _check_beacon(self, intervals: list[float]) -> bool:
        if len(intervals) < 2:
            return False
        if self.beacon_interval_s is None:
            return False
        target: float = self.beacon_interval_s
        tol = self.beacon_tolerance_s
        matching = sum(1 for iv in intervals if abs(iv - target) <= tol)
        return matching >= max(2, len(intervals) // 2)


# ---------------------------------------------------------------------------
# Multi-pattern index (Aho-Corasick with pure-Python fallback)
# ---------------------------------------------------------------------------

class PatternIndex:
    """
    Wraps pyahocorasick for O(n) multi-pattern search.
    Falls back to naive search if pyahocorasick is not installed.
    """

    def __init__(self) -> None:
        self._automaton = None
        self._patterns: dict[bytes, list[str]] = {}   # pattern → [rule_id, ...]
        self._use_aho = False
        self._build_attempted = False

    def add_pattern(self, pattern: bytes, rule_id: str) -> None:
        if pattern not in self._patterns:
            self._patterns[pattern] = []
        self._patterns[pattern].append(rule_id)
        self._build_attempted = False   # invalidate

    def build(self) -> None:
        """Build the Aho-Corasick automaton. Call after all patterns are added."""
        try:
            import ahocorasick  # type: ignore
            A = ahocorasick.Automaton()
            for i, (pattern, rule_ids) in enumerate(self._patterns.items()):
                A.add_word(pattern, (i, pattern, rule_ids))
            A.make_automaton()
            self._automaton = A
            self._use_aho = True
            logger.debug("Aho-Corasick automaton built with %d patterns", len(self._patterns))
        except ImportError:
            logger.warning(
                "pyahocorasick not installed — falling back to naive pattern search. "
                "Install it for 10-100x better throughput: pip install pyahocorasick"
            )
            self._use_aho = False
        self._build_attempted = True

    def search(self, payload: bytes) -> set[str]:
        """Return set of rule IDs whose patterns appear in payload."""
        if not self._build_attempted:
            self.build()

        matched_rule_ids: set[str] = set()

        if self._use_aho and self._automaton:
            for _, (_, _pattern, rule_ids) in self._automaton.iter(payload):
                matched_rule_ids.update(rule_ids)
        else:
            for pattern, rule_ids in self._patterns.items():
                if payload.find(pattern) != -1:
                    matched_rule_ids.update(rule_ids)

        return matched_rule_ids


# ---------------------------------------------------------------------------
# Flow interval tracker (for beacon detection)
# ---------------------------------------------------------------------------

class BeaconTracker:
    """
    Tracks per-flow packet arrival times to detect C2 beaconing intervals.
    Keeps a sliding window of inter-arrival times per (src_ip, dst_ip, dst_port).
    """

    def __init__(self, window: int = 20) -> None:
        self._window = window
        self._timestamps: dict[str, list[float]] = {}

    def record(self, packet: Packet) -> list[float]:
        """Record packet timestamp and return current list of inter-arrival intervals."""
        key = f"{packet.src_ip}->{packet.dst_ip}:{packet.dst_port}"
        timestamps = self._timestamps.setdefault(key, [])
        timestamps.append(packet.timestamp)
        if len(timestamps) > self._window + 1:
            timestamps.pop(0)
        intervals = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
        return intervals


# ---------------------------------------------------------------------------
# SignatureEngine
# ---------------------------------------------------------------------------

class SignatureEngine:
    """
    Matches packet payloads and flow metadata against a rule library.

    Usage::

        engine = SignatureEngine(enable_builtin=True)
        alert = engine.match(packet)
        if alert:
            print(alert.severity, alert.technique_id)

    Loading custom rules from a directory::

        engine = SignatureEngine(
            rule_path="/etc/threatwire/rules",
            enable_builtin=True,
        )

    Loading Suricata rules::

        engine = SignatureEngine(
            suricata_rules="/etc/suricata/rules/emerging-malware.rules"
        )

    Batch processing::

        alerts = engine.match_all([pkt1, pkt2, pkt3])
    """

    def __init__(
        self,
        rule_path: str | Path | None = None,
        suricata_rules: str | Path | None = None,
        enable_builtin: bool = True,
        min_severity: AlertSeverity = AlertSeverity.LOW,
        max_alerts_per_rule: int = 0,    # 0 = unlimited
    ) -> None:
        self.min_severity = min_severity
        self.max_alerts_per_rule = max_alerts_per_rule

        self._rules: dict[str, Rule] = {}
        self._pattern_index = PatternIndex()
        self._beacon_tracker = BeaconTracker()
        self._alert_counts: dict[str, int] = {}

        if enable_builtin:
            self._load_builtin_rules()

        if rule_path:
            self._load_from_path(Path(rule_path))

        if suricata_rules:
            self._load_suricata(Path(suricata_rules))

        self._pattern_index.build()
        logger.info("SignatureEngine ready — %d rules loaded", len(self._rules))

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def match(self, packet: Packet) -> ThreatAlert | None:
        """
        Match a single packet against all loaded rules.
        Returns the highest-severity alert, or None if no rule matches.
        """
        alerts = self.match_all([packet])
        if not alerts:
            return None
        return max(alerts, key=lambda a: a.severity.numeric)

    def match_all(self, packets: list[Packet]) -> list[ThreatAlert]:
        """Match a list of packets. Returns all alerts produced."""
        alerts = []
        for packet in packets:
            alerts.extend(self._process_packet(packet))
        return alerts

    def add_rule(self, rule: Rule) -> None:
        """Add a single rule at runtime."""
        self._rules[rule.rule_id] = rule
        for pattern in rule.payload_patterns:
            self._pattern_index.add_pattern(pattern, rule.rule_id)
        self._pattern_index.build()

    def rule_count(self) -> int:
        return len(self._rules)

    def loaded_rule_ids(self) -> list[str]:
        return list(self._rules.keys())

    # ------------------------------------------------------------------
    # Internal matching
    # ------------------------------------------------------------------

    def _process_packet(self, packet: Packet) -> list[ThreatAlert]:
        alerts = []

        # Beacon interval tracking (for C2 detection)
        flow_intervals = self._beacon_tracker.record(packet)

        # Phase 1: fast pattern pre-filter
        candidate_rule_ids = self._pattern_index.search(packet.payload)

        # Phase 2: also check rules with no payload patterns (port/protocol/beacon only)
        no_payload_rules = {
            rid for rid, r in self._rules.items() if not r.payload_patterns
        }
        candidate_rule_ids |= no_payload_rules

        # Phase 3: full rule evaluation on candidates
        for rule_id in candidate_rule_ids:
            rule = self._rules.get(rule_id)
            if rule is None:
                continue
            if rule.severity < self.min_severity:
                continue
            if self.max_alerts_per_rule:
                if self._alert_counts.get(rule_id, 0) >= self.max_alerts_per_rule:
                    continue
            if rule.matches(packet, flow_intervals):
                alert = self._build_alert(rule, packet)
                alerts.append(alert)
                self._alert_counts[rule_id] = self._alert_counts.get(rule_id, 0) + 1

        return alerts

    @staticmethod
    def _build_alert(rule: Rule, packet: Packet) -> ThreatAlert:
        matched_pattern = ""
        for p in rule.payload_patterns:
            if p in packet.payload:
                matched_pattern = p.decode("utf-8", errors="replace")
                break

        return ThreatAlert(
            rule_id=rule.rule_id,
            rule_name=rule.name,
            severity=rule.severity,
            confidence=rule.base_confidence,
            technique_id=rule.technique_id,
            tactic_id=rule.tactic_id,
            tactic_name=rule.tactic_name,
            src_ip=packet.src_ip,
            dst_ip=packet.dst_ip,
            src_port=packet.src_port,
            dst_port=packet.dst_port,
            protocol=packet.protocol.value,
            description=rule.description,
            matched_pattern=matched_pattern,
            packet_id=packet.id,
            raw_payload_hex=packet.payload[:64].hex(),
            dedup_key=f"{rule.rule_id}:{packet.src_ip}:{packet.dst_ip}",
        )

    # ------------------------------------------------------------------
    # Rule loading
    # ------------------------------------------------------------------

    def _load_builtin_rules(self) -> None:
        rules = RuleLoader.load_builtin()
        for rule in rules:
            self._rules[rule.rule_id] = rule
            for pattern in rule.payload_patterns:
                self._pattern_index.add_pattern(pattern, rule.rule_id)
        logger.debug("Loaded %d built-in rules", len(rules))

    def _load_from_path(self, path: Path) -> None:
        if not path.exists():
            raise RuleLoadError(f"Rule path does not exist: {path}")
        rules = RuleLoader.load_from_path(path)
        for rule in rules:
            self._rules[rule.rule_id] = rule
            for pattern in rule.payload_patterns:
                self._pattern_index.add_pattern(pattern, rule.rule_id)
        logger.debug("Loaded %d rules from %s", len(rules), path)

    def _load_suricata(self, path: Path) -> None:
        if not path.exists():
            raise RuleLoadError(f"Suricata rule file does not exist: {path}")
        rules = SuricataParser.parse_file(path)
        for rule in rules:
            self._rules[rule.rule_id] = rule
            for pattern in rule.payload_patterns:
                self._pattern_index.add_pattern(pattern, rule.rule_id)
        logger.debug("Loaded %d Suricata rules from %s", len(rules), path)
