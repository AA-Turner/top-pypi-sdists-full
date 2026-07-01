from __future__ import annotations

from typing_extensions import Annotated

from wireup import Inject, injectable

from pet_store_demo_app.services.audit import AuditService
from pet_store_demo_app.services.infra import ShelterStore
from pet_store_demo_app.services.pets import PetCatalogService
from pet_store_demo_app.services.session import SQLAlchemySession


@injectable(lifetime="scoped")
class AdoptionService:
    def __init__(
        self,
        catalog: PetCatalogService,
        audit: AuditService,
        shelter_store: ShelterStore,
        session: SQLAlchemySession,
        adoption_queue: Annotated[str, Inject(expr="${messaging.events.topic_prefix}-${pets.default_species}")],
    ) -> None:
        self.catalog = catalog
        self.audit = audit
        self.shelter_store = shelter_store
        self.session = session
        self.adoption_queue = adoption_queue

    def preview(self, pet_id: str) -> dict[str, object]:
        return {
            "pet": self.catalog.pet_detail(pet_id),
            "queue": self.adoption_queue,
            "audit_topic": self.audit.event_topic,
            "session": self.session.describe(),
        }
