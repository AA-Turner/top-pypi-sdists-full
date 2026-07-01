"""
threatwire.protocols.decoder
=============================
ProtocolDecoder — application-layer protocol decoding for DNS, HTTP, TLS, SMB.

Enriches Packet objects with structured decoded fields in packet.decoded.
Each decoder runs only when the packet matches the expected port/signature.
"""

from __future__ import annotations

import re
import struct

from threatwire.core.models import Packet, Protocol


class DNSDecoder:
    """
    Decodes DNS query/response packets.
    Key for C2 DNS tunneling detection — extracts query names, record types,
    response codes, and flags so SignatureEngine can match on them.
    """

    DNS_QUERY_TYPES = {1: "A", 2: "NS", 5: "CNAME", 15: "MX", 16: "TXT",
                       28: "AAAA", 33: "SRV", 255: "ANY"}

    def decode(self, payload: bytes) -> dict | None:
        if len(payload) < 12:
            return None
        try:
            txid = struct.unpack(">H", payload[:2])[0]
            flags = struct.unpack(">H", payload[2:4])[0]
            qdcount = struct.unpack(">H", payload[4:6])[0]
            ancount = struct.unpack(">H", payload[6:8])[0]

            is_response = bool(flags & 0x8000)
            rcode = flags & 0x000F

            # Parse question section
            questions = []
            offset = 12
            for _ in range(min(qdcount, 5)):
                name, offset = self._parse_name(payload, offset)
                if offset + 4 > len(payload):
                    break
                qtype = struct.unpack(">H", payload[offset:offset+2])[0]
                offset += 4
                questions.append({
                    "name": name,
                    "type": self.DNS_QUERY_TYPES.get(qtype, str(qtype)),
                })

            return {
                "protocol": "dns",
                "transaction_id": txid,
                "is_response": is_response,
                "return_code": rcode,
                "question_count": qdcount,
                "answer_count": ancount,
                "questions": questions,
                # Computed fields for C2 detection
                "has_txt_query": any(q["type"] == "TXT" for q in questions),
                "query_entropy": self._label_entropy(questions[0]["name"]) if questions else 0.0,
            }
        except Exception:
            return None

    @staticmethod
    def _parse_name(payload: bytes, offset: int) -> tuple[str, int]:
        labels = []
        visited = set()
        while offset < len(payload):
            length = payload[offset]
            if length == 0:
                offset += 1
                break
            if (length & 0xC0) == 0xC0:   # pointer
                if offset + 1 >= len(payload):
                    break
                ptr = ((length & 0x3F) << 8) | payload[offset + 1]
                if ptr in visited:
                    break
                visited.add(ptr)
                name, _ = DNSDecoder._parse_name(payload, ptr)
                labels.append(name)
                offset += 2
                break
            offset += 1
            labels.append(payload[offset:offset+length].decode("ascii", errors="replace"))
            offset += length
        return ".".join(labels), offset

    @staticmethod
    def _label_entropy(name: str) -> float:
        """Shannon entropy of the subdomain labels — high entropy = possible DGA/tunneling."""
        import math
        labels = name.split(".")[:-2]   # strip TLD and SLD
        if not labels:
            return 0.0
        s = "".join(labels)
        if not s:
            return 0.0
        freq = {c: s.count(c) / len(s) for c in set(s)}
        return -sum(p * math.log2(p) for p in freq.values())


class HTTPDecoder:
    """
    Decodes HTTP/1.x request and response headers.
    Extracts method, URI, host, user-agent, and content-type for
    C2 URI pattern matching and beacon detection.
    """

    _REQUEST_LINE_RE = re.compile(
        rb"^(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH|CONNECT) (\S+) HTTP/(\d\.\d)",
        re.IGNORECASE,
    )
    _RESPONSE_LINE_RE = re.compile(rb"^HTTP/(\d\.\d) (\d{3})")
    _HEADER_RE = re.compile(rb"^([A-Za-z0-9\-]+):\s*(.+)$", re.MULTILINE)

    def decode(self, payload: bytes) -> dict | None:
        if not payload:
            return None

        result: dict = {"protocol": "http"}

        req_m = self._REQUEST_LINE_RE.match(payload)
        if req_m:
            result.update({
                "direction": "request",
                "method": req_m.group(1).decode("ascii"),
                "uri": req_m.group(2).decode("utf-8", errors="replace"),
                "version": req_m.group(3).decode("ascii"),
            })
        else:
            resp_m = self._RESPONSE_LINE_RE.match(payload)
            if resp_m:
                result.update({
                    "direction": "response",
                    "status_code": int(resp_m.group(2)),
                })
            else:
                return None

        # Parse headers
        headers = {}
        for m in self._HEADER_RE.finditer(payload):
            key = m.group(1).decode("ascii", errors="replace").lower()
            val = m.group(2).decode("utf-8", errors="replace").strip()
            headers[key] = val

        result["headers"] = headers
        result["host"] = headers.get("host", "")
        result["user_agent"] = headers.get("user-agent", "")
        result["content_type"] = headers.get("content-type", "")
        result["content_length"] = int(headers.get("content-length", 0) or 0)

        return result


