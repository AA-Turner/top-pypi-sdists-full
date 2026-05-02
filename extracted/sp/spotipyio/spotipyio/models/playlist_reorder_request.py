from dataclasses import dataclass, asdict


@dataclass
class PlaylistReorderRequest:
    playlist_id: str
    range_start: int
    insert_before: int
    snapshot_id: str
    range_length: int = 1

    def to_payload(self) -> dict:
        payload = asdict(self)
        payload.pop("playlist_id")

        return payload
