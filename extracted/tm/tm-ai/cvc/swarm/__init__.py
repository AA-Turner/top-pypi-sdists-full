"""
cvc.swarm — peer-to-peer cluster primitives for the soul.

AstroSwarm is CVC at scale: every owner is a node, every node is a soul,
and souls can opt into sharing insights with other souls on the same
local network (mDNS) or over an explicit peer list.

This module is deliberately protocol-agnostic. It exposes the primitives
a peer uses:
  - Identity       : who am I (peer_id, public key fingerprint)
  - Discovery      : who's nearby (mDNS / manual list)
  - Share policy   : what I'm willing to share (per-data-class)
  - Broadcast      : anonymous insight sharing across the swarm

The actual wire transport (libp2p / gun / direct TCP) is pluggable. The
first implementation uses a JSON-over-HTTP probe for local peers and an
append-only inbox file for broadcasts (no central server).
"""

from __future__ import annotations

import hashlib
import logging
import secrets
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.swarm")


@dataclass
class PeerIdentity:
    """Who I am as a swarm node."""

    peer_id: str = field(default_factory=lambda: "cvc_" + secrets.token_hex(8))
    display_name: str = "unnamed-owner"
    created_at: float = field(default_factory=time.time)
    public_key_fp: str = ""
    capabilities: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "PeerIdentity":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class SharePolicy:
    """
    Per-data-class sharing rules. The owner decides what flows out.

    Classes:
      - identity      : peer_id + display name
      - entities      : people/places/projects the soul has learned about
      - values        : owner's stated beliefs
      - dreams        : dream diary entries (high-sensitivity)
      - insights      : anonymous meta-insights ("51% of souls learned X this week")
    """

    identity: str = "public"          # public | friends | private
    entities: str = "friends"
    values: str = "private"
    dreams: str = "private"
    insights: str = "public"

    def allows(self, data_class: str, audience: str = "public") -> bool:
        """
        True if data of `data_class` (with its set visibility level) is
        allowed to be seen by `audience`.

        Visibility rank: public (0, most visible) < friends (1) < private (2, least visible).
        An audience of `private` can only see data marked private or more open.
        An audience of `public` can see everything (because public is the lowest bar).
        """
        level = getattr(self, data_class, "private")
        rank = {"public": 0, "friends": 1, "private": 2}
        data_rank = rank.get(level, 2)
        aud_rank = rank.get(audience, 2)
        # data with lower rank is MORE visible; audience with higher rank is MORE trusted.
        # Allow iff data_rank <= aud_rank (data is at least as open as audience needs).
        return data_rank <= aud_rank

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Peer:
    """A discovered peer on the local network."""

    peer_id: str
    display_name: str
    address: str            # host:port
    last_seen: float = 0.0
    capabilities: list[str] = field(default_factory=list)
    trust: float = 0.0      # 0.0–1.0, owner-controlled

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Broadcast:
    """An anonymous insight shared with the swarm."""

    broadcast_id: str = field(default_factory=lambda: uuid.uuid4().hex)
    topic: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    peer_id: str = ""        # who sent it (anonymous to receivers unless revealed)
    signature: str = ""      # optional ed25519 signature over the payload

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SwarmNode:
    """
    A single owner's presence in the swarm.

    Persists peer identity, share policy, known peers, and the local
    inbox of incoming broadcasts to ``<vault>/swarm/``.
    """

    def __init__(self, swarm_dir: Path) -> None:
        self.swarm_dir = Path(swarm_dir)
        self.swarm_dir.mkdir(parents=True, exist_ok=True)
        self.identity_path = self.swarm_dir / "identity.json"
        self.peers_path = self.swarm_dir / "peers.json"
        self.policy_path = self.swarm_dir / "share_policy.json"
        self.inbox_path = self.swarm_dir / "inbox.jsonl"

    # ── identity ──────────────────────────────────────────────────────

    def identity(self) -> PeerIdentity:
        if self.identity_path.exists():
            try:
                import json
                return PeerIdentity.from_dict(
                    json.loads(self.identity_path.read_text(encoding="utf-8"))
                )
            except Exception:
                pass
        ident = PeerIdentity()
        import json
        self.identity_path.write_text(json.dumps(ident.to_dict(), indent=2), encoding="utf-8")
        return ident

    def rename(self, new_name: str) -> PeerIdentity:
        if not new_name or len(new_name) > 64:
            raise ValueError("display_name must be 1–64 chars")
        ident = self.identity()
        ident.display_name = new_name
        import json
        self.identity_path.write_text(json.dumps(ident.to_dict(), indent=2), encoding="utf-8")
        return ident

    # ── share policy ──────────────────────────────────────────────────

    def policy(self) -> SharePolicy:
        if self.policy_path.exists():
            try:
                import json
                return SharePolicy(
                    **{k: v for k, v in json.loads(self.policy_path.read_text(encoding="utf-8")).items() if k in SharePolicy.__dataclass_fields__}
                )
            except Exception:
                pass
        return SharePolicy()

    def set_policy(self, policy: SharePolicy) -> None:
        import json
        self.policy_path.write_text(json.dumps(policy.to_dict(), indent=2), encoding="utf-8")

    # ── peers ─────────────────────────────────────────────────────────

    def known_peers(self) -> list[Peer]:
        if not self.peers_path.exists():
            return []
        import json
        try:
            data = json.loads(self.peers_path.read_text(encoding="utf-8"))
            return [Peer(**{k: v for k, v in p.items() if k in Peer.__dataclass_fields__}) for p in data]
        except Exception:
            return []

    def add_peer(self, peer: Peer) -> None:
        peers = self.known_peers()
        peers = [p for p in peers if p.peer_id != peer.peer_id]
        peers.append(peer)
        import json
        self.peers_path.write_text(
            json.dumps([p.to_dict() for p in peers], indent=2), encoding="utf-8"
        )

    def remove_peer(self, peer_id: str) -> None:
        peers = [p for p in self.known_peers() if p.peer_id != peer_id]
        import json
        self.peers_path.write_text(
            json.dumps([p.to_dict() for p in peers], indent=2), encoding="utf-8"
        )

    # ── broadcasts ────────────────────────────────────────────────────

    def broadcast(self, topic: str, payload: dict[str, Any]) -> Broadcast:
        bc = Broadcast(
            topic=topic,
            payload=payload,
            peer_id=self.identity().peer_id,
            signature=hashlib.sha256(
                (json_dumps(payload) + topic).encode("utf-8")
            ).hexdigest()[:32],
        )
        # The local owner is also the first audience for their own broadcast
        self._append_inbox(bc)
        return bc

    def inbox(self, limit: int = 50) -> list[Broadcast]:
        if not self.inbox_path.exists():
            return []
        with self.inbox_path.open("r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        out: list[Broadcast] = []
        import json
        for line in lines[-limit:]:
            try:
                d = json.loads(line)
                out.append(Broadcast(**{k: v for k, v in d.items() if k in Broadcast.__dataclass_fields__}))
            except Exception:
                continue
        return out

    def _append_inbox(self, bc: Broadcast) -> None:
        import json
        with self.inbox_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(bc.to_dict()) + "\n")


def json_dumps(obj: Any) -> str:
    import json
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))