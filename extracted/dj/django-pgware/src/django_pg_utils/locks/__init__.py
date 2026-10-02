from django_pg_utils.locks._async import async_advisory_lock
from django_pg_utils.locks._sync import advisory_lock

__all__ = ["advisory_lock", "async_advisory_lock"]
