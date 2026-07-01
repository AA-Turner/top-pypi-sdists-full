"""
threatwire.core.models
======================
Shared data models used across the entire pipeline.
All models are dataclasses — serializable to dict/JSON for ECS and SIEM output.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Protocol(str, Enum):
    TCP = "tcp"
    UDP = "udp"
    ICMP = "icmp"
    DNS = "dns"
    HTTP = "http"
    TLS = "tls"
    SMB = "smb"
    UNKNOWN = "unknown"


class AlertSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def numeric(self) -> int:
        return {"info": 1, "low": 2, "medium": 3, "high": 4, "critical": 5}[self.value]

    def __ge__(self, other: AlertSeverity) -> bool:
        return self.numeric >= other.numeric

    def __gt__(self, other: AlertSeverity) -> bool:
        return self.numeric > other.numeric

    def __le__(self, other: AlertSeverity) -> bool:
        return self.numeric <= other.numeric

    def __lt__(self, other: AlertSeverity) -> bool:
        return self.numeric < other.numeric


class TCPFlag(str, Enum):
    SYN = "SYN"
    ACK = "ACK"
    FIN = "FIN"
    RST = "RST"
    PSH = "PSH"
    URG = "URG"


# ---------------------------------------------------------------------------
# Packet model
# ---------------------------------------------------------------------------

@dataclass
class Packet:
    """
    Normalized representation of a decoded network packet.
    Produced by PacketStreamer after protocol decoding and stream reassembly.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    # Network layer
    src_ip: str = ""
    dst_ip: str = ""
    protocol: Protocol = Protocol.UNKNOWN

    # Transport layer
    src_port: int | None = None
    dst_port: int | None = None
    flags: list[TCPFlag] = field(default_factory=list)
    ttl: int | None = None

    # Payload
    payload: bytes = b""
    payload_len: int = 0

    # Stream metadata (set by stream reassembler)
    stream_id: str | None = None
    is_reassembled: bool = False
    fragment_count: int = 1

    # Decoded application layer (set by protocol decoders)
    decoded: dict | None = None

    def has_flag(self, flag: TCPFlag) -> bool:
        return flag in self.flags

    def is_syn_only(self) -> bool:
        return TCPFlag.SYN in self.flags and TCPFlag.ACK not in self.flags

    def to_dict(self) -> dict:
        d = asdict(self)
        d["protocol"] = self.protocol.value
        d["flags"] = [f.value for f in self.flags]
        d["payload"] = self.payload.hex()
        return d


# ---------------------------------------------------------------------------
# Alert model
# ---------------------------------------------------------------------------

@dataclass
class ThreatAlert:
    """
    A threat detection event produced by SignatureEngine or other detectors.
    Structured for ECS (Elastic Common Schema) and MITRE ATT&CK field mapping.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)

    # Classification
    rule_id: str = ""
    rule_name: str = ""
    severity: AlertSeverity = AlertSeverity.MEDIUM
    confidence: float = 0.0          # 0.0 – 1.0

    # MITRE ATT&CK
    technique_id: str = ""           # e.g. "T1071.004"
    tactic_id: str = ""              # e.g. "TA0011"
    tactic_name: str = ""

    # Context
    src_ip: str = ""
    dst_ip: str = ""
    src_port: int | None = None
    dst_port: int | None = None
    protocol: str = ""
    description: str = ""

    # Evidence
    matched_pattern: str = ""
    packet_id: str = ""
    raw_payload_hex: str = ""

    # Deduplication
    dedup_key: str = ""              # set by ThreatEventBus

    def to_dict(self) -> dict:
        d = asdict(self)
        d["severity"] = self.severity.value
        return d

    def to_ecs(self) -> dict:
        """Elastic Common Schema compatible output."""
        return {
            "@timestamp": self.timestamp,
            "event": {
                "id": self.id,
                "kind": "alert",
                "category": ["intrusion_detection"],
                "severity": self.severity.numeric,
                "risk_score": round(self.confidence * 100),
            },
            "rule": {
                "id": self.rule_id,
                "name": self.rule_name,
                "description": self.description,
            },
            "threat": {
                "technique": {"id": self.technique_id},
                "tactic": {"id": self.tactic_id, "name": self.tactic_name},
                "framework": "MITRE ATT&CK",
            },
            "source": {"ip": self.src_ip, "port": self.src_port},
            "destination": {"ip": self.dst_ip, "port": self.dst_port},
            "network": {"protocol": self.protocol},
            "threatwire": {
                "matched_pattern": self.matched_pattern,
                "confidence": self.confidence,
                "packet_id": self.packet_id,
            },
        }


# ---------------------------------------------------------------------------
# Flow tracking
# ---------------------------------------------------------------------------

@dataclass
class NetworkFlow:
    """
    Tracks state for a bidirectional TCP/UDP flow across multiple packets.
    Used by PacketStreamer's stream reassembler.
    """
    flow_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    src_ip: str = ""
    dst_ip: str = ""
    src_port: int = 0
    dst_port: int = 0
    protocol: Protocol = Protocol.UNKNOWN

    start_time: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    packet_count: int = 0
    byte_count: int = 0

    # TCP state machine
    syn_count: int = 0
    syn_ack_count: int = 0
    is_established: bool = False
    is_closed: bool = False

    # Reassembled payload chunks
    payload_chunks: list[bytes] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.last_seen - self.start_time

    @property
    def full_payload(self) -> bytes:
        return b"".join(self.payload_chunks)

    def update(self, packet: Packet) -> None:
        self.last_seen = packet.timestamp
        self.packet_count += 1
        self.byte_count += packet.payload_len
        if packet.has_flag(TCPFlag.SYN):
            self.syn_count += 1
        if packet.has_flag(TCPFlag.SYN) and packet.has_flag(TCPFlag.ACK):
            self.syn_ack_count += 1
            self.is_established = True
        if packet.has_flag(TCPFlag.FIN) or packet.has_flag(TCPFlag.RST):
            self.is_closed = True
        if packet.payload:
            self.payload_chunks.append(packet.payload)
