"""Auto-assignment («autoasignación»): the round-robin configurations of a company (`assignment_config`) and the
history of what assignment-lambda assigned (`assignment_log`, which only the lambda writes). The ports of both.

A configuration is read and written as the row it is stored as (a dict, `_id` as stored): the API answers the row
itself, every field the lambda or an older writer left included, so there is no entity to rebuild it from. The
company goes in the lookup, as it always did (ADR-007 of api-chatty, «la empresa en la consulta»): a row whose
`company_id` is not that text is not found.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol


class AssignmentConfigRepository(Protocol):
    full_name: str
    """Where the rows live (`<database>.assignment_config`), which the list logs."""

    async def count_every_company(self) -> int:
        """How many rows the collection has, of every company and deleted ones too."""
        ...

    async def count_of(self, company_id: str) -> int:
        """How many rows of `company_id`, deleted ones too."""
        ...

    async def live_for_listing(self, company_id: str) -> List[Dict[str, Any]]:
        """The rows of `company_id` whose `deleted_at` is null or missing, as stored, read as the list of `main` did:
        on the `Assignment` logger, INFO «[LIST_CONFIGS] MongoDB query: …», then every row of the company (deleted ones
        too) read and logged as «[LIST_CONFIGS] ALL documents for company (including deleted): …», then the live
        rows read."""
        ...

    async def get(self, company_id: str, config_id: str, *, trace: bool = False) -> Optional[Dict[str, Any]]:
        """The row `config_id` of `company_id`, deleted or not, as stored; None if there is none. Raises if `config_id`
        is not an id. `trace` logs the id it looks for (INFO «[GET_CONFIG_BY_ID] Converted to ObjectId: …» on the
        `Assignment` logger), as the read of one row did."""
        ...

    async def has_company_room(self, company_id: str) -> bool:
        """Whether assignment-lambda finds a configuration for a request of the whole company: a live row without a
        funnel nor an area, in snake_case or in camelCase. Raises if it cannot read."""
        ...

    async def insert(self, fields: Dict[str, Any]) -> Any:
        """Inserts a row with `fields` (the dump of an `AssignmentConfig`, with its dates). Like Mongo, puts the new
        `_id` into `fields` and returns it."""
        ...

    async def overwrite(self, config_id: str, fields: Dict[str, Any]) -> None:
        """Sets `fields` on the row `config_id`, whatever its company (the caller read it first)."""
        ...

    async def mark_deleted(self, config_id: str, deleted_at: datetime) -> int:
        """Sets `deleted_at` on the row `config_id`, whatever its company (the caller read it first); how many rows
        changed."""
        ...


class AssignmentLogReader(Protocol):
    async def count_of(self, company_id: str) -> int:
        """How many assignments of `company_id` the lambda logged (under `room.company_id`, `room.companyId`,
        `company_id` or `companyId`)."""
        ...

    async def newest_of(self, company_id: str, limit: int) -> List[Dict[str, Any]]:
        """Those assignments, newest `created_at` first, at most `limit` (every one if 0), as stored."""
        ...
