"""
threatwire.rules.suricata
==========================
SuricataParser — converts Suricata rule syntax into threatwire Rule objects.

Supports:
  - content matching (payload_patterns)
  - pcre matching (regex_patterns)
  - port and protocol filters
  - msg, sid, severity (priority) fields
  - MITRE ATT&CK metadata tags

Limitations (by design — this is a bridge, not a full Suricata engine):
  - Does not support flow:, flowbits:, or stateful keywords
  - Byte_test and byte_extract are ignored
  - threshold: keyword is not applied
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

from threatwire.core.models import AlertSeverity

logger = logging.getLogger(__name__)

_PRIORITY_TO_SEVERITY = {
    1: AlertSeverity.CRITICAL,
    2: AlertSeverity.HIGH,
    3: AlertSeverity.MEDIUM,
    4: AlertSeverity.LOW,
}

_PROTO_MAP = {
    "tcp": ["tcp"],
    "udp": ["udp"],
    "http": ["tcp", "http"],
    "dns": ["udp", "dns"],
    "tls": ["tcp", "tls"],
    "smb": ["tcp", "smb"],
    "ip": ["tcp", "udp"],
}

# Regex to extract Suricata option fields
_OPTION_RE = re.compile(r'(\w+)\s*(?::\s*"([^"]*)"|\s*;|:\s*([^;]+);)')


class SuricataParser:

    @classmethod
    def parse_file(cls, path: Path) -> list:
        """Parse a .rules file and return a list of threatwire Rule objects."""
        from threatwire.core.signature_engine import Rule

        rule_cls = Rule  # noqa: N806
        rules = []
        text = path.read_text(encoding="utf-8", errors="replace")

        for lineno, line in enumerate(text.splitlines(), 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                rule = cls._parse_line(line, Rule)
                if rule:
                    rules.append(rule)
            except Exception as exc:
                logger.debug("Line %d skipped (%s): %s", lineno, exc, line[:80])

        logger.info("Parsed %d rules from %s", len(rules), path.name)
        return rules

    @classmethod
    def _parse_line(cls, line: str, Rule) -> object | None:  # noqa: N803
        # Suricata rule format:
        # action proto src_ip src_port dir dst_ip dst_port (options)
        header_match = re.match(
            r'(alert|drop|pass|reject)\s+(\w+)\s+\S+\s+(\S+)\s+[<>-]+\s+\S+\s+(\S+)\s+\((.+)\)',
            line, re.DOTALL
        )
        if not header_match:
            return None

        header_match.group(1)
        proto = header_match.group(2).lower()
        src_port_str = header_match.group(3)
        dst_port_str = header_match.group(4)
        options_str = header_match.group(5)

        options = cls._parse_options(options_str)

        msg = options.get("msg", "Unnamed Suricata rule")
        sid = options.get("sid", "0")
        priority = int(options.get("priority", "3"))
        rev = options.get("rev", "1")

        severity = _PRIORITY_TO_SEVERITY.get(priority, AlertSeverity.MEDIUM)
        protocols = _PROTO_MAP.get(proto, [proto])

        # Extract content patterns
        payload_patterns: list[bytes] = []
        for content in options.get("content_list", []):
            content = content.strip('"')
            # Handle hex escapes: |XX XX|
            content = re.sub(
                r'\|([0-9A-Fa-f ]+)\|',
                lambda m: bytes.fromhex(m.group(1).replace(" ", "")).decode("latin1"),
                content
            )
            payload_patterns.append(content.encode("latin1", errors="replace"))

        # Extract PCRE patterns
        regex_patterns: list[str] = []
        for pcre in options.get("pcre_list", []):
            # Strip leading/trailing /flags
            m = re.match(r'"?/(.+)/(\w*)"?', pcre)
            if m:
                regex_patterns.append(m.group(1))

        # Parse ports
        dst_ports = cls._parse_ports(dst_port_str)
        src_ports = cls._parse_ports(src_port_str)

        # MITRE tags from metadata
        technique_id = ""
        tactic_id = ""
        metadata = options.get("metadata", "")
        if metadata:
            m = re.search(r'attack\.t(\d+(?:\.\d+)?)', metadata, re.IGNORECASE)
            if m:
                technique_id = f"T{m.group(1)}"

        return Rule(
            rule_id=f"TW-SURICATA-{sid}",
            name=msg,
            severity=severity,
            description=f"Imported from Suricata rule sid:{sid} rev:{rev}",
            technique_id=technique_id,
            tactic_id=tactic_id,
            payload_patterns=payload_patterns,
            regex_patterns=regex_patterns,
            dst_ports=dst_ports,
            src_ports=src_ports,
            protocols=protocols,
            base_confidence=0.75,
        )

    @staticmethod
    def _parse_options(options_str: str) -> dict:
        result: dict = {
            "content_list": [],
            "pcre_list": [],
        }
        # Split on semicolons not inside quotes
        parts = re.split(r';\s*(?=(?:[^"]*"[^"]*")*[^"]*$)', options_str)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if ":" in part:
                key, _, val = part.partition(":")
                key = key.strip().lower()
                val = val.strip().strip('"')
                if key == "content":
                    result["content_list"].append(val)
                elif key == "pcre":
                    result["pcre_list"].append(val)
                else:
                    result[key] = val
            else:
                result[part.lower()] = True
        return result

    @staticmethod
    def _parse_ports(port_str: str) -> list[int]:
        ports: list[int] = []
        if port_str in ("any", "!any", ""):
            return ports
        port_str = port_str.strip("[]!")
        for part in port_str.split(","):
            part = part.strip()
            if ":" in part:
                lo, hi = part.split(":", 1)
                try:
                    ports.extend(range(int(lo), int(hi) + 1))
                except ValueError:
                    pass
            else:
                try:
                    ports.append(int(part))
                except ValueError:
                    pass
        return ports[:64]   # cap to avoid huge port lists
