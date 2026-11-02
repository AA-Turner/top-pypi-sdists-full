"""Custom capacities (`capacidades`): the port every capacity store implements.

A capacity is its own aggregate (staff gives it to a company; the company picks it in the motivo's action selector).
The entity is `letschatty.models.company.assets.atencion.capacidad.Capacidad`, unchanged. Stored documents are read and
returned raw (as stored, `_id` included) because cintia-lambdas reads the same collection directly and the list shows
whatever is stored. The company is part of every query (api-chatty ADR-007, «la empresa en la consulta»): there is no
read by id that checks the company afterwards, and a capacity of another company is simply not found.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

from ...models.company.assets.atencion.capacidad import Capacidad


class CapacityRepository(Protocol):
    async def list_live(self, company_id: str) -> List[Dict[str, Any]]:
        """The company's capacities without `deleted_at`, raw, oldest first (`created_at`)."""
        ...

    async def add(self, capacity: Capacidad) -> Dict[str, Any]:
        """Stores it and returns the stored document (with its `_id`)."""
        ...

    async def find_live(self, company_id: str, capacity_id: str) -> Optional[Dict[str, Any]]:
        """The company's live capacity, raw; None if there is none (another company's, deleted or unknown id)."""
        ...

    async def set_fields(self, company_id: str, capacity_id: str, fields: Dict[str, Any]) -> None:
        """`$set` on that capacity of the company, deleted or not."""
        ...

    async def soft_delete(self, company_id: str, capacity_id: str, now: datetime) -> bool:
        """One conditional write: sets `deleted_at` and `activa: false` on the company's live capacity. False when
        it matched nothing."""
        ...
