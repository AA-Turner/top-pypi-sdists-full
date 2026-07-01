from __future__ import annotations

from typing_extensions import Annotated

from wireup import Inject, injectable

from pet_store_demo_app.services.infra import ShelterStore


@injectable
class AuditService:
    def __init__(
        self,
        shelter_store: ShelterStore,
        event_topic: Annotated[str, Inject(expr="${messaging.events.topic_prefix}-${env.name}")],
    ) -> None:
        self.shelter_store = shelter_store
        self.event_topic = event_topic

    def describe(self) -> dict[str, str]:
        return {"event_topic": self.event_topic}