class TLSDecoder:
    """
    Decodes TLS ClientHello to extract SNI and cipher suites.
    JA3 fingerprint computation for TLS C2 detection.
    """

    TLS_CONTENT_TYPES = {20: "change_cipher_spec", 21: "alert",
                         22: "handshake", 23: "application_data"}

    def decode(self, payload: bytes) -> dict | None:
        if len(payload) < 5:
            return None
        content_type = payload[0]
        if content_type not in self.TLS_CONTENT_TYPES:
            return None

        version_major = payload[1]
        version_minor = payload[2]
        length = struct.unpack(">H", payload[3:5])[0]

        result = {
            "protocol": "tls",
            "content_type": self.TLS_CONTENT_TYPES.get(content_type, str(content_type)),
            "version": f"{version_major}.{version_minor}",
            "record_length": length,
        }

        # Try to parse ClientHello for SNI
        if content_type == 22 and len(payload) > 9:
            handshake_type = payload[5]
            if handshake_type == 1:   # ClientHello
                sni = self._extract_sni(payload[5:])
                ciphers = self._extract_cipher_suites(payload[5:])
                if sni:
                    result["sni"] = sni
                if ciphers:
                    result["cipher_suites"] = ciphers
                    result["ja3"] = self._compute_ja3_partial(version_minor, ciphers)

        return result

    @staticmethod
    def _extract_sni(hello: bytes) -> str | None:
        try:
            offset = 38
            if offset + 1 >= len(hello):
                return None
            session_len = hello[offset]
            offset += 1 + session_len
            cipher_len = struct.unpack(">H", hello[offset:offset+2])[0]
            offset += 2 + cipher_len
            comp_len = hello[offset]
            offset += 1 + comp_len
            ext_total = struct.unpack(">H", hello[offset:offset+2])[0]
            offset += 2
            end = offset + ext_total
            while offset + 4 < end:
                ext_type = struct.unpack(">H", hello[offset:offset+2])[0]
                ext_len = struct.unpack(">H", hello[offset+2:offset+4])[0]
                if ext_type == 0:   # SNI
                    sni_data = hello[offset+4:offset+4+ext_len]
                    sni = sni_data[5:].decode("ascii", errors="replace")
                    return sni
                offset += 4 + ext_len
        except Exception:
            pass
        return None

    @staticmethod
    def _extract_cipher_suites(hello: bytes) -> list[int]:
        try:
            offset = 38
            session_len = hello[offset]
            offset += 1 + session_len
            cipher_len = struct.unpack(">H", hello[offset:offset+2])[0]
            offset += 2
            ciphers = []
            for i in range(0, cipher_len, 2):
                c = struct.unpack(">H", hello[offset+i:offset+i+2])[0]
                ciphers.append(c)
            return ciphers
        except Exception:
            return []

    @staticmethod
    def _compute_ja3_partial(minor_version: int, ciphers: list[int]) -> str:
        """Simplified JA3-like fingerprint (version + ciphers only)."""
        import hashlib
        parts = f"3{minor_version}," + "-".join(str(c) for c in ciphers)
        return hashlib.md5(parts.encode()).hexdigest()


class SMBDecoder:
    """Minimal SMB1/SMB2 header decoder for lateral movement detection."""

    SMB1_COMMANDS = {0x72: "negotiate", 0x73: "session_setup", 0x75: "tree_connect",
                     0xa5: "trans2", 0x25: "trans"}
    SMB2_COMMANDS = {0: "negotiate", 1: "session_setup", 3: "tree_connect",
                     5: "create", 8: "read", 9: "write"}

    def decode(self, payload: bytes) -> dict | None:
        if len(payload) < 4:
            return None
        if payload[:4] == b"\xffSMB":
            return self._decode_smb1(payload)
        if payload[:4] == b"\xfeSMB":
            return self._decode_smb2(payload)
        return None

    def _decode_smb1(self, payload: bytes) -> dict:
        cmd = payload[4] if len(payload) > 4 else 0
        return {
            "protocol": "smb",
            "version": 1,
            "command": self.SMB1_COMMANDS.get(cmd, f"0x{cmd:02x}"),
        }

    def _decode_smb2(self, payload: bytes) -> dict:
        if len(payload) < 16:
            return {"protocol": "smb", "version": 2}
        cmd = struct.unpack("<H", payload[12:14])[0]
        return {
            "protocol": "smb",
            "version": 2,
            "command": self.SMB2_COMMANDS.get(cmd, f"cmd_{cmd}"),
            "message_id": struct.unpack("<Q", payload[28:36])[0] if len(payload) >= 36 else 0,
        }


class ProtocolDecoder:
    """
    Dispatcher that selects the right decoder based on port and payload heuristics.
    Sets packet.decoded and updates packet.protocol when a higher-layer protocol
    is identified.
    """

    def __init__(self) -> None:
        self._dns = DNSDecoder()
        self._http = HTTPDecoder()
        self._tls = TLSDecoder()
        self._smb = SMBDecoder()

    def decode(self, packet: Packet) -> Packet:
        decoded = None

        dst = packet.dst_port or 0
        src = packet.src_port or 0

        if dst == 53 or src == 53:
            decoded = self._dns.decode(packet.payload)
            if decoded:
                packet.protocol = Protocol.DNS

        elif dst in (80, 8080, 8000) or src in (80, 8080, 8000):
            decoded = self._http.decode(packet.payload)
            if decoded:
                packet.protocol = Protocol.HTTP

        elif dst == 443 or src == 443:
            decoded = self._tls.decode(packet.payload)
            if decoded:
                packet.protocol = Protocol.TLS

        elif dst in (445, 139) or src in (445, 139):
            decoded = self._smb.decode(packet.payload)
            if decoded:
                packet.protocol = Protocol.SMB

        else:
            # Heuristic fallback: try each decoder
            for decoder, proto in [
                (self._http, Protocol.HTTP),
                (self._dns, Protocol.DNS),
                (self._tls, Protocol.TLS),
                (self._smb, Protocol.SMB),
            ]:
                decoded = decoder.decode(packet.payload)
                if decoded:
                    packet.protocol = proto
                    break

        if decoded:
            packet.decoded = decoded

        return packet
