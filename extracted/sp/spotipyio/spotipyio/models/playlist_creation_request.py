from dataclasses import dataclass


@dataclass
class PlaylistCreationRequest:
    user_id: str
    name: str
    description: str
    public: bool

    def to_payload(self) -> dict:
        return {"name": self.name, "description": self.description, "public": self.public}
