"""
Demonstrates the smplkit SDK for Smpl Audit.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/audit_showcase.py
"""

import asyncio
import uuid
from datetime import datetime, timezone

from smplkit import AsyncSmplClient
from smplkit.audit import (
    ForwarderType,
    HttpConfiguration,
    HttpMethod,
    TransformType,
)

from setup.audit_setup import cleanup_showcase, setup_showcase


# JSON Logic filter — only forward ``invoice.*`` actions. Events that don't
# match the filter aren't forwarded (and produce no delivery record).
# See https://jsonlogic.com for the full operator reference.
INVOICE_FILTER = {"in": ["invoice.", {"var": "action"}]}

# JSONata template — reshape the event payload before POSTing to the
# destination. This example flattens the event into a compact SIEM-style
# record. See https://jsonata.org for the full language reference.
SIEM_TRANSFORM = """
{
    "event": action,
    "subject": resource_type & ":" & resource_id,
    "ts": occurred_at,
    "actor": actor_label
}
"""


async def main() -> None:

    # or SmplClient for synchronous use
    async with AsyncSmplClient() as client:
        await setup_showcase(client)
        some_resource_id = f"showcase-{uuid.uuid4().hex[:8]}"

        # ----- Events: record / list / get --------------------------------

        # record an event
        await client.audit.events.record(
            actor_id="billing-bot:42",
            actor_label="finance@example.com",
            actor_type="USER",
            category="billing",
            data={
                "snapshot": {"total_cents": 4900, "currency": "USD"},
                "request_id": "req-abc",
            },
            event_type="invoice.created",
            flush=True,  # or omit to have events flushed asynchronously
            occurred_at=datetime.now(timezone.utc),
            resource_id=some_resource_id,
            resource_type="invoice",
        )
        print(f"Recorded event for invoice {some_resource_id}")

        # list events
        page = await client.audit.events.list(
            resource_type="invoice", resource_id=some_resource_id
        )
        assert some_resource_id in {e.resource_id for e in page.events}
        recorded_event_id = page.events[0].id
        print(f"Listed {len(page)} event(s) for invoice {some_resource_id}")

        # fetch an event
        event = await client.audit.events.get(recorded_event_id)
        assert event.id == recorded_event_id
        assert event.resource_id == some_resource_id
        assert event.event_type == "invoice.created"
        assert event.actor_id == "billing-bot:42"
        assert event.actor_label == "finance@example.com"
        assert event.category == "billing"
        print(
            f"Fetched event {event.id}: {event.event_type} "
            f"by {event.actor_label} in {event.environment}"
        )

        # ----- Discovery: distinct resource_types / event_types / categories

        resource_types = await client.audit.resource_types.list()
        assert "invoice" in {rt.id for rt in resource_types}
        print(f"Observed resource types: {[rt.id for rt in resource_types]}")

        event_types = await client.audit.event_types.list()
        assert "invoice.created" in {et.id for et in event_types}
        print(f"Observed event types: {[et.id for et in event_types]}")

        categories = await client.audit.categories.list()
        assert "billing" in {c.id for c in categories}
        print(f"Observed categories: {[c.id for c in categories]}")

        # ----- Forwarders: SIEM streaming CRUD ----------------------------

        forwarder_id = "showcase-forwarder"

        try:
            # create a forwarder
            forwarder = client.audit.forwarders.new(
                forwarder_id,
                configuration=HttpConfiguration(
                    headers={"X-Showcase": "ok"},
                    method=HttpMethod.POST,
                    url="https://example.com",
                ),
                filter=INVOICE_FILTER,
                forwarder_type=ForwarderType.HTTP,
                transform=SIEM_TRANSFORM,
                transform_type=TransformType.JSONATA,
            )
            await forwarder.save()
            print(f"Created forwarder: {forwarder.name} (id={forwarder.id})")

            # list forwarders
            listed = await client.audit.forwarders.list()
            assert forwarder.id in {f.id for f in listed.forwarders}
            print(f"Account has {len(listed.forwarders)} forwarder(s)")

            # get a forwarder
            forwarder = await client.audit.forwarders.get(forwarder_id)
            print(f"Fetched forwarder: {forwarder.name} (id={forwarder.id})")
            assert forwarder.id == forwarder_id

            # configure where to forward events in production
            forwarder.environment("production").url = "https://httpbin.org/post"
            forwarder.environment("production").set_header("X-Showcase", "ok")
            await forwarder.save()
            assert (
                forwarder.environments["production"].url == "https://httpbin.org/post"
            )
            print(f"Updated forwarder: {forwarder.name}")

            # start forwarding events in production
            forwarder.environment("production").enabled = True
            await forwarder.save()
            print(
                f"Enabled forwarder {forwarder.name} (id={forwarder.id}) "
                "to start forwarding events in production"
            )

            # delete a forwarder
            await forwarder.delete()
            remaining = await client.audit.forwarders.list()
            assert forwarder_id not in {f.id for f in remaining.forwarders}
            print(f"Deleted forwarder: {forwarder.name}")
        finally:
            await cleanup_showcase(client)

        print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
