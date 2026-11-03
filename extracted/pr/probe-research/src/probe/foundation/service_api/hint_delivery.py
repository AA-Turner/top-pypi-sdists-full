"""Whether the hints the Probe service posts reach a session's agent: the `delivery_receipt` state.
Stdlib only: the service's start path, the mailbox reader and `probe status` read it."""

from __future__ import annotations


class DeliveryState:
    """Whether the hints posted to a session reach its agent (`delivery_receipt`)."""

    OK = "ok"  # a deliverer is there (its heartbeat), or a hint was shown lately
    UNPROVEN = "unproven"  # neither yet: the session's reader keeps its prompt turns and check-ins
    UNDELIVERABLE = "undeliverable"  # hints posted here keep missing chances to be shown
