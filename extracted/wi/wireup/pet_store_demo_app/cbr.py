from __future__ import annotations

from typing import Any

import fastapi
import wireup

from pet_store_demo_app.services.adoption import AdoptionService
from pet_store_demo_app.services.audit import AuditService
from pet_store_demo_app.services.session import SQLAlchemySession


class DemoClassBasedHandler:
    router = fastapi.APIRouter(prefix="/class-based")

    def __init__(self, audit_service: AuditService) -> None:
        self.audit_service = audit_service

    @router.get("/overview")
    async def overview(
        self,
        adoption_service: wireup.Injected[AdoptionService],
        session: wireup.Injected[SQLAlchemySession],
    ) -> dict[str, Any]:
        return {
            "adoption_preview": adoption_service.preview("class-based-pet"),
            "audit_topic": self.audit_service.event_topic,
            "session": session.describe(),
        }

    @router.get("/no-scoped-deps")
    async def no_scoped_deps(self) -> dict[str, Any]:
        return {}
