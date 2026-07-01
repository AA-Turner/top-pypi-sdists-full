"""
threatwire — Real-time network packet inspection and threat signature matching
for Python-based IDS/IPS pipelines.

    from threatwire import PacketStreamer, SignatureEngine, ThreatEventBus

MITRE ATT&CK: TA0011 · C2, TA0043 · Recon

This package ships a ``py.typed`` marker (PEP 561) so Pyright / mypy resolve
all re-exported symbols from this ``__init__`` without needing a ``.venv``.
"""

from threatwire.core.event_bus import ThreatEventBus as ThreatEventBus
from threatwire.core.models import AlertSeverity as AlertSeverity
from threatwire.core.models import Packet as Packet
from threatwire.core.models import ThreatAlert as ThreatAlert
from threatwire.core.pipeline import ThreatPipeline as ThreatPipeline
from threatwire.core.signature_engine import SignatureEngine as SignatureEngine
from threatwire.core.streamer import PacketStreamer as PacketStreamer

__version__ = "0.1.0"
__author__ = "threatwire contributors"
__license__ = "MIT"

__all__ = [
    "PacketStreamer",
    "SignatureEngine",
    "ThreatEventBus",
    "ThreatPipeline",
    "Packet",
    "ThreatAlert",
    "AlertSeverity",
]