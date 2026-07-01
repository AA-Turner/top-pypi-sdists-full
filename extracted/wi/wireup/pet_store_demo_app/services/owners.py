from __future__ import annotations

from wireup import injectable

from pet_store_demo_app.services.audit import AuditService
from pet_store_demo_app.services.infra import ShelterStore
from pet_store_demo_app.services.session import SQLAlchemySession


@injectable(lifetime="scoped")
class OwnerService:
    def __init__(
        self,
        shelter_store: ShelterStore,
        audit: AuditService,
        session: SQLAlchemySession,
    ) -> None:
        self.shelter_store = shelter_store
        self.audit = audit
        self.session = session

    def summary(self, owner_id: str) -> dict[str, object]:
        return {
            "owner_id": owner_id,
            "store": self.shelter_store.describe(),
            "audit_topic": self.audit.event_topic,
            "session": self.session.describe(),
        }
