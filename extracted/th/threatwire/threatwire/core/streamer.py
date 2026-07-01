"""
threatwire.core.streamer
========================
PacketStreamer — live and PCAP-file packet ingestion with BPF filter support.

Decodes Ethernet → IP → TCP/UDP/ICMP into structured Packet objects.
Normalizes fragmented streams and out-of-order segments via StreamReassembler
before packets reach the analysis stage.

Attack scenario addressed:
    Slow SYN scan (1 pkt/sec) to evade threshold detectors + DNS C2 tunneling.
    PacketStreamer reconstructs the full TCP state machine and hands the
    reassembled DNS stream to SignatureEngine for C2 domain matching.

Dependencies (optional — graceful fallback to pcap reading without live capture):
    pip install scapy
"""

from __future__ import annotations

import logging
import time
from collections import defaultdict
from collections.abc import Generator, Iterator
from pathlib import Path

from threatwire.core.models import (
    NetworkFlow,
    Packet,
    Protocol,
    TCPFlag,
)
from threatwire.protocols.decoder import ProtocolDecoder
from threatwire.utils.exceptions import (
    InterfaceError,
    PcapReadError,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Stream reassembler
# ---------------------------------------------------------------------------

class StreamReassembler:
    """
    Tracks per-flow state and reassembles TCP streams from out-of-order
    or fragmented packets.

    Key capability: detects slow SYN scans (many SYN-only packets over
    a long time window) that per-packet threshold detectors miss entirely.
    """

    def __init__(
        self,
        flow_timeout: float = 120.0,
        max_flows: int = 100_000,
        syn_scan_threshold: int = 5,
        syn_scan_window: float = 60.0,
    ) -> None:
        self.flow_timeout = flow_timeout
        self.max_flows = max_flows
        self.syn_scan_threshold = syn_scan_threshold
        self.syn_scan_window = syn_scan_window

        self._flows: dict[str, NetworkFlow] = {}
        self._syn_timestamps: dict[str, list[float]] = defaultdict(list)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(self, packet: Packet) -> tuple[Packet, NetworkFlow | None]:
        """
        Update flow state with this packet.
        Returns the enriched packet and the associated NetworkFlow.
        Marks packet.stream_id and packet.is_reassembled if part of a stream.
        """
        flow_key = self._flow_key(packet)
        flow = self._flows.get(flow_key)

        if flow is None:
            flow = self._create_flow(packet, flow_key)

        flow.update(packet)
        packet.stream_id = flow.flow_id
        packet.is_reassembled = flow.packet_count > 1

        # Track SYN-only packets for slow scan detection
        if packet.is_syn_only():
            self._syn_timestamps[packet.src_ip].append(packet.timestamp)
            self._expire_syn_timestamps(packet.src_ip, packet.timestamp)

        self._maybe_evict_stale_flows(packet.timestamp)
        return packet, flow

    def is_slow_syn_scan(self, src_ip: str, at_time: float | None = None) -> bool:
        """
        Returns True if src_ip has sent >= syn_scan_threshold SYN-only packets
        within the syn_scan_window without completing a handshake.
        """
        at_time = at_time or time.time()
        self._expire_syn_timestamps(src_ip, at_time)
        timestamps = self._syn_timestamps.get(src_ip, [])
        if len(timestamps) < self.syn_scan_threshold:
            return False
        # Check that none of these flows completed a handshake
        suspected = [
            k for k, f in self._flows.items()
            if f.src_ip == src_ip and not f.is_established and f.syn_count > 0
        ]
        return len(suspected) >= self.syn_scan_threshold

    def get_flow(self, flow_key: str) -> NetworkFlow | None:
        return self._flows.get(flow_key)

    def active_flow_count(self) -> int:
        return len(self._flows)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _flow_key(packet: Packet) -> str:
        # Bidirectional key — same key regardless of direction
        endpoints = sorted([
            f"{packet.src_ip}:{packet.src_port}",
            f"{packet.dst_ip}:{packet.dst_port}",
        ])
        return f"{packet.protocol.value}:{endpoints[0]}-{endpoints[1]}"

    def _create_flow(self, packet: Packet, flow_key: str) -> NetworkFlow:
        if len(self._flows) >= self.max_flows:
            self._evict_oldest_flow()
        flow = NetworkFlow(
            src_ip=packet.src_ip,
            dst_ip=packet.dst_ip,
            src_port=packet.src_port or 0,
            dst_port=packet.dst_port or 0,
            protocol=packet.protocol,
        )
        self._flows[flow_key] = flow
        return flow

    def _expire_syn_timestamps(self, src_ip: str, at_time: float) -> None:
        cutoff = at_time - self.syn_scan_window
        self._syn_timestamps[src_ip] = [
            t for t in self._syn_timestamps[src_ip] if t >= cutoff
        ]

    def _maybe_evict_stale_flows(self, at_time: float) -> None:
        if len(self._flows) < self.max_flows * 0.9:
            return
        cutoff = at_time - self.flow_timeout
        stale = [k for k, f in self._flows.items() if f.last_seen < cutoff]
        for k in stale:
            del self._flows[k]

    def _evict_oldest_flow(self) -> None:
        if not self._flows:
            return
        oldest_key = min(self._flows, key=lambda k: self._flows[k].last_seen)
        del self._flows[oldest_key]


# ---------------------------------------------------------------------------
# PacketStreamer
# ---------------------------------------------------------------------------

class PacketStreamer:
    """
    Live and PCAP-file packet ingestion with BPF filter support.

    Usage — live capture::

        streamer = PacketStreamer(interface="eth0", bpf_filter="tcp or udp")
        for packet in streamer.stream():
            print(packet.src_ip, packet.protocol)

    Usage — PCAP file::

        streamer = PacketStreamer(pcap_file="/captures/traffic.pcap")
        for packet in streamer.stream():
            process(packet)

    Usage — with stream reassembly disabled (raw per-packet)::

        streamer = PacketStreamer(interface="eth0", reconstruct_streams=False)
    """

    def __init__(
        self,
        interface: str | None = None,
        pcap_file: str | Path | None = None,
        bpf_filter: str = "",
        reconstruct_streams: bool = True,
        flow_timeout: float = 120.0,
        max_flows: int = 100_000,
        syn_scan_threshold: int = 5,
        syn_scan_window: float = 60.0,
        packet_count: int = 0,         # 0 = unlimited
        decode_application: bool = True,
    ) -> None:
        if interface is None and pcap_file is None:
            raise ValueError(
                "Provide either interface= for live capture "
                "or pcap_file= for PCAP reading."
            )
        if interface and pcap_file:
            raise ValueError("Provide interface= OR pcap_file=, not both.")

        self.interface = interface
        self.pcap_file = Path(pcap_file) if pcap_file else None
        self.bpf_filter = bpf_filter
        self.reconstruct_streams = reconstruct_streams
        self.packet_count = packet_count
        self.decode_application = decode_application

        self._reassembler = StreamReassembler(
            flow_timeout=flow_timeout,
            max_flows=max_flows,
            syn_scan_threshold=syn_scan_threshold,
            syn_scan_window=syn_scan_window,
        ) if reconstruct_streams else None

        self._decoder = ProtocolDecoder() if decode_application else None
        self._running = False

        logger.debug(
            "PacketStreamer initialised — source=%s bpf=%r streams=%s",
            interface or pcap_file,
            bpf_filter,
            reconstruct_streams,
        )

    # ------------------------------------------------------------------
    # Public streaming API
    # ------------------------------------------------------------------

    def stream(self) -> Generator[Packet, None, None]:
        """
        Yields fully decoded, stream-reassembled Packet objects.
        Blocks indefinitely on live interfaces until stop() is called.
        Exits automatically when PCAP file is exhausted.
        """
        self._running = True
        try:
            if self.interface:
                yield from self._stream_live()
            else:
                yield from self._stream_pcap()
        finally:
            self._running = False

    def stop(self) -> None:
        """Signal the streaming loop to stop after the current packet."""
        self._running = False

    @property
    def reassembler(self) -> StreamReassembler | None:
        return self._reassembler

    def is_slow_syn_scan(self, src_ip: str) -> bool:
        """Proxy to reassembler's slow-scan detector."""
        if self._reassembler is None:
            raise RuntimeError("Stream reassembly is disabled — enable reconstruct_streams=True.")
        return self._reassembler.is_slow_syn_scan(src_ip)

    def active_flows(self) -> int:
        if self._reassembler is None:
            return 0
        return self._reassembler.active_flow_count()

    # ------------------------------------------------------------------
    # Internal capture backends
    # ------------------------------------------------------------------

    def _stream_live(self) -> Iterator[Packet]:
        try:
            from scapy.all import sniff  # type: ignore
        except ImportError as exc:
            raise InterfaceError(
                "scapy is required for live packet capture. "
                "Install it with: pip install scapy"
            ) from exc

        logger.info("Starting live capture on %s (filter=%r)", self.interface, self.bpf_filter)

        import queue as _queue
        import threading as _threading

        _sentinel: object = object()
        pkt_queue: _queue.Queue = _queue.Queue(maxsize=2000)

        def _callback(scapy_pkt) -> None:
            if not self._running:
                return
            pkt = _scapy_to_packet(scapy_pkt)
            if pkt is not None:
                try:
                    pkt_queue.put_nowait(pkt)
                except _queue.Full:
                    logger.warning("Capture queue full — dropping packet")

        def _sniff_thread() -> None:
            try:
                sniff(
                    iface=self.interface,
                    filter=self.bpf_filter or None,
                    prn=_callback,
                    stop_filter=lambda _: not self._running,
                    count=self.packet_count or 0,
                    store=False,
                )
            except PermissionError as exc:
                raise InterfaceError(
                    f"Permission denied opening interface {self.interface!r}. "
                    "Try running with sudo or granting CAP_NET_RAW."
                ) from exc
            except OSError as exc:
                raise InterfaceError(
                    f"Cannot open interface {self.interface!r}: {exc}"
                ) from exc
            finally:
                pkt_queue.put(_sentinel)

        t = _threading.Thread(target=_sniff_thread, daemon=True, name="threatwire-sniff")
        t.start()

        while True:
            item = pkt_queue.get()
            if item is _sentinel:
                break
            yield self._enrich(item)  # type: ignore[arg-type]

    def _stream_pcap(self) -> Iterator[Packet]:
        if not self.pcap_file or not self.pcap_file.exists():
            raise PcapReadError(f"PCAP file not found: {self.pcap_file}")

        try:
            from scapy.all import PcapReader  # type: ignore
        except ImportError as exc:
            raise PcapReadError(
                "scapy is required for PCAP reading. "
                "Install it with: pip install scapy"
            ) from exc

        logger.info("Reading PCAP: %s", self.pcap_file)
        yielded = 0
        try:
            with PcapReader(str(self.pcap_file)) as reader:
                for scapy_pkt in reader:
                    if not self._running:
                        break
                    pkt = _scapy_to_packet(scapy_pkt)
                    if pkt is None:
                        continue
                    yield self._enrich(pkt)
                    yielded += 1
                    if self.packet_count and yielded >= self.packet_count:
                        break
        except Exception as exc:
            raise PcapReadError(f"Error reading PCAP {self.pcap_file}: {exc}") from exc

        logger.info("PCAP exhausted — %d packets yielded", yielded)

    # ------------------------------------------------------------------
    # Enrichment pipeline
    # ------------------------------------------------------------------

    def _enrich(self, packet: Packet) -> Packet:
        """Apply stream reassembly then application-layer decoding."""
        if self._reassembler:
            packet, _ = self._reassembler.process(packet)
        if self._decoder:
            packet = self._decoder.decode(packet)
        return packet


# ---------------------------------------------------------------------------
# Scapy → Packet conversion helper (kept outside class for testability)
# ---------------------------------------------------------------------------

def _scapy_to_packet(scapy_pkt) -> Packet | None:
    """Convert a scapy packet to a threatwire Packet. Returns None if unsupported."""
    try:
        from scapy.layers.inet import ICMP, IP, TCP, UDP  # type: ignore
    except ImportError:
        return None

    if not scapy_pkt.haslayer(IP):
        return None

    ip = scapy_pkt[IP]

    # Determine protocol
    if scapy_pkt.haslayer(TCP):
        transport = scapy_pkt[TCP]
        proto = Protocol.TCP
        flags = _parse_tcp_flags(transport.flags)
        payload = bytes(transport.payload)
        return Packet(
            timestamp=float(getattr(scapy_pkt, "time", time.time())),
            src_ip=ip.src,
            dst_ip=ip.dst,
            protocol=proto,
            src_port=transport.sport,
            dst_port=transport.dport,
            flags=flags,
            ttl=ip.ttl,
            payload=payload,
            payload_len=len(payload),
        )

    elif scapy_pkt.haslayer(UDP):
        transport = scapy_pkt[UDP]
        payload = bytes(transport.payload)
        return Packet(
            timestamp=float(getattr(scapy_pkt, "time", time.time())),
            src_ip=ip.src,
            dst_ip=ip.dst,
            protocol=Protocol.UDP,
            src_port=transport.sport,
            dst_port=transport.dport,
            ttl=ip.ttl,
            payload=payload,
            payload_len=len(payload),
        )

    elif scapy_pkt.haslayer(ICMP):
        return Packet(
            timestamp=float(getattr(scapy_pkt, "time", time.time())),
            src_ip=ip.src,
            dst_ip=ip.dst,
            protocol=Protocol.ICMP,
            ttl=ip.ttl,
        )

    return None


def _parse_tcp_flags(flag_int: int) -> list[TCPFlag]:
    """Convert scapy TCP flags integer to a list of TCPFlag enums."""
    result = []
    mapping = {0x02: TCPFlag.SYN, 0x10: TCPFlag.ACK, 0x01: TCPFlag.FIN,
               0x04: TCPFlag.RST, 0x08: TCPFlag.PSH, 0x20: TCPFlag.URG}
    for bit, flag in mapping.items():
        if flag_int & bit:
            result.append(flag)
    return result
