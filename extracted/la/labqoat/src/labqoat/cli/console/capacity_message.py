"""Concise capacity waiting reasons from retained admission evidence."""

from typing import ClassVar

from labqoat.json_document import JsonDocument


class CapacityMessage:
    """Keep provider quota, administrator limits and automatic capacity waits distinct."""

    reasons: ClassVar[dict[str, str]] = {
        "worker_limit": "Waiting for group capacity",
        "spend_limit": "Waiting for spend allowance",
        "quota_insufficient": "Waiting for provider quota",
        "quota_unknown": "Provider quota is unknown",
        "location_paused": "Location paused",
        "acquiring": "Acquiring a machine",
        "acquisition_limit": "Launch lanes busy",
        "launch_failed": "Machine launch failed",
        "parent_retains_capacity": "Waiting for parent capacity release",
        "cleanup_pending": "Waiting for cleanup",
        "pool_full": "Waiting for a free container in this function's pool",
        "pool_inactive": "This function's pool is not starting containers",
        "no_matching_hardware": "No machine fits this request; change cpu, memory, gpu or location (see `lab compute offerings`)",
    }

    @staticmethod
    def describe(data: JsonDocument) -> str:
        """Report measured dimensions and retry ownership without inventing a quota value."""
        code = str(data.get("code", "capacity"))
        title = CapacityMessage.reasons.get(code, code.replace("_", " ").capitalize())
        values = [
            f"{key}={data[key]}"
            for key in ("family", "dimension", "held", "cleaning", "requested", "limit", "location_id", "error")
            if data.get(key) is not None
        ]
        resolution = data.get("resolution")
        if resolution in ("administrator", "provider"):
            values.append(f"needs {resolution} action")
        return " · ".join([title, *values])
