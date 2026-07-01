from __future__ import annotations

from typing_extensions import Annotated

from wireup import Inject, injectable

from pet_store_demo_app.factories import SearchClient
from pet_store_demo_app.services.audit import AuditService
from pet_store_demo_app.services.infra import ShelterStore


@injectable
class PetCatalogService:
    def __init__(
        self,
        shelter_name: Annotated[str, Inject(config="pets.store_name")],
        search: SearchClient,
        shelter_store: ShelterStore,
        audit: AuditService,
        featured_tag: Annotated[str, Inject(expr="${env.name}-${pets.default_species}")],
    ) -> None:
        self.shelter_name = shelter_name
        self.search = search
        self.shelter_store = shelter_store
        self.audit = audit
        self.featured_tag = featured_tag

    def list_pets(self) -> dict[str, object]:
        return {
            "shelter": self.shelter_name,
            "featured_tag": self.featured_tag,
            "search": self.search.describe(),
            "audit_topic": self.audit.event_topic,
        }

    def pet_detail(self, pet_id: str) -> dict[str, object]:
        return {
            "pet_id": pet_id,
            "shelter": self.shelter_name,
            "store": self.shelter_store.describe(),
        }
