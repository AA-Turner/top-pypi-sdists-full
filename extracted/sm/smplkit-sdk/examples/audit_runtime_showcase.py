"""
Demonstrates the smplkit runtime SDK for Smpl Audit.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/audit_runtime_showcase.py
"""

import asyncio
import uuid
from datetime import datetime, timezone

from smplkit import AsyncSmplClient


async def main() -> None:

    # create the client (use SmplClient for synchronous use)
    async with AsyncSmplClient(
        environment="production", service="showcase-service"
    ) as client:
        some_resource_id = f"showcase-{uuid.uuid4().hex[:8]}"

        # record an event with full customer-supplied actor attribution
        client.audit.events.record(
            event_type="invoice.created",
            resource_type="invoice",
            resource_id=some_resource_id,
            occurred_at=datetime.now(timezone.utc),
            actor_type="USER",
            actor_id="billing-bot:42",
            actor_label="finance@example.com",
            data={
                "snapshot": {"total_cents": 4900, "currency": "USD"},
                "request_id": "req-abc",
            },
            flush=True,  # or omit to have events flushed asynchronously
        )
        print(f"Recorded events for invoice {some_resource_id}")

        # list events
        page = client.audit.events.list(
            resource_type="invoice", resource_id=some_resource_id
        )
        assert some_resource_id in {e.resource_id for e in page.events}
        recorded_event_id = page.events[0].id
        print(f"Listed {len(page)} event(s) for invoice {some_resource_id}")

        # fetch an event
        event = client.audit.events.get(recorded_event_id)
        assert event.id == recorded_event_id
        assert event.resource_id == some_resource_id
        assert event.event_type == "invoice.created"
        assert event.actor_id == "billing-bot:42"
        assert event.actor_label == "finance@example.com"
        print(
            f"Fetched event {event.id}: {event.event_type} by {event.actor_label}"
        )

        # list resource types observed
        resource_types = client.audit.resource_types.list()
        assert "invoice" in {rt.id for rt in resource_types}
        print(f"Observed resource types: {[rt.id for rt in resource_types]}")

        # list event types observed
        event_types = client.audit.event_types.list()
        assert "invoice.created" in {et.id for et in event_types}
        print(f"Observed event types: {[et.id for et in event_types]}")

        print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
