from __future__ import annotations

from typing import Protocol

from typing_extensions import Annotated

from wireup import Inject, injectable

from pet_store_demo_app.services.infra import ShelterStore


class AuditService(Protocol):
    event_topic: str

    def describe(self) -> dict[str, str]: ...


@injectable(as_type=AuditService)
class EventAuditService:
    def __init__(
        self,
        shelter_store: ShelterStore,
        event_topic: Annotated[str, Inject(expr="${messaging.events.topic_prefix}-${env.name}")],
    ) -> None:
        self.shelter_store = shelter_store
        self.event_topic = event_topic

    def describe(self) -> dict[str, str]:
        return {"backend": "event-log", "event_topic": self.event_topic}


@injectable(as_type=AuditService, qualifier="compliance")
class ComplianceAuditService:
    def __init__(
        self,
        shelter_store: ShelterStore,
        event_topic: Annotated[str, Inject(expr="${messaging.events.topic_prefix}-compliance")],
    ) -> None:
        self.shelter_store = shelter_store
        self.event_topic = event_topic

    def describe(self) -> dict[str, str]:
        return {"backend": "compliance", "event_topic": self.event_topic}
