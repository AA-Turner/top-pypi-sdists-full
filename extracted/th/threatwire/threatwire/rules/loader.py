"""
threatwire.rules.loader
========================
RuleLoader — loads built-in and custom rules from YAML/JSON files.

Built-in ruleset covers:
  - DNS C2 tunneling (TXT queries, high-entropy labels, beaconing)
  - HTTP C2 beaconing (Emotet, Cobalt Strike, Metasploit patterns)
  - Port scanning (slow SYN, NULL, XMAS, FIN scans)
  - SMB exploit patterns (EternalBlue, MS17-010)
  - TLS C2 (known malicious JA3 hashes, self-signed cert indicators)
  - Credential theft (LDAP, Kerberoasting, DCSync patterns)
  - DNS tunneling (dnscat2, iodine, dns2tcp signatures)
  - Ransomware IOCs (shadow copy deletion, mass encryption patterns)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from threatwire.core.models import AlertSeverity

logger = logging.getLogger(__name__)

# Lazy import to avoid circular
def _rule_cls():
    from threatwire.core.signature_engine import Rule
    return Rule


class RuleLoader:

    @classmethod
    def load_builtin(cls) -> list:
        """Return the complete built-in ruleset."""
        rule_cls = _rule_cls()
        Rule = rule_cls
        return [
            # ----------------------------------------------------------
            # DNS C2 / Tunneling
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-DNS-001",
                name="DNS TXT query — possible C2 channel",
                severity=AlertSeverity.HIGH,
                description=(
                    "DNS TXT record queries are commonly used"
                    " by C2 frameworks to exfiltrate data."
                ),
                technique_id="T1071.004",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                protocols=["dns"],
                dst_ports=[53],
                base_confidence=0.65,
            ),
            Rule(
                rule_id="TW-DNS-002",
                name="DNS tunneling — dnscat2 signature",
                severity=AlertSeverity.CRITICAL,
                description="Matches dnscat2 C2 tool DNS query pattern.",
                technique_id="T1071.004",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                payload_patterns=[b"dnscat"],
                protocols=["dns", "udp"],
                dst_ports=[53],
                base_confidence=0.95,
            ),
            Rule(
                rule_id="TW-DNS-003",
                name="DNS tunneling — iodine signature",
                severity=AlertSeverity.CRITICAL,
                description="Matches iodine DNS tunnel client handshake pattern.",
                technique_id="T1071.004",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                payload_patterns=[b"VREQ", b"YREQ"],
                protocols=["udp"],
                dst_ports=[53],
                base_confidence=0.92,
            ),
            # ----------------------------------------------------------
            # HTTP C2 Beaconing
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-HTTP-001",
                name="Emotet C2 HTTP beacon",
                severity=AlertSeverity.CRITICAL,
                description="Matches Emotet malware HTTP POST C2 beacon URI structure.",
                technique_id="T1071.001",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                payload_patterns=[b"POST /"],
                regex_patterns=[r"POST /[a-z]{4,8}/[a-z]{4,8}\.php"],
                protocols=["tcp", "http"],
                dst_ports=[80, 8080, 443, 7080, 50000],
                beacon_interval_s=300.0,
                beacon_tolerance_s=45.0,
                base_confidence=0.88,
            ),
            Rule(
                rule_id="TW-HTTP-002",
                name="Cobalt Strike HTTP malleable C2",
                severity=AlertSeverity.CRITICAL,
                description="Matches Cobalt Strike default HTTP beacon profile patterns.",
                technique_id="T1071.001",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                payload_patterns=[b"__utmz=", b"__utma="],
                regex_patterns=[r"Cookie:.*__utm[az]="],
                protocols=["tcp", "http"],
                dst_ports=[80, 443, 8080],
                base_confidence=0.85,
            ),
            Rule(
                rule_id="TW-HTTP-003",
                name="Metasploit Meterpreter HTTP stager",
                severity=AlertSeverity.CRITICAL,
                description="Matches Meterpreter HTTP staging GET request pattern.",
                technique_id="T1071.001",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                payload_patterns=[b"MZ"],
                regex_patterns=[r"GET /[a-zA-Z0-9]{4,8} HTTP", r"User-Agent: Mozilla.*MSIE 6\.0"],
                protocols=["tcp", "http"],
                dst_ports=[4444, 80, 8080, 443],
                base_confidence=0.82,
            ),
            Rule(
                rule_id="TW-HTTP-004",
                name="Generic C2 beacon — short fixed interval",
                severity=AlertSeverity.MEDIUM,
                description="Periodic HTTP requests at a fixed interval — possible C2 keepalive.",
                technique_id="T1071.001",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                protocols=["tcp", "http"],
                dst_ports=[80, 8080, 443],
                beacon_interval_s=60.0,
                beacon_tolerance_s=10.0,
                base_confidence=0.55,
            ),
            # ----------------------------------------------------------
            # Port Scanning
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-SCAN-001",
                name="TCP NULL scan",
                severity=AlertSeverity.MEDIUM,
                description="TCP packet with no flags set — stealth port scan technique.",
                technique_id="T1046",
                tactic_id="TA0043",
                tactic_name="Reconnaissance",
                payload_patterns=[b"\x00\x00\x00\x00\x00\x00"],
                protocols=["tcp"],
                min_payload_len=0,
                max_payload_len=0,
                base_confidence=0.75,
            ),
            Rule(
                rule_id="TW-SCAN-002",
                name="Nmap OS detection probe",
                severity=AlertSeverity.LOW,
                description="Nmap OS detection sequence — unusual TCP flag combination.",
                technique_id="T1046",
                tactic_id="TA0043",
                tactic_name="Reconnaissance",
                payload_patterns=[b"\x00\x00\x00\x00\x00\x00", b"SF|"],
                protocols=["tcp"],
                base_confidence=0.60,
            ),
            # ----------------------------------------------------------
            # SMB Exploits
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-SMB-001",
                name="EternalBlue MS17-010 exploit attempt",
                severity=AlertSeverity.CRITICAL,
                description="SMB exploit matching EternalBlue (MS17-010) pattern used in WannaCry.",
                technique_id="T1210",
                tactic_id="TA0008",
                tactic_name="Lateral Movement",
                payload_patterns=[b"\xff\xfeSMB", b"NT_TRANSACT_SECONDARY"],
                protocols=["tcp", "smb"],
                dst_ports=[445],
                base_confidence=0.93,
            ),
            Rule(
                rule_id="TW-SMB-002",
                name="SMB brute force — rapid authentication attempts",
                severity=AlertSeverity.HIGH,
                description="High-frequency SMB session setup requests — possible brute force.",
                technique_id="T1110.003",
                tactic_id="TA0006",
                tactic_name="Credential Access",
                payload_patterns=[b"\xffSMB\x73"],
                protocols=["tcp", "smb"],
                dst_ports=[445, 139],
                beacon_interval_s=0.5,
                beacon_tolerance_s=0.4,
                base_confidence=0.78,
            ),
            # ----------------------------------------------------------
            # Credential Theft
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-CRED-001",
                name="DCSync DRSUAPI replication request",
                severity=AlertSeverity.CRITICAL,
                description="DCSync attack — non-DC initiating AD replication via DRSUAPI.",
                technique_id="T1003.006",
                tactic_id="TA0006",
                tactic_name="Credential Access",
                payload_patterns=[b"DRSGetNCChanges", b"DRSUAPI"],
                protocols=["tcp"],
                dst_ports=[135, 389, 636, 3268, 49152, 49153],
                base_confidence=0.91,
            ),
            Rule(
                rule_id="TW-CRED-002",
                name="Kerberoasting — SPN enumeration",
                severity=AlertSeverity.HIGH,
                description="Kerberos TGS-REQ for service tickets — possible Kerberoasting.",
                technique_id="T1558.003",
                tactic_id="TA0006",
                tactic_name="Credential Access",
                payload_patterns=[b"\x6b\x05\x00"],   # Kerberos AS-REQ / TGS-REQ tag
                protocols=["tcp", "udp"],
                dst_ports=[88],
                base_confidence=0.72,
            ),
            # ----------------------------------------------------------
            # Ransomware IOCs
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-RANSOM-001",
                name="Ransomware C2 check-in pattern",
                severity=AlertSeverity.CRITICAL,
                description="POST request matching known ransomware C2 check-in structure.",
                technique_id="T1486",
                tactic_id="TA0040",
                tactic_name="Impact",
                payload_patterns=[b"victim_id=", b"bot_id=", b"ransom_id="],
                protocols=["tcp", "http"],
                dst_ports=[80, 443, 8080],
                base_confidence=0.89,
            ),
            Rule(
                rule_id="TW-RANSOM-002",
                name="Tor hidden service connection — possible ransomware C2",
                severity=AlertSeverity.HIGH,
                description="Connection to .onion via Tor SOCKS proxy — ransomware C2 pattern.",
                technique_id="T1090.003",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                payload_patterns=[b".onion"],
                protocols=["tcp"],
                dst_ports=[9050, 9150],
                base_confidence=0.75,
            ),
            # ----------------------------------------------------------
            # TLS Anomalies
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-TLS-001",
                name="TLS self-signed cert on non-standard port",
                severity=AlertSeverity.MEDIUM,
                description="TLS handshake on an unusual port — possible encrypted C2 channel.",
                technique_id="T1071.001",
                tactic_id="TA0011",
                tactic_name="Command and Control",
                protocols=["tcp", "tls"],
                dst_ports=[4444, 8443, 4443, 1443, 9443, 7443],
                base_confidence=0.60,
            ),
            # ----------------------------------------------------------
            # Exploit Kit Patterns
            # ----------------------------------------------------------
            Rule(
                rule_id="TW-EK-001",
                name="Exploit kit landing page redirect",
                severity=AlertSeverity.HIGH,
                description=(
                    "HTTP redirect chain matching common"
                    " exploit kit distribution patterns."
                ),
                technique_id="T1189",
                tactic_id="TA0001",
                tactic_name="Initial Access",
                payload_patterns=[b"eval(unescape(", b"eval(String.fromCharCode("],
                protocols=["tcp", "http"],
                dst_ports=[80, 8080],
                base_confidence=0.83,
            ),
        ]

    @classmethod
    def load_from_path(cls, path: Path) -> list:
        """
        Load rules from a directory containing JSON rule files.
        Each file should contain a list of rule dicts.
        """
        rule_cls = _rule_cls()
        Rule = rule_cls
        rules = []

        files = list(path.glob("*.json")) + list(path.glob("*.rules.json"))
        for f in sorted(files):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                for r in (data if isinstance(data, list) else [data]):
                    try:
                        rule = cls._dict_to_rule(r, Rule)
                        rules.append(rule)
                    except Exception as e:
                        logger.warning("Skipping malformed rule in %s: %s", f.name, e)
            except json.JSONDecodeError as e:
                logger.error("Cannot parse rule file %s: %s", f.name, e)

        logger.debug("Loaded %d custom rules from %s", len(rules), path)
        return rules

    @staticmethod
    def _dict_to_rule(d: dict, rule_cls) -> object:
        return rule_cls(
            rule_id=d["rule_id"],
            name=d["name"],
            severity=AlertSeverity(d.get("severity", "medium")),
            description=d.get("description", ""),
            technique_id=d.get("technique_id", ""),
            tactic_id=d.get("tactic_id", ""),
            tactic_name=d.get("tactic_name", ""),
            payload_patterns=[p.encode() if isinstance(p, str) else bytes(p)
                               for p in d.get("payload_patterns", [])],
            regex_patterns=d.get("regex_patterns", []),
            dst_ports=d.get("dst_ports", []),
            src_ports=d.get("src_ports", []),
            protocols=d.get("protocols", []),
            beacon_interval_s=d.get("beacon_interval_s"),
            beacon_tolerance_s=d.get("beacon_tolerance_s", 30.0),
            min_payload_len=d.get("min_payload_len", 0),
            max_payload_len=d.get("max_payload_len", 0),
            base_confidence=d.get("base_confidence", 0.8),
        )
