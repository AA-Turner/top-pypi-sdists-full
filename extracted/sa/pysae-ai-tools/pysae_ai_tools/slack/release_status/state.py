"""State model of a release-status message and its track transitions.

The model round-trips through the Slack message metadata: each ``release-status``
call reads the state from the message it finds, applies one transition, and
writes it back. The rendering (``render.py``) and transport (``cli.py``) layers
are built on top of this — the model itself has no Slack dependency.

Independent status tracks, each shown only once a status was sent for it
(so a web app shows just ``web``; a mobile app adds ``apple`` / ``android``):

    web      : building → awaiting-deploy → deploying → deployed
    service  : building → awaiting-deploy → deploying → deployed
    apple    : building → awaiting-publish → awaiting-store-review → deployed
    android  : building → awaiting-publish → awaiting-store-review → deployed

``web`` and ``service`` share the same deploy states; they differ only in how
they render (``service`` is the non-web backend track — schedulers, workers,
converters, APIs… — that ship through a plain build → deploy pipeline).

A ``failed`` state is accepted on any track. A message may also carry just the
release content (the primary-language release notes) with no track at all.
"""

from dataclasses import dataclass, field
from typing import Self

from ...common.project_config import Track

# Per-track ordered (state key -> French label). The last entry is the terminal
# "done" state (rendered with a check); every earlier one is "in progress".
TRACKS: dict[str, list[tuple[str, str]]] = {
    "web": [
        ("pending", "En attente"),
        ("building", "En cours de build"),
        ("awaiting-deploy", "En attente de déploiement"),
        ("deploying", "Déploiement en cours"),
        ("deployed", "Déployé"),
    ],
    # Non-web backend track (schedulers, workers, converters, APIs…) — same
    # build → deploy states as web, rendered with its own label/emoji.
    "service": [
        ("pending", "En attente"),
        ("building", "En cours de build"),
        ("awaiting-deploy", "En attente de déploiement"),
        ("deploying", "Déploiement en cours"),
        ("deployed", "Déployé"),
    ],
    "apple": [
        ("pending", "En attente"),
        ("building", "En cours de build"),
        ("awaiting-publish", "En attente de publication"),
        ("awaiting-store-review", "En attente de validation store"),
        ("deployed", "Déployé"),
    ],
    "android": [
        ("pending", "En attente"),
        ("building", "En cours de build"),
        ("awaiting-publish", "En attente de publication"),
        ("awaiting-store-review", "En attente de validation store"),
        ("deployed", "Déployé"),
    ],
    # Android private-store (enterprise) distribution — same states as android,
    # shown as its own line (e.g. driver ships standard + enterprise APKs).
    "android-enterprise": [
        ("pending", "En attente"),
        ("building", "En cours de build"),
        ("awaiting-publish", "En attente de publication"),
        ("awaiting-store-review", "En attente de validation store"),
        ("deployed", "Déployé"),
    ],
}

# Display order + per-track emoji/label come straight from the Track enum (single source).
TRACK_ORDER = [t.value for t in Track]

FAILED = "failed"
"""Generic terminal-error state accepted on any track."""

METADATA_EVENT_TYPE = "release_status"


def valid_state(track: str, state_key: str) -> bool:
    """True when ``state_key`` is a known state of ``track`` (or the generic FAILED)."""
    if state_key == FAILED:
        return True
    return any(key == state_key for key, _ in TRACKS.get(track, []))


@dataclass
class ReleaseState:
    """The full state of a release-status message — round-trips through metadata."""

    app: str
    version: str
    tracks: dict[str, str] = field(default_factory=dict)
    content: str = ""  # primary-language release notes mrkdwn (main message body)
    replies: dict[str, str] = field(default_factory=dict)  # reply kind (en|it|changelog) -> reply ts
    files: dict[str, str] = field(default_factory=dict)  # file kind (apk-prod|…) -> uploaded Slack file id

    def to_metadata(self) -> dict[str, object]:
        return {
            "event_type": METADATA_EVENT_TYPE,
            "event_payload": {
                "app": self.app,
                "version": self.version,
                "tracks": self.tracks,
                "content": self.content,
                "replies": self.replies,
                "files": self.files,
            },
        }

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> Self:
        raw_tracks = payload.get("tracks")
        tracks = {str(k): str(v) for k, v in raw_tracks.items()} if isinstance(raw_tracks, dict) else {}
        raw_replies = payload.get("replies")
        replies = {str(k): str(v) for k, v in raw_replies.items()} if isinstance(raw_replies, dict) else {}
        raw_files = payload.get("files")
        files = {str(k): str(v) for k, v in raw_files.items()} if isinstance(raw_files, dict) else {}
        return cls(
            app=str(payload.get("app", "")),
            version=str(payload.get("version", "")),
            tracks=tracks,
            content=str(payload.get("content", "")),
            replies=replies,
            files=files,
        )


def apply_update(state: ReleaseState, track: str | None, state_key: str | None) -> ReleaseState:
    """Set ``track`` to ``state_key`` on ``state`` (no-op when track is None). Validates input."""
    if track is None:
        return state
    if track not in TRACKS:
        raise ValueError(f"unknown track {track!r}; expected one of {sorted(TRACKS)}")
    if not state_key or not valid_state(track, state_key):
        valid = [k for k, _ in TRACKS[track]] + [FAILED]
        raise ValueError(f"invalid state {state_key!r} for track {track!r}; expected one of {valid}")
    state.tracks[track] = state_key
    return state
