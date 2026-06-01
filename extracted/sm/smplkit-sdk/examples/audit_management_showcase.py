"""
Demonstrates the smplkit management SDK for Smpl Audit.

Prerequisites:
    - ``pip install smplkit-sdk``
    - A valid smplkit API key, provided via one of:
        - ``SMPLKIT_API_KEY`` environment variable
        - ``~/.smplkit`` configuration file (see SDK docs)

Usage::

    python examples/audit_management_showcase.py
"""

import uuid

from smplkit import SmplManagementClient
from smplkit.audit import (
    ForwarderType,
    HttpConfiguration,
    HttpHeader,
    HttpMethod,
    TransformType,
)


# JSON Logic filter — only forward ``invoice.*`` actions.
# Events that don't match are recorded as ``filtered_out`` deliveries.
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


def main() -> None:

    # create the client (use AsyncSmplManagementClient for asynchronous use)
    with SmplManagementClient() as manage:
        forwarder_id = f"showcase-{uuid.uuid4().hex[:6]}"

        # create a new forwarder
        forwarder = manage.audit.forwarders.new(
            forwarder_id,
            forwarder_type=ForwarderType.HTTP,
            configuration=HttpConfiguration(
                method=HttpMethod.POST,
                url="https://httpbin.org/post",
                headers=[HttpHeader(name="X-Showcase", value="ok")],
            ),
            filter=INVOICE_FILTER,
            transform=SIEM_TRANSFORM,
            transform_type=TransformType.JSONATA,
        )
        forwarder.save()
        print(f"Created forwarder: {forwarder.name} (id={forwarder.id})")

        # list forwarders
        listed = manage.audit.forwarders.list()
        assert forwarder.id in {f.id for f in listed.forwarders}
        print(f"Account has {len(listed.forwarders)} forwarder(s)")

        # get a forwarder
        fetched = manage.audit.forwarders.get(forwarder.id)
        assert fetched.id == forwarder.id
        assert fetched.enabled is True
        print(f"Fetched forwarder: {fetched.name}")

        # update a forwarder
        fetched.enabled = False
        fetched.save()
        assert fetched.enabled is False
        print(
            f"Disabled forwarder: {fetched.name} (enabled={fetched.enabled})"
        )

        # delete a forwarder
        fetched.delete()
        remaining = manage.audit.forwarders.list()
        assert fetched.id not in {f.id for f in remaining.forwarders}
        print(f"Deleted forwarder: {fetched.name}")

        print("Done!")


if __name__ == "__main__":
    main()
